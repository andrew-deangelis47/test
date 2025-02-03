from typing import Dict, Any

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
            result[key] = self.replaced_type(type(field))
        return result

    def check_custom_header_custom_table_exists(self):
        primary_key = self._primary_key
        table_name = self._custom_table_name
        header_sample: Dict[str, Any] = self.create_paperless_table_header_sample()
        ImportCustomTable.check_custom_header_custom_table_exists(name=table_name,
                                                                  header_dict=header_sample,
                                                                  id_fields=[primary_key])


class WorkCenterCustomTableFormat(CustomTableFormat):
    _custom_table_name = "work_centers"
    _primary_key = "work_center"

    def __init__(self):
        self.work_center = "default"
        self.description = "description"
        self.standard_cost = 0
        self.location = "type"
        self.is_outside_service = 'default'
        self.overhead = 0


class MaterialCustomTableFormat(CustomTableFormat):
    _custom_table_name = 'raw_materials'
    _primary_key = 'raw_material_id'

    def __init__(self):
        self.raw_material_id = 'default'
        self.base_price = '0'
        self.description = 'description'
        self.last_cost = 0
        self.average_cost = 0
        self.last_modified = 'N/A'


class VendorCustomTableFormat(CustomTableFormat):
    _custom_table_name = 'vendors'
    _primary_key = 'vendor_id'

    def __init__(self):
        self.vendor_id = "EXAMPLEID"
        self.name = "Vendor Name"
        self.vendor_class = "Vendor Class"


class OutsideServiceCustomTableFormat(CustomTableFormat):
    _custom_table_name = 'acumatica_outside_services'
    _primary_key = 'osv_id'

    def __init__(self):
        self.osv_id = 'id'  # TODO VendorDetails ID
        self.vendor_id = "vendor_id"
        self.vendor_name = 'vendor_name'
        self.inventory_id = "inventory_id"
        self.description = "description"
