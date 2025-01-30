import datetime

from baseintegration.exporter import BaseProcessor
from inforvisual.models import WorkOrder, Operation, ShopResource, Part, OperationBinary, Vendor, Service
from paperless.objects.orders import Order, OrderComponent, OrderOperation
from baseintegration.datamigration import logger
from inforvisual.exporter.utils import WorkOrderData, OperationData


class OperationProcessor(BaseProcessor):

    def _process(self, order: Order, work_orders: list) -> list:
        logger.info("Processing operations")
        self.order = order
        self.created_operations = []
        for w_order in work_orders:
            w_order: WorkOrderData = w_order
            part_object: Part = w_order.work_order.part
            part_is_new: bool = w_order.part_is_new
            logger.info(f"Checking whether we need to add operations for {part_object.id}")
            if part_is_new:
                self.get_operations(w_order)
            else:
                logger.info(f"Part {part_object.id} is not new, skipping adding operations")
        return self.created_operations

    def get_operations(self, w_order: WorkOrderData):
        order_obj: WorkOrder = w_order.work_order
        component: OrderComponent = w_order.component
        operations: list = component.shop_operations
        if len(operations) > 0:
            self.create_operations(operations, component, order_obj)
        else:
            pass

    def get_bur_percent_run(self, operation: OrderOperation):
        for var in operation.costing_variables:
            if "burden percent run" in var.label.lower():
                return var.value
        else:
            return 0

    def get_bur_percent_setup(self, operation):
        for var in operation.costing_variables:
            if "burden percent setup" in var.label.lower():
                return var.value
        else:
            return 0

    def get_setup_cost_per_hr(self, operation):
        for var in operation.costing_variables:
            if "setup cost" in var.label.lower():
                return var.value
        else:
            return 0

    def get_run_cost_per_hr(self, operation):
        for var in operation.costing_variables:
            if "run cost" in var.label.lower():
                return var.value
        else:
            return 0

    def get_resource_id(self, operation: OrderOperation):
        return operation.get_variable(self._exporter.erp_config.vendor_variable)

    def create_operations(self, operations, component, order_obj: WorkOrder):
        sequence_no = 10
        logger.info(f"Processing operations for {str(component.part_number)}")
        for operation in operations:
            operation: OrderOperation = operation
            logger.info(f"Operations being processed for operation {operation.name}")
            resource_id: str = self.get_resource_id(operation)
            if not resource_id:
                resource_id = operation.name
            resource: ShopResource = self.get_resource(resource_id)
            if not resource:
                logger.info("Resource ID not found on operation. Must be an informational operation. Skipping and "
                            "going to the next one")
                continue

            if operation.is_outside_service:
                infor_operation = self.create_outside_service_operation(operation=operation, resource=resource,
                                                                        order_obj=order_obj, sequence_no=sequence_no)
            else:
                infor_operation = self.create_inside_service_operation(operation=operation, resource=resource,
                                                                       order_obj=order_obj, sequence_no=sequence_no)
            self.created_operations.append(OperationData(operation=infor_operation, component=component))
            sequence_no += 10

    def create_inside_service_operation(self, operation: OrderOperation, resource: ShopResource, order_obj: WorkOrder,
                                        sequence_no: int):

        setup_time = operation.setup_time if operation.setup_time else 0
        runtime = operation.runtime if operation.runtime else 0
        setup_hrs: float = round(setup_time, 2)
        run: float = round(runtime, 2)
        try:
            move_hrs = int(resource.user_4)
        except:
            move_hrs = 0
        run_hrs = run * order_obj.desired_qty
        op = Operation(
            workorder_type=order_obj.type,
            workorder_base=order_obj.base_id,
            workorder_lot=order_obj.lot_id,
            workorder_split=order_obj.split_id,
            workorder_sub=order_obj.sub_id,
            run_type="HRS/PC",
            move_hrs=move_hrs,
            resource=resource,
            sequence_no=sequence_no,
            setup_hrs=setup_hrs,
            run=run,
            run_hrs=run_hrs,
            fixed_scrap_units=0,
            calc_start_qty=order_obj.desired_qty,
            calc_end_qty=order_obj.desired_qty,
            status="U",
            setup_completed="N",
            override_qtys="N",
            begin_traceability="N",
            isdeterminant="N",
            scrap_yield_type="S",
            run_cost_per_hr=self.get_run_cost_per_hr(operation),
            setup_cost_per_hr=self.get_setup_cost_per_hr(operation),
            bur_percent_setup=self.get_bur_percent_setup(operation),
            bur_percent_run=self.get_bur_percent_run(operation),
            protect_cost="N",
            overlap_setup="N",
            setup_inspect_req="N",
            run_inspect_req="N",
            dispatch_sequence="99999",
            status_eff_date=datetime.datetime.now(),
            site_id=self._exporter.erp_config.default_site_id
        )
        op.save()
        self.create_operation_binary(operation, order_obj, sequence_no)
        logger.info(f"Op {operation.name} with base id {order_obj.base_id} has been created")
        return op

    def create_operation_binary(self, paperless_operation: OrderOperation, order_obj: WorkOrder,
                                sequence_no) -> OperationBinary:

        operation_notes = paperless_operation.notes
        if not operation_notes:
            return

        logger.info(
            f'Attempting to create operation binary for Paperless Operation {paperless_operation.operation_definition_name} '
            f'and infor op {sequence_no}')

        bits = operation_notes.encode('utf-16-le')
        bits_length = len(bits)

        op_binary = OperationBinary(
            workorder_type=order_obj.type,
            workorder_base=order_obj.base_id,
            workorder_lot=order_obj.lot_id,
            workorder_split=order_obj.split_id,
            workorder_sub=order_obj.sub_id,
            sequence_no=sequence_no,
            type='D',  # TODO
            bits=bits,
            bits_length=bits_length,
        )
        op_binary.save()
        logger.info('Saved operation binary')

    def create_outside_service_operation(self, operation: OrderOperation, resource: ShopResource, order_obj: WorkOrder,
                                         sequence_no: int):

        vendor_id = operation.get_variable(self._exporter.erp_config.vendor_id_var)
        service_id = operation.get_variable(self._exporter.erp_config.service_id_var)
        service_min_chg = operation.get_variable(self._exporter.erp_config.service_min_chg_var)
        run_cost_per_unit = operation.get_variable(self._exporter.erp_config.run_cost_per_unit_var)
        lead_days = operation.get_variable(self._exporter.erp_config.transit_days_var)
        service_base_chg = 0
        notes = operation.notes[0:80] if operation.notes else ''
        does_service_id_exist = self.check_service_id_exists(service_id=service_id)
        does_vendor_id_exist = self.check_vendor_id_exists(vendor_id=vendor_id)
        outside_resource = self.get_resource(resource_id=service_id)
        if not outside_resource:
            outside_resource = resource

        op = Operation(
            service_id=service_id if does_service_id_exist else None,
            vendor_id=vendor_id if does_vendor_id_exist else None,
            vendor_service_id=None,
            service_base_chg=service_base_chg or 0,
            service_min_chg=service_min_chg or 0,
            run_cost_per_unit=run_cost_per_unit or 0,
            service_part_id=order_obj.base_id,
            workorder_type=order_obj.type,
            workorder_base=order_obj.base_id,
            workorder_lot=order_obj.lot_id,
            workorder_split=order_obj.split_id,
            workorder_sub=order_obj.sub_id,
            transit_days=lead_days,
            run_type="HRS/PC",
            resource=outside_resource,
            sequence_no=sequence_no,
            fixed_scrap_units=0,
            calc_start_qty=order_obj.desired_qty,
            calc_end_qty=order_obj.desired_qty,
            status="U",
            setup_completed="N",
            override_qtys="N",
            begin_traceability="N",
            isdeterminant="N",
            scrap_yield_type="S",
            protect_cost="N",
            overlap_setup="N",
            setup_inspect_req="N",
            run_inspect_req="N",
            dispatch_sequence="99999",
            status_eff_date=datetime.datetime.now(),
            site_id=self._exporter.erp_config.default_site_id,
            user_1=notes,
        )
        op.save()
        self.create_operation_binary(operation, order_obj, sequence_no)
        logger.info(f"Op {operation.name} with base id {order_obj.base_id} has been created")
        return op

    def get_resource(self, resource_id: str):
        logger.info("Attempting to get resource out of the table")
        resource = ShopResource.objects.filter(id=resource_id).first()
        if not resource:
            resource = ShopResource.objects.filter(id="PPDEFAULT").first()
        return resource

    @staticmethod
    def check_service_id_exists(service_id: str) -> bool:
        service = Service.objects.filter(id=service_id).first()
        if service:
            return True
        logger.info(f'Service ID: {service_id} does not exist in InforVisual')
        return False

    @staticmethod
    def check_vendor_id_exists(vendor_id: str) -> bool:
        vendor = Vendor.objects.filter(id=vendor_id).first()
        if vendor:
            return True
        logger.info(f'Vendor ID: {vendor_id} does not exist in InforVisual')
        return False
