from dataclasses import dataclass
from typing import Optional

from baseintegration.utils import safe_get
from baseintegration.utils.sqlite_models import SQLiteDBGenerator
from inforvisual.models import Operation, ShopResource, Requirement, Part, Quote, Customer, QuoteLine, QuotePrice, \
    WorkOrder, PartSite, CustOrderLine, DemandSupplyLink


@dataclass
class PartData:
    is_root: bool = False
    part_type: str = 'manufactured'


part_id_separator = ':_:'


def get_part_id_from_requirement(requirement: Requirement):
    """
    Requirements (i.e. materials or child parts) do not need a part ID. This function generates
    an identifier for these based on the requirement ID.
    """
    backup_part_id = part_id_separator.join([str(requirement.piece_no), str(requirement.pk), '[WO ONLY]'])
    return requirement.part_id or backup_part_id


def is_part_id_from_requirement(part_id: str):
    return part_id.split(part_id_separator)[-1] == '[WO ONLY]'


def get_requirement_from_part_id(part_id: str, source_db="default") -> Optional[Requirement]:
    requirement_pk = part_id.split(part_id_separator)[1]
    return Requirement.objects.using(source_db).filter(pk=requirement_pk).first()


def get_operation_costing_variables(operation: Operation):
    resource: ShopResource = operation.resource
    operation_type = safe_get(operation, 'operation_type.id', '')
    return {
        "resource_id": (resource.id, str),
        "description": (resource.description, str),
        "type": (resource.type, str),
        "operation_type": (operation_type, str),
        "setup_hrs": (operation.setup_hrs, float),
        "run_hrs": (operation.run_hrs, float),
        "scrap_yield_pct": (operation.scrap_yield_pct, float),
        "setup_cost_per_hr": (operation.setup_cost_per_hr, float),
        "run_cost_per_hr": (operation.run_cost_per_hr, float),
        "bur_percent_setup": (operation.bur_percent_setup, float),
        "bur_percent_run": (operation.bur_percent_run, float),
        "move_hrs": (operation.move_hrs, float),
        "shift_1_capacity": (resource.shift_1_capacity, float),
        "shift_2_capacity": (resource.shift_2_capacity, float),
        "shift_3_capacity": (resource.shift_3_capacity, float),
    }


def get_material_costing_variables(requirement: Requirement):
    part: Part = requirement.part
    if part:
        description = part.description
        commodity_code = part.commodity_code
        qty_on_hand = part.qty_on_hand
    else:
        description = ""
        commodity_code = ""
        qty_on_hand = 0
    return {
        "material_id": (requirement.part_id, str),
        "description": (description, str),
        "commodity_code": (commodity_code, str),
        "qty_on_hand": (qty_on_hand, float),
        "calc_qty": (requirement.calc_qty, float),
        "fixed_qty": (requirement.fixed_qty, float),
        "unit_material_cost": (requirement.unit_material_cost, float),
        "length": (requirement.length, float),
        "width": (requirement.width, float),
        "height": (requirement.height, float),
        "planning_leadtime": (requirement.planning_leadtime, float),
        "user_1": (requirement.user_1, str),
        "user_2": (requirement.user_2, str),
        "user_3": (requirement.user_3, str),
        "user_4": (requirement.user_4, str),
        "user_5": (requirement.user_5, str),
    }


def create_all_sqlite_tables_if_not_exists():
    # Instantiate SQLite db generator. Configure SQLite DB. Create models.
    sql_db_generator = SQLiteDBGenerator("inforvisual")
    sql_db_generator.configure_db_connections()

    sql_db_generator.create_sqlite_table_from_model(Customer)
    sql_db_generator.create_sqlite_table_from_model(Quote)
    sql_db_generator.create_sqlite_table_from_model(QuoteLine)
    sql_db_generator.create_sqlite_table_from_model(QuotePrice)
    sql_db_generator.create_sqlite_table_from_model(WorkOrder)
    sql_db_generator.create_sqlite_table_from_model(Requirement)
    sql_db_generator.create_sqlite_table_from_model(Operation)
    sql_db_generator.create_sqlite_table_from_model(Part)
    sql_db_generator.create_sqlite_table_from_model(PartSite)
    sql_db_generator.create_sqlite_table_from_model(ShopResource)
    sql_db_generator.create_sqlite_table_from_model(CustOrderLine)
    sql_db_generator.create_sqlite_table_from_model(DemandSupplyLink)

    sql_db_generator.copy_data_to_sqlite()


def create_indexes_on_all_sqlite_tables():
    # Instantiate SQLite db generator. Configure SQLite DB. Create models.
    sql_db_generator = SQLiteDBGenerator("inforvisual")
    sql_db_generator.configure_db_connections()

    sql_db_generator.create_sqlite_index_from_fields(Part.id)
    sql_db_generator.create_sqlite_index_from_fields(Part.purchased)
    sql_db_generator.create_sqlite_index_from_fields(Part.id, Part.purchased)

    sql_db_generator.create_sqlite_index_from_fields(WorkOrder.part, WorkOrder.type, WorkOrder.sub_id)
    sql_db_generator.create_sqlite_index_from_fields(
        WorkOrder.type, WorkOrder.base_id, WorkOrder.lot_id, WorkOrder.split_id, WorkOrder.sub_id)

    sql_db_generator.create_sqlite_index_from_fields(PartSite.part)

    sql_db_generator.create_sqlite_index_from_fields(QuotePrice.quote_line_no)

    sql_db_generator.create_sqlite_index_from_fields(QuoteLine.part, QuoteLine.customer_part_id)
    sql_db_generator.create_sqlite_index_from_fields(
        QuoteLine.workorder_type, QuoteLine.workorder_base_id, QuoteLine.workorder_sub_id, QuoteLine.workorder_split_id,
        QuoteLine.workorder_lot_id)

    sql_db_generator.create_sqlite_index_from_fields(
        DemandSupplyLink.demand_type, DemandSupplyLink.supply_type, DemandSupplyLink.supply_base_id,
        DemandSupplyLink.supply_lot_id, DemandSupplyLink.supply_split_id, DemandSupplyLink.supply_sub_id)

    sql_db_generator.create_sqlite_index_from_fields(CustOrderLine.cust_order, CustOrderLine.line_no)

    sql_db_generator.create_sqlite_index_from_fields(
        Operation.workorder_type, Operation.workorder_base, Operation.workorder_sub, Operation.workorder_split,
        Operation.workorder_lot)

    sql_db_generator.create_sqlite_index_from_fields(
        Requirement.workorder_type, Requirement.workorder_base, Requirement.workorder_sub, Requirement.workorder_split,
        Requirement.workorder_lot)
