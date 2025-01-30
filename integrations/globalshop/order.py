import datetime
import decimal
from typing import NamedTuple, Union
from baseintegration.utils.data import sqlize_value, sqlize_str
from globalshop.client import GlobalShopClient


class OrderLineRecord(NamedTuple):
    external_order_no: str
    transaction_code: str
    gss_customer_no: str
    external_customer_no: str
    order_no: str
    line_number: int
    linetype: str
    gss_partnumber: str
    ext_partnumber: str
    qty_ordered: Union[decimal.Decimal, int]
    line_total_price: decimal.Decimal
    line_unit_price: decimal.Decimal
    price_before_discount: decimal.Decimal
    # order_discount_percent:decimal.Decimal
    part_loc: str
    order_due_date: datetime.date
    # Defaults to today
    order_date: datetime.date
    # only if different from order_date
    line_order_date: datetime.date
    line_promise_date: datetime.date
    freight: decimal.Decimal
    # freight_per_piece:decimal.Decimal
    user_field_1_head: str
    user_field_2_head: str
    user_field_3_head: str
    user_field_4_head: str
    user_field_5_head: str
    ship_via: str
    carrier: str
    # default empty
    ship_to_id: str
    # default False
    ship_to_intl_flag: bool
    ship_to_name: str
    ship_to_address_1: str
    ship_to_address_2: str
    ship_to_address_3: str
    ship_to_city: str
    ship_to_state: str
    ship_to_zip: str
    ship_to_country: str
    ship_to_attention: str
    ship_to_contact_name: str
    ship_to_contact_email: str
    bill_to_intl_flag: bool
    bill_to_name: str
    bill_to_address_1: str
    bill_to_address_2: str
    bill_to_address_3: str
    bill_to_city: str
    bill_to_state: str
    bill_to_zip: str
    bill_to_country: str
    bill_to_attention: str
    order_sort: str
    order_sort_2: str
    user_field_1_line: str
    user_field_2_line: str
    user_field_3_line: str
    user_field_4_line: str
    user_field_5_line: str
    addl_comments_head: str
    addl_comments_line: str
    customer_po: str
    order_loc: str
    # defaults to False
    # prosepect:bool
    # line_taxes:decimal.Decimal
    salesperson_code: str
    line_unit_cost: decimal.Decimal
    part_description: str
    terms: str
    # markshipment:?
    # Default False
    # shiphold:bool
    part_um: str
    quote_status: str
    approved: bool
    commission_type_code: str
    customer_part: str
    ship_to_address_4: str
    ship_to_address_5: str
    salesperson_code: str


class OrderLine:

    @classmethod
    def insert(cls, external_order_no: str,
               gss_customer_no: str,
               ext_customer_no: str,
               line_number: int,
               gss_part_number: str,
               ext_part_number: str,
               qty_ordered: Union[decimal.Decimal, int],
               line_total_price: decimal.Decimal,
               line_unit_price: decimal.Decimal,
               order_due_date: str = '',
               order_date: str = '',
               line_order_date: str = '',
               line_promise_date: str = '',
               part_loc: str = '',
               ship_to_id: str = '',
               ship_to_name: str = '',
               ship_to_address_1: str = '',
               ship_to_address_2: str = '',
               ship_to_city: str = '',
               ship_to_state: str = '',
               ship_to_zip: str = '',
               ship_to_country: str = '',
               ship_to_attention: str = '',
               ship_to_contact_name: str = '',
               ship_to_contact_email: str = '',
               bill_to_name: str = '',
               bill_to_address_1: str = '',
               bill_to_address_2: str = '',
               bill_to_address_3: str = '',
               bill_to_city: str = '',
               bill_to_state: str = '',
               bill_to_zip: str = '',
               bill_to_country: str = '',
               bill_to_attention: str = '',
               user_field_1_line: str = '',
               user_field_2_line: str = '',
               user_field_3_line: str = '',
               user_field_4_line: str = '',
               user_field_5_line: str = '',
               customer_po: str = '',
               order_loc: str = '',
               part_description: str = '',
               customer_part: str = '',
               salesperson_code: str = '',
               batch_process=True
               ) -> OrderLineRecord:
        # transaction_code: str = 'O', line_type: str = 'S') -> \

        """
        Insert an order line into the staging table. Each line includes all the
        header data as well, so any of them could be used to build the header
        by the GS GAB importer

        """

        # if not gss_customer_no:

        # TRANSACTIONCODE,
        # {sqlize_str(transaction_code)},

        # LINETYPE,
        # {sqlize_str(line_type)},

        sql_cmd = f"""INSERT INTO GCG_5807_ORDER_STAGE (ORDER_NO_EXTERNAL,
        GSS_CUSTOMERNO,
        EXT_CUSTOMERNO,
        LINENUMBER,
        GSS_PARTNUMBER,
        EXT_PARTNUMBER,
        QTYORDERED,
        LINETOTALPRICE,
        LINEUNITPRICE,
        PARTLOC,
        ORDERDUEDATE,
        ORDERDATE,
        LINEORDERDATE,
        LINEPROMISEDATE,
        SHIPTOID,
        SHIPTOADDRESS1,
        SHIPTOADDRESS2,
        SHIPTOCITY,
        SHIPTOSTATE,
        SHIPTOZIP,
        SHIPTOCOUNTRY,
        SHIPTOCONTACTNAME,
        SHIPTOCONTACTEMAIL,
        USERFIELD4LINE,
        CUSTOMERPO,
        ORDERLOCATION,
        PARTDESCRIPTION,
        CUSTOMER_PART,
        SalespersonCode,
        DELETE_ORDER
        )
        VALUES ({sqlize_str(external_order_no)},
        {sqlize_str(gss_customer_no)},
        {sqlize_str(ext_customer_no)},
        {sqlize_value(line_number)},
        {sqlize_str(gss_part_number)},
        {sqlize_str(ext_part_number)},
        {sqlize_value(qty_ordered)},
        {sqlize_value(line_total_price)},
        {sqlize_value(line_unit_price)},
        {sqlize_str(part_loc)},
        {sqlize_str(order_due_date)},
        {sqlize_str(order_date)},
        {sqlize_str(line_order_date)},
        {sqlize_str(line_promise_date)},
        {sqlize_str(ship_to_id)},
        {sqlize_str(ship_to_address_1)},
        {sqlize_str(ship_to_address_2)},
        {sqlize_str(ship_to_city)},
        {sqlize_str(ship_to_state)},
        {sqlize_str(ship_to_zip)},
        {sqlize_str(ship_to_country)},
        {sqlize_str(ship_to_contact_name)},
        {sqlize_str(ship_to_contact_email)},
        {sqlize_str(user_field_4_line)},
        {sqlize_str(customer_po)},
        {sqlize_str(order_loc)},
        {sqlize_str(part_description)},
        {sqlize_str(customer_part)},
        {sqlize_str(salesperson_code)},
        0
        )"""
        # f",'{web_address}',{credit_limit}," # f"{'true' if set_credit_hold
        # else 'false'},{'true' if set_shipping_hold else 'false'},
        # " f"'{salesperson_code}','{currency_code}','{order_notes}',
        # '{terms}'" # f",{'true' if credit_hold else 'false'}" )
        # print(sql_cmd)
        client: GlobalShopClient = GlobalShopClient.get_instance()

        if batch_process:
            client.cache(sql_cmd=sql_cmd)
        else:
            cursor = client.cursor()
            cursor.execute(sql_cmd)
            # row = cursor.fetchone()
            cursor.commit()
            cursor.close()
