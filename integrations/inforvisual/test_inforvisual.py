import os
import sys

import pendulum
import pytest
import random
import datetime
from paperless.objects.purchased_components import PurchasedComponent

# append to path
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))

# import models
from baseintegration.integration import Integration
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from baseintegration.utils.test_utils import get_order, get_repeat_parts_from_backend
from inforvisual.models import Customer, Part, PartSite, WorkOrder, ShopResource, Product, Requirement, CustContact, \
    Contact, PurchaseOrder, PurcOrderLine, QuoteLine, Operation, Quote, QuotePrice, DemandSupplyLink, CustOrderLine
from paperless.objects.customers import Account, Contact as PaperlessContact


@pytest.fixture
def setup_exporter():
    """Create integration to process orders"""
    integration = Integration()
    from inforvisual.exporter.exporter import InforVisualOrderExporter
    i = InforVisualOrderExporter(integration)
    ShopResource.objects.create(id="PPDEFAULT")
    Product.objects.create(code="CUSTOMER", rev_gl_acct_id="4000")
    Product.objects.create(code="SERVICE", rev_gl_acct_id="4001")
    return i


@pytest.fixture
def setup_account_importer():
    integration = Integration()
    from inforvisual.importer.importer import InforVisualAccountImporter
    return InforVisualAccountImporter(integration)


@pytest.fixture
def setup_purchased_component_importer():
    integration = Integration()
    from inforvisual.importer.importer import InforVisualPurchasedComponentImporter
    return InforVisualPurchasedComponentImporter(integration)


@pytest.fixture
def setup_material_importer():
    integration = Integration()
    from inforvisual.importer.importer import InforVisualMaterialImporter
    return InforVisualMaterialImporter(integration)


@pytest.fixture
def setup_repeat_work_importer():
    integration = Integration()
    integration.config_yaml["Importers"] = {"repeat_part": {"is_post_enabled": True}}
    from inforvisual.importer.repeat_part_importer import InforVisualRepeatPartImporter
    return InforVisualRepeatPartImporter(integration)


@pytest.mark.django_db
class TestInforvisualOrderExporter:
    """Runs tests against a dummy database using models.py"""

    def test_process_single_customer(self, setup_exporter):
        c = Customer.objects.count()
        assert c == 0
        setup_exporter._process_order(get_order(4))
        c = Customer.objects.count()
        assert c == 1

    def test_customer_attributes(self, setup_exporter):
        setup_exporter._process_order(get_order(4))
        c = Customer.objects.filter(id="MAINE").first()
        assert c.name == "Maine Blueberry Co"
        assert c.addr_1 == "100 Commercial Street"
        assert c.city == "Portland"
        assert c.state == "ME"
        assert c.zipcode == "04101"
        assert c.country == "USA"
        assert c.bill_to_name == "Maine Blueberry Co"
        assert c.bill_to_addr_1 == "100 Commercial Street"
        assert c.bill_to_city == "Portland"
        assert c.bill_to_state == "ME"
        assert c.bill_to_country == "USA"
        assert c.bill_to_zipcode == "04101"

    def test_customer_update_existing(self, setup_exporter):
        # update tax exempt, payment terms, payment terms period
        order = get_order(4)
        setup_exporter._process_order(order)
        order = get_order(3)
        order.contact.account.payment_terms = "Net 60"
        order.contact.account.payment_terms_period = 60
        setup_exporter._process_order(order)
        c = Customer.objects.first()
        assert c.id == "MAINE"
        assert c.terms_description == "Net 60"
        assert str(c.terms_net_days) == "60"

    def test_create_customer(self, setup_exporter):
        setup_exporter.erp_config.update_customers = False
        setup_exporter.erp_config.send_email_when_customer_not_found = True
        with pytest.raises(CancelledIntegrationActionException) as e:
            setup_exporter._process_order(get_order(134))
        assert "We're not bringing it over" in str(e.value)

    def test_do_not_duplicate_id(self, setup_exporter):
        setup_exporter._process_order(get_order(4))
        setup_exporter._process_order(get_order(3))
        c = Customer.objects.count()
        assert c == 1

    def test_process_parts(self, setup_exporter):
        assert Part.objects.count() == 0
        setup_exporter._process_order(get_order(4))
        assert Part.objects.count() == 4
        setup_exporter._process_order(get_order(134))
        assert Part.objects.count() == 5

    def test_duplicate_parts(self, setup_exporter):
        setup_exporter._process_order(get_order(4))
        assert Part.objects.count() == 4
        setup_exporter._process_order(get_order(7))
        assert Part.objects.count() == 4

    def test_part_attributes(self, setup_exporter):
        setup_exporter._process_order(get_order(4))
        part = Part.objects.filter(id="040821").first()
        assert part.commodity_code == "CUSTOMER"
        assert part.product_code == "CUSTOMER"
        assert part.stock_um == "EA"

    def test_part_site(self, setup_exporter):
        setup_exporter._process_order(get_order(4))
        part_site = PartSite.objects.filter(part_id="040821").first()
        assert part_site.site_id == "MTI"

    def test_process_single_work_order(self, setup_exporter):
        assert WorkOrder.objects.count() == 0
        setup_exporter._process_order(get_order(4))
        assert WorkOrder.objects.count() == 4

    def test_process_without_resource(self, setup_exporter, caplog):
        ShopResource.objects.first().delete()
        setup_exporter._process_order(get_order(4))
        assert "Resource ID not found on operation. Must be an informational operation." in caplog.text

    def test_assembly(self, setup_exporter):
        setup_exporter._process_order(get_order(8))
        assert WorkOrder.objects.count() == 6
        assert Part.objects.count() == 7
        assert Requirement.objects.count() == 5

    def test_duplicate_components_with_config_option(self, setup_exporter):
        setup_exporter.erp_config.should_export_assemblies_with_duplicate_components = True
        order = get_order(178)
        setup_exporter._process_order(order)
        expected_work_order_count = sum(1 for assm_comp in order.order_items[0].iterate_assembly_with_duplicates() if assm_comp.component.type != 'purchased')
        assert WorkOrder.objects.count() == expected_work_order_count
        assert Requirement.objects.count() > 0


@pytest.mark.django_db
class TestInforvisualImporter:

    def test_account_importer(self, setup_account_importer):
        customer_name = str(random.randint(1, 100000)) + " Company"
        addr = str(random.randint(100, 200))
        contact_addr = str(random.randint(300, 400))
        addr = addr + " Commercial Street"
        contact_addr = contact_addr + " Contact Street"
        customer = Customer.objects.create(
            id="BOAT",
            name=customer_name,
            addr_1=addr,
            city="Portland",
            state="ME",
            country="United States",
            zipcode="04101",
            status_eff_date=datetime.datetime.now())
        contact = Contact.objects.create(
            id="FACE",
            email="face@face.com",
            first_name="Boaty",
            last_name="McBoatFace",
            phone='123-456-7890',
            phone_ext='1',
            addr_1=contact_addr,
            city="Portland",
            state="ME",
            country="United States",
            zipcode="04101")
        CustContact.objects.create(customer=customer, contact=contact)

        setup_account_importer.run(account_id="BOAT")

        accounts = Account.filter(erp_code="BOAT")
        account: Account = Account.get(accounts[0].id)
        assert account.name == customer_name
        assert addr in account.sold_to_address.address1

        pp_contacts = PaperlessContact.filter(account_id=account.id)
        pp_contact: PaperlessContact = PaperlessContact.get(pp_contacts[0].id)
        assert pp_contact.email == contact.email
        assert pp_contact.first_name == contact.first_name
        assert pp_contact.last_name == contact.last_name
        assert pp_contact.address.address1 == contact.addr_1

    def test_purchased_component_importer(self, setup_purchased_component_importer):
        partno = str(random.randint(1, 1000000)) + "part"
        description = str(random.randint(1, 10000)) + "testing"
        Part.objects.create(id=partno,
                            stock_um="EA",
                            minimum_order_qty=1,
                            planning_leadtime=40,
                            order_policy="D",
                            fabricated="Y",
                            purchased="N",
                            stocked="N",
                            detail_only="N",
                            demand_history="N",
                            tool_or_fixture="N",
                            inspection_reqd="N",
                            mrp_required="N",
                            mrp_exceptions="N",
                            inventory_locked="N",
                            use_supply_bef_lt="Y",
                            ecn_rev_control="N",
                            is_kit="N",
                            controlled_by_ics="N",
                            qty_committed=0,
                            intrastat_exempt="N",
                            description=description,
                            status_eff_date=datetime.datetime.now(),
                            create_date=datetime.datetime.now())
        # we must create an object in both part and partsite
        PartSite.objects.create(site_id="MTI",
                                part_id=partno,
                                intrastat_exempt="N",
                                status="A",
                                engineering_mstr="0",
                                is_rate_based="N",
                                primary_whs_id="MTI",
                                primary_loc_id="STAGING",
                                create_date=datetime.datetime.now())
        setup_purchased_component_importer.run(partno)
        purchased_components: list = PurchasedComponent.search(partno)
        assert purchased_components[0].oem_part_number == partno
        assert purchased_components[0].internal_part_number == partno
        assert purchased_components[0].description == description

    def test_purchased_component_importer_from_purchase_order(self, setup_purchased_component_importer):
        setup_purchased_component_importer.listener.erp_config.import_from_purchase_orders = True
        partno = str(random.randint(1, 1000000)) + "part"
        purchase_order = PurchaseOrder.objects.create(
            id="test",
            order_date=datetime.datetime.now(),
            sell_rate=0.0,
            buy_rate=0.0,
            total_amt_ordered=0.0,
            total_amt_recvd=0.0,
            create_date=datetime.datetime.now(),
            status_eff_date=datetime.datetime.now(),
        )
        PurcOrderLine.objects.create(
            purc_order=purchase_order,
            vendor_part_id=partno,
            line_no=1,
            user_order_qty=1,
            order_qty=1,
            unit_price=5.0,
            trade_disc_percent=3.0,
            est_freight=1.0,
            total_act_freight=1.0,
            total_usr_recd_qty=1.0,
            total_received_qty=1.0,
            total_amt_recvd=1.0,
            total_amt_ordered=1.0,
            total_dispatch_qty=1.0,
            total_usr_disp_qty=1.0,
            allocated_qty=1.0,
            fulfilled_qty=1.0,
            status_eff_date=datetime.datetime.now(),
        )
        setup_purchased_component_importer.run("test")
        purchased_components: list = PurchasedComponent.search(partno)
        assert purchased_components[0].oem_part_number == partno
        assert float(purchased_components[0].piece_price) == 5.0
        assert setup_purchased_component_importer._bulk_process_purchased_component([partno])

    def test_material_importer(self, setup_material_importer, caplog):
        partno = str(random.randint(1, 1000000)) + "part"
        description = str(random.randint(1, 10000)) + "testing"
        Part.objects.create(id=partno,
                            stock_um="EA",
                            minimum_order_qty=1,
                            planning_leadtime=40,
                            order_policy="D",
                            fabricated="Y",
                            purchased="N",
                            stocked="N",
                            detail_only="N",
                            demand_history="N",
                            tool_or_fixture="N",
                            inspection_reqd="N",
                            mrp_required="N",
                            mrp_exceptions="N",
                            inventory_locked="N",
                            use_supply_bef_lt="Y",
                            ecn_rev_control="N",
                            is_kit="N",
                            controlled_by_ics="N",
                            qty_committed=0,
                            intrastat_exempt="N",
                            description=description,
                            status_eff_date=datetime.datetime.now(),
                            create_date=datetime.datetime.now())
        # we must create an object in both part and partsite
        PartSite.objects.create(site_id="MTI",
                                part_id=partno,
                                intrastat_exempt="N",
                                status="A",
                                engineering_mstr="0",
                                is_rate_based="N",
                                primary_whs_id="MTI",
                                primary_loc_id="STAGING",
                                create_date=datetime.datetime.now())
        setup_material_importer.run(partno)
        assert "Processed Inforvisual-material-bulk-upload-count-1 successfully" in caplog.text
        assert setup_material_importer._bulk_process_material([partno])


@pytest.mark.django_db
class TestInforvisualRepeatWorkImporter:

    def test_repeat_part_listener(self, setup_repeat_work_importer, caplog, mocker):
        # part1 has been updated recently
        Part(
            id="part1",
            modify_date=datetime.datetime.now(),
        ).fill_and_save()

        # part2 has not been updated recently
        part2 = Part(
            id="part2",
            modify_date=pendulum.naive(year=1970, month=1, day=2)
        ).fill_and_save()

        PartSite(
            part=part2,
            modify_date=pendulum.naive(year=1970, month=1, day=2)
        ).fill_and_save()

        WorkOrder(
            part=part2,
            create_date=pendulum.naive(year=1970, month=1, day=2)
        ).fill_and_save()

        quote = Quote(
            id="123",
            create_date=pendulum.naive(year=1970, month=1, day=2),
        ).fill_and_save()

        QuoteLine(
            quote=quote,
            part=part2,
            create_date=pendulum.naive(year=1970, month=1, day=2)
        ).fill_and_save()

        # part3 is tied to a part site that has been updated recently
        part3 = Part(
            id="part3",
            modify_date=pendulum.naive(year=1970, month=1, day=2)
        ).fill_and_save()

        PartSite(
            part=part3,
            modify_date=datetime.datetime.now()
        ).fill_and_save()

        mocker.patch('inforvisual.importer.repeat_part_importer.get_last_action_datetime_sql',
                     return_value=pendulum.naive(year=1980, month=1, day=2))

        new_parts = setup_repeat_work_importer.listener.get_new(bulk=False)

        assert set(new_parts) == {"part1", "part3"}

    def test_import_from_engineering_master(self, setup_repeat_work_importer, caplog):
        part_number = "infor_visual_test_part_123"
        child_part_number = "infor_visual_child_part_123"

        # create parent part

        part: Part = Part(
            id=part_number,
            revision_id="rev124"
        ).fill_and_save()

        work_order: WorkOrder = WorkOrder(
            rowid="2",
            part=part,
            type="M",
            base_id="root-job",
            sub_id="0"
        ).fill_and_save()

        # create child part

        child_part: Part = Part(
            id=child_part_number,
            revision_id="rev123",
            purchased="N"
        ).fill_and_save()

        child_work_order: WorkOrder = WorkOrder(
            rowid="1",
            part=child_part,
            type=work_order.type,
            base_id=work_order.base_id,
            lot_id=work_order.lot_id,
            split_id=work_order.split_id,
            sub_id="1"
        ).fill_and_save()

        self.create_test_requirements_and_operations(work_order, child_work_order)

        setup_repeat_work_importer.run(part_number)

        self.check_repeat_part_imported_correctly(
            part_number=part_number,
            child_part_number=child_part_number,
            expected_types=["template"],
            caplog=caplog
        )

    def test_import_from_quote_line(self, setup_repeat_work_importer, caplog):
        part_number = "infor_visual_test_part_125"
        child_part_number = "infor_visual_child_part_125"

        # create parent part

        part: Part = Part(
            id=part_number,
            revision_id="rev124"
        ).fill_and_save()

        work_order: WorkOrder = WorkOrder(
            rowid="2",
            part=part,
            type="Q",
            base_id="root-job",
            sub_id="0"
        ).fill_and_save()

        # create child part

        child_part: Part = Part(
            id=child_part_number,
            revision_id="rev123",
            purchased="N"
        ).fill_and_save()

        child_work_order: WorkOrder = WorkOrder(
            rowid="1",
            part=child_part,
            type=work_order.type,
            base_id=work_order.base_id,
            lot_id=work_order.lot_id,
            split_id=work_order.split_id,
            sub_id="1"
        ).fill_and_save()

        quote_line: QuoteLine = QuoteLine(
            part=part,
            workorder_type=work_order.type,
            workorder_base_id=work_order.base_id,
            workorder_lot_id=work_order.lot_id,
            workorder_split_id=work_order.split_id,
            workorder_sub_id=work_order.sub_id,
        ).fill_and_save()

        QuotePrice(
            quote=quote_line.quote,
            quote_line_no=quote_line.line_no
        ).fill_and_save()

        self.create_test_requirements_and_operations(work_order, child_work_order)

        setup_repeat_work_importer.run(part_number)

        self.check_repeat_part_imported_correctly(
            part_number=part_number,
            child_part_number=child_part_number,
            expected_types=["estimated"],
            caplog=caplog
        )

    def test_import_from_job_work_order(self, setup_repeat_work_importer, caplog):
        part_number = "infor_visual_test_part_124"
        child_part_number = "infor_visual_child_part_124"

        # create parent part

        part: Part = Part(
            id=part_number,
            revision_id="rev124"
        ).fill_and_save()

        work_order: WorkOrder = WorkOrder(
            rowid="2",
            part=part,
            type="W",
            base_id="root-job",
            sub_id="0"
        ).fill_and_save()

        # create child part

        child_part: Part = Part(
            id=child_part_number,
            revision_id="rev123",
            purchased="N"
        ).fill_and_save()

        child_work_order: WorkOrder = WorkOrder(
            rowid="1",
            part=child_part,
            type=work_order.type,
            base_id=work_order.base_id,
            lot_id=work_order.lot_id,
            split_id=work_order.split_id,
            sub_id="1"
        ).fill_and_save()

        # create customer order

        cust_order_line: CustOrderLine = CustOrderLine(
            line_no=1
        ).fill_and_save()

        DemandSupplyLink(
            demand_type='CO',
            supply_type='WO',
            supply_base_id=work_order.base_id,
            supply_lot_id=work_order.lot_id,
            supply_split_id=work_order.split_id,
            supply_sub_id=work_order.sub_id,
            demand_base_id=cust_order_line.cust_order_id,
            demand_seq_no=cust_order_line.line_no
        ).fill_and_save()

        self.create_test_requirements_and_operations(work_order, child_work_order)

        setup_repeat_work_importer.run(part_number)

        self.check_repeat_part_imported_correctly(
            part_number=part_number,
            child_part_number=child_part_number,
            expected_types=["engineered", "executed"],
            caplog=caplog
        )

    # all methods below are utilities

    def create_test_requirements_and_operations(self, work_order: WorkOrder, child_work_order: WorkOrder):
        material_part: Part = Part(
            id="material-part"
        ).fill_and_save()

        child_material_part: Part = Part(
            id="child-material-part"
        ).fill_and_save()

        Requirement(
            part=material_part,
            piece_no=1,
            workorder_type=work_order.type,
            workorder_base=work_order.base_id,
            workorder_lot=work_order.lot_id,
            workorder_split=work_order.split_id,
            workorder_sub=work_order.sub_id,
        ).fill_and_save()

        Requirement(
            part=child_work_order.part,
            piece_no=2,
            subord_wo_sub=child_work_order.sub_id,
            workorder_type=work_order.type,
            workorder_base=work_order.base_id,
            workorder_lot=work_order.lot_id,
            workorder_split=work_order.split_id,
            workorder_sub=work_order.sub_id,
        ).fill_and_save()

        Requirement(
            part=child_material_part,
            piece_no=3,
            workorder_type=child_work_order.type,
            workorder_base=child_work_order.base_id,
            workorder_lot=child_work_order.lot_id,
            workorder_split=child_work_order.split_id,
            workorder_sub=child_work_order.sub_id,
        ).fill_and_save()

        resource: ShopResource = ShopResource(
            id="test-work-center",
            description="Fake Work Center"
        ).fill_and_save()

        Operation(
            resource=resource,
            workorder_type=work_order.type,
            workorder_base=work_order.base_id,
            workorder_lot=work_order.lot_id,
            workorder_split=work_order.split_id,
            workorder_sub=work_order.sub_id,
        ).fill_and_save()

    def check_repeat_part_imported_correctly(self, part_number, child_part_number, expected_types, caplog):
        # ensure parent part is processed

        assert "Creating repeat part methods of manufacture from item ID:" in caplog.text
        assert "Creating repeat part headers from item ID:" in caplog.text
        assert "Creating repeat part from item ID:" in caplog.text

        parts = get_repeat_parts_from_backend(part_number)
        assert len(parts) == 1

        repeat_part = parts[0]
        headers = repeat_part["headers"]
        assert len(headers) == len(expected_types)
        assert set([h["type"] for h in headers]) == set(expected_types)

        for header in headers:
            moms = header["methods_of_manufacture"]
            assert len(moms) == 1
            method_of_manufacture = moms[0]

            materials = method_of_manufacture["required_materials"]
            assert len(materials) == 1

            operations = method_of_manufacture["operations"]
            assert len(operations) == 1

            children = method_of_manufacture["children"]
            assert len(children) == 1

        # ensure child part is processed

        assert "Creating repeat part methods of manufacture from item ID:" in caplog.text
        assert "Creating repeat part headers from item ID:" in caplog.text
        assert "Creating repeat part from item ID:" in caplog.text

        parts = get_repeat_parts_from_backend(child_part_number)
        assert len(parts) == 1

        repeat_part = parts[0]
        headers = repeat_part["headers"]

        assert len(headers) == len(expected_types)
        assert set([h["type"] for h in headers]) == set(expected_types)

        for header in headers:
            moms = header["methods_of_manufacture"]
            assert len(moms) == 1
            method_of_manufacture = moms[0]

            materials = method_of_manufacture["required_materials"]
            assert len(materials) == 1

            operations = method_of_manufacture["operations"]
            assert len(operations) == 0

            children = method_of_manufacture["children"]
            assert len(children) == 0
