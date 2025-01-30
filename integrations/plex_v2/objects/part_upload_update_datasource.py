import attr
from attr.validators import instance_of, optional
from plex_v2.objects.base import BaseObject, CreateDatasourceMixin, RetrieveMixin, SearchMixin


@attr.s(kw_only=True)
class PartUploadUpdateDatasource(BaseObject, CreateDatasourceMixin, RetrieveMixin, SearchMixin):
    _resource_name = '14409/execute'

    Part_No = attr.ib(validator=optional(instance_of((str, None))), default=None)
    Revision = attr.ib(validator=optional(instance_of((str, None))), default=None)
    Description = attr.ib(validator=optional(instance_of((str, None))), default=None)
    Name = attr.ib(validator=optional(instance_of((str, None))), default=None)
    Part_Group = attr.ib(validator=optional(instance_of((str, None))), default=None)
    Part_Type = attr.ib(validator=optional(instance_of((str, None))), default=None)
    Part_Status = attr.ib(validator=optional(instance_of((str, None))), default=None)
    Product_Type = attr.ib(validator=optional(instance_of((str, None))), default=None)
    Part_Source = attr.ib(validator=optional(instance_of((str, None))), default=None)
    Standard_Job_Quantity = attr.ib(validator=optional(instance_of((int, None))), default=None)
    Use_DCP = attr.ib(validator=optional(instance_of((int, None))), default=None)
    Engineer3 = attr.ib(validator=optional(instance_of((str, None))), default=None)  # this means Estimator
    Building_Code = attr.ib(validator=optional(instance_of((str, None))), default=None)
    Planning_Group = attr.ib(validator=optional(instance_of((str, None))), default=None)
    Country_Of_Origin = attr.ib(validator=optional(instance_of((str, None))), default=None)
    Weight = attr.ib(validator=optional(instance_of((float, None))), default=None)
    Grade = attr.ib(validator=optional(instance_of((str, None))), default=None)
    Cycle_Frequency = attr.ib(validator=optional(instance_of(str)), default=None)
    Internal_Note = attr.ib(validator=optional(instance_of(str)), default=None)
