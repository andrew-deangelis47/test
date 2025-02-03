from typing import NamedTuple, List
from inforvisual.models import Part, WorkOrder, Operation, Customer

from paperless.objects.orders import OrderOperation, OrderComponent, OrderItem
from paperless.objects.quotes import QuoteItem
from dataclasses import dataclass, field


class CustomerData(NamedTuple):
    customer: Customer
    customer_is_new: bool


class PartData(NamedTuple):
    part: Part
    component: OrderComponent
    part_is_new: bool


class MaterialData(NamedTuple):
    part_data: PartData
    material_op: OrderOperation


@dataclass
class WorkOrderChildData:
    child_work_orders: List['WorkOrderData'] = field(default_factory=list)
    child_purchased_components: List['PurchasedComponentData'] = field(default_factory=list)


class WorkOrderData(NamedTuple):
    work_order: WorkOrder
    component: OrderComponent
    part_is_new: bool
    quantity_per_parent: int = 1
    deliver_quantity: int = 1
    child_data: WorkOrderChildData = WorkOrderChildData()


class QuoteItemData(NamedTuple):
    quote_item: QuoteItem
    work_order: WorkOrderData
    part: Part
    should_process: bool


class OperationData(NamedTuple):
    operation: Operation
    component: OrderComponent


class PurchasedComponentData(NamedTuple):
    part: Part
    component: OrderComponent
    quantity_per_parent: int = 1
    deliver_quantity: int = 1


class OrderItemData(NamedTuple):
    order_item: OrderItem
    should_process: bool


class PartProcessorData(NamedTuple):
    part_data: list
    material_data: list
    order_item_data: list
