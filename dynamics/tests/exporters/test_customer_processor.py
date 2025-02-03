import pytest

from baseintegration.integration import Integration
from baseintegration.utils.test_utils import get_quote
from types import SimpleNamespace

from dynamics.exceptions import DynamicsNotFoundException
from dynamics.exporter.processors.customer import CustomerProcessor
from dynamics.objects.customer import Customer, Contact, PaymentTerm, CountryCode
from dynamics.tests.utils import get_object_mocks, with_mocks, DynamicsMock


@pytest.fixture
def setup_integration():
    integration = Integration()
    from dynamics.exporter.exporter import DynamicsQuoteExporter
    exporter = DynamicsQuoteExporter(integration)
    processor = CustomerProcessor(exporter)
    return processor


mock_dict = {
    Customer: SimpleNamespace(
        No='new number',
        Name='new name'
    ),
    Contact: SimpleNamespace(
        No='num'
    ),
    PaymentTerm: SimpleNamespace(
        Code='code'
    ),
    CountryCode: SimpleNamespace(
        Code='USA'
    )
}

basic_mocks = get_object_mocks(mock_dict)


class TestCustomerProcessor:

    @staticmethod
    def process_contact(processor):
        order_contact = get_quote(6).contact
        return processor._process(order_contact)

    def test_customer_and_contact_found(self, setup_integration):
        def run_test(call_data, get_args):
            result_customer, result_contact = self.process_contact(setup_integration)
            assert result_customer is mock_dict[Customer]
            assert result_contact is mock_dict[Contact]
            assert not call_data[Customer, 'create'].called
            assert not call_data[Contact, 'create'].called
        with_mocks(run_test, basic_mocks)

    def test_customer_not_found(self, setup_integration):
        def run_test(call_data, get_args):
            with pytest.raises(Exception):
                self.process_contact(setup_integration)
        with_mocks(run_test, [
            *basic_mocks,
            DynamicsMock(Customer, 'get_first', exception=DynamicsNotFoundException(''))
        ])

    def test_create_customer(self, setup_integration):
        def run_test(call_data, get_args):
            setup_integration._exporter.erp_config.should_create_customer = True
            self.process_contact(setup_integration)
            assert call_data[Customer, 'create'].called
        with_mocks(run_test, [
            *basic_mocks,
            DynamicsMock(Customer, 'get_first', exception=DynamicsNotFoundException(''))
        ])

    def test_contact_not_found(self, setup_integration):
        def run_test(call_data, get_args):
            result_customer, result_contact = self.process_contact(setup_integration)
            assert not result_contact
        with_mocks(run_test, [
            *basic_mocks,
            DynamicsMock(Contact, 'get_first', exception=DynamicsNotFoundException(''))
        ])

    def test_create_contact(self, setup_integration):
        def run_test(call_data, get_args):
            setup_integration._exporter.erp_config.should_create_contact = True
            self.process_contact(setup_integration)
            assert call_data[Contact, 'create'].called
        with_mocks(run_test, [
            *basic_mocks,
            DynamicsMock(Contact, 'get_first', exception=DynamicsNotFoundException(''))
        ])
