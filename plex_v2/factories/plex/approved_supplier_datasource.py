from plex_v2.factories.base import BaseFactory
from plex_v2.objects.approved_supplier_upload_datasource import ApprovedSupplierAddUpdateDatasource
from paperless.objects.orders import OrderComponent, OrderOperation
from plex_v2.objects.operations_mapping import OperationsMapping
from typing import List, Union
from plex_v2.objects.part import Part


class ApprovedSupplierDatasourceFactory(BaseFactory):

    def to_approved_suppliers_from_material_op(self, material_operation: OrderOperation, op_no: int, operations_mapping: OperationsMapping) -> List[ApprovedSupplierAddUpdateDatasource]:
        plex_material: Part = self.utils.get_plex_material_from_material_op(material_operation)

        # 1) if no op code in the op then we know to skip
        plex_op_code: str = self.utils.operation_utils.get_variable_value_from_operation(
            material_operation,
            self.config.plex_op_code_var,
            None
        )

        if plex_op_code is None:
            return []

        # 2) check for supplier code in the operation, and if not found then look at the op mapping table
        supplier_codes: List[str] = self.utils.get_supplier_codes_from_material_op(
            material_operation,
            plex_op_code,
            operations_mapping
        )

        approved_suppliers: List[ApprovedSupplierAddUpdateDatasource] = []
        for supplier_code in supplier_codes:
            approved_suppliers.append(ApprovedSupplierAddUpdateDatasource(
                Active=1,
                Part_No=plex_material.number,
                Revision=plex_material.revision,
                Operation_Code=plex_op_code,
                Operation_No=op_no,
                Supplier_Code=supplier_code,
                Price=self._get_price(material_operation)
            ))

        return approved_suppliers

    def to_approved_suppliers(self, component: OrderComponent, operation: OrderOperation, op_no: int, operations_mapping: OperationsMapping) -> List[ApprovedSupplierAddUpdateDatasource]:
        """
        creates one approved supplier datasource model for each approved supplier for the operation
        """

        # 1) first check for a supplier code in the operation
        supplier_code: str = self.utils.operation_utils.get_variable_value_from_operation(
            operation,
            self.config.supplier_code_var,
            None
        )

        # 2) If not found check the operations mapping table
        if supplier_code is None:
            approved_supplier_codes_for_op = operations_mapping.get_approved_supplier_codes_by_pp_op(operation)
        else:
            approved_supplier_codes_for_op = [supplier_code]

        approved_suppliers: List[ApprovedSupplierAddUpdateDatasource] = []
        for supplier_code in approved_supplier_codes_for_op:

            approved_suppliers.append(ApprovedSupplierAddUpdateDatasource(
                Active=1,
                Part_No=component.part_number,
                Revision=self.utils.get_plex_part_revision_from_paperless_component(component),
                Operation_Code=self.utils.get_plex_operation_code_from_paperless_operation(operation, operations_mapping),
                Operation_No=op_no,
                Supplier_Code=supplier_code,
                Price=self._get_price(operation)
            ))

        return approved_suppliers

    def _get_price(self, operation: OrderOperation) -> Union[float, int]:
        return self.utils.operation_utils.get_variable_value_from_operation(
            operation,
            self.config.piece_price_var
        )
