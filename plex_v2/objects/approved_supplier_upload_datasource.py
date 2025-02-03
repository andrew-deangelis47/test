import attr
from attr.validators import instance_of, optional
from plex_v2.objects.base import BaseObject, CreateDatasourceMixin, RetrieveMixin, SearchMixin


@attr.s(kw_only=True)
class ApprovedSupplierAddUpdateDatasource(BaseObject, CreateDatasourceMixin, RetrieveMixin, SearchMixin):
    _resource_name = '233467/execute'

    # required
    Active = attr.ib(validator=optional(instance_of(int)))
    Operation_Code = attr.ib(validator=optional(instance_of(str)))
    Operation_No = attr.ib(validator=optional(instance_of(int)))
    Part_No = attr.ib(validator=optional(instance_of(str)))
    Supplier_Code = attr.ib(validator=optional(instance_of(str)))

    # optional
    Business_Percentage = attr.ib(validator=optional(instance_of(float)), default=None)
    Cycle_Time = attr.ib(validator=optional(instance_of(float)), default=None)
    Fabrication_Release_Days = attr.ib(validator=optional(instance_of(int)), default=None)
    Lead_Time = attr.ib(validator=optional(instance_of(float)), default=None)
    Minimum_Quantity = attr.ib(validator=optional(instance_of(float)), default=None)
    MRP_Firm_Days = attr.ib(validator=optional(instance_of(int)), default=None)
    MRP_Forecast_Days = attr.ib(validator=optional(instance_of(int)), default=None)
    MRP_Plan_Days = attr.ib(validator=optional(instance_of(int)), default=None)
    New_Supplier_Code = attr.ib(validator=optional(instance_of(str)), default=None)
    Note = attr.ib(validator=optional(instance_of(str)), default=None)
    Price = attr.ib(validator=optional(instance_of(float)), default=None)
    Price_Conversion = attr.ib(validator=optional(instance_of(float)), default=None)
    Price_Unit = attr.ib(validator=optional(instance_of(str)), default=None)
    Raw_Release_Days = attr.ib(validator=optional(instance_of(int)), default=None)
    Remove_Supplier = attr.ib(validator=optional(instance_of(bool)), default=None)
    Revision = attr.ib(validator=optional(instance_of(str)), default=None)
    Sort_Order = attr.ib(validator=optional(instance_of(int)), default=None)
    Supplier_Part_No = attr.ib(validator=optional(instance_of(str)), default=None)
    Transit_Time = attr.ib(validator=optional(instance_of(float)), default=None)
    UPC_Code = attr.ib(validator=optional(instance_of(str)), default=None)
