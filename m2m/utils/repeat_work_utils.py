from dataclasses import dataclass
from decimal import Decimal
from typing import Union, Optional

from baseintegration.utils.sqlite_models import SQLiteDBGenerator, DataManager
from m2m.importer.processors.base import BaseM2MImportProcessor
from m2m.models import Qtitem, Qtdrtg, Inwork, Qtdbom, Inrtgs, Inboms, Inmastx, Jomast, Jodbom, Jodrtg, Inbomm

sql_cache = {}


@dataclass
class PartData:
    entry: Union[Inmastx, Qtitem, Jomast, Qtdbom, Jodbom]
    part_number: str
    revision: str

    def id(self) -> str:
        return f"{self.part_number.strip()} - {self.revision}"


@dataclass
class JobMaterialData:
    type: str
    quantity_per_parent: Decimal
    material_cost: Decimal


@dataclass
class JobData:
    quantity: int
    unit_price: Decimal
    total_price: Decimal


@dataclass
class TemplateRoot:
    item: Inmastx
    bom: Inbomm

    @property
    def pk(self):
        return self.item.pk, self.bom.pk


def get_estimated_erp_code(quote_item: Qtitem):
    quote_number = BaseM2MImportProcessor.generate_normalized_value(quote_item.fquoteno)
    quote_item_number = BaseM2MImportProcessor.generate_normalized_value(quote_item.fenumber)
    return f"{quote_number}-{quote_item_number}"


def matches_query(instance, query: dict):
    for k, v in query.items():
        if getattr(instance, k) != v:
            return False
    return True


def get_first_in_queryset(query_set, **query):
    results = [i for i in query_set if matches_query(i, query)]
    return results[0] if results else None


def get_first_cached(model, **query):
    table_name = model.__name__
    if table_name not in sql_cache:
        sql_cache[table_name] = model.objects.all()
    return get_first_in_queryset(sql_cache[table_name], **query)


def get_operation_costing_variables(routing_line: Union[Qtdrtg, Inrtgs, Jodrtg], work_center: Optional[Inwork]):
    return {
        "fchngrates": (routing_line.fchngrates, str),
        "felpstime": (routing_line.felpstime, float),
        "ffixcost": (routing_line.ffixcost, float),
        "flschedule": (routing_line.flschedule, bool),
        "fmovetime": (routing_line.fmovetime, float),
        "foperno": (routing_line.foperno, float),
        "foperqty": (routing_line.foperqty, float),
        "fothrcost": (routing_line.fothrcost, float),
        "fpro_id": (routing_line.fpro_id, str),
        "fsetuptime": (routing_line.fsetuptime, float),
        "fulabcost": (routing_line.fulabcost, float),
        "fuovrhdcos": (routing_line.fuovrhdcos, float),
        "fuprodtime": (routing_line.fuprodtime, float),
        "fusubcost": (routing_line.fusubcost, float),
        "fllotreqd": (routing_line.fllotreqd, bool),
        "identity_column": (routing_line.identity_column, str),
        "fopermemo": (routing_line.fopermemo, str),
        "fndbrmod": (routing_line.fndbrmod, float),
        "fnsimulops": (routing_line.fnsimulops, float),
        "cycleunits": (routing_line.cycleunits, float),
        "unitsize": (routing_line.unitsize, float),
        "fccharcode": (routing_line.fccharcode, str),
        **get_workcenter_costing_variables(work_center)
    }


def get_workcenter_costing_variables(work_center: Optional[Inwork]):
    if not work_center:
        return {}
    return {
        "fnavgwkhrs": (work_center.fnavgwkhrs, float),
        "fcpro_id": (work_center.fcpro_id, str),
        "fcpro_name": (work_center.fcpro_name, str),
        "fccomments": (work_center.fccomments, str),
        "fdept": (work_center.fdept, str),
        "flabcost": (work_center.flabcost, float),
        "fnavgque": (work_center.fnavgque, float),
        "fnmax1": (work_center.fnmax1, float),
        "fnmax2": (work_center.fnmax2, float),
        "fnmax3": (work_center.fnmax3, float),
        "fnmaxque": (work_center.fnmaxque, float),
        "fnpctutil": (work_center.fnpctutil, float),
        "fnqueallow": (work_center.fnqueallow, float),
        "fnstd1": (work_center.fnstd1, float),
        "fnstd2": (work_center.fnstd2, float),
        "fnstd3": (work_center.fnstd3, float),
        "fnstd_prod": (work_center.fnstd_prod, float),
        "fnstd_set": (work_center.fnstd_set, float),
        "fnsumdur": (work_center.fnsumdur, float),
        "fovrhdcost": (work_center.fovrhdcost, float),
        "fscheduled": (work_center.fscheduled, str),
        "fspandays": (work_center.fnpque, float),
        "flconstrnt": (work_center.flconstrnt, bool),
        "fac": (work_center.fac, str),
        "fcstdormax": (work_center.fcstdormax, str),
        "fnloadcapc": (work_center.fnloadcapc, float),
        "fnmaxcapload": (work_center.fnmaxcapload, float),
        "flaltset": (work_center.flaltset, bool),
        "fcsyncmisc": (work_center.fcsyncmisc, str),
        "queuehrs": (work_center.queuehrs, float),
        "constbuff": (work_center.constbuff, float),
        "resgroup": (work_center.resgroup, str),
        "flbflabor": (work_center.flbflabor, bool),
        "simopstype": (work_center.simopstype, str),
        "size": (work_center.size, float),
        "canbreak": (work_center.canbreak, bool),
        "sizeum": (work_center.sizeum, str),
        "timefence": (work_center.timefence, float),
        "fcgroup": (work_center.fcgroup, str),
        "fracsimops": (work_center.fracsimops, bool)
    }


def get_estimated_quote_material_costing_variables(bom_line: Qtdbom):
    return {
        "fbompart": (bom_line.fbompart, str),
        "fbomrev": (bom_line.fbomrev, str),
        "fbominum": (bom_line.fbominum, str),
        "fbommeas": (bom_line.fbommeas, str),
        "fbomsource": (bom_line.fbomsource, str),
        "ffixcost": (bom_line.ffixcost, float),
        "fitem": (bom_line.fitem, str),
        "flabcost": (bom_line.flabcost, float),
        "flextend": (bom_line.flextend, bool),
        "fltooling": (bom_line.fltooling, bool),
        "fmatlcost": (bom_line.fmatlcost, float),
        "forgbomqty": (bom_line.forgbomqty, float),
        "fovhdcost": (bom_line.fovhdcost, float),
        "ftotqty": (bom_line.ftotqty, float),
        "fuprice": (bom_line.fuprice, float),
        "fllotreqd": (bom_line.fllotreqd, bool),
        "fclotext": (bom_line.fclotext, str),
        "fnoperno": (bom_line.fnoperno, float),
        "identity_column": (bom_line.identity_column, str),
        "fbomdesc": (bom_line.fbomdesc, str),
        "fstdmemo": (bom_line.fstdmemo, str),
        "fac": (bom_line.fac, str),
        "fcbomudrev": (bom_line.fcbomudrev, str),
        "fndbrmod": (bom_line.fndbrmod, float),
        "flrfqreqd": (bom_line.flrfqreqd, bool),
        "fcsource": (bom_line.fcsource, str)
    }


def get_estimated_standard_material_costing_variables(bom_line: Inboms, item: Inmastx):
    return {
        "fbompart": (bom_line.fcomponent, str),
        "fbomrev": (bom_line.fcomprev, str),
        "fbominum": (bom_line.fitem, str),
        "fbommeas": (item.fmeasure, str),
        "fbomsource": (item.fsource, str),
        "ffixcost": (item.itcfixed, float),
        "fitem": (bom_line.fitem, str),
        "flabcost": (item.flabcost, float),
        "flextend": (bom_line.flextend, bool),
        "fltooling": (bom_line.fltooling, bool),
        "fmatlcost": (item.fmatlcost, float),
        "forgbomqty": (bom_line.forigqty, float),
        "fovhdcost": (item.fovhdcost, float),
        "ftotqty": (bom_line.fqty, float),
        "fuprice": (item.fprice, float),
        "fllotreqd": (item.fllotreqd, bool),
        "fclotext": (item.fclotext, str),
        "fnoperno": (bom_line.fnoperno, float),
        "identity_column": (bom_line.identity_column, str),
        "fbomdesc": (item.fdescript, str),
        "fstdmemo": (bom_line.fbommemo, str),
        "fac": (bom_line.cfacilityid, str),
        "fcbomudrev": (bom_line.fcompudrev, str),
        "fndbrmod": (bom_line.fndbrmod, float),
        "flrfqreqd": (bom_line.freqd, str),
        "fcsource": (bom_line.fcsource, str)
    }


def get_engineered_material_costing_variables(bom_line: Jodbom):
    return {
        "fbompart": (bom_line.fbompart, str),
        "fbomrev": (bom_line.fbomrev, str),
        "fbominum": (bom_line.fbominum, str),
        "fbommeas": (bom_line.fbommeas, str),
        "fbomsource": (bom_line.fbomsource, str),
        "ffixcost": (bom_line.ffixcost, float),
        "fitem": (bom_line.fitem, str),
        "flabcost": (bom_line.flabcost, float),
        "flextend": (bom_line.flextend, bool),
        "fltooling": (bom_line.fltooling, bool),
        "fmatlcost": (bom_line.fmatlcost, float),
        "forgbomqty": (bom_line.forigqty, float),
        "fovhdcost": (bom_line.fovrhdcost, float),
        "ftotqty": (bom_line.ftotqty, float),
        "fuprice": (0, float),
        "fllotreqd": (bom_line.fllotreqd, bool),
        "fclotext": (bom_line.fclotext, str),
        "fnoperno": (bom_line.fnoperno, float),
        "identity_column": (bom_line.identity_column, str),
        "fbomdesc": (bom_line.fbomdesc, str),
        "fstdmemo": (bom_line.fstdmemo, str),
        "fac": (bom_line.cfac, str),
        "fcbomudrev": (bom_line.fcbomudrev, str),
        "fndbrmod": (bom_line.fndbrmod, float),
        "flrfqreqd": (bom_line.freqd, str),
        "fcsource": (bom_line.fcsource, str)
    }


def create_all_sqlite_tables_if_not_exists():
    # Instantiate SQLite db generator. Configure SQLite DB. Create models.
    sql_db_generator = SQLiteDBGenerator("m2m")
    sql_db_generator.configure_db_connections()

    # Customer-related
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Slcdpmx", "identity_column")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Syphon", "identity_column")

    # Item-related
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Inwork", "identity_column")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Inboms", "identity_column")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Inbomm", "identity_column")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Inrtgs", "identity_column")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Inmastx", "identity_column")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Inmast_Ext", "identity_column")

    # Quote-related
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Qtmast", "identity_column")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Qtitem", "identity_column")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Qtpest", "identity_column")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Qtdbom", "identity_column")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Qtdrtg", "identity_column")

    # Sales order-related
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Somast", "identity_column")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Sorels", "identity_column")

    # Job-related
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Jomast", "identity_column")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Joitem", "identity_column")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Jodbom", "identity_column")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Jodrtg", "identity_column")

    # TODO: the below view is too expensive to query
    # sql_db_generator.create_sqlite_table_from_sql_server_schema("Ma_Jobmaterialsummary", "")
    sql_db_generator.create_sqlite_table_from_sql_server_schema("Ma_Joblaborsummary", "")


def insert_data_into_all_sqlite_tables():
    # Select data for each model, insert data into SQLite models
    data_manager = DataManager("m2m")
    data_manager.configure_db_connections()

    # Customer-related
    data_manager.select_data_in_chunks("Slcdpmx", "identity_column")
    data_manager.select_data_in_chunks("Syphon", "identity_column")

    # Item-related
    data_manager.select_data_in_chunks("Inwork", "identity_column")
    data_manager.select_data_in_chunks("Inboms", "identity_column")
    data_manager.select_data_in_chunks("Inbomm", "identity_column")
    data_manager.select_data_in_chunks("Inrtgs", "identity_column")
    data_manager.select_data_in_chunks("Inmastx", "identity_column")
    data_manager.select_data_in_chunks("Inmast_Ext", "identity_column")

    # Quote-related
    data_manager.select_data_in_chunks("Qtmast", "identity_column")
    data_manager.select_data_in_chunks("Qtitem", "identity_column")
    data_manager.select_data_in_chunks("Qtpest", "identity_column")
    data_manager.select_data_in_chunks("Qtdbom", "identity_column")
    data_manager.select_data_in_chunks("Qtdrtg", "identity_column")

    # Sales order-related
    data_manager.select_data_in_chunks("Somast", "identity_column")
    data_manager.select_data_in_chunks("Sorels", "identity_column")

    # Job-related
    data_manager.select_data_in_chunks("Jomast", "identity_column")
    data_manager.select_data_in_chunks("Joitem", "identity_column")
    data_manager.select_data_in_chunks("Jodbom", "identity_column")
    data_manager.select_data_in_chunks("Jodrtg", "identity_column")

    # TODO: the below view is too expensive to query
    # data_manager.select_data_in_chunks("Ma_Jobmaterialsummary", "jobno")
    data_manager.select_data_in_chunks("Ma_Joblaborsummary", "jobno")


def create_indexes_on_all_sqlite_tables():
    # Instantiate SQLite db generator. Configure SQLite DB. Create models.
    sql_db_generator = SQLiteDBGenerator("m2m")
    sql_db_generator.configure_db_connections()

    # Create SQLite item indexes
    sql_db_generator.create_sqlite_index("item_part_and_rev", "Inmastx", "fpartno, frev")
    sql_db_generator.create_sqlite_index("standard_bom_part_and_rev", "Inboms", "fcomponent, fcomprev")
    sql_db_generator.create_sqlite_index("standard_bom_parent_and_rev", "Inboms", "fparent, fparentrev")
    sql_db_generator.create_sqlite_index("standard_bom_header_part_and_rev", "Inbomm", "fpartno, fcpartrev")
    sql_db_generator.create_sqlite_index("standard_routing_part_and_rev", "Inrtgs", "fpartno, fcpartrev")

    # Create SQLite quote indexes
    sql_db_generator.create_sqlite_index("quote_item_part_and_rev", "Qtitem", "fpartno, fpartrev")
    sql_db_generator.create_sqlite_index("quote_item_part_rev_and_standpart", "Qtitem", "fpartno, fpartrev, fstandpart")
    sql_db_generator.create_sqlite_index("quote_item_quote_and_number", "Qtitem", "fquoteno, finumber")
    sql_db_generator.create_sqlite_index("quote_number", "Qtmast", "fquoteno")
    sql_db_generator.create_sqlite_index("quote_bom_part_and_rev", "Qtdbom", "fbompart, fbomrev")
    sql_db_generator.create_sqlite_index("quote_bom_quote_number_and_parent", "Qtdbom", "fquoteno, finumber, fparinum")
    sql_db_generator.create_sqlite_index("quote_routing_quote_number_and_bom_number", "Qtdrtg",
                                         "fquoteno, finumber, fbominum")
    sql_db_generator.create_sqlite_index("quote_quantity_quote_and_number", "Qtpest", "fquoteno, fenumber")

    # Create SQLite job indexes
    sql_db_generator.create_sqlite_index("sales_order_number", "Somast", "fsono")
    sql_db_generator.create_sqlite_index("sales_order_so_number_item_number", "Sorels", "fsono, finumber")
    sql_db_generator.create_sqlite_index("job_job_number", "Jomast", "fjobno")
    sql_db_generator.create_sqlite_index("job_part_and_rev", "Jomast", "fpartno, fpartrev")
    sql_db_generator.create_sqlite_index("job_part_and_rev_and_type", "Jomast", "fpartno, fpartrev, ftype")
    sql_db_generator.create_sqlite_index("job_part_rev_type_and_status", "Jomast", "fpartno, fpartrev, ftype, fstatus")
    sql_db_generator.create_sqlite_index("job_item_part_rev", "Joitem", "fpartno, fpartrev")
    sql_db_generator.create_sqlite_index("job_bom_job_number", "Jodbom", "fjobno")
    sql_db_generator.create_sqlite_index("job_bom_part_and_rev", "Jodbom", "fbompart, fbomrev")
    sql_db_generator.create_sqlite_index("job_routing_job_number", "Jodrtg", "fjobno")
    sql_db_generator.create_sqlite_index("job_labor_job_number", "MA_JobLaborSummary", "jobno")
