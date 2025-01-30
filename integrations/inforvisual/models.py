# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = IS_TEST` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from inforvisual.settings import IS_TEST
from baseintegration.utils.truncated_model import TruncatedModel


class Account(TruncatedModel):
    id = models.CharField(db_column='ID', primary_key=True, max_length=30)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=120, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1)  # Field name made lowercase.
    summary_account = models.CharField(db_column='SUMMARY_ACCOUNT', max_length=1)  # Field name made lowercase.
    parent_acct_id = models.CharField(db_column='PARENT_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    currency = models.ForeignKey('Currency', models.DO_NOTHING, db_column='CURRENCY_ID', blank=True, null=True)  # Field name made lowercase.
    revalue = models.CharField(db_column='REVALUE', max_length=1)  # Field name made lowercase.
    project_account = models.CharField(db_column='PROJECT_ACCOUNT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    active_flag = models.CharField(db_column='ACTIVE_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    status_eff_date = models.DateTimeField(db_column='STATUS_EFF_DATE')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ACCOUNT'


class Commodity(TruncatedModel):  # Field name made lowercase.
    code = models.CharField(db_column='CODE', primary_key=True, max_length=15)  # Field name made lowercase.
    univ_plan_material = models.CharField(db_column='UNIV_PLAN_MATERIAL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=80, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'COMMODITY'


class Contact(TruncatedModel):
    id = models.CharField(db_column='ID', primary_key=True, max_length=25)  # Field name made lowercase.
    first_name = models.CharField(db_column='FIRST_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    last_name = models.CharField(db_column='LAST_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    middle_name = models.CharField(db_column='MIDDLE_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    middle_initial = models.CharField(db_column='MIDDLE_INITIAL', max_length=2, blank=True, null=True)  # Field name made lowercase.
    position = models.CharField(db_column='POSITION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    salutation = models.CharField(db_column='SALUTATION', max_length=60, blank=True, null=True)  # Field name made lowercase.
    honorific = models.CharField(db_column='HONORIFIC', max_length=15, blank=True, null=True)  # Field name made lowercase.
    country_dial_code = models.CharField(db_column='COUNTRY_DIAL_CODE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='PHONE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    phone_ext = models.CharField(db_column='PHONE_EXT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='MOBILE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_1 = models.CharField(db_column='ADDR_1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_2 = models.CharField(db_column='ADDR_2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_3 = models.CharField(db_column='ADDR_3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='CITY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='STATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(db_column='ZIPCODE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='COUNTRY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    contact_country_id = models.CharField(db_column='CONTACT_COUNTRY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    web_user_id = models.CharField(db_column='WEB_USER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    web_password = models.CharField(db_column='WEB_PASSWORD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    preferred_contact_method = models.CharField(db_column='PREFERRED_CONTACT_METHOD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gender_code = models.CharField(db_column='GENDER_CODE', max_length=1)  # Field name made lowercase.
    marital_status = models.CharField(db_column='MARITAL_STATUS', max_length=1)  # Field name made lowercase.
    birth_date = models.DateTimeField(db_column='BIRTH_DATE', blank=True, null=True)  # Field name made lowercase.
    user_1 = models.CharField(db_column='USER_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_2 = models.CharField(db_column='USER_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_3 = models.CharField(db_column='USER_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_4 = models.CharField(db_column='USER_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_5 = models.CharField(db_column='USER_5', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_6 = models.CharField(db_column='USER_6', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_7 = models.CharField(db_column='USER_7', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_8 = models.CharField(db_column='USER_8', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_9 = models.CharField(db_column='USER_9', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_10 = models.CharField(db_column='USER_10', max_length=80, blank=True, null=True)  # Field name made lowercase.
    active_flag = models.CharField(db_column='ACTIVE_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    no_call_phone = models.CharField(db_column='NO_CALL_PHONE', max_length=1)  # Field name made lowercase.
    no_call_mobile = models.CharField(db_column='NO_CALL_MOBILE', max_length=1)  # Field name made lowercase.
    no_email = models.CharField(db_column='NO_EMAIL', max_length=1)  # Field name made lowercase.
    url_twitter = models.CharField(db_column='URL_TWITTER', max_length=255, blank=True, null=True)  # Field name made lowercase.
    url_facebook = models.CharField(db_column='URL_FACEBOOK', max_length=255, blank=True, null=True)  # Field name made lowercase.
    url_myspace = models.CharField(db_column='URL_MYSPACE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    url_linkedin = models.CharField(db_column='URL_LINKEDIN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    url_hyves = models.CharField(db_column='URL_HYVES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    udf_layout_id = models.CharField(db_column='UDF_LAYOUT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CONTACT'


class Customer(TruncatedModel):  # Field name made lowercase.
    id = models.CharField(db_column='ID', primary_key=True, max_length=15)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_1 = models.CharField(db_column='ADDR_1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_2 = models.CharField(db_column='ADDR_2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_3 = models.CharField(db_column='ADDR_3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='CITY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='STATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(db_column='ZIPCODE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='COUNTRY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    contact_first_name = models.CharField(db_column='CONTACT_FIRST_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact_last_name = models.CharField(db_column='CONTACT_LAST_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact_initial = models.CharField(db_column='CONTACT_INITIAL', max_length=2, blank=True, null=True)  # Field name made lowercase.
    contact_position = models.CharField(db_column='CONTACT_POSITION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    contact_honorific = models.CharField(db_column='CONTACT_HONORIFIC', max_length=15, blank=True, null=True)  # Field name made lowercase.
    contact_salutation = models.CharField(db_column='CONTACT_SALUTATION', max_length=60, blank=True, null=True)  # Field name made lowercase.
    contact_phone = models.CharField(db_column='CONTACT_PHONE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contact_fax = models.CharField(db_column='CONTACT_FAX', max_length=20, blank=True, null=True)  # Field name made lowercase.
    bill_to_name = models.CharField(db_column='BILL_TO_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bill_to_addr_1 = models.CharField(db_column='BILL_TO_ADDR_1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bill_to_addr_2 = models.CharField(db_column='BILL_TO_ADDR_2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bill_to_addr_3 = models.CharField(db_column='BILL_TO_ADDR_3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bill_to_city = models.CharField(db_column='BILL_TO_CITY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    bill_to_state = models.CharField(db_column='BILL_TO_STATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bill_to_zipcode = models.CharField(db_column='BILL_TO_ZIPCODE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bill_to_country = models.CharField(db_column='BILL_TO_COUNTRY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    discount_code = models.CharField(db_column='DISCOUNT_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    free_on_board = models.CharField(db_column='FREE_ON_BOARD', max_length=25, blank=True, null=True)  # Field name made lowercase.
    ship_via = models.CharField(db_column='SHIP_VIA', max_length=40, blank=True, null=True)  # Field name made lowercase.
    salesrep_id = models.CharField(db_column='SALESREP_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    territory = models.CharField(db_column='TERRITORY', max_length=15, blank=True, null=True)  # Field name made lowercase.
    currency_id = models.CharField(db_column='CURRENCY_ID', max_length=15)  # Field name made lowercase.
    def_sls_tax_grp_id = models.CharField(db_column='DEF_SLS_TAX_GRP_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    sic_code = models.CharField(db_column='SIC_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    ind_code = models.CharField(db_column='IND_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    finance_charge = models.DecimalField(db_column='FINANCE_CHARGE', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    tax_exempt = models.CharField(db_column='TAX_EXEMPT', max_length=1)  # Field name made lowercase.
    tax_id_number = models.CharField(db_column='TAX_ID_NUMBER', max_length=25, blank=True, null=True)  # Field name made lowercase.
    backorder_flag = models.CharField(db_column='BACKORDER_FLAG', max_length=1)  # Field name made lowercase.
    terms_net_type = models.CharField(db_column='TERMS_NET_TYPE', max_length=1)  # Field name made lowercase.
    terms_net_days = models.SmallIntegerField(db_column='TERMS_NET_DAYS', blank=True, null=True)  # Field name made lowercase.
    terms_net_date = models.DateTimeField(db_column='TERMS_NET_DATE', blank=True, null=True)  # Field name made lowercase.
    terms_disc_type = models.CharField(db_column='TERMS_DISC_TYPE', max_length=1)  # Field name made lowercase.
    terms_disc_days = models.SmallIntegerField(db_column='TERMS_DISC_DAYS', blank=True, null=True)  # Field name made lowercase.
    terms_disc_date = models.DateTimeField(db_column='TERMS_DISC_DATE', blank=True, null=True)  # Field name made lowercase.
    terms_disc_percent = models.DecimalField(db_column='TERMS_DISC_PERCENT', max_digits=5, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    terms_description = models.CharField(db_column='TERMS_DESCRIPTION', max_length=80, blank=True, null=True)  # Field name made lowercase.
    freight_terms = models.CharField(db_column='FREIGHT_TERMS', max_length=1)  # Field name made lowercase.
    dunning_letters = models.CharField(db_column='DUNNING_LETTERS', max_length=1)  # Field name made lowercase.
    last_order_date = models.DateTimeField(db_column='LAST_ORDER_DATE', blank=True, null=True)  # Field name made lowercase.
    open_date = models.DateTimeField(db_column='OPEN_DATE', blank=True, null=True)  # Field name made lowercase.
    modify_date = models.DateTimeField(db_column='MODIFY_DATE', blank=True, null=True)  # Field name made lowercase.
    user_1 = models.CharField(db_column='USER_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_2 = models.CharField(db_column='USER_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_3 = models.CharField(db_column='USER_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_4 = models.CharField(db_column='USER_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_5 = models.CharField(db_column='USER_5', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_6 = models.CharField(db_column='USER_6', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_7 = models.CharField(db_column='USER_7', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_8 = models.CharField(db_column='USER_8', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_9 = models.CharField(db_column='USER_9', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_10 = models.CharField(db_column='USER_10', max_length=80, blank=True, null=True)  # Field name made lowercase.
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    carrier_id = models.CharField(db_column='CARRIER_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    tax_on_wholesale = models.CharField(db_column='TAX_ON_WHOLESALE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    def_recv_acct_id = models.CharField(db_column='DEF_RECV_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf_layout_id = models.CharField(db_column='UDF_LAYOUT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    arrival_code = models.CharField(db_column='ARRIVAL_CODE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    trans_code = models.CharField(db_column='TRANS_CODE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    country_id = models.CharField(db_column='COUNTRY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    nature_of_trans = models.IntegerField(db_column='NATURE_OF_TRANS', blank=True, null=True)  # Field name made lowercase.
    mode_of_transport = models.IntegerField(db_column='MODE_OF_TRANSPORT', blank=True, null=True)  # Field name made lowercase.
    siret_number = models.DecimalField(db_column='SIRET_NUMBER', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    vat_registration = models.CharField(db_column='VAT_REGISTRATION', max_length=25, blank=True, null=True)  # Field name made lowercase.
    vat_book_code_i = models.CharField(db_column='VAT_BOOK_CODE_I', max_length=5, blank=True, null=True)  # Field name made lowercase.
    vat_book_code_m = models.CharField(db_column='VAT_BOOK_CODE_M', max_length=5, blank=True, null=True)  # Field name made lowercase.
    vat_exempt = models.CharField(db_column='VAT_EXEMPT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shipto_id = models.CharField(db_column='SHIPTO_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rma_required = models.CharField(db_column='RMA_REQUIRED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    contact_mobile = models.CharField(db_column='CONTACT_MOBILE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contact_email = models.CharField(db_column='CONTACT_EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    def_trans_currency = models.CharField(db_column='DEF_TRANS_CURRENCY', max_length=15, blank=True, null=True)  # Field name made lowercase.
    def_lbl_format_id = models.CharField(db_column='DEF_LBL_FORMAT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    accept_early = models.CharField(db_column='ACCEPT_EARLY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    days_early = models.SmallIntegerField(db_column='DAYS_EARLY', blank=True, null=True)  # Field name made lowercase.
    vat_discounted = models.CharField(db_column='VAT_DISCOUNTED', max_length=1)  # Field name made lowercase.
    web_user_id = models.CharField(db_column='WEB_USER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    web_password = models.CharField(db_column='WEB_PASSWORD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    priority = models.SmallIntegerField(db_column='PRIORITY', blank=True, null=True)  # Field name made lowercase.
    language_id = models.CharField(db_column='LANGUAGE_ID', max_length=2, blank=True, null=True)  # Field name made lowercase.
    bill_language_id = models.CharField(db_column='BILL_LANGUAGE_ID', max_length=2, blank=True, null=True)  # Field name made lowercase.
    def_ack_id = models.CharField(db_column='DEF_ACK_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    primarily_edi = models.CharField(db_column='PRIMARILY_EDI', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vat_always_disc = models.CharField(db_column='VAT_ALWAYS_DISC', max_length=1)  # Field name made lowercase.
    vat_code = models.CharField(db_column='VAT_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vat_override_seq = models.CharField(db_column='VAT_OVERRIDE_SEQ', max_length=1)  # Field name made lowercase.
    return_trans = models.IntegerField(db_column='RETURN_TRANS', blank=True, null=True)  # Field name made lowercase.
    cash_percent_var = models.CharField(db_column='CASH_PERCENT_VAR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cash_min_var = models.DecimalField(db_column='CASH_MIN_VAR', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    cash_max_var = models.DecimalField(db_column='CASH_MAX_VAR', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    take_disc_days = models.DecimalField(db_column='TAKE_DISC_DAYS', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    market_id = models.CharField(db_column='MARKET_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    credit_card_id = models.CharField(db_column='CREDIT_CARD_ID', max_length=250, blank=True, null=True)  # Field name made lowercase.
    web_url = models.CharField(db_column='WEB_URL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ups_account_id = models.CharField(db_column='UPS_ACCOUNT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    generate_asn = models.CharField(db_column='GENERATE_ASN', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hold_transfer_asn = models.CharField(db_column='HOLD_TRANSFER_ASN', max_length=1, blank=True, null=True)  # Field name made lowercase.
    customs_doc_print = models.CharField(db_column='CUSTOMS_DOC_PRINT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    suppress_ar_print = models.CharField(db_column='SUPPRESS_AR_PRINT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    accept_830 = models.CharField(db_column='ACCEPT_830', max_length=1, blank=True, null=True)  # Field name made lowercase.
    accept_862 = models.CharField(db_column='ACCEPT_862', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pool_code = models.CharField(db_column='POOL_CODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    inter_consignee = models.CharField(db_column='INTER_CONSIGNEE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    consol_ship_line = models.CharField(db_column='CONSOL_SHIP_LINE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pallet_details_req = models.CharField(db_column='PALLET_DETAILS_REQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    match_inv_to_pack = models.CharField(db_column='MATCH_INV_TO_PACK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    allow_over_paymnt = models.CharField(db_column='ALLOW_OVER_PAYMNT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    allow_adj_invoice = models.CharField(db_column='ALLOW_ADJ_INVOICE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    def_gl_acct_id = models.CharField(db_column='DEF_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    liq_gl_acct_id = models.CharField(db_column='LIQ_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pbc_gl_acct_id = models.CharField(db_column='PBC_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    generate_wsa = models.CharField(db_column='GENERATE_WSA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hold_transfer_wsa = models.CharField(db_column='HOLD_TRANSFER_WSA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    active_flag = models.CharField(db_column='ACTIVE_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    suppress_print_inv_non_edi = models.CharField(db_column='SUPPRESS_PRINT_INV_NON_EDI', max_length=1, blank=True, null=True)  # Field name made lowercase.
    open_oldest_recv = models.DateTimeField(db_column='OPEN_OLDEST_RECV', blank=True, null=True)  # Field name made lowercase.
    status_eff_date = models.DateTimeField(db_column='STATUS_EFF_DATE')  # Field name made lowercase.
    price_group = models.CharField(db_column='PRICE_GROUP', max_length=15, blank=True, null=True)  # Field name made lowercase.
    suppress_print_cust_stmt = models.CharField(db_column='SUPPRESS_PRINT_CUST_STMT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    def_terms_id = models.CharField(db_column='DEF_TERMS_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    customer_group_id = models.CharField(db_column='CUSTOMER_GROUP_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    internal_customer = models.CharField(db_column='INTERNAL_CUSTOMER', max_length=1, blank=True, null=True)  # Field name made lowercase.
    contact_phone_ext = models.CharField(db_column='CONTACT_PHONE_EXT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    email_cust_on_new_order = models.CharField(db_column='EMAIL_CUST_ON_NEW_ORDER', max_length=1)  # Field name made lowercase.
    email_cust_on_chg_order = models.CharField(db_column='EMAIL_CUST_ON_CHG_ORDER', max_length=1)  # Field name made lowercase.
    email_cust_on_shipment = models.CharField(db_column='EMAIL_CUST_ON_SHIPMENT', max_length=1)  # Field name made lowercase.
    email_empl_on_new_order = models.CharField(db_column='EMAIL_EMPL_ON_NEW_ORDER', max_length=1)  # Field name made lowercase.
    email_empl_on_chg_order = models.CharField(db_column='EMAIL_EMPL_ON_CHG_ORDER', max_length=1)  # Field name made lowercase.
    email_empl_on_shipment = models.CharField(db_column='EMAIL_EMPL_ON_SHIPMENT', max_length=1)  # Field name made lowercase.
    email_empl_on_inv_paid = models.CharField(db_column='EMAIL_EMPL_ON_INV_PAID', max_length=1)  # Field name made lowercase.
    customer_country_id = models.CharField(db_column='CUSTOMER_COUNTRY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    bill_to_country_id = models.CharField(db_column='BILL_TO_COUNTRY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CUSTOMER'


class CustContact(TruncatedModel):
    customer = models.OneToOneField(Customer, models.DO_NOTHING, db_column='CUSTOMER_ID', primary_key=True)  # Field name made lowercase.
    contact_no = models.SmallIntegerField(db_column='CONTACT_NO', blank=True, null=True)  # Field name made lowercase.
    contact = models.ForeignKey(Contact, models.DO_NOTHING, db_column='CONTACT_ID')  # Field name made lowercase.
    primary_contact = models.CharField(db_column='PRIMARY_CONTACT', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CUST_CONTACT'
        unique_together = (('customer', 'contact'),)


class CustomerBinary(TruncatedModel):  # Field name made lowercase.
    customer = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CUSTOMER_ID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1)  # Field name made lowercase.
    bits = models.BinaryField(db_column='BITS', blank=True, null=True)  # Field name made lowercase.
    bits_length = models.IntegerField(db_column='BITS_LENGTH')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CUSTOMER_BINARY'
        unique_together = (('customer', 'type'),)


class CustomerContact(TruncatedModel):  # Field name made lowercase.
    customer = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CUSTOMER_ID')  # Field name made lowercase.
    contact_no = models.SmallIntegerField(db_column='CONTACT_NO', primary_key=True)  # Field name made lowercase.
    contact_first_name = models.CharField(db_column='CONTACT_FIRST_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact_last_name = models.CharField(db_column='CONTACT_LAST_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact_position = models.CharField(db_column='CONTACT_POSITION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    contact_initial = models.CharField(db_column='CONTACT_INITIAL', max_length=2, blank=True, null=True)  # Field name made lowercase.
    contact_honorific = models.CharField(db_column='CONTACT_HONORIFIC', max_length=15, blank=True, null=True)  # Field name made lowercase.
    contact_phone = models.CharField(db_column='CONTACT_PHONE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contact_fax = models.CharField(db_column='CONTACT_FAX', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contact_mobile = models.CharField(db_column='CONTACT_MOBILE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contact_email = models.CharField(db_column='CONTACT_EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    web_user_id = models.CharField(max_length=20, blank=True, null=True)
    web_password = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = IS_TEST
        db_table = 'CUSTOMER_CONTACT'
        unique_together = (('customer', 'contact_no'),)


class CustAddress(TruncatedModel):
    customer = models.OneToOneField(Customer, models.DO_NOTHING, db_column='CUSTOMER_ID', primary_key=True)  # Field name made lowercase.
    addr_no = models.IntegerField(db_column='ADDR_NO')  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_1 = models.CharField(db_column='ADDR_1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_2 = models.CharField(db_column='ADDR_2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_3 = models.CharField(db_column='ADDR_3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='CITY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='STATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(db_column='ZIPCODE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='COUNTRY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cust_addr_country_id = models.CharField(db_column='CUST_ADDR_COUNTRY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    tax_id_number = models.CharField(db_column='TAX_ID_NUMBER', max_length=25, blank=True, null=True)  # Field name made lowercase.
    tax_exempt = models.CharField(db_column='TAX_EXEMPT', max_length=1)  # Field name made lowercase.
    territory = models.CharField(db_column='TERRITORY', max_length=15, blank=True, null=True)  # Field name made lowercase.
    ship_via = models.CharField(db_column='SHIP_VIA', max_length=40, blank=True, null=True)  # Field name made lowercase.
    free_on_board = models.CharField(db_column='FREE_ON_BOARD', max_length=25, blank=True, null=True)  # Field name made lowercase.
    siret_number = models.DecimalField(db_column='SIRET_NUMBER', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    shipto_id = models.CharField(db_column='SHIPTO_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    priority_code = models.CharField(db_column='PRIORITY_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    fill_rate_type = models.CharField(db_column='FILL_RATE_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    warehouse_id = models.CharField(db_column='WAREHOUSE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    compliance_label = models.CharField(db_column='COMPLIANCE_LABEL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    consolidate_orders = models.CharField(db_column='CONSOLIDATE_ORDERS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vat_registration = models.CharField(db_column='VAT_REGISTRATION', max_length=25, blank=True, null=True)  # Field name made lowercase.
    carrier_id = models.CharField(db_column='CARRIER_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    order_fill_rate = models.DecimalField(db_column='ORDER_FILL_RATE', max_digits=5, decimal_places=2)  # Field name made lowercase.
    language_id = models.CharField(db_column='LANGUAGE_ID', max_length=2, blank=True, null=True)  # Field name made lowercase.
    user_1 = models.CharField(db_column='USER_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_2 = models.CharField(db_column='USER_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_3 = models.CharField(db_column='USER_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_4 = models.CharField(db_column='USER_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_5 = models.CharField(db_column='USER_5', max_length=80, blank=True, null=True)  # Field name made lowercase
    user_6 = models.CharField(db_column='USER_6', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_7 = models.CharField(db_column='USER_7', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_8 = models.CharField(db_column='USER_8', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_9 = models.CharField(db_column='USER_9', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_10 = models.CharField(db_column='USER_10', max_length=80, blank=True, null=True)  # Field name made lowercase.
    udf_layout_id = models.CharField(db_column='UDF_LAYOUT_ID', max_length=80, blank=True, null=True)  # Field name made lowercase.
    generate_asn = models.CharField(db_column='GENERATE_ASN', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hold_transfer_asn = models.CharField(db_column='HOLD_TRANSFER_ASN', max_length=1, blank=True, null=True)  # Field name made lowercase.
    customs_doc_print = models.CharField(db_column='CUSTOMS_DOC_PRINT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    suppress_ar_print = models.CharField(db_column='SUPPRESS_AR_PRINT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    accept_830 = models.CharField(db_column='ACCEPT_830', max_length=1, blank=True, null=True)  # Field name made lowercase.
    accept_862 = models.CharField(db_column='ACCEPT_862', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pool_point_id = models.CharField(db_column='POOL_POINT_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pool_code = models.CharField(db_column='POOL_CODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dock_code_field = models.CharField(db_column='DOCK_CODE_FIELD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    duty_brokerage = models.CharField(db_column='DUTY_BROKERAGE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    material_issuer = models.CharField(db_column='MATERIAL_ISSUER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    trans_method_code = models.CharField(db_column='TRANS_METHOD_CODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    equipment_descr = models.CharField(db_column='EQUIPMENT_DESCR', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lading_code = models.CharField(db_column='LADING_CODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    model_year = models.CharField(db_column='MODEL_YEAR', max_length=20, blank=True, null=True)  # Field name made lowercase.
    handling_id = models.CharField(db_column='HANDLING_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    allow_charge_no = models.CharField(db_column='ALLOW_CHARGE_NO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    non_return_code = models.CharField(db_column='NON_RETURN_CODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mixed_code = models.CharField(db_column='MIXED_CODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    trading_partner = models.CharField(db_column='TRADING_PARTNER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    transit_time = models.DecimalField(db_column='TRANSIT_TIME', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    inter_consignee = models.CharField(db_column='INTER_CONSIGNEE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    consol_ship_line = models.CharField(db_column='CONSOL_SHIP_LINE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vat_code = models.CharField(db_column='VAT_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vat_override_seq = models.CharField(db_column='VAT_OVERRIDE_SEQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pallet_details_req = models.CharField(db_column='PALLET_DETAILS_REQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    match_inv_to_pack = models.CharField(db_column='MATCH_INV_TO_PACK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    generate_wsa = models.CharField(db_column='GENERATE_WSA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hold_transfer_wsa = models.CharField(db_column='HOLD_TRANSFER_WSA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    price_group = models.CharField(db_column='PRICE_GROUP', max_length=15, blank=True, null=True)  # Field name made lowercase.
    active_flag = models.CharField(db_column='ACTIVE_FLAG', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CUST_ADDRESS'


class CustomerOrder(TruncatedModel):  # Field name made lowercase.
    id = models.CharField(db_column='ID', primary_key=True, max_length=15)  # Field name made lowercase.
    customer = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CUSTOMER_ID')  # Field name made lowercase.
    customer_po_ref = models.CharField(db_column='CUSTOMER_PO_REF', max_length=40, blank=True, null=True)  # Field name made lowercase.
    contact_first_name = models.CharField(db_column='CONTACT_FIRST_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact_last_name = models.CharField(db_column='CONTACT_LAST_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact_initial = models.CharField(db_column='CONTACT_INITIAL', max_length=2, blank=True, null=True)  # Field name made lowercase.
    contact_position = models.CharField(db_column='CONTACT_POSITION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    contact_honorific = models.CharField(db_column='CONTACT_HONORIFIC', max_length=15, blank=True, null=True)  # Field name made lowercase.
    contact_salutation = models.CharField(db_column='CONTACT_SALUTATION', max_length=60, blank=True, null=True)  # Field name made lowercase.
    contact_phone = models.CharField(db_column='CONTACT_PHONE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contact_fax = models.CharField(db_column='CONTACT_FAX', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ship_to_addr_no = models.IntegerField(db_column='SHIP_TO_ADDR_NO', blank=True, null=True)  # Field name made lowercase.
    free_on_board = models.CharField(db_column='FREE_ON_BOARD', max_length=25, blank=True, null=True)  # Field name made lowercase.
    ship_via = models.CharField(db_column='SHIP_VIA', max_length=40, blank=True, null=True)  # Field name made lowercase.
    territory = models.CharField(db_column='TERRITORY', max_length=15, blank=True, null=True)  # Field name made lowercase.
    discount_code = models.CharField(db_column='DISCOUNT_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    sales_tax_group_id = models.CharField(db_column='SALES_TAX_GROUP_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    salesrep_id = models.CharField(db_column='SALESREP_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    site_id = models.CharField(db_column='SITE_ID', max_length=15)  # Field name made lowercase.
    terms_net_type = models.CharField(db_column='TERMS_NET_TYPE', max_length=1)  # Field name made lowercase.
    terms_net_days = models.SmallIntegerField(db_column='TERMS_NET_DAYS', blank=True, null=True)  # Field name made lowercase.
    terms_net_date = models.DateTimeField(db_column='TERMS_NET_DATE', blank=True, null=True)  # Field name made lowercase.
    terms_disc_type = models.CharField(db_column='TERMS_DISC_TYPE', max_length=1)  # Field name made lowercase.
    terms_disc_days = models.SmallIntegerField(db_column='TERMS_DISC_DAYS', blank=True, null=True)  # Field name made lowercase.
    terms_disc_date = models.DateTimeField(db_column='TERMS_DISC_DATE', blank=True, null=True)  # Field name made lowercase.
    terms_disc_percent = models.DecimalField(db_column='TERMS_DISC_PERCENT', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    terms_description = models.CharField(db_column='TERMS_DESCRIPTION', max_length=80, blank=True, null=True)  # Field name made lowercase.
    freight_terms = models.CharField(db_column='FREIGHT_TERMS', max_length=1)  # Field name made lowercase.
    order_date = models.DateTimeField(db_column='ORDER_DATE')  # Field name made lowercase.
    desired_ship_date = models.DateTimeField(db_column='DESIRED_SHIP_DATE', blank=True, null=True)  # Field name made lowercase.
    back_order = models.CharField(db_column='BACK_ORDER', max_length=1)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1)  # Field name made lowercase.
    sell_rate = models.DecimalField(db_column='SELL_RATE', max_digits=15, decimal_places=8)  # Field name made lowercase.
    buy_rate = models.DecimalField(db_column='BUY_RATE', max_digits=15, decimal_places=8)  # Field name made lowercase.
    last_shipped_date = models.DateTimeField(db_column='LAST_SHIPPED_DATE', blank=True, null=True)  # Field name made lowercase.
    posting_candidate = models.CharField(db_column='POSTING_CANDIDATE', max_length=1)  # Field name made lowercase.
    total_amt_ordered = models.DecimalField(db_column='TOTAL_AMT_ORDERED', max_digits=23, decimal_places=8)  # Field name made lowercase.
    total_amt_shipped = models.DecimalField(db_column='TOTAL_AMT_SHIPPED', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    marked_for_purge = models.CharField(db_column='MARKED_FOR_PURGE', max_length=1)  # Field name made lowercase.
    edi_flag = models.CharField(db_column='EDI_FLAG', max_length=1)  # Field name made lowercase.
    edi_accum_ship_qty = models.DecimalField(db_column='EDI_ACCUM_SHIP_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_accum_auth_qty = models.DecimalField(db_column='EDI_ACCUM_AUTH_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_accum_buy_qty = models.DecimalField(db_column='EDI_ACCUM_BUY_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_release_no = models.CharField(db_column='EDI_RELEASE_NO', max_length=30, blank=True, null=True)  # Field name made lowercase.
    edi_last_shipdate = models.DateTimeField(db_column='EDI_LAST_SHIPDATE', blank=True, null=True)  # Field name made lowercase.
    edi_accum_ship_adj = models.DecimalField(db_column='EDI_ACCUM_SHIP_ADJ', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_accum_ord_adj = models.DecimalField(db_column='EDI_ACCUM_ORD_ADJ', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    exch_rate_fixed = models.CharField(db_column='EXCH_RATE_FIXED', max_length=1)  # Field name made lowercase.
    promise_date = models.DateTimeField(db_column='PROMISE_DATE', blank=True, null=True)  # Field name made lowercase.
    printed_date = models.DateTimeField(db_column='PRINTED_DATE', blank=True, null=True)  # Field name made lowercase.
    edi_blanket_flag = models.CharField(db_column='EDI_BLANKET_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    edi_blanket_no = models.CharField(db_column='EDI_BLANKET_NO', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contract_id = models.CharField(db_column='CONTRACT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shipto_id = models.CharField(db_column='SHIPTO_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    currency_id = models.CharField(db_column='CURRENCY_ID', max_length=15)  # Field name made lowercase.
    warehouse_id = models.CharField(db_column='WAREHOUSE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    order_type = models.CharField(db_column='ORDER_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    carrier_id = models.CharField(db_column='CARRIER_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    accept_early = models.CharField(db_column='ACCEPT_EARLY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    days_early = models.SmallIntegerField(db_column='DAYS_EARLY', blank=True, null=True)  # Field name made lowercase.
    dispatched = models.CharField(db_column='DISPATCHED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    expire_date = models.DateTimeField(db_column='EXPIRE_DATE', blank=True, null=True)  # Field name made lowercase.
    contact_mobile = models.CharField(db_column='CONTACT_MOBILE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contact_email = models.CharField(db_column='CONTACT_EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='CREATE_DATE')  # Field name made lowercase.
    user_1 = models.CharField(db_column='USER_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_2 = models.CharField(db_column='USER_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_3 = models.CharField(db_column='USER_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_4 = models.CharField(db_column='USER_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_5 = models.CharField(db_column='USER_5', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_6 = models.CharField(db_column='USER_6', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_7 = models.CharField(db_column='USER_7', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_8 = models.CharField(db_column='USER_8', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_9 = models.CharField(db_column='USER_9', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_10 = models.CharField(db_column='USER_10', max_length=80, blank=True, null=True)  # Field name made lowercase.
    udf_layout_id = models.CharField(db_column='UDF_LAYOUT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    send_ack = models.CharField(db_column='SEND_ACK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    authorization_id = models.CharField(db_column='AUTHORIZATION_ID', max_length=250, blank=True, null=True)  # Field name made lowercase.
    edi_accum_clr_date = models.DateTimeField(db_column='EDI_ACCUM_CLR_DATE', blank=True, null=True)  # Field name made lowercase.
    project_id = models.CharField(db_column='PROJECT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    prime_contractor = models.CharField(db_column='PRIME_CONTRACTOR', max_length=20, blank=True, null=True)  # Field name made lowercase.
    shipped_from = models.CharField(db_column='SHIPPED_FROM', max_length=20, blank=True, null=True)  # Field name made lowercase.
    administered_by = models.CharField(db_column='ADMINISTERED_BY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pay_made_by = models.CharField(db_column='PAY_MADE_BY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    marked_for = models.CharField(db_column='MARKED_FOR', max_length=20, blank=True, null=True)  # Field name made lowercase.
    origin_cqa = models.CharField(db_column='ORIGIN_CQA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    origin_accept = models.CharField(db_column='ORIGIN_ACCEPT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dest_cqa = models.CharField(db_column='DEST_CQA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dest_accept = models.CharField(db_column='DEST_ACCEPT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pkg_level = models.CharField(db_column='PKG_LEVEL', max_length=40, blank=True, null=True)  # Field name made lowercase.
    acceptance_point = models.CharField(db_column='ACCEPTANCE_POINT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dd250_required = models.CharField(db_column='DD250_REQUIRED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    backorder_flag = models.CharField(db_column='BACKORDER_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    owner_id = models.CharField(db_column='OWNER_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    consolidation_id = models.CharField(db_column='CONSOLIDATION_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mark_for_id = models.CharField(db_column='MARK_FOR_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mark_for_addr_no = models.IntegerField(db_column='MARK_FOR_ADDR_NO', blank=True, null=True)  # Field name made lowercase.
    cod_amount = models.DecimalField(db_column='COD_AMOUNT', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    freight_bill_acct = models.CharField(db_column='FREIGHT_BILL_ACCT', max_length=30, blank=True, null=True)  # Field name made lowercase.
    revision_id = models.CharField(db_column='REVISION_ID', max_length=8, blank=True, null=True)  # Field name made lowercase.
    vscp_order = models.CharField(db_column='VSCP_ORDER', max_length=1, blank=True, null=True)  # Field name made lowercase.
    master_link_no = models.CharField(db_column='MASTER_LINK_NO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    link_sequence_no = models.CharField(db_column='LINK_SEQUENCE_NO', max_length=6, blank=True, null=True)  # Field name made lowercase.
    cust_bank_id = models.CharField(db_column='CUST_BANK_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    consignment = models.CharField(db_column='CONSIGNMENT', max_length=1)  # Field name made lowercase.
    status_eff_date = models.DateTimeField(db_column='STATUS_EFF_DATE')  # Field name made lowercase.
    promise_del_date = models.DateTimeField(db_column='PROMISE_DEL_DATE', blank=True, null=True)  # Field name made lowercase.
    terms_id = models.CharField(db_column='TERMS_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    internal_order = models.CharField(db_column='INTERNAL_ORDER', max_length=1, blank=True, null=True)  # Field name made lowercase.
    contact_id = models.CharField(db_column='CONTACT_ID', max_length=25, blank=True, null=True)  # Field name made lowercase.
    entered_by = models.CharField(db_column='ENTERED_BY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contact_phone_ext = models.CharField(db_column='CONTACT_PHONE_EXT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    email_notification = models.CharField(db_column='EMAIL_NOTIFICATION', max_length=1, default="N")  # Field name made lowercase.
    email_cust_on_new_order = models.CharField(db_column='EMAIL_CUST_ON_NEW_ORDER', max_length=1, default="N")  # Field name made lowercase.
    email_cust_on_chg_order = models.CharField(db_column='EMAIL_CUST_ON_CHG_ORDER', max_length=1, default="N")  # Field name made lowercase.
    email_cust_on_shipment = models.CharField(db_column='EMAIL_CUST_ON_SHIPMENT', max_length=1, default="N")  # Field name made lowercase.
    email_empl_on_new_order = models.CharField(db_column='EMAIL_EMPL_ON_NEW_ORDER', max_length=1, default="N")  # Field name made lowercase.
    email_empl_on_chg_order = models.CharField(db_column='EMAIL_EMPL_ON_CHG_ORDER', max_length=1, default="N")  # Field name made lowercase.
    email_empl_on_shipment = models.CharField(db_column='EMAIL_EMPL_ON_SHIPMENT', max_length=1, default="N")  # Field name made lowercase.
    email_empl_on_inv_paid = models.CharField(db_column='EMAIL_EMPL_ON_INV_PAID', max_length=1, default="N")  # Field name made lowercase.
    cust_ship_chg_acct_no = models.CharField(db_column='CUST_SHIP_CHG_ACCT_NO', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CUSTOMER_ORDER'


class CustomerSite(TruncatedModel):  # Field name made lowercase.
    customer = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CUSTOMER_ID')  # Field name made lowercase.
    site_id = models.CharField(db_column='SITE_ID', primary_key=True, max_length=15)  # Field name made lowercase.
    priority_code = models.CharField(db_column='PRIORITY_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    warehouse_id = models.CharField(db_column='WAREHOUSE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    customer_type = models.CharField(db_column='CUSTOMER_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    order_fill_rate = models.DecimalField(db_column='ORDER_FILL_RATE', max_digits=5, decimal_places=2)  # Field name made lowercase.
    fill_rate_type = models.CharField(db_column='FILL_RATE_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    allocation_fence = models.IntegerField(db_column='ALLOCATION_FENCE', blank=True, null=True)  # Field name made lowercase.
    co_alloc_level = models.CharField(db_column='CO_ALLOC_LEVEL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    reallocate = models.CharField(db_column='REALLOCATE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    consolidate_orders = models.CharField(db_column='CONSOLIDATE_ORDERS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    compliance_label = models.CharField(db_column='COMPLIANCE_LABEL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    auto_allocate = models.CharField(db_column='AUTO_ALLOCATE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    email_invoice = models.CharField(db_column='EMAIL_INVOICE', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CUSTOMER_SITE'
        unique_together = (('site_id', 'customer'),)


class CustOrderBinary(TruncatedModel):  # Field name made lowercase.
    cust_order = models.ForeignKey(CustomerOrder, models.DO_NOTHING, db_column='CUST_ORDER_ID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1)  # Field name made lowercase.
    bits = models.BinaryField(db_column='BITS', blank=True, null=True)  # Field name made lowercase.
    bits_length = models.IntegerField(db_column='BITS_LENGTH')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CUST_ORDER_BINARY'
        unique_together = (('cust_order', 'type'),)


class CustOrderLine(TruncatedModel):  # Field name made lowercase.
    rowid = models.AutoField(primary_key=True, db_column='ROWID')
    cust_order = models.ForeignKey(CustomerOrder, models.DO_NOTHING, db_column='CUST_ORDER_ID')  # Field name made lowercase.
    line_no = models.SmallIntegerField(db_column='LINE_NO')  # Field name made lowercase.
    part = models.ForeignKey('Part', models.DO_NOTHING, db_column='PART_ID', blank=True, null=True)  # Field name made lowercase.
    customer_part_id = models.CharField(db_column='CUSTOMER_PART_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    line_status = models.CharField(db_column='LINE_STATUS', max_length=1)  # Field name made lowercase.
    order_qty = models.DecimalField(db_column='ORDER_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    user_order_qty = models.DecimalField(db_column='USER_ORDER_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    selling_um = models.CharField(db_column='SELLING_UM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    desired_ship_date = models.DateTimeField(db_column='DESIRED_SHIP_DATE', blank=True, null=True)  # Field name made lowercase.
    unit_price = models.DecimalField(db_column='UNIT_PRICE', max_digits=22, decimal_places=8)  # Field name made lowercase.
    trade_disc_percent = models.DecimalField(db_column='TRADE_DISC_PERCENT', max_digits=6, decimal_places=3, default=0)  # Field name made lowercase.
    est_freight = models.DecimalField(db_column='EST_FREIGHT', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    commission_pct = models.DecimalField(db_column='COMMISSION_PCT', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    sales_tax_group_id = models.CharField(db_column='SALES_TAX_GROUP_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    misc_reference = models.CharField(db_column='MISC_REFERENCE', max_length=120, blank=True, null=True)  # Field name made lowercase.
    product_code = models.CharField(db_column='PRODUCT_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    commodity_code = models.CharField(db_column='COMMODITY_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    drawing_id = models.CharField(db_column='DRAWING_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    drawing_rev_no = models.CharField(db_column='DRAWING_REV_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    gl_revenue_acct_id = models.CharField(db_column='GL_REVENUE_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mat_gl_acct_id = models.CharField(db_column='MAT_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lab_gl_acct_id = models.CharField(db_column='LAB_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    bur_gl_acct_id = models.CharField(db_column='BUR_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ser_gl_acct_id = models.CharField(db_column='SER_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    last_shipped_date = models.DateTimeField(db_column='LAST_SHIPPED_DATE', blank=True, null=True)  # Field name made lowercase.
    total_act_freight = models.DecimalField(db_column='TOTAL_ACT_FREIGHT', max_digits=23, decimal_places=8)  # Field name made lowercase.
    total_shipped_qty = models.DecimalField(db_column='TOTAL_SHIPPED_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    total_usr_ship_qty = models.DecimalField(db_column='TOTAL_USR_SHIP_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    total_amt_shipped = models.DecimalField(db_column='TOTAL_AMT_SHIPPED', max_digits=23, decimal_places=8)  # Field name made lowercase.
    total_amt_ordered = models.DecimalField(db_column='TOTAL_AMT_ORDERED', max_digits=23, decimal_places=8)  # Field name made lowercase.
    promise_date = models.DateTimeField(db_column='PROMISE_DATE', blank=True, null=True)  # Field name made lowercase.
    service_charge_id = models.CharField(db_column='SERVICE_CHARGE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    piece_count = models.DecimalField(db_column='PIECE_COUNT', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    length = models.DecimalField(db_column='LENGTH', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    width = models.DecimalField(db_column='WIDTH', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    height = models.DecimalField(db_column='HEIGHT', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    dimensions_um = models.CharField(db_column='DIMENSIONS_UM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vat_code = models.CharField(db_column='VAT_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    edi_blanket_qty = models.DecimalField(db_column='EDI_BLANKET_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_blanket_usrqty = models.DecimalField(db_column='EDI_BLANKET_USRQTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_accum_qty_rel = models.DecimalField(db_column='EDI_ACCUM_QTY_REL', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_accum_usr_rel = models.DecimalField(db_column='EDI_ACCUM_USR_REL', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_accum_qty_rec = models.DecimalField(db_column='EDI_ACCUM_QTY_REC', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_accum_usr_rec = models.DecimalField(db_column='EDI_ACCUM_USR_REC', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_last_rec_date = models.DateTimeField(db_column='EDI_LAST_REC_DATE', blank=True, null=True)  # Field name made lowercase.
    edi_release_no = models.CharField(db_column='EDI_RELEASE_NO', max_length=30, blank=True, null=True)  # Field name made lowercase.
    edi_release_date = models.DateTimeField(db_column='EDI_RELEASE_DATE', blank=True, null=True)  # Field name made lowercase.
    edi_qty_released = models.DecimalField(db_column='EDI_QTY_RELEASED', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_usr_qty_rel = models.DecimalField(db_column='EDI_USR_QTY_REL', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_req_rel_date = models.DateTimeField(db_column='EDI_REQ_REL_DATE', blank=True, null=True)  # Field name made lowercase.
    shipto_id = models.CharField(db_column='SHIPTO_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    warehouse_id = models.CharField(db_column='WAREHOUSE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    wip_vas_unit_price = models.DecimalField(db_column='WIP_VAS_UNIT_PRICE', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    allocated_qty = models.DecimalField(db_column='ALLOCATED_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    fulfilled_qty = models.DecimalField(db_column='FULFILLED_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    accept_early = models.CharField(db_column='ACCEPT_EARLY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    days_early = models.SmallIntegerField(db_column='DAYS_EARLY', blank=True, null=True)  # Field name made lowercase.
    order_type = models.CharField(db_column='ORDER_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hts_code = models.CharField(db_column='HTS_CODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    orig_country_id = models.CharField(db_column='ORIG_COUNTRY_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    edi_accum_fab_qty = models.DecimalField(db_column='EDI_ACCUM_FAB_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_accum_raw_qty = models.DecimalField(db_column='EDI_ACCUM_RAW_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    ack_id = models.CharField(db_column='ACK_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    edi_last_shipdate = models.DateTimeField(db_column='EDI_LAST_SHIPDATE', blank=True, null=True)  # Field name made lowercase.
    edi_accum_ship_qty = models.DecimalField(db_column='EDI_ACCUM_SHIP_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_accum_ship_adj = models.DecimalField(db_column='EDI_ACCUM_SHIP_ADJ', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    user_1 = models.CharField(db_column='USER_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_2 = models.CharField(db_column='USER_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_3 = models.CharField(db_column='USER_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_4 = models.CharField(db_column='USER_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_5 = models.CharField(db_column='USER_5', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_6 = models.CharField(db_column='USER_6', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_7 = models.CharField(db_column='USER_7', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_8 = models.CharField(db_column='USER_8', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_9 = models.CharField(db_column='USER_9', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_10 = models.CharField(db_column='USER_10', max_length=80, blank=True, null=True)  # Field name made lowercase.
    udf_layout_id = models.CharField(db_column='UDF_LAYOUT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    send_ack = models.CharField(db_column='SEND_ACK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vat_category = models.CharField(max_length=15, blank=True, null=True)
    ita_special_charge = models.CharField(db_column='ITA_SPECIAL_CHARGE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    wbs_code = models.CharField(db_column='WBS_CODE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wbs_clin = models.CharField(db_column='WBS_CLIN', max_length=15, blank=True, null=True)  # Field name made lowercase.
    project_id = models.CharField(db_column='PROJECT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    wbs_contract_type = models.CharField(db_column='WBS_CONTRACT_TYPE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    ec_id = models.CharField(db_column='EC_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    mod_number = models.IntegerField(db_column='MOD_NUMBER', blank=True, null=True)  # Field name made lowercase.
    marked_for = models.CharField(db_column='MARKED_FOR', max_length=250, blank=True, null=True)  # Field name made lowercase.
    backorder_flag = models.CharField(db_column='BACKORDER_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    proj_ref_seq_no = models.SmallIntegerField(db_column='PROJ_REF_SEQ_NO', blank=True, null=True)  # Field name made lowercase.
    proj_ref_sub_id = models.CharField(db_column='PROJ_REF_SUB_ID', max_length=3, blank=True, null=True)  # Field name made lowercase.
    owner_id = models.CharField(db_column='OWNER_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    trace_qty = models.DecimalField(db_column='TRACE_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qa_qty = models.DecimalField(db_column='QA_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    mark_for_id = models.CharField(db_column='MARK_FOR_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    wsa_ref_no_1 = models.CharField(db_column='WSA_REF_NO_1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wsa_ref_no_2 = models.CharField(db_column='WSA_REF_NO_2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ship_order_status = models.CharField(db_column='SHIP_ORDER_STATUS', max_length=2, blank=True, null=True)  # Field name made lowercase.
    line_item_chg_rsn = models.CharField(db_column='LINE_ITEM_CHG_RSN', max_length=2, blank=True, null=True)  # Field name made lowercase.
    dd250_required = models.CharField(db_column='DD250_REQUIRED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    billing_basis = models.CharField(db_column='BILLING_BASIS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    funded_value = models.DecimalField(db_column='FUNDED_VALUE', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    dc_class_id = models.CharField(db_column='DC_CLASS_ID', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dispatched = models.CharField(db_column='DISPATCHED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    trans_category_id = models.CharField(db_column='TRANS_CATEGORY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    orig_stage_revision_id = models.CharField(db_column='ORIG_STAGE_REVISION_ID', max_length=24, blank=True, null=True)  # Field name made lowercase.
    status_eff_date = models.DateTimeField(db_column='STATUS_EFF_DATE')  # Field name made lowercase.
    promise_del_date = models.DateTimeField(db_column='PROMISE_DEL_DATE', blank=True, null=True)  # Field name made lowercase.
    price_note = models.CharField(db_column='PRICE_NOTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    discount_note = models.CharField(db_column='DISCOUNT_NOTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    freight_note = models.CharField(db_column='FREIGHT_NOTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    commission_note = models.CharField(db_column='COMMISSION_NOTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    site_id = models.CharField(db_column='SITE_ID', max_length=15)  # Field name made lowercase.
    entered_by = models.CharField(db_column='ENTERED_BY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email_notification = models.CharField(db_column='EMAIL_NOTIFICATION', max_length=1, default="N")  # Field name made lowercase.
    price_group_id = models.CharField(db_column='PRICE_GROUP_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    posting_candidate = models.CharField(db_column='POSTING_CANDIDATE', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CUST_ORDER_LINE'
        unique_together = (('cust_order', 'line_no'),)


class Location(TruncatedModel):
    id = models.CharField(db_column='ID', max_length=15)  # Field name made lowercase.
    warehouse = models.OneToOneField('Warehouse', models.DO_NOTHING, db_column='WAREHOUSE_ID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=80, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1)  # Field name made lowercase.
    customer = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CUSTOMER_ID', blank=True, null=True)  # Field name made lowercase.
    vendor = models.ForeignKey('Vendor', models.DO_NOTHING, db_column='VENDOR_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'LOCATION'
        unique_together = (('warehouse', 'id'),)


class HoldReason(TruncatedModel):
    id = models.CharField(db_column='ID', primary_key=True, max_length=15)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=80)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'HOLD_REASON'


class Operation(TruncatedModel):  # Field name made lowercase.
    rowid = models.AutoField(primary_key=True, db_column='ROWID')
    workorder_type = models.CharField(db_column='WORKORDER_TYPE', max_length=1)  # Field name made lowercase.
    workorder_base = models.CharField(db_column='WORKORDER_BASE_ID', max_length=30)  # Field name made lowercase.
    workorder_lot = models.CharField(db_column='WORKORDER_LOT_ID', max_length=3)  # Field name made lowercase.
    workorder_split = models.CharField(db_column='WORKORDER_SPLIT_ID', max_length=3)  # Field name made lowercase.
    workorder_sub = models.CharField(db_column='WORKORDER_SUB_ID', max_length=3)  # Field name made lowercase.
    sequence_no = models.SmallIntegerField(db_column='SEQUENCE_NO')  # Field name made lowercase.
    resource = models.ForeignKey('ShopResource', models.DO_NOTHING, db_column='RESOURCE_ID')  # Field name made lowercase.
    setup_hrs = models.DecimalField(db_column='SETUP_HRS', max_digits=8, decimal_places=3, blank=True, null=True, default=0)  # Field name made lowercase.
    run = models.DecimalField(db_column='RUN', max_digits=20, decimal_places=8, blank=True, null=True, default=0)  # Field name made lowercase.
    run_type = models.CharField(db_column='RUN_TYPE', max_length=15)  # Field name made lowercase.
    load_size_qty = models.DecimalField(db_column='LOAD_SIZE_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    run_hrs = models.DecimalField(db_column='RUN_HRS', max_digits=7, decimal_places=2, blank=True, null=True, default=0)  # Field name made lowercase.
    move_hrs = models.DecimalField(db_column='MOVE_HRS', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    transit_days = models.DecimalField(db_column='TRANSIT_DAYS', max_digits=6, decimal_places=3, blank=True, null=True, default=0)  # Field name made lowercase.
    service_id = models.CharField(db_column='SERVICE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    scrap_yield_pct = models.DecimalField(db_column='SCRAP_YIELD_PCT', max_digits=5, decimal_places=2, blank=True, null=True, default=0)  # Field name made lowercase.
    scrap_yield_type = models.CharField(db_column='SCRAP_YIELD_TYPE', max_length=1)  # Field name made lowercase.
    fixed_scrap_units = models.DecimalField(db_column='FIXED_SCRAP_UNITS', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    minimum_move_qty = models.DecimalField(db_column='MINIMUM_MOVE_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    calc_start_qty = models.DecimalField(db_column='CALC_START_QTY', max_digits=20, decimal_places=8, blank=True, null=True, default=0)  # Field name made lowercase.
    calc_end_qty = models.DecimalField(db_column='CALC_END_QTY', max_digits=20, decimal_places=8, blank=True, null=True, default=0)  # Field name made lowercase.
    completed_qty = models.DecimalField(db_column='COMPLETED_QTY', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    deviated_qty = models.DecimalField(db_column='DEVIATED_QTY', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    act_setup_hrs = models.DecimalField(db_column='ACT_SETUP_HRS', max_digits=7, decimal_places=2, default=0)  # Field name made lowercase.
    act_run_hrs = models.DecimalField(db_column='ACT_RUN_HRS', max_digits=7, decimal_places=2, default=0)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1)  # Field name made lowercase.
    setup_completed = models.CharField(db_column='SETUP_COMPLETED', max_length=1)  # Field name made lowercase.
    service_begin_date = models.DateTimeField(db_column='SERVICE_BEGIN_DATE', blank=True, null=True)  # Field name made lowercase.
    close_date = models.DateTimeField(db_column='CLOSE_DATE', blank=True, null=True)  # Field name made lowercase.
    operation_type = models.ForeignKey('OperationType', models.DO_NOTHING, db_column='OPERATION_TYPE', blank=True, null=True)  # Field name made lowercase.
    drawing_id = models.CharField(db_column='DRAWING_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    drawing_rev_no = models.CharField(db_column='DRAWING_REV_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    override_qtys = models.CharField(db_column='OVERRIDE_QTYS', max_length=1)  # Field name made lowercase.
    begin_traceability = models.CharField(db_column='BEGIN_TRACEABILITY', max_length=1)  # Field name made lowercase.
    capacity_usage_max = models.SmallIntegerField(db_column='CAPACITY_USAGE_MAX', blank=True, null=True)  # Field name made lowercase.
    capacity_usage_min = models.SmallIntegerField(db_column='CAPACITY_USAGE_MIN', blank=True, null=True)  # Field name made lowercase.
    test_id = models.CharField(db_column='TEST_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    spc_qty = models.DecimalField(db_column='SPC_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    sched_start_date = models.DateTimeField(db_column='SCHED_START_DATE', blank=True, null=True)  # Field name made lowercase.
    sched_finish_date = models.DateTimeField(db_column='SCHED_FINISH_DATE', blank=True, null=True)  # Field name made lowercase.
    could_finish_date = models.DateTimeField(db_column='COULD_FINISH_DATE', blank=True, null=True)  # Field name made lowercase.
    isdeterminant = models.CharField(db_column='ISDETERMINANT', max_length=1)  # Field name made lowercase.
    setup_cost_per_hr = models.DecimalField(db_column='SETUP_COST_PER_HR', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    run_cost_per_hr = models.DecimalField(db_column='RUN_COST_PER_HR', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    run_cost_per_unit = models.DecimalField(db_column='RUN_COST_PER_UNIT', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    bur_per_hr_setup = models.DecimalField(db_column='BUR_PER_HR_SETUP', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    bur_per_hr_run = models.DecimalField(db_column='BUR_PER_HR_RUN', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    bur_per_unit_run = models.DecimalField(db_column='BUR_PER_UNIT_RUN', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    service_base_chg = models.DecimalField(db_column='SERVICE_BASE_CHG', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    bur_percent_setup = models.DecimalField(db_column='BUR_PERCENT_SETUP', max_digits=6, decimal_places=3, default=0)  # Field name made lowercase.
    bur_percent_run = models.DecimalField(db_column='BUR_PERCENT_RUN', max_digits=6, decimal_places=3, default=0)  # Field name made lowercase.
    bur_per_operation = models.DecimalField(db_column='BUR_PER_OPERATION', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    est_atl_lab_cost = models.DecimalField(db_column='EST_ATL_LAB_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    est_atl_bur_cost = models.DecimalField(db_column='EST_ATL_BUR_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    est_atl_ser_cost = models.DecimalField(db_column='EST_ATL_SER_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    rem_atl_lab_cost = models.DecimalField(db_column='REM_ATL_LAB_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    rem_atl_bur_cost = models.DecimalField(db_column='REM_ATL_BUR_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    rem_atl_ser_cost = models.DecimalField(db_column='REM_ATL_SER_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    act_atl_lab_cost = models.DecimalField(db_column='ACT_ATL_LAB_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    act_atl_bur_cost = models.DecimalField(db_column='ACT_ATL_BUR_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    act_atl_ser_cost = models.DecimalField(db_column='ACT_ATL_SER_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    est_ttl_mat_cost = models.DecimalField(db_column='EST_TTL_MAT_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    est_ttl_lab_cost = models.DecimalField(db_column='EST_TTL_LAB_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    est_ttl_bur_cost = models.DecimalField(db_column='EST_TTL_BUR_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    est_ttl_ser_cost = models.DecimalField(db_column='EST_TTL_SER_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    rem_ttl_mat_cost = models.DecimalField(db_column='REM_TTL_MAT_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    rem_ttl_lab_cost = models.DecimalField(db_column='REM_TTL_LAB_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    rem_ttl_bur_cost = models.DecimalField(db_column='REM_TTL_BUR_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    rem_ttl_ser_cost = models.DecimalField(db_column='REM_TTL_SER_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    act_ttl_mat_cost = models.DecimalField(db_column='ACT_TTL_MAT_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    act_ttl_lab_cost = models.DecimalField(db_column='ACT_TTL_LAB_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    act_ttl_bur_cost = models.DecimalField(db_column='ACT_TTL_BUR_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    act_ttl_ser_cost = models.DecimalField(db_column='ACT_TTL_SER_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    split_adjustment = models.DecimalField(db_column='SPLIT_ADJUSTMENT', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    milestone_id = models.CharField(db_column='MILESTONE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    schedule_type = models.SmallIntegerField(db_column='SCHEDULE_TYPE', blank=True, null=True, default=0)  # Field name made lowercase.
    min_segment_size = models.DecimalField(db_column='MIN_SEGMENT_SIZE', max_digits=14, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    protect_cost = models.CharField(db_column='PROTECT_COST', max_length=1)  # Field name made lowercase.
    drawing_file = models.CharField(db_column='DRAWING_FILE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dispatched_qty = models.DecimalField(db_column='DISPATCHED_QTY', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    service_min_chg = models.DecimalField(db_column='SERVICE_MIN_CHG', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    vendor_id = models.CharField(db_column='VENDOR_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vendor_service_id = models.CharField(db_column='VENDOR_SERVICE_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    service_part_id = models.CharField(db_column='SERVICE_PART_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    last_disp_date = models.DateTimeField(db_column='LAST_DISP_DATE', blank=True, null=True)  # Field name made lowercase.
    last_recv_date = models.DateTimeField(db_column='LAST_RECV_DATE', blank=True, null=True)  # Field name made lowercase.
    warehouse_id = models.CharField(db_column='WAREHOUSE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    allocated_qty = models.DecimalField(db_column='ALLOCATED_QTY', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    fulfilled_qty = models.DecimalField(db_column='FULFILLED_QTY', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    least_min_move_qty = models.SmallIntegerField(db_column='LEAST_MIN_MOVE_QTY', blank=True, null=True)  # Field name made lowercase.
    max_gap_prev_op = models.IntegerField(db_column='MAX_GAP_PREV_OP', blank=True, null=True)  # Field name made lowercase.
    apply_calendar = models.CharField(db_column='APPLY_CALENDAR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    max_downtime = models.IntegerField(db_column='MAX_DOWNTIME', blank=True, null=True)  # Field name made lowercase.
    accum_downtime = models.CharField(db_column='ACCUM_DOWNTIME', max_length=1, blank=True, null=True)  # Field name made lowercase.
    run_qty_per_cycle = models.DecimalField(db_column='RUN_QTY_PER_CYCLE', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    user_1 = models.CharField(db_column='USER_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_2 = models.CharField(db_column='USER_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_3 = models.CharField(db_column='USER_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_4 = models.CharField(db_column='USER_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_5 = models.CharField(db_column='USER_5', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_6 = models.CharField(db_column='USER_6', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_7 = models.CharField(db_column='USER_7', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_8 = models.CharField(db_column='USER_8', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_9 = models.CharField(db_column='USER_9', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_10 = models.CharField(db_column='USER_10', max_length=80, blank=True, null=True)  # Field name made lowercase.
    udf_layout_id = models.CharField(db_column='UDF_LAYOUT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    num_mem_to_sched = models.SmallIntegerField(db_column='NUM_MEM_TO_SCHED', blank=True, null=True)  # Field name made lowercase.
    service_buffer = models.IntegerField(db_column='SERVICE_BUFFER', blank=True, null=True)  # Field name made lowercase.
    milestone_sub_id = models.CharField(db_column='MILESTONE_SUB_ID', max_length=3, blank=True, null=True)  # Field name made lowercase.
    post_milestone = models.CharField(db_column='POST_MILESTONE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    proj_milestone_op = models.CharField(db_column='PROJ_MILESTONE_OP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    wbs_code = models.CharField(db_column='WBS_CODE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wbs_start_date = models.DateTimeField(db_column='WBS_START_DATE', blank=True, null=True)  # Field name made lowercase.
    wbs_end_date = models.DateTimeField(db_column='WBS_END_DATE', blank=True, null=True)  # Field name made lowercase.
    wbs_duration = models.DecimalField(db_column='WBS_DURATION', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    milestone_seq_no = models.SmallIntegerField(db_column='MILESTONE_SEQ_NO', blank=True, null=True)  # Field name made lowercase.
    prd_insp_plan_id = models.CharField(db_column='PRD_INSP_PLAN_ID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    setup_inspect_req = models.CharField(db_column='SETUP_INSPECT_REQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    run_inspect_req = models.CharField(db_column='RUN_INSPECT_REQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    status_eff_date = models.DateTimeField(db_column='STATUS_EFF_DATE')  # Field name made lowercase.
    pred_sub_id = models.CharField(db_column='PRED_SUB_ID', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pred_seq_no = models.SmallIntegerField(db_column='PRED_SEQ_NO', blank=True, null=True)  # Field name made lowercase.
    site_id = models.CharField(db_column='SITE_ID', max_length=15)   # Field name made lowercase.
    sched_capacity_usage = models.IntegerField(db_column='SCHED_CAPACITY_USAGE', blank=True, null=True)  # Field name made lowercase.
    bid_rate_category_id = models.CharField(db_column='BID_RATE_CATEGORY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    overlap_setup = models.CharField(db_column='OVERLAP_SETUP', max_length=1)  # Field name made lowercase.
    percent_compl = models.CharField(db_column='PERCENT_COMPL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty_compl_by_hrs = models.CharField(db_column='QTY_COMPL_BY_HRS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    max_qty_complete = models.DecimalField(db_column='MAX_QTY_COMPLETE', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    dispatch_sequence = models.IntegerField(db_column='DISPATCH_SEQUENCE')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'OPERATION'
        unique_together = (('workorder_type', 'workorder_base', 'workorder_lot', 'workorder_split', 'workorder_sub', 'sequence_no'),)


class OperationBinary(TruncatedModel):  # Field name made lowercase.
    workorder_type = models.CharField(db_column='WORKORDER_TYPE', max_length=1)  # Field name made lowercase.
    workorder_base = models.CharField(db_column='WORKORDER_BASE_ID', max_length=30)  # Field name made lowercase.
    workorder_lot = models.CharField(db_column='WORKORDER_LOT_ID', max_length=3)  # Field name made lowercase.
    workorder_split = models.CharField(db_column='WORKORDER_SPLIT_ID', max_length=3)  # Field name made lowercase.
    workorder_sub = models.CharField(db_column='WORKORDER_SUB_ID', max_length=3)  # Field name made lowercase.
    sequence_no = models.SmallIntegerField(db_column='SEQUENCE_NO')  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1)  # Field name made lowercase.
    bits = models.BinaryField(db_column='BITS', blank=True, null=True)  # Field name made lowercase.
    bits_length = models.IntegerField(db_column='BITS_LENGTH')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'OPERATION_BINARY'
        unique_together = (('workorder_type', 'workorder_base', 'workorder_lot', 'workorder_split', 'workorder_sub', 'sequence_no', 'type'),)


class OperationType(TruncatedModel):  # Field name made lowercase.
    id = models.CharField(db_column='ID', primary_key=True, max_length=15)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=40, blank=True, null=True)  # Field name made lowercase.
    resource = models.ForeignKey('ShopResource', models.DO_NOTHING, db_column='RESOURCE_ID', blank=True, null=True)  # Field name made lowercase.
    setup_hrs = models.DecimalField(db_column='SETUP_HRS', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    run = models.DecimalField(db_column='RUN', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    run_type = models.CharField(db_column='RUN_TYPE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    load_size_qty = models.DecimalField(db_column='LOAD_SIZE_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    move_hrs = models.DecimalField(db_column='MOVE_HRS', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    service_id = models.CharField(db_column='SERVICE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    transit_days = models.DecimalField(db_column='TRANSIT_DAYS', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    scrap_yield_pct = models.DecimalField(db_column='SCRAP_YIELD_PCT', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    scrap_yield_type = models.CharField(db_column='SCRAP_YIELD_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fixed_scrap_units = models.DecimalField(db_column='FIXED_SCRAP_UNITS', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    minimum_move_qty = models.DecimalField(db_column='MINIMUM_MOVE_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    calc_start_qty = models.DecimalField(db_column='CALC_START_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    calc_end_qty = models.DecimalField(db_column='CALC_END_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    override_qtys = models.CharField(db_column='OVERRIDE_QTYS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    begin_traceability = models.CharField(db_column='BEGIN_TRACEABILITY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    test_id = models.CharField(db_column='TEST_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    setup_cost_per_hr = models.DecimalField(db_column='SETUP_COST_PER_HR', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    run_cost_per_hr = models.DecimalField(db_column='RUN_COST_PER_HR', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    bur_per_hr_setup = models.DecimalField(db_column='BUR_PER_HR_SETUP', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    bur_per_hr_run = models.DecimalField(db_column='BUR_PER_HR_RUN', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    service_base_chg = models.DecimalField(db_column='SERVICE_BASE_CHG', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    bur_percent_setup = models.DecimalField(db_column='BUR_PERCENT_SETUP', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    bur_percent_run = models.DecimalField(db_column='BUR_PERCENT_RUN', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    bur_per_operation = models.DecimalField(db_column='BUR_PER_OPERATION', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    capacity_usage_max = models.SmallIntegerField(db_column='CAPACITY_USAGE_MAX', blank=True, null=True)  # Field name made lowercase.
    capacity_usage_min = models.SmallIntegerField(db_column='CAPACITY_USAGE_MIN', blank=True, null=True)  # Field name made lowercase.
    schedule_type = models.SmallIntegerField(db_column='SCHEDULE_TYPE', blank=True, null=True, default=0)  # Field name made lowercase.
    min_segment_size = models.DecimalField(db_column='MIN_SEGMENT_SIZE', max_digits=14, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    service_min_chg = models.DecimalField(db_column='SERVICE_MIN_CHG', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    vendor_id = models.CharField(db_column='VENDOR_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vendor_service_id = models.CharField(db_column='VENDOR_SERVICE_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    service_part_id = models.CharField(db_column='SERVICE_PART_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    bur_per_unit_run = models.DecimalField(db_column='BUR_PER_UNIT_RUN', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    run_cost_per_unit = models.DecimalField(db_column='RUN_COST_PER_UNIT', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    site_id = models.CharField(db_column='SITE_ID', max_length=15)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'OPERATION_TYPE'
        unique_together = (('id', 'site_id'),)


class Part(TruncatedModel):  # Field name made lowercase.
    id = models.CharField(db_column='ID', primary_key=True, max_length=30)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=120, blank=True, null=True)  # Field name made lowercase.
    stock_um = models.CharField(db_column='STOCK_UM', max_length=15)  # Field name made lowercase.
    planning_leadtime = models.SmallIntegerField(db_column='PLANNING_LEADTIME')  # Field name made lowercase.
    order_policy = models.CharField(db_column='ORDER_POLICY', max_length=1)  # Field name made lowercase.
    order_point = models.DecimalField(db_column='ORDER_POINT', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    order_up_to_qty = models.DecimalField(db_column='ORDER_UP_TO_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    safety_stock_qty = models.DecimalField(db_column='SAFETY_STOCK_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    fixed_order_qty = models.DecimalField(db_column='FIXED_ORDER_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    days_of_supply = models.SmallIntegerField(db_column='DAYS_OF_SUPPLY', blank=True, null=True)  # Field name made lowercase.
    minimum_order_qty = models.DecimalField(db_column='MINIMUM_ORDER_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    maximum_order_qty = models.DecimalField(db_column='MAXIMUM_ORDER_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    product_code = models.CharField(db_column='PRODUCT_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    commodity_code = models.CharField(db_column='COMMODITY_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    mfg_name = models.CharField(db_column='MFG_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mfg_part_id = models.CharField(db_column='MFG_PART_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fabricated = models.CharField(db_column='FABRICATED', max_length=1)  # Field name made lowercase.
    purchased = models.CharField(db_column='PURCHASED', max_length=1)  # Field name made lowercase.
    stocked = models.CharField(db_column='STOCKED', max_length=1)  # Field name made lowercase.
    detail_only = models.CharField(db_column='DETAIL_ONLY', max_length=1)  # Field name made lowercase.
    demand_history = models.CharField(db_column='DEMAND_HISTORY', max_length=1)  # Field name made lowercase.
    tool_or_fixture = models.CharField(db_column='TOOL_OR_FIXTURE', max_length=1)  # Field name made lowercase.
    inspection_reqd = models.CharField(db_column='INSPECTION_REQD', max_length=1)  # Field name made lowercase.
    weight = models.DecimalField(db_column='WEIGHT', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    weight_um = models.CharField(db_column='WEIGHT_UM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    drawing_id = models.CharField(db_column='DRAWING_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    drawing_rev_no = models.CharField(db_column='DRAWING_REV_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    pref_vendor_id = models.CharField(db_column='PREF_VENDOR_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    mrp_required = models.CharField(db_column='MRP_REQUIRED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mrp_exceptions = models.CharField(db_column='MRP_EXCEPTIONS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    private_um_conv = models.CharField(db_column='PRIVATE_UM_CONV', max_length=1, blank=True, null=True)  # Field name made lowercase.
    auto_backflush = models.CharField(db_column='AUTO_BACKFLUSH', max_length=1, blank=True, null=True)  # Field name made lowercase.
    planner_user_id = models.CharField(db_column='PLANNER_USER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    buyer_user_id = models.CharField(db_column='BUYER_USER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    abc_code = models.CharField(db_column='ABC_CODE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    annual_usage_qty = models.DecimalField(db_column='ANNUAL_USAGE_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    inventory_locked = models.CharField(db_column='INVENTORY_LOCKED', max_length=1)  # Field name made lowercase.
    mat_gl_acct_id = models.CharField(db_column='MAT_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lab_gl_acct_id = models.CharField(db_column='LAB_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    bur_gl_acct_id = models.CharField(db_column='BUR_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ser_gl_acct_id = models.CharField(db_column='SER_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    qty_on_hand = models.DecimalField(db_column='QTY_ON_HAND', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    qty_available_iss = models.DecimalField(db_column='QTY_AVAILABLE_ISS', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    qty_available_mrp = models.DecimalField(db_column='QTY_AVAILABLE_MRP', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    qty_on_order = models.DecimalField(db_column='QTY_ON_ORDER', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    qty_in_demand = models.DecimalField(db_column='QTY_IN_DEMAND', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    user_1 = models.CharField(db_column='USER_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_2 = models.CharField(db_column='USER_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_3 = models.CharField(db_column='USER_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_4 = models.CharField(db_column='USER_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_5 = models.CharField(db_column='USER_5', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_6 = models.CharField(db_column='USER_6', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_7 = models.CharField(db_column='USER_7', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_8 = models.CharField(db_column='USER_8', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_9 = models.CharField(db_column='USER_9', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_10 = models.CharField(db_column='USER_10', max_length=80, blank=True, null=True)  # Field name made lowercase.
    nmfc_code_id = models.CharField(db_column='NMFC_CODE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    package_type = models.CharField(db_column='PACKAGE_TYPE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mrp_exception_info = models.CharField(db_column='MRP_EXCEPTION_INFO', max_length=80, blank=True, null=True)  # Field name made lowercase.
    multiple_order_qty = models.DecimalField(db_column='MULTIPLE_ORDER_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    add_forecast = models.CharField(db_column='ADD_FORECAST', max_length=1)  # Field name made lowercase.
    udf_layout_id = models.CharField(db_column='UDF_LAYOUT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    piece_tracked = models.CharField(db_column='PIECE_TRACKED', max_length=1)  # Field name made lowercase.
    length_reqd = models.CharField(db_column='LENGTH_REQD', max_length=1)  # Field name made lowercase.
    width_reqd = models.CharField(db_column='WIDTH_REQD', max_length=1)  # Field name made lowercase.
    height_reqd = models.CharField(db_column='HEIGHT_REQD', max_length=1)  # Field name made lowercase.
    dimensions_um = models.CharField(db_column='DIMENSIONS_UM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    ship_dimensions = models.CharField(db_column='SHIP_DIMENSIONS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    drawing_file = models.CharField(db_column='DRAWING_FILE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tariff_code = models.CharField(db_column='TARIFF_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    tariff_type = models.CharField(db_column='TARIFF_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    orig_country_id = models.CharField(db_column='ORIG_COUNTRY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    net_weight_2 = models.DecimalField(db_column='NET_WEIGHT_2', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    gross_weight_2 = models.DecimalField(db_column='GROSS_WEIGHT_2', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    weight_um_2 = models.CharField(db_column='WEIGHT_UM_2', max_length=15, blank=True, null=True)  # Field name made lowercase.
    volume = models.DecimalField(db_column='VOLUME', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    volume_um = models.CharField(db_column='VOLUME_UM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vat_code = models.CharField(db_column='VAT_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    demand_fence_1 = models.IntegerField(db_column='DEMAND_FENCE_1', blank=True, null=True)  # Field name made lowercase.
    demand_fence_2 = models.IntegerField(db_column='DEMAND_FENCE_2', blank=True, null=True)  # Field name made lowercase.
    roll_forecast = models.CharField(db_column='ROLL_FORECAST', max_length=1, blank=True, null=True)  # Field name made lowercase.
    consumable = models.CharField(db_column='CONSUMABLE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    primary_source = models.CharField(db_column='PRIMARY_SOURCE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    label_um = models.CharField(db_column='LABEL_UM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    hts_code = models.CharField(db_column='HTS_CODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    def_orig_country = models.CharField(db_column='DEF_ORIG_COUNTRY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    material_code = models.CharField(db_column='MATERIAL_CODE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    def_lbl_format_id = models.CharField(db_column='DEF_LBL_FORMAT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    volatile_leadtime = models.CharField(db_column='VOLATILE_LEADTIME', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lt_plus_days = models.IntegerField(db_column='LT_PLUS_DAYS', blank=True, null=True)  # Field name made lowercase.
    lt_minus_days = models.IntegerField(db_column='LT_MINUS_DAYS', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    use_supply_bef_lt = models.CharField(db_column='USE_SUPPLY_BEF_LT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty_committed = models.DecimalField(db_column='QTY_COMMITTED', max_digits=20, decimal_places=8)  # Field name made lowercase.
    intrastat_exempt = models.CharField(max_length=1)
    case_qty = models.DecimalField(db_column='CASE_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    pallet_qty = models.DecimalField(db_column='PALLET_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    minimum_leadtime = models.SmallIntegerField(db_column='MINIMUM_LEADTIME', blank=True, null=True)  # Field name made lowercase.
    leadtime_buffer = models.SmallIntegerField(db_column='LEADTIME_BUFFER', blank=True, null=True)  # Field name made lowercase.
    emergency_stockpct = models.IntegerField(db_column='EMERGENCY_STOCKPCT', blank=True, null=True)  # Field name made lowercase.
    replenish_level = models.DecimalField(db_column='REPLENISH_LEVEL', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    min_batch_size = models.DecimalField(db_column='MIN_BATCH_SIZE', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    eff_date_price = models.CharField(db_column='EFF_DATE_PRICE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ecn_revision = models.CharField(db_column='ECN_REVISION', max_length=1, blank=True, null=True)  # Field name made lowercase.
    revision_id = models.CharField(db_column='REVISION_ID', max_length=8, blank=True, null=True)  # Field name made lowercase.
    stage_id = models.CharField(db_column='STAGE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    ecn_rev_control = models.CharField(db_column='ECN_REV_CONTROL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    is_kit = models.CharField(db_column='IS_KIT', max_length=1)  # Field name made lowercase.
    yellow_stockpct = models.IntegerField(db_column='YELLOW_STOCKPCT', blank=True, null=True)  # Field name made lowercase.
    univ_plan_material = models.CharField(db_column='UNIV_PLAN_MATERIAL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rls_near_days = models.SmallIntegerField(db_column='RLS_NEAR_DAYS', blank=True, null=True)  # Field name made lowercase.
    sugg_rls_near_days = models.SmallIntegerField(db_column='SUGG_RLS_NEAR_DAYS', blank=True, null=True)  # Field name made lowercase.
    last_implode_date = models.DateTimeField(db_column='LAST_IMPLODE_DATE', blank=True, null=True)  # Field name made lowercase.
    status_eff_date = models.DateTimeField(db_column='STATUS_EFF_DATE')  # Field name made lowercase.
    controlled_by_ics = models.CharField(db_column='CONTROLLED_BY_ICS', max_length=1)  # Field name made lowercase.
    price_group = models.CharField(db_column='PRICE_GROUP', max_length=15, blank=True, null=True)  # Field name made lowercase.
    def_package_qty = models.DecimalField(db_column='DEF_PACKAGE_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    def_package_cap = models.DecimalField(db_column='DEF_PACKAGE_CAP', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    def_sls_tax_grp_id = models.CharField(db_column='DEF_SLS_TAX_GRP_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    mro_class = models.CharField(db_column='MRO_CLASS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    buffer_profile_id = models.CharField(db_column='BUFFER_PROFILE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    adu_horizon = models.SmallIntegerField(db_column='ADU_HORIZON', blank=True, null=True)  # Field name made lowercase.
    asr_leadtime = models.SmallIntegerField(db_column='ASR_LEADTIME', blank=True, null=True)  # Field name made lowercase.
    onhand_alert_red_pct = models.SmallIntegerField(db_column='ONHAND_ALERT_RED_PCT', blank=True, null=True)  # Field name made lowercase.
    process_type = models.CharField(db_column='PROCESS_TYPE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    bid_rate_category_id = models.CharField(db_column='BID_RATE_CATEGORY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='CREATE_DATE')  # Field name made lowercase.
    modify_date = models.DateTimeField(db_column='MODIFY_DATE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'PART'


class PartBinary(TruncatedModel):  # Field name made lowercase.
    part = models.ForeignKey(Part, models.DO_NOTHING, db_column='PART_ID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1)  # Field name made lowercase.
    bits = models.BinaryField(db_column='BITS', blank=True, null=True)  # Field name made lowercase.
    bits_length = models.IntegerField(db_column='BITS_LENGTH')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'PART_BINARY'
        unique_together = (('part', 'type'),)


class PartSite(TruncatedModel):  # Field name made lowercase.
    rowid = models.AutoField(primary_key=True, db_column='ROWID')
    site_id = models.CharField(db_column='SITE_ID', max_length=15)  # Field name made lowercase.
    part = models.ForeignKey(Part, models.DO_NOTHING, db_column='PART_ID')  # Field name made lowercase.
    planning_leadtime = models.SmallIntegerField(db_column='PLANNING_LEADTIME', blank=True, null=True)  # Field name made lowercase.
    order_policy = models.CharField(db_column='ORDER_POLICY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    order_point = models.DecimalField(db_column='ORDER_POINT', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    order_up_to_qty = models.DecimalField(db_column='ORDER_UP_TO_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    safety_stock_qty = models.DecimalField(db_column='SAFETY_STOCK_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    fixed_order_qty = models.DecimalField(db_column='FIXED_ORDER_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    days_of_supply = models.SmallIntegerField(db_column='DAYS_OF_SUPPLY', blank=True, null=True)  # Field name made lowercase.
    minimum_order_qty = models.DecimalField(db_column='MINIMUM_ORDER_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    maximum_order_qty = models.DecimalField(db_column='MAXIMUM_ORDER_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    engineering_mstr = models.CharField(db_column='ENGINEERING_MSTR', max_length=3, blank=True, null=True)  # Field name made lowercase.
    product_code = models.CharField(db_column='PRODUCT_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    fabricated = models.CharField(db_column='FABRICATED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    purchased = models.CharField(db_column='PURCHASED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    stocked = models.CharField(db_column='STOCKED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    detail_only = models.CharField(db_column='DETAIL_ONLY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    demand_history = models.CharField(db_column='DEMAND_HISTORY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tool_or_fixture = models.CharField(db_column='TOOL_OR_FIXTURE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    consumable = models.CharField(db_column='CONSUMABLE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inspection_reqd = models.CharField(db_column='INSPECTION_REQD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    demand_fence_1 = models.IntegerField(db_column='DEMAND_FENCE_1', blank=True, null=True)  # Field name made lowercase.
    demand_fence_2 = models.IntegerField(db_column='DEMAND_FENCE_2', blank=True, null=True)  # Field name made lowercase.
    planner_user_id = models.CharField(db_column='PLANNER_USER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    buyer_user_id = models.CharField(db_column='BUYER_USER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    abc_code = models.CharField(db_column='ABC_CODE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    annual_usage_qty = models.DecimalField(db_column='ANNUAL_USAGE_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    inventory_locked = models.CharField(db_column='INVENTORY_LOCKED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pref_vendor_id = models.CharField(db_column='PREF_VENDOR_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    primary_whs_id = models.CharField(db_column='PRIMARY_WHS_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    primary_loc_id = models.CharField(db_column='PRIMARY_LOC_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    backflush_whs_id = models.CharField(db_column='BACKFLUSH_WHS_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    backflush_loc_id = models.CharField(db_column='BACKFLUSH_LOC_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    inspect_whs_id = models.CharField(db_column='INSPECT_WHS_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    inspect_loc_id = models.CharField(db_column='INSPECT_LOC_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    mrp_required = models.CharField(db_column='MRP_REQUIRED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mrp_exceptions = models.CharField(db_column='MRP_EXCEPTIONS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    auto_backflush = models.CharField(db_column='AUTO_BACKFLUSH', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unit_price = models.DecimalField(db_column='UNIT_PRICE', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    eff_date_price = models.CharField(db_column='EFF_DATE_PRICE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unit_material_cost = models.DecimalField(db_column='UNIT_MATERIAL_COST', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    unit_labor_cost = models.DecimalField(db_column='UNIT_LABOR_COST', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    whsale_unit_cost = models.DecimalField(db_column='WHSALE_UNIT_COST', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    burden_percent = models.DecimalField(db_column='BURDEN_PERCENT', max_digits=5, decimal_places=2, default=0)  # Field name made lowercase.
    burden_per_unit = models.DecimalField(db_column='BURDEN_PER_UNIT', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    excise_unit_price = models.DecimalField(db_column='EXCISE_UNIT_PRICE', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    purc_bur_percent = models.DecimalField(db_column='PURC_BUR_PERCENT', max_digits=6, decimal_places=3, default=0)  # Field name made lowercase.
    unit_burden_cost = models.DecimalField(db_column='UNIT_BURDEN_COST', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    fixed_cost = models.DecimalField(db_column='FIXED_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    unit_service_cost = models.DecimalField(db_column='UNIT_SERVICE_COST', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    new_material_cost = models.DecimalField(db_column='NEW_MATERIAL_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    new_labor_cost = models.DecimalField(db_column='NEW_LABOR_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    new_burden_cost = models.DecimalField(db_column='NEW_BURDEN_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    new_service_cost = models.DecimalField(db_column='NEW_SERVICE_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    new_burden_percent = models.DecimalField(db_column='NEW_BURDEN_PERCENT', max_digits=5, decimal_places=2, default=0)  # Field name made lowercase.
    new_burden_perunit = models.DecimalField(db_column='NEW_BURDEN_PERUNIT', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    purc_bur_per_unit = models.DecimalField(db_column='PURC_BUR_PER_UNIT', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    new_fixed_cost = models.DecimalField(db_column='NEW_FIXED_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    mat_gl_acct_id = models.CharField(db_column='MAT_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lab_gl_acct_id = models.CharField(db_column='LAB_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    bur_gl_acct_id = models.CharField(db_column='BUR_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ser_gl_acct_id = models.CharField(db_column='SER_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    qty_on_hand = models.DecimalField(db_column='QTY_ON_HAND', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    qty_available_iss = models.DecimalField(db_column='QTY_AVAILABLE_ISS', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    qty_available_mrp = models.DecimalField(db_column='QTY_AVAILABLE_MRP', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    qty_on_order = models.DecimalField(db_column='QTY_ON_ORDER', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    qty_in_demand = models.DecimalField(db_column='QTY_IN_DEMAND', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    qty_committed = models.DecimalField(db_column='QTY_COMMITTED', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    tariff_code = models.CharField(db_column='TARIFF_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    tariff_type = models.CharField(db_column='TARIFF_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    vat_code = models.CharField(db_column='VAT_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    orig_country_id = models.CharField(db_column='ORIG_COUNTRY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    intrastat_exempt = models.CharField(db_column='INTRASTAT_EXEMPT', max_length=1)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    status_eff_date = models.DateTimeField(db_column='STATUS_EFF_DATE', blank=True, null=True)  # Field name made lowercase.
    use_supply_bef_lt = models.CharField(db_column='USE_SUPPLY_BEF_LT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    minimum_leadtime = models.SmallIntegerField(db_column='MINIMUM_LEADTIME', blank=True, null=True)  # Field name made lowercase.
    leadtime_buffer = models.SmallIntegerField(db_column='LEADTIME_BUFFER', blank=True, null=True)  # Field name made lowercase.
    emergency_stockpct = models.IntegerField(db_column='EMERGENCY_STOCKPCT', blank=True, null=True)  # Field name made lowercase.
    replenish_level = models.DecimalField(db_column='REPLENISH_LEVEL', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    min_batch_size = models.DecimalField(db_column='MIN_BATCH_SIZE', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    yellow_stockpct = models.IntegerField(db_column='YELLOW_STOCKPCT', blank=True, null=True)  # Field name made lowercase.
    mrp_exception_info = models.CharField(db_column='MRP_EXCEPTION_INFO', max_length=80, blank=True, null=True)  # Field name made lowercase.
    multiple_order_qty = models.DecimalField(db_column='MULTIPLE_ORDER_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    last_implode_date = models.DateTimeField(db_column='LAST_IMPLODE_DATE', blank=True, null=True)  # Field name made lowercase.
    mro_class = models.CharField(db_column='MRO_CLASS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    udf_layout_id = models.CharField(db_column='UDF_LAYOUT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    user_1 = models.CharField(db_column='USER_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_2 = models.CharField(db_column='USER_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_3 = models.CharField(db_column='USER_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_4 = models.CharField(db_column='USER_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_5 = models.CharField(db_column='USER_5', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_6 = models.CharField(db_column='USER_6', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_7 = models.CharField(db_column='USER_7', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_8 = models.CharField(db_column='USER_8', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_9 = models.CharField(db_column='USER_9', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_10 = models.CharField(db_column='USER_10', max_length=80, blank=True, null=True)  # Field name made lowercase.
    buffer_profile_id = models.CharField(db_column='BUFFER_PROFILE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    adu_horizon = models.SmallIntegerField(db_column='ADU_HORIZON', blank=True, null=True)  # Field name made lowercase.
    asr_leadtime = models.SmallIntegerField(db_column='ASR_LEADTIME', blank=True, null=True)  # Field name made lowercase.
    onhand_alert_red_pct = models.SmallIntegerField(db_column='ONHAND_ALERT_RED_PCT', blank=True, null=True)  # Field name made lowercase.
    last_abc_date = models.DateTimeField(db_column='LAST_ABC_DATE', blank=True, null=True)  # Field name made lowercase.
    process_type = models.CharField(db_column='PROCESS_TYPE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    bid_rate_category_id = models.CharField(db_column='BID_RATE_CATEGORY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='CREATE_DATE')  # Field name made lowercase.
    modify_date = models.DateTimeField(db_column='MODIFY_DATE', blank=True, null=True)  # Field name made lowercase.
    is_rate_based = models.CharField(db_column='IS_RATE_BASED', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'PART_SITE'
        unique_together = (('site_id', 'part'),)


class PartWarehouse(TruncatedModel):
    rowid = models.AutoField(primary_key=True, db_column='ROWID')
    warehouse_id = models.CharField(db_column='WAREHOUSE_ID', max_length=15)  # Field name made lowercase.
    part_id = models.CharField(db_column='PART_ID', max_length=30)  # Field name made lowercase.
    min_inv_qty = models.DecimalField(db_column='MIN_INV_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    committed_co = models.DecimalField(db_column='COMMITTED_CO', max_digits=20, decimal_places=8)  # Field name made lowercase.
    committed_req = models.DecimalField(db_column='COMMITTED_REQ', max_digits=20, decimal_places=8)  # Field name made lowercase.
    committed_plreq = models.DecimalField(db_column='COMMITTED_PLREQ', max_digits=20, decimal_places=8)  # Field name made lowercase.
    committed_ibt = models.DecimalField(db_column='COMMITTED_IBT', max_digits=20, decimal_places=8)  # Field name made lowercase.
    available_qty = models.DecimalField(db_column='AVAILABLE_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    expected_po = models.DecimalField(db_column='EXPECTED_PO', max_digits=20, decimal_places=8)  # Field name made lowercase.
    expected_wo = models.DecimalField(db_column='EXPECTED_WO', max_digits=20, decimal_places=8)  # Field name made lowercase.
    expected_pl = models.DecimalField(db_column='EXPECTED_PL', max_digits=20, decimal_places=8)  # Field name made lowercase.
    expected_ibt = models.DecimalField(db_column='EXPECTED_IBT', max_digits=20, decimal_places=8)  # Field name made lowercase.
    expect_commit_co = models.DecimalField(db_column='EXPECT_COMMIT_CO', max_digits=20, decimal_places=8)  # Field name made lowercase.
    expect_commit_req = models.DecimalField(db_column='EXPECT_COMMIT_REQ', max_digits=20, decimal_places=8)  # Field name made lowercase.
    expect_commit_plr = models.DecimalField(db_column='EXPECT_COMMIT_PLR', max_digits=20, decimal_places=8)  # Field name made lowercase.
    expect_commit_ibt = models.DecimalField(db_column='EXPECT_COMMIT_IBT', max_digits=20, decimal_places=8)  # Field name made lowercase.
    unalloc_demand_qty = models.DecimalField(db_column='UNALLOC_DEMAND_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    outbound_qty = models.DecimalField(db_column='OUTBOUND_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    on_hold_qty = models.DecimalField(db_column='ON_HOLD_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    locked_qty = models.DecimalField(db_column='LOCKED_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    unavailable_qty = models.DecimalField(db_column='UNAVAILABLE_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    auto_create = models.CharField(db_column='AUTO_CREATE', max_length=1)  # Field name made lowercase.
    source_type = models.CharField(db_column='SOURCE_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    source_id = models.CharField(db_column='SOURCE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    planning_leadtime = models.SmallIntegerField(db_column='PLANNING_LEADTIME')  # Field name made lowercase.
    order_policy = models.CharField(db_column='ORDER_POLICY', max_length=1)  # Field name made lowercase.
    order_point = models.DecimalField(db_column='ORDER_POINT', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    order_up_to_qty = models.DecimalField(db_column='ORDER_UP_TO_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    safety_stock_qty = models.DecimalField(db_column='SAFETY_STOCK_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    fixed_order_qty = models.DecimalField(db_column='FIXED_ORDER_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    days_of_supply = models.SmallIntegerField(db_column='DAYS_OF_SUPPLY', blank=True, null=True)  # Field name made lowercase.
    minimum_order_qty = models.DecimalField(db_column='MINIMUM_ORDER_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    maximum_order_qty = models.DecimalField(db_column='MAXIMUM_ORDER_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    planner_user_id = models.CharField(db_column='PLANNER_USER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    buyer_user_id = models.CharField(db_column='BUYER_USER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    annual_usage_qty = models.DecimalField(db_column='ANNUAL_USAGE_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    multiple_order_qty = models.DecimalField(db_column='MULTIPLE_ORDER_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    demand_fence_1 = models.IntegerField(db_column='DEMAND_FENCE_1', blank=True, null=True)  # Field name made lowercase.
    demand_fence_2 = models.IntegerField(db_column='DEMAND_FENCE_2', blank=True, null=True)  # Field name made lowercase.
    mrp_exceptions = models.CharField(db_column='MRP_EXCEPTIONS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mrp_exception_info = models.CharField(db_column='MRP_EXCEPTION_INFO', max_length=80, blank=True, null=True)  # Field name made lowercase.
    mrp_required = models.CharField(db_column='MRP_REQUIRED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    minimum_leadtime = models.SmallIntegerField(db_column='MINIMUM_LEADTIME', blank=True, null=True)  # Field name made lowercase.
    leadtime_buffer = models.SmallIntegerField(db_column='LEADTIME_BUFFER', blank=True, null=True)  # Field name made lowercase.
    emergency_stockpct = models.IntegerField(db_column='EMERGENCY_STOCKPCT', blank=True, null=True)  # Field name made lowercase.
    yellow_stockpct = models.IntegerField(db_column='YELLOW_STOCKPCT', blank=True, null=True)  # Field name made lowercase.
    replenish_level = models.DecimalField(db_column='REPLENISH_LEVEL', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    count_sequence = models.IntegerField(db_column='COUNT_SEQUENCE')  # Field name made lowercase.
    adu_horizon = models.SmallIntegerField(db_column='ADU_HORIZON', blank=True, null=True)  # Field name made lowercase.
    asr_leadtime = models.SmallIntegerField(db_column='ASR_LEADTIME', blank=True, null=True)  # Field name made lowercase.
    onhand_alert_red_pct = models.SmallIntegerField(db_column='ONHAND_ALERT_RED_PCT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'PART_WAREHOUSE'
        unique_together = (('warehouse_id', 'part_id'),)


class Product(TruncatedModel):  # Field name made lowercase.
    code = models.CharField(db_column='CODE', primary_key=True, max_length=15)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=80, blank=True, null=True)  # Field name made lowercase.
    rev_gl_acct_id = models.CharField(db_column='REV_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    adj_gl_acct_id = models.CharField(db_column='ADJ_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    inv_mat_gl_acct_id = models.CharField(db_column='INV_MAT_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    inv_lab_gl_acct_id = models.CharField(db_column='INV_LAB_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    inv_bur_gl_acct_id = models.CharField(db_column='INV_BUR_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    inv_ser_gl_acct_id = models.CharField(db_column='INV_SER_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    var_mat_gl_acct_id = models.CharField(db_column='VAR_MAT_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    var_lab_gl_acct_id = models.CharField(db_column='VAR_LAB_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    var_bur_gl_acct_id = models.CharField(db_column='VAR_BUR_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    var_ser_gl_acct_id = models.CharField(db_column='VAR_SER_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cgs_mat_gl_acct_id = models.CharField(db_column='CGS_MAT_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cgs_lab_gl_acct_id = models.CharField(db_column='CGS_LAB_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cgs_bur_gl_acct_id = models.CharField(db_column='CGS_BUR_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cgs_ser_gl_acct_id = models.CharField(db_column='CGS_SER_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wip_mat_gl_acct_id = models.CharField(db_column='WIP_MAT_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wip_lab_gl_acct_id = models.CharField(db_column='WIP_LAB_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wip_bur_gl_acct_id = models.CharField(db_column='WIP_BUR_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wip_ser_gl_acct_id = models.CharField(db_column='WIP_SER_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    withholding_code = models.CharField(db_column='WITHHOLDING_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    demand_fence_1 = models.IntegerField(db_column='DEMAND_FENCE_1', blank=True, null=True)  # Field name made lowercase.
    demand_fence_2 = models.IntegerField(db_column='DEMAND_FENCE_2', blank=True, null=True)  # Field name made lowercase.
    cost_category_id = models.CharField(db_column='COST_CATEGORY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    active_flag = models.CharField(db_column='ACTIVE_FLAG', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'PRODUCT'


class PurchaseOrder(TruncatedModel):
    id = models.CharField(db_column='ID', primary_key=True, max_length=15)  # Field name made lowercase.
    # vendor = models.ForeignKey('Vendor', models.DO_NOTHING, db_column='VENDOR_ID')  # Field name made lowercase.
    contact = models.ForeignKey(Contact, models.DO_NOTHING, db_column='CONTACT_ID', blank=True, null=True)  # Field name made lowercase.
    contact_first_name = models.CharField(db_column='CONTACT_FIRST_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact_last_name = models.CharField(db_column='CONTACT_LAST_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact_initial = models.CharField(db_column='CONTACT_INITIAL', max_length=2, blank=True, null=True)  # Field name made lowercase.
    contact_position = models.CharField(db_column='CONTACT_POSITION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    contact_honorific = models.CharField(db_column='CONTACT_HONORIFIC', max_length=15, blank=True, null=True)  # Field name made lowercase.
    contact_salutation = models.CharField(db_column='CONTACT_SALUTATION', max_length=60, blank=True, null=True)  # Field name made lowercase.
    contact_phone = models.CharField(db_column='CONTACT_PHONE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contact_fax = models.CharField(db_column='CONTACT_FAX', max_length=20, blank=True, null=True)  # Field name made lowercase.
    purc_ord_addr_no = models.IntegerField(db_column='PURC_ORD_ADDR_NO', blank=True, null=True)  # Field name made lowercase.
    # shipto_addr_no = models.ForeignKey('ShiptoAddress', models.DO_NOTHING, db_column='SHIPTO_ADDR_NO', blank=True, null=True)  # Field name made lowercase.
    order_date = models.DateTimeField(db_column='ORDER_DATE')  # Field name made lowercase.
    desired_recv_date = models.DateTimeField(db_column='DESIRED_RECV_DATE', blank=True, null=True)  # Field name made lowercase.
    buyer = models.CharField(db_column='BUYER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    free_on_board = models.CharField(db_column='FREE_ON_BOARD', max_length=25, blank=True, null=True)  # Field name made lowercase.
    ship_via = models.CharField(db_column='SHIP_VIA', max_length=40, blank=True, null=True)  # Field name made lowercase.
    sales_tax_group_id = models.CharField(db_column='SALES_TAX_GROUP_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1)  # Field name made lowercase.
    back_order = models.CharField(db_column='BACK_ORDER', max_length=1)  # Field name made lowercase.
    sell_rate = models.DecimalField(db_column='SELL_RATE', max_digits=15, decimal_places=8)  # Field name made lowercase.
    buy_rate = models.DecimalField(db_column='BUY_RATE', max_digits=15, decimal_places=8)  # Field name made lowercase.
    # site = models.ForeignKey('Site', models.DO_NOTHING, db_column='SITE_ID')  # Field name made lowercase.
    posting_candidate = models.CharField(db_column='POSTING_CANDIDATE', max_length=1)  # Field name made lowercase.
    last_received_date = models.DateTimeField(db_column='LAST_RECEIVED_DATE', blank=True, null=True)  # Field name made lowercase.
    total_amt_ordered = models.DecimalField(db_column='TOTAL_AMT_ORDERED', max_digits=23, decimal_places=8)  # Field name made lowercase.
    total_amt_recvd = models.DecimalField(db_column='TOTAL_AMT_RECVD', max_digits=23, decimal_places=8)  # Field name made lowercase.
    marked_for_purge = models.CharField(db_column='MARKED_FOR_PURGE', max_length=1)  # Field name made lowercase.
    exch_rate_fixed = models.CharField(db_column='EXCH_RATE_FIXED', max_length=1)  # Field name made lowercase.
    promise_date = models.DateTimeField(db_column='PROMISE_DATE', blank=True, null=True)  # Field name made lowercase.
    printed_date = models.DateTimeField(db_column='PRINTED_DATE', blank=True, null=True)  # Field name made lowercase.
    edi_blanket_flag = models.CharField(db_column='EDI_BLANKET_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    edi_blanket_po_no = models.CharField(db_column='EDI_BLANKET_PO_NO', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contract_id = models.CharField(db_column='CONTRACT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shipto_id = models.CharField(db_column='SHIPTO_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    terms_net_type = models.CharField(db_column='TERMS_NET_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terms_net_days = models.SmallIntegerField(db_column='TERMS_NET_DAYS', blank=True, null=True)  # Field name made lowercase.
    terms_net_date = models.DateTimeField(db_column='TERMS_NET_DATE', blank=True, null=True)  # Field name made lowercase.
    terms_disc_type = models.CharField(db_column='TERMS_DISC_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terms_disc_days = models.SmallIntegerField(db_column='TERMS_DISC_DAYS', blank=True, null=True)  # Field name made lowercase.
    terms_disc_date = models.DateTimeField(db_column='TERMS_DISC_DATE', blank=True, null=True)  # Field name made lowercase.
    terms_disc_percent = models.DecimalField(db_column='TERMS_DISC_PERCENT', max_digits=5, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    terms_description = models.CharField(db_column='TERMS_DESCRIPTION', max_length=80, blank=True, null=True)  # Field name made lowercase.
    # currency = models.ForeignKey('Currency', models.DO_NOTHING, db_column='CURRENCY_ID', blank=True, null=True)  # Field name made lowercase.
    warehouse_id = models.CharField(db_column='WAREHOUSE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='CREATE_DATE')  # Field name made lowercase.
    contact_mobile = models.CharField(db_column='CONTACT_MOBILE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contact_email = models.CharField(db_column='CONTACT_EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    user_1 = models.CharField(db_column='USER_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_2 = models.CharField(db_column='USER_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_3 = models.CharField(db_column='USER_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_4 = models.CharField(db_column='USER_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_5 = models.CharField(db_column='USER_5', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_6 = models.CharField(db_column='USER_6', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_7 = models.CharField(db_column='USER_7', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_8 = models.CharField(db_column='USER_8', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_9 = models.CharField(db_column='USER_9', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_10 = models.CharField(db_column='USER_10', max_length=80, blank=True, null=True)  # Field name made lowercase.
    udf_layout_id = models.CharField(db_column='UDF_LAYOUT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    dispatch_addr_id = models.CharField(db_column='DISPATCH_ADDR_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    carrier_id = models.CharField(db_column='CARRIER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    shipfrom_id = models.CharField(db_column='SHIPFROM_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    owner_id = models.CharField(db_column='OWNER_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    dispatched = models.CharField(db_column='DISPATCHED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vend_bank_id = models.CharField(db_column='VEND_BANK_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    vend_pack_id = models.CharField(db_column='VEND_PACK_ID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    vend_pack_date = models.DateTimeField(db_column='VEND_PACK_DATE', blank=True, null=True)  # Field name made lowercase.
    vend_freight_id = models.CharField(db_column='VEND_FREIGHT_ID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    consignment = models.CharField(db_column='CONSIGNMENT', max_length=1)  # Field name made lowercase.
    consigned_whs_id = models.CharField(db_column='CONSIGNED_WHS_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    status_eff_date = models.DateTimeField(db_column='STATUS_EFF_DATE')  # Field name made lowercase.
    promise_ship_date = models.DateTimeField(db_column='PROMISE_SHIP_DATE', blank=True, null=True)  # Field name made lowercase.
    sales_order_id = models.CharField(db_column='SALES_ORDER_ID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    special_price_auth = models.CharField(db_column='SPECIAL_PRICE_AUTH', max_length=100, blank=True, null=True)  # Field name made lowercase.
    entered_by = models.CharField(db_column='ENTERED_BY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    # terms = models.ForeignKey('Terms', models.DO_NOTHING, db_column='TERMS_ID', blank=True, null=True)  # Field name made lowercase.
    internal_order = models.CharField(db_column='INTERNAL_ORDER', max_length=1, blank=True, null=True)  # Field name made lowercase.
    contact_phone_ext = models.CharField(db_column='CONTACT_PHONE_EXT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    email_notification = models.CharField(db_column='EMAIL_NOTIFICATION', max_length=1)  # Field name made lowercase.
    email_vend_on_new_order = models.CharField(db_column='EMAIL_VEND_ON_NEW_ORDER', max_length=1)  # Field name made lowercase.
    email_vend_on_chg_order = models.CharField(db_column='EMAIL_VEND_ON_CHG_ORDER', max_length=1)  # Field name made lowercase.
    email_vend_on_po_receipt = models.CharField(db_column='EMAIL_VEND_ON_PO_RECEIPT', max_length=1)  # Field name made lowercase.
    email_empl_on_new_order = models.CharField(db_column='EMAIL_EMPL_ON_NEW_ORDER', max_length=1)  # Field name made lowercase.
    email_empl_on_chg_order = models.CharField(db_column='EMAIL_EMPL_ON_CHG_ORDER', max_length=1)  # Field name made lowercase.
    email_empl_on_po_receipt = models.CharField(db_column='EMAIL_EMPL_ON_PO_RECEIPT', max_length=1)  # Field name made lowercase.
    email_empl_on_inv_paid = models.CharField(db_column='EMAIL_EMPL_ON_INV_PAID', max_length=1)  # Field name made lowercase.
    confirmed_ship_date = models.DateTimeField(db_column='CONFIRMED_SHIP_DATE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'PURCHASE_ORDER'


class PurcOrderLine(TruncatedModel):
    purc_order = models.OneToOneField(PurchaseOrder, models.DO_NOTHING, db_column='PURC_ORDER_ID', primary_key=True)  # Field name made lowercase.
    line_no = models.SmallIntegerField(db_column='LINE_NO')  # Field name made lowercase.
    part = models.ForeignKey(Part, models.DO_NOTHING, db_column='PART_ID', blank=True, null=True)  # Field name made lowercase.
    vendor_part_id = models.CharField(db_column='VENDOR_PART_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    service = models.ForeignKey('Service', models.DO_NOTHING, db_column='SERVICE_ID', blank=True, null=True)  # Field name made lowercase.
    user_order_qty = models.DecimalField(db_column='USER_ORDER_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    order_qty = models.DecimalField(db_column='ORDER_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    # purchase_um = models.ForeignKey('Units', models.DO_NOTHING, db_column='PURCHASE_UM', blank=True, null=True)  # Field name made lowercase.
    unit_price = models.DecimalField(db_column='UNIT_PRICE', max_digits=22, decimal_places=8)  # Field name made lowercase.
    trade_disc_percent = models.DecimalField(db_column='TRADE_DISC_PERCENT', max_digits=6, decimal_places=3)  # Field name made lowercase.
    fixed_charge = models.DecimalField(db_column='FIXED_CHARGE', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    est_freight = models.DecimalField(db_column='EST_FREIGHT', max_digits=23, decimal_places=8)  # Field name made lowercase.
    # gl_expense_acct = models.ForeignKey(Account, models.DO_NOTHING, db_column='GL_EXPENSE_ACCT_ID', blank=True, null=True)  # Field name made lowercase.
    sales_tax_group_id = models.CharField(db_column='SALES_TAX_GROUP_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    product_code = models.CharField(db_column='PRODUCT_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    commodity_code = models.CharField(db_column='COMMODITY_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    desired_recv_date = models.DateTimeField(db_column='DESIRED_RECV_DATE', blank=True, null=True)  # Field name made lowercase.
    line_status = models.CharField(db_column='LINE_STATUS', max_length=1)  # Field name made lowercase.
    last_received_date = models.DateTimeField(db_column='LAST_RECEIVED_DATE', blank=True, null=True)  # Field name made lowercase.
    total_act_freight = models.DecimalField(db_column='TOTAL_ACT_FREIGHT', max_digits=23, decimal_places=8)  # Field name made lowercase.
    total_usr_recd_qty = models.DecimalField(db_column='TOTAL_USR_RECD_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    total_received_qty = models.DecimalField(db_column='TOTAL_RECEIVED_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    total_amt_recvd = models.DecimalField(db_column='TOTAL_AMT_RECVD', max_digits=23, decimal_places=8)  # Field name made lowercase.
    total_amt_ordered = models.DecimalField(db_column='TOTAL_AMT_ORDERED', max_digits=23, decimal_places=8)  # Field name made lowercase.
    mfg_name = models.CharField(db_column='MFG_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mfg_part_id = models.CharField(db_column='MFG_PART_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    promise_date = models.DateTimeField(db_column='PROMISE_DATE', blank=True, null=True)  # Field name made lowercase.
    piece_count = models.DecimalField(db_column='PIECE_COUNT', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    length = models.DecimalField(db_column='LENGTH', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    width = models.DecimalField(db_column='WIDTH', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    height = models.DecimalField(db_column='HEIGHT', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    dimensions_um = models.CharField(db_column='DIMENSIONS_UM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vat_code = models.CharField(db_column='VAT_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    total_dispatch_qty = models.DecimalField(db_column='TOTAL_DISPATCH_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    total_usr_disp_qty = models.DecimalField(db_column='TOTAL_USR_DISP_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    minimum_charge = models.DecimalField(db_column='MINIMUM_CHARGE', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    last_dispatch_date = models.DateTimeField(db_column='LAST_DISPATCH_DATE', blank=True, null=True)  # Field name made lowercase.
    edi_blanket_qty = models.DecimalField(db_column='EDI_BLANKET_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_blanket_usrqty = models.DecimalField(db_column='EDI_BLANKET_USRQTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_accum_qty_rel = models.DecimalField(db_column='EDI_ACCUM_QTY_REL', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_accum_usr_rel = models.DecimalField(db_column='EDI_ACCUM_USR_REL', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_accum_qty_rec = models.DecimalField(db_column='EDI_ACCUM_QTY_REC', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_accum_usr_rec = models.DecimalField(db_column='EDI_ACCUM_USR_REC', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_last_rec_date = models.DateTimeField(db_column='EDI_LAST_REC_DATE', blank=True, null=True)  # Field name made lowercase.
    edi_release_no = models.CharField(db_column='EDI_RELEASE_NO', max_length=30, blank=True, null=True)  # Field name made lowercase.
    edi_release_date = models.DateTimeField(db_column='EDI_RELEASE_DATE', blank=True, null=True)  # Field name made lowercase.
    edi_qty_released = models.DecimalField(db_column='EDI_QTY_RELEASED', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_usr_qty_rel = models.DecimalField(db_column='EDI_USR_QTY_REL', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    edi_req_rel_date = models.DateTimeField(db_column='EDI_REQ_REL_DATE', blank=True, null=True)  # Field name made lowercase.
    shipto_id = models.CharField(db_column='SHIPTO_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    warehouse_id = models.CharField(db_column='WAREHOUSE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    wip_vas_required = models.CharField(db_column='WIP_VAS_REQUIRED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    allocated_qty = models.DecimalField(db_column='ALLOCATED_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    fulfilled_qty = models.DecimalField(db_column='FULFILLED_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    hts_code = models.CharField(db_column='HTS_CODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    orig_country_id = models.CharField(db_column='ORIG_COUNTRY_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    user_1 = models.CharField(db_column='USER_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_2 = models.CharField(db_column='USER_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_3 = models.CharField(db_column='USER_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_4 = models.CharField(db_column='USER_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_5 = models.CharField(db_column='USER_5', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_6 = models.CharField(db_column='USER_6', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_7 = models.CharField(db_column='USER_7', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_8 = models.CharField(db_column='USER_8', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_9 = models.CharField(db_column='USER_9', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_10 = models.CharField(db_column='USER_10', max_length=80, blank=True, null=True)  # Field name made lowercase.
    udf_layout_id = models.CharField(db_column='UDF_LAYOUT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    # vat_category = models.ForeignKey('VatCategory', models.DO_NOTHING, db_column='vat_category', blank=True, null=True)
    vat_amount = models.DecimalField(db_column='VAT_AMOUNT', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    vat_rcv_amount = models.DecimalField(db_column='VAT_RCV_AMOUNT', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    wbs_code = models.CharField(db_column='WBS_CODE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    department_id = models.CharField(db_column='DEPARTMENT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    part_gl_account = models.CharField(db_column='PART_GL_ACCOUNT', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cost_category_id = models.CharField(db_column='COST_CATEGORY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    proj_ref_seq_no = models.SmallIntegerField(db_column='PROJ_REF_SEQ_NO', blank=True, null=True)  # Field name made lowercase.
    proj_ref_sub_id = models.CharField(db_column='PROJ_REF_SUB_ID', max_length=3, blank=True, null=True)  # Field name made lowercase.
    dispatch_addr_id = models.CharField(db_column='DISPATCH_ADDR_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    shipfrom_id = models.CharField(db_column='SHIPFROM_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    qa_qty = models.DecimalField(db_column='QA_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    owner_id = models.CharField(db_column='OWNER_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    trace_qty = models.DecimalField(db_column='TRACE_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    dispatched = models.CharField(db_column='DISPATCHED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    # trans_category = models.ForeignKey('TransCategory', models.DO_NOTHING, db_column='TRANS_CATEGORY_ID', blank=True, null=True)  # Field name made lowercase.
    orig_stage_revision_id = models.CharField(db_column='ORIG_STAGE_REVISION_ID', max_length=24, blank=True, null=True)  # Field name made lowercase.
    consigned_whs_id = models.CharField(db_column='CONSIGNED_WHS_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    consigned_loc_id = models.CharField(db_column='CONSIGNED_LOC_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    status_eff_date = models.DateTimeField(db_column='STATUS_EFF_DATE')  # Field name made lowercase.
    promise_ship_date = models.DateTimeField(db_column='PROMISE_SHIP_DATE', blank=True, null=True)  # Field name made lowercase.
    special_price_auth = models.CharField(db_column='SPECIAL_PRICE_AUTH', max_length=100, blank=True, null=True)  # Field name made lowercase.
    contract_id = models.CharField(db_column='CONTRACT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contract_line_no = models.SmallIntegerField(db_column='CONTRACT_LINE_NO', blank=True, null=True)  # Field name made lowercase.
    entered_by = models.CharField(db_column='ENTERED_BY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    # site = models.ForeignKey('Site', models.DO_NOTHING, db_column='SITE_ID')  # Field name made lowercase.
    posting_candidate = models.CharField(db_column='POSTING_CANDIDATE', max_length=1)  # Field name made lowercase.
    email_notification = models.CharField(db_column='EMAIL_NOTIFICATION', max_length=1)  # Field name made lowercase.
    vat_ie_percent = models.DecimalField(db_column='VAT_IE_PERCENT', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    vat_ie_amount = models.DecimalField(db_column='VAT_IE_AMOUNT', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    vat_ie_dr_gl_acct_id = models.CharField(db_column='VAT_IE_DR_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    vat_ie_cr_gl_acct_id = models.CharField(db_column='VAT_IE_CR_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    confirmed_ship_date = models.DateTimeField(db_column='CONFIRMED_SHIP_DATE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'PURC_ORDER_LINE'
        unique_together = (('purc_order', 'line_no'),)


class Requirement(TruncatedModel):  # Field name made lowercase.
    rowid = models.AutoField(primary_key=True, db_column='ROWID')
    workorder_type = models.CharField(db_column='WORKORDER_TYPE', max_length=1)  # Field name made lowercase.
    workorder_base = models.CharField(db_column='WORKORDER_BASE_ID', max_length=30)  # Field name made lowercase.
    workorder_lot = models.CharField(db_column='WORKORDER_LOT_ID', max_length=3)  # Field name made lowercase.
    workorder_split = models.CharField(db_column='WORKORDER_SPLIT_ID', max_length=3)  # Field name made lowercase.
    workorder_sub = models.CharField(db_column='WORKORDER_SUB_ID', max_length=3)  # Field name made lowercase.
    operation_seq_no = models.SmallIntegerField(db_column='OPERATION_SEQ_NO')  # Field name made lowercase.
    piece_no = models.SmallIntegerField(db_column='PIECE_NO')  # Field name made lowercase.
    subord_wo_sub = models.CharField(db_column='SUBORD_WO_SUB_ID', blank=True, null=True, max_length=3)  # Field name made lowercase.
    part = models.ForeignKey(Part, models.DO_NOTHING, db_column='PART_ID', blank=True, null=True)  # Field name made lowercase.
    reference = models.CharField(db_column='REFERENCE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1)  # Field name made lowercase.
    qty_per = models.DecimalField(db_column='QTY_PER', max_digits=20, decimal_places=8)  # Field name made lowercase.
    qty_per_type = models.CharField(db_column='QTY_PER_TYPE', max_length=1)  # Field name made lowercase.
    fixed_qty = models.DecimalField(db_column='FIXED_QTY', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    scrap_percent = models.DecimalField(db_column='SCRAP_PERCENT', max_digits=5, decimal_places=2, default=0)  # Field name made lowercase.
    dimensions = models.CharField(db_column='DIMENSIONS', max_length=80, blank=True, null=True)  # Field name made lowercase.
    dim_expression = models.CharField(db_column='DIM_EXPRESSION', max_length=128, blank=True, null=True)  # Field name made lowercase.
    usage_um = models.CharField(db_column='USAGE_UM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    effective_date = models.DateTimeField(db_column='EFFECTIVE_DATE', blank=True, null=True)  # Field name made lowercase.
    discontinue_date = models.DateTimeField(db_column='DISCONTINUE_DATE', blank=True, null=True)  # Field name made lowercase.
    calc_qty = models.DecimalField(db_column='CALC_QTY', max_digits=20, decimal_places=8, blank=True, null=True, default=0)  # Field name made lowercase.
    issued_qty = models.DecimalField(db_column='ISSUED_QTY', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    required_date = models.DateTimeField(db_column='REQUIRED_DATE', blank=True, null=True)  # Field name made lowercase.
    close_date = models.DateTimeField(db_column='CLOSE_DATE', blank=True, null=True)  # Field name made lowercase.
    unit_material_cost = models.DecimalField(db_column='UNIT_MATERIAL_COST', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    unit_labor_cost = models.DecimalField(db_column='UNIT_LABOR_COST', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    unit_burden_cost = models.DecimalField(db_column='UNIT_BURDEN_COST', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    unit_service_cost = models.DecimalField(db_column='UNIT_SERVICE_COST', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    burden_percent = models.DecimalField(db_column='BURDEN_PERCENT', max_digits=5, decimal_places=2, default=0)  # Field name made lowercase.
    burden_per_unit = models.DecimalField(db_column='BURDEN_PER_UNIT', max_digits=22, decimal_places=8, default=0)  # Field name made lowercase.
    fixed_cost = models.DecimalField(db_column='FIXED_COST', max_digits=23, decimal_places=8, blank=True, null=True, default=0)  # Field name made lowercase.
    drawing_id = models.CharField(db_column='DRAWING_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    drawing_rev_no = models.CharField(db_column='DRAWING_REV_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    vendor_id = models.CharField(db_column='VENDOR_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vendor_part_id = models.CharField(db_column='VENDOR_PART_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    est_material_cost = models.DecimalField(db_column='EST_MATERIAL_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    est_labor_cost = models.DecimalField(db_column='EST_LABOR_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    est_burden_cost = models.DecimalField(db_column='EST_BURDEN_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    est_service_cost = models.DecimalField(db_column='EST_SERVICE_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    rem_material_cost = models.DecimalField(db_column='REM_MATERIAL_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    rem_labor_cost = models.DecimalField(db_column='REM_LABOR_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    rem_burden_cost = models.DecimalField(db_column='REM_BURDEN_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    rem_service_cost = models.DecimalField(db_column='REM_SERVICE_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    act_material_cost = models.DecimalField(db_column='ACT_MATERIAL_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    act_labor_cost = models.DecimalField(db_column='ACT_LABOR_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    act_burden_cost = models.DecimalField(db_column='ACT_BURDEN_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    act_service_cost = models.DecimalField(db_column='ACT_SERVICE_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    mfg_name = models.CharField(db_column='MFG_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mfg_part_id = models.CharField(db_column='MFG_PART_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    protect_cost = models.CharField(db_column='PROTECT_COST', max_length=1, default="N")  # Field name made lowercase.
    length = models.DecimalField(db_column='LENGTH', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    width = models.DecimalField(db_column='WIDTH', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    height = models.DecimalField(db_column='HEIGHT', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    drawing_file = models.CharField(db_column='DRAWING_FILE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    warehouse_id = models.CharField(db_column='WAREHOUSE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    allocated_qty = models.DecimalField(db_column='ALLOCATED_QTY', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    fulfilled_qty = models.DecimalField(db_column='FULFILLED_QTY', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    planning_leadtime = models.SmallIntegerField(db_column='PLANNING_LEADTIME', blank=True, null=True)  # Field name made lowercase.
    required_for_setup = models.CharField(db_column='REQUIRED_FOR_SETUP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    user_1 = models.CharField(db_column='USER_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_2 = models.CharField(db_column='USER_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_3 = models.CharField(db_column='USER_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_4 = models.CharField(db_column='USER_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_5 = models.CharField(db_column='USER_5', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_6 = models.CharField(db_column='USER_6', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_7 = models.CharField(db_column='USER_7', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_8 = models.CharField(db_column='USER_8', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_9 = models.CharField(db_column='USER_9', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_10 = models.CharField(db_column='USER_10', max_length=80, blank=True, null=True)  # Field name made lowercase.
    udf_layout_id = models.CharField(db_column='UDF_LAYOUT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    calc_fixed_scrap = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True, default=0)
    wbs_code = models.CharField(db_column='WBS_CODE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wbs_description = models.CharField(db_column='WBS_DESCRIPTION', max_length=80, blank=True, null=True)  # Field name made lowercase.
    wbs_clin = models.CharField(db_column='WBS_CLIN', max_length=15, blank=True, null=True)  # Field name made lowercase.
    wbs_customer_wbs = models.CharField(db_column='WBS_CUSTOMER_WBS', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wbs_cdrl = models.CharField(db_column='WBS_CDRL', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wbs_tdc = models.CharField(db_column='WBS_TDC', max_length=30, blank=True, null=True)  # Field name made lowercase.
    inherit_warehouse = models.CharField(db_column='INHERIT_WAREHOUSE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    location_id = models.CharField(db_column='LOCATION_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    due_date = models.DateTimeField(db_column='DUE_DATE', blank=True, null=True)  # Field name made lowercase.
    dispatched = models.CharField(db_column='DISPATCHED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    orig_stage_revision_id = models.CharField(db_column='ORIG_STAGE_REVISION_ID', max_length=24, blank=True, null=True)  # Field name made lowercase.
    status_eff_date = models.DateTimeField(db_column='STATUS_EFF_DATE')  # Field name made lowercase.
    alt_part_parent_piece_no = models.SmallIntegerField(db_column='ALT_PART_PARENT_PIECE_NO', blank=True, null=True)  # Field name made lowercase.
    site_id = models.CharField(db_column='SITE_ID', max_length=15)  # Field name made lowercase.
    bid_rate_category_id = models.CharField(db_column='BID_RATE_CATEGORY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'REQUIREMENT'
        unique_together = (('workorder_type', 'workorder_base', 'workorder_lot', 'workorder_split', 'workorder_sub', 'operation_seq_no', 'piece_no'),)


class Service(TruncatedModel):
    id = models.CharField(db_column='ID', primary_key=True, max_length=15)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=40, blank=True, null=True)  # Field name made lowercase.
    vendor = models.ForeignKey('Vendor', models.DO_NOTHING, db_column='VENDOR_ID', blank=True, null=True)  # Field name made lowercase.
    vat_code = models.CharField(db_column='VAT_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    service_part_id = models.CharField(db_column='SERVICE_PART_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    usage_um = models.CharField(db_column='USAGE_UM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    plan_transit_days = models.SmallIntegerField(db_column='PLAN_TRANSIT_DAYS', blank=True, null=True)  # Field name made lowercase.
    schedule_rank = models.SmallIntegerField(db_column='SCHEDULE_RANK', blank=True, null=True)  # Field name made lowercase.
    run = models.DecimalField(db_column='RUN', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    run_type = models.CharField(db_column='RUN_TYPE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    load_size_qty = models.DecimalField(db_column='LOAD_SIZE_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    minimum_move_qty = models.DecimalField(db_column='MINIMUM_MOVE_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    long_description = models.BinaryField(db_column='LONG_DESCRIPTION', blank=True, null=True)  # Field name made lowercase.
    intrastat_include = models.CharField(db_column='INTRASTAT_INCLUDE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    status_eff_date = models.DateTimeField(db_column='STATUS_EFF_DATE')  # Field name made lowercase.
    bid_rate_category_id = models.CharField(db_column='BID_RATE_CATEGORY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'SERVICE'


class ShopResource(TruncatedModel):  # Field name made lowercase.
    id = models.CharField(db_column='ID', primary_key=True, max_length=15)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=40, blank=True, null=True)  # Field name made lowercase.
    schedule_normally = models.CharField(db_column='SCHEDULE_NORMALLY', max_length=1, default="N")  # Field name made lowercase.
    auto_reporting = models.CharField(db_column='AUTO_REPORTING', max_length=1, default="N")  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1, default="W")  # Field name made lowercase.
    exclusivity = models.CharField(db_column='EXCLUSIVITY', max_length=1, default="X")  # Field name made lowercase.
    shift_1_capacity = models.SmallIntegerField(db_column='SHIFT_1_CAPACITY', default=0)  # Field name made lowercase.
    shift_2_capacity = models.SmallIntegerField(db_column='SHIFT_2_CAPACITY', default=0)  # Field name made lowercase.
    shift_3_capacity = models.SmallIntegerField(db_column='SHIFT_3_CAPACITY', default=0)  # Field name made lowercase.
    schedule_group_id = models.CharField(db_column='SCHEDULE_GROUP_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    status_rank = models.SmallIntegerField(db_column='STATUS_RANK', default=0)  # Field name made lowercase.
    gl_acct_id = models.CharField(db_column='GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    afc_gl_acct_id = models.CharField(db_column='AFC_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    afb_gl_acct_id = models.CharField(db_column='AFB_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    grid_row = models.SmallIntegerField(db_column='GRID_ROW', blank=True, null=True)  # Field name made lowercase.
    grid_column = models.SmallIntegerField(db_column='GRID_COLUMN', blank=True, null=True)  # Field name made lowercase.
    schedule_type = models.SmallIntegerField(db_column='SCHEDULE_TYPE', blank=True, null=True)  # Field name made lowercase.
    min_segment_size = models.DecimalField(db_column='MIN_SEGMENT_SIZE', max_digits=14, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    efficiency_factor = models.DecimalField(db_column='EFFICIENCY_FACTOR', max_digits=14, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    service_buffer = models.IntegerField(db_column='SERVICE_BUFFER', blank=True, null=True)  # Field name made lowercase.
    monitor_load = models.CharField(db_column='MONITOR_LOAD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    wbs_resource_type = models.CharField(db_column='WBS_RESOURCE_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cost_category_id = models.CharField(db_column='COST_CATEGORY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    department_id = models.CharField(db_column='DEPARTMENT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    user_1 = models.CharField(db_column='USER_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_2 = models.CharField(db_column='USER_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_3 = models.CharField(db_column='USER_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_4 = models.CharField(db_column='USER_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_5 = models.CharField(db_column='USER_5', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_6 = models.CharField(db_column='USER_6', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_7 = models.CharField(db_column='USER_7', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_8 = models.CharField(db_column='USER_8', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_9 = models.CharField(db_column='USER_9', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_10 = models.CharField(db_column='USER_10', max_length=80, blank=True, null=True)  # Field name made lowercase.
    udf_layout_id = models.CharField(db_column='UDF_LAYOUT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    bid_rate_category_id = models.CharField(db_column='BID_RATE_CATEGORY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'SHOP_RESOURCE'


class ShopResourceSite(TruncatedModel):  # Field name made lowercase.
    site_id = models.CharField(db_column='SITE_ID', primary_key=True, max_length=15)  # Field name made lowercase.
    resource = models.ForeignKey(ShopResource, models.DO_NOTHING, db_column='RESOURCE_ID')  # Field name made lowercase.
    schedule_normally = models.CharField(db_column='SCHEDULE_NORMALLY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    auto_reporting = models.CharField(db_column='AUTO_REPORTING', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shift_1_capacity = models.SmallIntegerField(db_column='SHIFT_1_CAPACITY', blank=True, null=True)  # Field name made lowercase.
    shift_2_capacity = models.SmallIntegerField(db_column='SHIFT_2_CAPACITY', blank=True, null=True)  # Field name made lowercase.
    shift_3_capacity = models.SmallIntegerField(db_column='SHIFT_3_CAPACITY', blank=True, null=True)  # Field name made lowercase.
    setup_cost_per_hr = models.DecimalField(db_column='SETUP_COST_PER_HR', max_digits=22, decimal_places=8)  # Field name made lowercase.
    run_cost_per_hr = models.DecimalField(db_column='RUN_COST_PER_HR', max_digits=22, decimal_places=8)  # Field name made lowercase.
    service_buffer = models.IntegerField(db_column='SERVICE_BUFFER', blank=True, null=True)  # Field name made lowercase.
    bur_per_hr_setup = models.DecimalField(db_column='BUR_PER_HR_SETUP', max_digits=22, decimal_places=8)  # Field name made lowercase.
    bur_per_hr_run = models.DecimalField(db_column='BUR_PER_HR_RUN', max_digits=22, decimal_places=8)  # Field name made lowercase.
    run_cost_per_unit = models.DecimalField(db_column='RUN_COST_PER_UNIT', max_digits=22, decimal_places=8)  # Field name made lowercase.
    bur_percent_setup = models.DecimalField(db_column='BUR_PERCENT_SETUP', max_digits=6, decimal_places=3)  # Field name made lowercase.
    bur_percent_run = models.DecimalField(db_column='BUR_PERCENT_RUN', max_digits=6, decimal_places=3)  # Field name made lowercase.
    bur_per_operation = models.DecimalField(db_column='BUR_PER_OPERATION', max_digits=23, decimal_places=8)  # Field name made lowercase.
    gl_acct_id = models.CharField(db_column='GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    afc_gl_acct_id = models.CharField(db_column='AFC_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    afb_gl_acct_id = models.CharField(db_column='AFB_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    schedule_type = models.SmallIntegerField(db_column='SCHEDULE_TYPE', blank=True, null=True)  # Field name made lowercase.
    min_segment_size = models.DecimalField(db_column='MIN_SEGMENT_SIZE', max_digits=14, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    efficiency_factor = models.DecimalField(db_column='EFFICIENCY_FACTOR', max_digits=14, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    bur_per_unit_run = models.DecimalField(db_column='BUR_PER_UNIT_RUN', max_digits=22, decimal_places=8)  # Field name made lowercase.
    monitor_load = models.CharField(db_column='MONITOR_LOAD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cost_category_id = models.CharField(db_column='COST_CATEGORY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    department_id = models.CharField(db_column='DEPARTMENT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf_layout_id = models.CharField(db_column='UDF_LAYOUT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    user_1 = models.CharField(db_column='USER_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_2 = models.CharField(db_column='USER_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_3 = models.CharField(db_column='USER_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_4 = models.CharField(db_column='USER_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_5 = models.CharField(db_column='USER_5', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_6 = models.CharField(db_column='USER_6', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_7 = models.CharField(db_column='USER_7', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_8 = models.CharField(db_column='USER_8', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_9 = models.CharField(db_column='USER_9', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_10 = models.CharField(db_column='USER_10', max_length=80, blank=True, null=True)  # Field name made lowercase.
    bid_rate_category_id = models.CharField(db_column='BID_RATE_CATEGORY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'SHOP_RESOURCE_SITE'
        unique_together = (('site_id', 'resource'),)


class Trace(TruncatedModel):  # Field name made lowercase.
    part = models.ForeignKey(Part, models.DO_NOTHING, db_column='PART_ID', primary_key=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', max_length=30)  # Field name made lowercase.
    numbering_id = models.CharField(db_column='NUMBERING_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    out_qty = models.DecimalField(db_column='OUT_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    in_qty = models.DecimalField(db_column='IN_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    reported_qty = models.DecimalField(db_column='REPORTED_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    assigned_qty = models.DecimalField(db_column='ASSIGNED_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    aproperty_1 = models.CharField(db_column='APROPERTY_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    aproperty_2 = models.CharField(db_column='APROPERTY_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    aproperty_3 = models.CharField(db_column='APROPERTY_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    aproperty_4 = models.CharField(db_column='APROPERTY_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    aproperty_5 = models.CharField(db_column='APROPERTY_5', max_length=80, blank=True, null=True)  # Field name made lowercase.
    nproperty_1 = models.DecimalField(db_column='NPROPERTY_1', max_digits=15, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    nproperty_2 = models.DecimalField(db_column='NPROPERTY_2', max_digits=15, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    nproperty_3 = models.DecimalField(db_column='NPROPERTY_3', max_digits=15, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    nproperty_4 = models.DecimalField(db_column='NPROPERTY_4', max_digits=15, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    nproperty_5 = models.DecimalField(db_column='NPROPERTY_5', max_digits=15, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=250, blank=True, null=True)  # Field name made lowercase.
    expiration_date = models.DateTimeField(db_column='EXPIRATION_DATE', blank=True, null=True)  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='CREATE_DATE')  # Field name made lowercase.
    disp_in_qty = models.DecimalField(db_column='DISP_IN_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    disp_out_qty = models.DecimalField(db_column='DISP_OUT_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    unavailable_qty = models.DecimalField(db_column='UNAVAILABLE_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    owner_id = models.CharField(db_column='OWNER_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    lot_id = models.CharField(db_column='LOT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    serial_id = models.CharField(db_column='SERIAL_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    committed_qty = models.DecimalField(db_column='COMMITTED_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    production_date = models.DateTimeField(db_column='PRODUCTION_DATE', blank=True, null=True)  # Field name made lowercase.
    receive_by_date = models.DateTimeField(db_column='RECEIVE_BY_DATE', blank=True, null=True)  # Field name made lowercase.
    available_date = models.DateTimeField(db_column='AVAILABLE_DATE', blank=True, null=True)  # Field name made lowercase.
    ship_by_date = models.DateTimeField(db_column='SHIP_BY_DATE', blank=True, null=True)  # Field name made lowercase.
    site_id = models.CharField(db_column='SITE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'TRACE'
        unique_together = (('part', 'id'), ('numbering_id', 'id'),)


class TraceNumbering(TruncatedModel):  # Field name made lowercase.
    id = models.CharField(db_column='ID', primary_key=True, max_length=30)  # Field name made lowercase.
    next_number = models.DecimalField(db_column='NEXT_NUMBER', max_digits=15, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    alpha_prefix = models.CharField(db_column='ALPHA_PREFIX', max_length=4, blank=True, null=True)  # Field name made lowercase.
    alpha_suffix = models.CharField(db_column='ALPHA_SUFFIX', max_length=4, blank=True, null=True)  # Field name made lowercase.
    decimal_places = models.SmallIntegerField(db_column='DECIMAL_PLACES', blank=True, null=True)  # Field name made lowercase.
    leading_zeros = models.CharField(db_column='LEADING_ZEROS', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'TRACE_NUMBERING'


class TraceProfile(TruncatedModel):  # Field name made lowercase.
    part_id = models.CharField(db_column='PART_ID', primary_key=True, max_length=30)  # Field name made lowercase.
    numbering = models.ForeignKey(TraceNumbering, models.DO_NOTHING, db_column='NUMBERING_ID', blank=True, null=True)  # Field name made lowercase.
    apply_to_rec = models.CharField(db_column='APPLY_TO_REC', max_length=1)  # Field name made lowercase.
    apply_to_issue = models.CharField(db_column='APPLY_TO_ISSUE', max_length=1)  # Field name made lowercase.
    apply_to_adj = models.CharField(db_column='APPLY_TO_ADJ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    apply_to_labor = models.CharField(db_column='APPLY_TO_LABOR', max_length=1)  # Field name made lowercase.
    pre_assign = models.CharField(db_column='PRE_ASSIGN', max_length=1)  # Field name made lowercase.
    assign_method = models.CharField(db_column='ASSIGN_METHOD', max_length=1)  # Field name made lowercase.
    trace_id_label = models.CharField(db_column='TRACE_ID_LABEL', max_length=30, blank=True, null=True)  # Field name made lowercase.
    aproperty_label_1 = models.CharField(db_column='APROPERTY_LABEL_1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    aproperty_label_2 = models.CharField(db_column='APROPERTY_LABEL_2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    aproperty_label_3 = models.CharField(db_column='APROPERTY_LABEL_3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    aproperty_label_4 = models.CharField(db_column='APROPERTY_LABEL_4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    aproperty_label_5 = models.CharField(db_column='APROPERTY_LABEL_5', max_length=30, blank=True, null=True)  # Field name made lowercase.
    aproperty_1_reqd = models.CharField(db_column='APROPERTY_1_REQD', max_length=1)  # Field name made lowercase.
    aproperty_2_reqd = models.CharField(db_column='APROPERTY_2_REQD', max_length=1)  # Field name made lowercase.
    aproperty_3_reqd = models.CharField(db_column='APROPERTY_3_REQD', max_length=1)  # Field name made lowercase.
    aproperty_4_reqd = models.CharField(db_column='APROPERTY_4_REQD', max_length=1)  # Field name made lowercase.
    aproperty_5_reqd = models.CharField(db_column='APROPERTY_5_REQD', max_length=1)  # Field name made lowercase.
    nproperty_label_1 = models.CharField(db_column='NPROPERTY_LABEL_1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    nproperty_label_2 = models.CharField(db_column='NPROPERTY_LABEL_2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    nproperty_label_3 = models.CharField(db_column='NPROPERTY_LABEL_3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    nproperty_label_4 = models.CharField(db_column='NPROPERTY_LABEL_4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    nproperty_label_5 = models.CharField(db_column='NPROPERTY_LABEL_5', max_length=30, blank=True, null=True)  # Field name made lowercase.
    nproperty_1_reqd = models.CharField(db_column='NPROPERTY_1_REQD', max_length=1)  # Field name made lowercase.
    nproperty_2_reqd = models.CharField(db_column='NPROPERTY_2_REQD', max_length=1)  # Field name made lowercase.
    nproperty_3_reqd = models.CharField(db_column='NPROPERTY_3_REQD', max_length=1)  # Field name made lowercase.
    nproperty_4_reqd = models.CharField(db_column='NPROPERTY_4_REQD', max_length=1)  # Field name made lowercase.
    nproperty_5_reqd = models.CharField(db_column='NPROPERTY_5_REQD', max_length=1)  # Field name made lowercase.
    max_lot_qty = models.DecimalField(db_column='MAX_LOT_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    shelf_life = models.SmallIntegerField(db_column='SHELF_LIFE', blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=250, blank=True, null=True)  # Field name made lowercase.
    def_lbl_format_id = models.CharField(db_column='DEF_LBL_FORMAT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    aproperty_1_edit = models.CharField(db_column='APROPERTY_1_EDIT', max_length=1)  # Field name made lowercase.
    aproperty_2_edit = models.CharField(db_column='APROPERTY_2_EDIT', max_length=1)  # Field name made lowercase.
    aproperty_3_edit = models.CharField(db_column='APROPERTY_3_EDIT', max_length=1)  # Field name made lowercase.
    aproperty_4_edit = models.CharField(db_column='APROPERTY_4_EDIT', max_length=1)  # Field name made lowercase.
    aproperty_5_edit = models.CharField(db_column='APROPERTY_5_EDIT', max_length=1)  # Field name made lowercase.
    nproperty_1_edit = models.CharField(db_column='NPROPERTY_1_EDIT', max_length=1)  # Field name made lowercase.
    nproperty_2_edit = models.CharField(db_column='NPROPERTY_2_EDIT', max_length=1)  # Field name made lowercase.
    nproperty_3_edit = models.CharField(db_column='NPROPERTY_3_EDIT', max_length=1)  # Field name made lowercase.
    nproperty_4_edit = models.CharField(db_column='NPROPERTY_4_EDIT', max_length=1)  # Field name made lowercase.
    nproperty_5_edit = models.CharField(db_column='NPROPERTY_5_EDIT', max_length=1)  # Field name made lowercase.
    aproperty_1_vis = models.CharField(db_column='APROPERTY_1_VIS', max_length=1)  # Field name made lowercase.
    aproperty_2_vis = models.CharField(db_column='APROPERTY_2_VIS', max_length=1)  # Field name made lowercase.
    aproperty_3_vis = models.CharField(db_column='APROPERTY_3_VIS', max_length=1)  # Field name made lowercase.
    aproperty_4_vis = models.CharField(db_column='APROPERTY_4_VIS', max_length=1)  # Field name made lowercase.
    aproperty_5_vis = models.CharField(db_column='APROPERTY_5_VIS', max_length=1)  # Field name made lowercase.
    nproperty_1_vis = models.CharField(db_column='NPROPERTY_1_VIS', max_length=1)  # Field name made lowercase.
    nproperty_2_vis = models.CharField(db_column='NPROPERTY_2_VIS', max_length=1)  # Field name made lowercase.
    nproperty_3_vis = models.CharField(db_column='NPROPERTY_3_VIS', max_length=1)  # Field name made lowercase.
    nproperty_4_vis = models.CharField(db_column='NPROPERTY_4_VIS', max_length=1)  # Field name made lowercase.
    nproperty_5_vis = models.CharField(db_column='NPROPERTY_5_VIS', max_length=1)  # Field name made lowercase.
    edit_exp_date = models.CharField(db_column='EDIT_EXP_DATE', max_length=1)  # Field name made lowercase.
    auto_fill_trace = models.CharField(db_column='AUTO_FILL_TRACE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    apply_to_servdisp = models.CharField(db_column='APPLY_TO_SERVDISP', max_length=1)  # Field name made lowercase.
    apply_to_servrec = models.CharField(db_column='APPLY_TO_SERVREC', max_length=1)  # Field name made lowercase.
    ownership = models.CharField(db_column='OWNERSHIP', max_length=1)  # Field name made lowercase.
    lot = models.CharField(db_column='LOT', max_length=1)  # Field name made lowercase.
    serial = models.CharField(db_column='SERIAL', max_length=1)  # Field name made lowercase.
    colocate_owners = models.CharField(db_column='COLOCATE_OWNERS', max_length=1)  # Field name made lowercase.
    colocate_lots = models.CharField(db_column='COLOCATE_LOTS', max_length=1)  # Field name made lowercase.
    expiration = models.CharField(db_column='EXPIRATION', max_length=1)  # Field name made lowercase.
    colocate_alphas = models.CharField(db_column='COLOCATE_ALPHAS', max_length=1)  # Field name made lowercase.
    colocate_numerics = models.CharField(db_column='COLOCATE_NUMERICS', max_length=1)  # Field name made lowercase.
    accept_expired_rcv = models.CharField(db_column='ACCEPT_EXPIRED_RCV', max_length=1)  # Field name made lowercase.
    ownership_known = models.CharField(db_column='OWNERSHIP_KNOWN', max_length=1)  # Field name made lowercase.
    lot_known = models.CharField(db_column='LOT_KNOWN', max_length=1)  # Field name made lowercase.
    serial_known = models.CharField(db_column='SERIAL_KNOWN', max_length=1)  # Field name made lowercase.
    expiration_known = models.CharField(db_column='EXPIRATION_KNOWN', max_length=1)  # Field name made lowercase.
    aproperty_1_known = models.CharField(db_column='APROPERTY_1_KNOWN', max_length=1)  # Field name made lowercase.
    aproperty_2_known = models.CharField(db_column='APROPERTY_2_KNOWN', max_length=1)  # Field name made lowercase.
    aproperty_3_known = models.CharField(db_column='APROPERTY_3_KNOWN', max_length=1)  # Field name made lowercase.
    aproperty_4_known = models.CharField(db_column='APROPERTY_4_KNOWN', max_length=1)  # Field name made lowercase.
    aproperty_5_known = models.CharField(db_column='APROPERTY_5_KNOWN', max_length=1)  # Field name made lowercase.
    nproperty_1_known = models.CharField(db_column='NPROPERTY_1_KNOWN', max_length=1)  # Field name made lowercase.
    nproperty_2_known = models.CharField(db_column='NPROPERTY_2_KNOWN', max_length=1)  # Field name made lowercase.
    nproperty_3_known = models.CharField(db_column='NPROPERTY_3_KNOWN', max_length=1)  # Field name made lowercase.
    nproperty_4_known = models.CharField(db_column='NPROPERTY_4_KNOWN', max_length=1)  # Field name made lowercase.
    nproperty_5_known = models.CharField(db_column='NPROPERTY_5_KNOWN', max_length=1)  # Field name made lowercase.
    count_detail = models.CharField(db_column='COUNT_DETAIL', max_length=1)  # Field name made lowercase.
    production = models.CharField(db_column='PRODUCTION', max_length=1)  # Field name made lowercase.
    production_known = models.CharField(db_column='PRODUCTION_KNOWN', max_length=1)  # Field name made lowercase.
    colocate_prod = models.CharField(db_column='COLOCATE_PROD', max_length=1)  # Field name made lowercase.
    receive_by = models.CharField(db_column='RECEIVE_BY', max_length=1)  # Field name made lowercase.
    receive_by_known = models.CharField(db_column='RECEIVE_BY_KNOWN', max_length=1)  # Field name made lowercase.
    colocate_rec_by = models.CharField(db_column='COLOCATE_REC_BY', max_length=1)  # Field name made lowercase.
    available = models.CharField(db_column='AVAILABLE', max_length=1)  # Field name made lowercase.
    available_known = models.CharField(db_column='AVAILABLE_KNOWN', max_length=1)  # Field name made lowercase.
    colocate_available = models.CharField(db_column='COLOCATE_AVAILABLE', max_length=1)  # Field name made lowercase.
    ship_by = models.CharField(db_column='SHIP_BY', max_length=1)  # Field name made lowercase.
    ship_by_known = models.CharField(db_column='SHIP_BY_KNOWN', max_length=1)  # Field name made lowercase.
    colocate_ship_by = models.CharField(db_column='COLOCATE_SHIP_BY', max_length=1)  # Field name made lowercase.
    site_id = models.CharField(db_column='SITE_ID', max_length=15)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'TRACE_PROFILE'
        unique_together = (('site_id', 'part_id'),)


class Vendor(TruncatedModel):
    id = models.CharField(db_column='ID', primary_key=True, max_length=15)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_1 = models.CharField(db_column='ADDR_1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_2 = models.CharField(db_column='ADDR_2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_3 = models.CharField(db_column='ADDR_3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='CITY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='STATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(db_column='ZIPCODE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='COUNTRY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    vendor_country_id = models.CharField(db_column='VENDOR_COUNTRY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    contact_first_name = models.CharField(db_column='CONTACT_FIRST_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact_last_name = models.CharField(db_column='CONTACT_LAST_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact_initial = models.CharField(db_column='CONTACT_INITIAL', max_length=2, blank=True, null=True)  # Field name made lowercase.
    contact_position = models.CharField(db_column='CONTACT_POSITION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    contact_honorific = models.CharField(db_column='CONTACT_HONORIFIC', max_length=15, blank=True, null=True)  # Field name made lowercase.
    contact_salutation = models.CharField(db_column='CONTACT_SALUTATION', max_length=60, blank=True, null=True)  # Field name made lowercase.
    contact_phone = models.CharField(db_column='CONTACT_PHONE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contact_fax = models.CharField(db_column='CONTACT_FAX', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remit_to_name = models.CharField(db_column='REMIT_TO_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    remit_to_addr_1 = models.CharField(db_column='REMIT_TO_ADDR_1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    remit_to_addr_2 = models.CharField(db_column='REMIT_TO_ADDR_2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    remit_to_addr_3 = models.CharField(db_column='REMIT_TO_ADDR_3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    remit_to_city = models.CharField(db_column='REMIT_TO_CITY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    remit_to_state = models.CharField(db_column='REMIT_TO_STATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    remit_to_zipcode = models.CharField(db_column='REMIT_TO_ZIPCODE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    remit_to_country = models.CharField(db_column='REMIT_TO_COUNTRY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    remit_to_country_id = models.CharField(db_column='REMIT_TO_COUNTRY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    free_on_board = models.CharField(db_column='FREE_ON_BOARD', max_length=25, blank=True, null=True)  # Field name made lowercase.
    ship_via = models.CharField(db_column='SHIP_VIA', max_length=40, blank=True, null=True)  # Field name made lowercase.
    buyer = models.CharField(db_column='BUYER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    report_1099_misc = models.CharField(db_column='REPORT_1099_MISC', max_length=1)  # Field name made lowercase.
    terms_net_type = models.CharField(db_column='TERMS_NET_TYPE', max_length=1)  # Field name made lowercase.
    terms_net_days = models.SmallIntegerField(db_column='TERMS_NET_DAYS', blank=True, null=True)  # Field name made lowercase.
    terms_net_date = models.DateTimeField(db_column='TERMS_NET_DATE', blank=True, null=True)  # Field name made lowercase.
    terms_disc_type = models.CharField(db_column='TERMS_DISC_TYPE', max_length=1)  # Field name made lowercase.
    terms_disc_days = models.SmallIntegerField(db_column='TERMS_DISC_DAYS', blank=True, null=True)  # Field name made lowercase.
    terms_disc_date = models.DateTimeField(db_column='TERMS_DISC_DATE', blank=True, null=True)  # Field name made lowercase.
    terms_disc_percent = models.DecimalField(db_column='TERMS_DISC_PERCENT', max_digits=5, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    terms_description = models.CharField(db_column='TERMS_DESCRIPTION', max_length=80, blank=True, null=True)  # Field name made lowercase.
    # currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='CURRENCY_ID')  # Field name made lowercase.
    tax_id_number = models.CharField(db_column='TAX_ID_NUMBER', max_length=25, blank=True, null=True)  # Field name made lowercase.
    site_id = models.CharField(db_column='SITE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    # def_exp_gl_acct = models.ForeignKey(Account, models.DO_NOTHING, db_column='DEF_EXP_GL_ACCT_ID', blank=True, null=True)  # Field name made lowercase.
    def_sls_tax_grp_id = models.CharField(db_column='DEF_SLS_TAX_GRP_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    match_type = models.CharField(db_column='MATCH_TYPE', max_length=1)  # Field name made lowercase.
    match_high_pct = models.DecimalField(db_column='MATCH_HIGH_PCT', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    match_low_pct = models.DecimalField(db_column='MATCH_LOW_PCT', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    last_order_date = models.DateTimeField(db_column='LAST_ORDER_DATE', blank=True, null=True)  # Field name made lowercase.
    open_date = models.DateTimeField(db_column='OPEN_DATE', blank=True, null=True)  # Field name made lowercase.
    modify_date = models.DateTimeField(db_column='MODIFY_DATE', blank=True, null=True)  # Field name made lowercase.
    user_1 = models.CharField(db_column='USER_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_2 = models.CharField(db_column='USER_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_3 = models.CharField(db_column='USER_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_4 = models.CharField(db_column='USER_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_5 = models.CharField(db_column='USER_5', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_6 = models.CharField(db_column='USER_6', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_7 = models.CharField(db_column='USER_7', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_8 = models.CharField(db_column='USER_8', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_9 = models.CharField(db_column='USER_9', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_10 = models.CharField(db_column='USER_10', max_length=80, blank=True, null=True)  # Field name made lowercase.
    def_payb_acct_id = models.CharField(db_column='DEF_PAYB_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf_layout_id = models.CharField(db_column='UDF_LAYOUT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    # arrival_code = models.ForeignKey(PortOfArrival, models.DO_NOTHING, db_column='ARRIVAL_CODE', blank=True, null=True)  # Field name made lowercase.
    # trans_code = models.ForeignKey(PortOfTrans, models.DO_NOTHING, db_column='TRANS_CODE', blank=True, null=True)  # Field name made lowercase.
    # country_0 = models.ForeignKey(Country, models.DO_NOTHING, db_column='COUNTRY_ID', blank=True, null=True)  # Field name made lowercase. Field renamed because of name conflict.
    # nature_of_trans = models.ForeignKey(NatureOfTrans, models.DO_NOTHING, db_column='NATURE_OF_TRANS', blank=True, null=True)  # Field name made lowercase.
    # mode_of_transport = models.ForeignKey(ModeOfTransport, models.DO_NOTHING, db_column='MODE_OF_TRANSPORT', blank=True, null=True)  # Field name made lowercase.
    siret_number = models.DecimalField(db_column='SIRET_NUMBER', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    vat_registration = models.CharField(db_column='VAT_REGISTRATION', max_length=25, blank=True, null=True)  # Field name made lowercase.
    vat_book_code_i = models.CharField(db_column='VAT_BOOK_CODE_I', max_length=5, blank=True, null=True)  # Field name made lowercase.
    vat_book_code_m = models.CharField(db_column='VAT_BOOK_CODE_M', max_length=5, blank=True, null=True)  # Field name made lowercase.
    vat_exempt = models.CharField(db_column='VAT_EXEMPT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    # withholding_code = models.ForeignKey('Withholding', models.DO_NOTHING, db_column='WITHHOLDING_CODE', blank=True, null=True)  # Field name made lowercase.
    vend_bank_acct_id = models.CharField(db_column='VEND_BANK_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    payee_ref_code = models.CharField(db_column='PAYEE_REF_CODE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    payment_method = models.CharField(db_column='PAYMENT_METHOD', max_length=1)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    social_security_no = models.CharField(db_column='SOCIAL_SECURITY_NO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_of_birth = models.DateTimeField(db_column='DATE_OF_BIRTH', blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(db_column='SEX', max_length=1, blank=True, null=True)  # Field name made lowercase.
    place_of_birth = models.CharField(db_column='PLACE_OF_BIRTH', max_length=30, blank=True, null=True)  # Field name made lowercase.
    state_of_birth = models.CharField(db_column='STATE_OF_BIRTH', max_length=10, blank=True, null=True)  # Field name made lowercase.
    priority = models.SmallIntegerField(db_column='PRIORITY', blank=True, null=True)  # Field name made lowercase.
    def_exp_acct_id = models.CharField(db_column='DEF_EXP_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    qa_percentage = models.DecimalField(db_column='QA_PERCENTAGE', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    pref_order_medium = models.CharField(db_column='PREF_ORDER_MEDIUM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    def_carrier_id = models.CharField(db_column='DEF_CARRIER_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    contact_mobile = models.CharField(db_column='CONTACT_MOBILE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contact_email = models.CharField(db_column='CONTACT_EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # def_trans_currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='DEF_TRANS_CURRENCY', blank=True, null=True)  # Field name made lowercase.
    # def_lbl_format = models.ForeignKey(LabelFormat, models.DO_NOTHING, db_column='DEF_LBL_FORMAT_ID', blank=True, null=True)  # Field name made lowercase.
    vat_discounted = models.CharField(db_column='VAT_DISCOUNTED', max_length=1)  # Field name made lowercase.
    vat_always_disc = models.CharField(db_column='VAT_ALWAYS_DISC', max_length=1)  # Field name made lowercase.
    vat_code = models.CharField(db_column='VAT_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vat_override_seq = models.CharField(db_column='VAT_OVERRIDE_SEQ', max_length=1)  # Field name made lowercase.
    # return_trans = models.ForeignKey(NatureOfTrans, models.DO_NOTHING, db_column='RETURN_TRANS', blank=True, null=True)  # Field name made lowercase.
    web_url = models.CharField(db_column='WEB_URL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    shipto_id = models.CharField(db_column='SHIPTO_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dispatch_addr_id = models.CharField(db_column='DISPATCH_ADDR_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    disp_pallet_req = models.CharField(db_column='DISP_PALLET_REQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    active_flag = models.CharField(db_column='ACTIVE_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    status_eff_date = models.DateTimeField(db_column='STATUS_EFF_DATE')  # Field name made lowercase.
    # def_terms = models.ForeignKey(Terms, models.DO_NOTHING, db_column='DEF_TERMS_ID', blank=True, null=True)  # Field name made lowercase.
    # vendor_group = models.ForeignKey('VendorGroup', models.DO_NOTHING, db_column='VENDOR_GROUP_ID', blank=True, null=True)  # Field name made lowercase.
    internal_vendor = models.CharField(db_column='INTERNAL_VENDOR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prevent_edit_po_receipt = models.CharField(db_column='PREVENT_EDIT_PO_RECEIPT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    contact_phone_ext = models.CharField(db_column='CONTACT_PHONE_EXT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    email_vend_on_new_order = models.CharField(db_column='EMAIL_VEND_ON_NEW_ORDER', max_length=1)  # Field name made lowercase.
    email_vend_on_chg_order = models.CharField(db_column='EMAIL_VEND_ON_CHG_ORDER', max_length=1)  # Field name made lowercase.
    email_vend_on_po_receipt = models.CharField(db_column='EMAIL_VEND_ON_PO_RECEIPT', max_length=1)  # Field name made lowercase.
    email_empl_on_new_order = models.CharField(db_column='EMAIL_EMPL_ON_NEW_ORDER', max_length=1)  # Field name made lowercase.
    email_empl_on_chg_order = models.CharField(db_column='EMAIL_EMPL_ON_CHG_ORDER', max_length=1)  # Field name made lowercase.
    email_empl_on_po_receipt = models.CharField(db_column='EMAIL_EMPL_ON_PO_RECEIPT', max_length=1)  # Field name made lowercase.
    email_empl_on_inv_paid = models.CharField(db_column='EMAIL_EMPL_ON_INV_PAID', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'VENDOR'


class WorkorderBinary(TruncatedModel):  # Field name made lowercase.
    workorder_type = models.CharField(db_column='WORKORDER_TYPE', max_length=1)  # Field name made lowercase.
    workorder_base = models.CharField(db_column='WORKORDER_BASE_ID', max_length=30)  # Field name made lowercase.
    workorder_lot = models.CharField(db_column='WORKORDER_LOT_ID', max_length=3)  # Field name made lowercase.
    workorder_split = models.CharField(db_column='WORKORDER_SPLIT_ID', max_length=3)  # Field name made lowercase.
    workorder_sub = models.CharField(db_column='WORKORDER_SUB_ID', max_length=3)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1)  # Field name made lowercase.
    bits = models.BinaryField(db_column='BITS', blank=True, null=True)  # Field name made lowercase.
    bits_length = models.IntegerField(db_column='BITS_LENGTH')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'WORKORDER_BINARY'
        unique_together = (('workorder_type', 'workorder_base', 'workorder_lot', 'workorder_split', 'workorder_sub', 'type'),)


class CustGroup(TruncatedModel):  # Field name made lowercase.
    rowid = models.AutoField(primary_key=True, db_column='ROWID')  # Field name made lowercase.
    id = models.CharField(db_column='ID', max_length=6)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CUSTOMER_GROUP'


class CustGroupRelation(TruncatedModel):  # Field name made lowercase.
    rowid = models.AutoField(primary_key=True, db_column='ROWID')  # Field name made lowercase.
    group_id = models.CharField(db_column='GROUP_ID', max_length=6)  # Field name made lowercase.
    customer_id = models.CharField(db_column='CUSTOMER_ID', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CUST_GROUP_RELATION'


class WorkOrder(TruncatedModel):  # Field name made lowercase.
    rowid = models.AutoField(primary_key=True, db_column='ROWID')  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1)  # Field name made lowercase.
    base_id = models.CharField(db_column='BASE_ID', max_length=30)  # Field name made lowercase.
    lot_id = models.CharField(db_column='LOT_ID', max_length=3)  # Field name made lowercase.
    split_id = models.CharField(db_column='SPLIT_ID', max_length=3)  # Field name made lowercase.
    sub_id = models.CharField(db_column='SUB_ID', max_length=3)  # Field name made lowercase.
    part = models.ForeignKey(Part, models.DO_NOTHING, db_column='PART_ID', blank=True, null=True)  # Field name made lowercase.
    global_rank = models.SmallIntegerField(db_column='GLOBAL_RANK', blank=True, null=True)  # Field name made lowercase.
    desired_qty = models.DecimalField(db_column='DESIRED_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    received_qty = models.DecimalField(db_column='RECEIVED_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='CREATE_DATE')  # Field name made lowercase.
    desired_rls_date = models.DateTimeField(db_column='DESIRED_RLS_DATE', blank=True, null=True)  # Field name made lowercase.
    desired_want_date = models.DateTimeField(db_column='DESIRED_WANT_DATE', blank=True, null=True)  # Field name made lowercase.
    close_date = models.DateTimeField(db_column='CLOSE_DATE', blank=True, null=True)  # Field name made lowercase.
    costed_date = models.DateTimeField(db_column='COSTED_DATE', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1)  # Field name made lowercase.
    copy_from_split_id = models.CharField(db_column='COPY_FROM_SPLIT_ID', max_length=3, blank=True, null=True)  # Field name made lowercase.
    engineered_by = models.CharField(db_column='ENGINEERED_BY', max_length=40, blank=True, null=True)  # Field name made lowercase.
    engineered_date = models.DateTimeField(db_column='ENGINEERED_DATE', blank=True, null=True)  # Field name made lowercase.
    drawing_id = models.CharField(db_column='DRAWING_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    drawing_rev_no = models.CharField(db_column='DRAWING_REV_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    product_code = models.CharField(db_column='PRODUCT_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    commodity_code = models.CharField(db_column='COMMODITY_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    forward_schedule = models.CharField(db_column='FORWARD_SCHEDULE', max_length=1)  # Field name made lowercase.
    posting_candidate = models.CharField(db_column='POSTING_CANDIDATE', max_length=1)  # Field name made lowercase.
    mat_gl_acct_id = models.CharField(db_column='MAT_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lab_gl_acct_id = models.CharField(db_column='LAB_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    bur_gl_acct_id = models.CharField(db_column='BUR_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ser_gl_acct_id = models.CharField(db_column='SER_GL_ACCT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    variable_table = models.CharField(db_column='VARIABLE_TABLE', max_length=250, blank=True, null=True)  # Field name made lowercase.
    schedule_group_id = models.CharField(db_column='SCHEDULE_GROUP_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    sched_start_date = models.DateTimeField(db_column='SCHED_START_DATE', blank=True, null=True)  # Field name made lowercase.
    sched_finish_date = models.DateTimeField(db_column='SCHED_FINISH_DATE', blank=True, null=True)  # Field name made lowercase.
    could_finish_date = models.DateTimeField(db_column='COULD_FINISH_DATE', blank=True, null=True)  # Field name made lowercase.
    est_material_cost = models.DecimalField(db_column='EST_MATERIAL_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    est_labor_cost = models.DecimalField(db_column='EST_LABOR_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    est_burden_cost = models.DecimalField(db_column='EST_BURDEN_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    est_service_cost = models.DecimalField(db_column='EST_SERVICE_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    act_material_cost = models.DecimalField(db_column='ACT_MATERIAL_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    act_labor_cost = models.DecimalField(db_column='ACT_LABOR_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    act_burden_cost = models.DecimalField(db_column='ACT_BURDEN_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    act_service_cost = models.DecimalField(db_column='ACT_SERVICE_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    rem_material_cost = models.DecimalField(db_column='REM_MATERIAL_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    rem_labor_cost = models.DecimalField(db_column='REM_LABOR_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    rem_burden_cost = models.DecimalField(db_column='REM_BURDEN_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    rem_service_cost = models.DecimalField(db_column='REM_SERVICE_COST', max_digits=23, decimal_places=8, default=0)  # Field name made lowercase.
    marked_for_purge = models.CharField(db_column='MARKED_FOR_PURGE', max_length=1)  # Field name made lowercase.
    printed_date = models.DateTimeField(db_column='PRINTED_DATE', blank=True, null=True)  # Field name made lowercase.
    drawing_file = models.CharField(db_column='DRAWING_FILE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    warehouse_id = models.CharField(db_column='WAREHOUSE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    wip_vas_required = models.CharField(db_column='WIP_VAS_REQUIRED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    allocated_qty = models.DecimalField(db_column='ALLOCATED_QTY', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    fulfilled_qty = models.DecimalField(db_column='FULFILLED_QTY', max_digits=20, decimal_places=8, default=0)  # Field name made lowercase.
    def_lbl_format_id = models.CharField(db_column='DEF_LBL_FORMAT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hard_release_date = models.CharField(db_column='HARD_RELEASE_DATE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    user_1 = models.CharField(db_column='USER_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_2 = models.CharField(db_column='USER_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_3 = models.CharField(db_column='USER_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_4 = models.CharField(db_column='USER_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_5 = models.CharField(db_column='USER_5', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_6 = models.CharField(db_column='USER_6', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_7 = models.CharField(db_column='USER_7', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_8 = models.CharField(db_column='USER_8', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_9 = models.CharField(db_column='USER_9', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_10 = models.CharField(db_column='USER_10', max_length=80, blank=True, null=True)  # Field name made lowercase.
    udf_layout_id = models.CharField(db_column='UDF_LAYOUT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    dbr_type = models.CharField(db_column='DBR_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dbr_priority = models.CharField(db_column='DBR_PRIORITY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dbr_code = models.IntegerField(db_column='DBR_CODE', blank=True, null=True)  # Field name made lowercase.
    wbs_code = models.CharField(db_column='WBS_CODE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wbs_project = models.CharField(db_column='WBS_PROJECT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    wbs_cust_order_id = models.CharField(db_column='WBS_CUST_ORDER_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    milestone_seq_no = models.SmallIntegerField(db_column='MILESTONE_SEQ_NO', blank=True, null=True)  # Field name made lowercase.
    milestone_sub_id = models.CharField(db_column='MILESTONE_SUB_ID', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ecn_revision = models.CharField(db_column='ECN_REVISION', max_length=1, blank=True, null=True)  # Field name made lowercase.
    edi_blanket_flag = models.CharField(db_column='EDI_BLANKET_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dispatched = models.CharField(db_column='DISPATCHED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    orig_stage_revision_id = models.CharField(db_column='ORIG_STAGE_REVISION_ID', max_length=24, blank=True, null=True)  # Field name made lowercase.
    status_eff_date = models.DateTimeField(db_column='STATUS_EFF_DATE')  # Field name made lowercase.
    allow_alt_parts = models.CharField(db_column='ALLOW_ALT_PARTS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    allow_upd_from_mst = models.CharField(db_column='ALLOW_UPD_FROM_MST', max_length=1)  # Field name made lowercase.
    allow_upd_from_leg = models.CharField(db_column='ALLOW_UPD_FROM_LEG', max_length=1)  # Field name made lowercase.
    update_from_ref = models.CharField(db_column='UPDATE_FROM_REF', max_length=100, blank=True, null=True)  # Field name made lowercase.
    update_user_id = models.CharField(db_column='UPDATE_USER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    update_eng_master = models.CharField(db_column='UPDATE_ENG_MASTER', max_length=3, blank=True, null=True)  # Field name made lowercase.
    update_date = models.DateTimeField(db_column='UPDATE_DATE', blank=True, null=True)  # Field name made lowercase.
    site_id = models.CharField(db_column='SITE_ID', max_length=15)  # Field name made lowercase.
    prod_order_type = models.CharField(db_column='PROD_ORDER_TYPE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    planner_id = models.CharField(db_column='PLANNER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    inactive = models.CharField(db_column='INACTIVE', max_length=1)  # Field name made lowercase.
    entered_by = models.CharField(db_column='ENTERED_BY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    percent_compl = models.CharField(db_column='PERCENT_COMPL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty_compl_by_hrs = models.CharField(db_column='QTY_COMPL_BY_HRS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    max_qty_complete = models.DecimalField(db_column='MAX_QTY_COMPLETE', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    customer_priority = models.IntegerField(db_column='CUSTOMER_PRIORITY')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'WORK_ORDER'
        unique_together = (('type', 'base_id', 'lot_id', 'split_id', 'sub_id'), ('type', 'base_id', 'lot_id', 'split_id', 'sub_id', 'site_id'),)


class Currency(TruncatedModel):
    id = models.CharField(db_column='ID', primary_key=True, max_length=15)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=40, blank=True, null=True)  # Field name made lowercase.
    short_name = models.CharField(db_column='SHORT_NAME', max_length=10, blank=True, null=True)  # Field name made lowercase.
    country_profile = models.CharField(db_column='COUNTRY_PROFILE', max_length=40, blank=True, null=True)  # Field name made lowercase.
    i_currency = models.SmallIntegerField(db_column='I_CURRENCY', blank=True, null=True)  # Field name made lowercase.
    i_curr_digits = models.SmallIntegerField(db_column='I_CURR_DIGITS', blank=True, null=True)  # Field name made lowercase.
    i_neg_curr = models.SmallIntegerField(db_column='I_NEG_CURR', blank=True, null=True)  # Field name made lowercase.
    s_currency = models.CharField(db_column='S_CURRENCY', max_length=40, blank=True, null=True)  # Field name made lowercase.
    s_thousand = models.CharField(db_column='S_THOUSAND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    euro_participant = models.CharField(db_column='EURO_PARTICIPANT', max_length=1)  # Field name made lowercase.
    xchg_rate = models.DecimalField(db_column='XCHG_RATE', max_digits=15, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    iso_code = models.CharField(db_column='ISO_CODE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    reporting_currency = models.CharField(db_column='REPORTING_CURRENCY', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CURRENCY'


class CustomerDiscount(TruncatedModel):
    discount_code = models.CharField(db_column='DISCOUNT_CODE', primary_key=True, max_length=15)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=80, blank=True, null=True)  # Field name made lowercase.
    discount_percent = models.DecimalField(db_column='DISCOUNT_PERCENT', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CUSTOMER_DISCOUNT'


class CustPriceEffect(TruncatedModel):
    rowid = models.AutoField(primary_key=True, db_column='ROWID')  # Field name made lowercase.
    customer_id = models.CharField(db_column='CUSTOMER_ID', max_length=15)  # Field name made lowercase.
    part = models.ForeignKey('Part', models.DO_NOTHING, db_column='PART_ID')  # Field name made lowercase.
    selling_um = models.CharField(db_column='SELLING_UM', max_length=15)  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='CREATE_DATE')  # Field name made lowercase.
    effective_date = models.DateTimeField(db_column='EFFECTIVE_DATE', blank=True, null=True)  # Field name made lowercase.
    discontinue_date = models.DateTimeField(db_column='DISCONTINUE_DATE', blank=True, null=True)  # Field name made lowercase.
    customer_part_id = models.CharField(db_column='CUSTOMER_PART_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    qty_break_1 = models.DecimalField(db_column='QTY_BREAK_1', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_2 = models.DecimalField(db_column='QTY_BREAK_2', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_3 = models.DecimalField(db_column='QTY_BREAK_3', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_4 = models.DecimalField(db_column='QTY_BREAK_4', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_5 = models.DecimalField(db_column='QTY_BREAK_5', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_6 = models.DecimalField(db_column='QTY_BREAK_6', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_7 = models.DecimalField(db_column='QTY_BREAK_7', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_8 = models.DecimalField(db_column='QTY_BREAK_8', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_9 = models.DecimalField(db_column='QTY_BREAK_9', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_10 = models.DecimalField(db_column='QTY_BREAK_10', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_1 = models.DecimalField(db_column='UNIT_PRICE_1', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_2 = models.DecimalField(db_column='UNIT_PRICE_2', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_3 = models.DecimalField(db_column='UNIT_PRICE_3', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_4 = models.DecimalField(db_column='UNIT_PRICE_4', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_5 = models.DecimalField(db_column='UNIT_PRICE_5', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_6 = models.DecimalField(db_column='UNIT_PRICE_6', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_7 = models.DecimalField(db_column='UNIT_PRICE_7', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_8 = models.DecimalField(db_column='UNIT_PRICE_8', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_9 = models.DecimalField(db_column='UNIT_PRICE_9', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_10 = models.DecimalField(db_column='UNIT_PRICE_10', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    default_unit_price = models.DecimalField(db_column='DEFAULT_UNIT_PRICE', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    by_date_code = models.CharField(db_column='BY_DATE_CODE', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CUST_PRICE_EFFECT'
        unique_together = (('customer_id', 'part', 'selling_um', 'create_date'),)


class CustomerPrice(TruncatedModel):
    rowid = models.AutoField(primary_key=True, db_column='ROWID')  # Field name made lowercase.
    customer = models.OneToOneField(Customer, models.DO_NOTHING, db_column='CUSTOMER_ID')  # Field name made lowercase.
    part = models.ForeignKey('Part', models.DO_NOTHING, db_column='PART_ID')  # Field name made lowercase.
    selling_um = models.CharField(db_column='SELLING_UM', max_length=15)  # Field name made lowercase.
    customer_part_id = models.CharField(db_column='CUSTOMER_PART_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    qty_break_1 = models.DecimalField(db_column='QTY_BREAK_1', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_2 = models.DecimalField(db_column='QTY_BREAK_2', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_3 = models.DecimalField(db_column='QTY_BREAK_3', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_4 = models.DecimalField(db_column='QTY_BREAK_4', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_5 = models.DecimalField(db_column='QTY_BREAK_5', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_6 = models.DecimalField(db_column='QTY_BREAK_6', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_7 = models.DecimalField(db_column='QTY_BREAK_7', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_8 = models.DecimalField(db_column='QTY_BREAK_8', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_9 = models.DecimalField(db_column='QTY_BREAK_9', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_10 = models.DecimalField(db_column='QTY_BREAK_10', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_1 = models.DecimalField(db_column='UNIT_PRICE_1', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_2 = models.DecimalField(db_column='UNIT_PRICE_2', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_3 = models.DecimalField(db_column='UNIT_PRICE_3', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_4 = models.DecimalField(db_column='UNIT_PRICE_4', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_5 = models.DecimalField(db_column='UNIT_PRICE_5', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_6 = models.DecimalField(db_column='UNIT_PRICE_6', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_7 = models.DecimalField(db_column='UNIT_PRICE_7', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_8 = models.DecimalField(db_column='UNIT_PRICE_8', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_9 = models.DecimalField(db_column='UNIT_PRICE_9', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_10 = models.DecimalField(db_column='UNIT_PRICE_10', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    default_unit_price = models.DecimalField(db_column='DEFAULT_UNIT_PRICE', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CUSTOMER_PRICE'
        unique_together = (('customer', 'part', 'selling_um'),)


class Terms(TruncatedModel):
    id = models.CharField(db_column='ID', primary_key=True, max_length=15)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=80, blank=True, null=True)  # Field name made lowercase.
    net_type = models.CharField(db_column='NET_TYPE', max_length=1)  # Field name made lowercase.
    net_days = models.SmallIntegerField(db_column='NET_DAYS', blank=True, null=True)  # Field name made lowercase.
    net_date = models.DateTimeField(db_column='NET_DATE', blank=True, null=True)  # Field name made lowercase.
    disc_type = models.CharField(db_column='DISC_TYPE', max_length=1)  # Field name made lowercase.
    disc_days = models.SmallIntegerField(db_column='DISC_DAYS', blank=True, null=True)  # Field name made lowercase.
    disc_date = models.DateTimeField(db_column='DISC_DATE', blank=True, null=True)  # Field name made lowercase.
    disc_percent = models.DecimalField(db_column='DISC_PERCENT', max_digits=5, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    freight_terms = models.CharField(db_column='FREIGHT_TERMS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    end_of_month = models.CharField(db_column='END_OF_MONTH', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vat_on_first_inst = models.CharField(db_column='VAT_ON_FIRST_INST', max_length=1, blank=True, null=True)  # Field name made lowercase.
    period_type = models.CharField(db_column='PERIOD_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    disc_basis = models.CharField(db_column='DISC_BASIS', max_length=32, blank=True, null=True)  # Field name made lowercase.
    active_flag = models.CharField(db_column='ACTIVE_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'TERMS'


class AccountingEntity(TruncatedModel):
    id = models.CharField(db_column='ID', primary_key=True, max_length=15)  # Field name made lowercase.
    entity_name = models.CharField(db_column='ENTITY_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    entity_addr_1 = models.CharField(db_column='ENTITY_ADDR_1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    entity_addr_2 = models.CharField(db_column='ENTITY_ADDR_2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    entity_addr_3 = models.CharField(db_column='ENTITY_ADDR_3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    entity_city = models.CharField(db_column='ENTITY_CITY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    entity_state = models.CharField(db_column='ENTITY_STATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    entity_zipcode = models.CharField(db_column='ENTITY_ZIPCODE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    entity_country = models.CharField(db_column='ENTITY_COUNTRY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    entity_country_id = models.CharField(db_column='ENTITY_COUNTRY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1)  # Field name made lowercase.
    tax_id_number = models.CharField(db_column='TAX_ID_NUMBER', max_length=25, blank=True, null=True)  # Field name made lowercase.
    def_language_id = models.CharField(db_column='DEF_LANGUAGE_ID', max_length=3)  # Field name made lowercase.
    functional_currency_id = models.CharField(db_column='FUNCTIONAL_CURRENCY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    xchg_rate_date = models.CharField(db_column='XCHG_RATE_DATE', max_length=1)  # Field name made lowercase.
    xchg_rate_def_rcpt = models.CharField(db_column='XCHG_RATE_DEF_RCPT', max_length=1)  # Field name made lowercase.
    costing_interlevel = models.CharField(db_column='COSTING_INTERLEVEL', max_length=1)  # Field name made lowercase.
    costing_method = models.CharField(db_column='COSTING_METHOD', max_length=1)  # Field name made lowercase.
    costing_source = models.CharField(db_column='COSTING_SOURCE', max_length=1)  # Field name made lowercase.
    costing_std_labor = models.CharField(db_column='COSTING_STD_LABOR', max_length=1)  # Field name made lowercase.
    costing_wip_method = models.CharField(db_column='COSTING_WIP_METHOD', max_length=1)  # Field name made lowercase.
    cost_by_trace_id = models.CharField(db_column='COST_BY_TRACE_ID', max_length=1, blank=True, null=True)  # Field name made lowercase.
    burden_source = models.CharField(db_column='BURDEN_SOURCE', max_length=1)  # Field name made lowercase.
    fifo_by_location = models.CharField(db_column='FIFO_BY_LOCATION', max_length=1)  # Field name made lowercase.
    earned_rev_method = models.CharField(db_column='EARNED_REV_METHOD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vat_enabled = models.CharField(db_column='VAT_ENABLED', max_length=1)  # Field name made lowercase.
    vat_discounted = models.CharField(db_column='VAT_DISCOUNTED', max_length=1)  # Field name made lowercase.
    vat_registration = models.CharField(db_column='VAT_REGISTRATION', max_length=25, blank=True, null=True)  # Field name made lowercase.
    vat_payb_export_id = models.CharField(db_column='VAT_PAYB_EXPORT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vat_recv_export_id = models.CharField(db_column='VAT_RECV_EXPORT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vat_category_reqd = models.CharField(db_column='VAT_CATEGORY_REQD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vat_on_freight = models.CharField(db_column='VAT_ON_FREIGHT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    next_vat_seq = models.IntegerField(db_column='NEXT_VAT_SEQ')  # Field name made lowercase.
    vat_file_prefix = models.CharField(db_column='VAT_FILE_PREFIX', max_length=5, blank=True, null=True)  # Field name made lowercase.
    vat_file_zeros = models.CharField(db_column='VAT_FILE_ZEROS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vat_file_places = models.SmallIntegerField(db_column='VAT_FILE_PLACES', blank=True, null=True)  # Field name made lowercase.
    vat_book_num_gen = models.CharField(db_column='VAT_BOOK_NUM_GEN', max_length=1)  # Field name made lowercase.
    intrastat_enabled = models.CharField(db_column='INTRASTAT_ENABLED', max_length=1)  # Field name made lowercase.
    verify_intrastat = models.CharField(db_column='VERIFY_INTRASTAT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    country = models.ForeignKey('Country', models.DO_NOTHING, db_column='COUNTRY_ID', blank=True, null=True)  # Field name made lowercase.
    branch_id = models.CharField(db_column='BRANCH_ID', max_length=3, blank=True, null=True)  # Field name made lowercase.
    next_intrastat_seq = models.IntegerField(db_column='NEXT_INTRASTAT_SEQ')  # Field name made lowercase.
    intra_file_prefix = models.CharField(db_column='INTRA_FILE_PREFIX', max_length=5, blank=True, null=True)  # Field name made lowercase.
    intra_file_zeros = models.CharField(db_column='INTRA_FILE_ZEROS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    intra_file_places = models.IntegerField(db_column='INTRA_FILE_PLACES')  # Field name made lowercase.
    intrastat_freq = models.CharField(db_column='INTRASTAT_FREQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    intra_arrv_expt_id = models.CharField(db_column='INTRA_ARRV_EXPT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    intra_disp_expt_id = models.CharField(db_column='INTRA_DISP_EXPT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    next_esl_seq = models.IntegerField(db_column='NEXT_ESL_SEQ')  # Field name made lowercase.
    esl_file_prefix = models.CharField(db_column='ESL_FILE_PREFIX', max_length=5, blank=True, null=True)  # Field name made lowercase.
    esl_file_zeros = models.CharField(db_column='ESL_FILE_ZEROS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    esl_file_places = models.SmallIntegerField(db_column='ESL_FILE_PLACES', blank=True, null=True)  # Field name made lowercase.
    esl_freq = models.CharField(db_column='ESL_FREQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    esl_export_id = models.CharField(db_column='ESL_EXPORT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    a_show_country = models.CharField(db_column='A_SHOW_COUNTRY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    a_show_excise_pr = models.CharField(db_column='A_SHOW_EXCISE_PR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    a_show_port_arrvl = models.CharField(db_column='A_SHOW_PORT_ARRVL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    a_show_port_trans = models.CharField(db_column='A_SHOW_PORT_TRANS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    a_show_region = models.CharField(db_column='A_SHOW_REGION', max_length=1, blank=True, null=True)  # Field name made lowercase.
    a_show_siret_no = models.CharField(db_column='A_SHOW_SIRET_NO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    a_show_tariff_code = models.CharField(db_column='A_SHOW_TARIFF_CODE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    d_show_country = models.CharField(db_column='D_SHOW_COUNTRY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    d_show_excise_pr = models.CharField(db_column='D_SHOW_EXCISE_PR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    d_show_port_arrvl = models.CharField(db_column='D_SHOW_PORT_ARRVL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    d_show_port_trans = models.CharField(db_column='D_SHOW_PORT_TRANS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    d_show_region = models.CharField(db_column='D_SHOW_REGION', max_length=1, blank=True, null=True)  # Field name made lowercase.
    d_show_siret_no = models.CharField(db_column='D_SHOW_SIRET_NO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    d_show_tariff_code = models.CharField(db_column='D_SHOW_TARIFF_CODE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    next_pay_batch_seq = models.IntegerField(db_column='NEXT_PAY_BATCH_SEQ')  # Field name made lowercase.
    pay_file_prefix = models.CharField(db_column='PAY_FILE_PREFIX', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pay_file_zeros = models.CharField(db_column='PAY_FILE_ZEROS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pay_file_places = models.SmallIntegerField(db_column='PAY_FILE_PLACES')  # Field name made lowercase.
    withhold_enabled = models.CharField(db_column='WITHHOLD_ENABLED', max_length=1)  # Field name made lowercase.
    wh_certif_expt_id = models.CharField(db_column='WH_CERTIF_EXPT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    wh_summary_expt_id = models.CharField(db_column='WH_SUMMARY_EXPT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    next_withhold_seq = models.IntegerField(db_column='NEXT_WITHHOLD_SEQ')  # Field name made lowercase.
    cash_percent_var = models.CharField(db_column='CASH_PERCENT_VAR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cash_min_var = models.DecimalField(db_column='CASH_MIN_VAR', max_digits=23, decimal_places=8)  # Field name made lowercase.
    cash_max_var = models.DecimalField(db_column='CASH_MAX_VAR', max_digits=23, decimal_places=8)  # Field name made lowercase.
    commission_support = models.CharField(db_column='COMMISSION_SUPPORT', max_length=1)  # Field name made lowercase.
    comm_payment_meth = models.CharField(db_column='COMM_PAYMENT_METH', max_length=1)  # Field name made lowercase.
    social_security_no = models.CharField(db_column='SOCIAL_SECURITY_NO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    wipvas_enabled = models.CharField(db_column='WIPVAS_ENABLED', max_length=1)  # Field name made lowercase.
    ddp_enabled = models.CharField(db_column='DDP_ENABLED', max_length=1)  # Field name made lowercase.
    auto_allocate = models.CharField(db_column='AUTO_ALLOCATE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    co_alloc_level = models.CharField(db_column='CO_ALLOC_LEVEL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    req_alloc_level = models.CharField(db_column='REQ_ALLOC_LEVEL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    def_ship_weight_um = models.CharField(db_column='DEF_SHIP_WEIGHT_UM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    backord_fill_rate = models.DecimalField(db_column='BACKORD_FILL_RATE', max_digits=15, decimal_places=2)  # Field name made lowercase.
    proj_burden_rule = models.CharField(db_column='PROJ_BURDEN_RULE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    req_app1_label = models.CharField(db_column='REQ_APP1_LABEL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    req_app2_label = models.CharField(db_column='REQ_APP2_LABEL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    req_app3_label = models.CharField(db_column='REQ_APP3_LABEL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    req_app4_label = models.CharField(db_column='REQ_APP4_LABEL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    req_gen_all_tasks = models.CharField(db_column='REQ_GEN_ALL_TASKS', max_length=1)  # Field name made lowercase.
    req_cmnt_pwd_req = models.CharField(db_column='REQ_CMNT_PWD_REQ', max_length=1)  # Field name made lowercase.
    calendar = models.ForeignKey('FinancialCalendar', models.DO_NOTHING, db_column='CALENDAR_ID', blank=True, null=True)  # Field name made lowercase.
    def_cash_mgt_bank_ar = models.CharField(db_column='DEF_CASH_MGT_BANK_AR', max_length=15, blank=True, null=True)  # Field name made lowercase.
    def_cash_mgt_bank_ap = models.CharField(db_column='DEF_CASH_MGT_BANK_AP', max_length=15, blank=True, null=True)  # Field name made lowercase.
    cust_bal_incl_type = models.CharField(db_column='CUST_BAL_INCL_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fin_batch_single_trans = models.CharField(db_column='FIN_BATCH_SINGLE_TRANS', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ACCOUNTING_ENTITY'


class Site(TruncatedModel):
    id = models.CharField(db_column='ID', primary_key=True, max_length=15)  # Field name made lowercase.
    entity = models.ForeignKey(AccountingEntity, models.DO_NOTHING, db_column='ENTITY_ID')  # Field name made lowercase.
    soft_alloc_date = models.DateTimeField(db_column='SOFT_ALLOC_DATE', blank=True, null=True)  # Field name made lowercase.
    vq_enabled = models.CharField(db_column='VQ_ENABLED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vq_query_use = models.CharField(db_column='VQ_QUERY_USE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vq_directory = models.CharField(db_column='VQ_DIRECTORY', max_length=128, blank=True, null=True)  # Field name made lowercase.
    vq_dbname = models.CharField(db_column='VQ_DBNAME', max_length=80, blank=True, null=True)  # Field name made lowercase.
    del_pack_cls_prd = models.CharField(db_column='DEL_PACK_CLS_PRD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    part_udf_labels = models.CharField(db_column='PART_UDF_LABELS', max_length=250, blank=True, null=True)  # Field name made lowercase.
    proj_udf_labels = models.CharField(db_column='PROJ_UDF_LABELS', max_length=250, blank=True, null=True)  # Field name made lowercase.
    shop_udf_labels = models.CharField(db_column='SHOP_UDF_LABELS', max_length=250, blank=True, null=True)  # Field name made lowercase.
    site_name = models.CharField(db_column='SITE_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    site_addr_1 = models.CharField(db_column='SITE_ADDR_1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    site_addr_2 = models.CharField(db_column='SITE_ADDR_2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    site_addr_3 = models.CharField(db_column='SITE_ADDR_3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    site_city = models.CharField(db_column='SITE_CITY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    site_state = models.CharField(db_column='SITE_STATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    site_zipcode = models.CharField(db_column='SITE_ZIPCODE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    site_country = models.CharField(db_column='SITE_COUNTRY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    site_country_id = models.CharField(db_column='SITE_COUNTRY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    def_shipper_status = models.CharField(db_column='DEF_SHIPPER_STATUS', max_length=1)  # Field name made lowercase.
    demand_fence_1 = models.IntegerField(db_column='DEMAND_FENCE_1', blank=True, null=True)  # Field name made lowercase.
    demand_fence_2 = models.IntegerField(db_column='DEMAND_FENCE_2', blank=True, null=True)  # Field name made lowercase.
    use_mrp_dmnd_fence = models.CharField(db_column='USE_MRP_DMND_FENCE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    show_loc_message = models.CharField(db_column='SHOW_LOC_MESSAGE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    show_whs_message = models.CharField(db_column='SHOW_WHS_MESSAGE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    add_loc_on_fly = models.CharField(db_column='ADD_LOC_ON_FLY', max_length=1)  # Field name made lowercase.
    alloc_to_later_dem = models.CharField(db_column='ALLOC_TO_LATER_DEM', max_length=1)  # Field name made lowercase.
    sch_notch_size = models.SmallIntegerField(db_column='SCH_NOTCH_SIZE', blank=True, null=True)  # Field name made lowercase.
    use_cal_rls_calc = models.CharField(db_column='USE_CAL_RLS_CALC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    use_cal_lt_calc = models.CharField(db_column='USE_CAL_LT_CALC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hard_release_date = models.CharField(db_column='HARD_RELEASE_DATE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    use_supply_bef_lt = models.CharField(db_column='USE_SUPPLY_BEF_LT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dbr_can_delete_wo = models.CharField(db_column='DBR_CAN_DELETE_WO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag_res_ccr_pct = models.IntegerField(db_column='FLAG_RES_CCR_PCT', blank=True, null=True)  # Field name made lowercase.
    free_wo_ship_buf = models.IntegerField(db_column='FREE_WO_SHIP_BUF')  # Field name made lowercase.
    prevent_negative = models.CharField(db_column='PREVENT_NEGATIVE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    allocate_negative = models.CharField(db_column='ALLOCATE_NEGATIVE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    issue_negative = models.CharField(db_column='ISSUE_NEGATIVE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    issneg_location = models.CharField(db_column='ISSNEG_LOCATION', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ship_trk_enabled = models.CharField(db_column='SHIP_TRK_ENABLED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    def_lbl_format_id = models.CharField(db_column='DEF_LBL_FORMAT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partial_ship_prepay_bal = models.CharField(db_column='PARTIAL_SHIP_PREPAY_BAL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shp_reason_cd_req = models.CharField(db_column='SHP_REASON_CD_REQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ecn_change_on_hold = models.CharField(db_column='ECN_CHANGE_ON_HOLD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ecn_cmnt_pwd_req = models.CharField(db_column='ECN_CMNT_PWD_REQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ecn_gen_all_tasks = models.CharField(db_column='ECN_GEN_ALL_TASKS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ecn_revise_items = models.CharField(db_column='ECN_REVISE_ITEMS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    one_ecn_per_part = models.CharField(db_column='ONE_ECN_PER_PART', max_length=1, blank=True, null=True)  # Field name made lowercase.
    one_ecn_per_doc = models.CharField(db_column='ONE_ECN_PER_DOC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    one_ecn_per_wo = models.CharField(db_column='ONE_ECN_PER_WO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    one_ecn_per_mstr = models.CharField(db_column='ONE_ECN_PER_MSTR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    one_ecn_per_prj = models.CharField(db_column='ONE_ECN_PER_PRJ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ecn_auth_label = models.CharField(db_column='ECN_AUTH_LABEL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ecn_impl_label = models.CharField(db_column='ECN_IMPL_LABEL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ecn_aprv_label = models.CharField(db_column='ECN_APRV_LABEL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ecn_dist_label = models.CharField(db_column='ECN_DIST_LABEL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    apply_ecn_inprocess_wo = models.CharField(db_column='APPLY_ECN_INPROCESS_WO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ecn_req_for_update = models.CharField(db_column='ECN_REQ_FOR_UPDATE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lock_ecns = models.CharField(db_column='LOCK_ECNS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    autogen_lab_on_rec = models.CharField(db_column='AUTOGEN_LAB_ON_REC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    iss_reas_req_iss = models.CharField(db_column='ISS_REAS_REQ_ISS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    iss_reas_req_issrtn = models.CharField(db_column='ISS_REAS_REQ_ISSRTN', max_length=1, blank=True, null=True)  # Field name made lowercase.
    adj_reas_req_adjin = models.CharField(db_column='ADJ_REAS_REQ_ADJIN', max_length=1, blank=True, null=True)  # Field name made lowercase.
    adj_reas_req_adjout = models.CharField(db_column='ADJ_REAS_REQ_ADJOUT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    deviation_required = models.CharField(db_column='DEVIATION_REQUIRED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    def_warehouse_id = models.CharField(db_column='DEF_WAREHOUSE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    backflush_labtick = models.CharField(db_column='BACKFLUSH_LABTICK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    backflush_labcost = models.CharField(db_column='BACKFLUSH_LABCOST', max_length=1, blank=True, null=True)  # Field name made lowercase.
    backflush_sub_ids = models.CharField(db_column='BACKFLUSH_SUB_IDS', max_length=1)  # Field name made lowercase.
    default_employee = models.CharField(db_column='DEFAULT_EMPLOYEE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    transfer_reason_req = models.CharField(db_column='TRANSFER_REASON_REQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lab_tic_req_insp = models.CharField(db_column='LAB_TIC_REQ_INSP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    purc_recv_req_insp = models.CharField(db_column='PURC_RECV_REQ_INSP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    aps_def_loc_id = models.CharField(db_column='APS_DEF_LOC_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    aps_def_service_id = models.CharField(db_column='APS_DEF_SERVICE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    aps_def_whse_id = models.CharField(db_column='APS_DEF_WHSE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    aps_default_cust = models.CharField(db_column='APS_DEFAULT_CUST', max_length=15, blank=True, null=True)  # Field name made lowercase.
    aps_default_empl = models.CharField(db_column='APS_DEFAULT_EMPL', max_length=15, blank=True, null=True)  # Field name made lowercase.
    aps_default_vendor = models.CharField(db_column='APS_DEFAULT_VENDOR', max_length=15, blank=True, null=True)  # Field name made lowercase.
    aps_implied_dec = models.CharField(db_column='APS_IMPLIED_DEC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    aps_trim_strings = models.CharField(db_column='APS_TRIM_STRINGS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cal_exc_data_path = models.CharField(db_column='CAL_EXC_DATA_PATH', max_length=128, blank=True, null=True)  # Field name made lowercase.
    cust_ord_data_path = models.CharField(db_column='CUST_ORD_DATA_PATH', max_length=128, blank=True, null=True)  # Field name made lowercase.
    froze_op_data_path = models.CharField(db_column='FROZE_OP_DATA_PATH', max_length=128, blank=True, null=True)  # Field name made lowercase.
    inv_data_path = models.CharField(db_column='INV_DATA_PATH', max_length=128, blank=True, null=True)  # Field name made lowercase.
    labor_data_path = models.CharField(db_column='LABOR_DATA_PATH', max_length=128, blank=True, null=True)  # Field name made lowercase.
    mast_sch_data_path = models.CharField(db_column='MAST_SCH_DATA_PATH', max_length=128, blank=True, null=True)  # Field name made lowercase.
    part_data_path = models.CharField(db_column='PART_DATA_PATH', max_length=128, blank=True, null=True)  # Field name made lowercase.
    planning_data_path = models.CharField(db_column='PLANNING_DATA_PATH', max_length=128, blank=True, null=True)  # Field name made lowercase.
    purc_ord_data_path = models.CharField(db_column='PURC_ORD_DATA_PATH', max_length=128, blank=True, null=True)  # Field name made lowercase.
    sched_data_path = models.CharField(db_column='SCHED_DATA_PATH', max_length=128, blank=True, null=True)  # Field name made lowercase.
    shop_data_path = models.CharField(db_column='SHOP_DATA_PATH', max_length=128, blank=True, null=True)  # Field name made lowercase.
    work_ord_data_path = models.CharField(db_column='WORK_ORD_DATA_PATH', max_length=128, blank=True, null=True)  # Field name made lowercase.
    field_delimiter = models.CharField(db_column='FIELD_DELIMITER', max_length=1, blank=True, null=True)  # Field name made lowercase.
    record_delimiter = models.CharField(db_column='RECORD_DELIMITER', max_length=1, blank=True, null=True)  # Field name made lowercase.
    quoted_string = models.CharField(db_column='QUOTED_STRING', max_length=1, blank=True, null=True)  # Field name made lowercase.
    standard_sched_id = models.CharField(db_column='STANDARD_SCHED_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    ups_account_id = models.CharField(db_column='UPS_ACCOUNT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    rls_near_days = models.SmallIntegerField(db_column='RLS_NEAR_DAYS', blank=True, null=True)  # Field name made lowercase.
    sugg_rls_near_days = models.SmallIntegerField(db_column='SUGG_RLS_NEAR_DAYS', blank=True, null=True)  # Field name made lowercase.
    enabled_products = models.CharField(db_column='ENABLED_PRODUCTS', max_length=8, blank=True, null=True)  # Field name made lowercase.
    internal_cust_id = models.CharField(db_column='INTERNAL_CUST_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    plan_by_warehouse = models.CharField(db_column='PLAN_BY_WAREHOUSE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendor_exclusion = models.CharField(db_column='VENDOR_EXCLUSION', max_length=1)  # Field name made lowercase.
    plm_url = models.CharField(db_column='PLM_URL', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    plm_enabled = models.CharField(db_column='PLM_ENABLED', max_length=1)  # Field name made lowercase.
    periods_per_year = models.SmallIntegerField(db_column='PERIODS_PER_YEAR')  # Field name made lowercase.
    period_type = models.CharField(db_column='PERIOD_TYPE', max_length=1)  # Field name made lowercase.
    mult_ap_inv_rcvr = models.CharField(db_column='MULT_AP_INV_RCVR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dup_ap_check_no = models.CharField(db_column='DUP_AP_CHECK_NO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mrp_in_process = models.CharField(db_column='MRP_IN_PROCESS', max_length=1)  # Field name made lowercase.
    percent_compl = models.CharField(db_column='PERCENT_COMPL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty_compl_by_hrs = models.CharField(db_column='QTY_COMPL_BY_HRS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    max_qty_complete = models.DecimalField(db_column='MAX_QTY_COMPLETE', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    auto_issue_method = models.CharField(db_column='AUTO_ISSUE_METHOD', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'SITE'


class VendorPart(TruncatedModel):
    rowid = models.AutoField(primary_key=True, db_column='ROWID')  # Field name made lowercase.
    part = models.ForeignKey(Part, models.DO_NOTHING, db_column='PART_ID')  # Field name made lowercase.
    vendor = models.ForeignKey(Vendor, models.DO_NOTHING, db_column='VENDOR_ID')  # Field name made lowercase.
    vendor_part_id = models.CharField(db_column='VENDOR_PART_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    long_description = models.BinaryField(db_column='LONG_DESCRIPTION', blank=True, null=True)  # Field name made lowercase.
    leadtime_buffer = models.SmallIntegerField(db_column='LEADTIME_BUFFER', blank=True, null=True)  # Field name made lowercase.
    site = models.ForeignKey(Site, models.DO_NOTHING, db_column='SITE_ID')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'VENDOR_PART'
        unique_together = (('site', 'part', 'vendor', 'vendor_part_id'),)


class Quote(TruncatedModel):
    id = models.CharField(db_column='ID', primary_key=True, max_length=15)  # Field name made lowercase.
    customer = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CUSTOMER_ID', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_1 = models.CharField(db_column='ADDR_1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_2 = models.CharField(db_column='ADDR_2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_3 = models.CharField(db_column='ADDR_3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='CITY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='STATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(db_column='ZIPCODE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='COUNTRY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    quote_country_id = models.CharField(db_column='QUOTE_COUNTRY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    contact = models.ForeignKey(Contact, models.DO_NOTHING, db_column='CONTACT_ID', blank=True, null=True)  # Field name made lowercase.
    contact_first_name = models.CharField(db_column='CONTACT_FIRST_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact_last_name = models.CharField(db_column='CONTACT_LAST_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact_initial = models.CharField(db_column='CONTACT_INITIAL', max_length=2, blank=True, null=True)  # Field name made lowercase.
    contact_position = models.CharField(db_column='CONTACT_POSITION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    contact_honorific = models.CharField(db_column='CONTACT_HONORIFIC', max_length=15, blank=True, null=True)  # Field name made lowercase.
    contact_salutation = models.CharField(db_column='CONTACT_SALUTATION', max_length=60, blank=True, null=True)  # Field name made lowercase.
    contact_phone = models.CharField(db_column='CONTACT_PHONE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contact_fax = models.CharField(db_column='CONTACT_FAX', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contact_email = models.CharField(db_column='CONTACT_EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    salesrep_id = models.CharField(db_column='SALESREP_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    territory = models.CharField(db_column='TERRITORY', max_length=15, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1)  # Field name made lowercase.
    won_loss_date = models.DateTimeField(db_column='WON_LOSS_DATE', blank=True, null=True)  # Field name made lowercase.
    won_loss_reason = models.CharField(db_column='WON_LOSS_REASON', max_length=80, blank=True, null=True)  # Field name made lowercase.
    quote_date = models.DateTimeField(db_column='QUOTE_DATE')  # Field name made lowercase.
    expiration_date = models.DateTimeField(db_column='EXPIRATION_DATE', blank=True, null=True)  # Field name made lowercase.
    followup_date = models.DateTimeField(db_column='FOLLOWUP_DATE', blank=True, null=True)  # Field name made lowercase.
    expected_win_date = models.DateTimeField(db_column='EXPECTED_WIN_DATE', blank=True, null=True)  # Field name made lowercase.
    win_probability = models.DecimalField(db_column='WIN_PROBABILITY', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ship_via = models.CharField(db_column='SHIP_VIA', max_length=40, blank=True, null=True)  # Field name made lowercase.
    free_on_board = models.CharField(db_column='FREE_ON_BOARD', max_length=25, blank=True, null=True)  # Field name made lowercase.
    terms_net_type = models.CharField(db_column='TERMS_NET_TYPE', max_length=1)  # Field name made lowercase.
    terms_net_days = models.SmallIntegerField(db_column='TERMS_NET_DAYS', blank=True, null=True)  # Field name made lowercase.
    terms_net_date = models.DateTimeField(db_column='TERMS_NET_DATE', blank=True, null=True)  # Field name made lowercase.
    terms_disc_days = models.SmallIntegerField(db_column='TERMS_DISC_DAYS', blank=True, null=True)  # Field name made lowercase.
    terms_disc_type = models.CharField(db_column='TERMS_DISC_TYPE', max_length=1)  # Field name made lowercase.
    terms_disc_date = models.DateTimeField(db_column='TERMS_DISC_DATE', blank=True, null=True)  # Field name made lowercase.
    terms_disc_percent = models.DecimalField(db_column='TERMS_DISC_PERCENT', max_digits=5, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    terms_description = models.CharField(db_column='TERMS_DESCRIPTION', max_length=80, blank=True, null=True)  # Field name made lowercase.
    freight_terms = models.CharField(db_column='FREIGHT_TERMS', max_length=1)  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='CREATE_DATE')  # Field name made lowercase.
    user_id = models.CharField(db_column='USER_ID', max_length=20)  # Field name made lowercase.
    quoted_leadtime = models.SmallIntegerField(db_column='QUOTED_LEADTIME', blank=True, null=True)  # Field name made lowercase.
    currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='CURRENCY_ID', blank=True, null=True)  # Field name made lowercase.
    site = models.ForeignKey('Site', models.DO_NOTHING, db_column='SITE_ID')  # Field name made lowercase.
    discount_code = models.ForeignKey(CustomerDiscount, models.DO_NOTHING, db_column='DISCOUNT_CODE', blank=True, null=True)  # Field name made lowercase.
    printed_date = models.DateTimeField(db_column='PRINTED_DATE', blank=True, null=True)  # Field name made lowercase.
    user_1 = models.CharField(db_column='USER_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_2 = models.CharField(db_column='USER_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_3 = models.CharField(db_column='USER_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_4 = models.CharField(db_column='USER_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_5 = models.CharField(db_column='USER_5', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_6 = models.CharField(db_column='USER_6', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_7 = models.CharField(db_column='USER_7', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_8 = models.CharField(db_column='USER_8', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_9 = models.CharField(db_column='USER_9', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_10 = models.CharField(db_column='USER_10', max_length=80, blank=True, null=True)  # Field name made lowercase.
    udf_layout_id = models.CharField(db_column='UDF_LAYOUT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    status_eff_date = models.DateTimeField(db_column='STATUS_EFF_DATE')  # Field name made lowercase.
    project_id = models.CharField(db_column='PROJECT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    terms = models.ForeignKey('Terms', models.DO_NOTHING, db_column='TERMS_ID', blank=True, null=True)  # Field name made lowercase.
    contact_phone_ext = models.CharField(db_column='CONTACT_PHONE_EXT', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'QUOTE'


class QuoteLine(TruncatedModel):
    rowid = models.AutoField(primary_key=True, db_column='ROWID')  # Field name made lowercase.
    quote = models.OneToOneField(Quote, models.DO_NOTHING, db_column='QUOTE_ID')  # Field name made lowercase.
    line_no = models.SmallIntegerField(db_column='LINE_NO')  # Field name made lowercase.
    part = models.ForeignKey(Part, models.DO_NOTHING, db_column='PART_ID', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=120, blank=True, null=True)  # Field name made lowercase.
    customer_part_id = models.CharField(db_column='CUSTOMER_PART_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    workorder_type = models.CharField(db_column='WORKORDER_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    workorder_base_id = models.CharField(db_column='WORKORDER_BASE_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    workorder_lot_id = models.CharField(db_column='WORKORDER_LOT_ID', max_length=3, blank=True, null=True)  # Field name made lowercase.
    workorder_split_id = models.CharField(db_column='WORKORDER_SPLIT_ID', max_length=3, blank=True, null=True)  # Field name made lowercase.
    workorder_sub_id = models.CharField(db_column='WORKORDER_SUB_ID', max_length=3, blank=True, null=True)  # Field name made lowercase.
    drawing_id = models.CharField(db_column='DRAWING_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    drawing_rev_no = models.CharField(db_column='DRAWING_REV_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='CREATE_DATE')  # Field name made lowercase.
    product_code = models.CharField(db_column='PRODUCT_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    commodity_code = models.CharField(db_column='COMMODITY_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    service_charge_id = models.CharField(db_column='SERVICE_CHARGE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    user_1 = models.CharField(db_column='USER_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_2 = models.CharField(db_column='USER_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_3 = models.CharField(db_column='USER_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_4 = models.CharField(db_column='USER_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_5 = models.CharField(db_column='USER_5', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_6 = models.CharField(db_column='USER_6', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_7 = models.CharField(db_column='USER_7', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_8 = models.CharField(db_column='USER_8', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_9 = models.CharField(db_column='USER_9', max_length=80, blank=True, null=True)  # Field name made lowercase.
    user_10 = models.CharField(db_column='USER_10', max_length=80, blank=True, null=True)  # Field name made lowercase.
    udf_layout_id = models.CharField(db_column='UDF_LAYOUT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    orig_stage_revision_id = models.CharField(db_column='ORIG_STAGE_REVISION_ID', max_length=24, blank=True, null=True)  # Field name made lowercase.
    price_note = models.CharField(db_column='PRICE_NOTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    discount_note = models.CharField(db_column='DISCOUNT_NOTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    freight_note = models.CharField(db_column='FREIGHT_NOTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    commission_note = models.CharField(db_column='COMMISSION_NOTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    wbs_code = models.CharField(db_column='WBS_CODE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wbs_description = models.CharField(db_column='WBS_DESCRIPTION', max_length=80, blank=True, null=True)  # Field name made lowercase.
    wbs_clin = models.CharField(db_column='WBS_CLIN', max_length=15, blank=True, null=True)  # Field name made lowercase.
    proj_ref_sub_id = models.CharField(db_column='PROJ_REF_SUB_ID', max_length=3, blank=True, null=True)  # Field name made lowercase.
    proj_ref_seq_no = models.SmallIntegerField(db_column='PROJ_REF_SEQ_NO', blank=True, null=True)  # Field name made lowercase.
    length = models.DecimalField(db_column='LENGTH', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    width = models.DecimalField(db_column='WIDTH', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    height = models.DecimalField(db_column='HEIGHT', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    dimensions_um = models.CharField(db_column='DIMENSIONS_UM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    price_group_id = models.CharField(db_column='PRICE_GROUP_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'QUOTE_LINE'
        unique_together = (('quote', 'line_no'),)


class QuoteLineBilling(TruncatedModel):
    quote = models.OneToOneField(QuoteLine, models.DO_NOTHING, db_column='QUOTE_ID', primary_key=True)  # Field name made lowercase.
    quote_line_no = models.ForeignKey(QuoteLine, models.DO_NOTHING, db_column='QUOTE_LINE_NO')  # Field name made lowercase.
    event_seq_no = models.SmallIntegerField(db_column='EVENT_SEQ_NO')  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=80, blank=True, null=True)  # Field name made lowercase.
    bill_amount = models.DecimalField(db_column='BILL_AMOUNT', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    bill_percent = models.DecimalField(db_column='BILL_PERCENT', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    rev_amount = models.DecimalField(db_column='REV_AMOUNT', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    rev_percent = models.DecimalField(db_column='REV_PERCENT', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    milestone_id = models.CharField(db_column='MILESTONE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    event_date = models.DateTimeField(db_column='EVENT_DATE', blank=True, null=True)  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='CREATE_DATE')  # Field name made lowercase.
    user_id = models.CharField(db_column='USER_ID', max_length=20)  # Field name made lowercase.
    rev_gl_acct = models.ForeignKey(Account, models.DO_NOTHING, db_column='REV_GL_ACCT_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'QUOTE_LINE_BILLING'
        unique_together = (('quote', 'quote_line_no', 'event_seq_no'),)


class QuotePrice(TruncatedModel):
    rowid = models.AutoField(primary_key=True, db_column='ROWID')  # Field name made lowercase.
    quote = models.OneToOneField(Quote, models.DO_NOTHING, db_column='QUOTE_ID')  # Field name made lowercase.
    quote_line_no = models.SmallIntegerField(db_column='QUOTE_LINE_NO')  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    calc_unit_cost = models.DecimalField(db_column='CALC_UNIT_COST', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    calc_unit_price = models.DecimalField(db_column='CALC_UNIT_PRICE', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price = models.DecimalField(db_column='UNIT_PRICE', max_digits=22, decimal_places=8)  # Field name made lowercase.
    selling_um = models.CharField(db_column='SELLING_UM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    pur_matl_percent = models.DecimalField(db_column='PUR_MATL_PERCENT', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    fab_matl_percent = models.DecimalField(db_column='FAB_MATL_PERCENT', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    labor_percent = models.DecimalField(db_column='LABOR_PERCENT', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    burden_percent = models.DecimalField(db_column='BURDEN_PERCENT', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    service_percent = models.DecimalField(db_column='SERVICE_PERCENT', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    pur_matl_markup = models.DecimalField(db_column='PUR_MATL_MARKUP', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    fab_matl_markup = models.DecimalField(db_column='FAB_MATL_MARKUP', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    labor_markup = models.DecimalField(db_column='LABOR_MARKUP', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    burden_markup = models.DecimalField(db_column='BURDEN_MARKUP', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    service_markup = models.DecimalField(db_column='SERVICE_MARKUP', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    in_proforma = models.CharField(db_column='IN_PROFORMA', max_length=1)  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='CREATE_DATE')  # Field name made lowercase.
    pur_matl_gsa = models.DecimalField(db_column='PUR_MATL_GSA', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    fab_matl_gsa = models.DecimalField(db_column='FAB_MATL_GSA', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    labor_gsa = models.DecimalField(db_column='LABOR_GSA', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    burden_gsa = models.DecimalField(db_column='BURDEN_GSA', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    service_gsa = models.DecimalField(db_column='SERVICE_GSA', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    trade_disc_percent = models.DecimalField(db_column='TRADE_DISC_PERCENT', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    in_total = models.CharField(db_column='IN_TOTAL', max_length=1)  # Field name made lowercase.
    piece_count = models.DecimalField(db_column='PIECE_COUNT', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'QUOTE_PRICE'
        unique_together = (('quote', 'quote_line_no', 'qty'),)


class VendorService(TruncatedModel):
    service_id = models.CharField(db_column='SERVICE_ID', max_length=15)  # Field name made lowercase.
    vendor_id = models.CharField(db_column='VENDOR_ID', max_length=15)  # Field name made lowercase.
    vendor_service_id = models.CharField(db_column='VENDOR_SERVICE_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=40, blank=True, null=True)  # Field name made lowercase.
    est_cost_per_unit = models.DecimalField(db_column='EST_COST_PER_UNIT', max_digits=22, decimal_places=8)  # Field name made lowercase.
    est_min_charge = models.DecimalField(db_column='EST_MIN_CHARGE', max_digits=23, decimal_places=8)  # Field name made lowercase.
    est_base_charge = models.DecimalField(db_column='EST_BASE_CHARGE', max_digits=23, decimal_places=8)  # Field name made lowercase.
    vat_code = models.CharField(db_column='VAT_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    schedule_rank = models.SmallIntegerField(db_column='SCHEDULE_RANK', blank=True, null=True)  # Field name made lowercase.
    run = models.DecimalField(db_column='RUN', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    run_type = models.CharField(db_column='RUN_TYPE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    load_size_qty = models.DecimalField(db_column='LOAD_SIZE_QTY', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    transit_days = models.DecimalField(db_column='TRANSIT_DAYS', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    purchase_um = models.CharField(db_column='PURCHASE_UM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    long_description = models.BinaryField(db_column='LONG_DESCRIPTION', blank=True, null=True)  # Field name made lowercase.
    site = models.OneToOneField(Site, models.DO_NOTHING, db_column='SITE_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'VENDOR_SERVICE'
        unique_together = (('site', 'service_id', 'vendor_id'),)


class VendorServQuote(TruncatedModel):
    vendor_id = models.CharField(db_column='VENDOR_ID', max_length=15)  # Field name made lowercase.
    vendor_service_id = models.CharField(db_column='VENDOR_SERVICE_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='CURRENCY_ID')  # Field name made lowercase.
    qty_break_1 = models.DecimalField(db_column='QTY_BREAK_1', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_2 = models.DecimalField(db_column='QTY_BREAK_2', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_3 = models.DecimalField(db_column='QTY_BREAK_3', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_4 = models.DecimalField(db_column='QTY_BREAK_4', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_5 = models.DecimalField(db_column='QTY_BREAK_5', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_6 = models.DecimalField(db_column='QTY_BREAK_6', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_7 = models.DecimalField(db_column='QTY_BREAK_7', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_8 = models.DecimalField(db_column='QTY_BREAK_8', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_9 = models.DecimalField(db_column='QTY_BREAK_9', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_10 = models.DecimalField(db_column='QTY_BREAK_10', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_1 = models.DecimalField(db_column='UNIT_PRICE_1', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_2 = models.DecimalField(db_column='UNIT_PRICE_2', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_3 = models.DecimalField(db_column='UNIT_PRICE_3', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_4 = models.DecimalField(db_column='UNIT_PRICE_4', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_5 = models.DecimalField(db_column='UNIT_PRICE_5', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_6 = models.DecimalField(db_column='UNIT_PRICE_6', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_7 = models.DecimalField(db_column='UNIT_PRICE_7', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_8 = models.DecimalField(db_column='UNIT_PRICE_8', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_9 = models.DecimalField(db_column='UNIT_PRICE_9', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_10 = models.DecimalField(db_column='UNIT_PRICE_10', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    default_unit_price = models.DecimalField(db_column='DEFAULT_UNIT_PRICE', max_digits=22, decimal_places=8)  # Field name made lowercase.
    unit_price_curr_1 = models.DecimalField(db_column='UNIT_PRICE_CURR_1', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_2 = models.DecimalField(db_column='UNIT_PRICE_CURR_2', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_3 = models.DecimalField(db_column='UNIT_PRICE_CURR_3', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_4 = models.DecimalField(db_column='UNIT_PRICE_CURR_4', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_5 = models.DecimalField(db_column='UNIT_PRICE_CURR_5', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_6 = models.DecimalField(db_column='UNIT_PRICE_CURR_6', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_7 = models.DecimalField(db_column='UNIT_PRICE_CURR_7', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_8 = models.DecimalField(db_column='UNIT_PRICE_CURR_8', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_9 = models.DecimalField(db_column='UNIT_PRICE_CURR_9', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_10 = models.DecimalField(db_column='UNIT_PRICE_CURR_10', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    def_unit_price_curr = models.DecimalField(db_column='DEF_UNIT_PRICE_CURR', max_digits=22, decimal_places=8)  # Field name made lowercase.
    minimum_charge = models.DecimalField(db_column='MINIMUM_CHARGE', max_digits=23, decimal_places=8)  # Field name made lowercase.
    base_charge = models.DecimalField(db_column='BASE_CHARGE', max_digits=23, decimal_places=8)  # Field name made lowercase.
    purchase_um = models.CharField(db_column='PURCHASE_UM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    quote_date = models.DateTimeField(db_column='QUOTE_DATE', blank=True, null=True)  # Field name made lowercase.
    long_description = models.BinaryField(db_column='LONG_DESCRIPTION', blank=True, null=True)  # Field name made lowercase.
    contract_id = models.CharField(db_column='CONTRACT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contract_line_no = models.SmallIntegerField(db_column='CONTRACT_LINE_NO', blank=True, null=True)  # Field name made lowercase.
    vendor_clin = models.CharField(db_column='VENDOR_CLIN', max_length=15, blank=True, null=True)  # Field name made lowercase.
    effective_date = models.DateTimeField(db_column='EFFECTIVE_DATE', blank=True, null=True)  # Field name made lowercase.
    expiration_date = models.DateTimeField(db_column='EXPIRATION_DATE', blank=True, null=True)  # Field name made lowercase.
    site = models.ForeignKey(Site, models.DO_NOTHING, db_column='SITE_ID')  # Field name made lowercase.
    leadtime_1 = models.SmallIntegerField(db_column='LEADTIME_1', blank=True, null=True)  # Field name made lowercase.
    leadtime_2 = models.SmallIntegerField(db_column='LEADTIME_2', blank=True, null=True)  # Field name made lowercase.
    leadtime_3 = models.SmallIntegerField(db_column='LEADTIME_3', blank=True, null=True)  # Field name made lowercase.
    leadtime_4 = models.SmallIntegerField(db_column='LEADTIME_4', blank=True, null=True)  # Field name made lowercase.
    leadtime_5 = models.SmallIntegerField(db_column='LEADTIME_5', blank=True, null=True)  # Field name made lowercase.
    leadtime_6 = models.SmallIntegerField(db_column='LEADTIME_6', blank=True, null=True)  # Field name made lowercase.
    leadtime_7 = models.SmallIntegerField(db_column='LEADTIME_7', blank=True, null=True)  # Field name made lowercase.
    leadtime_8 = models.SmallIntegerField(db_column='LEADTIME_8', blank=True, null=True)  # Field name made lowercase.
    leadtime_9 = models.SmallIntegerField(db_column='LEADTIME_9', blank=True, null=True)  # Field name made lowercase.
    leadtime_10 = models.SmallIntegerField(db_column='LEADTIME_10', blank=True, null=True)  # Field name made lowercase.
    default_leadtime = models.SmallIntegerField(db_column='DEFAULT_LEADTIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'VENDOR_SERV_QUOTE'
        unique_together = (('vendor_id', 'vendor_service_id', 'contract_id', 'contract_line_no', 'site'),)


class Units(TruncatedModel):
    unit_of_measure = models.CharField(db_column='UNIT_OF_MEASURE', primary_key=True, max_length=15)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=40, blank=True, null=True)  # Field name made lowercase.
    scale = models.SmallIntegerField(db_column='SCALE')  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=64, blank=True, null=True)  # Field name made lowercase.
    user_defined_uom = models.CharField(db_column='USER_DEFINED_UOM', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'UNITS'


class UserDefFields(TruncatedModel):
    rowid = models.AutoField(db_column='ROWID', primary_key=True)  # Field name made lowercase.
    program_id = models.CharField(db_column='PROGRAM_ID', max_length=30)  # Field name made lowercase.
    id = models.CharField(db_column='ID', max_length=30)  # Field name made lowercase.
    document_id = models.CharField(db_column='DOCUMENT_ID', max_length=254, blank=True, null=True)  # Field name made lowercase.
    line_no = models.IntegerField(db_column='LINE_NO', blank=True, null=True)  # Field name made lowercase.
    del_line_no = models.IntegerField(db_column='DEL_LINE_NO', blank=True, null=True)  # Field name made lowercase.
    label = models.CharField(db_column='LABEL', max_length=254, blank=True, null=True)  # Field name made lowercase.
    data_type = models.IntegerField(db_column='DATA_TYPE', blank=True, null=True)  # Field name made lowercase.
    display_format = models.CharField(db_column='DISPLAY_FORMAT', max_length=30, blank=True, null=True)  # Field name made lowercase.
    tab_or_table = models.IntegerField(db_column='TAB_OR_TABLE', blank=True, null=True)  # Field name made lowercase.
    tab_id = models.CharField(db_column='TAB_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    table_id = models.CharField(db_column='TABLE_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    sequence_no = models.IntegerField(db_column='SEQUENCE_NO', blank=True, null=True)  # Field name made lowercase.
    udf_required = models.IntegerField(db_column='UDF_REQUIRED', blank=True, null=True)  # Field name made lowercase.
    string_val = models.CharField(db_column='STRING_VAL', max_length=254, blank=True, null=True)  # Field name made lowercase.
    number_val = models.DecimalField(db_column='NUMBER_VAL', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    bool_val = models.IntegerField(db_column='BOOL_VAL', blank=True, null=True)  # Field name made lowercase.
    date_val = models.DateTimeField(db_column='DATE_VAL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'USER_DEF_FIELDS'
        unique_together = (('program_id', 'id', 'document_id', 'line_no', 'del_line_no'),)


class VendorQuote(TruncatedModel):
    rowid = models.AutoField(primary_key=True, db_column='ROWID')  # Field name made lowercase.
    vendor = models.ForeignKey(Vendor, models.DO_NOTHING, db_column='VENDOR_ID')  # Field name made lowercase.
    vendor_part_id = models.CharField(db_column='VENDOR_PART_ID', max_length=30)  # Field name made lowercase.
    mfg_name = models.CharField(db_column='MFG_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mfg_part_id = models.CharField(db_column='MFG_PART_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='CURRENCY_ID')  # Field name made lowercase.
    qty_break_1 = models.DecimalField(db_column='QTY_BREAK_1', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_2 = models.DecimalField(db_column='QTY_BREAK_2', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_3 = models.DecimalField(db_column='QTY_BREAK_3', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_4 = models.DecimalField(db_column='QTY_BREAK_4', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_5 = models.DecimalField(db_column='QTY_BREAK_5', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_6 = models.DecimalField(db_column='QTY_BREAK_6', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_7 = models.DecimalField(db_column='QTY_BREAK_7', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_8 = models.DecimalField(db_column='QTY_BREAK_8', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_9 = models.DecimalField(db_column='QTY_BREAK_9', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    qty_break_10 = models.DecimalField(db_column='QTY_BREAK_10', max_digits=20, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_1 = models.DecimalField(db_column='UNIT_PRICE_1', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_2 = models.DecimalField(db_column='UNIT_PRICE_2', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_3 = models.DecimalField(db_column='UNIT_PRICE_3', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_4 = models.DecimalField(db_column='UNIT_PRICE_4', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_5 = models.DecimalField(db_column='UNIT_PRICE_5', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_6 = models.DecimalField(db_column='UNIT_PRICE_6', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_7 = models.DecimalField(db_column='UNIT_PRICE_7', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_8 = models.DecimalField(db_column='UNIT_PRICE_8', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_9 = models.DecimalField(db_column='UNIT_PRICE_9', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_10 = models.DecimalField(db_column='UNIT_PRICE_10', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    default_unit_price = models.DecimalField(db_column='DEFAULT_UNIT_PRICE', max_digits=22, decimal_places=8)  # Field name made lowercase.
    unit_price_curr_1 = models.DecimalField(db_column='UNIT_PRICE_CURR_1', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_2 = models.DecimalField(db_column='UNIT_PRICE_CURR_2', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_3 = models.DecimalField(db_column='UNIT_PRICE_CURR_3', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_4 = models.DecimalField(db_column='UNIT_PRICE_CURR_4', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_5 = models.DecimalField(db_column='UNIT_PRICE_CURR_5', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_6 = models.DecimalField(db_column='UNIT_PRICE_CURR_6', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_7 = models.DecimalField(db_column='UNIT_PRICE_CURR_7', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_8 = models.DecimalField(db_column='UNIT_PRICE_CURR_8', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_9 = models.DecimalField(db_column='UNIT_PRICE_CURR_9', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unit_price_curr_10 = models.DecimalField(db_column='UNIT_PRICE_CURR_10', max_digits=22, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    def_unit_price_curr = models.DecimalField(db_column='DEF_UNIT_PRICE_CURR', max_digits=22, decimal_places=8)  # Field name made lowercase.
    purchase_um = models.ForeignKey(Units, models.DO_NOTHING, db_column='PURCHASE_UM', blank=True, null=True)  # Field name made lowercase.
    quote_date = models.DateTimeField(db_column='QUOTE_DATE', blank=True, null=True)  # Field name made lowercase.
    long_description = models.BinaryField(db_column='LONG_DESCRIPTION', blank=True, null=True)  # Field name made lowercase.
    contract_id = models.CharField(db_column='CONTRACT_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contract_line_no = models.SmallIntegerField(db_column='CONTRACT_LINE_NO', blank=True, null=True)  # Field name made lowercase.
    vendor_clin = models.CharField(db_column='VENDOR_CLIN', max_length=15, blank=True, null=True)  # Field name made lowercase.
    effective_date = models.DateTimeField(db_column='EFFECTIVE_DATE', blank=True, null=True)  # Field name made lowercase.
    expiration_date = models.DateTimeField(db_column='EXPIRATION_DATE', blank=True, null=True)  # Field name made lowercase.
    site = models.ForeignKey(Site, models.DO_NOTHING, db_column='SITE_ID')  # Field name made lowercase.
    leadtime_1 = models.SmallIntegerField(db_column='LEADTIME_1', blank=True, null=True)  # Field name made lowercase.
    leadtime_2 = models.SmallIntegerField(db_column='LEADTIME_2', blank=True, null=True)  # Field name made lowercase.
    leadtime_3 = models.SmallIntegerField(db_column='LEADTIME_3', blank=True, null=True)  # Field name made lowercase.
    leadtime_4 = models.SmallIntegerField(db_column='LEADTIME_4', blank=True, null=True)  # Field name made lowercase.
    leadtime_5 = models.SmallIntegerField(db_column='LEADTIME_5', blank=True, null=True)  # Field name made lowercase.
    leadtime_6 = models.SmallIntegerField(db_column='LEADTIME_6', blank=True, null=True)  # Field name made lowercase.
    leadtime_7 = models.SmallIntegerField(db_column='LEADTIME_7', blank=True, null=True)  # Field name made lowercase.
    leadtime_8 = models.SmallIntegerField(db_column='LEADTIME_8', blank=True, null=True)  # Field name made lowercase.
    leadtime_9 = models.SmallIntegerField(db_column='LEADTIME_9', blank=True, null=True)  # Field name made lowercase.
    leadtime_10 = models.SmallIntegerField(db_column='LEADTIME_10', blank=True, null=True)  # Field name made lowercase.
    default_leadtime = models.SmallIntegerField(db_column='DEFAULT_LEADTIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'VENDOR_QUOTE'
        unique_together = (('vendor', 'vendor_part_id', 'contract_id', 'contract_line_no', 'mfg_name', 'mfg_part_id', 'site'),)


class OperServiceCost(TruncatedModel):
    workorder_type = models.CharField(db_column='WORKORDER_TYPE', max_length=1)  # Field name made lowercase.
    workorder_base_id = models.CharField(db_column='WORKORDER_BASE_ID', max_length=30)  # Field name made lowercase.
    workorder_lot_id = models.CharField(db_column='WORKORDER_LOT_ID', max_length=3)  # Field name made lowercase.
    workorder_split_id = models.CharField(db_column='WORKORDER_SPLIT_ID', max_length=3)  # Field name made lowercase.
    workorder_sub_id = models.CharField(db_column='WORKORDER_SUB_ID', max_length=3)  # Field name made lowercase.
    operation_seq_no = models.SmallIntegerField(db_column='OPERATION_SEQ_NO')  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    unit_cost = models.DecimalField(db_column='UNIT_COST', max_digits=22, decimal_places=8)  # Field name made lowercase.
    base_charge = models.DecimalField(db_column='BASE_CHARGE', max_digits=23, decimal_places=8)  # Field name made lowercase.
    minimum_charge = models.DecimalField(db_column='MINIMUM_CHARGE', max_digits=23, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    leadtime = models.SmallIntegerField(db_column='LEADTIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'OPER_SERVICE_COST'
        unique_together = (('workorder_type', 'workorder_base_id', 'workorder_lot_id', 'workorder_split_id', 'workorder_sub_id', 'operation_seq_no', 'qty'),)


class HistoryData(TruncatedModel):
    user_id = models.CharField(db_column='USER_ID', max_length=20)  # Field name made lowercase.
    tbl_name = models.CharField(db_column='TBL_NAME', max_length=50)  # Field name made lowercase.
    col_name = models.CharField(db_column='COL_NAME', max_length=50)  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='CREATE_DATE')  # Field name made lowercase.
    primary_key = models.CharField(db_column='PRIMARY_KEY', max_length=254, primary_key=True, blank=True, null=True)  # Field name made lowercase.
    action = models.CharField(db_column='ACTION', max_length=15, blank=True, null=True)  # Field name made lowercase.
    old_value = models.CharField(db_column='OLD_VALUE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    new_value = models.CharField(db_column='NEW_VALUE', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'HISTORY_DATA'


class DemandSupplyLink(TruncatedModel):
    rowid = models.IntegerField(db_column='ROWID')  # Field name made lowercase.
    id = models.IntegerField(primary_key=True, db_column='ID')  # Field name made lowercase.
    demand_type = models.CharField(db_column='DEMAND_TYPE', max_length=2)  # Field name made lowercase.
    demand_base_id = models.CharField(db_column='DEMAND_BASE_ID', max_length=30)  # Field name made lowercase.
    demand_lot_id = models.CharField(db_column='DEMAND_LOT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    demand_split_id = models.CharField(db_column='DEMAND_SPLIT_ID', max_length=3, blank=True, null=True)  # Field name made lowercase.
    demand_sub_id = models.CharField(db_column='DEMAND_SUB_ID', max_length=3, blank=True, null=True)  # Field name made lowercase.
    demand_seq_no = models.IntegerField(db_column='DEMAND_SEQ_NO', blank=True, null=True)  # Field name made lowercase.
    demand_no = models.IntegerField(db_column='DEMAND_NO', blank=True, null=True)  # Field name made lowercase.
    supply_type = models.CharField(db_column='SUPPLY_TYPE', max_length=2)  # Field name made lowercase.
    supply_base_id = models.CharField(db_column='SUPPLY_BASE_ID', max_length=30)  # Field name made lowercase.
    supply_lot_id = models.CharField(db_column='SUPPLY_LOT_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    supply_split_id = models.CharField(db_column='SUPPLY_SPLIT_ID', max_length=3, blank=True, null=True)  # Field name made lowercase.
    supply_sub_id = models.CharField(db_column='SUPPLY_SUB_ID', max_length=3, blank=True, null=True)  # Field name made lowercase.
    supply_seq_no = models.IntegerField(db_column='SUPPLY_SEQ_NO', blank=True, null=True)  # Field name made lowercase.
    supply_no = models.IntegerField(db_column='SUPPLY_NO', blank=True, null=True)  # Field name made lowercase.
    warehouse_id = models.CharField(db_column='WAREHOUSE_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    demand_part_id = models.CharField(db_column='DEMAND_PART_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    supply_part_id = models.CharField(db_column='SUPPLY_PART_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    allocated_qty = models.DecimalField(db_column='ALLOCATED_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    received_qty = models.DecimalField(db_column='RECEIVED_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    issued_qty = models.DecimalField(db_column='ISSUED_QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    supply_mode = models.CharField(db_column='SUPPLY_MODE', max_length=1)  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='CREATE_DATE')  # Field name made lowercase.
    user_id = models.CharField(db_column='USER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    reallocate = models.CharField(db_column='REALLOCATE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    demand_site_id = models.CharField(db_column='DEMAND_SITE_ID', max_length=15)  # Field name made lowercase.
    supply_site_id = models.CharField(db_column='SUPPLY_SITE_ID', max_length=15)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Demand_Supply_Link'


class Country(TruncatedModel):
    rowid = models.IntegerField(db_column='ROWID')  # Field name made lowercase.
    id = models.CharField(primary_key=True, db_column='ID', max_length=15)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    intrastat_reqd = models.CharField(db_column='INTRASTAT_REQD', max_length=1)  # Field name made lowercase.
    intra_country_id = models.CharField(db_column='INTRA_COUNTRY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    esl_country_id = models.CharField(db_column='ESL_COUNTRY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    esl_country = models.CharField(db_column='ESL_COUNTRY', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Country'


class FinancialCalendar(TruncatedModel):
    rowid = models.IntegerField(db_column='ROWID')  # Field name made lowercase.
    id = models.CharField(primary_key=True, db_column='ID', max_length=15)  # Field name made lowercase.
    period_type = models.CharField(db_column='PERIOD_TYPE', max_length=1)  # Field name made lowercase.
    periods_per_year = models.SmallIntegerField(db_column='PERIODS_PER_YEAR')  # Field name made lowercase.
    fiscal_year_end_month = models.DecimalField(db_column='FISCAL_YEAR_END_MONTH', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    fiscal_year_end_day = models.DecimalField(db_column='FISCAL_YEAR_END_DAY', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=80, blank=True, null=True)  # Field name made lowercase.
    active_flag = models.CharField(db_column='ACTIVE_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Financial_Calendar'


class Region(TruncatedModel):
    id = models.CharField(db_column='ID', primary_key=True, max_length=2)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'REGION'


class LabelType(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LABEL_TYPE'


class LabelFormat(TruncatedModel):
    id = models.CharField(db_column='ID', primary_key=True, max_length=30)  # Field name made lowercase.
    label_type = models.ForeignKey('LabelType', models.DO_NOTHING, db_column='LABEL_TYPE_ID')  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=40, blank=True, null=True)  # Field name made lowercase.
    format_file_name = models.CharField(db_column='FORMAT_FILE_NAME', max_length=250, blank=True, null=True)  # Field name made lowercase.
    label_printer_id = models.SmallIntegerField(db_column='LABEL_PRINTER_ID', blank=True, null=True)  # Field name made lowercase.
    qty_to_print = models.SmallIntegerField(db_column='QTY_TO_PRINT', blank=True, null=True)  # Field name made lowercase.
    label_mult_flag = models.CharField(db_column='LABEL_MULT_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    site_id = models.CharField(db_column='SITE_ID', max_length=15)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'LABEL_FORMAT'


class LabelFormatField(TruncatedModel):
    column_id = models.CharField(db_column='COLUMN_ID', max_length=70)  # Field name made lowercase.
    label_field = models.CharField(db_column='LABEL_FIELD', primary_key=True, max_length=50)  # Field name made lowercase.
    label_format = models.ForeignKey(LabelFormat, models.DO_NOTHING, db_column='LABEL_FORMAT_ID')  # Field name made lowercase.
    site_id = models.CharField(db_column='SITE_ID', max_length=15)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'LABEL_FORMAT_FIELD'
        unique_together = (('label_field', 'label_format'),)


class Warehouse(TruncatedModel):
    id = models.CharField(db_column='ID', primary_key=True, max_length=15)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=80, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_1 = models.CharField(db_column='ADDR_1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_2 = models.CharField(db_column='ADDR_2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr_3 = models.CharField(db_column='ADDR_3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='CITY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='STATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(db_column='ZIPCODE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='COUNTRY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    region = models.ForeignKey(Region, models.DO_NOTHING, db_column='REGION_ID', blank=True, null=True)  # Field name made lowercase.
    country_0 = models.ForeignKey(Country, models.DO_NOTHING, db_column='COUNTRY_ID', blank=True, null=True)  # Field name made lowercase. Field renamed because of name conflict.
    warehouse_country_id = models.CharField(db_column='WAREHOUSE_COUNTRY_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vat_registration = models.CharField(db_column='VAT_REGISTRATION', max_length=25, blank=True, null=True)  # Field name made lowercase.
    wip_vas = models.CharField(db_column='WIP_VAS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    def_lbl_format = models.ForeignKey(LabelFormat, models.DO_NOTHING, db_column='DEF_LBL_FORMAT_ID', blank=True, null=True)  # Field name made lowercase.
    independent = models.CharField(db_column='INDEPENDENT', max_length=1)  # Field name made lowercase.
    vdw_installed = models.CharField(db_column='VDW_INSTALLED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inv_not_shared = models.CharField(db_column='INV_NOT_SHARED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    customer = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CUSTOMER_ID', blank=True, null=True)  # Field name made lowercase.
    vendor = models.ForeignKey(Vendor, models.DO_NOTHING, db_column='VENDOR_ID', blank=True, null=True)  # Field name made lowercase.
    consigned_type = models.CharField(db_column='CONSIGNED_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mrp_exempt = models.CharField(db_column='MRP_EXEMPT', max_length=1)  # Field name made lowercase.
    site = models.ForeignKey(Site, models.DO_NOTHING, db_column='SITE_ID')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'WAREHOUSE'


class PartLocation(TruncatedModel):
    rowid = models.AutoField(primary_key=True, db_column='ROWID')
    part = models.ForeignKey(Part, models.DO_NOTHING, db_column='PART_ID')  # Field name made lowercase.
    warehouse = models.ForeignKey(Warehouse, models.DO_NOTHING, db_column='WAREHOUSE_ID')  # Field name made lowercase.
    location = models.ForeignKey(Location, models.DO_NOTHING, db_column='LOCATION_ID')  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=80, blank=True,
                                   null=True)  # Field name made lowercase.
    hold_reason = models.ForeignKey(HoldReason, models.DO_NOTHING, db_column='HOLD_REASON_ID', blank=True,
                                    null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=20, decimal_places=8)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1)  # Field name made lowercase.
    locked = models.CharField(db_column='LOCKED', max_length=1)  # Field name made lowercase.
    transit = models.CharField(db_column='TRANSIT', max_length=1)  # Field name made lowercase.
    last_count_date = models.DateTimeField(db_column='LAST_COUNT_DATE', blank=True,
                                           null=True)  # Field name made lowercase.
    purge_qty = models.DecimalField(db_column='PURGE_QTY', max_digits=20, decimal_places=8, blank=True,
                                    null=True)  # Field name made lowercase.
    committed_qty = models.DecimalField(db_column='COMMITTED_QTY', max_digits=20,
                                        decimal_places=8)  # Field name made lowercase.
    def_backflush_loc = models.CharField(db_column='DEF_BACKFLUSH_LOC', max_length=1)  # Field name made lowercase.
    auto_issue_loc = models.CharField(db_column='AUTO_ISSUE_LOC', max_length=1)  # Field name made lowercase.
    def_inspect_loc = models.CharField(db_column='DEF_INSPECT_LOC', max_length=1)  # Field name made lowercase.
    dc_class_id = models.CharField(db_column='DC_CLASS_ID', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    order_point = models.DecimalField(db_column='ORDER_POINT', max_digits=20, decimal_places=8, blank=True,
                                      null=True)  # Field name made lowercase.
    order_up_to_qty = models.DecimalField(db_column='ORDER_UP_TO_QTY', max_digits=20, decimal_places=8, blank=True,
                                          null=True)  # Field name made lowercase.
    status_eff_date = models.DateTimeField(db_column='STATUS_EFF_DATE')  # Field name made lowercase.
    from_hold_reason_id = models.CharField(db_column='FROM_HOLD_REASON_ID', max_length=15, blank=True,
                                           null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'PART_LOCATION'
        unique_together = (('part', 'warehouse', 'location'),)


class UnitsConversion(TruncatedModel):
    from_um = models.OneToOneField(Units, models.DO_NOTHING, db_column='FROM_UM', primary_key=True)  # Field name made lowercase.
    to_um = models.CharField(db_column='TO_UM', max_length=15)  # Field name made lowercase.
    conversion_factor = models.DecimalField(db_column='CONVERSION_FACTOR', max_digits=15, decimal_places=8)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'UNITS_CONVERSION'
        unique_together = (('from_um', 'to_um'),)


class RequirementBinary(TruncatedModel):  # Field name made lowercase.
    rowid = models.AutoField(primary_key=True, db_column='ROWID')
    workorder_type = models.CharField(db_column='WORKORDER_TYPE', max_length=1)  # Field name made lowercase.
    workorder_base_id = models.CharField(db_column='WORKORDER_BASE_ID', max_length=30)  # Field name made lowercase.
    workorder_lot_id = models.CharField(db_column='WORKORDER_LOT_ID', max_length=3)  # Field name made lowercase.
    workorder_split_id = models.CharField(db_column='WORKORDER_SPLIT_ID', max_length=3)  # Field name made lowercase.
    workorder_sub_id = models.CharField(db_column='WORKORDER_SUB_ID', max_length=3)  # Field name made lowercase.
    operation_seq_no = models.SmallIntegerField(db_column='OPERATION_SEQ_NO')  # Field name made lowercase.
    piece_no = models.SmallIntegerField(db_column='PIECE_NO')  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1)  # Field name made lowercase.
    bits = models.BinaryField(db_column='BITS', blank=True, null=True)  # Field name made lowercase.
    bits_length = models.IntegerField(db_column='BITS_LENGTH')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'REQUIREMENT_BINARY'
        unique_together = (('workorder_type', 'workorder_base_id', 'workorder_lot_id', 'workorder_split_id', 'workorder_sub_id', 'operation_seq_no', 'piece_no', 'type'),)
