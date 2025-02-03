from typing import NamedTuple, Optional

from paperless.objects.orders import OrderComponent, OrderItem
from acumatica.api_models.acumatica_models import Customer, StockItem,\
    ProductionOrder, ProductionOrderDetail, Contact


class AcumaticaConfig:
    def __init__(self):
        pass


class StockItemData(NamedTuple):
    component: OrderComponent
    order_item: OrderItem
    is_purchased: bool
    is_root_item: bool
    is_make_part: bool
    stock_item: StockItem = None
    qty_required: float = 0.0
    unit_cost: float = 0.0
    notes: str = ''
    deliver_to: str = None
    internal_notes: str = None
    router_sequence: int = 1


class SalesOrderDetailData(NamedTuple):
    ships_on: str
    stock_item: StockItemData
    order_item: OrderItem
    line_nbr: int


class ProductionOrderData(NamedTuple):
    production_order: ProductionOrder
    stock_item_data: StockItemData
    order_item: OrderItem
    is_root_component: bool


class ProductionOrderDetailData(NamedTuple):
    production_order_data: ProductionOrderData
    production_order_detail: ProductionOrderDetail


class CustomerData(NamedTuple):
    customer: Customer
    contact: Optional[Contact]
    facility_erp_code: Optional[str]


class Facility(NamedTuple):
    warehouse: str
    branch: str
