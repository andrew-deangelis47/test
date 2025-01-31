import pytest
import datetime
import sys
import os

# append to path
from ...baseintegration.integration import Integration
from ...baseintegration.utils.custom_table import ImportCustomTable
from paperless.custom_tables.custom_tables import CustomTable

sys.path.append(os.path.join(os.path.dirname(__file__), "./example_model"))
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from example_model.models import InstaModel, InstaTruncatedModel
from ...baseintegration.utils import trim_django_model, safe_get
from ...baseintegration.utils.operations import OperationUtils
from ...baseintegration.utils.address import AddressUtils
from django.utils.timezone import make_aware
from unittest.mock import create_autospec
import unittest
from ...baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from paperless.objects.orders import OrderComponent, OrderOperation, OrderCostingVariable
from paperless.objects.quotes import QuoteComponent, QuoteOperation, Quantity, CostingVariablePayload
from types import SimpleNamespace


def create_data():
    valid_model = InstaModel.objects.create(
        pk_field=1,
        job_title="Influencer",
        is_real_job=False,
        catch_phrase="Phone eats first",
        last_updated=make_aware(datetime.datetime.now())
    )
    invalid_model = InstaModel(
        pk_field=2,
        job_title="I make trinkets and I sell them online isn't this fun??",
        is_real_job=False,
        catch_phrase="I love pinterest and social media wahoo",
        last_updated=make_aware(datetime.datetime.now())
    )
    return valid_model, invalid_model


@pytest.mark.django_db
class TestUtils:

    def test_trim_django_model(self):
        valid_model, invalid_model = create_data()
        assert len(valid_model.job_title) <= 20
        assert len(valid_model.catch_phrase) <= 30

        trim_django_model(valid_model)
        assert len(valid_model.job_title) <= 20
        assert len(valid_model.catch_phrase) <= 30

        assert len(invalid_model.job_title) > 20
        assert len(invalid_model.catch_phrase) > 30
        trim_django_model(invalid_model)
        assert len(invalid_model.job_title) <= 20
        assert len(invalid_model.catch_phrase) <= 30

    def test_autotruncate_model(self):
        model = InstaTruncatedModel(
            pk_field=2,
            job_title="I make trinkets and I sell them online isn't this fun??",
            is_real_job=False,
            catch_phrase="I love pinterest and social media wahoo",
            last_updated=make_aware(datetime.datetime.now())
        )
        assert len(model.job_title) > 20
        assert len(model.catch_phrase) > 30
        model.save()
        assert len(model.job_title) <= 20
        assert len(model.catch_phrase) <= 30

    def test_truncate_queryset(self):
        ex_job_title = "I make trinkets and I sell them online isn't this fun!!"
        ex_job_title_2 = "bah bah black sheep have you any wool"
        ex_catch_phrase = "I love facebook, insta, and social media wahoo"
        ex_catch_phrase_2 = "I love facebook, insta, and social media wahoo!!!"
        model = InstaTruncatedModel(
            pk_field=2,
            job_title=ex_job_title,
            is_real_job=False,
            catch_phrase=ex_catch_phrase,
            last_updated=make_aware(datetime.datetime.now())
        )
        model.save()
        model2 = InstaTruncatedModel(
            pk_field=3,
            job_title=ex_job_title_2,
            is_real_job=False,
            catch_phrase=ex_catch_phrase_2,
            last_updated=make_aware(datetime.datetime.now())
        )
        model2.save()
        assert len(InstaTruncatedModel.objects.filter(job_title=ex_job_title)) == 1
        assert len(InstaTruncatedModel.objects.filter(catch_phrase=ex_catch_phrase)) == 2

    def test_safe_get(self):
        class Object:
            def __init__(self):
                self.name = "obj"

                class NestedObject:
                    def __init__(self):
                        self.name = "nestedobj"

                        class DoublyNestedObject:
                            def __init__(self):
                                self.name = "doublynestedobj"
                        self.obj = DoublyNestedObject()

                self.obj = NestedObject()

        x = Object()
        y = None
        assert safe_get(x, 'name') == "obj"
        assert safe_get(y, 'name') is None
        assert safe_get(x, 'test') is None
        assert safe_get(x, 'obj.name') == "nestedobj"
        assert safe_get(x, 'obj.test') is None
        assert safe_get(y, 'obj.name') is None
        assert safe_get(x, 'obj.obj.name') == "doublynestedobj"


@pytest.mark.django_db
class TestCustomTables:

    def test_inventory(self):
        Integration()
        create_data()
        r = ImportCustomTable.import_from_django_model(InstaModel, 'InstaModel', True, True)
        assert r is True

    def test_delete(self):
        Integration()
        table_name = 'test_delete_row'
        old_rows = []
        rows = CustomTable.get(table_name)['rows']
        new_rows = [{'name': 'test5', 'field1': 'some value'},
                    {'name': 'test6', 'field1': 'value'},
                    {'name': 'test7', 'field1': 'value'}]
        ImportCustomTable.upload_records(identifier="upload-test-data", records=new_rows, table_name=table_name)
        for index, row in enumerate(rows):
            if index in (0, 2):
                old_rows.append(row)
        result = ImportCustomTable.delete_records(identifier='delete-scheduling-', records=old_rows, table_name=table_name)
        assert result["successes"]


class TestAddressUtils:

    def test_gets_correct_country_code_from_country_name(self):
        country_alpha_3, state_province = AddressUtils.get_country_and_state(country_name='United States',
                                                                             state_province_name='NH',
                                                                             zipcode='03101')
        assert country_alpha_3 == 'USA'
        assert state_province == 'NH'

    def test_gets_correct_state_from_country_code(self):
        country_alpha_3, state_province = AddressUtils.get_country_and_state(zipcode='03101',
                                                                             fallback_country_alpha_3='USA')
        assert country_alpha_3 == 'USA'
        assert state_province == 'NH'
        country_alpha_3, state_province = AddressUtils.get_country_and_state(country_name='bad country',
                                                                             zipcode='03101',
                                                                             fallback_country_alpha_3='USA')
        assert country_alpha_3 == 'USA'
        assert state_province == 'NH'

    def test_gets_correct_state_from_non_us_countries(self):
        country_alpha_3, state_province = AddressUtils.get_country_and_state(country_name='Mexico',
                                                                             zipcode='44100')
        assert country_alpha_3 == 'MEX'
        assert state_province == 'JAL'

    def test_gets_correct_state_if_state_exists_in_multiple_countries(self):
        country_alpha_3, state_province = AddressUtils.get_country_and_state(country_name='United States',
                                                                             zipcode='21202')
        assert country_alpha_3 == 'USA'
        assert state_province == 'MD'

    def test_invalid_zipcode(self):
        country_alpha_3, state_province = AddressUtils.get_country_and_state(country_name='United States',
                                                                             zipcode='03152')
        assert country_alpha_3 == 'USA'
        assert state_province == ''


class TestOperationUtils(unittest.TestCase):

    TEST_OPERATION_NAME_0 = 'test_op_0'
    TEST_OPERATION_NAME_1 = 'test_op_1'
    TEST_OPERATION_VAR_VALUE = 'test_data'
    TEST_OPERATION_VAR_NAME = 'test'
    TEST_DEFAULT_OPERATION_VAR_VALUE = 'default'
    TEST_PART_NUMBER = 'part_number'
    TEST_ORDER_OPERATION_OBJ_VALUE = CostingVariablePayload(row={'test': 1}, options=None, value='1')
    TEST_QUOTE_OPERATION_OBJ_VALUE = OrderCostingVariable(label='na', row={'test': 1}, value='1', options=None,
                                                          value_type='str', variable_class='')

    def setUp(self) -> None:
        self.operation_utils = OperationUtils()

    def test_get_variable_value_from_operation_returns_var_value_if_exists_for_quote_operation(self):
        # setup mock quote operation
        operation = create_autospec(QuoteOperation)
        operation.get_variable.return_value = self.TEST_OPERATION_VAR_VALUE

        # test that we get the desired value back
        result = self.operation_utils.get_variable_value_from_operation(operation, self.TEST_OPERATION_VAR_NAME)
        self.assertEqual(self.TEST_OPERATION_VAR_VALUE, result)

    def test_get_variable_value_from_operation_returns_var_value_if_exists_for_order_operation(self):
        # setup mock quote operation
        operation = create_autospec(OrderOperation)
        operation.get_variable.return_value = self.TEST_OPERATION_VAR_VALUE

        # test that we get the desired value back
        result = self.operation_utils.get_variable_value_from_operation(operation, self.TEST_OPERATION_VAR_NAME)
        self.assertEqual(self.TEST_OPERATION_VAR_VALUE, result)

    def test_get_variable_value_from_order_operation_throws_exception_if_no_value_and_no_default_supplied_for_quote_operation(self):
        # setup mock quote operatiom
        operation = create_autospec(QuoteOperation)
        operation.operation_definition_name = self.TEST_OPERATION_NAME_0
        operation.get_variable.return_value = None

        # test that a cancel integration exception is thrown
        with self.assertRaises(CancelledIntegrationActionException):
            self.operation_utils.get_variable_value_from_operation(operation, self.TEST_OPERATION_VAR_NAME)

    def test_get_variable_value_from_order_operation_throws_exception_if_no_value_and_no_default_supplied_for_order_operation(self):
        # setup mock order operatiom
        operation = create_autospec(OrderOperation)
        operation.operation_definition_name = self.TEST_OPERATION_NAME_0
        operation.get_variable.return_value = None

        # test that a cancel integration exception is thrown
        with self.assertRaises(CancelledIntegrationActionException):
            self.operation_utils.get_variable_value_from_operation(operation, self.TEST_OPERATION_VAR_NAME)

    def test_get_variable_value_from_order_operation_returns_default_if_supplied_and_var_does_not_exist_for_quote_operation(self):
        # setup mock op
        operation = create_autospec(QuoteOperation)
        operation.get_variable.return_value = None

        # test that the default is returned
        value = self.operation_utils.get_variable_value_from_operation(operation, self.TEST_OPERATION_VAR_NAME, self.TEST_DEFAULT_OPERATION_VAR_VALUE)
        self.assertEqual(self.TEST_DEFAULT_OPERATION_VAR_VALUE, value)

    def test_get_variable_value_from_order_operation_returns_default_if_supplied_and_var_does_not_exist_for_order_operation(self):
        # setup mock op
        operation = create_autospec(OrderOperation)
        operation.get_variable.return_value = None

        # test that the default is returned
        value = self.operation_utils.get_variable_value_from_operation(operation, self.TEST_OPERATION_VAR_NAME, self.TEST_DEFAULT_OPERATION_VAR_VALUE)
        self.assertEqual(self.TEST_DEFAULT_OPERATION_VAR_VALUE, value)

    def test_get_operation_variable_value_from_component_throws_exception_if_op_not_found_and_no_default_supplied_for_quote_component(self):
        # setup mock quote operation
        quote_operation = create_autospec(QuoteOperation)
        quote_operation.operation_definition_name = self.TEST_OPERATION_NAME_0

        # setup mock quote component
        quote_component = create_autospec(QuoteComponent)
        quote_component.part_number = ''
        quote_component.shop_operations = [quote_operation]
        quote_component.material_operations = []

        # assert exception is thrown
        with self.assertRaises(CancelledIntegrationActionException):
            self.operation_utils.get_operation_variable_value_from_component(quote_component, self.TEST_OPERATION_NAME_1, self.TEST_OPERATION_VAR_NAME)

    def test_get_operation_variable_value_from_component_throws_exception_if_op_not_found_and_no_default_supplied_for_order_component(self):
        # setup mock order operation
        order_operation = create_autospec(OrderOperation)
        order_operation.operation_definition_name = self.TEST_OPERATION_NAME_0

        # setup mock order component
        order_component = create_autospec(OrderComponent)
        order_component.part_number = ''
        order_component.shop_operations = [order_operation]
        order_component.material_operations = []

        # assert exception is thrown
        with self.assertRaises(CancelledIntegrationActionException):
            self.operation_utils.get_operation_variable_value_from_component(order_component, self.TEST_OPERATION_NAME_1, self.TEST_OPERATION_VAR_NAME)

    def test_get_operation_variable_value_from_component_returns_default_if_op_not_found_and_default_is_supplied_for_quote_component(self):
        # setup mock quote operation
        quote_operation = create_autospec(QuoteOperation)
        quote_operation.operation_definition_name = self.TEST_OPERATION_NAME_0

        quote_component = create_autospec(QuoteComponent)
        quote_component.shop_operations = [quote_operation]
        quote_component.material_operations = []

        result = self.operation_utils.get_operation_variable_value_from_component(quote_component, self.TEST_OPERATION_NAME_1, self.TEST_OPERATION_VAR_NAME, self.TEST_DEFAULT_OPERATION_VAR_VALUE)

        # assert that we get the default value back
        self.assertEqual(self.TEST_DEFAULT_OPERATION_VAR_VALUE, result)

    def test_get_operation_variable_value_from_component_returns_default_if_op_not_found_and_default_is_supplied_for_order_component(self):
        # setup mock quote operation
        order_operation = create_autospec(OrderOperation)
        order_operation.operation_definition_name = self.TEST_OPERATION_NAME_0

        order_component = create_autospec(OrderComponent)
        order_component.shop_operations = [order_operation]
        order_component.material_operations = []

        result = self.operation_utils.get_operation_variable_value_from_component(order_component, self.TEST_OPERATION_NAME_1, self.TEST_OPERATION_VAR_NAME, self.TEST_DEFAULT_OPERATION_VAR_VALUE)

        # assert that we get the default value back
        self.assertEqual(self.TEST_DEFAULT_OPERATION_VAR_VALUE, result)

    def test_get_operation_variable_value_from_component_throws_exception_if_op_is_found_but_value_is_none_and_no_default_supplied_for_quote_component(self):
        # setup mock op
        quote_operation = create_autospec(QuoteOperation)
        quote_operation.operation_definition_name = self.TEST_OPERATION_NAME_0
        quote_operation.get_variable.return_value = None

        quote_component = create_autospec(QuoteComponent)
        quote_component.part_number = self.TEST_PART_NUMBER
        quote_component.shop_operations = [quote_operation]
        quote_component.material_operations = []

        # assert exception is thrown
        with self.assertRaises(CancelledIntegrationActionException):
            self.operation_utils.get_operation_variable_value_from_component(quote_component, self.TEST_OPERATION_NAME_0, self.TEST_OPERATION_VAR_NAME)

    def test_get_operation_variable_value_from_component_throws_exception_if_op_is_found_but_value_is_none_and_no_default_supplied_for_order_component(self):
        # setup mock op
        order_operation = create_autospec(OrderOperation)
        order_operation.operation_definition_name = self.TEST_OPERATION_NAME_0
        order_operation.get_variable.return_value = None

        order_component = create_autospec(OrderComponent)
        order_component.part_number = self.TEST_PART_NUMBER
        order_component.shop_operations = [order_operation]
        order_component.material_operations = []

        # assert exception is thrown
        with self.assertRaises(CancelledIntegrationActionException):
            self.operation_utils.get_operation_variable_value_from_component(order_component, self.TEST_OPERATION_NAME_0, self.TEST_OPERATION_VAR_NAME)

    def test_get_operation_variable_value_from_component_returns_default_value_if_op_is_found_but_value_is_none_and_default_supplied_for_quote_component(self):
        # setup mock op
        quote_operation = create_autospec(QuoteOperation)
        quote_operation.operation_definition_name = self.TEST_OPERATION_NAME_0
        quote_operation.get_variable.return_value = None

        quote_component = create_autospec(QuoteComponent)
        quote_component.part_number = self.TEST_PART_NUMBER
        quote_component.shop_operations = [quote_operation]
        quote_component.material_operations = []

        # assert exception is thrown
        result = self.operation_utils.get_operation_variable_value_from_component(quote_component, self.TEST_OPERATION_NAME_0, self.TEST_OPERATION_VAR_NAME, self.TEST_DEFAULT_OPERATION_VAR_VALUE)

        # assert that we get the default value back
        self.assertEqual(self.TEST_DEFAULT_OPERATION_VAR_VALUE, result)

    def test_get_operation_variable_value_from_component_returns_default_value_if_op_is_found_but_value_is_none_and_default_supplied_for_order_component(self):
        # setup mock op
        order_operation = create_autospec(OrderOperation)
        order_operation.operation_definition_name = self.TEST_OPERATION_NAME_0
        order_operation.get_variable.return_value = None

        order_component = create_autospec(OrderComponent)
        order_component.part_number = self.TEST_PART_NUMBER
        order_component.shop_operations = [order_operation]
        order_component.material_operations = []

        # assert exception is thrown
        result = self.operation_utils.get_operation_variable_value_from_component(order_component, self.TEST_OPERATION_NAME_0, self.TEST_OPERATION_VAR_NAME, self.TEST_DEFAULT_OPERATION_VAR_VALUE)

        # assert that we get the default value back
        self.assertEqual(self.TEST_DEFAULT_OPERATION_VAR_VALUE, result)

    def test_get_operation_variable_value_from_component_returns_alue_if_op_is_found_and_value_is_not_none_and_default_not_supplied_for_quote_component(self):
        # setup mock op
        quote_operation = create_autospec(QuoteOperation)
        quote_operation.operation_definition_name = self.TEST_OPERATION_NAME_0
        quote_operation.get_variable.return_value = self.TEST_OPERATION_VAR_VALUE

        quote_component = create_autospec(QuoteComponent)
        quote_component.shop_operations = [quote_operation]
        quote_component.material_operations = []

        # assert exception is thrown
        result = self.operation_utils.get_operation_variable_value_from_component(quote_component, self.TEST_OPERATION_NAME_0, self.TEST_OPERATION_VAR_NAME)
        # assert that we got the real var value
        self.assertEqual(self.TEST_OPERATION_VAR_VALUE, result)

    def test_get_operation_variable_value_from_component_returns_alue_if_op_is_found_and_value_is_not_none_and_default_not_supplied_for_order_component(self):
        # setup mock op
        order_operation = create_autospec(OrderOperation)
        order_operation.operation_definition_name = self.TEST_OPERATION_NAME_0
        order_operation.get_variable.return_value = self.TEST_OPERATION_VAR_VALUE

        order_component = create_autospec(OrderComponent)
        order_component.shop_operations = [order_operation]
        order_component.material_operations = []

        # assert exception is thrown
        result = self.operation_utils.get_operation_variable_value_from_component(order_component, self.TEST_OPERATION_NAME_0, self.TEST_OPERATION_VAR_NAME)
        # assert that we got the real var value
        self.assertEqual(self.TEST_OPERATION_VAR_VALUE, result)

    def test_get_operation_variable_value_from_component_returns_value_if_op_is_found_and_value_is_not_none_and_default_supplied_for_quote_component(self):
        # setup mock op
        quote_operation = create_autospec(QuoteOperation)
        quote_operation.operation_definition_name = self.TEST_OPERATION_NAME_0
        quote_operation.get_variable.return_value = self.TEST_OPERATION_VAR_VALUE

        quote_component = create_autospec(QuoteComponent)
        quote_component.shop_operations = [quote_operation]
        quote_component.material_operations = []

        # assert exception is thrown
        result = self.operation_utils.get_operation_variable_value_from_component(quote_component, self.TEST_OPERATION_NAME_0, self.TEST_OPERATION_VAR_NAME, self.TEST_DEFAULT_OPERATION_VAR_VALUE)
        # assert that we get the real var value
        self.assertEqual(self.TEST_OPERATION_VAR_VALUE, result)

    def test_get_operation_variable_value_from_component_returns_value_if_op_is_found_and_value_is_not_none_and_default_supplied_for_order_component(self):
        # setup mock op
        order_operation = create_autospec(OrderOperation)
        order_operation.operation_definition_name = self.TEST_OPERATION_NAME_0
        order_operation.get_variable.return_value = self.TEST_OPERATION_VAR_VALUE

        order_component = create_autospec(OrderComponent)
        order_component.shop_operations = [order_operation]
        order_component.material_operations = []

        # assert exception is thrown
        result = self.operation_utils.get_operation_variable_value_from_component(order_component, self.TEST_OPERATION_NAME_0, self.TEST_OPERATION_VAR_NAME, self.TEST_DEFAULT_OPERATION_VAR_VALUE)
        # assert that we get the real var value
        self.assertEqual(self.TEST_OPERATION_VAR_VALUE, result)

    def test_get_operation_variable_value_from_component_throws_exception_if_there_are_multiple_of_the_same_op_in_the_routing_for_quote_component(self):
        # setup mock quote operations with same name
        quote_operation_0 = create_autospec(QuoteOperation)
        quote_operation_0.operation_definition_name = self.TEST_OPERATION_NAME_0
        quote_operation_0.name = self.TEST_OPERATION_NAME_0
        quote_operation_0.get_variable.return_value = self.TEST_OPERATION_VAR_VALUE

        quote_operation_1 = create_autospec(QuoteOperation)
        quote_operation_1.name = self.TEST_OPERATION_NAME_0
        quote_operation_1.operation_definition_name = self.TEST_OPERATION_NAME_0
        quote_operation_1.get_variable.return_value = self.TEST_OPERATION_VAR_VALUE

        # setup mock quote component
        quote_component = create_autospec(QuoteComponent)
        quote_component.part_number = self.TEST_PART_NUMBER
        quote_component.shop_operations = [quote_operation_0, quote_operation_1]
        quote_component.material_operations = []

        # assert exception is thrown
        with self.assertRaises(CancelledIntegrationActionException):
            self.operation_utils.get_operation_variable_value_from_component(quote_component, self.TEST_OPERATION_NAME_0, self.TEST_OPERATION_VAR_NAME)

    def test_get_operation_variable_value_from_component_throws_exception_if_there_are_multiple_of_the_same_op_in_the_routing_for_order_component(self):
        # setup mock quote operations with same name
        order_operation_0 = create_autospec(OrderOperation)
        order_operation_0.operation_definition_name = self.TEST_OPERATION_NAME_0
        order_operation_0.name = self.TEST_OPERATION_NAME_0
        order_operation_0.get_variable.return_value = self.TEST_OPERATION_VAR_VALUE

        order_operation_1 = create_autospec(OrderOperation)
        order_operation_1.name = self.TEST_OPERATION_NAME_0
        order_operation_1.operation_definition_name = self.TEST_OPERATION_NAME_0
        order_operation_1.get_variable.return_value = self.TEST_OPERATION_VAR_VALUE

        # setup mock quote component
        order_component = create_autospec(OrderComponent)
        order_component.part_number = self.TEST_PART_NUMBER
        order_component.shop_operations = [order_operation_0, order_operation_1]
        order_component.material_operations = []

        # assert exception is thrown
        with self.assertRaises(CancelledIntegrationActionException):
            self.operation_utils.get_operation_variable_value_from_component(order_component, self.TEST_OPERATION_NAME_0, self.TEST_OPERATION_VAR_NAME)

    def test_get_variable_obj_from_returns_same_value_for_quotes_and_orders(self):
        order_operation = create_autospec(OrderOperation)
        order_operation.get_variable_obj.return_value = self.TEST_ORDER_OPERATION_OBJ_VALUE

        quote_operation = create_autospec(QuoteOperation)
        quote_operation.get_variable_for_qty.return_value = self.TEST_QUOTE_OPERATION_OBJ_VALUE
        quote_operation.quantities = [SimpleNamespace(**{'quantity': 1})]

        quote_component = create_autospec(QuoteComponent)
        quantity = create_autospec(Quantity)
        quantity.quantity = 1
        quote_component.quantities = [quantity]

        quote_result = self.operation_utils.get_variable_obj(operation=quote_operation,
                                                             variable_name='Any')
        order_result = self.operation_utils.get_variable_obj(operation=order_operation,
                                                             variable_name='Any')
        assert quote_result.row == order_result.row
