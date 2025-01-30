from plex_v2.exporter.processors.customer_address import CustomerAddressProcessor
from plex_v2.configuration import PlexConfig
from types import SimpleNamespace
from unittest.mock import create_autospec
from baseintegration.integration.integration_export_report import IntegrationExportReport
from plex_v2.factories.plex.customer_address import PlexCustomerAddressFactory
from plex_v2.objects.customer import Customer
from plex_v2.utils.export import ExportUtils
from paperless.objects.orders import AddressInfo
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException


class TestCustomerAddressProcessor:

    def setup_method(self):
        integration_report = create_autospec(IntegrationExportReport)
        integration_report.update_table.return_value = True

        self.processor = CustomerAddressProcessor(SimpleNamespace(
            erp_config=PlexConfig(),
            integration_report=integration_report
        ))

        self.customer = create_autospec(Customer)
        self.utils = create_autospec(ExportUtils)
        self.factory = create_autospec(PlexCustomerAddressFactory)
        self.address_info = create_autospec(AddressInfo)
        self.address_functions = []

    def test_customer_address_processor_throws_exception_if_no_address_info_on_order_and_not_configured_to_use_existing_addresses(self):
        config = PlexConfig(
            use_plex_address_as_fallback=False
        )
        self.processor.config = config
        code_suffix = 'Shipping'

        try:
            self.processor._process(
                self.customer,
                self.utils,
                self.factory,
                None,
                self.address_functions,
                code_suffix,
            )
        except CancelledIntegrationActionException as e:
            assert str(e) == f'No {code_suffix} address on the Paperless Parts order and integration is not configured to use Plex address as fallback'
            return

        # if it makes it here then it means the exception was not thrown
        assert False

    def test_customer_address_processor_uses_existing_plex_addr_if_no_address_info_on_order_and_configured_to_use_existing_addresses(self):
        config = PlexConfig(
            use_plex_address_as_fallback=True
        )
        self.processor.config = config
        code_suffix = 'Shipping'

        self.processor._process(
            self.customer,
            self.utils,
            self.factory,
            None,
            self.address_functions,
            code_suffix,
        )

        self.utils.get_existing_plex_address.assert_called_once()

    def test_customer_address_processor_gets_plex_addr_by_facility_name_if_has_facility_name(self):
        self.utils.has_facility_name.return_value = True

        code_suffix = 'Shipping'

        self.processor._process(
            self.customer,
            self.utils,
            self.factory,
            'non none value',
            self.address_functions,
            code_suffix,
        )

        self.utils.use_facility_name_to_get_address.assert_called_once()

    def test_customer_address_processor_tries_to_use_alt_code_to_match_plex_addr_if_does_not_have_facility_name(self):
        self.utils.has_facility_name.return_value = False

        code_suffix = 'Shipping'

        self.processor._process(
            self.customer,
            self.utils,
            self.factory,
            'non none value',
            self.address_functions,
            code_suffix,
        )

        self.utils.get_customer_address_by_alt_code.assert_called_once()

    def test_customer_address_processor_creates_plex_addr_if_it_cannot_find_match_on_facility_name_or_alt_code(self):
        self.utils.has_facility_name.return_value = False
        self.utils.get_customer_address_by_alt_code.return_value = None

        code_suffix = 'Shipping'

        self.processor._process(
            self.customer,
            self.utils,
            self.factory,
            'non none value',
            self.address_functions,
            code_suffix,
        )

        self.factory.to_plex_customer_address.assert_called_once()
        self.utils.create_address_if_no_match.assert_called_once()
