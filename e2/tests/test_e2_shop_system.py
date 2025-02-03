# please note -- to run these tests, you must set an environment variable ERP_VERSION to 'e2_shop_system'

# import standard libraries
import os
import sys
import pytest
from paperless.objects.orders import OrderComponent
from paperless.objects.customers import Account
from paperless.objects.purchased_components import PurchasedComponent
import random

# append to path
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))

from baseintegration.integration import Integration
from baseintegration.utils.test_utils import get_order
from e2.models import CustomerCode, Nextnumber, Shipto, Terms, Taxcode, Estim
from e2.query.address import assign_location_for_shipping_address, address_tokenize
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
        assert Shipto.objects.count() == 0
        setup_exporter._process_order(get_order(25))
        assert Shipto.objects.count() == 1

    def test_assign_location_for_shipping_address(self, setup_exporter):
        setup_exporter._process_order(get_order(25))
        assert assign_location_for_shipping_address(CustomerCode.objects.first()) == "LOCATION2"

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
        customer_name = str(random.randint(1, 10000000)) + " Company"
        terms_code = str(random.randint(1, 100000000))
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

    def test_purchased_component_importer(self, setup_purchased_component_importer):
        partno = str(random.randint(1, 10000000)) + "part"
        altpartno = partno + "alt"
        description = str(random.randint(1, 10000000)) + "testing"
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
            vendcode1='test',
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
            convert_me=None
        )
        setup_purchased_component_importer.run(purchased_component_id=partno)
        purchased_components: list = PurchasedComponent.search(partno)
        assert len(purchased_components) > 0
        assert setup_purchased_component_importer._bulk_process_purchased_component([partno])

    def test_material_importer(self, setup_material_importer, caplog):
        partno = str(random.randint(1, 100000000)) + "part"
        altpartno = partno + "alt"
        description = str(random.randint(1, 100000000)) + "testing"
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
            convert_me=None
        )
        setup_material_importer.run(material_id=partno)
        assert "Processed E2-material-bulk-upload-count-1 successfully" in caplog.text
        assert setup_material_importer._bulk_process_material([partno])
