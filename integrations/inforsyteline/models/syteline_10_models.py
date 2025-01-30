from django.db import models
from inforsyteline.settings import IS_TEST
from baseintegration.utils.truncated_model import TruncatedModel


class CoMst(TruncatedModel):
    site_ref = models.ForeignKey('TermsMst', models.DO_NOTHING, db_column='site_ref')
    type = models.CharField(max_length=1, blank=True, null=True)
    co_num = models.CharField(primary_key=True, max_length=10)
    est_num = models.CharField(max_length=10, blank=True, null=True)
    cust_num = models.ForeignKey('CustomerMst', models.DO_NOTHING, db_column='cust_num', blank=True, null=True)
    cust_seq = models.ForeignKey('CustomerMst', models.DO_NOTHING, db_column='cust_seq', blank=True, null=True)
    contact = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    cust_po = models.CharField(max_length=25, blank=True, null=True)
    order_date = models.DateTimeField()
    taken_by = models.CharField(max_length=15, blank=True, null=True)
    terms_code = models.ForeignKey('TermsMst', models.DO_NOTHING, db_column='terms_code', blank=True, null=True)
    ship_code = models.ForeignKey('ShipcodeMst', models.DO_NOTHING, db_column='ship_code', blank=True, null=True)
    price = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    weight = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    qty_packages = models.SmallIntegerField(blank=True, null=True)
    freight = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    misc_charges = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    prepaid_amt = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    sales_tax = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    stat = models.CharField(max_length=1, blank=True, null=True)
    cost = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)
    freight_t = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    m_charges_t = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    prepaid_t = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    sales_tax_t = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    eff_date = models.DateTimeField(blank=True, null=True)
    exp_date = models.DateTimeField(blank=True, null=True)
    whse = models.CharField(max_length=4, blank=True, null=True)
    sales_tax_2 = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    sales_tax_t2 = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    edi_order = models.SmallIntegerField(blank=True, null=True)
    process_ind = models.CharField(max_length=1, blank=True, null=True)
    use_exch_rate = models.SmallIntegerField(blank=True, null=True)
    tax_code1 = models.CharField(max_length=6, blank=True, null=True)
    tax_code2 = models.CharField(max_length=6, blank=True, null=True)
    frt_tax_code1 = models.CharField(max_length=6, blank=True, null=True)
    frt_tax_code2 = models.CharField(max_length=6, blank=True, null=True)
    msc_tax_code1 = models.CharField(max_length=6, blank=True, null=True)
    msc_tax_code2 = models.CharField(max_length=6, blank=True, null=True)
    discount_type = models.CharField(max_length=1, blank=True, null=True)
    disc_amount = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    disc = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    ship_partial = models.SmallIntegerField(blank=True, null=True)
    ship_early = models.SmallIntegerField(blank=True, null=True)
    matl_cost_t = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    lbr_cost_t = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    fovhd_cost_t = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    vovhd_cost_t = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    out_cost_t = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    exch_rate = models.DecimalField(max_digits=12, decimal_places=7, blank=True, null=True)
    fixed_rate = models.SmallIntegerField(blank=True, null=True)
    orig_site = models.CharField(max_length=8, blank=True, null=True)
    lcr_num = models.CharField(max_length=20, blank=True, null=True)
    edi_type = models.CharField(max_length=1, blank=True, null=True)
    invoiced = models.SmallIntegerField(blank=True, null=True)
    credit_hold = models.SmallIntegerField(blank=True, null=True)
    credit_hold_date = models.DateTimeField(blank=True, null=True)
    credit_hold_reason = models.CharField(max_length=3, blank=True, null=True)
    credit_hold_user = models.CharField(max_length=3, blank=True, null=True)
    sync_reqd = models.SmallIntegerField(blank=True, null=True)
    projected_date = models.DateTimeField(blank=True, null=True)
    order_source = models.CharField(max_length=8, blank=True, null=True)
    convert_type = models.CharField(max_length=1, blank=True, null=True)
    aps_pull_up = models.SmallIntegerField(blank=True, null=True)
    consolidate = models.SmallIntegerField(blank=True, null=True)
    inv_freq = models.CharField(max_length=1, blank=True, null=True)
    summarize = models.SmallIntegerField(blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    einvoice = models.SmallIntegerField(blank=True, null=True)
    charfld1 = models.CharField(max_length=20, blank=True, null=True)
    charfld2 = models.CharField(max_length=20, blank=True, null=True)
    charfld3 = models.CharField(max_length=20, blank=True, null=True)
    datefld = models.DateTimeField(blank=True, null=True)
    decifld1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    decifld2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    decifld3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    logifld = models.SmallIntegerField(blank=True, null=True)
    ack_stat = models.CharField(max_length=1, blank=True, null=True)
    config_id = models.CharField(max_length=12, blank=True, null=True)
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    include_tax_in_price = models.SmallIntegerField(blank=True, null=True)
    apply_to_inv_num = models.CharField(max_length=12, blank=True, null=True)
    export_type = models.CharField(max_length=1)
    external_confirmation_ref = models.CharField(max_length=80, blank=True, null=True)
    is_external = models.SmallIntegerField()
    days_shipped_before_due_date_tolerance = models.SmallIntegerField(blank=True, null=True)
    days_shipped_after_due_date_tolerance = models.SmallIntegerField(blank=True, null=True)
    shipped_over_ordered_qty_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    shipped_under_ordered_qty_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    consignment = models.SmallIntegerField()
    priority = models.SmallIntegerField(blank=True, null=True)
    demanding_site = models.CharField(max_length=8, blank=True, null=True)
    demanding_site_po_num = models.CharField(max_length=10, blank=True, null=True)
    shipment_approval_required = models.SmallIntegerField()
    portal_order = models.SmallIntegerField()
    ship_hold = models.SmallIntegerField()
    payment_method = models.CharField(max_length=1)
    surcharge = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    surcharge_t = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    config_doc_id = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        managed = IS_TEST
        db_table = 'co_mst'
        unique_together = (('credit_hold', 'cust_num', 'co_num', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('cust_num', 'co_num', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('cust_num', 'lcr_num', 'co_num', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('rowpointer', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('sync_reqd', 'orig_site', 'co_num', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('type', 'co_num', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('co_num', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'),)


class CoMstAll(TruncatedModel):
    site_ref = models.CharField(primary_key=True, max_length=8)
    type = models.CharField(max_length=1, blank=True, null=True)
    co_num = models.CharField(max_length=10)
    cust_num = models.CharField(max_length=7, blank=True, null=True)
    cust_seq = models.IntegerField(blank=True, null=True)
    cust_po = models.CharField(max_length=25, blank=True, null=True)
    order_date = models.DateTimeField()
    terms_code = models.CharField(max_length=3, blank=True, null=True)
    price = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    freight = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    misc_charges = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    prepaid_amt = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    sales_tax = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    stat = models.CharField(max_length=1, blank=True, null=True)
    cost = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    freight_t = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    m_charges_t = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    prepaid_t = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    sales_tax_t = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    sales_tax_2 = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    sales_tax_t2 = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    use_exch_rate = models.SmallIntegerField(blank=True, null=True)
    tax_code1 = models.CharField(max_length=6, blank=True, null=True)
    tax_code2 = models.CharField(max_length=6, blank=True, null=True)
    frt_tax_code1 = models.CharField(max_length=6, blank=True, null=True)
    frt_tax_code2 = models.CharField(max_length=6, blank=True, null=True)
    msc_tax_code1 = models.CharField(max_length=6, blank=True, null=True)
    msc_tax_code2 = models.CharField(max_length=6, blank=True, null=True)
    disc = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    exch_rate = models.DecimalField(max_digits=12, decimal_places=7, blank=True, null=True)
    orig_site = models.CharField(max_length=8, blank=True, null=True)
    credit_hold = models.SmallIntegerField(blank=True, null=True)
    credit_hold_date = models.DateTimeField(blank=True, null=True)
    credit_hold_reason = models.CharField(max_length=3, blank=True, null=True)
    credit_hold_user = models.CharField(max_length=3, blank=True, null=True)
    sync_reqd = models.SmallIntegerField(blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', unique=True, max_length=36)  # Field name made lowercase.
    slsman = models.CharField(max_length=8, blank=True, null=True)
    lcr_num = models.CharField(max_length=20, blank=True, null=True)
    qty_packages = models.SmallIntegerField(blank=True, null=True)
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    discount_type = models.CharField(max_length=1, blank=True, null=True)
    disc_amount = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    prospect_id = models.CharField(max_length=7, blank=True, null=True)
    shipment_approval_required = models.SmallIntegerField()
    portal_order = models.SmallIntegerField()
    ship_hold = models.SmallIntegerField()
    payment_method = models.CharField(max_length=1)
    ship_method = models.CharField(max_length=4, blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)
    surcharge = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    surcharge_t = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = IS_TEST
        db_table = 'co_mst_all'


class TermsMst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    terms_code = models.CharField(primary_key=True, max_length=3)
    description = models.CharField(max_length=40, blank=True, null=True)
    due_days = models.IntegerField(blank=True, null=True)
    disc_days = models.IntegerField()
    disc_pct = models.DecimalField(max_digits=6, decimal_places=3)
    prox_day = models.SmallIntegerField(blank=True, null=True)
    tax_disc = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    cash_only = models.SmallIntegerField()
    prox_code = models.SmallIntegerField()
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    advanced = models.SmallIntegerField()
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    use_multi_due_dates = models.SmallIntegerField(blank=True, null=True)
    prox_month_to_forward = models.SmallIntegerField()
    prox_disc_day = models.SmallIntegerField()
    prox_disc_month_to_forward = models.SmallIntegerField()
    cutoff_day = models.SmallIntegerField()
    holiday_offset_method = models.CharField(max_length=1)

    class Meta:
        managed = IS_TEST
        db_table = 'terms_mst'
        unique_together = (('rowpointer', 'site_ref'), ('terms_code', 'site_ref'),)


class CarrierMst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    carrier_code = models.CharField(primary_key=True, max_length=15)
    carrier_name = models.CharField(max_length=60, blank=True, null=True)
    url = models.CharField(max_length=150, blank=True, null=True)
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'carrier_mst'
        unique_together = (('rowpointer', 'site_ref'), ('carrier_code', 'site_ref'),)


class ShipcodeMst(TruncatedModel):
    site_ref = models.ForeignKey(CarrierMst, models.DO_NOTHING, db_column='site_ref')
    ship_code = models.CharField(primary_key=True, max_length=4)
    description = models.CharField(max_length=40, blank=True, null=True)
    transport = models.CharField(max_length=3, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    carrier_code = models.ForeignKey(CarrierMst, models.DO_NOTHING, db_column='carrier_code', blank=True, null=True)
    carrier_service_type = models.CharField(max_length=10, blank=True, null=True)
    active_for_customer_portal = models.SmallIntegerField()
    international = models.SmallIntegerField()

    class Meta:
        managed = IS_TEST
        db_table = 'shipcode_mst'
        unique_together = (('rowpointer', 'site_ref'), ('ship_code', 'site_ref'),)


class SlsclassMst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    slsclass = models.CharField(primary_key=True, max_length=3)
    description = models.CharField(max_length=40, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'slsclass_mst'
        unique_together = (('rowpointer', 'site_ref'), ('slsclass', 'site_ref'),)


class SlsmanMst(TruncatedModel):
    site_ref = models.ForeignKey(SlsclassMst, models.DO_NOTHING, db_column='site_ref')
    slsman = models.CharField(primary_key=True, max_length=8)
    slsclass = models.ForeignKey(SlsclassMst, models.DO_NOTHING, db_column='slsclass', blank=True, null=True)
    sales_ptd = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    sales_ytd = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    outside = models.SmallIntegerField(blank=True, null=True)
    ref_num = models.CharField(max_length=7, blank=True, null=True)
    code = models.CharField(max_length=3, blank=True, null=True)
    slsmangr = models.CharField(max_length=8, blank=True, null=True)
    logifld = models.SmallIntegerField(blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    charfld1 = models.CharField(max_length=20, blank=True, null=True)
    charfld2 = models.CharField(max_length=20, blank=True, null=True)
    charfld3 = models.CharField(max_length=20, blank=True, null=True)
    decifld1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    decifld2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    decifld3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    datefld = models.DateTimeField(blank=True, null=True)
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    username = models.CharField(max_length=30, blank=True, null=True)
    portal_reseller = models.SmallIntegerField()

    class Meta:
        managed = IS_TEST
        db_table = 'slsman_mst'
        unique_together = (('rowpointer', 'site_ref'), ('slsman', 'site_ref'),)


class CommodityMst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    comm_code = models.CharField(primary_key=True, max_length=12)
    description = models.CharField(max_length=40, blank=True, null=True)
    suppl_qty_req = models.SmallIntegerField(blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    suppl_qty_conv_factor = models.FloatField()

    class Meta:
        managed = IS_TEST
        db_table = 'commodity_mst'
        unique_together = (('rowpointer', 'site_ref'), ('comm_code', 'site_ref'),)


class CommodityMstAll(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    comm_code = models.CharField(primary_key=True, max_length=12)
    description = models.CharField(max_length=40, blank=True, null=True)
    rowpointer = models.CharField(db_column='RowPointer', unique=True, max_length=36)  # Field name made lowercase.
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'commodity_mst_all'
        unique_together = (('comm_code', 'site_ref'),)


class CoitemMst(TruncatedModel):
    site_ref = models.ForeignKey('Unitcd4Mst', models.DO_NOTHING, db_column='site_ref')
    co_num = models.CharField(max_length=10)
    co_line = models.SmallIntegerField()
    co_release = models.SmallIntegerField()
    item = models.CharField(max_length=30)
    qty_ordered = models.DecimalField(max_digits=19, decimal_places=8)
    qty_ready = models.DecimalField(max_digits=19, decimal_places=8)
    qty_shipped = models.DecimalField(max_digits=19, decimal_places=8)
    qty_packed = models.DecimalField(max_digits=19, decimal_places=8)
    disc = models.DecimalField(max_digits=11, decimal_places=8)
    cost = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    ref_type = models.CharField(max_length=1, blank=True, null=True)
    ref_num = models.CharField(max_length=10, blank=True, null=True)
    ref_line_suf = models.SmallIntegerField(blank=True, null=True)
    ref_release = models.SmallIntegerField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    ship_date = models.DateTimeField(blank=True, null=True)
    reprice = models.SmallIntegerField()
    cust_item = models.CharField(max_length=30, blank=True, null=True)
    qty_invoiced = models.DecimalField(max_digits=19, decimal_places=8)
    qty_returned = models.DecimalField(max_digits=19, decimal_places=8)
    cgs_total = models.DecimalField(max_digits=23, decimal_places=8)
    feat_str = models.CharField(max_length=40, blank=True, null=True)
    stat = models.CharField(max_length=1, blank=True, null=True)
    cust_num = models.CharField(max_length=7, blank=True, null=True)
    cust_seq = models.IntegerField(blank=True, null=True)
    prg_bill_tot = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    prg_bill_app = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    release_date = models.DateTimeField(blank=True, null=True)
    promise_date = models.DateTimeField(blank=True, null=True)
    whse = models.CharField(max_length=4, blank=True, null=True)
    wks_basis = models.CharField(max_length=1, blank=True, null=True)
    wks_value = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    comm_code = models.ForeignKey('CommodityMst', models.DO_NOTHING, db_column='comm_code', blank=True, null=True)
    process_ind = models.CharField(max_length=1, blank=True, null=True)
    unit_weight = models.DecimalField(max_digits=11, decimal_places=3, blank=True, null=True)
    origin = models.CharField(max_length=2, blank=True, null=True)
    cons_num = models.IntegerField(blank=True, null=True)
    tax_code1 = models.CharField(max_length=6, blank=True, null=True)
    tax_code2 = models.CharField(max_length=6, blank=True, null=True)
    export_value = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    ec_code = models.CharField(max_length=2, blank=True, null=True)
    transport = models.CharField(max_length=3, blank=True, null=True)
    pick_date = models.DateTimeField(blank=True, null=True)
    pricecode = models.CharField(max_length=3, blank=True, null=True)
    u_m = models.CharField(max_length=3)
    qty_ordered_conv = models.DecimalField(max_digits=19, decimal_places=8)
    price_conv = models.DecimalField(max_digits=20, decimal_places=8)
    co_cust_num = models.CharField(max_length=7, blank=True, null=True)
    packed = models.SmallIntegerField(blank=True, null=True)
    bol = models.SmallIntegerField(blank=True, null=True)
    qty_rsvd = models.DecimalField(max_digits=19, decimal_places=8)
    matl_cost = models.DecimalField(max_digits=20, decimal_places=8)
    lbr_cost = models.DecimalField(max_digits=20, decimal_places=8)
    fovhd_cost = models.DecimalField(max_digits=20, decimal_places=8)
    vovhd_cost = models.DecimalField(max_digits=20, decimal_places=8)
    out_cost = models.DecimalField(max_digits=20, decimal_places=8)
    cgs_total_matl = models.DecimalField(max_digits=23, decimal_places=8)
    cgs_total_lbr = models.DecimalField(max_digits=23, decimal_places=8)
    cgs_total_fovhd = models.DecimalField(max_digits=23, decimal_places=8)
    cgs_total_vovhd = models.DecimalField(max_digits=23, decimal_places=8)
    cgs_total_out = models.DecimalField(max_digits=23, decimal_places=8)
    cost_conv = models.DecimalField(max_digits=20, decimal_places=8)
    matl_cost_conv = models.DecimalField(max_digits=20, decimal_places=8)
    lbr_cost_conv = models.DecimalField(max_digits=20, decimal_places=8)
    fovhd_cost_conv = models.DecimalField(max_digits=20, decimal_places=8)
    vovhd_cost_conv = models.DecimalField(max_digits=20, decimal_places=8)
    out_cost_conv = models.DecimalField(max_digits=20, decimal_places=8)
    ship_site = models.CharField(max_length=8, blank=True, null=True)
    sync_reqd = models.SmallIntegerField(blank=True, null=True)
    co_orig_site = models.CharField(max_length=8, blank=True, null=True)
    cust_po = models.CharField(max_length=25, blank=True, null=True)
    rma_num = models.CharField(max_length=10, blank=True, null=True)
    rma_line = models.SmallIntegerField(blank=True, null=True)
    projected_date = models.DateTimeField(blank=True, null=True)
    consolidate = models.SmallIntegerField()
    inv_freq = models.CharField(max_length=1, blank=True, null=True)
    summarize = models.SmallIntegerField()
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(primary_key=True, db_column='RowPointer', max_length=36)  # Field name made lowercase.
    description = models.CharField(max_length=40, blank=True, null=True)
    config_id = models.CharField(max_length=12, blank=True, null=True)
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    rcpt_rqmt = models.CharField(max_length=1)
    suppl_qty_conv_factor = models.FloatField()
    print_kit_components = models.SmallIntegerField()
    due_date_day = models.DateTimeField(blank=True, null=True)
    external_reservation_ref = models.CharField(max_length=80, blank=True, null=True)
    days_shipped_before_due_date_tolerance = models.SmallIntegerField(blank=True, null=True)
    days_shipped_after_due_date_tolerance = models.SmallIntegerField(blank=True, null=True)
    shipped_over_ordered_qty_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    shipped_under_ordered_qty_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    priority = models.SmallIntegerField(blank=True, null=True)
    invoice_hold = models.SmallIntegerField()
    qty_picked = models.DecimalField(max_digits=19, decimal_places=8)
    fs_inc_num = models.CharField(max_length=10, blank=True, null=True)
    external_shipment_line_id = models.CharField(max_length=22, blank=True, null=True)
    last_external_shipment_doc_id = models.CharField(max_length=35, blank=True, null=True)
    last_process_shipment_doc_id = models.CharField(max_length=35, blank=True, null=True)

    class Meta:
        managed = IS_TEST
        db_table = 'coitem_mst'
        unique_together = (('co_cust_num', 'co_num', 'co_line', 'co_release', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('stat', 'item', 'due_date_day', 'rcpt_rqmt', 'rowpointer', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('rowpointer', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('ship_site', 'co_num', 'co_line', 'co_release', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('co_num', 'co_line', 'co_release', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'),)


class Unitcd4Mst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    unit4 = models.CharField(primary_key=True, max_length=4)
    description = models.CharField(max_length=40, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'unitcd4_mst'
        unique_together = (('rowpointer', 'site_ref'), ('unit4', 'site_ref'),)


class Unitcd4MstAll(TruncatedModel):
    site_ref = models.CharField(primary_key=True, max_length=8)
    unit4 = models.CharField(max_length=4)
    description = models.CharField(max_length=40, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', unique=True, max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'unitcd4_mst_all'
        unique_together = (('site_ref', 'unit4'),)


class CoitemMstAll(TruncatedModel):
    site_ref = models.CharField(primary_key=True, max_length=8)
    co_num = models.CharField(max_length=10)
    co_line = models.SmallIntegerField()
    co_release = models.SmallIntegerField()
    item = models.CharField(max_length=30)
    qty_ordered = models.DecimalField(max_digits=19, decimal_places=8)
    qty_ready = models.DecimalField(max_digits=19, decimal_places=8)
    qty_shipped = models.DecimalField(max_digits=19, decimal_places=8)
    qty_packed = models.DecimalField(max_digits=19, decimal_places=8)
    disc = models.DecimalField(max_digits=11, decimal_places=8)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    ref_type = models.CharField(max_length=1, blank=True, null=True)
    ref_num = models.CharField(max_length=10, blank=True, null=True)
    ref_line_suf = models.SmallIntegerField(blank=True, null=True)
    ref_release = models.SmallIntegerField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    ship_date = models.DateTimeField(blank=True, null=True)
    reprice = models.SmallIntegerField()
    cust_item = models.CharField(max_length=30, blank=True, null=True)
    qty_invoiced = models.DecimalField(max_digits=19, decimal_places=8)
    qty_returned = models.DecimalField(max_digits=19, decimal_places=8)
    feat_str = models.CharField(max_length=40, blank=True, null=True)
    stat = models.CharField(max_length=1, blank=True, null=True)
    cust_num = models.CharField(max_length=7, blank=True, null=True)
    cust_seq = models.IntegerField(blank=True, null=True)
    prg_bill_tot = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    prg_bill_app = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    release_date = models.DateTimeField(blank=True, null=True)
    promise_date = models.DateTimeField(blank=True, null=True)
    whse = models.CharField(max_length=4, blank=True, null=True)
    comm_code = models.CharField(max_length=12, blank=True, null=True)
    trans_nat = models.CharField(max_length=2, blank=True, null=True)
    process_ind = models.CharField(max_length=1, blank=True, null=True)
    delterm = models.CharField(max_length=4, blank=True, null=True)
    unit_weight = models.DecimalField(max_digits=11, decimal_places=3, blank=True, null=True)
    origin = models.CharField(max_length=2, blank=True, null=True)
    cons_num = models.IntegerField(blank=True, null=True)
    tax_code1 = models.CharField(max_length=6, blank=True, null=True)
    tax_code2 = models.CharField(max_length=6, blank=True, null=True)
    export_value = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    ec_code = models.CharField(max_length=2, blank=True, null=True)
    transport = models.CharField(max_length=3, blank=True, null=True)
    u_m = models.CharField(max_length=3)
    qty_ordered_conv = models.DecimalField(max_digits=19, decimal_places=8)
    price_conv = models.DecimalField(max_digits=20, decimal_places=8)
    co_cust_num = models.CharField(max_length=7, blank=True, null=True)
    packed = models.SmallIntegerField(blank=True, null=True)
    qty_rsvd = models.DecimalField(max_digits=19, decimal_places=8)
    ship_site = models.CharField(max_length=8, blank=True, null=True)
    sync_reqd = models.SmallIntegerField(blank=True, null=True)
    co_orig_site = models.CharField(max_length=8, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', unique=True, max_length=36)  # Field name made lowercase.
    description = models.CharField(max_length=40, blank=True, null=True)
    pricecode = models.CharField(max_length=3, blank=True, null=True)
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    projected_date = models.DateTimeField(blank=True, null=True)
    cost = models.DecimalField(max_digits=20, decimal_places=8)
    trans_nat_2 = models.CharField(max_length=2, blank=True, null=True)
    suppl_qty_conv_factor = models.FloatField()
    days_shipped_before_due_date_tolerance = models.SmallIntegerField(blank=True, null=True)
    days_shipped_after_due_date_tolerance = models.SmallIntegerField(blank=True, null=True)
    shipped_over_ordered_qty_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    shipped_under_ordered_qty_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    invoice_hold = models.SmallIntegerField()
    manufacturer_id = models.CharField(max_length=7, blank=True, null=True)
    manufacturer_item = models.CharField(max_length=30, blank=True, null=True)
    qty_picked = models.DecimalField(max_digits=19, decimal_places=8)
    cgs_total = models.DecimalField(max_digits=23, decimal_places=8)
    cost_conv = models.DecimalField(max_digits=20, decimal_places=8)
    promotion_code = models.CharField(max_length=10, blank=True, null=True)
    last_external_shipment_doc_id = models.CharField(max_length=35, blank=True, null=True)
    last_process_shipment_doc_id = models.CharField(max_length=35, blank=True, null=True)
    consolidate = models.SmallIntegerField()

    class Meta:
        managed = IS_TEST
        db_table = 'coitem_mst_all'
        unique_together = (('site_ref', 'co_num', 'co_line', 'co_release'),)


class CustomerMstAll(TruncatedModel):
    site_ref = models.CharField(max_length=8, db_column='site_ref', default="P2METCAM")
    cust_num = models.CharField(primary_key=True, max_length=7)
    cust_seq = models.IntegerField(db_column='cust_seq')
    contact_1 = models.CharField(db_column='contact##1', max_length=30, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    contact_2 = models.CharField(db_column='contact##2', max_length=30, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    contact_3 = models.CharField(db_column='contact##3', max_length=30, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    phone_1 = models.CharField(db_column='phone##1', max_length=25, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    phone_2 = models.CharField(db_column='phone##2', max_length=25, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    phone_3 = models.CharField(db_column='phone##3', max_length=25, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cust_type = models.CharField(max_length=6, blank=True, null=True)
    terms_code = models.CharField(max_length=3, blank=True, null=True)
    slsman = models.CharField(max_length=8, blank=True, null=True)
    state_cycle = models.CharField(max_length=1, blank=True, null=True)
    bank_code = models.CharField(max_length=3, blank=True, null=True)
    tax_code1 = models.CharField(max_length=6, blank=True, null=True)
    tax_code2 = models.CharField(max_length=6, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', unique=True, max_length=36)  # Field name made lowercase.
    order_bal = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    posted_bal = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    export_type = models.CharField(max_length=1)
    ship_code = models.CharField(max_length=4, blank=True, null=True)
    fin_chg = models.SmallIntegerField(blank=True, null=True)
    last_inv = models.DateTimeField(blank=True, null=True)
    last_paid = models.DateTimeField(blank=True, null=True)
    sales_ytd = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    sales_lst_yr = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    disc_ytd = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    disc_lst_yr = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    last_fin_chg = models.DateTimeField(blank=True, null=True)
    sales_ptd = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    calc_date = models.DateTimeField(blank=True, null=True)
    num_periods = models.SmallIntegerField(blank=True, null=True)
    avg_days_os = models.SmallIntegerField(blank=True, null=True)
    num_invoices = models.IntegerField(blank=True, null=True)
    hist_days_os = models.IntegerField(blank=True, null=True)
    larg_days_os = models.IntegerField(blank=True, null=True)
    last_days_os = models.SmallIntegerField(blank=True, null=True)
    avg_bal_os = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    large_bal_os = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    last_bal_os = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    whse = models.CharField(max_length=4, blank=True, null=True)
    charfld1 = models.CharField(max_length=20, blank=True, null=True)
    charfld2 = models.CharField(max_length=20, blank=True, null=True)
    charfld3 = models.CharField(max_length=20, blank=True, null=True)
    decifld1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    decifld2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    decifld3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    logifld = models.SmallIntegerField(blank=True, null=True)
    datefld = models.DateTimeField(blank=True, null=True)
    pay_type = models.CharField(max_length=1, blank=True, null=True)
    edi_cust = models.SmallIntegerField(blank=True, null=True)
    branch_id = models.CharField(max_length=3, blank=True, null=True)
    trans_nat = models.CharField(max_length=2, blank=True, null=True)
    delterm = models.CharField(max_length=4, blank=True, null=True)
    process_ind = models.CharField(max_length=1, blank=True, null=True)
    use_exch_rate = models.SmallIntegerField(blank=True, null=True)
    pricecode = models.CharField(max_length=3, blank=True, null=True)
    ship_early = models.SmallIntegerField(blank=True, null=True)
    ship_partial = models.SmallIntegerField(blank=True, null=True)
    lang_code = models.CharField(max_length=3, blank=True, null=True)
    end_user_type = models.CharField(max_length=6, blank=True, null=True)
    ship_site = models.CharField(max_length=8, blank=True, null=True)
    lcr_reqd = models.SmallIntegerField(blank=True, null=True)
    cust_bank = models.CharField(max_length=3, blank=True, null=True)
    draft_print_flag = models.SmallIntegerField(blank=True, null=True)
    rcv_internal_email = models.SmallIntegerField(blank=True, null=True)
    customer_email_addr = models.CharField(max_length=60, blank=True, null=True)
    send_customer_email = models.SmallIntegerField(blank=True, null=True)
    aps_pull_up = models.SmallIntegerField(blank=True, null=True)
    do_invoice = models.CharField(max_length=1, blank=True, null=True)
    consolidate = models.SmallIntegerField(blank=True, null=True)
    inv_freq = models.CharField(max_length=1, blank=True, null=True)
    summarize = models.SmallIntegerField(blank=True, null=True)
    einvoice = models.SmallIntegerField(blank=True, null=True)
    crm_guid = models.CharField(max_length=36, blank=True, null=True)
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    print_pack_inv = models.SmallIntegerField()
    one_pack_inv = models.SmallIntegerField()
    inv_category = models.CharField(max_length=15)
    include_tax_in_price = models.SmallIntegerField(blank=True, null=True)
    trans_nat_2 = models.CharField(max_length=2, blank=True, null=True)
    use_revision_pay_days = models.SmallIntegerField(blank=True, null=True)
    revision_day = models.SmallIntegerField(blank=True, null=True)
    revision_day_start_time_1 = models.DateTimeField(db_column='revision_day_start_time##1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    revision_day_start_time_2 = models.DateTimeField(db_column='revision_day_start_time##2', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    revision_day_end_time_1 = models.DateTimeField(db_column='revision_day_end_time##1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    revision_day_end_time_2 = models.DateTimeField(db_column='revision_day_end_time##2', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    pay_day = models.SmallIntegerField(blank=True, null=True)
    pay_day_start_time_1 = models.DateTimeField(db_column='pay_day_start_time##1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    pay_day_start_time_2 = models.DateTimeField(db_column='pay_day_start_time##2', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    pay_day_end_time_1 = models.DateTimeField(db_column='pay_day_end_time##1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    pay_day_end_time_2 = models.DateTimeField(db_column='pay_day_end_time##2', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    active_for_data_integration = models.SmallIntegerField()
    show_in_ship_to_drop_down_list = models.SmallIntegerField()
    show_in_drop_down_list = models.SmallIntegerField()
    sic_code = models.CharField(max_length=4, blank=True, null=True)
    number_of_employees = models.IntegerField(blank=True, null=True)
    company_revenue = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    territory_code = models.CharField(max_length=8, blank=True, null=True)
    sales_team_id = models.CharField(max_length=7, blank=True, null=True)
    days_shipped_before_due_date_tolerance = models.SmallIntegerField(blank=True, null=True)
    days_shipped_after_due_date_tolerance = models.SmallIntegerField(blank=True, null=True)
    shipped_over_ordered_qty_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    shipped_under_ordered_qty_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    default_ship_to = models.IntegerField()
    reseller_slsman = models.CharField(max_length=8, blank=True, null=True)
    shipment_approval_required = models.SmallIntegerField()
    ship_hold = models.SmallIntegerField()
    ship_method_group = models.CharField(max_length=30, blank=True, null=True)
    jp_consumption_tax_round_method = models.CharField(db_column='JP_consumption_tax_round_method', max_length=1)  # Field name made lowercase.
    jp_consumption_tax_header_line_method = models.CharField(db_column='JP_consumption_tax_header_line_method', max_length=1)  # Field name made lowercase.
    include_orders_in_tax_rpt = models.SmallIntegerField()
    constructive_sale_price_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    jp_inv_batch_cutoff_day = models.SmallIntegerField(db_column='JP_inv_batch_cutoff_day')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'customer_mst_all'
        unique_together = (('cust_num', 'cust_seq', 'site_ref'),)


class Unitcd1Mst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    unit1 = models.CharField(primary_key=True, max_length=4)
    description = models.CharField(max_length=40, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'unitcd1_mst'
        unique_together = (('rowpointer', 'site_ref'), ('unit1', 'site_ref'),)


class BankHdrMst(TruncatedModel):
    site_ref = models.ForeignKey('Unitcd1Mst', models.DO_NOTHING, db_column='site_ref')
    bank_code = models.CharField(primary_key=True, max_length=3)
    bank_acct_no = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    for_balance = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    dom_balance = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    business_identifier_code = models.CharField(max_length=11, blank=True, null=True)
    international_bank_account = models.CharField(max_length=34, blank=True, null=True)

    class Meta:
        managed = IS_TEST
        db_table = 'bank_hdr_mst'
        unique_together = (('rowpointer', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('bank_code', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'),)


class BankHdrMstAll(TruncatedModel):
    site_ref = models.CharField(primary_key=True, max_length=8)
    bank_code = models.CharField(max_length=3)
    name = models.CharField(max_length=60, blank=True, null=True)
    inworkflow = models.SmallIntegerField(db_column='InWorkflow', blank=True, null=True)  # Field name made lowercase.
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag', blank=True, null=True)  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate', blank=True, null=True)  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', unique=True, max_length=36, blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30, blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    bank_acct_no = models.CharField(max_length=20, blank=True, null=True)
    curr_code = models.CharField(max_length=3, blank=True, null=True)
    dom_balance = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = IS_TEST
        db_table = 'bank_hdr_mst_all'
        unique_together = (('site_ref', 'bank_code'),)


class CustomerMst(TruncatedModel):
    site_ref = models.CharField(db_column='site_ref', max_length=8, default="P2METCAM")
    cust_num = models.CharField(max_length=7)
    cust_seq = models.IntegerField(db_column='cust_seq')
    contact_1 = models.CharField(db_column='contact##1', max_length=30, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    contact_2 = models.CharField(db_column='contact##2', max_length=30, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    contact_3 = models.CharField(db_column='contact##3', max_length=30, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    phone_1 = models.CharField(db_column='phone##1', max_length=25, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    phone_2 = models.CharField(db_column='phone##2', max_length=25, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    phone_3 = models.CharField(db_column='phone##3', max_length=25, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cust_type = models.CharField(max_length=6, blank=True, null=True)
    terms_code = models.ForeignKey('TermsMst', models.DO_NOTHING, db_column='terms_code', blank=True, null=True)
    ship_code = models.ForeignKey('ShipcodeMst', models.DO_NOTHING, db_column='ship_code', blank=True, null=True)
    slsman = models.CharField(max_length=8, blank=True, null=True)
    state_cycle = models.CharField(max_length=1, blank=True, null=True)
    fin_chg = models.SmallIntegerField(blank=True, null=True)
    last_inv = models.DateTimeField(blank=True, null=True)
    last_paid = models.DateTimeField(blank=True, null=True)
    sales_ytd = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    sales_lst_yr = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    disc_ytd = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    disc_lst_yr = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    last_fin_chg = models.DateTimeField(blank=True, null=True)
    sales_ptd = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    calc_date = models.DateTimeField(blank=True, null=True)
    num_periods = models.SmallIntegerField(blank=True, null=True)
    avg_days_os = models.SmallIntegerField(blank=True, null=True)
    num_invoices = models.IntegerField(blank=True, null=True)
    hist_days_os = models.IntegerField(blank=True, null=True)
    larg_days_os = models.IntegerField(blank=True, null=True)
    last_days_os = models.SmallIntegerField(blank=True, null=True)
    avg_bal_os = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    large_bal_os = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    last_bal_os = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    whse = models.CharField(max_length=4, blank=True, null=True)
    charfld1 = models.CharField(max_length=20, blank=True, null=True)
    charfld2 = models.CharField(max_length=20, blank=True, null=True)
    charfld3 = models.CharField(max_length=20, blank=True, null=True)
    decifld1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    decifld2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    decifld3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    logifld = models.SmallIntegerField(blank=True, null=True)
    datefld = models.DateTimeField(blank=True, null=True)
    tax_reg_num1 = models.CharField(max_length=25, blank=True, null=True)
    tax_reg_num2 = models.CharField(max_length=25, blank=True, null=True)
    pay_type = models.CharField(max_length=1, blank=True, null=True)
    edi_cust = models.SmallIntegerField(blank=True, null=True)
    branch_id = models.CharField(max_length=3, blank=True, null=True)
    trans_nat = models.CharField(max_length=2, blank=True, null=True)
    process_ind = models.CharField(max_length=1, blank=True, null=True)
    use_exch_rate = models.SmallIntegerField(blank=True, null=True)
    tax_code1 = models.CharField(max_length=6, blank=True, null=True)
    tax_code2 = models.CharField(max_length=6, blank=True, null=True)
    ship_early = models.SmallIntegerField(blank=True, null=True)
    ship_partial = models.SmallIntegerField(blank=True, null=True)
    lang_code = models.CharField(max_length=3, blank=True, null=True)
    end_user_type = models.CharField(max_length=6, blank=True, null=True)
    ship_site = models.CharField(max_length=8, blank=True, null=True)
    lcr_reqd = models.SmallIntegerField(blank=True, null=True)
    cust_bank = models.CharField(max_length=3, blank=True, null=True)
    draft_print_flag = models.SmallIntegerField(blank=True, null=True)
    rcv_internal_email = models.SmallIntegerField(blank=True, null=True)
    customer_email_addr = models.CharField(max_length=60, blank=True, null=True)
    send_customer_email = models.SmallIntegerField(blank=True, null=True)
    aps_pull_up = models.SmallIntegerField(blank=True, null=True)
    do_invoice = models.CharField(max_length=1, blank=True, null=True)
    consolidate = models.SmallIntegerField(blank=True, null=True)
    inv_freq = models.CharField(max_length=1, blank=True, null=True)
    summarize = models.SmallIntegerField(blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(primary_key=True, db_column='RowPointer', max_length=36)  # Field name made lowercase.
    einvoice = models.SmallIntegerField(blank=True, null=True)
    order_bal = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    posted_bal = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    crm_guid = models.CharField(max_length=36, blank=True, null=True)
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    print_pack_inv = models.SmallIntegerField(default=1)
    one_pack_inv = models.SmallIntegerField(default=1)
    inv_category = models.CharField(max_length=15)
    include_tax_in_price = models.SmallIntegerField(blank=True, null=True)
    use_revision_pay_days = models.SmallIntegerField(blank=True, null=True)
    revision_day = models.SmallIntegerField(blank=True, null=True)
    revision_day_start_time_1 = models.DateTimeField(db_column='revision_day_start_time##1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    revision_day_start_time_2 = models.DateTimeField(db_column='revision_day_start_time##2', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    revision_day_end_time_1 = models.DateTimeField(db_column='revision_day_end_time##1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    revision_day_end_time_2 = models.DateTimeField(db_column='revision_day_end_time##2', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    pay_day = models.SmallIntegerField(blank=True, null=True)
    pay_day_start_time_1 = models.DateTimeField(db_column='pay_day_start_time##1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    pay_day_start_time_2 = models.DateTimeField(db_column='pay_day_start_time##2', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    pay_day_end_time_1 = models.DateTimeField(db_column='pay_day_end_time##1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    pay_day_end_time_2 = models.DateTimeField(db_column='pay_day_end_time##2', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    export_type = models.CharField(max_length=1)
    active_for_data_integration = models.SmallIntegerField(default=1)
    show_in_ship_to_drop_down_list = models.SmallIntegerField(default=1)
    show_in_drop_down_list = models.SmallIntegerField(default=1)
    sic_code = models.CharField(max_length=4, blank=True, null=True)
    number_of_employees = models.IntegerField(blank=True, null=True)
    company_revenue = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    days_shipped_before_due_date_tolerance = models.SmallIntegerField(blank=True, null=True)
    days_shipped_after_due_date_tolerance = models.SmallIntegerField(blank=True, null=True)
    shipped_over_ordered_qty_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    shipped_under_ordered_qty_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    default_ship_to = models.IntegerField(default=1)
    reseller_slsman = models.CharField(max_length=8, blank=True, null=True)
    shipment_approval_required = models.SmallIntegerField(default=1)
    ship_hold = models.SmallIntegerField(default=1)
    jp_consumption_tax_round_method = models.CharField(db_column='JP_consumption_tax_round_method', max_length=1)  # Field name made lowercase.
    jp_consumption_tax_header_line_method = models.CharField(db_column='JP_consumption_tax_header_line_method', max_length=1)  # Field name made lowercase.
    vrtx_geocode = models.CharField(max_length=20, blank=True, null=True)
    include_orders_in_tax_rpt = models.SmallIntegerField(default=1)
    constructive_sale_price_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    tax_reg_num1_exp_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = IS_TEST
        db_table = 'customer_mst'


class Unitcd1MstAll(TruncatedModel):
    site_ref = models.CharField(primary_key=True, max_length=8)
    unit1 = models.CharField(max_length=4)
    description = models.CharField(max_length=40, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', unique=True, max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'unitcd1_mst_all'
        unique_together = (('site_ref', 'unit1'),)


class JobMst(TruncatedModel):
    site_ref = models.ForeignKey('Unitcd3Mst', models.DO_NOTHING, db_column='site_ref')
    type = models.CharField(max_length=1, blank=True, null=True)
    job = models.CharField(primary_key=True, max_length=20)
    suffix = models.SmallIntegerField()
    job_date = models.DateTimeField(blank=True, null=True)
    cust_num = models.CharField(max_length=7, blank=True, null=True)
    ord_type = models.CharField(max_length=1, blank=True, null=True)
    ord_num = models.CharField(max_length=10, blank=True, null=True)
    ord_line = models.SmallIntegerField(blank=True, null=True)
    ord_release = models.SmallIntegerField(blank=True, null=True)
    est_job = models.CharField(max_length=20, blank=True, null=True)
    est_suf = models.SmallIntegerField(blank=True, null=True)
    item = models.CharField(max_length=30)
    qty_released = models.DecimalField(max_digits=19, decimal_places=8)
    qty_complete = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    qty_scrapped = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    stat = models.CharField(max_length=1, blank=True, null=True)
    lst_trx_date = models.DateTimeField(blank=True, null=True)
    root_job = models.CharField(max_length=20, blank=True, null=True)
    root_suf = models.SmallIntegerField(blank=True, null=True)
    ref_job = models.CharField(max_length=20, blank=True, null=True)
    ref_suf = models.SmallIntegerField()
    ref_oper = models.IntegerField()
    ref_seq = models.SmallIntegerField(blank=True, null=True)
    low_level = models.SmallIntegerField(blank=True, null=True)
    effect_date = models.DateTimeField(blank=True, null=True)
    wip_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_complete = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_special = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    revision = models.CharField(max_length=8, blank=True, null=True)
    picked = models.SmallIntegerField(blank=True, null=True)
    whse = models.CharField(max_length=4, blank=True, null=True)
    ps_num = models.CharField(max_length=10, blank=True, null=True)
    wip_matl_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_lbr_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_fovhd_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_vovhd_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_out_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_matl_comp = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_lbr_comp = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_fovhd_comp = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_vovhd_comp = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_out_comp = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    rollup_date = models.DateTimeField(blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    description = models.CharField(max_length=40, blank=True, null=True)
    config_id = models.CharField(max_length=12, blank=True, null=True)
    co_product_mix = models.SmallIntegerField(blank=True, null=True)
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    scheduled = models.SmallIntegerField()
    rcpt_rqmt = models.CharField(max_length=1)
    export_type = models.CharField(max_length=1)
    contains_tax_free_matl = models.SmallIntegerField()
    midnight_of_job_sch_end_date = models.DateTimeField(blank=True, null=True)
    midnight_of_job_sch_compdate = models.DateTimeField(blank=True, null=True)
    rework = models.SmallIntegerField()
    unlinked_xref = models.SmallIntegerField()
    is_external = models.SmallIntegerField()
    preassign_lots = models.SmallIntegerField()
    preassign_serials = models.SmallIntegerField()
    config_doc_id = models.CharField(max_length=12, blank=True, null=True)
    mo_bom_alternate_id = models.CharField(db_column='MO_bom_alternate_id', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mo_bom_alternate_description = models.CharField(db_column='MO_bom_alternate_description', max_length=40, blank=True, null=True)  # Field name made lowercase.
    mo_co_job = models.SmallIntegerField(db_column='MO_co_job')  # Field name made lowercase.
    mo_product_cycle = models.IntegerField(db_column='MO_product_cycle', blank=True, null=True)  # Field name made lowercase.
    mo_qty_per_cycle = models.DecimalField(db_column='MO_qty_per_cycle', max_digits=19, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    mo_job_description = models.CharField(db_column='MO_job_description', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'job_mst'
        unique_together = (('type', 'item', 'midnight_of_job_sch_compdate', 'rcpt_rqmt', 'rowpointer', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('type', 'item', 'midnight_of_job_sch_end_date', 'rcpt_rqmt', 'rowpointer', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('rowpointer', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('job', 'suffix', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'),)


class JobMstAll(TruncatedModel):
    site_ref = models.CharField(primary_key=True, max_length=8)
    type = models.CharField(max_length=1, blank=True, null=True)
    job = models.CharField(max_length=20)
    suffix = models.SmallIntegerField()
    stat = models.CharField(max_length=1, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', unique=True, max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    item = models.CharField(max_length=30)
    qty_released = models.DecimalField(max_digits=19, decimal_places=8)
    qty_complete = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    qty_scrapped = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    ps_num = models.CharField(max_length=10, blank=True, null=True)
    description = models.CharField(max_length=40, blank=True, null=True)
    lst_trx_date = models.DateTimeField(blank=True, null=True)
    ord_line = models.SmallIntegerField(blank=True, null=True)
    ord_num = models.CharField(max_length=10, blank=True, null=True)
    ord_release = models.SmallIntegerField(blank=True, null=True)
    ord_type = models.CharField(max_length=1, blank=True, null=True)
    wip_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    prospect_id = models.CharField(max_length=7, blank=True, null=True)
    wip_complete = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    cust_num = models.CharField(max_length=7, blank=True, null=True)
    job_date = models.DateTimeField(blank=True, null=True)
    revision = models.CharField(max_length=8, blank=True, null=True)
    whse = models.CharField(max_length=4, blank=True, null=True)
    ref_job = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = IS_TEST
        db_table = 'job_mst_all'
        unique_together = (('site_ref', 'job', 'suffix'),)


class JobPriceBreakMst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    job = models.CharField(max_length=20)
    suffix = models.SmallIntegerField()
    break_qty = models.DecimalField(max_digits=19, decimal_places=8)
    setup_markup = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    run_markup = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    outside_markup = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    matl_markup = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    fixture_cost = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    fixture_markup = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    tool_cost = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    tool_markup = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    other_cost = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    other_markup = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    non_recurring_cost = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    non_recurring_markup = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(primary_key=True, db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    overhead_markup = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = IS_TEST
        db_table = 'job_price_break_mst'
        unique_together = (('rowpointer', 'site_ref'), ('job', 'suffix', 'break_qty', 'site_ref'),)


class JobRefMst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    job = models.CharField(max_length=20)
    suffix = models.SmallIntegerField()
    oper_num = models.IntegerField()
    sequence = models.SmallIntegerField()
    ref_seq = models.SmallIntegerField()
    ref_des = models.CharField(max_length=10, blank=True, null=True)
    bubble = models.CharField(max_length=4, blank=True, null=True)
    assy_seq = models.CharField(max_length=4, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(primary_key=True, db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'job_ref_mst'
        unique_together = (('rowpointer', 'site_ref'), ('job', 'suffix', 'oper_num', 'sequence', 'ref_seq', 'site_ref'),)


class JobSchMst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    job = models.CharField(max_length=20)
    suffix = models.SmallIntegerField()
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    start_tick = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    end_tick = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    priority = models.SmallIntegerField(blank=True, null=True)
    prfreeze = models.SmallIntegerField(blank=True, null=True)
    sequence = models.CharField(max_length=3, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(primary_key=True, db_column='RowPointer', max_length=36)  # Field name made lowercase.
    compdate = models.DateTimeField(blank=True, null=True)
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    compdate_day = models.DateTimeField(blank=True, null=True)
    end_date_day = models.DateTimeField(blank=True, null=True)
    published_start_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = IS_TEST
        db_table = 'job_sch_mst'
        unique_together = (('rowpointer', 'site_ref'), ('job', 'suffix', 'site_ref'),)


class JobSchMstAll(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    job = models.CharField(primary_key=True, max_length=20)
    suffix = models.SmallIntegerField()
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    start_tick = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    end_tick = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    priority = models.SmallIntegerField(blank=True, null=True)
    prfreeze = models.SmallIntegerField(blank=True, null=True)
    sequence = models.CharField(max_length=3, blank=True, null=True)
    compdate = models.DateTimeField(blank=True, null=True)
    compdate_day = models.DateTimeField(blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', unique=True, max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'job_sch_mst_all'
        unique_together = (('job', 'suffix', 'site_ref'),)


class JobitemMst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    job = models.CharField(primary_key=True, max_length=20)
    suffix = models.SmallIntegerField()
    item = models.CharField(max_length=30)
    ord_type = models.CharField(max_length=1, blank=True, null=True)
    cust_num = models.CharField(max_length=7, blank=True, null=True)
    ord_num = models.CharField(max_length=10, blank=True, null=True)
    ord_line = models.SmallIntegerField(blank=True, null=True)
    ord_release = models.SmallIntegerField(blank=True, null=True)
    qty_released = models.DecimalField(max_digits=19, decimal_places=8)
    qty_complete = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    qty_scrapped = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    wip_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_complete = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_special = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_matl_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_lbr_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_fovhd_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_vovhd_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_out_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_matl_comp = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_lbr_comp = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_fovhd_comp = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_vovhd_comp = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_out_comp = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    ratio1 = models.SmallIntegerField(blank=True, null=True)
    ratio2 = models.SmallIntegerField(blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    rcpt_rqmt = models.CharField(max_length=1)
    midnight_of_job_sch_end_date = models.DateTimeField(blank=True, null=True)
    midnight_of_job_sch_compdate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = IS_TEST
        db_table = 'jobitem_mst'
        unique_together = (('item', 'midnight_of_job_sch_compdate', 'rcpt_rqmt', 'rowpointer', 'site_ref'), ('item', 'midnight_of_job_sch_end_date', 'rcpt_rqmt', 'rowpointer', 'site_ref'), ('rowpointer', 'site_ref'), ('job', 'suffix', 'item', 'site_ref'),)


class FeatureMst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    feature = models.CharField(primary_key=True, max_length=8)
    description = models.CharField(max_length=40, blank=True, null=True)
    qual_mask = models.CharField(max_length=40, blank=True, null=True)
    code_offset = models.SmallIntegerField(blank=True, null=True)
    code_length = models.SmallIntegerField(blank=True, null=True)
    mandatory = models.SmallIntegerField(blank=True, null=True)
    sel_qty = models.SmallIntegerField(blank=True, null=True)
    allow_new = models.SmallIntegerField(blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'feature_mst'
        unique_together = (('rowpointer', 'site_ref'), ('feature', 'site_ref'),)


class FeatureMstAll(TruncatedModel):
    site_ref = models.CharField(primary_key=True, max_length=8)
    feature = models.CharField(max_length=8)
    code_offset = models.SmallIntegerField(blank=True, null=True)
    code_length = models.SmallIntegerField(blank=True, null=True)
    mandatory = models.SmallIntegerField(blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', unique=True, max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'feature_mst_all'
        unique_together = (('site_ref', 'feature'),)


class JobmatlMst(TruncatedModel):
    site_ref = models.ForeignKey(FeatureMst, models.DO_NOTHING, db_column='site_ref')
    job = models.CharField(max_length=20)
    suffix = models.SmallIntegerField()
    oper_num = models.IntegerField()
    sequence = models.SmallIntegerField()
    matl_type = models.CharField(max_length=1, blank=True, null=True)
    item = models.CharField(max_length=30)
    matl_qty = models.DecimalField(max_digits=18, decimal_places=8, blank=True, null=True)
    units = models.CharField(max_length=1, blank=True, null=True)
    cost = models.DecimalField(max_digits=20, decimal_places=8)
    qty_issued = models.DecimalField(max_digits=18, decimal_places=8, blank=True, null=True)
    a_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    ref_type = models.CharField(max_length=1, blank=True, null=True)
    ref_num = models.CharField(max_length=10, blank=True, null=True)
    ref_line_suf = models.SmallIntegerField(blank=True, null=True)
    ref_release = models.SmallIntegerField(blank=True, null=True)
    po_unit_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    effect_date = models.DateTimeField(blank=True, null=True)
    obs_date = models.DateTimeField(blank=True, null=True)
    scrap_fact = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    qty_var = models.DecimalField(max_digits=18, decimal_places=8, blank=True, null=True)
    fixovhd_t = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    varovhd_t = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    feature = models.ForeignKey(FeatureMst, models.DO_NOTHING, db_column='feature', blank=True, null=True)
    probable = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)
    opt_code = models.CharField(max_length=8, blank=True, null=True)
    inc_price = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    description = models.CharField(max_length=40, blank=True, null=True)
    pick_date = models.DateTimeField(blank=True, null=True)
    bom_seq = models.SmallIntegerField(blank=True, null=True)
    matl_qty_conv = models.DecimalField(max_digits=18, decimal_places=8, blank=True, null=True)
    u_m = models.CharField(max_length=3, blank=True, null=True)
    inc_price_conv = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    cost_conv = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    backflush = models.SmallIntegerField(blank=True, null=True)
    bflush_loc = models.CharField(max_length=15, blank=True, null=True)
    fmatlovhd = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    vmatlovhd = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    matl_cost = models.DecimalField(max_digits=20, decimal_places=8)
    lbr_cost = models.DecimalField(max_digits=20, decimal_places=8)
    fovhd_cost = models.DecimalField(max_digits=20, decimal_places=8)
    vovhd_cost = models.DecimalField(max_digits=20, decimal_places=8)
    out_cost = models.DecimalField(max_digits=20, decimal_places=8)
    a_matl_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    a_lbr_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    a_fovhd_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    a_vovhd_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    a_out_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    matl_cost_conv = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    lbr_cost_conv = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    fovhd_cost_conv = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    vovhd_cost_conv = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    out_cost_conv = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(primary_key=True, db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    alt_group = models.SmallIntegerField()
    alt_group_rank = models.SmallIntegerField()
    planned_alternate = models.SmallIntegerField(blank=True, null=True)
    new_sequence = models.SmallIntegerField(blank=True, null=True)
    pp_matl_is_paper = models.SmallIntegerField(db_column='PP_matl_is_paper')  # Field name made lowercase.
    mo_formula_matl_weight_pct = models.DecimalField(db_column='MO_formula_matl_weight_pct', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'jobmatl_mst'
        unique_together = (('rowpointer', 'site_ref', 'site_ref'), ('job', 'suffix', 'oper_num', 'sequence', 'site_ref', 'site_ref'),)


class Unitcd3Mst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    unit3 = models.CharField(primary_key=True, max_length=4)
    description = models.CharField(max_length=40, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'unitcd3_mst'
        unique_together = (('rowpointer', 'site_ref'), ('unit3', 'site_ref'),)


class Unitcd3MstAll(TruncatedModel):
    site_ref = models.CharField(primary_key=True, max_length=8)
    unit3 = models.CharField(max_length=4)
    description = models.CharField(max_length=40, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', unique=True, max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'unitcd3_mst_all'
        unique_together = (('site_ref', 'unit3'),)


class JobrouteMst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    job = models.CharField(max_length=20)
    suffix = models.SmallIntegerField()
    oper_num = models.IntegerField()
    wc = models.ForeignKey('WcMst', models.DO_NOTHING, db_column='wc')
    setup_hrs_t = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    setup_cost_t = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    complete = models.SmallIntegerField(blank=True, null=True)
    setup_hrs_v = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    wip_amt = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    qty_scrapped = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    qty_received = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    qty_moved = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    qty_complete = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    effect_date = models.DateTimeField(blank=True, null=True)
    obs_date = models.DateTimeField(blank=True, null=True)
    bflush_type = models.CharField(max_length=1, blank=True, null=True)
    run_basis_lbr = models.CharField(max_length=1, blank=True, null=True)
    run_basis_mch = models.CharField(max_length=1, blank=True, null=True)
    fixovhd_t_lbr = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    fixovhd_t_mch = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    varovhd_t_lbr = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    varovhd_t_mch = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    run_hrs_t_lbr = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    run_hrs_t_mch = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    run_hrs_v_lbr = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    run_hrs_v_mch = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    run_cost_t_lbr = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    cntrl_point = models.SmallIntegerField(blank=True, null=True)
    setup_rate = models.DecimalField(max_digits=10, decimal_places=3)
    efficiency = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    fovhd_rate_mch = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    vovhd_rate_mch = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    run_rate_lbr = models.DecimalField(max_digits=10, decimal_places=3)
    varovhd_rate = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    fixovhd_rate = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    wip_matl_amt = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    wip_lbr_amt = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    wip_fovhd_amt = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    wip_vovhd_amt = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    wip_out_amt = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(primary_key=True, db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    yield_field = models.DecimalField(db_column='yield', max_digits=5, decimal_places=2)  # Field renamed because it was a Python reserved word.
    opm_consec_oper = models.SmallIntegerField()
    mo_shared = models.SmallIntegerField(db_column='MO_shared')  # Field name made lowercase.
    mo_seconds_per_cycle = models.DecimalField(db_column='MO_seconds_per_cycle', max_digits=8, decimal_places=4)  # Field name made lowercase.
    mo_formula_matl_weight = models.DecimalField(db_column='MO_formula_matl_weight', max_digits=9, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mo_formula_matl_weight_units = models.CharField(db_column='MO_formula_matl_weight_units', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'jobroute_mst'
        unique_together = (('rowpointer', 'site_ref', 'site_ref'), ('job', 'suffix', 'oper_num', 'site_ref', 'site_ref'),)


class JobrouteMstAll(TruncatedModel):
    site_ref = models.CharField(primary_key=True, max_length=8)
    job = models.CharField(max_length=20)
    suffix = models.SmallIntegerField()
    oper_num = models.IntegerField()
    effect_date = models.DateTimeField(blank=True, null=True)
    obs_date = models.DateTimeField(blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', unique=True, max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    complete = models.SmallIntegerField(blank=True, null=True)
    wc = models.CharField(max_length=6)
    bflush_type = models.CharField(max_length=1, blank=True, null=True)
    run_basis_lbr = models.CharField(max_length=1, blank=True, null=True)
    run_basis_mch = models.CharField(max_length=1, blank=True, null=True)
    cntrl_point = models.SmallIntegerField(blank=True, null=True)
    efficiency = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    run_rate_lbr = models.DecimalField(max_digits=10, decimal_places=3)
    setup_rate = models.DecimalField(max_digits=10, decimal_places=3)
    fixovhd_rate = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    varovhd_rate = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    fovhd_rate_mch = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    vovhd_rate_mch = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    setup_cost_t = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    run_cost_t_lbr = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    fixovhd_t_lbr = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    fixovhd_t_mch = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    varovhd_t_lbr = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    varovhd_t_mch = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    yield_field = models.DecimalField(db_column='yield', max_digits=5, decimal_places=2)  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = IS_TEST
        db_table = 'jobroute_mst_all'
        unique_together = (('site_ref', 'job', 'suffix', 'oper_num'),)


class WcMst(TruncatedModel):
    site_ref = models.ForeignKey(Unitcd1Mst, models.DO_NOTHING, db_column='site_ref')
    wc = models.CharField(primary_key=True, max_length=6)
    description = models.CharField(max_length=40, blank=True, null=True)
    outside = models.SmallIntegerField(blank=True, null=True)
    setup_rate = models.DecimalField(max_digits=10, decimal_places=3)
    efficiency = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    dept = models.CharField(max_length=6, blank=True, null=True)
    alternate = models.CharField(max_length=6, blank=True, null=True)
    queue_hrs_a = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    queue_qty_t = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    setup_rate_a = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    setup_hrs_t = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    calendar = models.CharField(max_length=6, blank=True, null=True)
    charfld1 = models.CharField(max_length=20, blank=True, null=True)
    charfld2 = models.CharField(max_length=20, blank=True, null=True)
    charfld3 = models.CharField(max_length=20, blank=True, null=True)
    decifld1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    decifld2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    decifld3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    logifld = models.SmallIntegerField(blank=True, null=True)
    datefld = models.DateTimeField(blank=True, null=True)
    queue_ticks = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    bflush_type = models.CharField(max_length=1, blank=True, null=True)
    run_hrs_t_mch = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    fovhd_rate_mch = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    vovhd_rate_mch = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    run_hrs_t_lbr = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    run_rate_lbr = models.DecimalField(max_digits=10, decimal_places=3)
    run_rate_a_lbr = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    overhead = models.CharField(max_length=3, blank=True, null=True)
    cntrl_point = models.SmallIntegerField()
    wip_matl_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_lbr_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_fovhd_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_vovhd_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    wip_out_total = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    queue_hrs = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    dispatch_lists_email = models.CharField(max_length=60, blank=True, null=True)
    sched_drv = models.CharField(max_length=1, blank=True, null=True)
    finish_hrs = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    setuprgid = models.CharField(max_length=30, blank=True, null=True)
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'wc_mst'
        unique_together = (('rowpointer', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('wc', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'),)


class CountryMst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    country = models.CharField(primary_key=True, max_length=30)
    ec_code = models.CharField(max_length=2, blank=True, null=True)
    ssd_ec_code = models.CharField(max_length=2, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    exp_doc_reqd = models.SmallIntegerField(blank=True, null=True)
    mx_nationality = models.CharField(db_column='MX_nationality', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'country_mst'
        unique_together = (('rowpointer', 'site_ref'), ('country', 'site_ref'),)


class ItemMst(TruncatedModel):
    site_ref = models.CharField(db_column='site_ref', max_length=8)
    item = models.CharField(primary_key=True, max_length=30)
    description = models.CharField(max_length=40, blank=True, null=True)
    qty_allocjob = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    u_m = models.CharField(max_length=3, db_column='u_m', blank=True, null=True)
    lead_time = models.SmallIntegerField()
    lot_size = models.DecimalField(max_digits=18, decimal_places=8, blank=True, null=True)
    qty_used_ytd = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    qty_mfg_ytd = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    abc_code = models.CharField(max_length=1, blank=True, null=True)
    drawing_nbr = models.CharField(max_length=25, blank=True, null=True)
    product_code = models.CharField(max_length=10, blank=True, null=True)
    p_m_t_code = models.CharField(max_length=1, blank=True, null=True)
    cost_method = models.CharField(max_length=1, blank=True, null=True)
    lst_lot_size = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    lst_u_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    avg_u_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    job = models.CharField(primary_key=True, max_length=20, blank=True, null=True)
    suffix = models.SmallIntegerField(blank=True, null=True)
    stocked = models.SmallIntegerField(blank=True, null=True)
    matl_type = models.CharField(max_length=1, blank=True, null=True)
    low_level = models.SmallIntegerField(blank=True, null=True)
    last_inv = models.DateTimeField(blank=True, null=True)
    days_supply = models.SmallIntegerField(blank=True, null=True)
    order_min = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    order_mult = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    plan_code = models.CharField(max_length=3, blank=True, null=True)
    mps_flag = models.SmallIntegerField(blank=True, null=True)
    accept_req = models.SmallIntegerField(blank=True, null=True)
    change_date = models.DateTimeField(blank=True, null=True)
    revision = models.CharField(max_length=8, blank=True, null=True)
    phantom_flag = models.SmallIntegerField(blank=True, null=True)
    plan_flag = models.SmallIntegerField(blank=True, null=True)
    paper_time = models.SmallIntegerField()
    dock_time = models.SmallIntegerField()
    asm_setup = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    asm_run = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    asm_matl = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    asm_tool = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    asm_fixture = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    asm_other = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    asm_fixed = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    asm_var = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    asm_outside = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    comp_setup = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    comp_run = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    comp_matl = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    comp_tool = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    comp_fixture = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    comp_other = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    comp_fixed = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    comp_var = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    comp_outside = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    sub_matl = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    shrink_fact = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True, default=0)
    alt_item = models.CharField(max_length=30, blank=True, null=True)
    unit_weight = models.DecimalField(max_digits=11, decimal_places=5, blank=True, null=True, default=0)
    weight_units = models.CharField(max_length=3, blank=True, null=True)
    charfld4 = models.CharField(max_length=20, blank=True, null=True)
    cur_u_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    feat_type = models.CharField(max_length=1, blank=True, null=True, default="I")
    var_lead = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, default=0)
    feat_str = models.CharField(max_length=40, blank=True, null=True)
    next_config = models.SmallIntegerField(blank=True, null=True, default=1)
    feat_templ = models.CharField(max_length=55, blank=True, null=True)
    backflush = models.SmallIntegerField(blank=True, null=True, default=1)
    charfld1 = models.CharField(max_length=20, blank=True, null=True)
    charfld2 = models.CharField(max_length=20, blank=True, null=True)
    charfld3 = models.CharField(max_length=20, blank=True, null=True)
    decifld1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    decifld2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    decifld3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    logifld = models.SmallIntegerField(blank=True, null=True, default=0)
    datefld = models.DateTimeField(blank=True, null=True)
    track_ecn = models.SmallIntegerField(blank=True, null=True)
    u_ws_price = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    comm_code = models.ForeignKey(CommodityMst, models.DO_NOTHING, db_column='comm_code', blank=True, null=True)
    origin = models.CharField(max_length=2, blank=True, null=True)
    unit_mat_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    unit_duty_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    unit_freight_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    unit_brokerage_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    cur_mat_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    cur_duty_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    cur_freight_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    cur_brokerage_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    tax_code1 = models.CharField(max_length=6, blank=True, null=True)
    tax_code2 = models.CharField(max_length=6, blank=True, null=True)
    reservable = models.SmallIntegerField(blank=True, null=True, default=0)
    shelf_life = models.SmallIntegerField(blank=True, null=True)
    lot_prefix = models.CharField(max_length=15, blank=True, null=True)
    serial_prefix = models.CharField(max_length=30, blank=True, null=True)
    serial_length = models.SmallIntegerField(blank=True, null=True, default=30)
    issue_by = models.CharField(max_length=3, blank=True, null=True, default="LOC")
    serial_tracked = models.SmallIntegerField(blank=True, null=True, default=0)
    lot_tracked = models.SmallIntegerField(blank=True, null=True, default=0)
    cost_type = models.CharField(max_length=1, blank=True, null=True, default="S")
    matl_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    lbr_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    fovhd_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    vovhd_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    out_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    cur_matl_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    cur_lbr_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    cur_fovhd_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    cur_vovhd_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    cur_out_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    avg_matl_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    avg_lbr_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    avg_fovhd_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    avg_vovhd_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    avg_out_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    prod_type = models.CharField(max_length=1, blank=True, null=True, default="J")
    rate_per_day = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, default=1)
    mps_plan_fence = models.SmallIntegerField(blank=True, null=True)
    pass_req = models.SmallIntegerField(blank=True, null=True)
    lot_gen_exp = models.SmallIntegerField(blank=True, null=True, default=0)
    supply_site = models.ForeignKey('Site', models.DO_NOTHING, db_column='supply_site', blank=True, null=True)
    stat = models.CharField(max_length=1, blank=True, null=True)
    status_chg_user_code = models.CharField(max_length=3, blank=True, null=True)
    chg_date = models.DateTimeField(blank=True, null=True)
    reason_code = models.CharField(max_length=3, blank=True, null=True)
    supply_whse = models.CharField(max_length=4, blank=True, null=True)
    due_period = models.SmallIntegerField(blank=True, null=True)
    order_max = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    mrp_part = models.SmallIntegerField(blank=True, null=True, default=0)
    infinite_part = models.SmallIntegerField(blank=True, null=True, default=0)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag', default=0)  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    supply_tolerance_hrs = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=0)
    exp_lead_time = models.SmallIntegerField(default=0)
    var_exp_lead = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, default=0)
    buyer = models.CharField(max_length=60, blank=True, null=True)
    order_configurable = models.SmallIntegerField(default=0)
    job_configurable = models.SmallIntegerField(default=0)
    cfg_model = models.CharField(max_length=255, blank=True, null=True)
    auto_job = models.CharField(max_length=1)
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow', default=0)  # Field name made lowercase.
    mfg_supply_switching_active = models.SmallIntegerField(blank=True, null=True, default=0)
    time_fence_rule = models.SmallIntegerField(blank=True, null=True, default=0)
    time_fence_value = models.FloatField(blank=True, null=True, default=0)
    earliest_planned_po_receipt = models.DateTimeField(blank=True, null=True)
    use_reorder_point = models.SmallIntegerField(blank=True, null=True, default=0)
    reorder_point = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    fixed_order_qty = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    unit_insurance_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    unit_loc_frt_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    cur_insurance_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    cur_loc_frt_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    tax_free_matl = models.SmallIntegerField(default=0)
    tax_free_days = models.SmallIntegerField(blank=True, null=True, default=0)
    safety_stock_percent = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    tariff_classification = models.CharField(max_length=20, blank=True, null=True)
    lowdate = models.DateTimeField(blank=True, null=True)
    rcpt_rqmt = models.CharField(max_length=1)
    active_for_data_integration = models.SmallIntegerField(default=1)
    rcvd_over_po_qty_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    rcvd_under_po_qty_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    include_in_net_change_planning = models.SmallIntegerField(blank=True, null=True, default=0)
    kit = models.SmallIntegerField(default=0)
    print_kit_components = models.SmallIntegerField(default=0)
    safety_stock_rule = models.SmallIntegerField(blank=True, null=True, default=1)
    show_in_drop_down_list = models.SmallIntegerField(default=0)
    controlled_by_external_ics = models.SmallIntegerField(default=0)
    inventory_ucl_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    inventory_lcl_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    batch_release_attribute1 = models.FloatField(blank=True, null=True)
    batch_release_attribute2 = models.FloatField(blank=True, null=True)
    batch_release_attribute3 = models.FloatField(blank=True, null=True)
    picture = models.BinaryField(blank=True, null=True)
    active_for_customer_portal = models.SmallIntegerField(default=0)
    featured = models.SmallIntegerField(default=0)
    top_seller = models.SmallIntegerField(default=0)
    overview = models.TextField(blank=True, null=True)
    preassign_lots = models.SmallIntegerField(default=0)
    preassign_serials = models.SmallIntegerField(default=0)
    attr_group = models.CharField(max_length=10, blank=True, null=True)
    dimension_group = models.CharField(max_length=10, blank=True, null=True)
    lot_attr_group = models.CharField(max_length=10, blank=True, null=True)
    track_pieces = models.SmallIntegerField(default=0)
    bom_last_import_date = models.DateTimeField(blank=True, null=True)
    save_current_rev_upon_bom_import = models.SmallIntegerField(default=0)
    nafta_pref_crit = models.CharField(max_length=1, blank=True, null=True)
    subject_to_nafta_rvc = models.SmallIntegerField(default=0)
    producer = models.SmallIntegerField(default=0)
    nafta_country_of_origin = models.CharField(max_length=3, blank=True, null=True)
    must_use_future_rcpts_before_pln = models.SmallIntegerField(default=0)
    portal_pricing_site = models.CharField(max_length=8, blank=True, null=True)
    portal_pricing_enabled = models.SmallIntegerField(default=0)
    subject_to_excise_tax = models.SmallIntegerField(default=0)
    excise_tax_percent = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    freight_amt = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    item_content = models.SmallIntegerField(default=0)
    estimated_matl_use_up_date = models.DateTimeField(blank=True, null=True)
    last_matl_use_up_report_date = models.DateTimeField(blank=True, null=True)
    pp_length_linear_dimension = models.DecimalField(db_column='PP_length_linear_dimension', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    pp_width_linear_dimension = models.DecimalField(db_column='PP_width_linear_dimension', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    pp_height_linear_dimension = models.DecimalField(db_column='PP_height_linear_dimension', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    pp_density = models.DecimalField(db_column='PP_density', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase. # Field name made lowercase.
    pp_area = models.DecimalField(db_column='PP_area', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase. # Field name made lowercase.
    pp_bulk_mass = models.DecimalField(db_column='PP_bulk_mass', max_digits=11, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pp_ream_mass = models.DecimalField(db_column='PP_ream_mass', max_digits=11, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pp_grade = models.IntegerField(db_column='PP_grade', blank=True, null=True)  # Field name made lowercase.
    pp_abnormal_size = models.SmallIntegerField(db_column='PP_abnormal_size', default=0)  # Field name made lowercase.
    pp_paper_mass_basis = models.CharField(db_column='PP_paper_mass_basis', max_length=1, default=0)  # Field name made lowercase.
    charge_item = models.SmallIntegerField(blank=True, null=True)
    pull_up_safety_stock_rule = models.SmallIntegerField(default=0)
    pull_up_safety_stock_value = models.FloatField(default=0)
    commodity_jurisdiction = models.CharField(max_length=20, blank=True, null=True)
    eccn_usml_value = models.CharField(max_length=20, blank=True, null=True)
    export_compliance_program = models.CharField(max_length=20, blank=True, null=True)
    sched_b_num = models.CharField(max_length=20, blank=True, null=True)
    hts_code = models.CharField(max_length=50, blank=True, null=True)
    family_code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = IS_TEST
        db_table = 'item_mst'
        unique_together = (('item', 'lowdate', 'rcpt_rqmt', 'rowpointer', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('low_level', 'item', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('plan_code', 'item', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('product_code', 'item', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('rowpointer', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('serial_tracked', 'item', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('use_reorder_point', 'item', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('item', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'),)


class ItemMstAll(TruncatedModel):
    site_ref = models.CharField(primary_key=True, max_length=8)
    item = models.CharField(max_length=30)
    description = models.CharField(max_length=40, blank=True, null=True)
    qty_allocjob = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    u_m = models.CharField(max_length=3, blank=True, null=True)
    lead_time = models.SmallIntegerField(blank=True, null=True)
    lot_size = models.DecimalField(max_digits=18, decimal_places=8, blank=True, null=True)
    abc_code = models.CharField(max_length=1, blank=True, null=True)
    drawing_nbr = models.CharField(max_length=25, blank=True, null=True)
    product_code = models.CharField(max_length=10, blank=True, null=True)
    p_m_t_code = models.CharField(max_length=1, blank=True, null=True)
    cost_method = models.CharField(max_length=1, blank=True, null=True)
    lst_lot_size = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    lst_u_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    avg_u_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    job = models.CharField(max_length=20, blank=True, null=True)
    suffix = models.SmallIntegerField(blank=True, null=True)
    stocked = models.SmallIntegerField(blank=True, null=True)
    matl_type = models.CharField(max_length=1, blank=True, null=True)
    family_code = models.CharField(max_length=10, blank=True, null=True)
    days_supply = models.SmallIntegerField(blank=True, null=True)
    order_min = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    order_mult = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    plan_code = models.CharField(max_length=3, blank=True, null=True)
    mps_flag = models.SmallIntegerField(blank=True, null=True)
    accept_req = models.SmallIntegerField(blank=True, null=True)
    revision = models.CharField(max_length=8, blank=True, null=True)
    phantom_flag = models.SmallIntegerField(blank=True, null=True)
    plan_flag = models.SmallIntegerField(blank=True, null=True)
    paper_time = models.SmallIntegerField(blank=True, null=True)
    dock_time = models.SmallIntegerField(blank=True, null=True)
    shrink_fact = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    alt_item = models.CharField(max_length=30, blank=True, null=True)
    unit_weight = models.DecimalField(max_digits=11, decimal_places=5, blank=True, null=True)
    weight_units = models.CharField(max_length=3, blank=True, null=True)
    cur_u_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    feat_type = models.CharField(max_length=1, blank=True, null=True)
    var_lead = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    feat_str = models.CharField(max_length=40, blank=True, null=True)
    next_config = models.SmallIntegerField(blank=True, null=True)
    feat_templ = models.CharField(max_length=55, blank=True, null=True)
    backflush = models.SmallIntegerField(blank=True, null=True)
    track_ecn = models.SmallIntegerField(blank=True, null=True)
    u_ws_price = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    comm_code = models.CharField(max_length=12, blank=True, null=True)
    origin = models.CharField(max_length=2, blank=True, null=True)
    unit_mat_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    unit_duty_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    unit_freight_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    unit_brokerage_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    cur_mat_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    cur_duty_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    cur_freight_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    cur_brokerage_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    tax_code1 = models.CharField(max_length=6, blank=True, null=True)
    tax_code2 = models.CharField(max_length=6, blank=True, null=True)
    bflush_loc = models.CharField(max_length=15, blank=True, null=True)
    reservable = models.SmallIntegerField(blank=True, null=True)
    shelf_life = models.SmallIntegerField(blank=True, null=True)
    lot_prefix = models.CharField(max_length=15, blank=True, null=True)
    serial_prefix = models.CharField(max_length=30, blank=True, null=True)
    serial_length = models.SmallIntegerField(blank=True, null=True)
    issue_by = models.CharField(max_length=3, blank=True, null=True)
    serial_tracked = models.SmallIntegerField(blank=True, null=True)
    lot_tracked = models.SmallIntegerField(blank=True, null=True)
    cost_type = models.CharField(max_length=1, blank=True, null=True)
    matl_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    lbr_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    fovhd_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    vovhd_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    out_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    cur_matl_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    cur_lbr_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    cur_fovhd_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    cur_vovhd_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    cur_out_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    avg_matl_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    avg_lbr_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    avg_fovhd_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    avg_vovhd_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    avg_out_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    prod_type = models.CharField(max_length=1, blank=True, null=True)
    rate_per_day = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    mps_plan_fence = models.SmallIntegerField(blank=True, null=True)
    pass_req = models.SmallIntegerField(blank=True, null=True)
    supply_site = models.CharField(max_length=8, blank=True, null=True)
    stat = models.CharField(max_length=1, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', unique=True, max_length=36)  # Field name made lowercase.
    buyer = models.CharField(max_length=60, blank=True, null=True)
    order_configurable = models.SmallIntegerField()
    job_configurable = models.SmallIntegerField()
    cfg_model = models.CharField(max_length=255, blank=True, null=True)
    co_post_config = models.CharField(max_length=80, blank=True, null=True)
    job_post_config = models.CharField(max_length=80, blank=True, null=True)
    auto_job = models.CharField(max_length=1)
    auto_post = models.CharField(max_length=1)
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    unit_insurance_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    unit_loc_frt_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    cur_insurance_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    cur_loc_frt_cost = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    tax_free_matl = models.SmallIntegerField()
    tax_free_days = models.SmallIntegerField(blank=True, null=True)
    safety_stock_percent = models.DecimalField(max_digits=3, decimal_places=1)
    tariff_classification = models.CharField(max_length=20, blank=True, null=True)
    kit = models.SmallIntegerField()
    print_kit_components = models.SmallIntegerField()
    show_in_drop_down_list = models.SmallIntegerField(blank=True, null=True)
    low_level = models.SmallIntegerField(blank=True, null=True)
    active_for_data_integration = models.SmallIntegerField()
    inventory_lcl_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    inventory_ucl_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    supply_whse = models.CharField(max_length=4, blank=True, null=True)
    exp_lead_time = models.SmallIntegerField()
    var_exp_lead = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    mrp_part = models.SmallIntegerField(blank=True, null=True)
    infinite_part = models.SmallIntegerField(blank=True, null=True)
    supply_tolerance_hrs = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    time_fence_rule = models.SmallIntegerField(blank=True, null=True)
    time_fence_value = models.FloatField(blank=True, null=True)
    setupgroup = models.CharField(max_length=10, blank=True, null=True)
    order_max = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    use_reorder_point = models.SmallIntegerField(blank=True, null=True)
    reorder_point = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    fixed_order_qty = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    earliest_planned_po_receipt = models.DateTimeField(blank=True, null=True)
    reason_code = models.CharField(max_length=3, blank=True, null=True)
    chg_date = models.DateTimeField(blank=True, null=True)
    status_chg_user_code = models.CharField(max_length=3, blank=True, null=True)
    prod_mix = models.CharField(max_length=7, blank=True, null=True)
    rcvd_over_po_qty_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    rcvd_under_po_qty_tolerance = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    due_period = models.SmallIntegerField(blank=True, null=True)
    charfld1 = models.CharField(max_length=20, blank=True, null=True)
    charfld2 = models.CharField(max_length=20, blank=True, null=True)
    charfld3 = models.CharField(max_length=20, blank=True, null=True)
    decifld1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    decifld2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    decifld3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    logifld = models.SmallIntegerField(blank=True, null=True)
    datefld = models.DateTimeField(blank=True, null=True)
    preassign_lots = models.SmallIntegerField()
    preassign_serials = models.SmallIntegerField()
    overview = models.TextField(blank=True, null=True)
    active_for_customer_portal = models.SmallIntegerField()
    featured = models.SmallIntegerField()
    top_seller = models.SmallIntegerField()
    attr_group = models.CharField(max_length=10, blank=True, null=True)
    dimension_group = models.CharField(max_length=10, blank=True, null=True)
    lot_attr_group = models.CharField(max_length=10, blank=True, null=True)
    track_pieces = models.SmallIntegerField()
    bom_last_import_date = models.DateTimeField(blank=True, null=True)
    save_current_rev_upon_bom_import = models.SmallIntegerField()
    nafta_pref_crit = models.CharField(max_length=1, blank=True, null=True)
    subject_to_nafta_rvc = models.SmallIntegerField()
    producer = models.SmallIntegerField()
    nafta_country_of_origin = models.CharField(max_length=3, blank=True, null=True)
    change_date = models.DateTimeField(blank=True, null=True)
    portal_pricing_site = models.CharField(max_length=8, blank=True, null=True)
    portal_pricing_enabled = models.SmallIntegerField()
    subject_to_excise_tax = models.SmallIntegerField()
    excise_tax_percent = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    freight_amt = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    item_content = models.SmallIntegerField()
    estimated_matl_use_up_date = models.DateTimeField(blank=True, null=True)
    last_matl_use_up_report_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = IS_TEST
        db_table = 'item_mst_all'
        unique_together = (('site_ref', 'item'),)


class Site(TruncatedModel):
    site = models.CharField(primary_key=True, max_length=8)
    site_name = models.CharField(max_length=60, blank=True, null=True)
    lang_code = models.CharField(max_length=3, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    reports_to_site = models.CharField(max_length=8, blank=True, null=True)
    last_consolidated = models.DateTimeField(blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', unique=True, max_length=36)  # Field name made lowercase.
    description = models.CharField(max_length=40, blank=True, null=True)
    app_db_name = models.CharField(max_length=255, blank=True, null=True)
    time_zone = models.CharField(max_length=50, blank=True, null=True)
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    strings_table = models.CharField(max_length=128, blank=True, null=True)
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    message_bus_logical_id = models.CharField(max_length=256, blank=True, null=True)
    intranetlicensing = models.SmallIntegerField(db_column='IntranetLicensing')  # Field name made lowercase.
    reportoutputdirectory = models.CharField(db_column='ReportOutputDirectory', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tenantid = models.CharField(db_column='TenantID', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'site'


class UMMst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    u_m = models.CharField(primary_key=True, max_length=3)
    description = models.CharField(max_length=40, blank=True, null=True)
    precision_field = models.SmallIntegerField(db_column='precision_', blank=True, null=True)  # Field renamed because it ended with '_'.
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'u_m_mst'
        unique_together = (('rowpointer', 'site_ref'), ('u_m', 'site_ref'),)


class ChartMst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    acct = models.CharField(primary_key=True, max_length=12)
    type = models.CharField(max_length=1, blank=True, null=True)
    description = models.CharField(max_length=40, blank=True, null=True)
    eff_date = models.DateTimeField(blank=True, null=True)
    obs_date = models.DateTimeField(blank=True, null=True)
    reports_to_acct = models.CharField(max_length=12, blank=True, null=True)
    trans_method = models.CharField(max_length=1, blank=True, null=True)
    use_buy_rate = models.SmallIntegerField(blank=True, null=True)
    access_unit1 = models.CharField(max_length=1, blank=True, null=True)
    access_unit2 = models.CharField(max_length=1, blank=True, null=True)
    access_unit3 = models.CharField(max_length=1, blank=True, null=True)
    access_unit4 = models.CharField(max_length=1, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    acct_class = models.CharField(max_length=1, blank=True, null=True)
    is_control = models.SmallIntegerField()
    mx_applies_to_ietu = models.SmallIntegerField(db_column='MX_applies_to_ietu', blank=True, null=True)  # Field name made lowercase.
    mx_ietu_deduction_pct = models.DecimalField(db_column='MX_ietu_deduction_pct', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mx_diot_trans_type = models.CharField(db_column='MX_diot_trans_type', max_length=2, blank=True, null=True)  # Field name made lowercase.
    mx_ietu_class = models.CharField(db_column='MX_ietu_class', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'chart_mst'
        unique_together = (('rowpointer', 'site_ref'), ('acct', 'site_ref'),)


class ProdcodeMst(TruncatedModel):
    site_ref = models.ForeignKey(ChartMst, models.DO_NOTHING, db_column='site_ref')
    product_code = models.CharField(primary_key=True, max_length=10)
    markup = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    description = models.CharField(max_length=40, blank=True, null=True)
    fcst_ahead = models.SmallIntegerField(blank=True, null=True)
    fcst_behind = models.SmallIntegerField(blank=True, null=True)
    exc_ahead = models.SmallIntegerField(blank=True, null=True)
    exc_behind = models.SmallIntegerField(blank=True, null=True)
    exc_ahd_j = models.SmallIntegerField(blank=True, null=True)
    exc_bhd_j = models.SmallIntegerField(blank=True, null=True)
    cycle_tol = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    fmatlovhd = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    vmatlovhd = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    exp_doc_item = models.SmallIntegerField(blank=True, null=True)
    tax_free_days = models.SmallIntegerField(blank=True, null=True)
    purchovhd_type = models.CharField(max_length=1)
    purchovhd = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = IS_TEST
        db_table = 'prodcode_mst'
        unique_together = (('rowpointer', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('product_code', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref', 'site_ref'),)


class CustaddrMst(TruncatedModel):
    site_ref = models.CharField(max_length=8, db_column='site_ref', default="P2METCAM")
    cust_num = models.CharField(max_length=7)
    cust_seq = models.IntegerField()
    name = models.CharField(max_length=60, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=5, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    county = models.CharField(max_length=30, blank=True, null=True)
    country = models.ForeignKey(CountryMst, models.DO_NOTHING, db_column='country', blank=True, null=True)
    fax_num = models.CharField(max_length=25, blank=True, null=True)
    telex_num = models.CharField(max_length=25, blank=True, null=True)
    bal_method = models.CharField(max_length=1, blank=True, null=True)
    addr_1 = models.CharField(db_column='addr##1', max_length=50, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_2 = models.CharField(db_column='addr##2', max_length=50, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_3 = models.CharField(db_column='addr##3', max_length=50, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_4 = models.CharField(db_column='addr##4', max_length=50, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    credit_hold = models.SmallIntegerField(blank=True, null=True)
    credit_hold_user = models.CharField(max_length=3, blank=True, null=True)
    credit_hold_date = models.DateTimeField(blank=True, null=True)
    credit_hold_reason = models.CharField(max_length=3, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    corp_cust = models.CharField(max_length=7, blank=True, null=True)
    corp_cred = models.SmallIntegerField(blank=True, null=True)
    corp_address = models.SmallIntegerField(blank=True, null=True)
    amt_over_inv_amt = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)
    days_over_inv_due_date = models.SmallIntegerField(blank=True, null=True)
    ship_to_email = models.CharField(max_length=60, blank=True, null=True)
    bill_to_email = models.CharField(max_length=60, blank=True, null=True)
    internet_url = models.CharField(max_length=150, blank=True, null=True)
    internal_email_addr = models.CharField(max_length=60, blank=True, null=True)
    external_email_addr = models.CharField(max_length=60, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(primary_key=True, db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    carrier_account = models.CharField(max_length=25, blank=True, null=True)
    carrier_upcharge_pct = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    carrier_residential_indicator = models.SmallIntegerField()
    carrier_bill_to_transportation = models.CharField(max_length=5, blank=True, null=True)
    order_credit_limit = models.DecimalField(max_digits=23, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = IS_TEST
        db_table = 'custaddr_mst'


class ItempriceMst(TruncatedModel):
    site_ref = models.ForeignKey(ItemMst, models.DO_NOTHING, db_column='site_ref')
    item = models.ForeignKey(ItemMst, models.DO_NOTHING, db_column='item')
    effect_date = models.DateTimeField()
    curr_code = models.CharField(max_length=3)
    unit_price1 = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    unit_price2 = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    unit_price3 = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    unit_price4 = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    unit_price5 = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    unit_price6 = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    reprice = models.SmallIntegerField(blank=True, null=True)
    brk_qty_1 = models.DecimalField(db_column='brk_qty##1', max_digits=19, decimal_places=8, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    brk_qty_2 = models.DecimalField(db_column='brk_qty##2', max_digits=19, decimal_places=8, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    brk_qty_3 = models.DecimalField(db_column='brk_qty##3', max_digits=19, decimal_places=8, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    brk_qty_4 = models.DecimalField(db_column='brk_qty##4', max_digits=19, decimal_places=8, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    brk_qty_5 = models.DecimalField(db_column='brk_qty##5', max_digits=19, decimal_places=8, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    brk_price_1 = models.DecimalField(db_column='brk_price##1', max_digits=20, decimal_places=8, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    brk_price_2 = models.DecimalField(db_column='brk_price##2', max_digits=20, decimal_places=8, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    brk_price_3 = models.DecimalField(db_column='brk_price##3', max_digits=20, decimal_places=8, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    brk_price_4 = models.DecimalField(db_column='brk_price##4', max_digits=20, decimal_places=8, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    brk_price_5 = models.DecimalField(db_column='brk_price##5', max_digits=20, decimal_places=8, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    base_code_1 = models.CharField(db_column='base_code##1', max_length=2, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    base_code_2 = models.CharField(db_column='base_code##2', max_length=2, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    base_code_3 = models.CharField(db_column='base_code##3', max_length=2, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    base_code_4 = models.CharField(db_column='base_code##4', max_length=2, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    base_code_5 = models.CharField(db_column='base_code##5', max_length=2, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    dol_percent_1 = models.CharField(db_column='dol_percent##1', max_length=1, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    dol_percent_2 = models.CharField(db_column='dol_percent##2', max_length=1, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    dol_percent_3 = models.CharField(db_column='dol_percent##3', max_length=1, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    dol_percent_4 = models.CharField(db_column='dol_percent##4', max_length=1, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    dol_percent_5 = models.CharField(db_column='dol_percent##5', max_length=1, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    pricecode = models.CharField(max_length=10, db_column='pricecode', blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(primary_key=True, db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'itemprice_mst'
        unique_together = (('curr_code', 'item', 'effect_date', 'site_ref', 'site_ref'), ('item', 'effect_date', 'curr_code', 'site_ref', 'site_ref'), ('rowpointer', 'site_ref', 'site_ref'), ('item', 'curr_code', 'effect_date', 'site_ref', 'site_ref'),)


class Rgrp000Mst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    rgid = models.CharField(db_column='RGID', primary_key=True, max_length=30)  # Field name made lowercase.
    sltype = models.CharField(db_column='SLTYPE', max_length=1)  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=40)  # Field name made lowercase.
    allocatr = models.CharField(db_column='ALLOCATR', max_length=30)  # Field name made lowercase.
    allocrl = models.SmallIntegerField(db_column='ALLOCRL')  # Field name made lowercase.
    reallocfg = models.CharField(db_column='REALLOCFG', max_length=1)  # Field name made lowercase.
    batdefid = models.CharField(db_column='BATDEFID', max_length=30)  # Field name made lowercase.
    bufferin = models.FloatField(db_column='BUFFERIN')  # Field name made lowercase.
    bufferout = models.FloatField(db_column='BUFFEROUT')  # Field name made lowercase.
    infcap = models.FloatField(db_column='INFCAP')  # Field name made lowercase.
    infinitefg = models.CharField(db_column='INFINITEFG', max_length=1)  # Field name made lowercase.
    costtype = models.CharField(db_column='COSTTYPE', max_length=1)  # Field name made lowercase.
    loadfg = models.CharField(db_column='LOADFG', max_length=1)  # Field name made lowercase.
    quefg = models.CharField(db_column='QUEFG', max_length=1)  # Field name made lowercase.
    sumfg = models.CharField(db_column='SUMFG', max_length=1)  # Field name made lowercase.
    utilfg = models.CharField(db_column='UTILFG', max_length=1)  # Field name made lowercase.
    waitfg = models.CharField(db_column='WAITFG', max_length=1)  # Field name made lowercase.
    flags = models.IntegerField(db_column='FLAGS')  # Field name made lowercase.
    descrshadow = models.CharField(db_column='DESCRshadow', max_length=40, blank=True, null=True)  # Field name made lowercase.
    allocatrshadow = models.CharField(db_column='ALLOCATRshadow', max_length=30, blank=True, null=True)  # Field name made lowercase.
    batdefidshadow = models.CharField(db_column='BATDEFIDshadow', max_length=30, blank=True, null=True)  # Field name made lowercase.
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'RGRP000_mst'
        unique_together = (('rowpointer', 'site_ref'), ('rgid', 'site_ref'),)


class JrtresourcegroupMst(TruncatedModel):
    site_ref = models.ForeignKey(Rgrp000Mst, models.DO_NOTHING, db_column='site_ref')
    job = models.CharField(max_length=20)
    suffix = models.SmallIntegerField()
    oper_num = models.IntegerField()
    rgid = models.ForeignKey(Rgrp000Mst, models.DO_NOTHING, db_column='rgid')
    qty_resources = models.SmallIntegerField()
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(primary_key=True, db_column='RowPointer', max_length=36)  # Field name made lowercase.
    resactn = models.CharField(max_length=1)
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    sequence = models.IntegerField()

    class Meta:
        managed = IS_TEST
        db_table = 'jrtresourcegroup_mst'
        unique_together = (('rowpointer', 'site_ref'), ('job', 'suffix', 'oper_num', 'sequence', 'rgid', 'site_ref'),)


class Batch000Mst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    batdefid = models.CharField(db_column='BATDEFID', max_length=30)  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=40)  # Field name made lowercase.
    procplanid = models.CharField(db_column='PROCPLANID', max_length=36)  # Field name made lowercase.
    addovfg = models.CharField(db_column='ADDOVFG', max_length=1)  # Field name made lowercase.
    locremfg = models.CharField(db_column='LOCREMFG', max_length=1)  # Field name made lowercase.
    minquan = models.FloatField(db_column='MINQUAN')  # Field name made lowercase.
    maxquan = models.FloatField(db_column='MAXQUAN')  # Field name made lowercase.
    ovcycle = models.FloatField(db_column='OVCYCLE')  # Field name made lowercase.
    overrl = models.SmallIntegerField(db_column='OVERRL')  # Field name made lowercase.
    ovthresh = models.FloatField(db_column='OVTHRESH')  # Field name made lowercase.
    perffg = models.CharField(db_column='PERFFG', max_length=1)  # Field name made lowercase.
    perovfg = models.CharField(db_column='PEROVFG', max_length=1)  # Field name made lowercase.
    qatribid = models.CharField(db_column='QATRIBID', max_length=30)  # Field name made lowercase.
    quanrl = models.SmallIntegerField(db_column='QUANRL')  # Field name made lowercase.
    qvalue = models.FloatField(db_column='QVALUE')  # Field name made lowercase.
    satribid = models.CharField(db_column='SATRIBID', max_length=30)  # Field name made lowercase.
    seprl = models.SmallIntegerField(db_column='SEPRL')  # Field name made lowercase.
    sumfg = models.CharField(db_column='SUMFG', max_length=1)  # Field name made lowercase.
    costdist = models.CharField(db_column='COSTDIST', max_length=1)  # Field name made lowercase.
    flate = models.CharField(db_column='FLATE', max_length=8)  # Field name made lowercase.
    form = models.CharField(db_column='FORM', max_length=8)  # Field name made lowercase.
    relea = models.CharField(db_column='RELEA', max_length=8)  # Field name made lowercase.
    rlate = models.CharField(db_column='RLATE', max_length=8)  # Field name made lowercase.
    xpfla = models.IntegerField(db_column='XPFLA')  # Field name made lowercase.
    xpfor = models.IntegerField(db_column='XPFOR')  # Field name made lowercase.
    xprel = models.IntegerField(db_column='XPREL')  # Field name made lowercase.
    xprla = models.IntegerField(db_column='XPRLA')  # Field name made lowercase.
    ypfla = models.IntegerField(db_column='YPFLA')  # Field name made lowercase.
    ypfor = models.IntegerField(db_column='YPFOR')  # Field name made lowercase.
    yprel = models.IntegerField(db_column='YPREL')  # Field name made lowercase.
    yprla = models.IntegerField(db_column='YPRLA')  # Field name made lowercase.
    job = models.CharField(db_column='JOB', max_length=20)  # Field name made lowercase.
    suffix = models.SmallIntegerField(db_column='SUFFIX')  # Field name made lowercase.
    item = models.CharField(db_column='ITEM', max_length=30)  # Field name made lowercase.
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', primary_key=True, max_length=36)  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'BATCH000_mst'
        unique_together = (('batdefid', 'site_ref'), ('rowpointer', 'site_ref'),)


class ProductionBatchMst(TruncatedModel):
    site_ref = models.ForeignKey(Batch000Mst, models.DO_NOTHING, db_column='site_ref')
    prod_batch_id = models.IntegerField(primary_key=True)
    batch_definition = models.ForeignKey(Batch000Mst, models.DO_NOTHING)
    batch_job = models.CharField(max_length=20)
    batch_suffix = models.SmallIntegerField()
    status = models.CharField(max_length=1)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'production_batch_mst'
        unique_together = (('rowpointer', 'site_ref'), ('prod_batch_id', 'site_ref'),)


class LookuphdrMst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    tabid = models.CharField(primary_key=True, max_length=30)
    matrixtype = models.CharField(max_length=1)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(db_column='RowPointer', max_length=36)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'lookuphdr_mst'
        unique_together = (('rowpointer', 'site_ref'), ('tabid', 'site_ref'),)


class JrtSchMst(TruncatedModel):
    site_ref = models.CharField(max_length=8)
    job = models.CharField(max_length=20)
    suffix = models.SmallIntegerField()
    oper_num = models.IntegerField()
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    sched_ticks = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    sched_off = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    move_ticks = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    queue_ticks = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    freeze_sch = models.SmallIntegerField(blank=True, null=True)
    start_tick = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    end_tick = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    setup_ticks = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    run_ticks_lbr = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    run_ticks_mch = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    pcs_per_lbr_hr = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    pcs_per_mch_hr = models.DecimalField(max_digits=19, decimal_places=8, blank=True, null=True)
    move_hrs = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    queue_hrs = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sched_hrs = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    setup_hrs = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    run_lbr_hrs = models.DecimalField(max_digits=15, decimal_places=8, blank=True, null=True)
    run_mch_hrs = models.DecimalField(max_digits=15, decimal_places=8, blank=True, null=True)
    offset_hrs = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    noteexistsflag = models.SmallIntegerField(db_column='NoteExistsFlag')  # Field name made lowercase.
    recorddate = models.DateTimeField(db_column='RecordDate')  # Field name made lowercase.
    rowpointer = models.CharField(primary_key=True, db_column='RowPointer', max_length=36)  # Field name made lowercase.
    sched_drv = models.CharField(max_length=1)
    matrixtype = models.CharField(max_length=1, blank=True, null=True)
    tabid = models.ForeignKey('LookuphdrMst', models.DO_NOTHING, db_column='tabid', blank=True, null=True)
    plannerstep = models.SmallIntegerField(blank=True, null=True)
    whenrule = models.SmallIntegerField(blank=True, null=True)
    setuprule = models.SmallIntegerField(blank=True, null=True)
    setuprgid = models.ForeignKey(Rgrp000Mst, models.DO_NOTHING, db_column='setuprgid', blank=True, null=True)
    crsbrkrule = models.SmallIntegerField(blank=True, null=True)
    splitsize = models.FloatField(blank=True, null=True)
    finish_hrs = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=30)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    schedsteprule = models.SmallIntegerField(blank=True, null=True)
    inworkflow = models.SmallIntegerField(db_column='InWorkflow')  # Field name made lowercase.
    allow_reallocation = models.SmallIntegerField()
    batch_definition = models.ForeignKey(Batch000Mst, models.DO_NOTHING, blank=True, null=True)
    prod_batch = models.ForeignKey('ProductionBatchMst', models.DO_NOTHING, blank=True, null=True)
    splitrule = models.SmallIntegerField(blank=True, null=True)
    splitgroup = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = IS_TEST
        db_table = 'jrt_sch_mst'
        unique_together = (('rowpointer', 'site_ref', 'site_ref', 'site_ref', 'site_ref'), ('job', 'suffix', 'oper_num', 'site_ref', 'site_ref', 'site_ref', 'site_ref'),)
