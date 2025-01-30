from typing import Dict, Any

from pydantic.class_validators import validator

from baseintegration.utils.custom_table import ImportCustomTable


class CustomTableFormat:

    _custom_table_name: str  # This is what will appear in paperless, and how the table will be referenced
    _primary_key: str  # This is the attribute alias

    @staticmethod
    def replaced_type(value_type):
        if value_type == str:
            return "str"
        elif value_type == float:
            return 1.0
        elif value_type == int:
            return 0
        elif value_type == bool:
            return True

    def create_paperless_table_header_sample(self, ) -> Dict[str, Any]:  # Dict["column_name", "value_type"]
        """
        Assembles header sample without _custom_table_name as a column header.
        """
        result: dict = {}
        for key, field in self.__dict__.items():
            if key == "_custom_table_name":
                continue
            result[key] = self.replaced_type(field)
        return result

    def check_custom_header_custom_table_exists(self):
        primary_key = self._primary_key
        table_name = self._custom_table_name
        header_sample: Dict[str, Any] = self.create_paperless_table_header_sample()
        ImportCustomTable.check_custom_header_custom_table_exists(name=table_name,
                                                                  header_dict=header_sample,
                                                                  id_fields=[primary_key])


class MaterialCustomTableFormat(CustomTableFormat):

    _custom_table_name = "materials_custom_table"  # This is what will appear in paperless, and how the table will be referenced
    _primary_key = "part_num"  # This is the attribute alias

    def __init__(self):
        self.part_num = "EXAMPLE PART NUMBER"
        self.part_description = "Part description"
        self.class_id = "SHT"
        self.type_code = "P"
        self.non_stock = True
        self.prod_code = "CODE"
        self.ium = "Inv. Unit of Measure"
        self.pum = "Purch. unit of measure"
        self.avg_cost = 0
        self.last_cost = 0

    @validator("part_description")
    def truncate_description_for_paperless_payload(cls, value: str) -> str:
        max_chars = 100
        return value[:max_chars]

    @validator("unit_price")
    def truncate_for_paperless_payload(cls, value: float) -> str:
        str_format = '{:.4f}'
        return str_format.format(value)


class VendorCustomTableFormat(CustomTableFormat):

    _custom_table_name = "vendors_custom_table"  # This is what will appear in paperless, and how the table will be referenced
    _primary_key = "vendor_id"  # This is the attribute alias

    def __init__(self):
        self.vendor_id = "EXAMPLEID"
        self.name = "Vendor name"
        self.vendor_num = 123
        # self.comment = "test_comment"
        self.min_order_value = 0
        self.approved = False
        self.early_buffer = 0
        self.late_buffer = 0


class OperationCustomTableFormat(CustomTableFormat):
    _custom_table_name = "operations_custom_table"
    _primary_key = "operation_code"

    def __init__(self):
        self.operation_code = "EXAMPLEID"
        self.description = "description"
        self.type = "type"
        self.resource_group_id = 'resource_group'
        self.resource_id = 'resource'
        self.subcontract = False
        self.vendor_num = 0


class ResourceGroupCustomTableFormat(CustomTableFormat):
    _custom_table_name = "resource_groups_custom_table"
    _primary_key = "resource_group_id"

    def __init__(self):
        self.resource_group_id = "EXAMPLEID"
        self.description = "description"
        self.operation_code = "EXAMPLEID"
        self.plant = "plant"
        self.prod_burden_rate = 0
        self.prod_labor_rate = 0
        self.setup_burden_rate = 0
        self.setup_labor_rate = 0
        self.quoting_prod_burden_rate = 0
        self.quoting_prod_labor_rate = 0
        self.quoting_setup_burden_rate = 0
        self.quoting_setup_labor_rate = 0


class ResourceCustomTableFormat(CustomTableFormat):
    _custom_table_name = "resources_custom_table"
    _primary_key = "resource_id"

    def __init__(self):
        self.resource_id = "EXAMPLEID"
        self.description = "description"
        self.resource_group_id = "EXAMPLEID"
        self.operation_code = "EXAMPLEID"
        self.prod_burden_rate = 0
        self.prod_labor_rate = 0
        self.setup_burden_rate = 0
        self.setup_labor_rate = 0
        self.quoting_prod_burden_rate = 0
        self.quoting_prod_labor_rate = 0
        self.quoting_setup_burden_rate = 0
        self.quoting_setup_labor_rate = 0


class OperationDetailsCustomTableFormat(CustomTableFormat):
    _custom_table_name = "operation_details_custom_table"
    _primary_key = "operation_details_id"

    def __init__(self):
        self.operation_details_id = "operation_details"
        self.operation_code = "operation_code"
        self.resource_group_id = "resource_group_id"
        self.plant = "plant"
