from typing import NamedTuple, Union, List
from paperless.objects.orders import OrderComponent, OrderOperation
from sage.models.sage_models.part import PartFullEntity as Part
from uuid import uuid4


class TreeNode(NamedTuple):
    component_id: Union[int, None] = None
    component_instance_uuid: Union[uuid4, None] = None
    assembly_seq_num: Union[int, None] = None
    parent_id: Union[int, None] = None
    parent_instance_uuid: Union[uuid4, None] = None
    quantity_per_parent: Union[int, None] = None
    part_number: Union[str, None] = None
    line_item_num: Union[int, None] = None


class ItemData(NamedTuple):
    part_number: str
    component: OrderComponent
    item_is_new: bool
    revision: Union[str, None]
    part_class: str
    part_description: str
    quote_line: int
    quote_assm_seq_num: int = None
    unit_price: float = 0
    sage_part_record: Part = None


class MaterialData(NamedTuple):
    part_data: ItemData
    parent_item_no: str
    material_op: OrderOperation


class PurchasedComponentData(NamedTuple):
    component_data: ItemData
    parent_item_no: str = None


class LineItemData(NamedTuple):
    manufactured_components: List[ItemData] = []
    purchased_components: List[PurchasedComponentData] = []
    materials: List[MaterialData] = []
    true_assembly_tree_nodes: List[TreeNode] = []
    quote_detail_number: int = None
