import jobboss.models as jb
from typing import Union, List
from baseintegration.utils import logger
from baseintegration.utils.repeat_work_objects import Header, Operation, RequiredMaterials, Child, MethodOfManufacture
from baseintegration.utils.sqlite_models import SQLiteDBGenerator, DataManager
from collections import namedtuple


class RepeatPartUtilObject:
    def __init__(self, jb_quotes_queryset, jb_jobs_queryset, jb_quote_hardware_queryset, jb_job_hardware_queryset):
        self.jb_quotes_queryset = jb_quotes_queryset
        self.jb_jobs_queryset = jb_jobs_queryset
        self.jb_quote_hardware_queryset = jb_quote_hardware_queryset
        self.jb_job_hardware_queryset = jb_job_hardware_queryset
        self.origin_jb_part = self.set_origin_jb_part()
        self.repeat_part = None
        self.rfq_utils = []
        self.job_utils = []
        self.quote_mom_utils = []
        self.job_mom_utils = []

    def set_origin_jb_part(self):
        if len(self.jb_quotes_queryset) > 0:
            return self.jb_quotes_queryset[0]
        elif len(self.jb_jobs_queryset) > 0:
            return self.jb_jobs_queryset[0]
        elif len(self.jb_quote_hardware_queryset) > 0:
            return self.jb_quote_hardware_queryset[0]
        elif len(self.jb_job_hardware_queryset) > 0:
            return self.jb_job_hardware_queryset[0]
        else:
            return None


class RfqUtil:
    def __init__(self, jb_rfq: jb.Rfq):
        self.jb_rfq: jb.Rfq = jb_rfq
        self.repeat_part_headers: List[Header] = []
        self.jb_quotes: List[jb.Quote] = []


class JobUtil:
    def __init__(self, jb_job, repeat_part_header):
        self.jb_job: jb.Job = jb_job
        self.repeat_part_header: Header = repeat_part_header


class QuoteMOMUtil:
    def __init__(self, jb_quote, jb_quote_qty, mom):
        self.jb_quote = jb_quote
        self.mom: MethodOfManufacture = mom
        self.jb_quote_qty: jb.QuoteQty = jb_quote_qty
        self.operations: List[Operation] = []
        self.required_materials: List[RequiredMaterials] = []
        self.children: List[Child] = []


class JobMOMUtil:
    def __init__(self, jb_job, mom):
        self.jb_job: jb.Job = jb_job
        self.mom: MethodOfManufacture = mom
        self.operations: List[Operation] = []
        self.required_materials: List[RequiredMaterials] = []
        self.children: List[Child] = []


QuantityNode = namedtuple("QuantityNode", "qty_per_parent parent_qty")


def get_repeat_part_type_from_jb_quote_or_job(jb_object: Union[jb.Quote, jb.Job]):
    if jb_object.type == "Assembly":
        return "assembled"
    return "manufactured"


def get_jb_contact_names(jb_contact: Union[jb.Contact, None]):
    if jb_contact is not None:
        first_name = "FIRST_NAME"
        last_name = "LAST_NAME"
        full_name = jb_contact.contact_name
        if full_name:
            fragments = full_name.split(' ')
            if len(fragments) > 0:
                first_name = fragments[0]
            if len(fragments) > 1:
                last_name = ' '.join(fragments[1:])
        return first_name, last_name
    logger.info("Contact is not assigned.")
    return None, None


def get_quote_erp_code(jb_quote: jb.Quote) -> str:
    root_comp_line_number = jb_quote.line
    if jb_quote.assembly_level > 0:
        try:
            root_component = jb.Quote.objects.filter(quote=jb_quote.top_lvl_quote).first()
            root_comp_line_number = root_component.line
        except Exception as e:
            logger.info(
                f"Could not find root component for this quote. This quote assembly may be corrupt.\n"
                f"Assigning the non-root quote line number instead - (NOTE: This may cause this part to fail to"
                f"import due to a non-matching <RFQ#>-<Line#> combination. {e}"
            )
    return f"{jb_quote.rfq}-{root_comp_line_number}"


def convert_to_string_if_not_null(value):
    if value is not None:
        return str(value)
    return None


def get_empty_string_if_none(value):
    if value is not None:
        return str(value)
    return ""


def create_all_sqlite_tables_if_not_exists():
    # Instantiate SQLite db generator. Configure SQLite DB. Create models.
    sql_db_generator = SQLiteDBGenerator("jobboss")
    sql_db_generator.configure_db_connections()
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Customer", "Customer")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Contact", "Contact")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Work_Center", "Work_Center")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Vendor", "Vendor")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Material", "Material")
    # NOTE: For some reason, only the "PAPERLESS" customer is causing an error in the import...
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Rfq", "Rfq")
    sql_db_generator.create_sqlite_table_from_sql_server_schema(
        "Quote",
        "Quote",
        "Rfq",
        "Rfq",
        "Rfq"
    )
    sql_db_generator.create_sqlite_table_from_sql_server_schema(
        "Bill_Of_Quotes",
        "Bill_Of_Quotes",
        "Component_Quote",
        "Quote",
        "Quote"
    )
    sql_db_generator.create_sqlite_table_from_sql_server_schema(
        "Quote_Qty",
        "Quote_QtyKey",
        "Quote",
        "Quote",
        "Quote"
    )
    sql_db_generator.create_sqlite_table_from_sql_server_schema(
        "Quote_Operation",
        "Quote_OperationKey",
        "Quote",
        "Quote",
        "Quote"
    )
    sql_db_generator.create_sqlite_table_from_sql_server_schema(
        "Quote_Operation_Qty",
        "Quote_Operation_QtyKey",
        "Quote_Operation",
        "Quote_Operation",
        "Quote_Operation"
    )
    sql_db_generator.create_sqlite_table_from_sql_server_schema(
        "Quote_Req",
        "Quote_ReqKey",
        "Quote",
        "Quote",
        "Quote"
    )
    sql_db_generator.create_sqlite_table_from_sql_server_schema(
        "Quote_Req_Qty",
        "Quote_Req_QtyKey",
        "Quote_Req",
        "Quote_Req",
        "Quote_Req"
    )
    sql_db_generator.create_sqlite_table_from_sql_server_schema(
        "Quote_Addl_Charge",
        "Quote_Addle_ChargeKey",
        "Quote",
        "Quote",
        "Quote"
    )
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Job", "Job")
    sql_db_generator.create_sqlite_table_from_sql_server_schema(
        "Bill_Of_Jobs",
        "Object_Id",
        "Component_Job",
        "Job",
        "Job"
    )
    sql_db_generator.create_sqlite_table_from_sql_server_schema(
        "Job_Operation",
        "Job_OperationKey",
        "Job",
        "Job",
        "Job"
    )
    sql_db_generator.create_sqlite_table_from_sql_server_schema(
        "Material_Req",
        "Material_ReqKey",
        "Job",
        "Job",
        "Job"
    )
    sql_db_generator.create_sqlite_table_from_sql_server_schema(
        "Additional_Charge",
        "Additional_ChargeKey",
        "Job",
        "Job",
        "Job"
    )


def insert_data_into_all_sqlite_tables():
    # Select data for each model, insert data into SQLite models
    data_manager = DataManager("jobboss")
    data_manager.configure_db_connections()
    # General
    data_manager.select_data_in_chunks("Customer", "Customer")
    data_manager.select_data_in_chunks("Contact", "Contact")
    data_manager.select_data_in_chunks("Work_Center", "Work_Center")
    data_manager.select_data_in_chunks("Vendor", "Vendor")
    data_manager.select_data_in_chunks("Material", "Material")

    # Quote-related
    data_manager.select_data_in_chunks("Rfq", "Rfq")
    data_manager.select_data_in_chunks("Quote", "Quote")
    data_manager.select_data_in_chunks("Bill_Of_Quotes", "Component_Quote")
    data_manager.select_data_in_chunks("Quote_Qty", "Quote_QtyKey")
    data_manager.select_data_in_chunks("Quote_Operation", "Quote_OperationKey")
    data_manager.select_data_in_chunks("Quote_Operation_Qty", "Quote_Operation_QtyKey")
    data_manager.select_data_in_chunks("Quote_Req", "Quote_Req")
    data_manager.select_data_in_chunks("Quote_Req_Qty", "Quote_Req_QtyKey")
    data_manager.select_data_in_chunks("Quote_Addl_Charge", "Quote_Addl_ChargeKey")

    # Job-related
    data_manager.select_data_in_chunks("Job", "Job")
    data_manager.select_data_in_chunks("Bill_Of_Jobs", "Component_Job")
    data_manager.select_data_in_chunks("Job_Operation", "Job_OperationKey")
    data_manager.select_data_in_chunks("Material_Req", "Material_ReqKey")
    data_manager.select_data_in_chunks("Additional_Charge", "Additional_ChargeKey")


def create_indexes_on_all_sqlite_tables():
    # Instantiate SQLite db generator. Configure SQLite DB. Create models.
    sql_db_generator = SQLiteDBGenerator("jobboss")
    sql_db_generator.configure_db_connections()
    # Create SQLite quote indexes
    sql_db_generator.create_sqlite_index("quote_id_qty", "Quote_Qty", "quote")
    sql_db_generator.create_sqlite_index("quote_id_op", "Quote_Operation", "quote")
    sql_db_generator.create_sqlite_index("quote_id_op_qty", "Quote_Operation_Qty", "quote_operation")
    sql_db_generator.create_sqlite_index("quote_id_req", "Quote_Req", "quote")
    sql_db_generator.create_sqlite_index("quote_id_req_qty", "Quote_Req_Qty", "quote")
    sql_db_generator.create_sqlite_index("quote_id_adll", "Quote_Addl_Charge", "quote")

    # Create SQLite job indexes
    sql_db_generator.create_sqlite_index("job_id_op", "Job_Operation", "job")
    sql_db_generator.create_sqlite_index("job_id_mat", "Material_Req", "job")
    sql_db_generator.create_sqlite_index("job_id_addl", "Additional_Charge", "job")


# Defines all shop operation variables for both jobs and quotes
SHOP_OP_COSTING_VARS = {
    "operation_service": ("operation_service", str),
    "setup_time": ("setup_time", float),  # Note: This will always be zero due to fixed hrs units. P3L will assign
    "runtime": ("runtime", float),  # Note: This will always be zero due to fixed hrs units. P3L will assign
    "est_setup_hrs": ("est_setup_hrs", float),
    "est_run_per_part": ("est_run_per_part", float),
    "inside_oper": ("inside_oper", float),
    "name": ("name", str),
    "est_setup_labor": ("est_setup_labor", float),
    "est_run_labor": ("est_run_labor", float),
    "est_labor_burden": ("est_labor_burden", float),
    "est_machine_burden": ("est_machine_burden", float),
    "est_ga_burden": ("est_ga_burden", float),
    "attended_pct": ("attended_pct", float),
    "efficiency_pct": ("efficiency_pct", float),
    "lead_days": ("lead_days", float),
    "est_required_qty": ("est_required_qty", float),
    "est_unit_cost": ("est_unit_cost", float),
    "minimum_chg_amt": ("minimum_chg_amt", float),
    "est_total_cost": ("est_total_cost", float),
    "run_labor_rate": ("run_labor_rate", float),
    "setup_labor_rate": ("setup_labor_rate", float),
    "run_labor_burden_rate": ("run_labor_burden_rate", float),
    "setup_labor_burden_rate": ("setup_labor_burden_rate", float),
    "machine_burden_rate": ("machine_burden_rate", float),
    "ga_burden_rate": ("ga_burden_rate", float),
    "run_method": ("run_method", str)
}

# Defines all material operation variables for jobs and quotes
MATERIAL_OP_COSTING_VARS = {
    "material": ("material", str),
    "quantity_per_basis": ("quantity_per_basis", str),
    "quantity_per": ("quantity_per", float),
    "uofm": ("uofm", "ea"),
    "est_qty": ("est_qty", float),
    "est_unit_cost": ("est_unit_cost", float),
    "est_addl_cost": ("est_addl_cost", float),  # This field only applies to type "M" materials
    "est_total_cost": ("est_total_cost", float),
    "part_length": ("part_length", float),
    "part_width": ("part_width", float),
    "bar_end": ("bar_end", float),
    "cutoff": ("cutoff", float),
    "facing": ("facing", float),
    "bar_length": ("bar_length", float),
    "lead_days": ("lead_days", float),
    "cost_uofm": ("cost_uofm", "ea"),
    "cost_unit_conv": ("cost_unit_conv", float),
    "quantity_multiplier": ("quantity_multiplier", float),
    "rounded": ("rounded", float),
    "sheet_density": ("sheet_density", float),
    "sheet_cost_per_lb": ("sheet_cost_per_lb", float),  # Does this variable even do anything?
    "sheet_cost": ("sheet_cost", float),
}

MATERIAL_MASTER_COSTING_VARS = {
    "sheet_length": ("is_length", float),
    "sheet_width": ("is_width", float),
    "sheet_thickness": ("is_thickness", float),
    "last_cost": ("last_cost", float),
    "standard_cost": ("standard_cost", float),
    "average_cost": ("average_cost", float)
}

MARKUP_CATEGORIES = (
    "profit_pct",
    "labor_markup_pct",
    "mat_markup_pct",
    "serv_markup_pct",
    "labor_burden_markup_pct",
    "machine_burden_markup_pct",
    "ga_burden_markup_pct"
)
