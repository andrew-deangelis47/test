from typing import NamedTuple, List, Optional, Union
from paperless.objects.orders import OrderComponent, OrderOperation
from baseintegration.datamigration import logger
from epicor.client import EpicorClient
from epicor.customer import Customer, Contact, ShipTo
from epicor.exceptions import EpicorNotFoundException
from epicor.operation import Resource, ResourceGroup, Operation, OperationDetails
from epicor.part import Part
from uuid import uuid4


class EpicorConfig:

    def __init__(self):
        pass


class TreeNode(NamedTuple):
    component_id: Union[int, None] = None
    component_instance_uuid: Union[uuid4, None] = None
    assembly_seq_num: Union[int, None] = None
    bom_level: Union[int, None] = None
    parent_id: Union[int, None] = None
    parent_instance_uuid: Union[uuid4, None] = None
    quantity_per_parent: Union[int, None] = None
    part_number: Union[str, None] = None
    part_description: Union[str, None] = None
    part_revision: Union[str, None] = None
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
    epicor_part_record: Part = None
    part_record_exists: bool = True


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


class CustomerData(NamedTuple):
    customer: Customer
    contact: Optional[Contact]
    shipping_address: Optional[ShipTo]


class QuoteHeaderData(NamedTuple):
    line_items: List[LineItemData]
    customer_data: CustomerData = None


class WorkCenterIDData(NamedTuple):
    type: Union[type(Operation), type(Resource), type(ResourceGroup), type(OperationDetails)]
    id: str


def get_part_number_and_name(component, pp_mat_id_variable: Optional[str] = None):
    # Could be either a component or operation - based on whether we're creating a component or material item
    if isinstance(component, OrderOperation) and pp_mat_id_variable is not None:
        logger.info("Getting part number out of material operation")
        part_number = component.get_variable(pp_mat_id_variable)
        part_name = part_number
    else:
        part_number = component.part_number.strip() if component.part_number is not None else None
        if not part_number:
            part_number = str(component.part_name)[0:50]
        part_name = component.part_name
    logger.info(f"Processing part with part number '{part_number}'")
    return part_number, part_name


def get_item_data_by_part_number(mfg_item_data_list: List[ItemData], part_num) -> ItemData:
    for mfg_part in mfg_item_data_list:
        if mfg_part.part_number == part_num:
            return mfg_part
    else:
        raise ValueError("Item data not found")


def get_item_data_by_component_id(mfg_item_data_list: List[ItemData], component_id) -> ItemData:
    """
    Get manufactured ItemData by matching attempting to match each ItemData object's component ID with
    the supplied component ID.
    """
    for mfg_part in mfg_item_data_list:
        if mfg_part.component.id == component_id:
            return mfg_part
    else:
        raise ValueError("Item data not found")


def get_line_item_data_by_line_number(line_items_list, line_number) -> LineItemData:
    for line_item_data in line_items_list:
        if line_item_data.quote_detail_number == line_number:
            return line_item_data
    else:
        raise ValueError("Quote detail item data not found")


def get_true_assembly_tree_nodes_by_line_number(line_items_list, line_number) -> List[TreeNode]:
    return get_line_item_data_by_line_number(line_items_list, line_number).true_assembly_tree_nodes


def get_manufactured_components_by_line_number(line_items_list, line_number) -> List[ItemData]:
    return get_line_item_data_by_line_number(line_items_list, line_number).manufactured_components


def get_materials_by_line_number(line_items_list, line_number) -> List[MaterialData]:
    return get_line_item_data_by_line_number(line_items_list, line_number).materials


def get_purchased_components_by_line_number(line_items_list, line_number) -> List[PurchasedComponentData]:
    return get_line_item_data_by_line_number(line_items_list, line_number).purchased_components


def get_epicor_part_cost_model(component_id: str, epicor_client: EpicorClient = None) -> dict:
    client = epicor_client if epicor_client else EpicorClient.get_instance()
    specific_endoint = 'Erp.BO.PartCostSearchSvc/PartCostSearches'
    filter_query: dict = {"$filter": f"PartNum eq '{component_id}'"}
    get_part: list = client.get_resource(specific_endoint, params=filter_query)["value"]
    if not get_part:
        raise EpicorNotFoundException(f"Epicor Part '{component_id}' does not exist.")
    else:
        get_part: dict = get_part[0]
    return get_part
