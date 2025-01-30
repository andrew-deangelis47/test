from pydantic import Field

from plex_v2.objects.custom_table import CustomTableFormat
from typing import Dict, Any
from plex_v2.configuration import PlexConfig
from plex_v2.utils.import_utils import ImportUtils


ATTRIBUTE_CONFIG_KEY_FIELD = 'field'
ATTRIBUTE_CONFIG_KEY_TYPE = 'type'


# pragma: no cover
class RawMaterialCustomTable(CustomTableFormat):
    _custom_table_name = "raw_material_integration_import"  # This is what will appear in paperless, and how the table will be referenced
    _primary_key = "Number_And_Revision"

    # pragma: no cover
    def __init__(self, config: PlexConfig, utils: ImportUtils):
        self.config = config
        self.utils = utils
        # default custom fields
        self.Number: str = Field(alias="Number", default='')
        self.Revision: str = Field(alias="Revision", default='')
        self.Number_And_Revision: str = Field(alias="Number_And_Revision", default='')
        self.Description: str = Field(alias="Description", default='')
        self.Part_Name: str = Field(alias="Part_Name", default='')
        self.Part_Type: str = Field(alias="Part_Type", default='')
        self.Part_Group: str = Field(alias="Part_Group", default='')
        self.Part_Source: str = Field(alias="Part_Source", default='')
        self.Status: str = Field(alias="Status", default='')
        self.Lead_Time_Days: float = Field(alias="Lead_Time_Days", default=0)
        self.Last_Import_Time: str = Field(alias="Last_Import_Time", default='')

        if self.config.should_import_material_pricing:
            self.Price: float = Field(alias='Price', default=0.0)
            self.Price_Unit: str = Field(alias='Price_Unit', default='')

        # part attributes - setting the fields based on whats in the config
        attribute: dict
        for attribute in self.config.raw_material_part_attributes:
            attribute_name = attribute[ATTRIBUTE_CONFIG_KEY_FIELD].replace(" ", "_")
            self.__setattr__(attribute_name, Field(alias=attribute_name))

    # pragma: no cover
    def create_paperless_table_header_sample(self) -> Dict[str, Any]:  # Dict["column_name", "value_type"]
        """
        Assembles header sample without _custom_table_name as a column header.
        """

        # we need to ignore the raw material attributes at first because their type depends on the config
        # otherwise it would just set them all to string
        attribute_field_names = []
        for attribute in self.config.raw_material_part_attributes:
            attribute_field_names.append(attribute['field'].replace(' ', '_'))

        result: dict = {}
        for key, field in self.__dict__.items():
            if key == "_custom_table_name" or key == 'config' or key == 'utils' or key in attribute_field_names:
                continue
            result[key] = self.replaced_type(type(field.default))

        # add in the configured part attributes
        attribute: dict
        for attribute in self.config.raw_material_part_attributes:
            field_name = attribute[ATTRIBUTE_CONFIG_KEY_FIELD].replace(' ', '_')
            result[field_name] = self.replaced_type(eval(attribute[ATTRIBUTE_CONFIG_KEY_TYPE]))

        return result
