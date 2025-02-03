import os
import sys
import pytest
import json

# append to path
from baseintegration.utils.test_utils import get_order
from m1.exporter.processors.jobs import ProcessJobs
from m1.exporter.processors.sales_orders import ProcessSalesOrder
from m1.exporter.processors.utils import PartUtils
from m1.exporter.processors.organizations import ProcessOrganization
from m1.importer.processors.accounts import AccountImportProcessor
from m1.models import Organizations, Organizationlocations, Organizationcontacts, Partrevisions, Paymentterms, Parts
from paperless.objects.customers import Account, Contact
from paperless.objects.orders import OrderComponent, OrderCostingVariable, OrderOperation, Order

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))

# import models
from baseintegration.integration import Integration


@pytest.fixture
def setup_exporter():
    """Create integration to process orders"""
    integration = Integration()
    from m1.exporter.exporter import M1OrderExporter
    i = M1OrderExporter(integration)
    return i


@pytest.fixture
def setup_importer_account():
    integration = Integration()
    from m1.importer.importer import M1AccountImporter
    i = M1AccountImporter(integration)
    return i


@pytest.mark.django_db
class TestM1OrderExport:

    def test_process_assembly_order(self, setup_exporter):
        passed = setup_exporter._process_order(get_order(25))
        assert passed

    def test_process_alpha_numeric_order(self, setup_exporter):
        passed = setup_exporter._process_order(get_order(1))
        assert passed
        passed = setup_exporter._process_order(get_order(1))
        assert passed is False

    def test_process_no_erp_code_order(self, setup_exporter):
        order: Order = get_order(26)
        account = Account.get(order.contact.account.id)
        org_code = account.erp_code
        account.erp_code = None
        account.update()
        passed = setup_exporter._process_order(get_order(26))
        assert passed
        account.erp_code = org_code
        account.update()

    def test_convert_pp_payment_terms(self, setup_exporter):
        Paymentterms.objects.create(
            xatpaymenttermid='NET30',
            xatdescription='NET 30 days',
            xatdaysdue=30,
            xatdiscountdays=0,
            xatdiscountpercent=0.00,
            xatgraceperiod=0,
            xatcalculationtype=0,
            xatimmediatepaymentrequired=False,
            xatcalculationdayofmonth=0,
            xatdiscountdayofmonth=0,
        )
        assert 'NET30' == ProcessSalesOrder.convert_pp_payment_terms(term='Net 30')
        assert None is ProcessSalesOrder.convert_pp_payment_terms(term=None)

    def test_generate_m1_org_id(self, setup_exporter):
        org_id = ProcessOrganization.generate_m1_org_id(erp_code='  Hello  World   From Pankaj \t\n\r\tHi There  ')
        assert org_id == 'HELLOWORLD'

    def test_jobs_create_material_job_materials(self, setup_exporter):
        material = OrderCostingVariable(label="Material Type", variable_class="basic", value_type="string",
                                        value="Test Steel", row=None, options=None)
        mop = OrderOperation(costing_variables=[material], name='Customer Supplied test Steel', id=2135,
                             category='material', cost=1000.00, is_finish=False, is_outside_service=False,
                             operation_definition_name='Material Operation', notes='', position=1, quantities=[],
                             runtime=30.00, setup_time=2.00, operation_definition_erp_code='test_erp_code')
        mop2 = OrderOperation(costing_variables=[], name='Customer Supplied test Steel', id=2135,
                              category='material', cost=1000.00, is_finish=False, is_outside_service=False,
                              operation_definition_name='Material Operation', notes='', position=1, quantities=[],
                              runtime=30.00, setup_time=2.00, operation_definition_erp_code='test_erp_code')

        assert 1 == ProcessJobs.create_material_job_materials(job_id='TEST', material_operations=[mop, mop2])


@pytest.mark.django_db
class TestM1PartCrud:
    def test_component_part_crud(self):
        with open(os.path.join(os.path.dirname(__file__), "test-data/order_component.json"), 'r') as f:
            mock_order_component_json = json.load(f)
        mock_order_component = OrderComponent(**mock_order_component_json)

        PartUtils.get_create_component_part(component=mock_order_component)

        with open(os.path.join(os.path.dirname(__file__), "test-data/order_component2.json"), 'r') as f:
            mock_order_component_json2 = json.load(f)
        mock_order_component2 = OrderComponent(**mock_order_component_json2)

        PartUtils.get_create_component_part(component=mock_order_component2)

        revs: [Partrevisions] = Partrevisions.objects.filter(imrpartid=mock_order_component2.part_number, )

        assert len(revs) == 2

        with open(os.path.join(os.path.dirname(__file__), "test-data/order_component3.json"), 'r') as f:
            mock_order_component_json3 = json.load(f)
        mock_order_component3 = OrderComponent(**mock_order_component_json3)

        PartUtils.get_create_component_part(component=mock_order_component3)

    def test_placeholder_part_crud(self):
        PartUtils.get_create_placeholder_parts(part_number='place_test1', short_description='test test',
                                               long_description='test test test')

        PartUtils.get_create_placeholder_parts(part_number='place_test1', short_description='test test',
                                               long_description='test test test')
        assert 1 == len(Parts.objects.filter(imppartid='place_test1'))
        assert 1 == len(Partrevisions.objects.filter(imrpartid='place_test1', imrpartrevisionid=''))


@pytest.mark.django_db
class TestM1AccountImports:
    def test_process_account(self, setup_importer_account):
        org: Organizations = Organizations.objects.create(
            cmoorganizationid='M1T',
            cmoname='Test TEST M1',
            cmoaddressline1='213 Test ave.',
            cmoaddressline2='unit 45',
            cmoaddressline3='',
            cmocity='Mach Vegas',
            cmostate='NH',
            cmopostcode='03152',
            cmocountry='USA',
            cmophonenumber='3256987410',
            cmowebaddress='test.com',
            cmoprintstatement=False,
            cmoemployeecount=0,
            cmofinancecompany=False,
            cmocompetitor=False,
            cmolongdescriptionrtf='test notest',
            cmolongdescriptiontext='test notest',
            cmocustomerstatus=2,
            cmosupplierstatus=0,
            cmorequires1099=False,
            cmosuppliertaxable=False,
            cmocustomertaxable=False,
            cmocalculatefinancecharges=False,
            cmoincludefreightinprice=False,
            cmocredithold=False,
            cmocustomercreditlimit=56378.00,
            cmodirectpayment=False,
            cmoarinvoicepershipmentline=False,
            cmocreatedfromweb=False,
            cmoresellerstatus=0,
            cmoresellercommissionrate=0.00,
            cmorequiresinspection=False,
            cmoresidentialaddress=False,
            cmosupplieraccredited=False,
            cmocreatedby='ppadmin',
            cmoapincludetaxinretention=False,
            cmoarincludetaxinretention=False,
            cmoform1099box=0,
            cmoavalaraaddressvalidated=False,
            cmocontractor=False,
            cmotaxreportable=False,
            cmocreatedfrommobile=False,
            cmoignoreavalara=False,
            cmosuperfund=False,
            cmoupsvalidated=False,
            cmobarecostofduty=False,
            cmobaretransportationcost=False,
            cmoediintegrated=False,
            cmosplitpercenttotal=0.00,
            cmoexpensesplitpercenttotal=0.00,
            cmojobpriorityid=0
        )

        Organizationlocations.objects.create(
            cmlorganizationid=org.cmoorganizationid,
            cmllocationid='',
            cmlname='Test Test',
            cmladdressline1=org.cmoaddressline1,
            cmladdressline2=org.cmoaddressline2,
            cmlcity=org.cmocity,
            cmlstate=org.cmostate,
            cmlpostcode=org.cmopostcode,
            cmlcountry=org.cmocountry,
            cmlphonenumber=org.cmophonenumber,
            cmlquotelocation=True,
            cmlshiplocation=False,
            cmlarinvoicelocation=False,
            cmlpurchaselocation=False,
            cmlapinvoicelocation=False,
            cmlcustomertaxable=org.cmocustomertaxable,
            cmlarinvoicepershipmentline=False,
            cmlinactive=False,
            cmlresidentialaddress=False,
            cmlcreditcheckforlocation=False,
            cmlcustomercreditlimit=org.cmocustomercreditlimit,
            cmlcredithold=False,
            cmldirectpayment=False,
            cmlcreatedby='ppadmin',
            cmlavalaraaddressvalidated=False,
            cmlcontractor=False,
            cmltaxreportable=False,
            cmlcreatedfrommobile=False,
            cmlbarecostofduty=False,
            cmlbaretransportationcost=False,
            cmlignoreavalara=False,
            cmlupsvalidated=False,
            cmlediintegrated=False,
            cmlsplitpercenttotal=0.00
        )

        Organizationlocations.objects.create(
            cmlorganizationid=org.cmoorganizationid,
            cmllocationid='Test1',
            cmlname='Test Test1',
            cmladdressline1=org.cmoaddressline1,
            cmladdressline2=org.cmoaddressline2,
            cmlcity=org.cmocity,
            cmlstate=org.cmostate,
            cmlpostcode=org.cmopostcode,
            cmlcountry=org.cmocountry,
            cmlphonenumber=org.cmophonenumber,
            cmlquotelocation=False,
            cmlshiplocation=False,
            cmlarinvoicelocation=False,
            cmlpurchaselocation=False,
            cmlapinvoicelocation=False,
            cmlcustomertaxable=org.cmocustomertaxable,
            cmlarinvoicepershipmentline=False,
            cmlinactive=False,
            cmlresidentialaddress=False,
            cmlcreditcheckforlocation=False,
            cmlcustomercreditlimit=org.cmocustomercreditlimit,
            cmlcredithold=False,
            cmldirectpayment=False,
            cmlcreatedby='ppadmin',
            cmlavalaraaddressvalidated=False,
            cmlcontractor=False,
            cmltaxreportable=False,
            cmlcreatedfrommobile=False,
            cmlbarecostofduty=False,
            cmlbaretransportationcost=False,
            cmlignoreavalara=False,
            cmlupsvalidated=False,
            cmlediintegrated=False,
            cmlsplitpercenttotal=0.00
        )

        Organizationlocations.objects.create(
            cmlorganizationid=org.cmoorganizationid,
            cmllocationid='Test2',
            cmlname='Test Test2',
            cmladdressline1=org.cmoaddressline1,
            cmladdressline2=org.cmoaddressline2,
            cmlcity=' ',
            cmlstate='OHI',
            cmlpostcode='35612168',
            cmlcountry=org.cmocountry,
            cmlphonenumber=org.cmophonenumber,
            cmlquotelocation=False,
            cmlshiplocation=False,
            cmlarinvoicelocation=False,
            cmlpurchaselocation=False,
            cmlapinvoicelocation=False,
            cmlcustomertaxable=org.cmocustomertaxable,
            cmlarinvoicepershipmentline=False,
            cmlinactive=False,
            cmlresidentialaddress=False,
            cmlcreditcheckforlocation=False,
            cmlcustomercreditlimit=org.cmocustomercreditlimit,
            cmlcredithold=False,
            cmldirectpayment=False,
            cmlcreatedby='ppadmin',
            cmlavalaraaddressvalidated=False,
            cmlcontractor=False,
            cmltaxreportable=False,
            cmlcreatedfrommobile=False,
            cmlbarecostofduty=False,
            cmlbaretransportationcost=False,
            cmlignoreavalara=False,
            cmlupsvalidated=False,
            cmlediintegrated=False,
            cmlsplitpercenttotal=0.00
        )

        Organizationlocations.objects.create(
            cmlorganizationid=org.cmoorganizationid,
            cmllocationid='Test3',
            cmlname='Test Test3',
            cmladdressline1=org.cmoaddressline1,
            cmladdressline2=org.cmoaddressline2,
            cmlcity=' ',
            cmlstate='OHI',
            cmlpostcode='35612168',
            cmlcountry=org.cmocountry,
            cmlphonenumber=org.cmophonenumber,
            cmlquotelocation=True,
            cmlshiplocation=False,
            cmlarinvoicelocation=False,
            cmlpurchaselocation=False,
            cmlapinvoicelocation=False,
            cmlcustomertaxable=org.cmocustomertaxable,
            cmlarinvoicepershipmentline=False,
            cmlinactive=False,
            cmlresidentialaddress=False,
            cmlcreditcheckforlocation=False,
            cmlcustomercreditlimit=org.cmocustomercreditlimit,
            cmlcredithold=False,
            cmldirectpayment=False,
            cmlcreatedby='ppadmin',
            cmlavalaraaddressvalidated=False,
            cmlcontractor=False,
            cmltaxreportable=False,
            cmlcreatedfrommobile=False,
            cmlbarecostofduty=False,
            cmlbaretransportationcost=False,
            cmlignoreavalara=False,
            cmlupsvalidated=False,
            cmlediintegrated=False,
            cmlsplitpercenttotal=0.00
        )

        Organizationlocations.objects.create(
            cmlorganizationid=org.cmoorganizationid,
            cmllocationid='Test4',
            cmlname='Test Test1',
            cmladdressline1=org.cmoaddressline1,
            cmladdressline2=org.cmoaddressline2,
            cmlcity=org.cmocity,
            cmlstate=org.cmostate,
            cmlpostcode=org.cmopostcode,
            cmlcountry=org.cmocountry,
            cmlphonenumber=org.cmophonenumber,
            cmlquotelocation=False,
            cmlshiplocation=False,
            cmlarinvoicelocation=False,
            cmlpurchaselocation=False,
            cmlapinvoicelocation=False,
            cmlcustomertaxable=org.cmocustomertaxable,
            cmlarinvoicepershipmentline=False,
            cmlinactive=False,
            cmlresidentialaddress=False,
            cmlcreditcheckforlocation=False,
            cmlcustomercreditlimit=org.cmocustomercreditlimit,
            cmlcredithold=False,
            cmldirectpayment=False,
            cmlcreatedby='ppadmin',
            cmlavalaraaddressvalidated=False,
            cmlcontractor=False,
            cmltaxreportable=False,
            cmlcreatedfrommobile=False,
            cmlbarecostofduty=False,
            cmlbaretransportationcost=False,
            cmlignoreavalara=False,
            cmlupsvalidated=False,
            cmlediintegrated=False,
            cmlsplitpercenttotal=0.00
        )

        Organizationcontacts.objects.create(
            cmcorganizationid=org.cmoorganizationid,
            cmclocationid='',
            cmccontactid='test1',
            cmcname='test test',
            cmcphonenumber=org.cmophonenumber,
            cmcemailaddress='test+m1@paperlessparts.com',
            cmcwebloginenabled=False,
            cmcnomailings=False,
            cmcnotertf='test',
            cmcnotetext='test',
            cmcinactive=False,
            cmccreatedfrommobile=False,
            cmccreatedby='ppadmin',
            cmceasyorderenabled=False,
            cmccreatedbyeasyorder=False,
            cmceoeditshippingaddress=False,
            cmceoreceiveemails=False,
            cmceohtmlmail=False,
            cmceoreminderofopenorders=False,
            cmceoorderauthorisationmessage=False,
            cmceoauthorisationrequest=False,
            cmceomaynotcreordtemp=False,
        )

        Organizationcontacts.objects.create(
            cmcorganizationid=org.cmoorganizationid,
            cmclocationid='',
            cmccontactid='test2',
            cmcname='test test invalid',
            cmcphonenumber=org.cmophonenumber,
            cmcemailaddress='test+m1@paperlessparts.com',
            cmcwebloginenabled=False,
            cmcnomailings=False,
            cmcnotertf='test',
            cmcnotetext='test',
            cmcinactive=False,
            cmccreatedfrommobile=False,
            cmccreatedby='ppadmin',
            cmceasyorderenabled=False,
            cmccreatedbyeasyorder=False,
            cmceoeditshippingaddress=False,
            cmceoreceiveemails=False,
            cmceohtmlmail=False,
            cmceoreminderofopenorders=False,
            cmceoorderauthorisationmessage=False,
            cmceoauthorisationrequest=False,
            cmceomaynotcreordtemp=False,
        )

        Organizationcontacts.objects.create(
            cmcorganizationid=org.cmoorganizationid,
            cmclocationid='',
            cmccontactid='test3',
            cmcname='test test duplicate',
            cmcphonenumber=org.cmophonenumber,
            cmcemailaddress='',
            cmcwebloginenabled=False,
            cmcnomailings=False,
            cmcnotertf='test',
            cmcnotetext='test',
            cmcinactive=False,
            cmccreatedfrommobile=False,
            cmccreatedby='ppadmin',
            cmceasyorderenabled=False,
            cmccreatedbyeasyorder=False,
            cmceoeditshippingaddress=False,
            cmceoreceiveemails=False,
            cmceohtmlmail=False,
            cmceoreminderofopenorders=False,
            cmceoorderauthorisationmessage=False,
            cmceoauthorisationrequest=False,
            cmceomaynotcreordtemp=False,
        )

        Paymentterms.objects.create(
            xatpaymenttermid='NET10',
            xatdescription='NET 10 days',
            xatdaysdue=10,
            xatdiscountdays=0,
            xatdiscountpercent=0.00,
            xatgraceperiod=0,
            xatcalculationtype=0,
            xatimmediatepaymentrequired=False,
            xatcalculationdayofmonth=0,
            xatdiscountdayofmonth=0,
        )

        passed = setup_importer_account._process_account(account_id='M1T')
        assert passed
        org.cmopostcode = '5463587'
        org.cmostate = 'ARK'
        org.save()
        passed = setup_importer_account._process_account(account_id='M1T')
        assert passed
        accts = Account.filter(erp_code='M1T')
        assert len(accts) > 0
        account = Account.get(accts[0].id)
        account.erp_code = None
        account.update()
        passed = setup_importer_account._process_account(account_id='M1T')
        assert passed
        org.cmoorganizationid = 'M1T2'
        org.cmocustomerpaymenttermsid = 'NET10'
        org.save()
        passed = setup_importer_account._process_account(account_id='M1T2')
        assert passed
        passed = setup_importer_account._process_account(account_id='M1T2')
        assert passed
        accts = Account.filter(erp_code='M1T2')
        assert len(accts) > 0
        account2 = Account.get(accts[0].id)

        pp_contacts_list = Contact.filter(account_id=account.id)
        assert len(pp_contacts_list) == 1
        for c in pp_contacts_list:
            con: Contact = Contact.get(id=c.id)
            assert 'test' in con.first_name
            con.delete()
        account.delete()
        account2.delete()

    def test_get_payment_terms_imports(self, setup_importer_account):
        Paymentterms.objects.create(
            xatpaymenttermid='NET30',
            xatdescription='NET 30 days',
            xatdaysdue=30,
            xatdiscountdays=0,
            xatdiscountpercent=0.00,
            xatgraceperiod=0,
            xatcalculationtype=0,
            xatimmediatepaymentrequired=False,
            xatcalculationdayofmonth=0,
            xatdiscountdayofmonth=0,
        )

        term, period = AccountImportProcessor.get_payment_terms(term_code='NET30')

        assert term == 'Net 30'
        assert period == 30
