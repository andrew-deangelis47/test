import attr
from attr.validators import instance_of, optional
from plex_v2.objects.base import BaseObject, CreateDatasourceMixin, RetrieveMixin, SearchMixin


@attr.s(kw_only=True)
class RoutingUploadDataSource(BaseObject, CreateDatasourceMixin, RetrieveMixin, SearchMixin):
    _resource_name = '20274/execute'

    Active = attr.ib(validator=optional(instance_of(int)))
    Part_No = attr.ib(validator=optional(instance_of(str)))
    Revision = attr.ib(validator=optional(instance_of(str)))
    Operation_No = attr.ib(validator=optional(instance_of(int)))
    Operation_Code = attr.ib(validator=optional(instance_of(str)))
    Part_Op_Type = attr.ib(validator=optional(instance_of(str)))
    Label_Name = attr.ib(validator=optional(instance_of((str, None))), default=None)
    Net_Weight = attr.ib(validator=optional(instance_of((float, None))), default=None)
    Description = attr.ib(validator=optional(instance_of((str, None))), default=None)
    Note = attr.ib(validator=optional(instance_of((str, None))), default=None)
