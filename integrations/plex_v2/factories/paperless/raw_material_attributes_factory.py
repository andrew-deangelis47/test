from plex_v2.factories.base import BaseFactory
from plex_v2.objects.raw_material_attribute import RawMaterialAttribute
from typing import List
from plex_v2.objects.part import Part
from plex_v2.objects.part_attribute_data_source import PartAttributeDataSource


ATTRIBUTE_CONFIG_KEY_FIELD = 'field'
ATTRIBUTE_CONFIG_KEY_TYPE = 'type'


class RawMaterialAttributesFactory(BaseFactory):

    def get_raw_material_attributes(self, material: Part) -> List[RawMaterialAttribute]:
        attributes: List[RawMaterialAttribute] = []
        field_and_type: dict
        for field_and_type in self.config.raw_material_part_attributes:
            field = field_and_type[ATTRIBUTE_CONFIG_KEY_FIELD]
            type = field_and_type[ATTRIBUTE_CONFIG_KEY_TYPE]
            value = self._get_value(material, field, type)
            attributes.append(RawMaterialAttribute(field=field, type=type, value=value))

        return attributes

    def _get_value(self, material: Part, field: str, type: str):
        # there are different defaults for str vs numeric types
        default_value = self.config.default_raw_material_numeric_value
        if type == 'str':
            default_value = self.config.default_raw_material_attribute_value

        attribute_data_sources: List[PartAttributeDataSource] = PartAttributeDataSource.get(material.number, material.revision, field)
        if len(attribute_data_sources) == 0:
            return default_value
        return attribute_data_sources[0].Value
