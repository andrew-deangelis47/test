import random
from types import SimpleNamespace
import pytest

from baseintegration.integration import Integration
from dynamics.exceptions import DynamicsNotFoundException

from dynamics.objects.item import Material, CoatingItem, ItemAttribute, ItemAttributeValueMapping, ItemAttributeValue
from dynamics.tests.utils import with_mocks, get_object_mocks, DynamicsMock


@pytest.fixture
def setup_integration():
    integration = Integration()
    from dynamics.importer.importer import DynamicsMaterialImporter
    return DynamicsMaterialImporter(integration)


material_num = str(random.randint(1, 100))

material_mocks = get_object_mocks({
    Material: Material(
        No=material_num,
        Description='Test',
        Type='test',
        Unit_Cost=0,
        Unit_Price=0,
        Vendor_No='test',
        Base_Unit_of_Measure='test',
        Search_Description='test',
        Inventory_Posting_Group='test',
        Profit_Percent=0,
        Last_Direct_Cost=0,
        Indirect_Cost_Percent=0,
        Vendor_Item_No='test',
        Lead_Time_Calculation='test',
        Global_Dimension_1_Code='test',
        Global_Dimension_2_Code='test',
        Sales_Unit_of_Measure='test',
        Purch_Unit_of_Measure='test',
        Item_Category_Code='test',
        Inventory=0,
        Production_BOM_No='test',
        Routing_No='test',
        Substitutes_Exist=False,
        Tax_Group_Code='test',
        Last_DateTime_Modified='test'
    ),
    ItemAttribute: SimpleNamespace(
        ID='attribute_id'
    ),
    ItemAttributeValueMapping: SimpleNamespace(
        Item_Attribute_Value_ID='attribute_value_id'
    ),
    ItemAttributeValue: SimpleNamespace(
        Value='attribute_value'
    )
})

coating_item_mocks = get_object_mocks({
    CoatingItem: CoatingItem(
        No=material_num,
        Description='Test',
        Type='test',
        Unit_Cost=0,
        Unit_Price=0,
        Vendor_No='test',
        Base_Unit_of_Measure='test',
        Search_Description='test',
        Inventory_Posting_Group='test',
        Profit_Percent=0,
        Last_Direct_Cost=0,
        Indirect_Cost_Percent=0,
        Vendor_Item_No='test',
        Lead_Time_Calculation='test',
        Global_Dimension_1_Code='test',
        Global_Dimension_2_Code='test',
        Sales_Unit_of_Measure='test',
        Purch_Unit_of_Measure='test',
        Item_Category_Code='test',
        Inventory=0,
        Production_BOM_No='test',
        Routing_No='test',
        Substitutes_Exist=False,
        Tax_Group_Code='test',
        Last_DateTime_Modified='test'
    ),
    ItemAttribute: SimpleNamespace(
        ID='attribute_id'
    ),
    ItemAttributeValueMapping: SimpleNamespace(
        Item_Attribute_Value_ID='attribute_value_id'
    ),
    ItemAttributeValue: SimpleNamespace(
        Value='attribute_value'
    )
})


class TestDynamicsRawMaterialImport:
    def test_import_material(self, setup_integration):
        def run_test(call_data, get_args):
            setup_integration.materials_table_name = 'dynamics_materials'
            setup_integration.coating_items_table_name = 'dynamics_coating_items'
            setup_integration.run(material_id=material_num)
            assert setup_integration._bulk_process_material([material_num])

        with_mocks(run_test, [
            *material_mocks,
            DynamicsMock(CoatingItem, 'get_first', exception=DynamicsNotFoundException(''))
        ])

    def test_import_coating_item(self, setup_integration):
        def run_test(call_data, get_args):
            setup_integration.materials_table_name = 'dynamics_materials'
            setup_integration.coating_items_table_name = 'dynamics_coating_items'
            setup_integration.run(material_id=material_num)
            assert setup_integration._bulk_process_material([material_num])

        with_mocks(run_test, [
            *coating_item_mocks,
            DynamicsMock(Material, 'get_first', exception=DynamicsNotFoundException(''))
        ])
