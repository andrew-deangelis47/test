import random
from types import SimpleNamespace

import pytest
from paperless.objects.customers import Account, Contact as PaperlessContact

from baseintegration.integration import Integration
from dynamics.objects.customer import Customer, Contact, PaymentTerm, CountryCode
from dynamics.tests.utils import with_mocks, get_object_mocks


@pytest.fixture
def setup_integration():
    integration = Integration()
    from dynamics.importer.importer import DynamicsAccountImporter
    return DynamicsAccountImporter(integration)


cust_num = str(random.randint(1, 10000))
customer_name = cust_num + " Company"

mock_dict = {
    Customer: Customer(
        No=cust_num,
        Name=customer_name,
        Home_Page='test',
        Payment_Terms_Code='test',
        Gen_Bus_Posting_Group='test',
        Customer_Posting_Group='test',
        Tax_Area_Code='test',
        E_Mail='test@test.com',
        Phone_No='test',
        Address='test',
        Address_2='test',
        City='test',
        County='MA',
        Post_Code='11111',
        Country_Region_Code='test'
    ),
    Contact: Contact(
        No='test',
        Company_Name=customer_name,
        Type='Person',
        Name='test',
        First_Name='test',
        Surname='test',
        E_Mail='test@test.com',
        Phone_No='test',
        Address='test',
        Address_2='test',
        City='test',
        County='MA',
        Post_Code='11111',
        Country_Region_Code='test'
    ),
    PaymentTerm: SimpleNamespace(
        Due_Date_Calculation='30D'
    ),
    CountryCode: SimpleNamespace(
        Name='USA'
    )
}


basic_mocks = get_object_mocks(mock_dict)


class TestDynamicsAccountImport:
    @staticmethod
    def get_account(erp_code):
        accounts = Account.filter(erp_code=erp_code)
        account = None
        for acct in accounts:
            if acct.erp_code == cust_num:
                account = Account.get(acct.id)
        return account

    @staticmethod
    def get_contact(account):
        contact = None
        contacts = PaperlessContact.filter(account_id=account.id)
        if len(contacts) > 0:
            contact = PaperlessContact.get(id=contacts[0].id)
        return contact

    def test_import_account(self, setup_integration):
        def run_test(call_data, get_args):
            # create account and contact

            setup_integration.run(account_id=cust_num)

            account = self.get_account(cust_num)
            assert account is not None
            assert account.payment_terms_period == 30

            contact = self.get_contact(account)
            assert contact is not None

            # update contact

            mock_dict[Contact].First_Name = 'test2'

            setup_integration.run(account_id=cust_num)

            contact = self.get_contact(account)
            assert contact.first_name == 'test2'

            # update account

            mock_dict[Customer].Address = 'test2'

            setup_integration.run(account_id=cust_num)

            account = self.get_account(cust_num)
            assert account.sold_to_address.address1 == 'test2'

            contact.delete()
            account.delete()

        with_mocks(run_test, basic_mocks)
