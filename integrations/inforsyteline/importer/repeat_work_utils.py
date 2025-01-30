from baseintegration.utils.sqlite_models import SQLiteDBGenerator
from inforsyteline.models import JobrouteMst, JobmatlMst, WcMst, CustomerMst, ItemMst, JobMst, CoitemMst, CustaddrMst, \
    ItempriceMst, JrtresourcegroupMst, JrtSchMst


def get_product_code(item: ItemMst, source_database: str = 'default'):
    # we need the line below to get the raw product_code value, since it is a foreign key in default_models but not in syteline_10_models
    return ItemMst.objects.using(source_database).filter(item=item.item).values_list('product_code', flat=True).first()


def get_operation_costing_variables(job_route: JobrouteMst, work_center: WcMst):
    return {
        "description": (work_center.description, str),
        "site_ref": (job_route.site_ref, str),
        "job": (job_route.job, str),
        "suffix": (job_route.suffix, float),
        "oper_num": (job_route.oper_num, float),
        "wc": (job_route.wc.wc, str),
        "setup_hrs_t": (job_route.setup_hrs_t, float),
        "setup_cost_t": (job_route.setup_cost_t, float),
        "complete": (job_route.complete, float),
        "setup_hrs_v": (job_route.setup_hrs_v, float),
        "wip_amt": (job_route.wip_amt, float),
        "qty_scrapped": (job_route.qty_scrapped, float),
        "qty_received": (job_route.qty_received, float),
        "qty_moved": (job_route.qty_moved, float),
        "qty_complete": (job_route.qty_complete, float),
        "effect_date": (job_route.effect_date, str),
        "obs_date": (job_route.obs_date, str),
        "bflush_type": (job_route.bflush_type, str),
        "run_basis_lbr": (job_route.run_basis_lbr, str),
        "run_basis_mch": (job_route.run_basis_mch, str),
        "fixovhd_t_lbr": (job_route.fixovhd_t_lbr, float),
        "fixovhd_t_mch": (job_route.fixovhd_t_mch, float),
        "varovhd_t_lbr": (job_route.varovhd_t_lbr, float),
        "varovhd_t_mch": (job_route.varovhd_t_mch, float),
        "run_hrs_t_lbr": (job_route.run_hrs_t_lbr, float),
        "run_hrs_t_mch": (job_route.run_hrs_t_mch, float),
        "run_hrs_v_lbr": (job_route.run_hrs_v_lbr, float),
        "run_hrs_v_mch": (job_route.run_hrs_v_mch, float),
        "run_cost_t_lbr": (job_route.run_cost_t_lbr, float),
        "cntrl_point": (job_route.cntrl_point, float),
        "setup_rate": (job_route.setup_rate, float),
        "efficiency": (job_route.efficiency, float),
        "fovhd_rate_mch": (job_route.fovhd_rate_mch, float),
        "vovhd_rate_mch": (job_route.vovhd_rate_mch, float),
        "run_rate_lbr": (job_route.run_rate_lbr, float),
        "varovhd_rate": (job_route.varovhd_rate, float),
        "fixovhd_rate": (job_route.fixovhd_rate, float),
        "wip_matl_amt": (job_route.wip_matl_amt, float),
        "wip_lbr_amt": (job_route.wip_lbr_amt, float),
        "wip_fovhd_amt": (job_route.wip_fovhd_amt, float),
        "wip_vovhd_amt": (job_route.wip_vovhd_amt, float),
        "wip_out_amt": (job_route.wip_out_amt, float),
        "noteexistsflag": (job_route.noteexistsflag, float),
        "recorddate": (job_route.recorddate, str),
        "rowpointer": (job_route.rowpointer, str),
        "createdby": (job_route.createdby, str),
        "updatedby": (job_route.updatedby, str),
        "createdate": (job_route.createdate, str),
        "inworkflow": (job_route.inworkflow, float),
        "yield_field": (job_route.yield_field, float),
        "opm_consec_oper": (job_route.opm_consec_oper, float),
        "mo_shared": (job_route.mo_shared, float),
        "mo_seconds_per_cycle": (job_route.mo_seconds_per_cycle, float),
        "mo_formula_matl_weight": (job_route.mo_formula_matl_weight, float),
        "mo_formula_matl_weight_units": (job_route.mo_formula_matl_weight_units, str),
    }


def get_material_costing_variables(job_material: JobmatlMst):
    return {
        "site_ref": (job_material.site_ref, str),
        "job": (job_material.job, str),
        "suffix": (job_material.suffix, float),
        "oper_num": (job_material.oper_num, float),
        "sequence": (job_material.sequence, float),
        "matl_type": (job_material.matl_type, str),
        "item": (job_material.item, str),
        "matl_qty": (job_material.matl_qty, float),
        "units": (job_material.units, str),
        "cost": (job_material.cost, float),
        "qty_issued": (job_material.qty_issued, float),
        "a_cost": (job_material.a_cost, float),
        "ref_type": (job_material.ref_type, str),
        "ref_num": (job_material.ref_num, str),
        "ref_line_suf": (job_material.ref_line_suf, float),
        "ref_release": (job_material.ref_release, float),
        "po_unit_cost": (job_material.po_unit_cost, float),
        "effect_date": (job_material.effect_date, str),
        "obs_date": (job_material.obs_date, str),
        "scrap_fact": (job_material.scrap_fact, float),
        "qty_var": (job_material.qty_var, float),
        "fixovhd_t": (job_material.fixovhd_t, float),
        "varovhd_t": (job_material.varovhd_t, float),
        "feature": (job_material.feature, str),
        "probable": (job_material.probable, float),
        "opt_code": (job_material.opt_code, str),
        "inc_price": (job_material.inc_price, float),
        "description": (job_material.description, str),
        "pick_date": (job_material.pick_date, str),
        "bom_seq": (job_material.bom_seq, float),
        "matl_qty_conv": (job_material.matl_qty_conv, float),
        "u_m": (job_material.u_m, str),
        "inc_price_conv": (job_material.inc_price_conv, float),
        "cost_conv": (job_material.cost_conv, float),
        "backflush": (job_material.backflush, float),
        "bflush_loc": (job_material.bflush_loc, str),
        "fmatlovhd": (job_material.fmatlovhd, float),
        "vmatlovhd": (job_material.vmatlovhd, float),
        "matl_cost": (job_material.matl_cost, float),
        "lbr_cost": (job_material.lbr_cost, float),
        "fovhd_cost": (job_material.fovhd_cost, float),
        "vovhd_cost": (job_material.vovhd_cost, float),
        "out_cost": (job_material.out_cost, float),
        "a_matl_cost": (job_material.a_matl_cost, float),
        "a_lbr_cost": (job_material.a_lbr_cost, float),
        "a_fovhd_cost": (job_material.a_fovhd_cost, float),
        "a_vovhd_cost": (job_material.a_vovhd_cost, float),
        "a_out_cost": (job_material.a_out_cost, float),
        "matl_cost_conv": (job_material.matl_cost_conv, float),
        "lbr_cost_conv": (job_material.lbr_cost_conv, float),
        "fovhd_cost_conv": (job_material.fovhd_cost_conv, float),
        "vovhd_cost_conv": (job_material.vovhd_cost_conv, float),
        "out_cost_conv": (job_material.out_cost_conv, float),
        "noteexistsflag": (job_material.noteexistsflag, float),
        "recorddate": (job_material.recorddate, str),
        "rowpointer": (job_material.rowpointer, str),
        "createdby": (job_material.createdby, str),
        "updatedby": (job_material.updatedby, str),
        "createdate": (job_material.createdate, str),
        "inworkflow": (job_material.inworkflow, float),
        "alt_group": (job_material.alt_group, float),
        "alt_group_rank": (job_material.alt_group_rank, float),
        "planned_alternate": (job_material.planned_alternate, float),
        "new_sequence": (job_material.new_sequence, float),
        "pp_matl_is_paper": (job_material.pp_matl_is_paper, float),
        "mo_formula_matl_weight_pct": (job_material.mo_formula_matl_weight_pct, float),
    }


def create_all_sqlite_tables_if_not_exists():
    # Instantiate SQLite db generator. Configure SQLite DB. Create models.
    sql_db_generator = SQLiteDBGenerator("inforsyteline")
    sql_db_generator.configure_db_connections()

    sql_db_generator.create_sqlite_table_from_model(CustomerMst)
    sql_db_generator.create_sqlite_table_from_model(CustaddrMst)
    sql_db_generator.create_sqlite_table_from_model(CoitemMst)
    sql_db_generator.create_sqlite_table_from_model(ItemMst)
    sql_db_generator.create_sqlite_table_from_model(ItempriceMst)
    sql_db_generator.create_sqlite_table_from_model(JobMst)
    sql_db_generator.create_sqlite_table_from_model(JobmatlMst)
    sql_db_generator.create_sqlite_table_from_model(JobrouteMst)
    sql_db_generator.create_sqlite_table_from_model(JrtresourcegroupMst)
    sql_db_generator.create_sqlite_table_from_model(JrtSchMst)
    sql_db_generator.create_sqlite_table_from_model(WcMst)

    sql_db_generator.copy_data_to_sqlite()


def create_indexes_on_all_sqlite_tables():
    # Instantiate SQLite db generator. Configure SQLite DB. Create models.
    sql_db_generator = SQLiteDBGenerator("inforsyteline")
    sql_db_generator.configure_db_connections()

    sql_db_generator.create_sqlite_index_from_fields(ItemMst.item)

    sql_db_generator.create_sqlite_index_from_fields(JobMst.type, JobMst.item)
    sql_db_generator.create_sqlite_index_from_fields(JobMst.type, JobMst.item, JobMst.mo_bom_alternate_id)
    sql_db_generator.create_sqlite_index_from_fields(JobMst.type, JobMst.job, JobMst.suffix)
    sql_db_generator.create_sqlite_index_from_fields(JobMst.type, JobMst.job, JobMst.suffix, JobMst.mo_bom_alternate_id)
    sql_db_generator.create_sqlite_index_from_fields(JobMst.job, JobMst.suffix)
    sql_db_generator.create_sqlite_index_from_fields(JobMst.item)
    sql_db_generator.create_sqlite_index_from_fields(JobMst.item, JobMst.ref_job)

    sql_db_generator.create_sqlite_index_from_fields(JobmatlMst.item)
    sql_db_generator.create_sqlite_index_from_fields(JobmatlMst.job, JobmatlMst.suffix)
    sql_db_generator.create_sqlite_index_from_fields(JobmatlMst.ref_type, JobmatlMst.ref_num, JobmatlMst.ref_line_suf)

    sql_db_generator.create_sqlite_index_from_fields(JobrouteMst.job, JobrouteMst.suffix)

    sql_db_generator.create_sqlite_index_from_fields(JrtSchMst.job, JrtSchMst.suffix, JrtSchMst.oper_num)

    sql_db_generator.create_sqlite_index_from_fields(JrtresourcegroupMst.job, JrtresourcegroupMst.suffix,
                                                     JrtresourcegroupMst.oper_num)

    sql_db_generator.create_sqlite_index_from_fields(ItempriceMst.item)

    sql_db_generator.create_sqlite_index_from_fields(CoitemMst.co_num, CoitemMst.co_line)
    sql_db_generator.create_sqlite_index_from_fields(CoitemMst.ref_type, CoitemMst.ref_num, CoitemMst.ref_line_suf)

    sql_db_generator.create_sqlite_index_from_fields(CustomerMst.cust_num)

    sql_db_generator.create_sqlite_index_from_fields(CustaddrMst.cust_num)
