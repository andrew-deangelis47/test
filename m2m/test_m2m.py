import os
import sys
from typing import List

import pytest
import datetime
import json
from django.utils.timezone import make_aware

# append to path
from m2m.models import Inmastx, Qtmast, Qtitem, Qtdbom, Qtpest, Jomast, Joitem, Jodbom, Inbomm, Inboms

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))

# import models
from baseintegration.integration import Integration
from paperless.objects.orders import OrderComponent, OrderCostingVariable, OrderOperation
from paperless.client import PaperlessClient
from m2m.exporter.processors.standard_bom import StandardBOMFactory
from m2m.utils.address import AddressHelper
import m2m.models as mm


@pytest.fixture
def setup_exporter():
    """Create integration to process orders"""
    integration = Integration()
    from m2m.exporter.exporter import M2MOrderExporter
    i = M2MOrderExporter(integration)
    return i


@pytest.fixture
def setup_importer_account():
    integration = Integration()
    from m2m.importer.importer import M2MAccountImporter
    i = M2MAccountImporter(integration)
    return i


@pytest.fixture
def setup_importer_purchase_components():
    integration = Integration()
    from m2m.importer.importer import M2MPurchasedComponentImporter
    i = M2MPurchasedComponentImporter(integration)
    return i


@pytest.fixture
def setup_importer_materials():
    integration = Integration()
    from m2m.importer.importer import M2MMaterialImporter
    i = M2MMaterialImporter(integration)
    return i


@pytest.fixture
def setup_importer_workcenter():
    from m2m.importer.processors.work_centers import M2MWorkCenterBulkImportProcessor
    M2MWorkCenterBulkImportProcessor.w_table_name = 'M2M_workcenter-test'
    M2MWorkCenterBulkImportProcessor.w_table_name = 'M2M_op_descriptions-test'
    integration = Integration()
    from m2m.importer.importer import M2MWorkCenterImporter
    i = M2MWorkCenterImporter(integration)
    return i


@pytest.fixture
def setup_repeat_work_importer():
    integration = Integration()
    integration.config_yaml["Importers"] = {"repeat_part": {"is_post_enabled": True}}
    from m2m.importer.importer import M2MRepeatPartImporter
    return M2MRepeatPartImporter(integration)


class SeedData:
    @staticmethod
    def seed_company() -> mm.Slcdpmx:
        now = make_aware(datetime.datetime.utcnow())
        mm.Sysequ.objects.create(
            fcclass='CUSTNO',
            fcnumber='123456',
            fnwidth=1,
            fnincremen=1,
            fnbase36di=1,
            fnmaxwidth=1,
            flallowwidthchng=1,
        )
        company = mm.Slcdpmx(
            fcustno='ADV600',
            fcompany='CUSTOMER',
            fcreated=now,
            fcurrency='USD',
            fdbdate=now,
            fdusrdate1=now,
            fllongdist=True,
            ffincharge=False,
            fpaytype='3',
            fsalespn='NEW',
            fsince=now,
            ftype='P',
            fcstatus='G',
            fscmprty=4,
            fdisttype='Email',
            subtype='NONE',
            fledited=False,
            fcngdate=now,
            flpaybycc=False,
        ).fill_and_save()
        addr = mm.Syaddr(
            fllongdist=True,
            fncrmmod=1,
            fcaddrkey='000001',
            fcaddrtype='S',
            fcalias='SLCDPM',
            fcaliaskey=company.fcustno,
            fcfname='JOE',
            fclname='SMITH',
            fccompany='CUSTOMER',
            fccity='BOSTON',
            fccountry='United States',
            fcphone='6175551212',
            fcstate='MA',
            fczip='02114',
            fmstreet='123 VINEYARD BLVD SUITE A',
            createddate=now,
            modifieddate=now,
        )
        addr.save()

        return company


@pytest.mark.django_db
class TestOrderExport:

    def test_get_quantity_for_material(self, setup_exporter):
        cost_var_1 = OrderCostingVariable(label="Unit of Measure", variable_class="basic", value_type="string",
                                          value="ft", row=None, options=None)
        cost_var_2 = OrderCostingVariable(label="Unit Material Qty", variable_class="basic", value_type="string",
                                          value="3.158", row=None, options=None)
        mop = OrderOperation(costing_variables=[cost_var_1, cost_var_2], name='Customer Supplied test Steel', id=2135,
                             category='material', cost=1000.00, is_finish=False, is_outside_service=False,
                             operation_definition_name='Material Operation', notes='', position=1, quantities=[],
                             runtime=30.00, setup_time=2.00, operation_definition_erp_code='test_erp_code')
        bom_factory = StandardBOMFactory(configuration=setup_exporter.m2m_config)
        assert 3.158 == bom_factory.get_quantity_for_material(material_op=mop)
        cost_var_3 = OrderCostingVariable(label="Parts Per Sheet", variable_class="basic", value_type="string",
                                          value="32", row=None, options=None)
        mop_1 = OrderOperation(costing_variables=[cost_var_3], name='Customer Supplied test Steel', id=2135,
                               category='material', cost=1000.00, is_finish=False, is_outside_service=False,
                               operation_definition_name='Material Operation', notes='', position=1, quantities=[],
                               runtime=30.00, setup_time=2.00, operation_definition_erp_code='test_erp_code')
        assert (1 / 32) == bom_factory.get_quantity_for_material(material_op=mop_1)
        cost_var_4 = OrderCostingVariable(label="Unit of Measure", variable_class="basic", value_type="string",
                                          value="ft", row=None, options=None)
        cost_var_5 = OrderCostingVariable(label="QTY - ft", variable_class="basic", value_type="string",
                                          value="3.158", row=None, options=None)
        mop_2 = OrderOperation(costing_variables=[cost_var_4, cost_var_5], name='Customer Supplied test Steel', id=2135,
                               category='material', cost=1000.00, is_finish=False, is_outside_service=False,
                               operation_definition_name='Material Operation', notes='', position=1, quantities=[],
                               runtime=30.00, setup_time=2.00, operation_definition_erp_code='test_erp_code')
        assert 3.158 == bom_factory.get_quantity_for_material(material_op=mop_2)


@pytest.mark.django_db
class TestAccountImport:

    def test_customer_import(self, setup_importer_account):
        company = SeedData.seed_company()
        assert setup_importer_account._process_account(account_id=company.fcustno)


@pytest.mark.django_db
class TestPurchaseComponentImport:

    def test_purchase_component_import(self, setup_importer_purchase_components):
        from m2m.utils.item_master import ItemMasterHelper

        with open(os.path.join(os.path.dirname(__file__), "test-data/order_component.json"), 'r') as f:
            mock_order_component_json = json.load(f)
        mock_order_component = OrderComponent(**mock_order_component_json)
        ItemMasterHelper.check_create_item_for_make(comp=mock_order_component, customer_erp='TEST')

        with open(os.path.join(os.path.dirname(__file__), "test-data/order_component2.json"), 'r') as f:
            mock_order_component_json2 = json.load(f)
        mock_order_component2 = OrderComponent(**mock_order_component_json2)
        ItemMasterHelper.check_create_item_for_make(comp=mock_order_component2, customer_erp='TEST')

        with open(os.path.join(os.path.dirname(__file__), "test-data/order_component3.json"), 'r') as f:
            mock_order_component_json3 = json.load(f)
        mock_order_component3 = OrderComponent(**mock_order_component_json3)
        ItemMasterHelper.check_create_item_for_make(comp=mock_order_component3, customer_erp='TEST')

        assert setup_importer_purchase_components._bulk_process_purchased_component(
            purchased_component_ids=['123456', '123457', 'Subassembly1'])
        assert setup_importer_purchase_components._process_purchased_component(purchased_component_id='123456')


@pytest.mark.django_db
class TestMaterialImport:

    def test_material_import(self, setup_importer_materials):
        from m2m.utils.item_master import ItemMasterHelper

        with open(os.path.join(os.path.dirname(__file__), "test-data/order_component.json"), 'r') as f:
            mock_order_component_json = json.load(f)
        mock_order_component = OrderComponent(**mock_order_component_json)
        ItemMasterHelper.check_create_item_for_make(comp=mock_order_component, customer_erp='TEST')

        with open(os.path.join(os.path.dirname(__file__), "test-data/order_component2.json"), 'r') as f:
            mock_order_component_json2 = json.load(f)
        mock_order_component2 = OrderComponent(**mock_order_component_json2)
        ItemMasterHelper.check_create_item_for_make(comp=mock_order_component2, customer_erp='TEST')

        with open(os.path.join(os.path.dirname(__file__), "test-data/order_component3.json"), 'r') as f:
            mock_order_component_json3 = json.load(f)
        mock_order_component3 = OrderComponent(**mock_order_component_json3)
        ItemMasterHelper.check_create_item_for_make(comp=mock_order_component3, customer_erp='TEST')
        from m2m.importer.processors.materials import M2MMaterialBulkImportProcessor
        M2MMaterialBulkImportProcessor.table_name = 'm2m_test_raw_materials'
        setup_importer_materials.check_custom_table_exists()
        assert setup_importer_materials._bulk_process_material(material_ids=['123456', '123457', 'Subassembly1'])
        assert setup_importer_materials._process_material(material_id='123456')


@pytest.mark.django_db
class TestWorkCenterImport:

    def test_workcenter_import(self, setup_importer_workcenter):
        mm.Inwork(
            fcpro_id=100,
            fcpro_name='OBS',
            fccomments='',
            fdept='12',
            flabcost=15.85,
            flschedule=True,
            fnmax1=1,
            fnstd1=1,
            fovrhdcost=13,
            identity_column=10,
            fac='Default',
            fcstdormax='MAX',
            fnloadcapc=0.21,
            queuehrs=1.65,
        ).fill_and_save()

        op = mm.Inopds(
            fdescnum='1201',
            fcpro_id='100',
            fnstd_prod=0.123,
            fnstd_set=5.123,
            identity_column=5,
            fopmemo='Deburr shakers & glitches during run time.',
            fac='Default'
        )
        op.save()
        setup_importer_workcenter.check_custom_table_exists()
        assert setup_importer_workcenter._process_work_center(work_center_id='100')


@pytest.mark.django_db
class TestAddressUtils:
    def test_create_address(self):
        from paperless.objects.address import AddressInfo
        info = AddressInfo(address1='25 Dartmouth Dr.',
                           address2='unit 32',
                           attention='Bob Bugers',
                           city='Manch Vegas',
                           state='NH',
                           country='USA',
                           postal_code='03102',
                           phone='5043922390',
                           business_name='',
                           facility_name='',
                           phone_ext='')
        company = SeedData.seed_company()
        addr = AddressHelper.create_address(company=company,
                                            addr_type='S',
                                            address_info=info)
        assert addr.fcaddrkey == '000002'

    def test_validate_address_type(self):
        assert AddressHelper.validate_address_type(addr_type='S')
        assert AddressHelper.validate_address_type(addr_type='O')
        assert AddressHelper.validate_address_type(addr_type='B')
        assert AddressHelper.validate_address_type(addr_type='G') is False
        assert AddressHelper.validate_address_type(addr_type=None) is False
        assert AddressHelper.validate_address_type(addr_type='') is False


def make_search_view_request(search_json: dict):
    client: PaperlessClient = PaperlessClient.get_instance()
    url = "/v2/erp_stores/public/historical_work_search_view"
    return client.request(url, method="get", params=search_json)


def get_parts(part_number) -> List[dict]:
    part_search_json = {"part_number": part_number, "search_root_parts_only": True}
    r = make_search_view_request(part_search_json)
    assert r.status_code == 200
    parts: list = r.json()
    return parts


@pytest.mark.django_db
class TestRepeatPartImport:

    def test_import_from_item(self, setup_repeat_work_importer, caplog):
        part_number = "pp_test_part_123"
        part_rev = "1"

        Inmastx(
            fpartno=part_number,
            frev=part_rev
        ).fill_and_save()

        Inbomm(
            fpartno=part_number,
            fcpartrev=part_rev
        ).fill_and_save()

        Inboms(
            fparent=part_number,
            fparentrev=part_rev,
            fcomponent="material",
            fcomprev="12",
            fqty=3
        ).fill_and_save()

        Inmastx(
            fpartno="material",
            frev="12"
        ).fill_and_save()

        setup_repeat_work_importer.run((part_number, part_rev))
        assert "Creating repeat part headers from M2M item ID" in caplog.text
        assert "Creating repeat part methods of manufacture from M2M item ID" in caplog.text

        parts = [p for p in get_parts(part_number) if p["revision"] == part_rev]
        assert len(parts) == 1

        part = parts[0]
        headers = part["headers"]
        assert len(headers) == 1

        moms = headers[0]["methods_of_manufacture"]
        assert len(moms) == 1

        materials = moms[0]["required_materials"]
        assert len(materials) == 1

    def test_import_from_quote(self, setup_repeat_work_importer, caplog):
        part_number = "pp_test_part_123"
        part_rev = "3"

        Inmastx(
            fpartno=part_number,
            frev=part_rev
        ).fill_and_save()

        quote = Qtmast(
            fquoteno="1"
        ).fill_and_save()

        quote_item = Qtitem(
            fquoteno=quote.fquoteno,
            finumber="1",
            fenumber="1",
            fpartno=part_number,
            fpartrev=part_rev,
        ).fill_and_save()

        quote_bom_line = Qtdbom(
            fquoteno=quote_item.fquoteno,
            finumber=quote_item.finumber,
            fbompart=part_number,
            fbomrev=part_rev,
            fbominum="1",
            flevel="0"
        ).fill_and_save()

        Qtdbom(
            fquoteno=quote_bom_line.fquoteno,
            finumber=quote_bom_line.finumber,
            fparinum=quote_bom_line.fbominum,
            fbompart="child-part",
            fbomrev="NS",
            flevel="1"
        ).fill_and_save()

        Qtpest(
            fquoteno=quote_item.fquoteno,
            finumber=quote_item.finumber,
            fenumber=quote_item.fenumber,
            fquantity=5
        ).fill_and_save()

        Qtpest(
            fquoteno=quote_item.fquoteno,
            finumber=quote_item.finumber,
            fenumber=quote_item.fenumber,
            fquantity=10
        ).fill_and_save()

        setup_repeat_work_importer.run((part_number, part_rev))
        assert "Creating repeat part headers from M2M item ID" in caplog.text
        assert "Creating repeat part methods of manufacture from M2M item ID" in caplog.text

        parts = [p for p in get_parts(part_number) if p["revision"] == part_rev]
        assert len(parts) == 1

        part = parts[0]
        headers = part["headers"]
        assert len(headers) == 1

        moms = headers[0]["methods_of_manufacture"]
        assert len(moms) == 2

    def test_import_from_job(self, setup_repeat_work_importer, caplog):
        part_number = "pp_test_part_124"
        part_rev = "0"

        Inmastx(
            fpartno=part_number,
            frev=part_rev
        ).fill_and_save()

        job = Jomast(
            fjobno="1",
            fpartno=part_number,
            fpartrev=part_rev,
            ftype="C",
            fstatus="CLOSED"  # should generate an engineered and executed MoM
        ).fill_and_save()

        Joitem(
            fjobno=job.fjobno,
            fpartno=part_number,
            fpartrev=part_rev,
        ).fill_and_save()

        Jodbom(
            fjobno=job.fjobno
        ).fill_and_save()

        setup_repeat_work_importer.run((part_number, part_rev))
        assert "Creating repeat part headers from M2M item ID" in caplog.text
        assert "Creating repeat part methods of manufacture from M2M item ID" in caplog.text

        parts = [p for p in get_parts(part_number) if p["revision"] == part_rev]
        assert len(parts) == 1

        part = parts[0]
        headers = part["headers"]
        assert len(headers) == 2

        header_1_moms = headers[0]["methods_of_manufacture"]
        assert len(header_1_moms) == 1

        header_2_moms = headers[1]["methods_of_manufacture"]
        assert len(header_2_moms) == 1
