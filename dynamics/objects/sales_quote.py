import attr

from dynamics.objects.base import BaseObject, str_type, num_type


@attr.s
class SalesQuote(BaseObject):

    resource_name = 'Sales_Quote_Excel'

    No = attr.ib(**str_type)
    Sell_to_Customer_No = attr.ib(**str_type)


@attr.s
class SalesQuoteLine(BaseObject):

    resource_name = 'Sales_QuoteSalesLines_Excel'

    Document_No = attr.ib(**str_type)
    Type = attr.ib(**str_type)
    No = attr.ib(**str_type)
    Quantity = attr.ib(**num_type)
