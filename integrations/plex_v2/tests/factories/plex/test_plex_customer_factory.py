from plex_v2.factories.plex.customer import PlexCustomerFactory
from plex_v2.configuration import PlexConfig
from unittest.mock import create_autospec
from plex_v2.utils.export import ExportUtils
from paperless.objects.customers import Account


class TestPlexCustomerFactory:

    VALID_ACCOUNT_NAME = 'VALID_ACCOUNT_NAME'
    VALID_ACCOUNT_ERP_CODE = 'VALID_ACCOUNT_ERP_CODE'
    VALID_ACCOUNT_NOTES = 'VALID_ACCOUNT_NOTES'
    VALID_DEFAULT_CUSTOMER_STATUS = 'VALID_DEFAULT_CUSTOMER_STATUS'
    VALID_DEFAULT_CUSTOMER_TYPE = 'VALID_DEFAULT_CUSTOMER_TYPE'

    def setup_method(self):
        self.config = create_autospec(PlexConfig)
        self.config.default_customer_status = self.VALID_DEFAULT_CUSTOMER_STATUS
        self.config.default_customer_type = self.VALID_DEFAULT_CUSTOMER_TYPE

        self.utils = create_autospec(ExportUtils)

        self.factory = PlexCustomerFactory(
            config=self.config,
            utils=self.utils
        )

        self.account = create_autospec(Account)
        self.account.name = self.VALID_ACCOUNT_NAME
        self.account.erp_code = self.VALID_ACCOUNT_ERP_CODE
        self.account.notes = self.VALID_ACCOUNT_NOTES

    def test_to_plex_customer_sets_name_to_account_name(self):
        customer = self.factory.to_plex_customer(
            self.account
        )

        assert customer.name == self.account.name

    def test_to_plex_customer_sets_code_to_account_erp_code_if_not_none(self):
        customer = self.factory.to_plex_customer(
            self.account
        )

        assert customer.code == self.account.erp_code

    def test_to_plex_customer_sets_code_to_account_name_if_erp_code_is_none(self):
        self.account.erp_code = None
        customer = self.factory.to_plex_customer(
            self.account
        )

        assert customer.code == self.account.name

    def test_to_plex_customer_sets_status_to_default_status_in_config(self):
        customer = self.factory.to_plex_customer(
            self.account
        )

        assert customer.status == self.config.default_customer_status

    def test_to_plex_customer_sets_type_to_default_type_in_config(self):
        customer = self.factory.to_plex_customer(
            self.account
        )

        assert customer.type == self.config.default_customer_type

    def test_to_plex_customer_sets_note_to_account_notes_if_not_none(self):
        customer = self.factory.to_plex_customer(
            self.account
        )

        assert customer.note == self.account.notes

    def test_to_plex_customer_sets_note_to_blank_string_if_account_notes_is_none(self):
        self.account.notes = None
        customer = self.factory.to_plex_customer(
            self.account
        )

        assert customer.note == ""
