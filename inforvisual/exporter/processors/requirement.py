import datetime
from typing import List

from paperless.objects.orders import Order, OrderComponent, OrderOperation

from baseintegration.datamigration import logger
from baseintegration.exporter import BaseProcessor
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException

from inforvisual.models import Part, Requirement, WorkOrder
from inforvisual.exporter.utils import WorkOrderData, PurchasedComponentData, MaterialData


class RequirementProcessor(BaseProcessor):

    def _process(self, order: Order, work_orders: list, purchased_components: list, materials: list) -> list:
        logger.info("Creating requirements")
        logger.info(f"Number of work orders is {str(len(work_orders))}")

        self.order = order
        self.work_orders = work_orders
        self.requirements = []

        # We iterate over all work orders but only process work orders of root components.
        for w_order in self.work_orders:
            piece_no = 10
            w_order: WorkOrderData = w_order
            part_object: Part = w_order.work_order.part
            part_is_new: bool = w_order.part_is_new

            # check if part is a new root component. Otherwise, skip adding children, purchased components and
            # materials.
            if w_order.component.is_root_component:
                if part_is_new:
                    logger.info(f"Root component {part_object.id} is new, adding requirements for that part")
                    self.add_sub_work_orders(w_order, piece_no, materials, purchased_components)
                else:
                    logger.info(f"Root component {part_object.id} is not new, not adding requirements for that part")

        return self.requirements

    def add_purchased_components(self, w_order: WorkOrderData, purchased_components: List[PurchasedComponentData],
                                 piece_no):
        logger.info(f"Adding purchased components to {w_order.component.part_number}"
                    f" with piece no {piece_no}")

        w_order_obj: WorkOrder = w_order.work_order
        if self._exporter.erp_config.should_export_assemblies_with_duplicate_components:
            for p in w_order.child_data.child_purchased_components:
                piece_no = self.add_purchased_component(
                    purchased_component_data=p,
                    w_order_obj=w_order_obj,
                    piece_no=piece_no,
                    quantity_per_parent=p.quantity_per_parent,
                    deliver_quantity=p.deliver_quantity
                )
        else:
            w_order_component: OrderComponent = w_order.component
            for p in purchased_components:
                p_component: OrderComponent = p.component
                if len(p_component.parent_ids) == 1 and p_component.parent_ids[0] == w_order_component.id:
                    piece_no = self.add_purchased_component(
                        purchased_component_data=p,
                        w_order_obj=w_order_obj,
                        piece_no=piece_no,
                        quantity_per_parent=p_component.innate_quantity,
                        deliver_quantity=p_component.deliver_quantity
                    )
        return piece_no

    def add_purchased_component(self, purchased_component_data: PurchasedComponentData, w_order_obj: WorkOrder,
                                piece_no: int, quantity_per_parent: int, deliver_quantity: int):
        part = purchased_component_data.part
        self.verify_first_op_exists(w_order_obj.base_id, w_order_obj.sub_id)
        req = Requirement(
            workorder_type=w_order_obj.type,
            workorder_base=w_order_obj.base_id,
            workorder_lot=w_order_obj.lot_id,
            workorder_split=w_order_obj.split_id,
            workorder_sub=w_order_obj.sub_id,
            operation_seq_no=10,
            piece_no=piece_no,
            part_id=part.id,
            status="U",
            qty_per=quantity_per_parent,
            qty_per_type="S",
            calc_qty=deliver_quantity,
            site_id=self._exporter.erp_config.default_site_id,
            protect_cost="N",
            status_eff_date=datetime.datetime.now()
        )
        try:
            req.save()
            self.requirements.append(req)
            piece_no = piece_no + 10
            logger.info(f"Added sub work order requirement of {w_order_obj.part.id} "
                        f"for purchased component {part.id}")
        except Exception as e:
            logger.error(f'Error saving purchased component requirement: \n\n {e}')
            raise CancelledIntegrationActionException(f"Error adding sub work order requirement of "
                                                      f"{w_order_obj.part.id} for purchased component "
                                                      f"{part.id}")
        return piece_no

    def add_sub_work_orders(self, w_order: WorkOrderData, piece_no: int, materials: [MaterialData],
                            purchased_components: [PurchasedComponentData]):

        logger.info(f"Adding sub work orders requirements for {w_order.work_order.part}. ")

        w_order_obj: WorkOrder = w_order.work_order
        w_order_component: OrderComponent = w_order.component

        piece_no = self.add_materials(w_order, materials, piece_no)

        if len(w_order_component.child_ids) == 0:
            return
        else:

            piece_no = self.add_purchased_components(w_order, purchased_components, piece_no)

            child_work_orders: list = self.get_child_work_orders(w_order)
            for child in child_work_orders:
                child: WorkOrderData = child
                child_work_order_obj: WorkOrder = child.work_order
                child_component = child.component

                if self._exporter.erp_config.leg_assembly:
                    part_id = None
                    sub_wo_sub_id = child_work_order_obj.sub_id
                else:
                    part_id = child_work_order_obj.part.id
                    sub_wo_sub_id = None

                self.verify_first_op_exists(w_order_obj.base_id, w_order_obj.sub_id)
                quantity_per_parent = child.quantity_per_parent \
                    if self._exporter.erp_config.should_export_assemblies_with_duplicate_components \
                    else child_component.innate_quantity
                req = Requirement(
                    workorder_type=w_order_obj.type,
                    workorder_base=w_order_obj.base_id,
                    workorder_lot=w_order_obj.lot_id,
                    workorder_split=w_order_obj.split_id,
                    workorder_sub=w_order_obj.sub_id,
                    part_id=part_id,
                    subord_wo_sub=sub_wo_sub_id,
                    operation_seq_no=10,
                    piece_no=piece_no,
                    status="U",
                    qty_per=quantity_per_parent,
                    qty_per_type="S",
                    est_material_cost=0,
                    site_id=self._exporter.erp_config.default_site_id,
                    protect_cost="N",
                    status_eff_date=datetime.datetime.now()
                )

                try:
                    req.save()
                    self.requirements.append(req)
                    piece_no = piece_no + 10
                    logger.info(f"Added sub work order requirement of {w_order_obj.part.id} "
                                f"for child {child_component.part_number}")
                except Exception as e:
                    logger.error(f'Error saving child requirement: \n\n {e}')
                    raise CancelledIntegrationActionException(f'Error saving raw material requirement of'
                                                              f'{w_order.component.part_number} for child component '
                                                              f'{part_id}')

                # We reset piece number to 10 as we descend to each level of the BOM.
                self.add_sub_work_orders(child, 10, materials, purchased_components)
        return piece_no

    def add_materials(self, w_order: WorkOrderData, materials: [MaterialData], piece_no: int):

        logger.info(f"Adding raw materials to sub work order {w_order.component.part_number}")
        w_order_obj: WorkOrder = w_order.work_order
        w_order_component: OrderComponent = w_order.component

        for material in materials:
            material: MaterialData = material
            material_parent_component: OrderComponent = material.part_data.component
            if w_order_component.id == material_parent_component.id:
                part: Part = material.part_data.part
                material_operation: OrderOperation = material.material_op

                self.verify_first_op_exists(w_order_obj.base_id, w_order_obj.sub_id)

                deliver_quantity = w_order.deliver_quantity \
                    if self._exporter.erp_config.should_export_assemblies_with_duplicate_components \
                    else self.get_material_quantity(material_operation)
                req = Requirement(
                    workorder_type=w_order_obj.type,
                    workorder_base=w_order_obj.base_id,
                    workorder_lot=w_order_obj.lot_id,
                    workorder_split=w_order_obj.split_id,
                    workorder_sub=w_order_obj.sub_id,
                    operation_seq_no=10,
                    piece_no=piece_no,
                    part_id=part.id,
                    status="U",
                    calc_qty=deliver_quantity,
                    qty_per=self.get_material_qty_per(material_operation),
                    qty_per_type="S",
                    protect_cost="N",
                    unit_material_cost=self.get_unit_material_cost(material_operation),
                    site_id=self._exporter.erp_config.default_site_id,
                    status_eff_date=datetime.datetime.now()
                )

                try:
                    req.save()
                    self.requirements.append(req)
                    piece_no = piece_no + 10
                except Exception as e:
                    logger.error(f'Error saving raw material requirement: \n\n {e}')
                    raise CancelledIntegrationActionException(f'Error saving raw material requirement of'
                                                              f'{w_order.component.part_number} for raw material '
                                                              f'{part.id}')
        return piece_no

    def get_child_work_orders(self, w_order: WorkOrderData) -> list:
        if self._exporter.erp_config.should_export_assemblies_with_duplicate_components:
            return w_order.child_data.child_work_orders

        child_work_orders = []
        w_order_component: OrderComponent = w_order.component
        for child in w_order_component.child_ids:
            for sub_w_order in self.work_orders:
                sub_w_order: WorkOrderData = sub_w_order
                sub_work_order_component: OrderComponent = sub_w_order.component
                if child == sub_work_order_component.id:
                    child_work_orders.append(sub_w_order)
        return child_work_orders

    def get_material_qty_per(self, material_operation: OrderOperation) -> float:
        try:
            x = round((1 / material_operation.get_variable(
                self._exporter.erp_config.pp_parts_per_material_unit_variable)), 3)
            return x
        except Exception as e:
            logger.error(f'Error getting material qty per: \n\n {e}')
            return 1

    def get_unit_material_cost(self, material_operation: OrderOperation) -> float:
        if len(material_operation.quantities) > 0:
            return float(material_operation.cost.dollars / material_operation.quantities[0].quantity)
        else:
            return 0

    def get_material_quantity(self, material_operation: OrderOperation) -> int:
        if len(material_operation.quantities) > 0:
            return material_operation.quantities[0].quantity
        else:
            return 0

    def verify_first_op_exists(self, base_id, sub_id):
        if not self._exporter._integration.test_mode:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM OPERATION WHERE WORKORDER_BASE_ID = %s AND WORKORDER_SUB_ID = %s AND "
                               "SEQUENCE_NO = 10", [base_id, sub_id])
                row = cursor.fetchone()
                if not row:
                    self._exporter.send_email(subject=f"Order {self.order.number} failed to process",
                                              body=f"Order {self.order.number} failed to process because we attempted "
                                              f"to add either a material or purchased component for a parent "
                                              f"component with no operations. Please check the routing on the "
                                              f"Paperless Parts order item has at least one operation which maps"
                                              f" to Infor Visual")
                    if not self._exporter._integration.test_mode:
                        raise ValueError(f"Order {self.order.number} attempted to create requirement without a matching"
                                         f" op")
