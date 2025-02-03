import attr
from attr.validators import instance_of, optional
from plex_v2.objects.base import BaseObject, CreateMixin, RetrieveDataSourceMixin, SearchMixin


@attr.s(kw_only=True)
class PartGetDataSource(BaseObject, CreateMixin, RetrieveDataSourceMixin, SearchMixin):
    _resource_name = '149/execute'

    Part_No = attr.ib(validator=optional(instance_of(str)))
    Revision = attr.ib(validator=optional(instance_of(str)))
    Grade = attr.ib(validator=optional(instance_of(str)))
    Part_Key = attr.ib(validator=optional(instance_of(int)))
    APQP_Checklist_No = attr.ib(validator=optional(instance_of(int)))
    Grade = attr.ib(validator=optional(instance_of(str)))
    Image = attr.ib(validator=optional(instance_of(str)), default=None)
    Name = attr.ib(validator=optional(instance_of(str)))
    Note = attr.ib(validator=optional(instance_of(str)))
    Part_Key = attr.ib(validator=optional(instance_of(int)))
    Part_No = attr.ib(validator=optional(instance_of(str)))
    Part_No_Revision = attr.ib(validator=optional(instance_of(str)))
    Part_Status = attr.ib(validator=optional(instance_of(str)))
    Part_Type = attr.ib(validator=optional(instance_of(str)))
    Revision = attr.ib(validator=optional(instance_of(str)))
    Revision_Effective_Date = attr.ib(validator=optional(instance_of(str)), default=None)
    Spec_Rev_Exists = attr.ib(validator=optional(instance_of(str)))
    Temper = attr.ib(validator=optional(instance_of(str)), default=None)

    @classmethod
    def get(cls, part_num: str, revision: str):
        if revision is None:
            revision = '0'

        body = {
            "Part_No": part_num,
            "Revision": revision
        }

        return super().datasource_get(body)
