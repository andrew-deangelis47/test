# import standard libraries
import os
import sys
import pytest
from paperless.objects.orders import OrderCostingVariable, OrderOperation
from paperless.objects.components import PurchasedComponent

# append to path
from visualestitrack.models import Quoteheader, Requestforquote, Inventory
from visualestitrack.exporter.processors.quote import CreateQuotePeripherals
from visualestitrack.importer.importer import VisualEstiTrackAccountListener

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))
from baseintegration.integration import Integration
from baseintegration.utils.test_utils import get_order, generate_random_string
from paperless.objects.customers import Account, Contact


@pytest.fixture
def setup_exporter():
    integration = Integration()
    from visualestitrack.exporter.exporter import VisualEstiTrackOrderExporter
    i = VisualEstiTrackOrderExporter(integration)
    return i


@pytest.fixture
def setup_importer_account():
    integration = Integration()
    from visualestitrack.importer.importer import VisualEstiTrackAccountImporter
    i = VisualEstiTrackAccountImporter(integration)
    return i


@pytest.fixture
def setup_importer_material():
    integration = Integration()
    from visualestitrack.importer.importer import VisualEstiTrackMaterialImporter
    i = VisualEstiTrackMaterialImporter(integration)
    return i


@pytest.mark.django_db
class TestVisualEstiTrack:
    """Runs tests against a dummy database using models.py"""

    def test_process_order(self, setup_exporter):
        passed = setup_exporter._process_order(get_order(1))
        assert passed

    def test_process_order_assembly(self, setup_exporter):
        passed = setup_exporter._process_order(get_order(25))
        assert passed

    def test_get_operations_costing_variables(self):
        work_center = OrderCostingVariable(label="Workcenter", variable_class="basic", value_type="string",
                                           value="PRFAB", row=None, options=None)
        rate_lookup = OrderCostingVariable(label="Rate Lookup", variable_class="table", value_type="number",
                                           value=27.95,
                                           row={
                                               "pop": 100.0,
                                               "name": "Programming - Fab",
                                               "ucost": 27.95,
                                               "inv_op": "PRFAB",
                                               "qty_time": 0.25,
                                               "labor_rate": 21.5,
                                               "row_number": 0,
                                               "burden_rate": 6.45
                                           }, options=None)
        total_cost = OrderCostingVariable(label="Total Rate ($)", variable_class="basic", value_type="currency",
                                          value=27.95, row=None, options=None)
        costing_variables = [work_center, rate_lookup, total_cost]
        laborrate, burdenrate, setuphourlyrate, workcentercode = \
            CreateQuotePeripherals.get_operations_costing_variables(costing_variables)

        assert laborrate == 21.5
        assert burdenrate == 6.45
        assert setuphourlyrate == 27.95
        assert workcentercode == 'PRFAB'
        work_center = OrderCostingVariable(label="Workcenter", variable_class="basic", value_type="string",
                                           value="PRFAB1", row=None, options=None)
        rate_lookup = OrderCostingVariable(label="Rate Lookup", variable_class="table", value_type="number",
                                           value=27.95,
                                           row={
                                               "pop": 100.0,
                                               "name": "Programming - Fab",
                                               "ucost": 27.95,
                                               "inv_op": "PRFAB1",
                                               "qty_time": 0.25,
                                               "labor_rate": 21.5,
                                               "row_number": 0,
                                               "burden_rate": 6.45
                                           }, options=None)
        total_cost = OrderCostingVariable(label="Total Rate ($)", variable_class="basic", value_type="currency",
                                          value=27.95, row=None, options=None)
        costing_variables = [work_center, rate_lookup, total_cost]
        laborrate, burdenrate, setuphourlyrate, workcentercode = \
            CreateQuotePeripherals.get_operations_costing_variables(costing_variables)

        assert laborrate == 21.5
        assert burdenrate == 6.45
        assert setuphourlyrate == 27.95
        assert workcentercode == 'PRFAB'

        costing_variables = []
        laborrate, burdenrate, setuphourlyrate, workcentercode = \
            CreateQuotePeripherals.get_operations_costing_variables(costing_variables)

        assert laborrate == 0.0
        assert burdenrate == 0.0
        assert setuphourlyrate == 0.0
        assert workcentercode == 'PP'

        work_center = OrderCostingVariable(label="Workcenter", variable_class="basic", value_type="string",
                                           value=None, row=None, options=None)

        costing_variables = [work_center]
        laborrate, burdenrate, setuphourlyrate, workcentercode = \
            CreateQuotePeripherals.get_operations_costing_variables(costing_variables)

        assert laborrate == 0.0
        assert burdenrate == 0.0
        assert setuphourlyrate == 0.0
        assert workcentercode == 'PP'

    def test_purchase_component_create(self):
        rfq = Requestforquote(
            id="6000",
            rfqdate="2000-11-11",
            processed=False,
            customername="name",
            customercode="code",
            customeraddressline1="add1",
            customeraddressline2="add2",
            customeraddressline3="add3",
            customeraddressline4="add4",
            salespersonname="sales_person_name",
            salespersonemail="sales_person_email")
        rfq.save()

        quote = Quoteheader(
            id="6000-1",
            requestforquoteid=rfq,
            parentquoteid="6000-1",
            subquotenum=0,
            quotedate=rfq.rfqdate,
            partdescription="des",
            extendedpartdescription="des_ext",
            revisionnumber="1",
            partnumber="part_number",
            internalnotes="private_notes",
            customernotes="public_notes",
            fginventoryno=''
        )
        quote.save()

        purchased_component = PurchasedComponent(oem_part_number="TestPurchased-04282021", internal_part_number="007-1",
                                                 description="TestPurchased-04282021", piece_price="1.0000",
                                                 properties=[])
        total_cost = OrderCostingVariable(label="Total Rate ($)", variable_class="basic", value_type="currency",
                                          value=27.95, row=None, options=None)
        operation = OrderOperation(id=3965999,
                                   category="operation",
                                   cost="6.00",
                                   costing_variables=[total_cost],
                                   is_finish=False,
                                   is_outside_service=False,
                                   name="PC Piece Price",
                                   operation_definition_name="PC Piece Price",
                                   notes=None,
                                   quantities=[],
                                   position=1,
                                   runtime=None,
                                   setup_time=None,
                                   operation_definition_erp_code='test_erp_code')
        shop_operations = [operation]
        CreateQuotePeripherals.create_peripheral_quote_purchase_component(quote.id, 1, purchased_component,
                                                                          shop_operations)

    def test_part_number_truncate(self):
        from visualestitrack.exporter.processors.quote import Utilities
        part_number_1 = Utilities.shorten_part_number('test_part_number')
        assert part_number_1 == 'test_part_number'
        part_number_2 = Utilities.shorten_part_number('test_part_number_lost_of_characters')
        assert part_number_2 == 'test_part_number_lost_of_char*'

    def test_split_part_description(self):
        from visualestitrack.exporter.processors.quote import Utilities
        description1 = 'Test Test Test'
        des1, des_ext1 = Utilities.split_part_description(description1)

        assert des1 == 'Test Test Test'
        assert des_ext1 == ''

        description2 = 'Test Test Test Test Test Test Test Test Test Test Test Test'
        des2, des_ext2 = Utilities.split_part_description(description2)

        assert des2 == 'Test Test Test Test Test Test Test Test Test T...'
        assert des_ext2 == 'est Test Test'

        description3 = None
        des3, des_ext3 = Utilities.split_part_description(description3)

        assert des3 is None
        assert des_ext3 == ''

    def test_split_rev_shorten(self):
        from visualestitrack.exporter.processors.quote import Utilities
        description1 = 'Tests Test Test'
        rev = Utilities.shorten_revision_number(description1)

        assert rev == 'Tests*'

    def test_get_op_type(self):
        from visualestitrack.exporter.processors.quote import CreateQuotePeripherals

        value1 = CreateQuotePeripherals.get_op_type(True)
        assert value1 == 'S'

        value2 = CreateQuotePeripherals.get_op_type(False)
        assert value2 == 'I'

        value3 = CreateQuotePeripherals.get_op_type()
        assert value3 == 'C'

    def test_materials_inventory(self, setup_importer_material):
        from visualestitrack.models import Materialtype
        assert setup_importer_material._process_material(material_id=1)
        mt1: Materialtype = Materialtype(materialcode='LFF1', description='This is material type 1')
        mt1.save()
        mt2: Materialtype = Materialtype(materialcode='LFF2', description='This is material type 2')
        mt2.save()
        mt3: Materialtype = Materialtype(materialcode='LFF3', description='This is material type 3')
        mt3.save()

        i1: Inventory = Inventory(id=1,
                                  inventory_number=' ITEM 1 - BODY',
                                  description='BODY',
                                  extendedpartdescription=0,
                                  piece_price=0.0,
                                  thickness=0.0,
                                  width=0.0,
                                  length=0.0,
                                  shape_code='',
                                  inventory=0,
                                  materialcode='LFF3')
        i1.save()
        assert setup_importer_material._process_material(material_id=1)

    def test_account(self, setup_importer_account):
        listener = VisualEstiTrackAccountListener(integration=setup_importer_account)
        from visualestitrack.models import Accounts, Facilities, Contacts
        new_acct = generate_random_string(length=7)
        in_new_acct = f'IN{new_acct}'
        account: Accounts = Accounts(credit_line='132465',
                                     estitrack_account_id=new_acct,
                                     notes='Test account notes',
                                     payment_terms='Net 30 Days ',
                                     phone='6028846528',
                                     phone_ext='65',
                                     url='cool.com',
                                     address1='1 Cool St.',
                                     address2='',
                                     city='Manchester',
                                     country='USA',
                                     postal_code='03105',
                                     state='NY')
        account.save()
        facility: Facilities = Facilities(name=new_acct,
                                          attention=f'cool Tech Inc. {new_acct}',
                                          estitrack_account_id=new_acct,
                                          address1='1 Cool St.',
                                          address2='',
                                          city='Manchester',
                                          country='USA',
                                          postal_code='03105',
                                          state='NY')
        facility.save()
        account_copy: Accounts = Accounts(credit_line='132465',
                                          estitrack_account_id=f'{new_acct}_copy',
                                          notes='Test account notes',
                                          payment_terms='Net 30 Days ',
                                          phone='6028846528',
                                          phone_ext='65',
                                          url='cool.com',
                                          address1='1 Cool St.',
                                          address2='',
                                          city='Manchester',
                                          country='USA',
                                          postal_code='03105',
                                          state='NY')
        account_copy.save()
        facility_copy: Facilities = Facilities(name=f'{new_acct}_copy',
                                               attention=f'cool Tech Inc. {new_acct}',
                                               estitrack_account_id=f'{new_acct}_copy',
                                               address1='1 Cool St.',
                                               address2='',
                                               city='Manchester',
                                               country='USA',
                                               postal_code='03105',
                                               state='NY')
        facility_copy.save()
        account1: Accounts = Accounts(credit_line='132465',
                                      estitrack_account_id=in_new_acct,
                                      notes='Test account notes',
                                      payment_terms='C.O.D.',
                                      phone='6028846528',
                                      phone_ext='65',
                                      url='cool.com',
                                      address1='1 Cool St.',
                                      address2='',
                                      city='Manchester',
                                      country='',
                                      postal_code='',
                                      state='')
        account1.save()
        facility1: Facilities = Facilities(name=new_acct,
                                           attention=f'cool Tech Inc. {in_new_acct}',
                                           estitrack_account_id=in_new_acct,
                                           address1='1 Cool St.',
                                           address2='',
                                           city='Manchester',
                                           country='',
                                           postal_code='',
                                           state='')
        facility1.save()
        contact1: Contacts = Contacts(email=f'cool1{new_acct}@paperless.com',
                                      name=f'Cool Man {new_acct}',
                                      notes='Cool tech Contact',
                                      phone='6028846528',
                                      phone_ext='65',
                                      address1='1 Cool St.',
                                      address2='',
                                      city='Manchester',
                                      country='USA',
                                      postal_code='03105',
                                      state='NY',
                                      customercode=new_acct)
        contact1.save()
        contact2: Contacts = Contacts(email=f'cool2{new_acct}@paperless.com',
                                      name=f'Cool Man {new_acct}',
                                      notes='Cool tech Contact',
                                      phone='6028846528',
                                      phone_ext='65',
                                      address1='1 Cool St.',
                                      address2='',
                                      city='Manchester',
                                      country='',
                                      postal_code='',
                                      state='',
                                      customercode=new_acct)
        contact2.save()
        contact3: Contacts = Contacts(email='',
                                      name=f'Bad Cool Man {new_acct}',
                                      notes='Cool tech Contact',
                                      phone='6028846528',
                                      phone_ext='65',
                                      address1='1 Cool St.',
                                      address2='',
                                      city='Manchester',
                                      country='USA',
                                      postal_code='03105',
                                      state='NY',
                                      customercode=new_acct)
        contact3.save()
        contact4: Contacts = Contacts(email='bad',
                                      name=f'Bad Cool Man {new_acct}',
                                      notes='Cool tech Contact',
                                      phone='6028846528',
                                      phone_ext='65',
                                      address1='1 Cool St.',
                                      address2='',
                                      city='Manchester',
                                      country='USA',
                                      postal_code='03105',
                                      state='NY',
                                      customercode=new_acct)
        contact4.save()
        contact5: Contacts = Contacts(email=f'cool1{in_new_acct}@paperless.com',
                                      name=f'Cool Man {in_new_acct}',
                                      notes='Cool tech Contact',
                                      phone='6028846528',
                                      phone_ext='65',
                                      address1='1 Cool St.',
                                      address2='',
                                      city='Manchester',
                                      country='USA',
                                      postal_code='03105',
                                      state='NY',
                                      customercode=in_new_acct)
        contact5.save()
        contact6: Contacts = Contacts(email=f'cool1{new_acct}@paperless.com',
                                      name=f'Cool Man {in_new_acct}',
                                      notes='Cool tech Contact',
                                      phone='6028846528',
                                      phone_ext='65',
                                      address1='1 Cool St.',
                                      address2='',
                                      city='Manchester',
                                      country='USA',
                                      postal_code='03105',
                                      state='NY',
                                      customercode=in_new_acct)
        contact6.save()
        list_to_process = listener.get_new()
        assert len(list_to_process) == 3
        assert setup_importer_account._process_account(account_id=new_acct)
        assert setup_importer_account._process_account(account_id=in_new_acct)
        account1.address1 = '1 Cool St.'
        account1.city = 'Manchester'
        account1.country = 'USA'
        account1.postal_code = '03101'
        account1.state = 'NH'
        account1.save()
        facility1.address1 = '1 Cool St.'
        facility1.city = 'Manchester'
        facility1.country = 'USA'
        facility1.postal_code = '03101'
        facility1.state = 'NH'
        facility1.save()
        assert setup_importer_account._process_account(account_id=new_acct)
        assert setup_importer_account._process_account(account_id=f'{new_acct}_copy')
        assert setup_importer_account._process_account(account_id=in_new_acct)
        accts = Account.filter(erp_code=new_acct)
        assert len(accts) > 0
        account = Account.get(accts[0].id)
        from visualestitrack.importer.processors.accounts import AccountImportProcessor
        AccountImportProcessor.set_payment_terms(account_id=account.id, vet_account=account, pp_account=account)
        pp_contacts_list = Contact.filter(account_id=account.id)
        assert len(pp_contacts_list) > 1
        list_to_process_after = listener.get_new()
        assert len(list_to_process_after) == 0
        for c in pp_contacts_list:
            con: Contact = Contact.get(id=c.id)
            assert new_acct in con.first_name
            con.delete()
        account.delete()

    def test_testing_works(self):
        assert True is True
        assert False is False

    def test_is_excluded_operation(self):
        ex_list = ['exclude']
        assert CreateQuotePeripherals.is_excluded_operation('exclude_op', ex_list) is True
        assert CreateQuotePeripherals.is_excluded_operation('op_exclude_op', ex_list) is True
        assert CreateQuotePeripherals.is_excluded_operation('op_exclude_op', ex_list) is True
        assert CreateQuotePeripherals.is_excluded_operation('op', ex_list) is False
