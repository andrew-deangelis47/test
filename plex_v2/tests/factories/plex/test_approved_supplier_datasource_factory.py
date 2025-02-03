from plex_v2.factories.plex.approved_supplier_datasource import ApprovedSupplierDatasourceFactory
from plex_v2.configuration import PlexConfig
from unittest.mock import create_autospec, Mock
from plex_v2.utils.export import ExportUtils
from paperless.objects.orders import OrderComponent, OrderOperation
from plex_v2.objects.operations_mapping import OperationsMapping


class TestApprovedSupplierDatasourceFactory:

    VALID_APPROVED_SUPPLIER_CODE_0 = 'approved_supplier_code_0'
    VALID_APPROVED_SUPPLIER_CODE_1 = 'approved_supplier_code_1'
    VALID_COMPONENT_PART_NO = 'part_no'
    VALID_COMPONENT_REV = 'rev'
    VALID_PLEX_OP_CODE = 'plex_op_code'
    VALID_PRICE = 1.24
    VALID_OP_DEF_NAME = 'valid_op_def_name'
    SUPPLIER_CODE_VAR = 'supplier_code_var'
    SUPPLIER_CODE = 'supplier_code'
    PIECE_PRICE_VAR = 'piece_price_var'

    def setup_method(self):
        self.config = create_autospec(PlexConfig)
        self.config.supplier_code_var = self.SUPPLIER_CODE_VAR
        self.config.piece_price_var = self.PIECE_PRICE_VAR

        self.order_component = create_autospec(OrderComponent)
        self.order_component.part_number = self.VALID_COMPONENT_PART_NO
        self.order_component.revision = self.VALID_COMPONENT_REV

        self.order_operation = create_autospec(OrderOperation)
        self.order_operation.operation_definition_name = self.VALID_OP_DEF_NAME

        self.operation_utils = Mock()
        self.operation_utils.get_variable_value_from_operation.side_effect = self.op_side_effect

        self.utils = create_autospec(ExportUtils)
        self.utils.operation_utils = self.operation_utils
        self.utils.get_plex_part_revision_from_paperless_component.return_value = self.VALID_COMPONENT_REV

        self.factory = ApprovedSupplierDatasourceFactory(
            config=self.config,
            utils=self.utils
        )

        self.op_no = 10
        self.operations_mapping = create_autospec(OperationsMapping)
        self.operations_mapping.get_approved_supplier_codes_by_pp_op.return_value = [self.VALID_APPROVED_SUPPLIER_CODE_0]
        self.operations_mapping.get_plex_op_code_from_pp_op_using_mapping_table.return_value = self.VALID_PLEX_OP_CODE
        self.operations_mapping.get_approved_supplier_codes_by_pp_op.side_effect = self.side_effect_get_approved_supplier_codes_by_pp_op

    def op_side_effect(self, mat_op, var, default=None):
        if var == self.PIECE_PRICE_VAR:
            return self.VALID_PRICE
        elif var == self.SUPPLIER_CODE_VAR:
            return self.SUPPLIER_CODE

    def side_effect_get_approved_supplier_codes_by_pp_op(self, operation):
        return [
            self.VALID_APPROVED_SUPPLIER_CODE_0,
            self.VALID_APPROVED_SUPPLIER_CODE_1
        ]

    def test_approved_supplier_factory_sets_part_no_to_component_part_no(self):
        approved_supplier = self.factory.to_approved_suppliers(
            self.order_component,
            self.order_operation,
            self.op_no,
            self.operations_mapping
        )[0]

        assert approved_supplier.Part_No == self.order_component.part_number

    def test_approved_supplier_factory_sets_rev_to_result_of_get_plex_part_revision_from_paperless_component(self):
        approved_supplier = self.factory.to_approved_suppliers(
            self.order_component,
            self.order_operation,
            self.op_no,
            self.operations_mapping
        )[0]

        assert approved_supplier.Revision == self.VALID_COMPONENT_REV

    def test_approved_supplier_factory_sets_op_code_to_op_code_from_op_mapping_object(self):
        approved_supplier = self.factory.to_approved_suppliers(
            self.order_component,
            self.order_operation,
            self.op_no,
            self.operations_mapping
        )[0]

        assert approved_supplier.Operation_Code == self.VALID_PLEX_OP_CODE

    def test_approved_supplier_factory_sets_op_no_to_what_is_passed_in(self):
        approved_supplier = self.factory.to_approved_suppliers(
            self.order_component,
            self.order_operation,
            self.op_no,
            self.operations_mapping
        )[0]

        assert approved_supplier.Operation_No == self.op_no

    def test_approved_supplier_factory_sets_price_to_piece_price_from_operation_utils(self):
        approved_supplier = self.factory.to_approved_suppliers(
            self.order_component,
            self.order_operation,
            self.op_no,
            self.operations_mapping
        )[0]

        assert approved_supplier.Price == self.VALID_PRICE

    def side_effect_return_none(self, op, var, default=None):
        if var == self.PIECE_PRICE_VAR:
            return self.VALID_PRICE
        elif var == self.SUPPLIER_CODE_VAR:
            return None

    def test_approved_supplier_factory_creates_as_many_objects_as_ops_associated_supplier_codes(self):
        # force return of Null when getting it from the operation
        self.operation_utils.get_variable_value_from_operation.side_effect = self.side_effect_return_none

        approved_suppliers = self.factory.to_approved_suppliers(
            self.order_component,
            self.order_operation,
            self.op_no,
            self.operations_mapping
        )

        assert len(approved_suppliers) == 2
