import json
from baseintegration.datamigration import logger

import attr
from attr.validators import instance_of, optional, deep_iterable

from client import PlexClient
from plex.objects.base import BaseObject, CreateMixin, SearchMixin
from typing import List
from plex.exceptions import PlexException


@attr.s(kw_only=True)
class SalesOrderLinePrice(BaseObject, CreateMixin):
    order_id = None
    line_id = None

    unit = attr.ib(validator=instance_of(str))
    currencyCode = attr.ib(validator=instance_of(str))

    price = attr.ib(validator=optional(instance_of((int, float))), default=None)
    breakpointQuantity = attr.ib(validator=optional(instance_of((int, float))), default=None)
    effectiveDate = attr.ib(validator=optional(instance_of(str)), default=None)
    expirationDate = attr.ib(validator=optional(instance_of(str)), default=None)

    @classmethod
    def get_serialization_schema(cls, mode):
        if mode == 'out':
            schema = super().get_serialization_schema('out')
            del schema['id']
            # del schema['order_id']
            # del schema['line_id']
            return schema
        elif mode == 'in':
            return super().get_serialization_schema('in')

    @classmethod
    def get_resource_name(cls, action, instance=None, **kwargs):
        version = 'v1-beta1' if action == 'create' else 'v1'
        if instance is not None:
            order_id = instance.order_id
            line_id = instance.line_id
            if order_id is not None and line_id is not None:
                return f'sales/{version}/orders/{order_id}/lines/{line_id}/prices'
        if 'order_id' not in kwargs or 'line_id' not in kwargs:
            raise KeyError(
                'order_id and line_id must be given to resource_name_kwargs for SalesOrderLinePrice'
            )
        order_id = kwargs['order_id']
        line_id = kwargs['line_id']
        return f'sales/{version}/orders/{order_id}/lines/{line_id}/prices'


@attr.s(kw_only=True)
class SalesOrderRelease(BaseObject, CreateMixin):
    type = attr.ib(validator=instance_of(str))
    quantity = attr.ib(validator=instance_of((int, float)))
    status = attr.ib(validator=instance_of(str))
    shipFrom = attr.ib(validator=instance_of(str))  # Building 1
    orderLineId = attr.ib(validator=instance_of(str))
    dueDate = attr.ib(validator=instance_of(str))

    releaseNumber = attr.ib(validator=optional(instance_of(str)), default='')
    shipToAddressId = attr.ib(validator=optional(instance_of(str)), default=None)
    shipDate = attr.ib(validator=optional(instance_of(str)), default=None)
    source = attr.ib(validator=optional(instance_of(str)), default=None)
    note = attr.ib(validator=optional(instance_of(str)), default='')
    scheduleNo = attr.ib(validator=optional(instance_of(str)), default='')
    scheduleDate = attr.ib(validator=optional(instance_of(str)), default=None)
    orderQuantity = attr.ib(validator=instance_of((int, float)), default=0)
    fabAuthorizationNo = attr.ib(validator=optional(instance_of(str)), default='')
    rawAuthorizationNo = attr.ib(validator=optional(instance_of(str)), default='')
    productionStartDate = attr.ib(validator=optional(instance_of(str)), default=None)
    modelName = attr.ib(validator=optional(instance_of(str)), default=None)
    packagingNote = attr.ib(validator=optional(instance_of(str)), default='')

    @classmethod
    def get_serialization_schema(cls, mode):
        if mode == 'out':
            schema = super().get_serialization_schema('out')
            del schema['id']
            return schema
        elif mode == 'in':
            return super().get_serialization_schema('in')

    @classmethod
    def get_resource_name(cls, action, instance=None, **kwargs):
        version = 'v1-beta1' if action == 'create' else 'v1'
        return f'sales/{version}/releases'


@attr.s(kw_only=True)
class SalesOrderLineApprovedShipTo(BaseObject, CreateMixin):
    shipToAddressId = attr.ib(validator=optional(instance_of(str)), default=None)
    defaultCarrier = attr.ib(validator=optional(instance_of(str)), default=None)
    defaultShipFromId = attr.ib(validator=optional(instance_of(str)), default=None)
    defaultShipFromCode = attr.ib(validator=optional(instance_of(str)), default=None)

    order_id = None
    line_id = None

    @classmethod
    def get_serialization_schema(cls, mode):
        if mode == 'out':
            schema = super().get_serialization_schema('out')
            del schema['id']
            # del schema['order_id']
            # del schema['line_id']
            return schema
        elif mode == 'in':
            return super().get_serialization_schema('in')

    @classmethod
    def get_resource_name(cls, action, instance=None, **kwargs):
        version = 'v1-beta1' if action == 'create' else 'v1'
        if instance is not None:
            order_id = instance.order_id
            line_id = instance.line_id
            if order_id is not None and line_id is not None:
                return f'sales/{version}/orders/{order_id}/lines/{line_id}/approved-ship-tos'
        if 'order_id' not in kwargs or 'line_id' not in kwargs:
            raise KeyError(
                'order_id and line_id must be given to resource_name_kwargs for SalesOrderLinePrice'
            )
        order_id = kwargs['order_id']
        line_id = kwargs['line_id']
        return f'sales/{version}/orders/{order_id}/lines/{line_id}/prices'


@attr.s(kw_only=True)
class SalesOrderLine(BaseObject, CreateMixin):
    partId = attr.ib(validator=optional(instance_of(str)), default=None)
    customerPartId = attr.ib(validator=optional(instance_of(str)), default=None)
    note = attr.ib(validator=optional(instance_of(str)), default='')
    lineNumber = attr.ib(validator=instance_of(str), default='')
    containerType = attr.ib(validator=optional(instance_of(str)), default=None)
    standardPackQuantity = attr.ib(validator=instance_of((int, float)), default=0)
    accountingJobNumber = attr.ib(validator=optional(instance_of(str)), default=None)
    active = attr.ib(validator=instance_of(bool), default=False)
    defaultOrderUnitId = attr.ib(validator=optional(instance_of(str)), default=None)
    packagingNote = attr.ib(validator=optional(instance_of(str)), default='')
    shippingInstructions = attr.ib(validator=optional(instance_of(str)), default='')

    _line_prices: List[SalesOrderLinePrice] = attr.ib(
        validator=optional(
            deep_iterable(member_validator=instance_of(SalesOrderLinePrice), iterable_validator=instance_of(list))),
        default=None,
    )
    order_id = None

    def add_line_price(self, price: SalesOrderLinePrice):
        if self._line_prices is None:
            self._line_prices = []
        self._line_prices.append(price)

    @classmethod
    def get_serialization_schema(cls, mode):
        if mode == 'out':
            schema = super().get_serialization_schema('out')
            del schema['id']
            # del schema['order_id']
            del schema['_line_prices']
            return schema
        elif mode == 'in':
            schema = super().get_serialization_schema('in')
            del schema['_line_prices']
            return schema

    @classmethod
    def get_resource_name(cls, action, instance=None, **kwargs):
        if instance is not None:
            order_id = instance.order_id
            if order_id is not None:
                return f'sales/v1-beta1/orders/{order_id}/lines'
        if 'order_id' not in kwargs:
            raise KeyError('order_id must be given to resource_name_kwargs for OrderLine')
        order_id = kwargs['order_id']
        return f'sales/v1-beta1/orders/{order_id}/lines'

    def make_release(self, quantity, status, ship_from, type, due_date, create=False) -> SalesOrderRelease:
        if not self.is_created() and create is True:
            self.create(in_place=True)
        elif not self.is_created() and create is False:
            raise PlexException('make_release cannot be called until this object is created.')
        return SalesOrderRelease(
            orderLineId=self.id,
            quantity=quantity,
            status=status,
            shipFrom=ship_from,
            type=type,
            dueDate=due_date,
        )

    def create(self, in_place=True, resource_name_kwargs=None):
        created_order_line = super().create(in_place=in_place, resource_name_kwargs=resource_name_kwargs)
        new_order_line_prices = []
        for price in self._line_prices:
            price.order_id = self.order_id
            price.line_id = created_order_line.id
            new_order_line_prices.append(price.create(in_place=in_place))
        created_order_line._line_prices = new_order_line_prices
        return created_order_line


@attr.s(kw_only=True)
class SalesOrder(BaseObject, CreateMixin, SearchMixin):
    customerId = attr.ib(validator=instance_of(str))
    orderNumber = attr.ib(validator=instance_of(str), default='')
    poNumber = attr.ib(validator=instance_of(str))
    status = attr.ib(validator=instance_of(str))
    type = attr.ib(validator=instance_of(str))
    terms = attr.ib(validator=optional(instance_of(str)), default=None)
    fob = attr.ib(validator=instance_of(str))
    poNumberRevision = attr.ib(validator=instance_of(str))

    note = attr.ib(validator=instance_of(str), default='')
    invoiceInternalNote = attr.ib(validator=instance_of(str), default='')
    invoicePrintedNote = attr.ib(validator=instance_of(str), default='')
    incoTerms = attr.ib(validator=optional(instance_of(str)), default='')
    freightTerms = attr.ib(validator=optional(instance_of(str)), default='')

    category = attr.ib(validator=optional(instance_of(str)), default=None)
    insideSalesId = attr.ib(validator=optional(instance_of(str)), default=None)
    outsideSalesId = attr.ib(validator=optional(instance_of(str)), default=None)
    poNumberRevisionDate = attr.ib(validator=optional(instance_of(str)), default=None)
    orderDate = attr.ib(validator=optional(instance_of(str)), default=None)
    expirationDate = attr.ib(validator=optional(instance_of(str)), default=None)
    contactId = attr.ib(validator=optional(instance_of(str)), default=None)
    carrier = attr.ib(validator=optional(instance_of(str)), default=None)
    multipleDocksPerShipper = attr.ib(validator=instance_of(bool), default=False)
    multiplePOPerShipper = attr.ib(validator=instance_of(bool), default=False)

    createdById = attr.ib(validator=optional(instance_of(str)), default=None)
    modifiedById = attr.ib(validator=optional(instance_of(str)), default=None)
    billToAddressId = attr.ib(validator=optional(instance_of(str)), default=None)
    shipToAddressId = attr.ib(validator=optional(instance_of(str)), default=None)

    @classmethod
    def get_serialization_schema(cls, mode):
        if mode == 'out':
            schema = super().get_serialization_schema('out')
            del schema['id']
            return schema
        elif mode == 'in':
            return super().get_serialization_schema('in')

    @classmethod
    def get_resource_name(cls, action, instance=None, **kwargs):
        version = 'v1-beta1' if action == 'create' else 'v1'
        return f'sales/{version}/orders'

    @classmethod
    def find_sales_orders(cls, poNumber=None, customerId=None):
        return cls.search(
            poNumber=poNumber,
            customerId=customerId,
            exclude_if_null=['poNumber', 'customerId'],
        )


@attr.s(kw_only=True)
class SalesOrder2Tier(BaseObject, CreateMixin, SearchMixin):
    Bill_To_Customer_Address_Code = attr.ib(validator=instance_of(str), default='')
    Carrier_Code = attr.ib(validator=instance_of(str), default='')
    Carrier_Text = attr.ib(validator=instance_of(str), default='')
    Customer_Code = attr.ib(validator=optional(instance_of(str)), default='')
    customerId = attr.ib(validator=instance_of(str))
    Freight_Amount = attr.ib(validator=instance_of(int), default=0)
    Freight_Terms = attr.ib(validator=instance_of(str), default='')
    Inside_Sales = attr.ib(validator=instance_of(str), default='')
    Note = attr.ib(validator=instance_of(str), default='')
    Order_No_Custom = attr.ib(validator=instance_of(str), default='')
    Order_No_Prefix = attr.ib(validator=instance_of(str), default='')
    Order_Terms = attr.ib(validator=instance_of(str), default='')
    Ordered_By = attr.ib(validator=instance_of(str), default='')
    PO_Category = attr.ib(validator=instance_of(str), default='')
    PO_No = attr.ib(validator=instance_of(str), default='')
    PO_Type = attr.ib(validator=instance_of(str), default='')
    Prepaid_Amount = attr.ib(validator=instance_of(int), default=0)
    Prepaid_Authorization = attr.ib(validator=instance_of(str), default='')
    Printed_Note = attr.ib(validator=instance_of(str), default='')
    Ship_From_Building_Code = attr.ib(validator=instance_of(str), default='')
    Ship_To_Customer_Address_Code = attr.ib(validator=instance_of(str), default='')
    Shipper_Email = attr.ib(validator=instance_of(str), default='')
    Shipping_Instructions = attr.ib(validator=instance_of(str), default='')
    Shipping_Service = attr.ib(validator=instance_of(str), default='')
    Tax_Amount = attr.ib(validator=instance_of(int), default=0)
    c_url = attr.ib(validator=optional(instance_of(str)), default='')

    def create(self):
        body = {
            "inputs": {
                '3Tier_Order': "False",
                'Bill_To_Customer_Address_Code': self.Bill_To_Customer_Address_Code,
                'Carrier_Code': self.Carrier_Code,
                'Carrier_Text': self.Carrier_Text,
                'Customer_Code': self.Customer_Code,
                'Freight_Amount': self.Freight_Amount,
                'Freight_Terms': self.Freight_Terms,
                'Inside_Sales': self.Inside_Sales,
                'Note': self.Note,
                'Order_No_Custom': self.Order_No_Custom,
                'Order_No_Prefix': self.Order_No_Prefix,
                'Order_Terms': self.Order_Terms,
                'Ordered_By': self.Ordered_By,
                'PO_Category': self.PO_Category,
                'PO_No': self.PO_No,
                'PO_Type': self.PO_Type,
                'Prepaid_Amount': self.Prepaid_Amount,
                'Prepaid_Authorization': self.Prepaid_Authorization,
                'Printed_Note': self.Printed_Note,
                'Ship_From_Building_Code': self.Ship_From_Building_Code,
                'Ship_To_Customer_Address_Code': self.Ship_To_Customer_Address_Code,
                'Shipper_Email': self.Shipper_Email,
                'Shipping_Instructions': self.Shipping_Instructions,
                'Shipping_Service': self.Shipping_Service,
                'Tax_Amount': self.Tax_Amount
            }
        }

        client = self._get_client()
        resp = client.request(url=self.c_url, method=PlexClient.METHODS.POST, data=json.dumps(body), datasource=True)
        r_json: dict = json.loads(resp.text)
        output: dict = r_json.get('outputs', {})
        logger.debug(output)
        if not output.get('Result_Error'):
            order_number: str = output.get('Order_No')
            new_sales_orders = SalesOrder.find_sales_orders(poNumber=self.PO_No, customerId=self.customerId)
            new_sales_order = new_sales_orders[0] if len(new_sales_orders) > 0 else None
            new_sales_order.order_number = order_number
            return new_sales_order
        return output.get('ResultMessage')


@attr.s(kw_only=True)
class SalesOrderLineDataSource(BaseObject, CreateMixin):
    customerId = attr.ib(validator=optional(instance_of(str)), default=None)
    partId = attr.ib(validator=optional(instance_of(str)), default=None)
    customerPartId = attr.ib(validator=optional(instance_of(str)), default=None)
    partRev = attr.ib(validator=optional(instance_of(str)), default=None)
    customerPartRev = attr.ib(validator=optional(instance_of(str)), default=None)
    price = attr.ib(validator=optional(instance_of(float)), default=None)
    note = attr.ib(validator=optional(instance_of(str)), default='')
    standardPackQuantity = attr.ib(validator=instance_of((int, float)), default=1)
    unit_type = attr.ib(validator=optional(instance_of(str)), default='')
    packagingNote = attr.ib(validator=optional(instance_of(str)), default='')
    priority = attr.ib(validator=optional(instance_of(str)), default='')
    releaseSource = attr.ib(validator=optional(instance_of(str)), default='')
    releaseStatus = attr.ib(validator=optional(instance_of(str)), default='')
    releaseType = attr.ib(validator=optional(instance_of(str)), default='')
    shipDate = attr.ib(validator=optional(instance_of(str)), default='')
    dueDate = attr.ib(validator=optional(instance_of(str)), default='')
    order_id = attr.ib(validator=optional(instance_of(str)), default=None)
    c_url = attr.ib(validator=optional(instance_of(str)), default='')

    _line_prices: List[SalesOrderLinePrice] = attr.ib(
        validator=optional(
            deep_iterable(member_validator=instance_of(SalesOrderLinePrice), iterable_validator=instance_of(list))),
        default=None,
    )

    @classmethod
    def get_serialization_schema(cls, mode):
        return SalesOrderLine.get_serialization_schema(mode)

    @classmethod
    def get_resource_name(cls, action, instance=None, **kwargs):
        return SalesOrderLine.get_resource_name(action, instance, **kwargs)

    def create(self) -> bool:
        body = {
            "inputs": {
                "Customer_Code": self.customerId,
                "Customer_Part_No": self.customerPartId,
                "Customer_Part_Revision": self.customerPartRev,
                "Order_No": self.order_id,
                "Part_No": self.partId,
                "Price": self.price,
                "Price_Unit": self.unit_type,
                "Priority": self.priority,
                "Quantity": self.standardPackQuantity,
                "Quantity_Unit": self.unit_type,
                "Release_Note": self.note,
                "Release_Printed_Note": self.packagingNote,
                "Release_Source": self.releaseSource,
                "Release_Status": "Wait for Release",
                "Release_Type": self.releaseType,
                "Revision": self.partRev,
                "Ship_Date": self.shipDate,
                "Due_Date": self.dueDate
            }
        }
        logger.debug(json.dumps(body))
        client = self._get_client()
        resp = client.request(url=self.c_url, method=PlexClient.METHODS.POST, data=json.dumps(body), datasource=True)
        logger.debug(resp)
        return True
