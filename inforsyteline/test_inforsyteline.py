import os
import sys

import pendulum
import pytest
from baseintegration.utils.test_utils import get_order, fill_and_save, get_repeat_parts_from_backend
from baseintegration.integration import Integration
from paperless.objects.customers import Account
from paperless.objects.purchased_components import PurchasedComponent
from paperless.objects.orders import Order
import datetime
import random
import uuid
import math

# append to path
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))

from inforsyteline.models import CustomerMst, CustaddrMst, ItemMst, ProdcodeMst, WcMst, JobMst, JobmatlMst, \
    JobrouteMst, CoitemMst, JrtSchMst
from inforsyteline.exporter.processors.customer import CustomerProcessor


@pytest.fixture
def setup_exporter():
    """Create integration to process orders"""
    from inforsyteline.exporter.exporter import InforSytelineOrderExporter
    i = InforSytelineOrderExporter(Integration())
    CustomerMst.objects.create(site_ref="SYTE",
                               cust_num="3",
                               cust_seq=0,
                               noteexistsflag=0,
                               rowpointer="0",
                               createdby="blah",
                               updatedby="blah",
                               createdate=datetime.datetime.now(),
                               inworkflow=0,
                               default_ship_to=0,
                               recorddate=datetime.datetime.now())
    CustaddrMst.objects.create(cust_num="3", cust_seq=0, name="Maine Blueberry Co", rowpointer="1")
    CustomerMst.objects.create(site_ref="SYTE",
                               cust_num="2",
                               cust_seq=0,
                               noteexistsflag=0,
                               rowpointer="2",
                               createdby="blah",
                               updatedby="blah",
                               createdate=datetime.datetime.now(),
                               inworkflow=0,
                               default_ship_to=0,
                               recorddate=datetime.datetime.now())
    CustaddrMst.objects.create(cust_num="2", cust_seq=0, name="Georgia Peach Farming Co")
    return i


@pytest.fixture
def setup_account_importer():
    integration = Integration()
    from inforsyteline.importer.importer import InforSytelineAccountImporter
    i = InforSytelineAccountImporter(integration)
    return i


@pytest.fixture
def setup_purchased_component_importer():
    integration = Integration()
    from inforsyteline.importer.importer import InforSytelinePurchasedComponentImporter
    i = InforSytelinePurchasedComponentImporter(integration)
    return i


@pytest.fixture
def setup_material_importer():
    integration = Integration()
    from inforsyteline.importer.importer import InforSytelineMaterialImporter
    i = InforSytelineMaterialImporter(integration)
    return i


@pytest.fixture
def setup_repeat_work_importer():
    integration = Integration()
    integration.config_yaml["Importers"] = {"repeat_part": {"is_post_enabled": True}}
    from inforsyteline.importer.importer import InforSytelineRepeatPartImporter
    return InforSytelineRepeatPartImporter(integration)


@pytest.mark.django_db
class TestInforSyteline:
    """Runs tests against a dummy database using models.py"""

    def seed_wc(self, exporter, order: Order):
        for o_item in order.order_items:
            for comp in o_item.components:
                for op in comp.shop_operations:
                    op_variable = op.get_variable(exporter.erp_config.pp_work_center_variable)
                    if op_variable is not None:
                        if not WcMst.objects.filter(wc=int(op_variable)).first():
                            WcMst.objects.create(
                                site_ref="SYTE",
                                wc=int(op_variable),
                                description=op.name
                            )

    def test_get_customer(self):
        cust = CustomerMst.objects.create(cust_num="10", cust_seq=0, rowpointer="0")
        cust_addr = CustaddrMst.objects.create(cust_num="10", cust_seq=0, name="Testface Engineering", rowpointer="0")
        assert cust_addr == CustomerProcessor.get_customer_addr(erp_code="10", business_name="Testface Engineering")
        assert cust_addr == CustomerProcessor.get_customer_addr(erp_code="10", business_name="Testface")
        assert cust == CustomerProcessor.get_customer_from_addr(cust_addr)

    def test_create_customer(self, setup_exporter):
        ProdcodeMst.objects.create(product_code="FCS")
        self.seed_wc(setup_exporter, get_order(163))
        setup_exporter._process_order(get_order(163))
        assert CustomerMst.objects.count() == 3

    def test_item_processor(self, setup_exporter):
        ProdcodeMst.objects.create(product_code="FCS")
        self.seed_wc(setup_exporter, get_order(134))
        setup_exporter._process_order(get_order(134))
        assert ItemMst.objects.count() == 1
        item: ItemMst = ItemMst.objects.first()
        assert item.description == "Level 2.STEP"
        assert item.item == "040921"
        assert item.cost_type == "S"
        assert item.cost_method == "S"
        # test we don't create the item twice

    def test_do_not_create_item_twice(self, setup_exporter):
        prod = ProdcodeMst.objects.create(product_code="FCS")
        ItemMst.objects.create(item="040921",
                               description="040921",
                               product_code=prod,
                               cost_type="S",
                               cost_method="S")
        self.seed_wc(setup_exporter, get_order(134))
        setup_exporter._process_order(get_order(134))
        assert ItemMst.objects.count() == 1

    def test_assembly(self, setup_exporter):
        self.seed_wc(setup_exporter, get_order(8))
        setup_exporter._process_order(get_order(8))
        assert JobMst.objects.count() == 6
        assert JobmatlMst.objects.count() == 4
        assert JobmatlMst.objects.first().item == '14Z539-90.step' and JobmatlMst.objects.first().oper_num == 10

    def test_purchased_components(self, setup_exporter):
        CustomerMst.objects.create(cust_num="10", cust_seq=0)
        CustaddrMst.objects.create(cust_num="10", cust_seq=0, name="Testface Engineering")
        ProdcodeMst.objects.create(product_code="FCS")
        ProdcodeMst.objects.create(product_code="HDW")
        self.seed_wc(setup_exporter, get_order(31))
        setup_exporter._process_order(get_order(31))
        pc = ItemMst.objects.filter(item='74-451-R-1   EDGE SEALER').first()
        assert pc.product_code.product_code == "HDW"

    def test_account_importer(self, setup_account_importer):
        customer_name = str(random.randint(1, 10000000)) + " Company"
        CustomerMst.objects.create(site_ref="SYTE",
                                   cust_num="7",
                                   cust_seq=0,
                                   noteexistsflag=0,
                                   rowpointer="0",
                                   createdby="blah",
                                   updatedby="blah",
                                   createdate=datetime.datetime.now(),
                                   inworkflow=0,
                                   default_ship_to=0,
                                   recorddate=datetime.datetime.now())
        CustaddrMst.objects.create(site_ref="SYTE",
                                   cust_num="7",
                                   cust_seq=0,
                                   noteexistsflag=0,
                                   name=customer_name,
                                   addr_1="100 Commercial St",
                                   city="Portland",
                                   state="ME",
                                   zip="04101",
                                   rowpointer="0",
                                   createdby="blah",
                                   updatedby="blah",
                                   createdate=datetime.datetime.now(),
                                   inworkflow=0,
                                   carrier_residential_indicator=0,
                                   recorddate=datetime.datetime.now())
        setup_account_importer.run(account_id="7")
        accounts = Account.filter(erp_code="7")
        account: Account = Account.get(accounts[0].id)
        assert account.name == customer_name

    def test_purchased_component_importer(self, setup_purchased_component_importer):
        partno = str(random.randint(1, 10000000)) + "part"
        part_name = str(random.randint(1, 1000000)) + "name"
        unit_cost = random.randint(1, 10)
        prod = ProdcodeMst.objects.create(product_code="HDW")
        ItemMst.objects.create(
            site_ref="P2METCAM",
            item=partno,
            description=part_name,
            qty_allocjob=0,
            u_m="EA",
            lead_time=0,
            lot_size=1,
            qty_used_ytd=0,
            qty_mfg_ytd=0,
            abc_code="C",
            product_code=prod,
            p_m_t_code="M",
            cost_method="C",
            lst_lot_size=0,
            unit_cost=unit_cost,
            lst_u_cost=0,
            avg_u_cost=0,
            stocked=0,
            matl_type="M",
            low_level=0,
            days_supply=5,
            order_min=1,
            order_mult=1,
            mps_flag=0,
            accept_req=0,
            change_date=datetime.datetime.now(),
            revision=1,
            phantom_flag=0,
            plan_flag=0,
            paper_time=2,
            dock_time=0,
            order_max=0,
            recorddate=datetime.datetime.now(),
            rowpointer=str(uuid.uuid4())[0:36],
            createdby="PAPERLESS",
            updatedby="PAPERLESS",
            createdate=datetime.datetime.now(),

        )
        setup_purchased_component_importer.run(purchased_component_id=partno)
        purchased_components: list = PurchasedComponent.search(partno)
        assert len(purchased_components) > 0
        assert math.isclose(float(purchased_components[0].piece_price), float(unit_cost), abs_tol=0.1)
        assert purchased_components[0].oem_part_number == partno
        assert purchased_components[0].description == part_name
        setup_purchased_component_importer.run(purchased_component_id=partno)
        new_purchased_components: list = PurchasedComponent.search(partno)
        assert len(purchased_components) == len(new_purchased_components)
        assert setup_purchased_component_importer._bulk_process_purchased_component([partno])

    def test_material_importer(self, setup_material_importer, caplog):
        partno = str(random.randint(1, 10000)) + "part"
        part_name = str(random.randint(1, 10000)) + "name"
        unit_cost = random.randint(1, 10)
        prod = ProdcodeMst.objects.create(product_code="HDW")
        ItemMst.objects.create(
            site_ref="P2METCAM",
            item=partno,
            description=part_name,
            qty_allocjob=0,
            u_m="EA",
            lead_time=0,
            lot_size=1,
            qty_used_ytd=0,
            qty_mfg_ytd=0,
            abc_code="C",
            product_code=prod,
            p_m_t_code="M",
            cost_method="C",
            lst_lot_size=0,
            unit_cost=unit_cost,
            lst_u_cost=0,
            avg_u_cost=0,
            stocked=0,
            matl_type="M",
            low_level=0,
            days_supply=5,
            order_min=1,
            order_mult=1,
            mps_flag=0,
            accept_req=0,
            change_date=datetime.datetime.now(),
            revision=1,
            phantom_flag=0,
            plan_flag=0,
            paper_time=2,
            dock_time=0,
            order_max=0,
            recorddate=datetime.datetime.now(),
            rowpointer=str(uuid.uuid4())[0:36],
            createdby="PAPERLESS",
            updatedby="PAPERLESS",
            createdate=datetime.datetime.now(),

        )
        setup_material_importer.check_custom_table_exists()
        setup_material_importer._process_material(partno)
        assert f"Processed material {partno}" in caplog.text
        assert setup_material_importer._bulk_process_material([partno])


@pytest.mark.django_db
class TestRepeatPartImport:

    def test_repeat_part_listener(self, setup_repeat_work_importer, caplog):
        item1 = ItemMst(
            item="part1",
            recorddate=datetime.datetime.now(),
        )
        fill_and_save(item1)

        item2 = ItemMst(
            item="part2",
            recorddate=pendulum.naive(year=1970, month=1, day=2)
        )
        fill_and_save(item2)

        job = JobMst(
            item="part3",
            job="job1",
            recorddate=pendulum.naive(year=1970, month=1, day=2)
        )
        fill_and_save(job)

        job_material = JobmatlMst(
            job="job1",
            recorddate=datetime.datetime.now()
        )
        fill_and_save(job_material)

        new_parts = setup_repeat_work_importer.listener.get_new(
            bulk=False, date_to_search=pendulum.naive(year=1990, month=1, day=2))

        assert set(new_parts) == {"part1", "part3"}

    def test_import_from_item(self, setup_repeat_work_importer, caplog):
        part_number = "syteline_test_part_123"

        # create child part

        child_item: ItemMst = ItemMst(
            rowpointer="2",
            item="child-part",
            revision="1"
        ).fill_and_save()

        JobMst(
            rowpointer="2",
            type='S',
            item=child_item.item,
            job='child-job',
            suffix=1,
            mo_bom_alternate_id='Current',
        ).fill_and_save()

        # create parent part

        item: ItemMst = ItemMst(
            rowpointer="1",
            item=part_number,
            revision="1"
        ).fill_and_save()

        job: JobMst = JobMst(
            rowpointer="1",
            type='S',
            item=item.item,
            job='standard-item-job',
            suffix=1,
            mo_bom_alternate_id='Current'
        ).fill_and_save()

        JobmatlMst(
            rowpointer="1",
            job=job.job,
            suffix=job.suffix,
            item="matl-item"
        ).fill_and_save()

        JobmatlMst(
            rowpointer="2",
            job=job.job,
            suffix=job.suffix,
            item=child_item.item
        ).fill_and_save()

        wc: WcMst = WcMst(
            wc="myworkcenter"
        ).fill_and_save()

        job_operation: JobrouteMst = JobrouteMst(
            job=job.job,
            suffix=job.suffix,
            wc=wc,
            oper_num=1
        ).fill_and_save()

        JrtSchMst(
            job=job_operation.job,
            suffix=job_operation.suffix,
            oper_num=job_operation.oper_num
        ).fill_and_save()

        setup_repeat_work_importer.run(part_number)
        assert "Creating repeat part headers from item ID" in caplog.text
        assert "Creating repeat part methods of manufacture from Infor Syteline item ID:" in caplog.text

        parts = get_repeat_parts_from_backend(part_number)
        assert len(parts) == 1

        part = parts[0]
        headers = part["headers"]
        assert len(headers) == 1
        assert headers[0]["type"] == "template"

        moms = headers[0]["methods_of_manufacture"]
        assert len(moms) == 1
        method_of_manufacture = moms[0]

        materials = method_of_manufacture["required_materials"]
        assert len(materials) == 1

        operations = method_of_manufacture["operations"]
        assert len(operations) == 1

        children = method_of_manufacture["children"]
        assert len(children) == 1

    def test_import_from_estimate(self, setup_repeat_work_importer, caplog):
        part_number = "syteline_test_part_124"

        # create child part

        child_item: ItemMst = ItemMst(
            rowpointer="2",
            item="child-part",
            revision="1"
        ).fill_and_save()

        child_job: JobMst = JobMst(
            rowpointer="2",
            type='E',
            item=child_item.item,
            job='child-job',
            suffix=1,
        ).fill_and_save()

        # create parent part

        item: ItemMst = ItemMst(
            rowpointer="1",
            item=part_number,
            revision="1"
        ).fill_and_save()

        job: JobMst = JobMst(
            rowpointer="1",
            type='E',
            item=item.item,
            job='estimate-job',
            suffix=1,
        ).fill_and_save()

        JobmatlMst(
            rowpointer="1",
            job=job.job,
            suffix=job.suffix,
            item="matl-item"
        ).fill_and_save()

        JobmatlMst(
            rowpointer="2",
            job=job.job,
            suffix=job.suffix,
            item=child_item.item,
            ref_num=child_job.job,
            ref_line_suf=child_job.suffix
        ).fill_and_save()

        wc: WcMst = WcMst(
            wc="myworkcenter"
        ).fill_and_save()

        job_operation: JobrouteMst = JobrouteMst(
            job=job.job,
            suffix=job.suffix,
            wc=wc,
            oper_num=1
        ).fill_and_save()

        JrtSchMst(
            job=job_operation.job,
            suffix=job_operation.suffix,
            oper_num=job_operation.oper_num
        ).fill_and_save()

        CoitemMst(
            ref_type='J',
            ref_num=job.job,
            ref_line_suf=job.suffix,
            item=item,
            price=10
        ).fill_and_save()

        setup_repeat_work_importer.run(part_number)
        assert "Creating repeat part headers from item ID" in caplog.text
        assert "Creating repeat part methods of manufacture from Infor Syteline item ID:" in caplog.text

        parts = get_repeat_parts_from_backend(part_number)
        assert len(parts) == 1

        part = parts[0]
        headers = part["headers"]
        assert len(headers) == 1
        assert headers[0]["type"] == "estimated"

        moms = headers[0]["methods_of_manufacture"]
        assert len(moms) == 1
        method_of_manufacture = moms[0]

        materials = method_of_manufacture["required_materials"]
        assert len(materials) == 1

        operations = method_of_manufacture["operations"]
        assert len(operations) == 1

        children = method_of_manufacture["children"]
        assert len(children) == 1

    def test_import_from_job(self, setup_repeat_work_importer, caplog):
        part_number = "syteline_test_part_125"

        # create child part

        child_item: ItemMst = ItemMst(
            rowpointer="2",
            item="child-part",
            revision="1"
        ).fill_and_save()

        child_job: JobMst = JobMst(
            rowpointer="2",
            type='J',
            item=child_item.item,
            job='child-job',
            suffix=1,
        ).fill_and_save()

        # create parent part

        item: ItemMst = ItemMst(
            rowpointer="1",
            item=part_number,
            revision="1"
        ).fill_and_save()

        job: JobMst = JobMst(
            rowpointer="1",
            type='J',
            item=item.item,
            job='test-job',
            suffix=1,
        ).fill_and_save()

        JobmatlMst(
            rowpointer="1",
            job=job.job,
            suffix=job.suffix,
            item="matl-item"
        ).fill_and_save()

        JobmatlMst(
            rowpointer="2",
            job=job.job,
            suffix=job.suffix,
            item=child_item.item,
            ref_num=child_job.job,
            ref_line_suf=child_job.suffix
        ).fill_and_save()

        wc: WcMst = WcMst(
            wc="myworkcenter"
        ).fill_and_save()

        job_operation: JobrouteMst = JobrouteMst(
            job=job.job,
            suffix=job.suffix,
            wc=wc,
            oper_num=1
        ).fill_and_save()

        JrtSchMst(
            job=job_operation.job,
            suffix=job_operation.suffix,
            oper_num=job_operation.oper_num
        ).fill_and_save()

        setup_repeat_work_importer.run(part_number)
        assert "Creating repeat part headers from item ID" in caplog.text
        assert "Creating repeat part methods of manufacture from Infor Syteline item ID:" in caplog.text

        parts = get_repeat_parts_from_backend(part_number)
        assert len(parts) == 1

        part = parts[0]
        headers = part["headers"]
        assert len(headers) == 2
        assert set([h["type"] for h in headers]) == {"engineered", "executed"}

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
