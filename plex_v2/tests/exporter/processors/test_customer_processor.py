from plex_v2.exporter.processors.customer import CustomerProcessor
from plex_v2.configuration import PlexConfig
from types import SimpleNamespace
from unittest.mock import create_autospec
from baseintegration.integration.integration_export_report import IntegrationExportReport
from paperless.objects.orders import OrderAccount
from plex_v2.utils.export import ExportUtils
from plex_v2.factories.plex.customer import PlexCustomerFactory
from plex_v2.objects.customer import Customer
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException


class TestApprovedSupplierDatasourceProcessor:

    def setup_method(self):
        integration_report = create_autospec(IntegrationExportReport)
        integration_report.update_table.return_value = True

        self.processor = CustomerProcessor(SimpleNamespace(
            erp_config=PlexConfig(),
            integration_report=integration_report
        ))

        self.order_account = create_autospec(OrderAccount)
        self.order_account.erp_code = 'erp_code'
        self.order_account.name = 'account_name'
        self.utils = create_autospec(ExportUtils)
        self.customer_factory = create_autospec(PlexCustomerFactory)
        self.plex_customer = create_autospec(Customer)
        self.plex_customer.name = 'name'
        self.plex_customer.code = 'code'

    def test_customer_processor_creates_customer_if_not_existing_and_creation_enabled(self):
        config = PlexConfig(
            can_creat_new_customers=True
        )
        self.processor.config = config
        self.utils.get_plex_customer_by_code_or_name.return_value = None

        created_customer = create_autospec(Customer)
        created_customer.name = 'created_cust_name'
        created_customer.code = 'created_cust_code'
        self.customer_factory.to_plex_customer.return_value = created_customer

        self.processor._process(
            self.order_account,
            self.utils,
            self.customer_factory
        )

        created_customer.create.assert_called_once()

    def test_customer_processor_throws_exception_if_not_existing_and_creation_disabled(self):
        config = PlexConfig(
            can_creat_new_customers=False
        )
        self.processor.config = config
        self.utils.get_plex_customer_by_code_or_name.return_value = None

        try:
            self.processor._process(
                self.order_account,
                self.utils,
                self.customer_factory
            )
        # checking exception thrown with right message
        except CancelledIntegrationActionException as e:
            assert str(e) == 'Customer does not exist in Plex and creation is disabled. Will not export'
