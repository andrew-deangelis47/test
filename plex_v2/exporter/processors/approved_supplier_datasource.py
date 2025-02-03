from plex_v2.exporter.processors.base import PlexProcessor
from paperless.objects.orders import Order, OrderItem, OrderOperation, OrderComponent
from plex_v2.factories.plex.approved_supplier_datasource import ApprovedSupplierDatasourceFactory
from plex_v2.objects.approved_supplier_upload_datasource import ApprovedSupplierAddUpdateDatasource
from typing import List
from plex_v2.objects.operations_mapping import OperationsMapping
from plex_v2.utils.export import ExportUtils


class ApprovedSupplierDatasourceProcessor(PlexProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'approved_suppliers'

    def _process(self, order: Order, factory: ApprovedSupplierDatasourceFactory, operations_mapping: OperationsMapping, utils: ExportUtils):
        self._process_components(order, factory, operations_mapping, utils)
        self._process_material_routings(order, factory, operations_mapping, utils)

    def _process_material_routings(self, order: Order, factory: ApprovedSupplierDatasourceFactory, operations_mapping: OperationsMapping, utils: ExportUtils):
        """
        creates approved suppliers for materials that have an op attached, uses supplier picker in the op, and operations_mapping as a backup
        """
        order_item: OrderItem
        for order_item in order.order_items:

            component: OrderComponent
            for component in order_item.components:

                material_op: OrderOperation
                for material_op in component.material_operations:
                    op_num = utils.get_material_op_no(material_op)

                    approved_suppliers: List[ApprovedSupplierAddUpdateDatasource] = factory.to_approved_suppliers_from_material_op(
                        material_op,
                        op_num,
                        operations_mapping
                    )

                    created_approved_suppliers: List[ApprovedSupplierAddUpdateDatasource] = self._create_approved_suppliers(approved_suppliers)
                    self._log_created_approved_suppliers(created_approved_suppliers)

    def _process_components(self, order: Order, factory: ApprovedSupplierDatasourceFactory, operations_mapping: OperationsMapping, utils: ExportUtils):
        """
        creates approved suppliers for the whole order where needed according to the operations mapping table
        """

        order_item: OrderItem
        for order_item in order.order_items:

            component: OrderComponent
            for component in order_item.components:

                operation: OrderOperation
                op_num = self.config.part_operation_increment_step
                valid_operations = utils.get_non_ignored_operations_for_component(component)
                for operation in valid_operations:

                    # create approved suppliers for operation
                    approved_suppliers: List[ApprovedSupplierAddUpdateDatasource] = factory.to_approved_suppliers(
                        component,
                        operation,
                        op_num,
                        operations_mapping
                    )
                    created_approved_suppliers: List[ApprovedSupplierAddUpdateDatasource] = self._create_approved_suppliers(approved_suppliers)
                    self._log_created_approved_suppliers(created_approved_suppliers)
                    op_num += self.config.part_operation_increment_step

    def _create_approved_suppliers(self, approved_suppliers: List[ApprovedSupplierAddUpdateDatasource]):
        created_approved_suppliers: List[ApprovedSupplierAddUpdateDatasource] = []
        approved_supplier: ApprovedSupplierAddUpdateDatasource
        for approved_supplier in approved_suppliers:
            approved_supplier.create()
            created_approved_suppliers.append(approved_supplier)

        return created_approved_suppliers

    def _log_created_approved_suppliers(self, created_approved_suppliers: List[ApprovedSupplierAddUpdateDatasource]):
        if len(created_approved_suppliers) == 0:
            return
        part_no = created_approved_suppliers[0].Part_No
        operation_code = created_approved_suppliers[0].Operation_Code
        approved_supplier_code_list = [x.Supplier_Code for x in created_approved_suppliers]

        self._add_report_message(f'The following approved suppliers were created or already exists for part {part_no} on operations {operation_code}: {",".join(approved_supplier_code_list)}')
