from collections import namedtuple
from datetime import datetime
from typing import List

import attr

from dynamics.exceptions import DynamicsNotFoundException
from dynamics.objects.base import BaseObject, str_type, num_type, bool_type


@attr.s
class Item(BaseObject):

    resource_name = 'Item_Card'

    No = attr.ib(**str_type)
    Description = attr.ib(**str_type)
    Last_DateTime_Modified = attr.ib(**str_type)
    Unit_Cost = attr.ib(**num_type)
    Unit_Price = attr.ib(**num_type)
    Profit_Percent = attr.ib(**num_type)
    Last_Direct_Cost = attr.ib(**num_type)
    Indirect_Cost_Percent = attr.ib(**num_type)
    Inventory = attr.ib(**num_type)
    Vendor_No = attr.ib(**str_type)
    Vendor_Item_No = attr.ib(**str_type)
    Search_Description = attr.ib(**str_type)
    Tax_Group_Code = attr.ib(**str_type)
    Global_Dimension_1_Code = attr.ib(**str_type)
    Global_Dimension_2_Code = attr.ib(**str_type)
    Base_Unit_of_Measure = attr.ib(**str_type)
    Sales_Unit_of_Measure = attr.ib(**str_type)
    Purch_Unit_of_Measure = attr.ib(**str_type)
    Inventory_Posting_Group = attr.ib(**str_type)
    Type = attr.ib(**str_type)
    Lead_Time_Calculation = attr.ib(**str_type)
    Item_Category_Code = attr.ib(**str_type)
    Production_BOM_No = attr.ib(**str_type)
    Routing_No = attr.ib(**str_type)
    Substitutes_Exist = attr.ib(**bool_type)

    @classmethod
    def get_first(cls, filters: dict):
        # truncate item number to 20 characters
        if filters.get('No'):
            filters['No'] = filters['No'][:20]
        return super().get_first(filters)

    @classmethod
    def create(cls, data: dict):
        # truncate item number to 20 characters
        if data.get('No'):
            data['No'] = data['No'][:20]
        return super().create(data)


@attr.s
class ItemVariant(BaseObject):

    resource_name = 'Item_Variants'

    Item_No = attr.ib(**str_type)
    Code = attr.ib(**str_type)
    TS_Raw_Part_Variant_Code = attr.ib(**str_type)
    Description = attr.ib(**str_type)
    TS_Unit_Weight = attr.ib(**num_type)
    TS_Pricing_UOM_Code = attr.ib(**str_type)
    TS_Raw_Part_No = attr.ib(**str_type)


@attr.s
class Routing(BaseObject):

    resource_name = 'Routing'

    No = attr.ib(**str_type)


@attr.s
class RoutingOperation(BaseObject):

    resource_name = 'RoutingRoutingLine'

    Operation_No = attr.ib(**str_type)
    Routing_No = attr.ib(**str_type)
    Type = attr.ib(**str_type)
    No = attr.ib(**str_type)  # machine center
    TS_Operation_Name = attr.ib(**str_type)
    Description = attr.ib(**str_type)
    Setup_Time = attr.ib(**num_type)
    Run_Time = attr.ib(**num_type)


@attr.s
class MachineCenter(BaseObject):

    resource_name = 'Machine_Center_Card'

    No = attr.ib(**str_type)
    Name = attr.ib(**str_type)
    Search_Name = attr.ib(**str_type)
    Work_Center_No = attr.ib(**str_type)
    Capacity = attr.ib(**num_type)
    Efficiency = attr.ib(**num_type)
    Overhead_Rate = attr.ib(**num_type)


@attr.s
class ProcessesAndOperations(BaseObject):
    resource_name = 'Process_Operations'


@attr.s
class ProductionBOM(BaseObject):

    resource_name = 'Production_BOM'

    No = attr.ib(**str_type)
    Unit_of_Measure_Code = attr.ib(**str_type)


@attr.s
class ProductionBOMItem(BaseObject):

    resource_name = 'Production_BOMProdBOMLine'

    Type = attr.ib(**str_type)
    No = attr.ib(**str_type)
    Production_BOM_No = attr.ib(**str_type)
    Description = attr.ib(**str_type)
    Quantity_per = attr.ib(**num_type)
    # TODO: add these
    # Unit_of_Measure_Code: attr.ib(**str_type)


@attr.s
class ProcessMap(BaseObject):

    resource_name = 'Process_Map'

    Item_No = attr.ib(**str_type)
    Routing_No = attr.ib(**str_type)
    Production_BOM_No = attr.ib(**str_type)
    Modifier = attr.ib(**str_type)


@attr.s
class PurchasedComponent(Item):

    @classmethod
    def get_with_filter_strings(cls, filter_strings: List[str]):
        """
        Filter items to only get purchased components.
        """
        filter_strings.append("Item_Category_Code ne ''")
        filter_strings.append("Item_Category_Code ne '999'")
        filter_strings.append("Item_Category_Code ne '9999'")
        filter_strings.append("startswith(Item_Category_Code, '1001') ne true")
        filter_strings.append("startswith(Item_Category_Code, '1002') ne true")
        filter_strings.append("startswith(Item_Category_Code, '3') ne true")
        return super().get_with_filter_strings(filter_strings)


@attr.s
class ItemAttributeValueMapping(BaseObject):
    resource_name = 'Item_Attribute_Value_Mapping'

    No = attr.ib(**str_type)
    Item_Attribute_ID = attr.ib(**num_type)
    Item_Attribute_Value_ID = attr.ib(**num_type)


@attr.s
class ItemAttribute(BaseObject):
    resource_name = 'Item_Attribute'

    ID = attr.ib(**num_type)
    Name = attr.ib(**str_type)


@attr.s
class ItemAttributeValue(BaseObject):
    resource_name = 'Item_Attribute_Value'

    ID = attr.ib(**num_type)
    Value = attr.ib(**str_type)


MaterialAttribute = namedtuple('MaterialAttribute', ['pp_column_name', 'dynamics_name', 'default_value'])


@attr.s
class RawMaterial(Item):
    """
    A raw material is either a "material" or a "coating item".
    """

    @classmethod
    def get_attributes(cls) -> List[MaterialAttribute]:
        raise NotImplementedError

    def get_attribute_values(self):
        attribute_vals = {}
        for (pp_column_name, dynamics_name, default_value) in self.get_attributes():
            value = None
            try:
                # get the ID of the attribute
                attribute_id = ItemAttribute.get_first({
                    'Name': dynamics_name
                }).ID
                # get the ID of attribute value corresponding to the attribute for the item
                attribute_value_id = ItemAttributeValueMapping.get_first({
                    'No': self.No,
                    'Item_Attribute_ID': attribute_id
                }).Item_Attribute_Value_ID
                # get the attribute value from its ID
                value = ItemAttributeValue.get_first({
                    'ID': attribute_value_id
                }).Value
            except DynamicsNotFoundException:
                # if we fail to get the attribute value for an item, use the default
                value = default_value

            attribute_vals[pp_column_name] = value

        return attribute_vals

    @classmethod
    def get_all_modified_after(cls, date: datetime):
        """
        We need to ensure an item is marked as modified if its attributes change.
        """
        items_modified = super().get_all_modified_after(date)
        attrs_modified = ItemAttributeValueMapping.get_all_modified_after(date)
        for attr_map in attrs_modified:
            item_matches = [item for item in items_modified if item.No == attr_map.No]
            if not item_matches:
                try:
                    items_modified.append(cls.get_first({
                        'No': attr_map.No
                    }))
                except DynamicsNotFoundException:
                    # the modified attribute does not apply to this type of raw material
                    pass
        return items_modified


@attr.s
class CoatingItem(RawMaterial):
    @classmethod
    def get_attributes(cls):
        return [
            MaterialAttribute('Mils', 'Mils', 0),
            MaterialAttribute('LBs_per_Mils', 'LBs per Mils', 0),
            MaterialAttribute('Specific_Gravity', 'Specific Gravity', 0),
            MaterialAttribute('Percent_Solids', '% Solids', 0),
            MaterialAttribute('Coverage_per_Gallon', 'Coverage per Gallon', 0),
            MaterialAttribute('Mix_Ratio', 'Mix Ratio', ''),
            MaterialAttribute('Fil_Thickness', 'Fil Thickness', 0),
            MaterialAttribute('Coverage_per_Mil', 'Coverage per Mil', 0),
            MaterialAttribute('Adhesion', 'Adhesion', ''),
            MaterialAttribute('Direct_Impact', 'Direct Impact', 0),
            MaterialAttribute('VOC', 'VOC', 0),
            MaterialAttribute('Minium_DFT', 'Minium DFT', 0)
        ]

    @classmethod
    def get_with_filter_strings(cls, filter_strings: List[str]):
        """
        Filter items to only get raw materials.
        """
        filter_strings.append("("
                              "startswith(Item_Category_Code, '1001') or "
                              "startswith(Item_Category_Code, '1002')"
                              ")")
        return super().get_with_filter_strings(filter_strings)


@attr.s
class Material(RawMaterial):
    @classmethod
    def get_attributes(cls):
        return [
            MaterialAttribute('Length', 'Length', 0),
            MaterialAttribute('Width', 'Width', 0),
            MaterialAttribute('Thickness_Wall', 'Thickness/Wall', 0),
            MaterialAttribute('Pencil_Harness', 'Pencil Harness', 0),
            MaterialAttribute('Diameter', 'Diameter', 0),
            MaterialAttribute('Height_A', 'Height A', 0),
            MaterialAttribute('Height_B', 'Height B', 0),
            MaterialAttribute('Depth', 'Depth', 0)
        ]

    @classmethod
    def get_with_filter_strings(cls, filter_strings: List[str]):
        """
        Filter items to only get materials (excluding coating items).
        """
        filter_strings.append("startswith(Item_Category_Code, '3')")
        return super().get_with_filter_strings(filter_strings)
