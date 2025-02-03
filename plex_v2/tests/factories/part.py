import unittest
from plex_v2.configuration import PlexConfig
from unittest.mock import create_autospec
from paperless.objects.orders import OrderComponent, Order, OrderItem, OrderOperation
from plex_v2.factories.plex.part import PlexPartFactory
from plex_v2.utils.export import ExportUtils
from baseintegration.utils.operations import OperationUtils


class PartFactoryTest(unittest.TestCase):

    TEST_PART_NUMBER = 'test_part_number'
    TEST_PART_NAME = 'test_part_name'
    TEST_REVISION = 'test_rev'
    TEST_DESCRIPTION = 'test_description'
    TEST_MAKE_QUANITY = 3

    DEFAULT_PART_TYPE = 'default_part_type'
    DEFAULT_PART_GROUP = 'default_part_group'
    DEFAULT_PRODUCT_TYPE = 'default_product_type'
    DEFAULT_PART_STATUS = 'default_part_status'
    DEFAULT_PART_SOURCE = 'default_part_source'
    DEFAULT_PART_BUILDING_CODE = 'default_part_building_code'

    TEST_QUOTE_NUMBER = 1
    TEST_QUOTE_REVISION_NUMBER = 2

    TEST_ORDER_ITEM_LEAD_DAYS = 5

    TEST_OP_DEF_NAME = 'op_def_name'
    TEST_OP_VAR_NAME = 'op_var_name'
    TEST_OP_VAR_VALUE = 'op_var_val'

    VALID_PART_TYPE_OP_VAR_VALUE = 'part_type'

    def setUp(self) -> None:
        # setup required config values
        self.config = PlexConfig(
            default_part_type=self.DEFAULT_PART_TYPE,
            part_type_var=self.TEST_OP_DEF_NAME,
            default_part_group=self.DEFAULT_PART_GROUP,
            part_group_var=self.TEST_OP_DEF_NAME,
            default_product_type=self.DEFAULT_PRODUCT_TYPE,
            part_product_type_var=self.TEST_OP_DEF_NAME,
            default_part_status=self.DEFAULT_PART_STATUS,
            part_status_var=self.TEST_OP_DEF_NAME,
            default_part_source=self.DEFAULT_PART_STATUS,
            part_source_var=self.TEST_OP_DEF_NAME,
            default_part_building_code=self.DEFAULT_PART_BUILDING_CODE,
            part_building_code_var=self.TEST_OP_DEF_NAME,
        )

        # setup test order
        order = create_autospec(Order)
        order.quote_number = self.TEST_QUOTE_NUMBER
        order.quote_revision_number = self.TEST_QUOTE_REVISION_NUMBER
        self.order = order

        # setup test order item
        order_item = create_autospec(OrderItem)
        order_item.lead_days = self.TEST_ORDER_ITEM_LEAD_DAYS
        self.order_item = order_item

        # setup test order component
        order_component = create_autospec(OrderComponent)
        order_component.part_number = self.TEST_PART_NUMBER
        order_component.part_name = self.TEST_PART_NAME
        order_component.revision = self.TEST_REVISION
        order_component.description = self.TEST_DESCRIPTION
        order_component.make_quantity = self.TEST_MAKE_QUANITY
        order_component.shop_operations = []
        order_component.material_operations = []
        self.order_component = order_component

        # force mocks to return what we need
        self.operation_utils = create_autospec(OperationUtils)
        self.operation_utils.get_operation_variable_value_from_component.return_value = 'test'

        self.export_utils = create_autospec(ExportUtils)
        self.export_utils.operation_utils = self.operation_utils
        self.export_utils.get_plex_part_number_of_pp_component.return_value = self.TEST_PART_NUMBER
        self.export_utils.get_plex_part_revision_from_paperless_component.return_value = self.TEST_REVISION
        self.export_utils.is_new_rev_of_old_part.return_value = False

        self.factory = PlexPartFactory(self.config, self.export_utils)

    def test_to_plex_part_sets_number_to_part_number_if_part_number_exists(self):
        plex_part = self.factory.to_plex_part(
            self.order,
            self.order_item,
            self.order_component
        )
        self.assertEqual(plex_part.number, self.TEST_PART_NUMBER)

    def test_to_plex_part_sets_revision_to_part_revision_if_not_none(self):
        plex_part = self.factory.to_plex_part(
            self.order,
            self.order_item,
            self.order_component
        )
        self.assertEqual(plex_part.revision, self.TEST_REVISION)

    def test_to_plex_part_sets_description_to_part_description_if_exists(self):
        plex_part = self.factory.to_plex_part(
            self.order,
            self.order_item,
            self.order_component
        )
        self.assertEqual(plex_part.description, self.TEST_DESCRIPTION)

    def test_to_plex_part_sets_description_to_empty_string_if_description_is_none(self):
        self.order_component.description = None
        plex_part = self.factory.to_plex_part(
            self.order,
            self.order_item,
            self.order_component
        )
        self.assertEqual(plex_part.description, '')

    def test_to_plex_part_sets_standard_job_quantity_to_make_quantity(self):
        plex_part = self.factory.to_plex_part(
            self.order,
            self.order_item,
            self.order_component
        )
        self.assertEqual(plex_part.standard_job_qty, self.TEST_MAKE_QUANITY)

    def test_to_plex_part_sets_bom_substitution_allowed_to_true(self):
        plex_part = self.factory.to_plex_part(
            self.order,
            self.order_item,
            self.order_component
        )
        self.assertEqual(plex_part.bom_substitution_allowed, True)

    def test_to_plex_part_sets_type_to_operation_value_if_exists(self):
        # create mock op to return the value
        self.operation_utils.get_operation_variable_value_from_component.return_value = self.TEST_OP_VAR_VALUE
        self.export_utils.operation_utils = self.operation_utils
        factory = PlexPartFactory(self.config, self.export_utils)

        # test
        plex_part = factory.to_plex_part(
            self.order,
            self.order_item,
            self.order_component
        )

        self.assertEqual(self.TEST_OP_VAR_VALUE, plex_part.type)

    def test_to_plex_part_sets_group_to_operation_value_if_exists(self):
        # create mock op to return the value
        self.operation_utils.get_operation_variable_value_from_component.return_value = self.TEST_OP_VAR_VALUE
        self.export_utils.operation_utils = self.operation_utils
        factory = PlexPartFactory(self.config, self.export_utils)

        # test
        plex_part = factory.to_plex_part(
            self.order,
            self.order_item,
            self.order_component
        )

        self.assertEqual(self.TEST_OP_VAR_VALUE, plex_part.group)

    def test_to_plex_part_sets_product_type_to_operation_value_if_exists(self):
        # create mock op to return the value
        self.operation_utils.get_operation_variable_value_from_component.return_value = self.TEST_OP_VAR_VALUE
        self.export_utils.operation_utils = self.operation_utils
        factory = PlexPartFactory(self.config, self.export_utils)

        # test
        plex_part = factory.to_plex_part(
            self.order,
            self.order_item,
            self.order_component
        )

        self.assertEqual(self.TEST_OP_VAR_VALUE, plex_part.productType)

    def test_to_plex_part_sets_status_to_operation_value_if_exists(self):
        # create mock op to return the value
        self.operation_utils.get_operation_variable_value_from_component.return_value = self.TEST_OP_VAR_VALUE
        self.export_utils.operation_utils = self.operation_utils
        factory = PlexPartFactory(self.config, self.export_utils)

        # test
        plex_part = factory.to_plex_part(
            self.order,
            self.order_item,
            self.order_component
        )

        self.assertEqual(self.TEST_OP_VAR_VALUE, plex_part.status)

    def test_to_plex_part_sets_source_to_operation_value_if_exists(self):
        # create mock op to return the value
        self.operation_utils.get_operation_variable_value_from_component.return_value = self.TEST_OP_VAR_VALUE
        self.export_utils.operation_utils = self.operation_utils
        factory = PlexPartFactory(self.config, self.export_utils)

        # test
        plex_part = factory.to_plex_part(
            self.order,
            self.order_item,
            self.order_component
        )

        self.assertEqual(self.TEST_OP_VAR_VALUE, plex_part.source)

    def test_to_plex_part_sets_note_to_link_to_pp_quote(self):
        expected_note = f'Paperless Parts Quote: https://app.paperlessparts.com/quotes/edit/{self.order.quote_number}-{self.order.quote_revision_number}'

        # test
        plex_part = self.factory.to_plex_part(
            self.order,
            self.order_item,
            self.order_component
        )

        self.assertEqual(expected_note, plex_part.note)

    def test_to_plex_part_sets_is_new_rev_of_old_part_to_return_value_from_utils(self):
        # 1) test True
        self.export_utils.is_new_rev_of_old_part.return_value = True
        self.factory.utils = self.export_utils

        # test
        plex_part = self.factory.to_plex_part(
            self.order,
            self.order_item,
            self.order_component
        )

        self.assertEqual(plex_part.is_new_rev_of_old_part, True)

        # 2) test False
        self.export_utils.is_new_rev_of_old_part.return_value = False
        self.factory.utils = self.export_utils

        # test
        plex_part = self.factory.to_plex_part(
            self.order,
            self.order_item,
            self.order_component
        )

        self.assertEqual(plex_part.is_new_rev_of_old_part, False)

    def test_to_plex_part_update_datasource_gets_part_no_and_rev_from_op_when_operation(self):
        self.export_utils.operation_utils.get_variable_value_from_operation.return_value = 'test_pn'
        self.export_utils.get_plex_revision_from_material_operation.return_value = 'test_rev'
        order_op = create_autospec(OrderOperation)

        plex_part = self.factory.to_plex_part_update_datasource(
            order_op
        )

        assert plex_part.Part_No == 'test_pn'
        assert plex_part.Revision == 'test_rev'

    def test_to_plex_part_update_datasource_gets_part_no_and_rev_from_component_when_component(self):

        plex_part = self.factory.to_plex_part_update_datasource(
            self.order_component
        )

        assert plex_part.Part_No == self.TEST_PART_NUMBER
        assert plex_part.Revision == self.TEST_REVISION

    def test_to_plex_part_update_datasource_sets_grade_if_configured(self):
        self.config.should_export_part_grade = True
        self.config.default_part_grade = 'test_grade'
        self.export_utils.operation_utils.get_operation_variable_value_from_component.return_value = 'test_grade'

        plex_part = self.factory.to_plex_part_update_datasource(
            self.order_component
        )

        assert plex_part.Grade == 'test_grade'

    def test_to_plex_part_update_datasource_sets_internal_note_if_configured(self):
        self.config.should_export_internal_note = True
        self.config.default_internal_note = 'test_note'
        self.export_utils.operation_utils.get_operation_variable_value_from_component.return_value = 'test_note'

        plex_part = self.factory.to_plex_part_update_datasource(
            self.order_component
        )

        assert plex_part.Internal_Note == 'test_note'

    def test_to_plex_part_update_datasource_sets_part_cycle_frequency_if_configured(self):
        self.config.should_export_part_cycle_frequency = True
        self.config.default_part_cycle_frequency = 'test_cycle'
        self.export_utils.operation_utils.get_operation_variable_value_from_component.return_value = 'test_cycle'

        plex_part = self.factory.to_plex_part_update_datasource(
            self.order_component
        )

        assert plex_part.Cycle_Frequency == 'test_cycle'

    def test_to_plex_part_update_datasource_sets_part_building_code_if_configured(self):
        self.config.should_export_part_building_code = True
        self.config.default_part_building_code = 'test_building_code'
        self.export_utils.operation_utils.get_operation_variable_value_from_component.return_value = 'test_building_code'

        plex_part = self.factory.to_plex_part_update_datasource(
            self.order_component
        )

        assert plex_part.Building_Code == 'test_building_code'

    def test_to_plex_part_update_datasource_sets_part_weight_if_configured(self):
        self.config.should_export_part_weight = True
        self.config.default_part_weight = 'test_weight'
        self.export_utils.operation_utils.get_operation_variable_value_from_component.return_value = 'test_weight'

        plex_part = self.factory.to_plex_part_update_datasource(
            self.order_component
        )

        assert plex_part.Weight == 'test_weight'
