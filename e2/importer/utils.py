from typing import List, Optional

from baseintegration.utils.repeat_work_objects import Part as RepeatPart, MethodOfManufacture
from baseintegration.utils.sqlite_models import SQLiteDBGenerator
from e2.models import (
    Estim,
    JobReq,
    Quotedet,
    Releases,
    Quote,
    Materials,
    OrderDet,
    OrderRouting,
    Routing,
    Workcntr,
    Order,
    CustomerCode,
    Contacts
)
from baseintegration.datamigration import logger

ESTIM_NUM_PRICES = 8


class RepeatPartUtilObject:

    def __init__(self, repeat_part: RepeatPart, e2_part: Estim):
        self.repeat_part: RepeatPart = repeat_part
        self.e2_part: Estim = e2_part
        self.job_mom_utils: List[JobMOMUtil] = []
        self.quote_mom_utils: List[QuoteMOMUtil] = []
        self.template_mom_utils: List[TemplateMOMUtil] = []


class JobMOMUtil:

    def __init__(self, method_of_manufacture: MethodOfManufacture, type: str, erp_code: str,
                 order_detail: Optional[OrderDet] = None, job_requirement: Optional[JobReq] = None):
        self.method_of_manufacture: MethodOfManufacture = method_of_manufacture
        # either order_detail or job_requirement will have a value
        self.order_detail: Optional[OrderDet] = order_detail
        self.job_requirement: Optional[JobReq] = job_requirement
        self.type: str = type
        self.erp_code: str = erp_code


class QuoteMOMUtil:

    def __init__(self, method_of_manufacture: MethodOfManufacture, quote_detail: Quotedet, type: str, erp_code: str):
        self.method_of_manufacture: MethodOfManufacture = method_of_manufacture
        self.quote_detail: Quotedet = quote_detail
        self.type: str = type
        self.erp_code: str = erp_code


class TemplateMOMUtil:

    def __init__(self, method_of_manufacture: MethodOfManufacture, template: Estim, type: str, erp_code: str):
        self.method_of_manufacture: MethodOfManufacture = method_of_manufacture
        self.template: Estim = template
        self.type: str = type
        self.erp_code: str = erp_code


def get_quote_detail_erp_code(e2_quote_detail: Quotedet) -> str:
    erp_code = f"{e2_quote_detail.quoteno}-{e2_quote_detail.itemno}"
    return erp_code


def is_required_material_quantity(quantity: float) -> bool:
    if quantity is None:
        return False
    rounded_quantity = int(quantity)
    return abs(rounded_quantity - quantity) > 0.001


def iterate_job_requirements(source_database: str, job_mom_util: JobMOMUtil):
    job_reqs: List[JobReq] = JobReq.objects.using(source_database).filter(jobno=job_mom_util.order_detail.job_no)
    for job_req in job_reqs:
        estim: Estim = Estim.objects.using(source_database).filter(partno=job_req.partno).first()
        if not estim:
            logger.info(f"Job req with part number {job_req.partno} for parent {job_mom_util.order_detail.part_no} not found as an estim")
            continue
        yield job_req, estim


def iterate_child_order_dets(source_database: str, job_mom_util: JobMOMUtil):
    child_order_dets: List[OrderDet] = OrderDet.objects.using(source_database).filter(master_job_no=job_mom_util.order_detail.job_no)
    for child_order_det in child_order_dets:
        estim: Estim = Estim.objects.using(source_database).filter(partno=child_order_det.part_no).first()
        if not estim:
            logger.info(f"Child order det with part number {child_order_det.part_no} for parent {job_mom_util.order_detail.part_no} not found as an estim")
            continue
        yield child_order_det, estim


def iterate_template_materials(source_database: str, part_number: str):
    e2_materials: List[Materials] = Materials.objects.using(source_database).filter(partno=part_number)
    for e2_material in e2_materials:
        estim: Estim = Estim.objects.using(source_database).filter(partno=e2_material.subpartno).first()
        if not estim:
            logger.info(
                f"Material with part number {e2_material.subpartno} for parent {e2_material.partno} not found as an estim")
            continue
        yield e2_material, estim


ORDER_ROUTING_COSTING_VARIABLES = {
    "step_no": 0,
    "work_or_vend": 0,
    "work_cntr": "string",
    "vend_code": "string",
    "oper_code": "string",
    "cycle_time": 0,
    "mach_run": 0,
    "team_size": 0,
    "scrap_pct": 0,
    "pct_eff": 0,
    "labor_acct": "string",
    "setup_rate": 0,
    "cycle_rate": 0,
    "burden_rate": 0,
    "labor_rate": 0,
    "lead_time": 0,
    "markup_pct": 0,
    "cert_req": "string",
    "gl_code": "string",
    "setup_price": 0,
    "cycle_price": 0,
    "total": 0,
    "estim_qty": 0,
    "actual_pcs_good": 0,
    "actual_pcs_scrap": 0,
    "num_mach_for_job": 0,
    "status": "string",
    "empl_code": "string",
    "tot_est_hrs": 0,
    "tot_act_hrs": 0,
    "tot_hrs_left": 0,
    "dept_num": "string",
    "overlap": "string"
}


ROUTING_TO_ORDER_ROUTING_COSTING_VARIABLES = {
    "stepno": "step_no",
    "workorvend": "work_or_vend",
    "workcntr": "work_cntr",
    "vendcode": "vend_code",
    "opercode": "oper_code",
    "cycletime": "cycle_time",
    "machrun": "mach_run",
    "teamsize": "team_size",
    "scrappct": "scrap_pct",
    "pcteff": "pct_eff",
    "laboracct": "labor_acct",
    "setuprate": "setup_rate",
    "cyclerate": "cycle_rate",
    "burdenrate": "burden_rate",
    "laborrate": "labor_rate",
    "leadtime": "lead_time",
    "markuppct": "markup_pct",
    "certreq": "cert_req",
    "glcode": "gl_code",
    "setupprice": "setup_price",
    "cycleprice": "cycle_price",
    "total": "total",
    "estimqty": "estim_qty",
    "actualpiecesgood": "actual_pcs_good",
    "actualpiecesscrapped": "actual_pcs_scrap",
    "nummachforjob": "num_mach_for_job"
}


WORK_CENTER_COSTING_VARIABLES = {
    "hrsavail": 0,
    "defaulttimeunit": "string",
    "queue_time": 0,
    "defsetuptime": 0,
    "altopcode": 0,
    "attendcode": "string",
    "capacityfactor": 0,
    "active": "string",
    "locationtop": 0,
    "locationleft": 0,
    "loadingmethod": "string",
    "utilizationpct": 0
}


REQUIRED_MATERIAL_E2_MATERIAL_COSTING_VARIABLES = {
    "qty": 0,
    "unit": "string",
    "purchased": 0,
    "vendor": "string",
    "totalqty": 0,
    "unitcost": 0,
    "unitprice": 0,
    "totalcost": 0,
    "totalprice": 0,
    "totalwt": 0,
    "partwt": 0
}


REQUIRED_MATERIAL_JOB_REQ_COSTING_VARIABLES = {
    "qty": ("qty2buy", 0),
    "unit": ("pricingunit", "string"),
    "purchased": (None, 1),
    "vendor": ("vendcode", "string"),
    "totalqty": ("qtytobuy", 0),
    "unitcost": (None, 0),
    "unitprice": (None, 0),
    "totalcost": ("cost", 0),
    "totalprice": ("price", 0),
    "totalwt": (None, 0),
    "partwt": (None, 0)
}


REQUIRED_MATERIAL_ESTIM_COSTING_VARIABLES = {
    "prodcode": "string",
    "glcode": "string",
    "pricingunit": "string",
    "stockunit": "string",
    "qtyonhand": 0,
    "reordlevel": 0,
    "reordqty": 0,
    "qtyonres": 0,
    "leadtime": 0,
    "purchunit": "string",
    "purchfactor": 0,
    "stockingcost": 0,
    "qtyonorder": 0,
    "qtyoutside": 0,
    "active": "string"
}


def create_all_sqlite_tables_if_not_exists():
    # Instantiate SQLite db generator. Configure SQLite DB. Create models.
    sql_db_generator = SQLiteDBGenerator("e2")
    sql_db_generator.configure_db_connections()

    sql_db_generator.create_sqlite_table_from_model(Releases)
    sql_db_generator.create_sqlite_table_from_model(JobReq)
    sql_db_generator.create_sqlite_table_from_model(Quotedet)
    sql_db_generator.create_sqlite_table_from_model(Quote)
    sql_db_generator.create_sqlite_table_from_model(Estim)
    sql_db_generator.create_sqlite_table_from_model(Materials)
    sql_db_generator.create_sqlite_table_from_model(OrderDet)
    sql_db_generator.create_sqlite_table_from_model(OrderRouting)
    sql_db_generator.create_sqlite_table_from_model(Routing)
    sql_db_generator.create_sqlite_table_from_model(Workcntr)
    sql_db_generator.create_sqlite_table_from_model(Order)
    sql_db_generator.create_sqlite_table_from_model(CustomerCode)
    sql_db_generator.create_sqlite_table_from_model(Contacts)

    sql_db_generator.copy_data_to_sqlite()


def create_indexes_on_all_sqlite_tables():
    # Instantiate SQLite db generator. Configure SQLite DB. Create models.
    sql_db_generator = SQLiteDBGenerator("e2")
    sql_db_generator.configure_db_connections()

    sql_db_generator.create_sqlite_index_from_fields(Materials.partno)
    sql_db_generator.create_sqlite_index_from_fields(Materials.subpartno)
    sql_db_generator.create_sqlite_index_from_fields(Materials.partno, Materials.stepno)

    sql_db_generator.create_sqlite_index_from_fields(Estim.partno)

    sql_db_generator.create_sqlite_index_from_fields(Releases.orderno, Releases.jobno, Releases.partno)

    sql_db_generator.create_sqlite_index_from_fields(Order.order_no)

    sql_db_generator.create_sqlite_index_from_fields(Quote.quoteno)

    sql_db_generator.create_sqlite_index_from_fields(Contacts.code, Contacts.contact)
    sql_db_generator.create_sqlite_index_from_fields(Contacts.code)
    sql_db_generator.create_sqlite_index_from_fields(Contacts.contact)

    sql_db_generator.create_sqlite_index_from_fields(JobReq.partno)

    sql_db_generator.create_sqlite_index_from_fields(OrderDet.orderno, OrderDet.job_no, OrderDet.part_no)
    sql_db_generator.create_sqlite_index_from_fields(OrderDet.job_no, OrderDet.part_no, OrderDet.quote_no,
                                                     OrderDet.quote_item_no)

    sql_db_generator.create_sqlite_index_from_fields(Quotedet.partno)

    sql_db_generator.create_sqlite_index_from_fields(OrderRouting.order_no, OrderRouting.part_no, OrderRouting.job_no)
    sql_db_generator.create_sqlite_index_from_fields(OrderRouting.part_no, OrderRouting.job_no)

    sql_db_generator.create_sqlite_index_from_fields(Routing.partno)

    sql_db_generator.create_sqlite_index_from_fields(Workcntr.oldworkcntr)
