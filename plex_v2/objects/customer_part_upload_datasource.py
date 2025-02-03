import attr
from attr.validators import instance_of, optional
from plex_v2.objects.base import BaseObject, CreateDatasourceMixin, RetrieveMixin, SearchMixin


@attr.s(kw_only=True)
class CustomerPartUploadDataSource(BaseObject, CreateDatasourceMixin, RetrieveMixin, SearchMixin):
    _resource_name = '18264/execute'

    # required
    Customer_Part_No = attr.ib(validator=optional(instance_of(str)))
    Part_No = attr.ib(validator=optional(instance_of(str)))

    # optional
    Account_No = attr.ib(validator=optional(instance_of(str)), default=None)
    Active = attr.ib(validator=optional(instance_of(int)), default=None)
    Application = attr.ib(validator=optional(instance_of(str)), default=None)
    Breakpoint_Quantity = attr.ib(validator=optional(instance_of(float)), default=None)
    Customer_Address_Code = attr.ib(validator=optional(instance_of(str)), default=None)
    Customer_Code = attr.ib(validator=optional(instance_of(str)), default=None)
    Customer_Part_Description = attr.ib(validator=optional(instance_of(str)), default=None)
    Customer_Part_No = attr.ib(validator=optional(instance_of(str)), default=None)
    Customer_Part_Price_Key = attr.ib(validator=optional(instance_of(int)), default=None)
    Customer_Part_Revision = attr.ib(validator=optional(instance_of(str)), default=None)
    Customer_Part_Weight = attr.ib(validator=optional(instance_of(str)), default=None)
    Default_Container_Type = attr.ib(validator=optional(instance_of(str)), default=None)
    Drawing_No = attr.ib(validator=optional(instance_of(str)), default=None)
    Drawing_Revision = attr.ib(validator=optional(instance_of(str)), default=None)
    Effective_Date = attr.ib(validator=optional(instance_of(str)), default=None)
    End_Usage_Type = attr.ib(validator=optional(instance_of(str)), default=None)
    Estimated_Annual_Usage = attr.ib(validator=optional(instance_of(int)), default=None)
    Expiration_Date = attr.ib(validator=optional(instance_of(str)), default=None)
    Index_Delta_Calculation = attr.ib(validator=optional(instance_of(str)), default=None)
    Invoice_Adjustment_Amount = attr.ib(validator=optional(instance_of(float)), default=None)
    Label_Format = attr.ib(validator=optional(instance_of(str)), default=None)
    Minimum_Buy_Quantity = attr.ib(validator=optional(instance_of(float)), default=None)
    New_Effective_Date = attr.ib(validator=optional(instance_of(str)), default=None)
    New_Expiration_Date = attr.ib(validator=optional(instance_of(str)), default=None)
    Parent_Customer_Code = attr.ib(validator=optional(instance_of(str)), default=None)
    Part_Label_Format = attr.ib(validator=optional(instance_of(str)), default=None)
    Price = attr.ib(validator=optional(instance_of(float)), default=None)
    Price_Action = attr.ib(validator=optional(instance_of(str)), default=None)
    Price_Index = attr.ib(validator=optional(instance_of(str)), default=None)
    Price_Note = attr.ib(validator=optional(instance_of(str)), default=None)
    Printed_Note = attr.ib(validator=optional(instance_of(str)), default=None)
    Product_Type = attr.ib(validator=optional(instance_of(str)), default=None)
    Program_Code = attr.ib(validator=optional(instance_of(str)), default=None)
    Program_Quantity_Per_Vehicle = attr.ib(validator=optional(instance_of(float)), default=None)
    Quantity_Per_Vehicle = attr.ib(validator=optional(instance_of(float)), default=None)
    Reference_No = attr.ib(validator=optional(instance_of(str)), default=None)
    Revision = attr.ib(validator=optional(instance_of(str)), default=None)
    UPC_Code = attr.ib(validator=optional(instance_of(int)), default=None)
    Update_Open_Orders = attr.ib(validator=optional(instance_of(int)), default=None)
