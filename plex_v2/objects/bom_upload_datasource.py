import attr
from attr.validators import instance_of, optional
from plex_v2.objects.base import BaseObject, CreateDatasourceMixin, RetrieveMixin, SearchMixin


@attr.s(kw_only=True)
class BomUploadDatasource(BaseObject, CreateDatasourceMixin, RetrieveMixin, SearchMixin):
    _resource_name = '15908/execute'

    # required
    Component_Part_No = attr.ib(validator=optional(instance_of(str)))
    Operation_Code = attr.ib(validator=optional(instance_of(str)))
    Part_No = attr.ib(validator=optional(instance_of(str)))
    Quantity = attr.ib(validator=optional(instance_of((int, float))))

    # optional
    Auto_Deplete = attr.ib(validator=optional(instance_of(int)), default=None)
    Component_Revision = attr.ib(validator=optional(instance_of(str)))
    Component_Type = attr.ib(validator=optional(instance_of(str)), default=None)
    Engineering_Quantity = attr.ib(validator=optional(instance_of(float)), default=None)
    Fixed_Loss = attr.ib(validator=optional(instance_of(float)), default=None)
    Fixed_Qty = attr.ib(validator=optional(instance_of(int)), default=None)
    Max_Qty = attr.ib(validator=optional(instance_of(float)), default=None)
    Min_Qty = attr.ib(validator=optional(instance_of(float)), default=None)
    Note = attr.ib(validator=optional(instance_of(str)), default=None)
    Operation_No = attr.ib(validator=optional(instance_of(int)))
    Position = attr.ib(validator=optional(instance_of(str)), default=None)
    Revision = attr.ib(validator=optional(instance_of(str)))
    Scaling = attr.ib(validator=optional(instance_of(int)), default=None)
    Sort_Order = attr.ib(validator=optional(instance_of(float)), default=None)
    Transfer_Heat = attr.ib(validator=optional(instance_of(int)))
    Unit_Conversion = attr.ib(validator=optional(instance_of(str)), default=None)
    Validate = attr.ib(validator=optional(instance_of(int)), default=None)
    Yield_Management_Enabled = attr.ib(validator=optional(instance_of(bool)), default=None)
    Yield_Percentage = attr.ib(validator=optional(instance_of(float)), default=None)
