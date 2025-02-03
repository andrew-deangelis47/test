# import standard libraries
import os
import sys

import pendulum
import pytest

from paperless.objects.orders import OrderComponent
from paperless.objects.customers import Account, Contact
from paperless.objects.purchased_components import PurchasedComponent
import random

# append to path
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))

from baseintegration.integration import Integration
from baseintegration.utils.test_utils import get_order, get_repeat_parts_from_backend
from e2.models import CustomerCode, Nextnumber, Shipto, Terms, Taxcode, Estim, Contacts, Workcntr, Vendcode, Quotedet, \
    OrderDet, Quote, JobReq, Releases, OrderRouting, Routing, Order
from e2.query.address import get_or_create_shipping_address, assign_location_for_shipping_address, get_shipping_address_by_location, address_tokenize
from e2.query.customer_code import get_or_create_customer_code, filter_fuzzy_customer_code, increment_code
from e2.exporter.processors.part import PartProcessor


@pytest.fixture
def setup_exporter():
    integration = Integration()
    from e2.exporter.exporter import E2OrderExporter
    i = E2OrderExporter(integration)
    # set nextnumber so that test saves will work
    Nextnumber.objects.create(object="ORDER", nextnumber=1)
    return i


@pytest.fixture
def setup_quote_exporter():
    integration = Integration()
    from e2.exporter.exporter import E2QuoteExporter
    e = E2QuoteExporter(integration)
    return e


@pytest.fixture
def setup_account_importer():
    integration = Integration()
    from e2.importer.importer import E2AccountImporter
    i = E2AccountImporter(integration)
    # set nextnumber so that test saves will work
    Nextnumber.objects.create(object="ORDER", nextnumber=1)
    return i


@pytest.fixture
def setup_purchased_component_importer():
    integration = Integration()
    from e2.importer.importer import E2PurchasedComponentImporter
    i = E2PurchasedComponentImporter(integration)
    # set nextnumber so that test saves will work
    Nextnumber.objects.create(object="ORDER", nextnumber=1)
    return i


@pytest.fixture
def setup_material_importer():
    integration = Integration()
    from e2.importer.importer import E2MaterialImporter
    i = E2MaterialImporter(integration)
    # set nextnumber so that test saves will work
    Nextnumber.objects.create(object="ORDER", nextnumber=1)
    return i


@pytest.fixture
def setup_workcenter_importer():
    integration = Integration()
    from e2.importer.importer import E2WorkCenterImporter
    i = E2WorkCenterImporter(integration)
    # set nextnumber so that test saves will work
    Nextnumber.objects.create(object="ORDER", nextnumber=1)
    return i


@pytest.fixture
def setup_vendor_importer():
    integration = Integration()
    from e2.importer.importer import E2VendorImporter
    i = E2VendorImporter(integration)
    # set nextnumber so that test saves will work
    Nextnumber.objects.create(object="ORDER", nextnumber=1)
    return i


@pytest.fixture
def setup_repeat_work_importer():
    integration = Integration()
    integration.config_yaml["Importers"] = {"repeat_part": {"is_post_enabled": True}}
    from e2.importer.repeat_work_importer import E2RepeatWorkImporter
    return E2RepeatWorkImporter(integration)


def create_part(partno, description, altpartno):
    Estim.objects.create(
        partno=partno,
        descrip=description,  # This is the description field
        altpartno=altpartno,
        pricingunit="ea",
        qty1=1,
        price1=0.0,
        qty2=None,
        price2=0.0,
        qty3=None,
        price3=0.0,
        qty4=None,
        price4=0.0,
        qty5=None,
        price5=0.0,
        qty6=None,
        price6=0.0,
        qty7=None,
        price7=0.0,
        qty8=None,
        price8=0.0,
        lastpricechg=None,
        revdate=None,
        drawnum=None,
        partwt=None,
        commpct=0.,
        miscchg=None,
        miscdescrip='',
        drawingfilename=None,
        globalmarkuppct=None,
        ljno=None,
        ljqty=None,
        ljdatefin=None,
        ljprice=None,
        ljquoteno=None,
        ljdate=None,
        qtyip=None,
        lastdelticketno=None,
        lastdelticketdate=None,
        lastdelticketqty=None,
        comments="hi",
        stockunit="ea",
        qtyonhand=None,
        reordlevel=None,
        reordqty=None,
        qtyonres=None,
        lrno=None,
        lrdate=None,
        lrqty=None,
        binloc1=None,
        binqty1=None,
        binloc2=None,
        binqty2=None,
        binloc3=None,
        binqty3=None,
        binloc4=None,
        binqty4=None,
        binloc5=None,
        binqty5=None,
        vendcode1=None,
        vendcode2=None,
        vendcode3=None,
        leadtime=None,
        purchunit="ea",
        purchfactor=1.0,
        markuppct=None,
        pqty1=None,
        pcost1=0.0,
        pqty2=None,
        pcost2=0.0,
        pqty3=None,
        pcost3=0.0,
        pqty4=None,
        pcost4=0.0,
        pqty5=None,
        pcost5=0.0,
        pqty6=None,
        pcost6=0.0,
        pqty7=None,
        pcost7=0.0,
        pqty8=None,
        pcost8=0.0,
        stockingcost=None,
        lpono=None,
        lpodate=None,
        lpoqty=None,
        lpocost=None,
        qtyonorder=None,
        qtyoutside=None,
        markup1=0.0,
        markup2=0.0,
        markup3=0.0,
        markup4=0.0,
        markup5=0.0,
        markup6=0.0,
        markup7=0.0,
        markup8=0.0,
        lockprice='Y',  # this needs to be 'Y'
        calcmethod="Y",
        printed='N',
        purchglcode=None,
        bin1lot=None,
        bin2lot=None,
        bin3lot=None,
        bin4lot=None,
        bin5lot=None,
        active='Y',
        defaultbinloc=None,
        user_date1=None,
        user_date2=None,
        user_text1=None,
        user_text2=None,
        user_text3=None,
        user_text4=None,
        user_currency1=None,
        user_currency2=None,
        user_number1=None,
        user_number2=None,
        user_number3=None,
        user_number4=None,
        user_memo1=None,
        matchqtybreaks='Y',
        allow_decimal_inventory=None,
        allow_decimal_purchasing=None,
        automatically_fill_requirements=None,
        automatically_use_partial_records=None,
        automatically_combine_partial_records=None,
        inspect_orders=None,
        inspect_customer_returns=None,
        inspect_receivers=None,
        inspect_internal_rejections=None,
        using_time_tickets=None,
        stocking_unit_new=None,
        stocking_purchasing_factor_new=None,
        purchasing_unit_new=None,
        purchasing_purchasing_factor_new=None,
        part_weight_new=None,
        saved_by_utility=None,
        new_purchasing_factor=None,
        convert_me=None,
        imagerepositoryid=None,
        accountingid=None,
        lastmoddate=None,
        lastmoduser=None,
        istaxable=True,  # TODO - what to do here?
        qbitemtype='NonInventory'  # TODO - what to do here?
    )


def create_workcenter(workcenter_id, shortname, description):
    Workcntr.objects.create(
        workcntr=workcenter_id,
        descrip=description,
        shortname=shortname,
        burdenrate=0.01,
        laborrate=0.01,
        cycle1=1,
        setup1=1
    )


def create_vendor(vendcode, vendname):
    Vendcode.objects.create(
        vendcode=vendcode,
        vendname=vendname,
        vendtype='Vendtype',
        outserv='Y',
        minorder=100,
        leadtime=24
    )


@pytest.mark.django_db
class TestE2QuoteExporter:
    def test_exporter_has_config(self, setup_quote_exporter):
        assert type(setup_quote_exporter._integration.config) is dict


@pytest.mark.django_db
class TestE2Exporter:
    """Runs tests against a dummy database using models.py"""

    def test_process_single_customer(self, setup_exporter):
        assert CustomerCode.objects.count() == 0

        setup_exporter.erp_config.should_update_e2_billing_address = True
        setup_exporter.erp_config.should_update_e2_payment_terms = True
        setup_exporter.erp_config.should_create_e2_shipping_address = True
        setup_exporter.erp_config.should_update_e2_customer_notes = True
        setup_exporter.erp_config.should_update_e2_customer_sales_id = True

        setup_exporter._process_order(get_order(25))
        assert CustomerCode.objects.count() == 1

    def test_get_create_shipping_address(self, setup_exporter):
        setup_exporter._process_order(get_order(25))
        assert Shipto.objects.count() == 1
        get_or_create_shipping_address(CustomerCode.objects.first(), {})
        assert Shipto.objects.count() == 2

    def test_assign_location_for_shipping_address(self, setup_exporter):
        setup_exporter._process_order(get_order(25))
        assert assign_location_for_shipping_address(CustomerCode.objects.first()) == "LOCATION2"

    def test_get_shipping_address_by_location(self, setup_exporter):
        setup_exporter._process_order(get_order(25))
        assert get_shipping_address_by_location(CustomerCode.objects.first(), "LOCATION2") is None

    def test_get_or_create_customer_code(self, setup_exporter):
        get_or_create_customer_code(name="test")
        assert CustomerCode.objects.count() == 1
        get_or_create_customer_code(name="test", code="TEST")
        assert CustomerCode.objects.count() == 1

    def test_filter_fuzzy_customer_code(self, setup_exporter):
        get_or_create_customer_code(name="test 123")
        assert filter_fuzzy_customer_code(name="test-123") is not None

    def test_outside_service(self, setup_exporter):
        import e2.models as e2
        setup_exporter._process_order(get_order(26))
        assert e2.Routing.objects.filter(workorvend=1).count() == 1

    def test_inside_operations(self, setup_exporter):
        import e2.models as e2
        setup_exporter._process_order(get_order(145))
        assert e2.Routing.objects.filter(workorvend=0).count() == 14

    def test_material_operations(self, setup_exporter):
        import e2.models as e2
        setup_exporter.erp_config.should_use_new_multiple_material_logic = True
        setup_exporter._process_order(get_order(188))
        first_material = e2.Materials.objects.filter(partno="E2-MULTIPLE-MATERIALS", subpartno="4270part").first()
        second_material = e2.Materials.objects.filter(partno="E2-MULTIPLE-MATERIALS", subpartno="6251part").first()
        assert first_material is not None
        assert second_material is not None

    def test_get_part_number(self):
        component_with_part_num: OrderComponent = get_order(29).order_items[0].root_component
        assert PartProcessor.get_part_number(component_with_part_num) == "TESTASSEMBLY"
        component_no_part_num: OrderComponent = get_order(30).order_items[0].root_component
        assert PartProcessor.get_part_number(component_no_part_num) == os.path.splitext(component_no_part_num.part_name)[0]

    def test_increment_code(self):
        assert increment_code('1', 100) == '2'
        assert increment_code('CUST', 10) == 'CUST1'

    def test_runtime_units(self, setup_exporter):
        setup_exporter.erp_config.runtime_units = "M"
        setup_exporter.erp_config.setup_time_units = "M"
        import e2.models as e2
        setup_exporter._process_order(get_order(26))
        assert e2.Routing.objects.filter(timeunit="M").first()
        assert e2.Routing.objects.filter(cycleunit="M").first()

    def test_address_tokenize(self):
        assert address_tokenize("100 Commercial Street") == ["100", "commercial", "st"]
        assert address_tokenize("commercial") == ["commercial"]


@pytest.mark.django_db
class TestE2Importer:

    def test_account_importer(self, setup_account_importer):
        customer_name = str(random.randint(1, 100000000)) + " Company"
        terms_code = str(random.randint(1, 1000000000))
        netduedays = random.randint(1, 10)
        Taxcode.objects.create(taxcode="tax")
        CustomerCode.objects.create(customer_code="BOAT", customer_name=customer_name, taxcode="tax", termscode=terms_code, active="Y")
        Terms.objects.create(termscode=terms_code, netduedays=netduedays)

        setup_account_importer.run(account_id="BOAT")
        accounts = Account.filter(erp_code="BOAT")
        account: Account = Account.get(accounts[0].id)
        assert account.name == customer_name
        assert account.payment_terms == terms_code
        assert account.payment_terms_period == netduedays
        assert account.tax_exempt

    def test_account_importer_new(self, setup_account_importer):
        customer_name = str(random.randint(1, 10000)) + " Company"
        new_account = str(random.randint(10, 1000000))
        terms_code = str(random.randint(1, 10000000))
        netduedays = random.randint(1, 10)
        Taxcode.objects.create(taxcode="tax")
        CustomerCode.objects.create(customer_code=new_account,
                                    customer_name=customer_name,
                                    taxcode="tax",
                                    termscode=terms_code,
                                    active="Y",
                                    b_addr1="100 Commercial St",
                                    b_addr2="Unit 415",
                                    b_city="Portland",
                                    b_zip_code="04101",
                                    b_state="ME",
                                    b_country="United States"
                                    )
        Terms.objects.create(termscode=terms_code, netduedays=netduedays)
        addr = str(random.randint(1, 1000))
        Shipto.objects.create(
            custcode=new_account,
            saddr1=f"{addr} Commercial Street",
            location="HQ",
            saddr2="Unit 415",
            scity="Portland",
            sstate="ME",
            szipcode="04101",
            scountry="United States",
            shipphone="2074155440",
            shipcontact="Boaty B."
        )
        boat_name = str(random.randint(1, 1000))
        Contacts.objects.create(
            object='CUST',
            code=new_account,
            contact=f"Boat {boat_name}",
            phone="2074155440",
            email=f"boaty{boat_name}@boat1.com",
            extension="123",
            comments="test",
            active='Y'
        )
        setup_account_importer.run(account_id=new_account)
        accounts = Account.filter(erp_code=new_account)
        account: Account = Account.get(accounts[0].id)
        assert account.name == customer_name
        assert account.payment_terms == terms_code
        assert account.payment_terms_period == netduedays
        assert account.tax_exempt
        pp_contacts_list = Contact.filter(account_id=account.id)
        assert len(pp_contacts_list) > 0
        found = False
        for c in pp_contacts_list:
            contact: Contact = Contact.get(id=c.id)
            if boat_name in contact.first_name or boat_name in contact.last_name:
                found = True
            contact.delete()
        assert found
        account.delete()

    def test_purchased_component_importer(self, setup_purchased_component_importer):
        partno = str(random.randint(1, 10000000)) + "part"
        altpartno = partno + "alt"
        description = str(random.randint(1, 10000000)) + "testing"
        create_part(partno, altpartno, description)
        setup_purchased_component_importer.run(purchased_component_id=partno)
        purchased_components: list = PurchasedComponent.search(partno)
        assert len(purchased_components) > 0
        # existing part
        setup_purchased_component_importer.run(purchased_component_id="1054part")
        purchased_components: list = PurchasedComponent.search(partno)
        assert len(purchased_components) > 0
        assert setup_purchased_component_importer._bulk_process_purchased_component([partno])

    def test_material_importer(self, setup_material_importer, caplog):
        partno = str(random.randint(1, 10000000)) + "part"
        altpartno = partno + "alt"
        description = str(random.randint(1, 10000000)) + "testing"
        create_part(partno, altpartno, description)
        setup_material_importer.run(material_id=partno)
        assert "Processed E2-material-bulk-upload-count-1 successfully" in caplog.text
        assert setup_material_importer._bulk_process_material([partno])

    def test_workcenter_importer(self, setup_workcenter_importer, caplog):
        workcenter_id = random.randint(1, 10000000)
        shortname = f'{workcenter_id} short'
        description = f'{workcenter_id} testing description'
        create_workcenter(workcenter_id, shortname, description)
        setup_workcenter_importer.run(work_center_id=workcenter_id)
        assert "Processed E2-work-center-bulk-upload-count-1 successfully" in caplog.text
        assert setup_workcenter_importer._bulk_process_work_center([workcenter_id])

    def test_vendor_importer(self, setup_vendor_importer, caplog):
        vendcode = str(random.randint(1, 10000000))
        vendname = f'{vendcode} name'
        create_vendor(vendcode, vendname)
        setup_vendor_importer.run(vendor_id=vendcode)
        assert "Processed E2-vendor-bulk-upload-count-1 successfully" in caplog.text
        assert setup_vendor_importer._bulk_process_vendor([vendcode])


@pytest.mark.django_db
class TestRepeatPartImport:

    def test_repeat_part_listener(self, setup_repeat_work_importer, caplog, mocker):
        OrderRouting(
            part_no="1",
            last_mod_date=pendulum.naive(year=1990, month=1, day=2)
        ).fill_and_save()
        JobReq(
            partno="2",
            lastmoddate=pendulum.naive(year=1990, month=1, day=2)
        ).fill_and_save()
        quote: Quote = Quote(
            quoteno="myquote",
            lastmoddate=pendulum.naive(year=1990, month=1, day=2)
        ).fill_and_save()
        Quotedet(
            partno="3",
            quoteno=quote.quoteno,
        ).fill_and_save()
        Estim.objects.create(
            partno="4",
            lastmoddate=pendulum.naive(year=1990, month=1, day=2)
        )
        Estim.objects.create(
            partno="5",
            lastmoddate=pendulum.naive(year=1970, month=1, day=2)
        )

        mocker.patch('e2.importer.repeat_work_importer.get_last_action_datetime_value', return_value=pendulum.naive(year=1980, month=1, day=2))

        new_parts = set()
        setup_repeat_work_importer.listener._get_new_default(new_parts, bulk=True)
        assert new_parts == {"1", "2", "3", "4"}

        new_parts = set()
        setup_repeat_work_importer.listener._get_new_shop_system(new_parts)
        assert new_parts == {"1", "2", "3", "4", "5"}

    def test_import_template(self, setup_repeat_work_importer, caplog):
        part_number = "pp_e2_test_part_123"

        estim: Estim = Estim.objects.create(
            partno=part_number,
            qty1=4,
            price1=10,
            custcode="mycust",
            descrip="Estim #1",
            prodcode="Prod Code #1"
        )
        routing: Routing = Routing(
            partno=estim.partno,
            descrip="Routing #1",
            workcntr="Work center #1"
        ).fill_and_save()
        Workcntr(
            oldworkcntr=routing.workcntr
        ).fill_and_save()
        Contacts.objects.create(
            code=estim.custcode
        )
        CustomerCode.objects.create(
            customer_code=estim.custcode
        )

        setup_repeat_work_importer.run(part_number)

        parts = get_repeat_parts_from_backend(part_number)
        assert len(parts) == 1

        part = parts[0]
        headers = [h for h in part["headers"] if h["type"] == "template"]
        assert len(headers) == 1

        moms = headers[0]["methods_of_manufacture"]
        assert len(moms) == 1

    def test_import_quote(self, setup_repeat_work_importer, caplog):
        part_number = "pp_e2_test_part_124"

        estim = Estim.objects.create(
            partno=part_number
        )
        quote: Quote = Quote(
            quoteno="myquote",
            custcode="mycust"
        ).fill_and_save()
        quote_detail: Quotedet = Quotedet(
            partno=estim.partno,
            jobno="myjob",
            quoteno=quote.quoteno,
            itemno=1,
            descrip="Descrip #1",
            workcode="Work code #1",
            jobnotes="Job notes"
        ).fill_and_save()
        OrderDet(
            job_no=quote_detail.jobno,
            part_no=quote_detail.partno,
            quote_no=quote_detail.quoteno,
            quote_item_no=quote_detail.itemno
        ).fill_and_save()
        order_routing: OrderRouting = OrderRouting(
            part_no=quote_detail.partno,
            job_no=quote_detail.jobno,
            descrip="Order routing #1",
            work_cntr="Work center #1",
            status="Ordered"
        ).fill_and_save()
        Workcntr(
            oldworkcntr=order_routing.work_cntr
        ).fill_and_save()
        Contacts.objects.create(
            code=quote.custcode
        )
        CustomerCode.objects.create(
            customer_code=quote.custcode
        )

        setup_repeat_work_importer.run(part_number)

        parts = get_repeat_parts_from_backend(part_number)
        assert len(parts) == 1

        part = parts[0]
        headers = [h for h in part["headers"] if h["type"] == "estimated"]
        assert len(headers) == 1

        moms = headers[0]["methods_of_manufacture"]
        assert len(moms) == 1

    def test_import_engineered_job(self, setup_repeat_work_importer, caplog):
        part_number = "pp_e2_test_part_125"
        part_number_2 = "pp_e2_test_part_126"
        child_part_number = "pp_e2_test_child_part_125"
        material_part_number = "pp_e2_test_material_125"

        self.setup_jobs(part_number, part_number_2, child_part_number, material_part_number)

        # import root part
        setup_repeat_work_importer.run(part_number)

        parts = get_repeat_parts_from_backend(part_number)
        assert len(parts) == 1

        part = parts[0]
        headers = [h for h in part["headers"] if h["type"] == "engineered"]
        assert len(headers) == 1
        header = headers[0]

        moms = header["methods_of_manufacture"]
        assert len(moms) == 1

        # import child part
        setup_repeat_work_importer.run(child_part_number)

        parts = get_repeat_parts_from_backend(child_part_number)
        assert len(parts) == 1

        part = parts[0]
        headers = [h for h in part["headers"] if h["type"] == "engineered"]
        assert len(headers) == 2

        for header in headers:
            moms = header["methods_of_manufacture"]
            assert len(moms) == 1

    def test_import_executed_job(self, setup_repeat_work_importer, caplog):
        part_number = "pp_e2_test_part_127"
        part_number_2 = "pp_e2_test_part_128"
        child_part_number = "pp_e2_test_child_part_127"
        material_part_number = "pp_e2_test_material_127"

        order_det_1, order_det_2 = self.setup_jobs(part_number, part_number_2, child_part_number, material_part_number)

        Releases(
            jobno=order_det_1.job_no,
            partno=order_det_1.part_no,
            orderno=order_det_1.orderno,
        ).fill_and_save()
        Releases(
            jobno=order_det_2.job_no,
            partno=order_det_2.part_no,
            orderno=order_det_2.orderno,
        ).fill_and_save()

        setup_repeat_work_importer.run(part_number)

        parts = get_repeat_parts_from_backend(part_number)
        assert len(parts) == 1

        part = parts[0]
        headers = [h for h in part["headers"] if h["type"] == "executed"]
        assert len(headers) == 1

        moms = headers[0]["methods_of_manufacture"]
        assert len(moms) == 1

        # import child part
        setup_repeat_work_importer.run(child_part_number)

        parts = get_repeat_parts_from_backend(child_part_number)
        assert len(parts) == 1

        part = parts[0]
        headers = [h for h in part["headers"] if h["type"] == "executed"]
        assert len(headers) == 2

        for header in headers:
            moms = header["methods_of_manufacture"]
            assert len(moms) == 1

    @staticmethod
    def setup_jobs(part_number, part_number_2, child_part_number, material_part_number):
        # set up an assembly
        order: Order = Order.objects.create(
            order_no="myorder",
            customer_code="mycust"
        )
        top_level_order_det: OrderDet = OrderDet(
            job_no="top-job",
            part_no=part_number,
            orderno=order.order_no,
        ).fill_and_save()
        child_order_det: OrderDet = OrderDet(
            job_no="child-job",
            master_job_no=top_level_order_det.job_no,
            part_no=child_part_number,
            orderno=order.order_no,
        ).fill_and_save()
        JobReq(
            partno=material_part_number,
            jobno=child_order_det.job_no,
            orderno=order.order_no,
            partdesc="Descrip #1",
            workcode="Work code #1",
            prodcode="Prod code #1"
        ).fill_and_save()
        OrderRouting(
            order_no=top_level_order_det.orderno,
            part_no=top_level_order_det.part_no,
            job_no=top_level_order_det.job_no,
            descrip="Order routing #1",
            work_cntr="Work center #1",
            status="Ordered"
        ).fill_and_save()

        # set up a different assembly with different root but same children
        top_level_order_det_2: OrderDet = OrderDet(
            job_no="top-job-2",
            part_no=part_number_2,
            orderno=order.order_no,
        ).fill_and_save()
        OrderDet(
            job_no="child-job-2",
            master_job_no=top_level_order_det_2.job_no,
            part_no=material_part_number,
            orderno=order.order_no,
        ).fill_and_save()
        JobReq(
            partno=child_part_number,
            jobno=top_level_order_det_2.job_no,
            orderno=order.order_no,
            partdesc="Descrip #2",
            workcode="Work code #2",
            prodcode="Prod code #2"
        ).fill_and_save()

        Estim.objects.create(
            partno=part_number
        )
        Estim.objects.create(
            partno=part_number_2
        )
        Estim.objects.create(
            partno=child_part_number
        )
        Estim.objects.create(
            partno=material_part_number
        )
        Contacts.objects.create(
            code=order.customer_code
        )
        CustomerCode.objects.create(
            customer_code=order.customer_code
        )

        return top_level_order_det, top_level_order_det_2
