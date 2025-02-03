# import standard libraries
import pytest
import os
import uuid
import sys
from paperless.objects.orders import Order
from django.utils.timezone import make_aware

# append to path
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))

# import helper functions
from jobboss.query.customer import tokenize, filter_exact_customer_name, \
    filter_fuzzy_customer_name, increment_code, get_available_customer_code, \
    get_or_create_customer, get_or_create_contact, match_address, \
    get_available_address_code, get_or_create_address, \
    get_address_types_by_customer
from jobboss.query.job import shipping_option_summary, increment_job, \
    get_default_vendor, get_default_work_center, DEFAULT_VENDOR_NAME, \
    DEFAULT_WORK_CENTER_NAME, get_material
from jobboss.models import Customer, Contact, Address, Service, VendorService, JobOperation, Employee
from jobboss.models import WorkCenter, Vendor, Material, Rfq, Quote, QuoteQty, AutoNumber
from jobboss.exporter.routing import generate_routing_lines, OP_MAP, FINISH_MAP, is_inside_op, \
    is_outside_op, RoutingLine
from jobboss.exporter.processors.job_operation import JobOperationProcessor
from jobboss.exporter.exporter import JobBossQuoteExporter
from jobboss.importer.importer import JobBossWorkCenterImporter, JobBossOutsideServiceImporter
from baseintegration.integration import Integration
from baseintegration.utils.test_utils import get_order, get_quote
from baseintegration.utils import address_tokenize

# import config
import datetime

CUST_CODE = 'CUST01'
JB_NAME = 'CUSTOMER 1'
PP_NAME = 'Customer 1 '
JB_CONTACT_NAME = 'JOHN SMITH'
PP_CONTACT_NAME = 'John Smith'
ADDR_DICT = {
    'business_name': 'Customer 1',
    'city': 'Washington',
    'country': 'USA',
    'first_name': 'John',
    'last_name': 'Smith',
    'address1': '1600 Penn Ave',
    'address2': None,
    'phone': '123-456-7890',
    'phone_ext': None,
    'postal_code': '20500',
    'state': 'DC'
}
SHIPPING_OPTION_1 = {
    'customers_account_number': '12345',
    'customers_carrier': 'UPS',
    'shipping_method': 'ground'
}

SHIPPING_OPTION_2 = {
    'customers_account_number': None,
    'customers_carrier': None,
    'shipping_method': 'next day'
}


@pytest.fixture
def jb_order_exporter():
    """Create integration and register the customer processor to process orders"""
    integration = Integration()
    from jobboss.exporter.exporter import JobBossOrderExporter
    jb_order_exporter = JobBossOrderExporter(integration)
    customer = Customer.objects.create(
        customer=CUST_CODE,
        name=JB_NAME,
        last_updated=make_aware(datetime.datetime.utcnow()),
        print_statement=False,
        accept_bo=False,
        send_report_by_email=False,
        status='Active'
    )
    Contact.objects.create(
        customer=CUST_CODE,
        contact_name=JB_CONTACT_NAME,
        last_updated=make_aware(datetime.datetime.utcnow())
    )
    Address.objects.create(
        customer=customer,
        status='Active',
        type='000',
        ship_to_id='SHIP',
        line1=ADDR_DICT['address1'].upper(),
        line2=ADDR_DICT['address2'],
        city=ADDR_DICT['city'].upper(),
        state=ADDR_DICT['state'].upper(),
        zip=ADDR_DICT['postal_code'],
        name='{} {}'.format(ADDR_DICT['first_name'],
                            ADDR_DICT['last_name']).upper(),
        country='US',
        phone=ADDR_DICT['phone'],
        lead_days=0,
        last_updated=make_aware(datetime.datetime.utcnow()),
        billable=False,
        shippable=True
    )
    Employee.objects.create(
        employee="RLANCE",
        type="Other",
        status="Active",
        class_field="E",
        last_updated=make_aware(datetime.datetime.utcnow()),
        tran_repeater=False,
        objectid=uuid.uuid4()
    )
    return jb_order_exporter


@pytest.mark.django_db
class TestCustomer:

    def test_tokenize(self, jb_order_exporter):
        assert ['one', 'two', 'three'] == tokenize('One, Two, & Three')
        assert ['one', 'two', 'three', 'four'] == tokenize('One, Two, & Three, Inc. d/b/a Four')
        assert ['inc'] == tokenize('Inc.')

    def test_exact_name_match(self, jb_order_exporter):
        assert filter_exact_customer_name('bad name') is None
        assert JB_NAME == filter_exact_customer_name(JB_NAME).name

    def test_fuzzy_name_match(self, jb_order_exporter):
        assert filter_fuzzy_customer_name('bad name') is None
        assert JB_NAME == filter_fuzzy_customer_name(PP_NAME).name
        assert JB_NAME == filter_fuzzy_customer_name(PP_NAME + ', Inc.').name
        assert filter_fuzzy_customer_name('1 customer') is None

    def test_code_mutation(self, jb_order_exporter):
        assert 'CUST1' == increment_code('CUST')
        assert 'CUST2' == increment_code('CUST1')
        assert 'CUSTOMERA1' == increment_code('CUSTOMERAB')
        assert 'CUSTOMER10' == increment_code('CUSTOMERA9')
        assert 'Strange c1' == increment_code('Strange case 13 ')
        assert 'ABCDE1' == increment_code('ABCDEF', 6)
        assert 'ABCDE2' == increment_code('ABCDE1', 6)

    def test_available_code(self, jb_order_exporter):
        assert 'TEST' == get_available_customer_code('test')
        assert 'CUST2' == get_available_customer_code(CUST_CODE)

    def test_customer_get_or_create(self, jb_order_exporter):
        c = Customer.objects.count()
        customer = get_or_create_customer(PP_NAME)
        assert Customer.objects.count()
        assert JB_NAME == customer.name
        customer.status = 'Inactive'
        customer.save()
        customer = get_or_create_customer(PP_NAME)
        assert 'Active' == customer.status
        customer = get_or_create_customer('Paperless')
        assert c + 1 == Customer.objects.count()
        assert 'PAPERLESS' == customer.customer
        assert 'Paperless' == customer.name
        # test that we can look this up by code
        customer = get_or_create_customer('Other name', code='PAPERLESS')
        assert c + 1 == Customer.objects.count()
        assert 'PAPERLESS' == customer.customer
        assert 'Paperless' == customer.name
        assert customer.accept_bo is False
        # test that we can set a field by kwarg
        customer = get_or_create_customer('Customer 2', accept_bo=True)
        assert c + 2 == Customer.objects.count()
        assert customer.accept_bo is True

    def test_contact_get_or_create(self, jb_order_exporter):
        customer = Customer.objects.first()
        c = Contact.objects.count()
        contact = get_or_create_contact(customer, PP_CONTACT_NAME)
        assert c == Contact.objects.count()
        assert contact.contact_name == JB_CONTACT_NAME
        contact = get_or_create_contact(customer, 'Jane Smith')
        assert c + 1 == Contact.objects.count()
        assert contact.contact_name == 'Jane Smith'
        assert CUST_CODE == contact.customer
        assert contact.contact > 0

    def test_match_address(self, jb_order_exporter):
        customer = Customer.objects.first()
        address = match_address(customer, ADDR_DICT)
        assert ADDR_DICT['address1'].upper() == address.line1
        d = ADDR_DICT.copy()
        d['address1'] = '1600 Pennsylvania Ave NW'  # not a match
        assert match_address(customer, d) is None

        # try some fuzzier cases
        d = ADDR_DICT.copy()
        d['address1'] = '1600 Penn Avenue'
        d['phone'] = '1234567890'
        d['postal_code'] = '20500-1234'
        address = match_address(customer, d)
        assert address is not None
        d = ADDR_DICT.copy()
        d['postal_code'] = '20501-1234'
        address = match_address(customer, d)
        assert address is None
        d = ADDR_DICT.copy()
        d['postal_code'] = '20501'
        address = match_address(customer, d)
        assert address is None
        d = ADDR_DICT.copy()
        d['phone'] = '2015551212'
        address = match_address(customer, d)
        assert address is None

    def test_address_code(self, jb_order_exporter):
        customer = Customer.objects.first()
        assert 'BILL' == get_available_address_code(customer, ship=False)
        assert 'SHIP1' == get_available_address_code(customer, ship=True)

    def test_address_get_or_create(self, jb_order_exporter):
        customer = Customer.objects.first()
        c = Address.objects.count()
        address = get_or_create_address(customer, ADDR_DICT, True)
        assert c == Address.objects.count()
        assert ADDR_DICT['address1'].upper() == address.line1
        assert address.billable is False
        assert '001' == address.type  # set to default shipping
        address = get_or_create_address(customer, ADDR_DICT, False)
        assert address.billable
        assert '011' == address.type  # set to default billing
        d = ADDR_DICT.copy()
        d['address1'] = '1600 Pennsylvania Ave NW'  # not a match
        address = get_or_create_address(customer, d, True)
        assert c + 1 == Address.objects.count()
        assert address.shippable is True
        assert address.billable is False
        assert address.ship_to_id.startswith('SHIP')
        assert '100' == address.type

    def test_address_types(self, jb_order_exporter):
        customer = Customer.objects.first()
        m, b, s = get_address_types_by_customer(customer)
        assert m is False
        assert b is False
        assert s is False

        customer = Customer.objects.create(
            customer='CUST02',
            name='CUSTOMER 2',
            last_updated=make_aware(datetime.datetime.utcnow()),
            print_statement=False,
            accept_bo=False,
            send_report_by_email=False
        )
        # add addresses to this customer until they have all address types
        for type_str, type_tuple in [
            ('000', (False, False, False)),
            ('100', (True, False, False)),
            ('010', (True, True, False)),
            ('001', (True, True, True)),
        ]:
            Address.objects.create(
                customer=customer,
                status='Active',
                type=type_str,
                ship_to_id='SHIP',
                line1=ADDR_DICT['address1'].upper(),
                line2=ADDR_DICT['address2'],
                city=ADDR_DICT['city'].upper(),
                state=ADDR_DICT['state'].upper(),
                zip=ADDR_DICT['postal_code'],
                name='{} {}'.format(ADDR_DICT['first_name'],
                                    ADDR_DICT['last_name']).upper(),
                country='US',
                phone=ADDR_DICT['phone'],
                lead_days=0,
                last_updated=make_aware(datetime.datetime.utcnow()),
                billable=False,
                shippable=True
            )
            assert type_tuple == get_address_types_by_customer(customer)

    def test_address_tokenize(self, jb_order_exporter):
        assert ['123', 'main', 'st'] == address_tokenize('123 Main Street')
        assert ['123', 'main', 'st'] == address_tokenize('123 Main St.')

    def test_initial_address(self, jb_order_exporter):
        """Test that new customers have default billing and shipping
        addresses."""
        business_name = "Big Co."
        erp_code = "BIGCO"
        address = {
            'business_name': business_name,
            'city': 'Miami',
            'country': 'USA',
            'first_name': 'Joe',
            'last_name': 'Schmo',
            'address1': '123 NW 7th Ave',
            'address2': None,
            'phone': '123-456-7890',
            'phone_ext': None,
            'postal_code': '33136-1234',
            'state': 'FL'
        }
        customer = get_or_create_customer(business_name, erp_code)
        assert (False, False, False) == get_address_types_by_customer(customer)
        contact = get_or_create_contact(customer, "Joe Schmo")
        bill_to = get_or_create_address(customer, address, False)
        contact.address = bill_to.address
        get_or_create_address(customer, address, True)
        contact.save()
        # address should be 111
        assert (True, True, True) == get_address_types_by_customer(customer)


@pytest.mark.django_db
class TestJob:

    def test_ship_via(self, jb_order_exporter):
        assert 'UPS 12345' == shipping_option_summary(SHIPPING_OPTION_1)
        assert 'next day' == shipping_option_summary(SHIPPING_OPTION_2)

    def test_increment_job(self, jb_order_exporter):
        assert '123-1a' == increment_job('123-1')
        assert '123-1b' == increment_job('123-1a')

    def test_default_wc(self, jb_order_exporter):
        c = WorkCenter.objects.count()
        wc = get_default_work_center()
        assert DEFAULT_WORK_CENTER_NAME == wc.work_center
        assert c + 1 == WorkCenter.objects.count()
        wc = get_default_work_center()
        assert DEFAULT_WORK_CENTER_NAME == wc.work_center
        assert c + 1 == WorkCenter.objects.count()

    def test_email_sent_on_job_creation(self, jb_order_exporter, caplog):

        import jobboss.models as jb
        jb.AutoNumber.objects.create(
            type='SalesOrder',
            system_generated=True,
            last_nbr=1
        )
        jb.AdditionalCharge.objects.create(
            additional_chargekey=1,
            additional_charge=1,
            description=None,
            est_price=10,
            job_revenue=False,
            commissionable=False,
            processed=False,
            taxable=False,
            note_text=10,
            last_updated=make_aware(datetime.datetime.utcnow()),
            approved=False,
            recurring=False,
            commissionincluded=False
        )
        jb.AutoNumber.objects.create(
            type='Job',
            system_generated=True,
            last_nbr=1
        )

        jb_order_exporter.erp_config.should_email_when_job_created = True
        jb_order_exporter._process_order(get_order(28))
        assert "Sending job created email. Job number: " in caplog.text

    def test_default_vendor(self, jb_order_exporter):
        c = Vendor.objects.count()
        v = get_default_vendor()
        assert DEFAULT_VENDOR_NAME, v.vendor
        assert c + 1 == Vendor.objects.count()
        v = get_default_vendor()
        assert DEFAULT_VENDOR_NAME, v.vendor
        assert c + 1 == Vendor.objects.count()

    def test_get_vendor_from_op_variable(self, jb_order_exporter):
        order: Order = get_order(28)
        op = order.order_items[0].root_component.shop_operations[0]
        vendor_name, vendor_instance = JobOperationProcessor.get_jb_vendor_from_op_variable(
            "Workcenter Default Op", op, "PAPERLESS"
        )
        assert vendor_name == "test"
        assert vendor_instance == Vendor.objects.filter(vendor="PAPERLESS").first()

    def test_outside_service(self, jb_order_exporter):
        import jobboss.models as jb
        jb.AutoNumber.objects.create(
            type='SalesOrder',
            system_generated=True,
            last_nbr=1
        )
        jb.AdditionalCharge.objects.create(
            additional_chargekey=1,
            additional_charge=1,
            description=None,
            est_price=10,
            job_revenue=False,
            commissionable=False,
            processed=False,
            taxable=False,
            note_text=10,
            last_updated=make_aware(datetime.datetime.utcnow()),
            approved=False,
            recurring=False,
            commissionincluded=False
        )
        jb.AutoNumber.objects.create(
            type='Job',
            system_generated=True,
            last_nbr=1
        )
        jb_order_exporter._process_order(get_order(28))
        assert jb.JobOperation.objects.filter(inside_oper=False).first()

    def test_get_material(self, jb_order_exporter):
        Material.objects.create(
            material='123',
            rev='A',
            location_id='',
            type='F',
            status='Active',
            pick_buy_indicator='P',
            stocked_uofm='ea',
            purchase_uofm='ea',
            cost_uofm='ea',
            price_uofm='ea',
            standard_cost=0,
            reorder_qty=0,
            lead_days=0,
            uofm_conv_factor=1,
            lot_trace=False,
            rd_whole_unit=False,
            make_buy='M',
            use_price_breaks=True,
            last_updated=make_aware(datetime.datetime.utcnow()),
            taxable=False,
            affects_schedule=True,
            tooling=False,
            isserialized=False,
            objectid=uuid.uuid4()
        )
        assert get_material('123') is not None
        assert get_material('123 ') is not None
        assert get_material('456') is None

    def test_get_jobboss_work_center_instance(self, jb_order_exporter):
        pp_to_job_op_mapping = {}
        assert JobOperationProcessor.get_jobboss_work_center_instance(pp_to_job_op_mapping, "test", "test") is None

        jb_order_exporter.erp_config.default_work_center_name = "test"
        WorkCenter.objects.create(work_center="test", type="test", link_material=True, link_component=True, is_parent=True, has_parent=False, last_updated=make_aware(datetime.datetime.utcnow()))
        operation_object = JobOperationProcessor(jb_order_exporter)
        assert operation_object.get_default_jobboss_work_center() is not None

    def test_get_jb_service_name_from_op_variable(self, jb_order_exporter):
        order = get_order(28)
        op = order.order_items[0].root_component.shop_operations[0]
        jb_order_exporter.erp_config.service_variable = "SERVICE_VARIABLE"
        service_name = JobOperationProcessor.get_jb_service_name_from_op_variable(
            jb_order_exporter.erp_config.service_variable, op)
        assert service_name is None


@pytest.mark.django_db
class TestAssembly:

    def test_assembly(self, jb_order_exporter):
        from jobboss.exporter.processors.job import JobProcessor
        from collections import namedtuple
        SuffixPosition = namedtuple("suffix_position", "level level_index level_count parent_job")
        Job = namedtuple("job", "job")
        job = Job("12345")

        job_processor = JobProcessor(jb_order_exporter)

        root_comp_position = SuffixPosition(0, 0, 1, None)
        character = JobProcessor.generate_custom_job_number(job_processor, "-", "", root_comp_position)
        assert character == root_comp_position

        second = SuffixPosition(2, 1, 3, job)
        character = JobProcessor.generate_custom_job_number(job_processor, "", "prefix", second)
        assert character == "prefix12345B"

        third = SuffixPosition(3, 2, 3, job)
        character = JobProcessor.generate_custom_job_number(job_processor, "-", "", third)
        assert character == "123453"

        big_assembly1 = SuffixPosition(24, 25, 35, job)
        character = JobProcessor.generate_custom_job_number(job_processor, "-", "", big_assembly1)
        assert character == "12345Z"

        big_assembly2 = SuffixPosition(24, 27, 35, job)
        character = JobProcessor.generate_custom_job_number(job_processor, "-", "", big_assembly2)
        assert character == "12345AB"

        second = SuffixPosition(2, 1, 3, job)
        character = JobProcessor.generate_custom_job_number(job_processor, "-", "RD", second)
        assert character == "RD12345B"

    def test_solo_mfg_comp_assembly(self, jb_order_exporter):
        import jobboss.models as jb
        jb.AutoNumber.objects.create(
            type='SalesOrder',
            system_generated=True,
            last_nbr=1
        )
        jb.AdditionalCharge.objects.create(
            additional_chargekey=1,
            additional_charge=1,
            description=None,
            est_price=10,
            job_revenue=False,
            commissionable=False,
            processed=False,
            taxable=False,
            note_text=10,
            last_updated=make_aware(datetime.datetime.utcnow()),
            approved=False,
            recurring=False,
            commissionincluded=False
        )
        jb.AutoNumber.objects.create(
            type='Job',
            system_generated=True,
            last_nbr=1
        )
        jb_order_exporter.erp_config.solo_mfg_comp_assembly = True
        jb_order_exporter._process_order(get_order(27))
        assert jb.Job.objects.count() == 1

    def export_order_with_duplicate_components(self, jb_order_exporter):
        import jobboss.models as jb
        jb.AutoNumber.objects.create(
            type='SalesOrder',
            system_generated=True,
            last_nbr=1
        )
        jb.AutoNumber.objects.create(
            type='Job',
            system_generated=True,
            last_nbr=1
        ),
        jb.AdditionalCharge.objects.create(
            additional_chargekey=1,
            additional_charge=1,
            description=None,
            est_price=10,
            job_revenue=False,
            commissionable=False,
            processed=False,
            taxable=False,
            note_text=10,
            last_updated=make_aware(datetime.datetime.utcnow()),
            approved=False,
            recurring=False,
            commissionincluded=False
        )
        order = get_order(178)
        jb_order_exporter._process_order(order)
        jb_order_exporter.erp_config.should_export_assemblies_with_duplicate_components = True
        return order

    def test_assembly_with_duplicates_does_not_export_duplicates(self, jb_order_exporter):
        import jobboss.models as jb
        jb_order_exporter.erp_config.should_export_assemblies_with_duplicate_components = False
        order = self.export_order_with_duplicate_components(jb_order_exporter)
        expected_job_count = len([comp for comp in order.order_items[0].components if not comp.is_hardware])
        assert jb.Job.objects.count() == expected_job_count

    def test_assembly_with_duplicates_exports_duplicates_if_config_set(self, jb_order_exporter):
        import jobboss.models as jb
        jb_order_exporter.erp_config.should_export_assemblies_with_duplicate_components = True
        order = self.export_order_with_duplicate_components(jb_order_exporter)
        expected_job_count = sum(1 for assm_comp in order.order_items[0].iterate_assembly_with_duplicates() if assm_comp.component.type != 'purchased')
        assert jb.Job.objects.count() == expected_job_count


@pytest.mark.django_db
class TestConnector:

    def test_connector(self, jb_order_exporter):
        import jobboss.models as jb
        jb.AutoNumber.objects.create(
            type='SalesOrder',
            system_generated=True,
            last_nbr=1
        )
        jb.AutoNumber.objects.create(
            type='Job',
            system_generated=True,
            last_nbr=1
        ),
        jb.AdditionalCharge.objects.create(
            additional_chargekey=1,
            additional_charge=1,
            description=None,
            est_price=10,
            job_revenue=False,
            commissionable=False,
            processed=False,
            taxable=False,
            note_text=10,
            last_updated=make_aware(datetime.datetime.utcnow()),
            approved=False,
            recurring=False,
            commissionincluded=False
        )
        order = get_order(9)
        jb_order_exporter._process_order(order)
        parent_jobs = jb.Job.objects.filter(top_lvl_job__exact='')
        assert len(order.order_items) == parent_jobs.count()
        component_count = 0
        for oi in order.order_items:
            component_count += len([comp for comp in oi.components if not comp.is_hardware])
        assert component_count == jb.Job.objects.count()
        op_count = 0
        addon_count = 0
        for oi in order.order_items:
            addon_count += len(oi.ordered_add_ons)
            for comp in oi.components:
                op_count += len(comp.shop_operations)
        assert addon_count + 1 == jb.AdditionalCharge.objects.count()  # additional charge was seeded
        assert op_count == jb.JobOperation.objects.count()

    def test_generate_finished_good(self, jb_order_exporter):
        import jobboss.models as jb
        jb.AutoNumber.objects.create(
            type='SalesOrder',
            system_generated=True,
            last_nbr=1
        )
        jb.AutoNumber.objects.create(
            type='Job',
            system_generated=True,
            last_nbr=1
        ),
        jb.AdditionalCharge.objects.create(
            additional_chargekey=1,
            additional_charge=1,
            description=None,
            est_price=10,
            job_revenue=False,
            commissionable=False,
            processed=False,
            taxable=False,
            note_text=10,
            last_updated=make_aware(datetime.datetime.utcnow()),
            approved=False,
            recurring=False,
            commissionincluded=False
        )
        order = get_order(25)
        jb_order_exporter.erp_config.generate_finished_good_material = True
        jb_order_exporter._process_order(order)
        assert jb.Material.objects.filter(type="F").first() is not None

    def test_routing(self, jb_order_exporter):
        inside_name = 'Test Paperless Op'
        outside_name = 'Anodizing'
        OP_MAP[inside_name] = [['WC1', 'OP1']]
        FINISH_MAP[outside_name] = [['VENDOR1', 'SERVICE1']]
        lines = list(generate_routing_lines('No op'))
        assert len(lines) == 1
        line: RoutingLine = lines[0]
        assert line.is_inside is True
        assert line.wc == "No op"
        assert is_inside_op('No op') is False
        assert is_outside_op('No op') is False
        lines = list(generate_routing_lines(inside_name))
        assert 1 == len(lines)
        line: RoutingLine = lines[0]
        assert line.is_inside is True
        assert line.notes is not None
        assert line.wc == "WC1"
        assert is_inside_op(inside_name) is True
        assert is_outside_op(inside_name) is False
        lines = list(generate_routing_lines(outside_name))
        line: RoutingLine = lines[0]
        assert line.is_inside is False
        assert 'VENDOR1' == line.vendor
        assert line.has_work_center is False
        assert line.vendor_instance is not None
        assert is_inside_op(outside_name) is False
        assert is_outside_op(outside_name) is True
        OP_MAP[inside_name] = []
        lines = list(generate_routing_lines(inside_name))
        assert 0 == len(lines)
        OP_MAP.pop(inside_name)
        FINISH_MAP.pop(outside_name)


@pytest.mark.django_db
class TestJobOperation:
    def test_get_operation_total_hours(self, jb_order_exporter):
        order = get_order(53)
        order_item1 = order.order_items[0]
        component1 = order_item1.root_component
        runtime = 1
        setup_time = 1
        total_operation_hours = JobOperationProcessor(jb_order_exporter).get_operation_total_hours(component1, setup_time, runtime)
        assert total_operation_hours == 2

    def test_get_template_job_operation_total_hours(self, jb_order_exporter):
        import jobboss.models as jb
        # Process a job to associate the dummy job op to
        order = get_order(53)
        jb.AutoNumber.objects.create(
            type='Job',
            system_generated=True,
            last_nbr=1
        )
        jb.AutoNumber.objects.create(
            type='SalesOrder',
            system_generated=True,
            last_nbr=1
        )
        jb_order_exporter._process_order(order)
        job_op = JobOperation.objects.create(
            job=jb.Job.objects.last(),
            wc_vendor="WORK CENTER",
            inside_oper=True,
            est_run_per_part=1,
            run_method="FixedHrs",
            est_setup_hrs=1,
            sequence=1,
            est_unit_cost=100.00,
            deferred_qty=1,
            act_unit_cost=100.00,
            schedule_exception_old=False,
            minimum_chg_amt=0,
            cost_unit_conv=0,
            currency_conv_rate=1,
            fixed_rate=True,
            last_updated=make_aware(datetime.datetime.utcnow()),
            objectid=uuid.uuid4(),
            manual_start_lock=False,
            manual_stop_lock=False,
            priority_zero_lock=False,
            firm_zone_lock=False
        )
        order_item1 = order.order_items[0]
        component1 = order_item1.root_component
        total_operation_hours = JobOperationProcessor(jb_order_exporter).get_template_job_operation_total_hours(component1, job_op)
        assert total_operation_hours == 2
        job_op.run_method = "Parts/Hr"
        job_op.est_run_per_part = 5
        total_operation_hours = JobOperationProcessor(jb_order_exporter).get_template_job_operation_total_hours(component1, job_op)
        assert total_operation_hours == 6

    def test_should_ignore_op(self):
        pp_to_job_op_mapping = {
            "Paperless Operation Name": ["JB Work Center", "Optional Operation"],
            "Part Level": ["IGNORE", ""]
        }
        op_def_name = "Paperless Operation Name"
        should_ignore = JobOperationProcessor.should_ignore_op(pp_to_job_op_mapping, op_def_name)
        assert should_ignore is False
        op_def_name = "This Name Doesn't Exist"
        should_ignore = JobOperationProcessor.should_ignore_op(pp_to_job_op_mapping, op_def_name)
        assert should_ignore is False
        op_def_name = "Part Level"
        should_ignore = JobOperationProcessor.should_ignore_op(pp_to_job_op_mapping, op_def_name)
        assert should_ignore is True


@pytest.mark.django_db
class TestSalesOrder:
    def test_get_estimator_name(self):
        import jobboss.models as jb
        from jobboss.exporter.processors.so_header import SoHeaderProcessor
        from collections import namedtuple

        tuple_fields = namedtuple('estimator', ['first_name', 'last_name', 'email'])
        good_estimator = tuple_fields("Good", "Will", "goodwill@hunting.com")
        bad_estimator = tuple_fields("Good", "Will", "abc123@email.com")

        jb.Employee.objects.create(
            employee="GWHUNT",
            type="Other",
            status="Active",
            class_field="E",
            last_updated=make_aware(datetime.datetime.utcnow()),
            tran_repeater=False,
            objectid=uuid.uuid4()
        )

        jb.Employee.objects.create(
            employee="STEVE",
            type="Other",
            status="Active",
            class_field="E",
            last_updated=make_aware(datetime.datetime.utcnow()),
            tran_repeater=False,
            objectid=uuid.uuid4()
        )

        pp_to_jb_estimator_mapping = {"goodwill@hunting.com": "GWHUNT"}
        name = SoHeaderProcessor.get_estimator_name("STEVE", good_estimator, pp_to_jb_estimator_mapping)
        assert name == "GWHUNT"
        name = SoHeaderProcessor.get_estimator_name("STEVE", bad_estimator, pp_to_jb_estimator_mapping)
        assert name == "STEVE"

    def test_sales_order_inactive(self, jb_order_exporter, caplog):
        import jobboss.models as jb
        jb.AutoNumber.objects.create(
            type='SalesOrder',
            system_generated=True,
            last_nbr=1
        )
        jb.AutoNumber.objects.create(
            type='Job',
            system_generated=True,
            last_nbr=1
        ),
        jb.AdditionalCharge.objects.create(
            additional_chargekey=1,
            additional_charge=1,
            description=None,
            est_price=10,
            job_revenue=False,
            commissionable=False,
            processed=False,
            taxable=False,
            note_text=10,
            last_updated=make_aware(datetime.datetime.utcnow()),
            approved=False,
            recurring=False,
            commissionincluded=False
        )
        order = get_order(29)
        jb_order_exporter.erp_config.sales_orders_active = False
        jb_order_exporter._process_order(order)
        assert "Sales Orders are disabled." in caplog.text


@pytest.mark.django_db
class TestMaterialMaster:
    def test_generate_default_material(self, jb_order_exporter):
        import jobboss.models as jb

        jb.AutoNumber.objects.create(
            type='SalesOrder',
            system_generated=True,
            last_nbr=1
        )
        jb.AutoNumber.objects.create(
            type='Job',
            system_generated=True,
            last_nbr=1
        ),
        jb.Material.objects.create(
            material="PPARTS_DEFAULT",
            description="Default material",
            drawing=None,
            ext_description="The best test jest crest lest fest",
            sales_code=None,
            rev="A",
            location_id="SHOP",
            type="M",
            status='Active',
            pick_buy_indicator="B",
            stocked_uofm='ea',
            purchase_uofm='ea',
            cost_uofm='ea',
            price_uofm='ea',
            selling_price=100,
            standard_cost=100,
            last_cost=90,
            average_cost=95,
            on_order_qty=0,
            order_point=0,
            reorder_qty=0,
            lead_days=0,
            uofm_conv_factor=1,
            lot_trace=False,
            rd_whole_unit=1,
            price_unit_conv=1,
            make_buy='M',
            use_price_breaks=True,
            last_updated=make_aware(datetime.datetime.utcnow()),
            taxable=False,
            affects_schedule=0,
            tooling=False,
            isserialized=False,
            maxusage=0,
            shelflife=0,
            objectid=uuid.uuid4()
        )

        assert len(jb.Material.objects.all()) == 1
        order = get_order(29)
        jb_order_exporter.erp_config.default_raw_material = "PPARTS_DEFAULT"
        jb_order_exporter.erp_config.generate_material_ops = True
        jb_order_exporter.erp_config.should_create_new_hardware_materials = True
        jb_order_exporter._process_order(order)
        hardware_count = 0
        for oi in order.order_items:
            for comp in oi.components:
                if comp.is_hardware:
                    hardware_count += 1
        assert hardware_count == 2
        assert len(jb.Material.objects.all()) == 3


@pytest.mark.django_db
class TestMaterialReq:
    def test_mat_ops_generated(self, jb_order_exporter):
        import jobboss.models as jb

        jb.AutoNumber.objects.create(
            type='SalesOrder',
            system_generated=True,
            last_nbr=1
        )
        jb.AutoNumber.objects.create(
            type='Job',
            system_generated=True,
            last_nbr=1
        )

        order = get_order(29)
        jb_order_exporter._process_order(order)
        mat_op_count = 0
        hardware_count = 0
        for oi in order.order_items:
            for comp in oi.components:
                if comp.material_operations:
                    mat_op_count += len(comp.material_operations)
                if comp.is_hardware:
                    hardware_count += 1
        assert len(jb.MaterialReq.objects.all()) - hardware_count == mat_op_count

    def test_get_quantity_per(self, jb_order_exporter):
        import jobboss.models as jb
        jb.AutoNumber.objects.create(
            type='SalesOrder',
            system_generated=True,
            last_nbr=1
        )
        jb.AutoNumber.objects.create(
            type='Job',
            system_generated=True,
            last_nbr=1
        )
        from jobboss.exporter.processors.material_req import MaterialReqProcessor
        order = get_order(29)
        jb_order_exporter._process_order(order)
        mat_type = "H"
        for oi in order.order_items:
            for comp in oi.components:
                qty_per = MaterialReqProcessor.get_quantity_per(oi, comp, mat_type)
                assert qty_per == comp.innate_quantity

    def test_get_material_name(self, jb_order_exporter):
        import jobboss.models as jb
        jb.AutoNumber.objects.create(
            type='SalesOrder',
            system_generated=True,
            last_nbr=1
        )
        jb.AutoNumber.objects.create(
            type='Job',
            system_generated=True,
            last_nbr=1
        )
        from jobboss.exporter.processors.material_req import MaterialReqProcessor
        order = get_order(29)
        jb_order_exporter._process_order(order)
        mat_obj = MaterialReqProcessor(jb_order_exporter)
        jb_order_exporter.erp_config.should_create_new_hardware_materials = True
        for oi in order.order_items:
            for comp in oi.components:
                mat_type = "H"
                name = mat_obj.get_material_name(comp, mat_type)
                if comp.part_number and jb_order_exporter.erp_config.should_create_new_hardware_materials is True:
                    assert name == comp.part_number[:30]
                mat_type = "R"
                name = mat_obj.get_material_name(comp, mat_type)
                if comp.material and jb_order_exporter.erp_config.should_create_new_hardware_materials is True:
                    assert name == comp.material.name.upper()[0:30]

    def test_get_mat_name_from_op_variable(self, jb_order_exporter):
        import jobboss.models as jb
        jb.AutoNumber.objects.create(
            type='SalesOrder',
            system_generated=True,
            last_nbr=1
        )
        jb.AutoNumber.objects.create(
            type='Job',
            system_generated=True,
            last_nbr=1
        )
        jb.Material.objects.create(
            material="TEST MATERIAL",
            description="Testing materials",
            drawing=None,
            ext_description="The best test jest crest lest fest",
            sales_code=None,
            rev="A",
            location_id="SHOP",
            type="M",
            status='Active',
            pick_buy_indicator="B",
            stocked_uofm='ea',
            purchase_uofm='ea',
            cost_uofm='ea',
            price_uofm='ea',
            selling_price=100,
            standard_cost=100,
            last_cost=90,
            average_cost=95,
            on_order_qty=0,
            order_point=0,
            reorder_qty=0,
            lead_days=0,
            uofm_conv_factor=1,
            lot_trace=False,
            rd_whole_unit=1,
            price_unit_conv=1,
            make_buy='M',
            use_price_breaks=True,
            last_updated=make_aware(datetime.datetime.utcnow()),
            taxable=False,
            affects_schedule=0,
            tooling=False,
            isserialized=False,
            maxusage=0,
            shelflife=0,
            objectid=uuid.uuid4()
        )
        order = get_order(32)  # Order 32 has material operations.
        jb_order_exporter._process_order(order)
        from jobboss.exporter.processors.material_req import MaterialReqProcessor
        mat_obj = MaterialReqProcessor(jb_order_exporter)

        mat_ops = []
        for oi in order.order_items:
            for comp in oi.components:
                for mat_op in comp.material_operations:
                    mat_ops.append(mat_op)

        jb_order_exporter.erp_config.use_default_materials = True
        default_mat_name = "default name"
        material_op_variable = "JB Material ID"
        mat_name = mat_obj.get_mat_name_from_op_variable(mat_ops[0], material_op_variable, default_mat_name)
        assert mat_name == "TEST MATERIAL"
        mat_name = mat_obj.get_mat_name_from_op_variable(mat_ops[1], material_op_variable, default_mat_name)
        assert mat_name == "default name"
        jb_order_exporter.erp_config.use_default_materials = False
        material_op_variable = "this variable doesn't exist"
        mat_name = mat_obj.get_mat_name_from_op_variable(mat_ops[1], material_op_variable, default_mat_name)
        assert mat_name == "No Name Specified"

    def test_get_op_variable_value_or_zero(self, jb_order_exporter):
        import jobboss.models as jb
        jb.AutoNumber.objects.create(
            type='SalesOrder',
            system_generated=True,
            last_nbr=1
        )
        jb.AutoNumber.objects.create(
            type='Job',
            system_generated=True,
            last_nbr=1
        )
        jb.Material.objects.create(
            material="TEST MATERIAL",
            description="Testing materials",
            drawing=None,
            ext_description="The best test jest crest lest fest",
            sales_code=None,
            rev="A",
            location_id="SHOP",
            type="M",
            status='Active',
            pick_buy_indicator="B",
            stocked_uofm='ea',
            purchase_uofm='ea',
            cost_uofm='ea',
            price_uofm='ea',
            selling_price=100,
            standard_cost=100,
            last_cost=90,
            average_cost=95,
            on_order_qty=0,
            order_point=0,
            reorder_qty=0,
            lead_days=0,
            uofm_conv_factor=1,
            lot_trace=False,
            rd_whole_unit=1,
            price_unit_conv=1,
            make_buy='M',
            use_price_breaks=True,
            last_updated=make_aware(datetime.datetime.utcnow()),
            taxable=False,
            affects_schedule=0,
            tooling=False,
            isserialized=False,
            maxusage=0,
            shelflife=0,
            objectid=uuid.uuid4()
        )
        order = get_order(32)  # Order 32 has material operations.
        jb_order_exporter._process_order(order)
        from jobboss.exporter.processors.material_req import MaterialReqProcessor
        mat_obj = MaterialReqProcessor(jb_order_exporter)

        mat_ops = []
        for oi in order.order_items:
            for comp in oi.components:
                for mat_op in comp.material_operations:
                    mat_ops.append(mat_op)

        variable_value = mat_obj.get_op_variable_value_or_zero(mat_ops[0], "JB Material ID")
        assert variable_value == "TEST MATERIAL"
        variable_value = mat_obj.get_op_variable_value_or_zero(mat_ops[0], "doesn't exist")
        assert variable_value == 0

    def test_should_generate_buy_item(self):
        import jobboss.models as jb
        jb.AutoNumber.objects.create(
            type='SalesOrder',
            system_generated=True,
            last_nbr=1
        )
        jb.AutoNumber.objects.create(
            type='Job',
            system_generated=True,
            last_nbr=1
        )
        jb.Material.objects.create(
            material="TEST MATERIAL",
            description="Testing materials",
            drawing=None,
            ext_description="The best test jest crest lest fest",
            sales_code=None,
            rev="A",
            location_id="SHOP",
            type="M",
            status='Active',
            pick_buy_indicator="B",
            stocked_uofm='ea',
            purchase_uofm='ea',
            cost_uofm='ea',
            price_uofm='ea',
            selling_price=100,
            standard_cost=100,
            last_cost=90,
            average_cost=95,
            on_order_qty=0,
            order_point=0,
            reorder_qty=0,
            lead_days=0,
            uofm_conv_factor=1,
            lot_trace=False,
            rd_whole_unit=1,
            price_unit_conv=1,
            make_buy='M',
            use_price_breaks=True,
            last_updated=make_aware(datetime.datetime.utcnow()),
            taxable=False,
            affects_schedule=0,
            tooling=False,
            isserialized=False,
            maxusage=0,
            shelflife=0,
            objectid=uuid.uuid4()
        )
        from jobboss.exporter.processors.material_req import MaterialReqProcessor
        should_generate_buy_item = MaterialReqProcessor.should_generate_buy_item("TEST MATERIAL")
        assert should_generate_buy_item is False
        should_generate_buy_item = MaterialReqProcessor.should_generate_buy_item("Schmeebly")
        assert should_generate_buy_item is True

    def test_get_comp_type(self, jb_order_exporter):
        import jobboss.models as jb
        jb.AutoNumber.objects.create(
            type='SalesOrder',
            system_generated=True,
            last_nbr=1
        )
        jb.AutoNumber.objects.create(
            type='Job',
            system_generated=True,
            last_nbr=1
        )
        from jobboss.exporter.processors.material_req import MaterialReqProcessor
        order = get_order(29)
        jb_order_exporter._process_order(order)
        for oi in order.order_items:
            for comp in oi.components:
                type = MaterialReqProcessor.get_comp_type(comp)
                if comp.is_hardware:
                    assert type == "H"
                else:
                    assert type == "R"


@pytest.mark.django_db
class TestQuoteExporter:

    def test_quote_exporter(self, jb_order_exporter):
        AutoNumber.objects.create(type="Quote", last_nbr=1, system_generated=False)
        quote_exporter = JobBossQuoteExporter(jb_order_exporter._integration)
        quote_exporter._process_quote(get_quote(13))
        assert Rfq.objects.count() == 1
        assert Quote.objects.count() == 2
        assert QuoteQty.objects.count() == 3


@pytest.mark.django_db
class TestWorkCenterImporter:

    def test_work_center_importer(self, jb_order_exporter, caplog):
        import random
        wc_name = "test" + str(random.randint(1, 100))
        WorkCenter.objects.create(work_center=wc_name, type="test", link_material=True, link_component=True, is_parent=True, has_parent=False, last_updated=make_aware(datetime.datetime.utcnow()))
        jb_wc_importer = JobBossWorkCenterImporter(jb_order_exporter._integration)
        jb_wc_importer.run(wc_name)
        assert f"Processed {wc_name} successfully" in caplog.text


@pytest.mark.django_db
class TestOutsideServiceImporter:

    def test_outside_service_importer(self, jb_order_exporter, caplog):
        import random
        service_name = "RIPOFF" + str(random.randint(1, 100))
        vendor_name = "BEST_BUY"
        service = Service.objects.create(
            service=service_name,
            user_values=None,
            description="everything broke",
            minimum_chg=100,
            lead_days=10,
            note_text="best birthday ever",
            last_updated=make_aware(datetime.datetime.utcnow())
        )
        vendor = Vendor.objects.create(
            vendor=vendor_name,
            send_1099=False,
            last_updated=make_aware(datetime.datetime.utcnow()),
            send_report_by_email=False
        )
        VendorService.objects.create(
            vendor_servicekey=1,
            vendor_service=1,
            vendor=vendor,
            service=service,
            minimum_chg=123.00,
            currency_conv_rate=1,
            fixed_rate=False,
            lead_days=5,
            last_updated=make_aware(datetime.datetime.utcnow()),
        )
        jb_outside_service_importer = JobBossOutsideServiceImporter(jb_order_exporter._integration)
        jb_outside_service_importer.run(service_name)
        assert f"Processed Service id: {service_name}" in caplog.text
