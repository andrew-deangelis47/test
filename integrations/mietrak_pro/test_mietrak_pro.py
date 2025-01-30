# import standard libraries
from typing import Optional

import pytest
import os

# append to path
import sys

# append to path
from mietrak_pro.query.address import match_shipping_address, create_shipping_address, match_billing_address, \
    create_billing_address

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))

from paperless.objects.orders import Order, OrderOperation, OrderCostingVariable
from paperless.objects.quotes import Quote, QuoteCostingVariable, CostingVariablePayload
from baseintegration.integration import Integration
from mietrak_pro.models import Party, Division, Address, Addresstype, Country, State, Salesorderstatus, Itemtype, \
    Calculationtype, Unitofmeasure, Unitofmeasureset, Pricetype, Routerstatus, Salesorderlineitemtype, \
    Salesorderlinelotstatus, Item, Routerworkcenter, Router, Salestaxtype, Iteminventorylocation, Location, User, \
    Requestforquote, Requestforquoteline, Salesorderline, Salesorder, Operation, Workcenter, Quote as MTPQuote, \
    Quoteassembly, Quotequantity, Workorder, Workorderrelease, Workordercompletion, Activitylogtype, Purchaseorderline, \
    Itemvendor, Requestforquotesupplier, Customergroup, Purchaseorderlinestatus, Purchaseorder, Purchaseorderstatus, \
    Confirmingstatement
from mietrak_pro.query.part import get_item_type, create_item
from mietrak_pro.exporter.processors.routing_line import RoutingLineProcessor
from mietrak_pro.query.customer import create_customer
from mietrak_pro.query.contact import create_contact
from baseintegration.utils.test_utils import get_order, get_quote, get_repeat_parts_from_backend
import random
from paperless.objects.customers import Account, Contact
from paperless.objects.purchased_components import PurchasedComponent
from mietrak_pro.exporter.processors.account import AccountProcessor
from mietrak_pro.exporter.processors.salesperson import PartySalespersonProcessor, OrderSalespersonProcessor
from mietrak_pro.importer.importer import MietrakProPurchasedComponentListener, MietrakProMaterialImportListener, \
    MietrakProOutsideServiceImportListener, MietrakProWorkCenterImportListener
from mietrak_pro.importer.configuration import MaterialImportConfig, OutsideServiceImportConfig, \
    WorkCenterImportConfig, PurchasedComponentImportConfig
from unittest import mock
from typing import Union


def seed_models():
    # Seed the database with the built-in MIE Trak Pro records
    Division.objects.create()
    Location.objects.create()
    Addresstype.objects.create(code='001', description='Billing')
    Addresstype.objects.create(code='002', description='Shipping')
    Addresstype.objects.create(code='003', description='Billing & Shipping')
    country = Country.objects.create(
        code='US',
        description='United States of America',
        alpha2code='US',
        alpha3code='USA',
        uncode='840',
    )
    State.objects.create(
        countryfk=country,
        code='MA',
        description='Massachusetts',
    )

    Salesorderstatus.objects.create(code='001', description='All')
    Salesorderstatus.objects.create(code='002', description='Open')
    Salesorderstatus.objects.create(code='003', description='Hold')
    Salesorderstatus.objects.create(code='004', description='Production Hold')
    Salesorderstatus.objects.create(code='005', description='Closed')
    Salesorderstatus.objects.create(code='006', description='Inactive')

    item_type_standard = Itemtype.objects.create(code='001', description='Standard')
    item_type_material = Itemtype.objects.create(code='002', description='Material')
    item_type_hardware = Itemtype.objects.create(code='003', description='Hardware/Supplies')
    Itemtype.objects.create(code='004', description='Miscellaneous')
    Itemtype.objects.create(code='005', description='Outside Process')
    Itemtype.objects.create(code='006', description='Kit')
    item_type_tooling = Itemtype.objects.create(code='007', description='Tooling')

    Item.objects.create(itemtypefk=item_type_tooling, partnumber='Tooling Charge')

    Calculationtype.objects.create(code='101', description='Piece Price', itemtypefk=item_type_standard)
    Calculationtype.objects.create(code='201', description='Single Part Price', itemtypefk=item_type_material)
    Calculationtype.objects.create(code='301', description='Piece Price', itemtypefk=item_type_hardware)

    unit_of_measure = Unitofmeasure.objects.create(code='EACH', name='EACH')
    Unitofmeasureset.objects.create(
        baseunitofmeasurefk=unit_of_measure,
        inventoryunitofmeasurefk=unit_of_measure,
        purchaseunitofmeasurefk=unit_of_measure,
        shippingunitofmeasurefk=unit_of_measure,
        quotingunitofmeasurefk=unit_of_measure,
        code='EACH',
        name='EACH',
        baseunitofmeasurevalue=1.,
        purchaseunitofmeasureoverride=0,
        purchaseunitofmeasurevalue=1.,
        shippingunitofmeasurevalue=1.,
        quotingunitofmeasureoverride=0,
        quotingunitofmeasurevalue=1.,
    )
    Pricetype.objects.create(code='001', description='Base Price')
    Salestaxtype.objects.create(code='001', description='Tax Invoice Amount')

    Routerstatus.objects.create(code='001', description='Pending Approval')
    Routerstatus.objects.create(code='002', description='Approved')
    Routerstatus.objects.create(code='003', description='Inactive')

    Salesorderlineitemtype.objects.create(code='001', description='Standard Item')

    Salesorderlinelotstatus.objects.create(code='003', description='Firm')

    User.objects.create(firstname='Test', lastname='Testerson', code=1)

    Party.objects.create(name='test')

    wc = Workcenter.objects.create(description='CNC')

    Operation.objects.create(name='CNC', description='CNC',
                             workcenterfk=wc, setupoperationoverheadrate=1, runoperationoverheadrate=1)

    Activitylogtype.objects.create(activitylogtypepk=7)
    Activitylogtype.objects.create(activitylogtypepk=11)
    Activitylogtype.objects.create(activitylogtypepk=46)
    Activitylogtype.objects.create(activitylogtypepk=74)

    Itemvendor.objects.create()
    Requestforquotesupplier.objects.create()
    Customergroup.objects.create()
    Purchaseorderlinestatus.objects.create()
    Purchaseorder.objects.create()
    Purchaseorderstatus.objects.create()
    Confirmingstatement.objects.create()
    Purchaseorderline.objects.create()


@pytest.fixture
def setup_integration():
    """Create integration and register the customer processor to process orders"""
    integration = Integration()
    from mietrak_pro.exporter.exporter import MieTrakProOrderExporter, MieTrakProQuoteExporter
    order_exporter = MieTrakProOrderExporter(integration)
    quote_exporter = MieTrakProQuoteExporter(integration)
    seed_models()
    return order_exporter, quote_exporter


@pytest.fixture
def setup_account_importer():
    integration = Integration()
    from mietrak_pro.importer.importer import MietrakProAccountImporter
    i = MietrakProAccountImporter(integration)
    seed_models()
    yield i
    # delete acct if needed
    try:
        acct = Account.filter(erp_code="1")[0]
        a = Account.get(acct.id)
        a.delete()
    except Exception:
        pass


@pytest.fixture
def setup_purchased_component_importer():
    integration = Integration()
    from mietrak_pro.importer.importer import MietrakProPurchasedComponentImporter
    i = MietrakProPurchasedComponentImporter(integration)
    seed_models()
    return i


@pytest.fixture
def setup_material_importer():
    integration = Integration()
    from mietrak_pro.importer.importer import MietrakProMaterialImporter
    i = MietrakProMaterialImporter(integration)
    seed_models()
    return i


@pytest.fixture
def setup_outside_process_importer():
    integration = Integration()
    from mietrak_pro.importer.importer import MietrakProOutsideServiceImporter
    i = MietrakProOutsideServiceImporter(integration)
    seed_models()
    return i


@pytest.fixture
def setup_vendor_importer():
    integration = Integration()
    from mietrak_pro.importer.importer import MietrakProVendorImporter
    i = MietrakProVendorImporter(integration)
    seed_models()
    return i


@pytest.fixture
def setup_workcenter_importer():
    integration = Integration()
    from mietrak_pro.importer.importer import MietrakProWorkCenterImporter
    i = MietrakProWorkCenterImporter(integration)
    seed_models()
    return i


@pytest.fixture
def setup_repeat_work_importer():
    integration = Integration()
    integration.config_yaml["Importers"] = {"repeat_part": {"is_post_enabled": True}}
    from mietrak_pro.importer.repeat_work_importer import MieTrakProRepeatPartImporter
    return MieTrakProRepeatPartImporter(integration)


def get_or_create_shipping_address(customer: Party, addr_dict: dict) -> Address:
    shipping_address = match_shipping_address(customer, addr_dict)
    if shipping_address is None:
        shipping_address = create_shipping_address(customer, addr_dict, 1)
    return shipping_address


def get_or_create_billing_address(customer: Party, addr_dict: dict) -> Address:
    billing_address = match_billing_address(customer, addr_dict)
    if billing_address is None:
        billing_address = create_billing_address(customer, addr_dict, 1)
    return billing_address


@pytest.mark.django_db
class TestMieTrakProOrderExporter:
    """Runs tests against a dummy database using models.py"""

    def test_process_single_customer(self, setup_integration):
        def override_process_account_info(quote_or_order: Union[Quote, Order]):
            account_id = quote_or_order.contact.account.id
            contact_id = quote_or_order.contact.id
            account = Account.get(account_id)
            account.purchase_orders_enabled = False

            business_name = account.name
            erp_code = account.erp_code
            customer_notes = account.notes
            return account, business_name, erp_code, customer_notes, contact_id

        order_exporter, quote_exporter = setup_integration
        c = Party.objects.count()
        assert c == 1
        order: Order = get_order(31)
        with mock.patch.object(AccountProcessor, 'process_account_info', new=override_process_account_info):
            order_exporter._process_order(order)
        c = Party.objects.count()
        assert c == 3

    def test_process_single_customer_disable_write_to_paperless_parts(self, setup_integration):
        order_exporter, quote_exporter = setup_integration
        order_exporter._integration.paperless_config.should_write_to_paperless_parts = False
        c = Party.objects.count()
        assert c == 1
        with mock.patch('baseintegration.utils.create_new_paperless_parts_account') as mock_func:
            order_exporter._process_order(get_order(31))
        mock_func.assert_not_called()
        c = Party.objects.count()
        assert c == 3

    def test_outside_service(self, setup_integration):
        order_exporter, quote_exporter = setup_integration

        def override_map_pp_op_to_mietrak_pro_outside_service_item(cls, *args, **kwargs):
            return 'OUTSIDE_PROCESS_ITEM', None

        with mock.patch.object(RoutingLineProcessor, 'map_pp_op_to_mietrak_pro_outside_service_item',
                               new=override_map_pp_op_to_mietrak_pro_outside_service_item):
            order_exporter._process_order(get_order(31))
        outside_service_item = Item.objects.filter(partnumber='OUTSIDE_PROCESS_ITEM').first()
        assert outside_service_item is not None
        outside_service_item_vendor = outside_service_item.partyfk
        assert outside_service_item_vendor.name == 'test'

    def test_order_add_on(self, setup_integration):
        order_exporter, quote_exporter = setup_integration
        c = Party.objects.count()
        assert c == 1
        order: Order = get_order(35)

        # Make sure the ordered add-on has the correct costing variable pointing to the correct add-on Item
        order_item = order.order_items[0]
        tooling_charge_item = Item.objects.get(partnumber='Tooling Charge')
        mapping_costing_var = OrderCostingVariable(label="MIE Trak Pro Item ID", variable_class="basic",
                                                   value_type="string", value=tooling_charge_item.itempk,
                                                   row=None, options=None)
        order_item.ordered_add_ons[0].costing_variables.append(mapping_costing_var)

        order_exporter._process_order(order)

        add_on_bom_item = Routerworkcenter.objects.filter(itemfk=tooling_charge_item).first()
        assert add_on_bom_item is not None

        add_on_sales_order_line = Salesorderline.objects.filter(itemfk=tooling_charge_item).first()
        assert add_on_sales_order_line is not None

    def test_sales_order_line_items(self, setup_integration):
        """ Test that the sales order reference line number is assigned correctly """
        order_exporter, quote_exporter = setup_integration
        order: Order = get_order(35)
        # Make sure the ordered add-on has the correct costing variable pointing to the correct add-on Item
        order_item = order.order_items[0]
        tooling_charge_item = Item.objects.get(partnumber='Tooling Charge')
        mapping_costing_var = OrderCostingVariable(label="MIE Trak Pro Item ID", variable_class="basic",
                                                   value_type="string", value=tooling_charge_item.itempk,
                                                   row=None, options=None)
        order_item.ordered_add_ons[0].costing_variables.append(mapping_costing_var)
        order_exporter._process_order(order)

        sales_order = Salesorder.objects.first()
        sales_order_lines = Salesorderline.objects.filter(salesorderfk=sales_order)
        assert len(sales_order_lines) == 3  # Two actual line items, and one add-on for the first line item
        sales_order_line_reference_numbers = set([sol.linereferencenumber for sol in sales_order_lines])
        assert sales_order_line_reference_numbers == {1, 2, 3}

    def test_process_assembly(self, setup_integration):
        order_exporter, quote_exporter = setup_integration
        c = Party.objects.count()
        assert c == 1
        order: Order = get_order(35)
        order_exporter._process_order(order)
        c = Party.objects.count()
        assert c == 3

        customer = Party.objects.filter(customer=1).first()
        shipping_address = Address.objects.filter(partyfk=customer, addresstypefk__description='Shipping').first()
        assert shipping_address.name == 'HQ'

        # Test that the root component router is created properly
        root_component_part_number = 'TESTASSEMBLY'
        root_component_router = Router.objects.filter(partnumber=root_component_part_number).first()
        assert root_component_router is not None
        assert root_component_router.partnumber == root_component_part_number

        # Test that purchased components are created properly
        purchased_component_part_number = '74-451-R-1   EDGE SEALER'
        purchased_component_item = Item.objects.filter(partnumber=purchased_component_part_number).first()
        assert purchased_component_item.inventoriable == 1
        assert purchased_component_item is not None
        bom_item_link = \
            Routerworkcenter.objects.filter(routerfk=root_component_router, itemfk=purchased_component_item).first()
        assert bom_item_link is not None
        assert bom_item_link.quantityrequired == 8
        item_inventory_location = Iteminventorylocation.objects.filter(itemfk=purchased_component_item).first()
        assert item_inventory_location is not None
        purchased_component_item_vendor = purchased_component_item.partyfk
        assert purchased_component_item_vendor.name == 'test'

        addr_dict1 = {'country': 'USA', 'state': 'NH', 'address1': '1200 Elm St.', 'address2': 'Unit 529',  # noqa: E128
                      'city': 'Manchester', 'postal_code': '03101', 'phone': '6035588221', 'phone_ext': '523',
                      # noqa: E128
                      'attention': 'Bob'}  # noqa: E128
        addr_dict2 = {'country': 'USA', 'state': 'NH', 'address1': '1200 Elm St.', 'address2': 'Unit 528',  # noqa: E128
                      'city': 'Manchester', 'postal_code': '03101', 'phone': '6035588221', 'phone_ext': '523',
                      # noqa: E128
                      'attention': 'Bob'}  # noqa: E128
        addr_dict3 = {'country': 'USA', 'state': 'NH', 'address1': '1200 Elm Dr.', 'address2': 'Unit 529',  # noqa: E128
                      'city': 'Manchester', 'postal_code': '03101', 'phone': '6035588221', 'phone_ext': '523',
                      # noqa: E128
                      'attention': 'Bob'}  # noqa: E128
        addr_dict4 = {'country': 'USA', 'state': 'NH', 'address1': '1200 Elm St.', 'address2': 'Unit 529',  # noqa: E128
                      'city': 'Manchester', 'postal_code': '03102', 'phone': '6035588221', 'phone_ext': '523',
                      # noqa: E128
                      'attention': 'Bob'}  # noqa: E128
        addr_dict5 = {'country': 'USA', 'state': 'NH', 'address1': '1200 Elm St.', 'address2': 'Unit 529',  # noqa: E128
                      'city': 'Auburn', 'postal_code': '03101', 'phone': '6035588221', 'phone_ext': '523',  # noqa: E128
                      'attention': 'Bob'}  # noqa: E128
        addr_dict6 = {'country': 'CA', 'state': 'NH', 'address1': '1200 Elm St.', 'address2': 'Unit 529',  # noqa: E128
                      'city': 'Auburn', 'postal_code': '03101', 'phone': '6035588221', 'phone_ext': '523',  # noqa: E128
                      'attention': 'Bob'}  # noqa: E128
        addr_dict7 = {'country': 'USA', 'state': 'NY', 'address1': '1200 Elm St.', 'address2': 'Unit 529',  # noqa: E128
                      'city': 'Auburn', 'postal_code': '03101', 'phone': '6035588221', 'phone_ext': '523',  # noqa: E128
                      'attention': 'Bob'}  # noqa: E128
        p = Party.objects.first()

        shipping_address1 = get_or_create_shipping_address(customer=p, addr_dict=addr_dict1)
        shipping_address2 = get_or_create_shipping_address(customer=p, addr_dict=addr_dict1)
        assert shipping_address1 == shipping_address2

        billing_address1 = get_or_create_billing_address(customer=p, addr_dict=addr_dict1)
        billing_address2 = get_or_create_billing_address(customer=p, addr_dict=addr_dict1)
        assert billing_address1 == billing_address2
        billing_address3 = get_or_create_billing_address(customer=p, addr_dict=addr_dict2)
        assert billing_address1 != billing_address3
        billing_address4 = get_or_create_billing_address(customer=p, addr_dict=addr_dict3)
        assert billing_address1 != billing_address4
        billing_address5 = get_or_create_billing_address(customer=p, addr_dict=addr_dict4)
        assert billing_address1 != billing_address5
        billing_address6 = get_or_create_billing_address(customer=p, addr_dict=addr_dict5)
        assert billing_address1 != billing_address6
        billing_address7 = get_or_create_billing_address(customer=p, addr_dict=addr_dict6)
        assert billing_address1 != billing_address7
        billing_address8 = get_or_create_billing_address(customer=p, addr_dict=addr_dict7)
        assert billing_address1 != billing_address8

    def test_assembly_conversion(self, setup_integration):
        order_exporter, quote_exporter = setup_integration
        order_exporter.erp_config.should_perform_assembly_conversion = True
        order: Order = get_order(49)

        # Make sure the ordered add-on has the correct costing variable pointing to the correct add-on Item
        order_item = order.order_items[0]
        tooling_charge_item = Item.objects.get(partnumber='Tooling Charge')
        mapping_costing_var = OrderCostingVariable(label="MIE Trak Pro Item ID", variable_class="basic",
                                                   value_type="string", value=tooling_charge_item.itempk,
                                                   row=None, options=None)
        order_item.ordered_add_ons[0].costing_variables.append(mapping_costing_var)

        order_exporter._process_order(order)

        # We are specifically testing the "manufactured component with hardware" case - we need to make sure only one
        # Router was created in MIE Trak Pro for the first order item
        assert Router.objects.count() == 2
        router = Router.objects.get(itemfk__partnumber='TESTPART20211105')

        # Ensure that the ops on the assembled component are added after the ops on the manufactured component
        routing_lines = Routerworkcenter.objects.filter(routerfk=router, workcenterfk__isnull=False)
        assert routing_lines.count() == 8
        forming_op = routing_lines.get(sequencenumber=5)
        assert 'This is the fifth step.' in forming_op.comment
        shipping_op = routing_lines.get(sequencenumber=8)
        assert 'This is the eighth step.' in shipping_op.comment

        # Make sure the purchase components and raw materials were added to the Router as BOM items
        bom_items = Routerworkcenter.objects.filter(routerfk=router, itemfk__isnull=False)
        assert bom_items.count() == 4
        bom_item_part_numbers = [bom_item.itemfk.partnumber for bom_item in bom_items]
        assert set(bom_item_part_numbers) == {'TEST_SHEET_STOCK', 'F-440-1', 'F-632-1', 'Tooling Charge'}

        # Check that add-ons are handled correctly by the assembly conversion logic
        add_on_bom_item = Routerworkcenter.objects.filter(itemfk=tooling_charge_item).first()
        assert add_on_bom_item is not None
        sales_order = Salesorder.objects.first()
        sales_order_lines = Salesorderline.objects.filter(salesorderfk=sales_order)
        assert len(sales_order_lines) == 3  # One actual line item, and one add-on for the first line item
        sales_order_line_reference_numbers = set([sol.linereferencenumber for sol in sales_order_lines])
        assert sales_order_line_reference_numbers == {1, 2, 3}

    def test_static_methods_routing_line_processor(self, setup_integration):
        order_exporter, quote_exporter = setup_integration
        processor = RoutingLineProcessor(order_exporter)

        r_uom = RoutingLineProcessor.get_outside_service_item_unit_of_measure_set()

        assert isinstance(r_uom, Unitofmeasureset)

        r_mposim = RoutingLineProcessor.get_paperless_parts_operation_to_mietrak_pro_outside_service_item_mapping()

        assert isinstance(r_mposim, dict)

        r_sit = RoutingLineProcessor.get_outside_service_item_type()

        assert r_sit is not None

        material = get_item_type(component_type='material', is_raw_material=True, is_outside_process=False)
        r_ict1 = RoutingLineProcessor.get_outside_service_item_calc_type(material)

        assert r_ict1.description == 'Single Part Price'

        manufactured = get_item_type(component_type='manufactured', is_raw_material=False, is_outside_process=False)
        r_ict2 = RoutingLineProcessor.get_outside_service_item_calc_type(manufactured)

        assert r_ict2.description == 'Piece Price'

        purchased = get_item_type(component_type='purchased', is_raw_material=False, is_outside_process=False)
        r_ict3 = RoutingLineProcessor.get_outside_service_item_calc_type(purchased)

        assert r_ict3.description == 'Piece Price'

        purchased_bad = get_item_type(component_type='purchased', is_raw_material=False, is_outside_process=False)
        purchased_bad.description = 'Bad Description'
        r_ict4 = RoutingLineProcessor.get_outside_service_item_calc_type(purchased_bad)
        assert r_ict4 is None

        r_sigla = RoutingLineProcessor.get_outside_service_item_general_ledger_account()
        assert r_sigla is None

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
                                   notes='test note',
                                   quantities=[],
                                   position=1,
                                   runtime=None,
                                   setup_time=None,
                                   operation_definition_erp_code='test_erp_code')
        r = RoutingLineProcessor.get_outside_service_item_description(operation)
        assert r == 'test note'

        r_gwcfos = processor.get_work_center_for_outside_service(operation)
        assert r_gwcfos is None

    def test_salesperson(self, setup_integration, caplog):
        order_exporter, quote_exporter = setup_integration
        order_exporter._process_order(get_order(42))
        assert "account_salesperson_id is None" in caplog.text


@pytest.mark.django_db
class TestMieTrakProQuoteExporter:
    """Runs tests against a dummy database using models.py"""
    quotes = {}

    def _get_quote(self, quote_num: int, quote_revision_num: Optional[int] = None):
        # cache orders to avoid hitting rate limit
        if (quote_num, quote_revision_num) not in self.quotes:
            self.quotes[(quote_num, quote_revision_num)] = Quote.get(quote_num, quote_revision_num)
        return self.quotes[(quote_num, quote_revision_num)]

    def test_process_single_customer(self, setup_integration):
        order_exporter, quote_exporter = setup_integration
        c = Party.objects.count()
        assert c == 1
        quote_exporter._process_quote(get_quote(13, 3))
        c = Party.objects.count()
        assert c == 3
        contact = Party.objects.filter(buyer=True).first()
        assert contact.phone is not None

    def test_add_on(self, setup_integration):
        order_exporter, quote_exporter = setup_integration
        c = Party.objects.count()
        assert c == 1
        quote: Quote = get_quote(9, 21)

        # Make sure the quote add-on has the correct costing variable pointing to the correct add-on Item
        quote_item = quote.quote_items[0]
        tooling_charge_item = Item.objects.get(partnumber='Tooling Charge')
        mapping_costing_var = QuoteCostingVariable(label="MIE Trak Pro Item ID", quantity_specific=False,
                                                   variable_class="basic", value_type="string",
                                                   quantities={
                                                       1: CostingVariablePayload(value=1, row=None, options=None)
                                                   },
                                                   value=1)
        quote_item.root_component.add_ons[0].costing_variables.append(mapping_costing_var)

        quote_exporter._process_quote(quote)

        add_on_bom_item = Routerworkcenter.objects.filter(itemfk=tooling_charge_item.itempk).first()
        assert add_on_bom_item is not None

    def test_process_assembly(self, setup_integration):
        order_exporter, quote_exporter = setup_integration
        c = Party.objects.count()
        assert c == 1
        quote: Quote = get_quote(14)
        quote_exporter._process_quote(quote)
        c = Party.objects.count()
        assert c == 3

        # Test that the root component router is created properly
        root_component_part_number = 'TESTASSEMBLY'
        root_component_router = Router.objects.filter(partnumber=root_component_part_number).first()
        assert root_component_router is not None
        assert root_component_router.partnumber == root_component_part_number

        # Test that purchased components are created properly
        purchased_component_part_number = '74-451-R-1   EDGE SEALER'
        purchased_component_item = Item.objects.filter(partnumber=purchased_component_part_number).first()
        assert purchased_component_item.inventoriable == 1
        assert purchased_component_item is not None
        bom_item_link = \
            Routerworkcenter.objects.filter(routerfk=root_component_router, itemfk=purchased_component_item).first()
        assert bom_item_link is not None
        assert bom_item_link.quantityrequired == 8

    def test_request_for_quote(self, setup_integration, caplog):
        order_exporter, quote_exporter = setup_integration
        quote: Quote = get_quote(14)
        quote_exporter._process_quote(quote)
        assert "Processing 14" in caplog.text

        rfq = Requestforquote.objects.first()
        assert rfq is not None
        assert rfq.totalamount > 0
        assert rfq.totalamount == rfq.totalextendedamount

        rfq_line = Requestforquoteline.objects.first()
        assert rfq_line is not None
        assert rfq_line.quantity == 1

    def test_assembly_conversion(self, setup_integration):
        order_exporter, quote_exporter = setup_integration
        quote_exporter.erp_config.should_perform_assembly_conversion = True
        quote: Quote = get_quote(18, 4)

        # Make sure the ordered add-on has the correct costing variable pointing to the correct add-on Item
        quote_item = quote.quote_items[0]
        tooling_charge_item = Item.objects.get(partnumber='Tooling Charge')
        mapping_costing_var = QuoteCostingVariable(label="MIE Trak Pro Item ID", quantity_specific=False,
                                                   variable_class="basic", value_type="string",
                                                   quantities={
                                                       1: CostingVariablePayload(value=1, row=None, options=None)
                                                   },
                                                   value=1)
        quote_item.root_component.add_ons[0].costing_variables.append(mapping_costing_var)

        quote_exporter._process_quote(quote)

        # We are specifically testing the "manufactured component with hardware" case - we need to make sure only one
        # Router was created in MIE Trak Pro for the first order item
        assert Router.objects.count() == 2
        router = Router.objects.get(itemfk__partnumber='TESTPART20211105')

        # Ensure that the ops on the assembled component are added after the ops on the manufactured component
        routing_lines = Routerworkcenter.objects.filter(routerfk=router, workcenterfk__isnull=False)
        assert routing_lines.count() == 8
        forming_op = routing_lines.get(sequencenumber=5)
        assert 'This is the fifth step.' in forming_op.comment
        shipping_op = routing_lines.get(sequencenumber=8)
        assert 'This is the eighth step.' in shipping_op.comment

        # Make sure the purchase components and raw materials were added to the Router as BOM items
        bom_items = Routerworkcenter.objects.filter(routerfk=router, itemfk__isnull=False)
        assert bom_items.count() == 4
        bom_item_part_numbers = [bom_item.itemfk.partnumber for bom_item in bom_items]
        assert set(bom_item_part_numbers) == {'TEST_SHEET_STOCK', 'F-440-1', 'F-632-1', 'Tooling Charge'}

        # Check that add-ons are handled correctly by the assembly conversion logic
        add_on_bom_item = Routerworkcenter.objects.filter(itemfk=tooling_charge_item).first()
        assert add_on_bom_item is not None


@pytest.mark.django_db
class TestMieTrakProImporter:

    def test_account_importer(self, setup_account_importer):
        cust_num = str(random.randint(1, 10000))
        customer_name = cust_num + " Company"
        addr_dict1 = {'country': 'USA', 'state': 'NH', 'address1': '1200 Elm St.', 'address2': 'Unit 529',  # noqa: E128
                      'city': 'Manchester', 'postal_code': '03101', 'phone': '6035588221', 'phone_ext': '523',
                      # noqa: E128
                      'attention': 'Bob'}  # noqa: E128
        party = create_customer(customer_name)
        create_contact(party, customer_name, f"{cust_num}@gmail.com")
        get_or_create_billing_address(customer=party, addr_dict=addr_dict1)
        get_or_create_shipping_address(customer=party, addr_dict=addr_dict1)

        customer = Party.objects.filter(name=customer_name, customer=1).first()
        assert customer is not None
        billing_address = Address.objects.filter(partyfk=customer, addresstypefk__description='Billing').first()
        assert billing_address is not None

        setup_account_importer.run(account_id=party.partypk)
        accounts = Account.filter(erp_code=party.partypk)
        acct_found = False
        account = None
        for acct in accounts:
            account: Account = Account.get(acct.id)
            if account.name == customer_name:
                acct_found = True
                break
        assert acct_found and account is not None
        pp_contacts_list = Contact.filter(account_id=account.id)
        assert len(pp_contacts_list) > 0
        for c in pp_contacts_list:
            contact: Contact = Contact.get(id=c.id)
            assert (cust_num in contact.first_name or cust_num in contact.last_name)
            contact.delete()
        account.delete()

    def test_purchased_component_importer(self, setup_purchased_component_importer):
        customer_name = str(random.randint(1, 10000)) + " Company"
        partno = str(random.randint(1, 10000)) + "part"
        description = str(random.randint(1, 10000)) + "testing"
        party = create_customer(customer_name)
        calc_type = Calculationtype.objects.filter(code='101').first()
        um = RoutingLineProcessor.get_outside_service_item_unit_of_measure_set()
        manufactured = get_item_type(component_type='manufactured', is_raw_material=False, is_outside_process=False)
        item: Item = create_item(partno, "A", description, party, False, manufactured,
                                 calc_type, None, None, um, 1)
        setup_purchased_component_importer.run(purchased_component_id=item.itempk)  # Part is not posting to PP
        purchased_components: list = PurchasedComponent.search(partno)
        created = len(purchased_components)
        assert created > 0  # This assertion is throwing the error. Fix it.
        # run it a second time to ensure we don't create an unnecessary PC
        setup_purchased_component_importer.run(purchased_component_id=item.itempk)
        purchased_components: list = PurchasedComponent.search(partno)
        assert len(purchased_components) == created
        assert setup_purchased_component_importer._bulk_process_purchased_component(
            purchased_component_ids=[item.itempk])

    def test_material_importer(self, setup_material_importer, caplog):
        customer_name = str(random.randint(1, 10000)) + " Company"
        partno = str(random.randint(1, 10000)) + "part"
        description = str(random.randint(1, 10000)) + "testing"
        party = create_customer(customer_name)
        manufactured = get_item_type(component_type='manufactured', is_raw_material=False, is_outside_process=False)
        calc_type = Calculationtype.objects.filter(code='101').first()
        um = RoutingLineProcessor.get_outside_service_item_unit_of_measure_set()
        item: Item = create_item(partno, "A", description, party, False, manufactured,
                                 calc_type, None, None, um, 1)
        setup_material_importer.run(material_id=item.itempk)
        assert f"Processed {item.itempk} successfully" in caplog.text

    def test_outside_process_importer(self, setup_outside_process_importer, caplog):
        customer_name = str(random.randint(1, 10000)) + " Company"
        partno = str(random.randint(1, 10000)) + "part"
        description = str(random.randint(1, 10000)) + "testing"
        party = create_customer(customer_name)
        manufactured = get_item_type(component_type='manufactured', is_raw_material=False, is_outside_process=True)
        calc_type = Calculationtype.objects.filter(code='101').first()
        um = RoutingLineProcessor.get_outside_service_item_unit_of_measure_set()
        item: Item = create_item(partno, "A", description, party, False, manufactured,
                                 calc_type, None, None, um, 1)
        setup_outside_process_importer.run(service_id=item.itempk)
        assert f"Processed {item.itempk} successfully" in caplog.text

    def test_vendor_importer(self, setup_vendor_importer, caplog):
        vendor_num = str(random.randint(1, 10000))
        vendor_name = vendor_num + " Company"
        party = create_customer(vendor_name)
        party.customer = False
        party.supplier = True
        party.save()

        vendor = Party.objects.filter(name=vendor_name, supplier=1).first()
        assert vendor is not None

        setup_vendor_importer.run(vendor_id=party.partypk)

        assert f"Processed {party.partypk} successfully" in caplog.text

    def test_workcenter_importer(self, setup_workcenter_importer, caplog):
        setup_workcenter_importer.run(1)
        assert "Processed work center 1" in caplog.text

    def test_get_or_create_party_salesperson_salesperson_not_found(self, caplog):
        party_salesperson_processor = PartySalespersonProcessor(exporter=None)
        customer = Party()

        party_salesperson, is_party_salesperson_new = party_salesperson_processor.get_or_create_party_salesperson(
            customer, 1)
        assert "Could not find Salesperson with ID: 1 - not assigning salesperson for this customer" in caplog.text
        assert party_salesperson is None
        assert is_party_salesperson_new is False

    def test_get_or_create_order_salesperson_salesperson_not_found(self, caplog):
        order_salesperson_processor = OrderSalespersonProcessor(exporter=None)
        sales_order = Salesorder()

        order_salesperson, is_order_salesperson_new = order_salesperson_processor.get_or_create_order_salesperson(
            sales_order, 1)
        assert "Could not find Salesperson with ID: 1 - not assigning salesperson for this sales order" in caplog.text
        assert order_salesperson is None
        assert is_order_salesperson_new is False

    def test_import_listener_queries(self):
        purchased_component_import_config = PurchasedComponentImportConfig(should_skip_non_inventory_items=False,
                                                                           should_skip_inactive=False,
                                                                           should_import_category=False)
        purchased_component_listener = MietrakProPurchasedComponentListener(
            integration=None, erp_config=purchased_component_import_config
        )
        new_query: str = purchased_component_listener._get_new_query(10, 15)

        assert new_query == ("SELECT Item.ItemPK, Item.LastAccess FROM Item INNER JOIN ItemType ON Item.ItemTypeFK = "
                             "ItemType.ItemTypePK WHERE ItemType.Description = 'Hardware/Supplies' AND "
                             "Item.LastAccess > 0x0000000000000000 AND Item.ItemPK >= 15 UNION SELECT "
                             "ItemInventoryPK, Iteminventory.LastAccess FROM Iteminventory INNER JOIN Item ON "
                             "ItemInventory.ItemInventoryPK = Item.ItemPK INNER JOIN ItemType ON Item.ItemTypeFK = "
                             "ItemType.ItemTypePK WHERE ItemType.Description = 'Hardware/Supplies' AND "
                             "Iteminventory.LastAccess > 0x0000000000000000")

        material_import_config = MaterialImportConfig(should_skip_material_no_description=True,
                                                      should_skip_inactive=True)
        material_import_listener = MietrakProMaterialImportListener(integration=None, erp_config=material_import_config)
        new_query: str = material_import_listener._get_new_query(10, 15)
        assert new_query == ("SELECT Item.ItemPK, Item.LastAccess FROM Item INNER JOIN ItemType ON Item.ItemTypeFK = "
                             "ItemType.ItemTypePK WHERE ItemType.Description = 'Material' AND Item.LastAccess > "
                             "0x0000000000000000 AND Item.ItemPK >= 15 AND Item.InactiveDate IS NULL AND "
                             "Item.Description IS NOT NULL UNION SELECT ItemInventoryPK, Iteminventory.LastAccess "
                             "FROM Iteminventory INNER JOIN Item ON ItemInventory.ItemInventoryPK = Item.ItemPK "
                             "INNER JOIN ItemType ON Item.ItemTypeFK = ItemType.ItemTypePK WHERE "
                             "ItemType.Description = 'Material' AND "
                             "Iteminventory.LastAccess > 0x0000000000000000")

        outside_service_import_config = OutsideServiceImportConfig(part_number_exclusion_term="ten", starting_year=2000)
        outside_service_import_listener = MietrakProOutsideServiceImportListener(integration=None,
                                                                                 erp_config=outside_service_import_config)
        new_query: str = outside_service_import_listener._get_new_query(10, 15)
        assert new_query == ("SELECT Item.ItemPK, Item.LastAccess FROM Item INNER JOIN ItemType ON Item.ItemTypeFK = "
                             "ItemType.ItemTypePK WHERE ItemType.Description = 'Outside Process' AND Item.LastAccess "
                             "> 0x0000000000000000 AND Item.ItemPK >= 15 AND PartNumber NOT LIKE '%ten%' AND Item.CreateDate > '2000'")

        work_center_import_config = WorkCenterImportConfig(should_import_division=False)
        workcenter_listener = MietrakProWorkCenterImportListener(integration=None, erp_config=work_center_import_config)
        new_query: str = workcenter_listener._get_new_query(10, 15)
        assert new_query == "SELECT OperationPK, LastAccess FROM Operation"


@pytest.mark.django_db
class TestMieTrakProRepeatWorkImporter:

    def test_import_from_item(self, setup_repeat_work_importer, caplog):
        part_number = "mtp_test_part_1"

        item = Item(partnumber=part_number).fill_and_save()
        router_status = Routerstatus().fill_and_save()
        router = Router(itemfk=item, routerstatusfk=router_status).fill_and_save()

        parent_router_status = Routerstatus().fill_and_save()
        parent_router = Router(routerstatusfk=parent_router_status).fill_and_save()
        router_link: Routerworkcenter = Routerworkcenter(routerfk=parent_router, itemrouterfk=router,
                                                         quantityrequired=2).fill_and_save()

        setup_repeat_work_importer.run(repeat_work_id=str(item.pk))

        assert "Creating repeat part headers from Mie Trak Pro item ID" in caplog.text
        assert "Creating repeat part methods of manufacture from Mie Trak Pro item ID" in caplog.text

        parts = get_repeat_parts_from_backend(part_number)
        assert len(parts) == 1

        part = parts[0]
        headers = part["headers"]
        assert len(headers) == 2

        part_header = [h for h in headers if h["erp_code"] == str(router.pk)][0]
        assert part_header["type"] == "template"
        part_moms = part_header["methods_of_manufacture"]
        assert len(part_moms) == 1
        assert part_moms[0]["requested_qty"] == 1

        parent_header = [h for h in headers if h["erp_code"] == str(parent_router.pk)][0]
        assert parent_header["type"] == "template"
        parent_moms = parent_header["methods_of_manufacture"]
        assert len(parent_moms) == 1
        assert parent_moms[0]["requested_qty"] == router_link.quantityrequired

    def test_import_from_quote(self, setup_repeat_work_importer, caplog):
        part_number = "mtp_test_part_2"

        item = Item(partnumber=part_number).fill_and_save()
        quote = MTPQuote(itemfk=item).fill_and_save()

        parent_quote = MTPQuote().fill_and_save()
        quantity1 = Quotequantity(quotefk=parent_quote, quantity=5).fill_and_save()
        quantity2 = Quotequantity(quotefk=parent_quote, quantity=10).fill_and_save()
        quote_link: Quoteassembly = Quoteassembly(quotefk=parent_quote, itemquotefk=quote,
                                                  quantityrequired=2).fill_and_save()

        setup_repeat_work_importer.run(repeat_work_id=str(item.pk))

        assert "Creating repeat part headers from Mie Trak Pro item ID" in caplog.text
        assert "Creating repeat part methods of manufacture from Mie Trak Pro item ID" in caplog.text

        parts = get_repeat_parts_from_backend(part_number, root_only=False)
        assert len(parts) == 1

        part = parts[0]
        headers = part["headers"]
        assert len(headers) == 1

        parent_header = [h for h in headers if h["erp_code"] == str(parent_quote.pk)][0]
        assert parent_header["type"] == "estimated"

        parent_moms = parent_header["methods_of_manufacture"]
        assert len(parent_moms) == 2
        quantities = set([m["requested_qty"] for m in parent_moms])
        assert quantities == {quote_link.quantityrequired * quantity1.quantity,
                              quote_link.quantityrequired * quantity2.quantity}

    def test_import_from_job(self, setup_repeat_work_importer, caplog):
        part_number = "mtp_test_part_3"

        item = Item(partnumber=part_number).fill_and_save()
        parent_work_order = Workorder().fill_and_save()
        work_order: Workorderrelease = Workorderrelease(itemfk=item, workorderfk=parent_work_order,
                                                        quantityrequired=2).fill_and_save()
        Workordercompletion(workorderfk=parent_work_order).fill_and_save()

        setup_repeat_work_importer.run(repeat_work_id=str(item.pk))

        assert "Creating repeat part headers from Mie Trak Pro item ID" in caplog.text
        assert "Creating repeat part methods of manufacture from Mie Trak Pro item ID" in caplog.text

        parts = get_repeat_parts_from_backend(part_number, root_only=False)
        assert len(parts) == 1

        part = parts[0]
        headers = part["headers"]
        assert len(headers) == 2

        engineered_header = [h for h in headers
                             if h["erp_code"] == str(parent_work_order.pk) and h["type"] == "engineered"][0]
        engineered_moms = engineered_header["methods_of_manufacture"]
        assert len(engineered_moms) == 1
        assert engineered_moms[0]["requested_qty"] == work_order.quantityrequired

        executed_header = [h for h in headers
                           if h["erp_code"] == str(parent_work_order.pk) and h["type"] == "executed"][0]
        executed_moms = executed_header["methods_of_manufacture"]
        assert len(executed_moms) == 1
        assert executed_moms[0]["requested_qty"] == work_order.quantityrequired
