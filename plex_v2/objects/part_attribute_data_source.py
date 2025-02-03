import attr
from attr.validators import instance_of, optional
from plex_v2.objects.base import BaseObject, CreateMixin, SearchMixin, RetrieveDataSourceMixin


@attr.s(kw_only=True)
class PartAttributeDataSource(BaseObject, CreateMixin, RetrieveDataSourceMixin, SearchMixin):
    _resource_name = '17751/execute'

    Value = attr.ib(validator=optional(instance_of(str)))
    Attribute_Key = attr.ib(validator=optional(instance_of(int)))
    Attribute_Type = attr.ib(validator=optional(instance_of(str)))
    Part_Key = attr.ib(validator=optional(instance_of(int)))

    @classmethod
    def get(cls, part_num: str, rev: str, attribute_name: str):
        payload_dict: dict = {
            "Part_No": part_num,
            "Attribute_Name": attribute_name,
            "Revision": rev
        }

        return super().datasource_get(payload_dict)
