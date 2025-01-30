import pytest

from baseintegration.integration import Integration
from globalshop.tests.test_integration import GSIntegrationTestClass
from paperless.objects.customers import AccountList, Account, Contact as \
    PaperlessContact, ContactList

from globalshop.importer.importer import GlobalShopAccountImporter
from globalshop.tests.test_connection import mock_conn_client
from globalshop.client import GlobalShopClient


class TestAccountImport:

    @pytest.fixture
    def setup_integration(self) -> Integration:
        integration = GSIntegrationTestClass()
        """Create integration and register the customer processor to process
        orders """
        # i = GlobalShopAccountImporter(integration)
        return integration

    @pytest.fixture()
    def setup_importer(self, setup_integration) -> GlobalShopAccountImporter:
        importer = GlobalShopAccountImporter(setup_integration)
        return importer

    @pytest.fixture()
    def setup_gs_client(self, mocker):
        mock_conn_client(mocker)
        client = GlobalShopClient(server_name='test', database='dbq',
                                  username='user1', password='pwd1')
        return client

    @pytest.fixture()
    def mock_get_customer(self, mocker):
        from globalshop.tests.test_customer import mock_fetchone, dummy_cus_row
        mock_fetchone(mocker, dummy_cus_row)

    @pytest.fixture()
    def mock_get_contact(self, mocker):
        from globalshop.tests.test_customer import mock_fetchall, \
            dummy_cont_rows
        mock_fetchall(mocker, dummy_cont_rows())

    @pytest.fixture()
    def mock_account_apis(self, mocker):
        mocker.patch.object(AccountList,
                            'filter',
                            return_value=[AccountList(name='test',
                                                      erp_code='ABC123',
                                                      id=123,
                                                      phone='5555555',
                                                      phone_ext='',
                                                      type='Customer')])
        mocker.patch.object(Account,
                            'create',
                            return_value=True)
        mocker.patch.object(Account,
                            'update',
                            return_value=True)
        mocker.patch.object(Account,
                            'get',
                            return_value=Account(name='test',
                                                      erp_code='ABC123',
                                                      id=123,
                                                      phone='5555555',
                                                      phone_ext='',
                                                      type='Customer'))

    @pytest.fixture()
    def mock_contact_apis(self, mocker):
        mocker.patch.object(PaperlessContact,
                            'filter',
                            return_value=[
                                ContactList(first_name='test',
                                            last_name='last',
                                            email='email@address.com',
                                            id=123,
                                            phone='5555555',
                                            phone_ext='',
                                            account_id=123,
                                            created='yesterday')])
        mocker.patch.object(PaperlessContact,
                            'create',
                            return_value=True)
        mocker.patch.object(PaperlessContact,
                            'update',
                            return_value=True)

    # @pytest.fixture()
    # def mock_salesperson_on_select(self,mocker):
    #     """
    #     If a salesperson is selected, return a dummy value, based on if it
    #     is in the cursor.execute sql command
    #     """
    #     sales_mocker = mocker
    #     global sales_mocker

    # mocker.patch.object(FakeCursor,'execute',
    #                     return_value=sales_side_effect)

    def test_get_integration(self, setup_integration):
        assert setup_integration

    def test_get_import(self, setup_importer):
        assert setup_importer

    def test_processor_accounts(self, setup_importer, setup_gs_client,
                                mock_get_customer, mock_get_contact,
                                mock_account_apis, mock_contact_apis):
        account_id = 'ABC123'
        # setup_importer._process_account(account_id=account_id)
        from globalshop.importer.processors.account import \
            AccountImportProcessor
        processor = AccountImportProcessor(setup_importer)
        customer_rec, account = processor._process_account(account_id)
        processor._process_contacts(customer_rec, pp_account_id=account.id)
        processor._process_salesperson(pp_account=account,
                                       gs_customer=customer_rec)
        # self._process_ship_tos(customer=customer_rec, account=account)
        # AccountImportProcessor._process_account(account_id=account_id)

    def test_import_ship_to(self):
        pass

    # def test_processor_contacts(self,setup_importer,setup_gs_client,
    #                             mock_get_contact):
    # setup_importer._process_account(account_id=account_id)
    # from paperless

    # def test_import_account(self,setup_integration):

    # def test_create_importer(self):
    #     AccountImporter()

    # def test_account_processor(self):
