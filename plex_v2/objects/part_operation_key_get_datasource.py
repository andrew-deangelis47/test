import attr
from attr.validators import instance_of, optional
from plex_v2.objects.base import BaseObject, CreateMixin, RetrieveDataSourceMixin, SearchMixin


@attr.s(kw_only=True)
class PartOperationKeyGetDatasource(BaseObject, CreateMixin, RetrieveDataSourceMixin, SearchMixin):
    _resource_name = '29200/execute'

    Operation_Key = attr.ib(validator=optional(instance_of(int)))
    Part_Operation_Key = attr.ib(validator=optional(instance_of(int)))

    @classmethod
    def get(cls, op_code: str, part_key: int):
        body = {
            "Operation_Code": op_code,
            "Part_Key": part_key
        }

        return super().datasource_get(body)
