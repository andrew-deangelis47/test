import attr
from attr.validators import instance_of, optional
from plex_v2.objects.base import BaseObject, CreateMixin, RetrieveDataSourceMixin, SearchMixin


@attr.s(kw_only=True)
class WorkCenterImportDataSource(BaseObject, CreateMixin, RetrieveDataSourceMixin, SearchMixin):
    _resource_name = '790/execute'

    Name = attr.ib(validator=optional(instance_of(str)))
    Direct_Labor_Cost = attr.ib(validator=optional(instance_of(float)))
    Other_Burden_Cost = attr.ib(validator=optional(instance_of(float)))
    Workcenter_Code = attr.ib(validator=optional(instance_of(str)))

    def to_custom_table_row(self):
        return {
            "Workcenter_Code": self.Workcenter_Code,
            "Name": self.Name,
            "Direct_Labor_Cost": self.Direct_Labor_Cost,
            "Other_Burden_Cost": self.Other_Burden_Cost
        }

    @classmethod
    def get(cls, code: str):
        body = {
            "Workcenter_Code": code
        }
        return cls.datasource_get(body)[0]

    @classmethod
    def get_all(cls):
        body = {}
        return cls.datasource_get(body)
