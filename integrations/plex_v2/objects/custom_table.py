from typing import Dict, Any
from baseintegration.utils.custom_table import ImportCustomTable


class CustomTableFormat(ImportCustomTable):

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
