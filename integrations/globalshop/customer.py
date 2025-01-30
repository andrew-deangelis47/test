import decimal
from typing import NamedTuple, List

from baseintegration.integration import logger
from globalshop.client import GlobalShopClient
from decimal import Decimal
from baseintegration.utils.data import safe_trim


# Using a Named Tuple to represent an immutable state of data rather than a
# true class, as this will not have a save(), create(), delete() interface
# that relies on updating fields

class CustomerRecord(NamedTuple):
    # This is the PP account_id only used on the INSERT as a cached value
    account_id: int
    gss_customer_number: str
    customer_name: str
    address_1: str
    address_2: str
    city: str
    state: str
    zip: str
    country: str
    phone: str
    # FIXME: THis is actually a foreign key, and not necessarily a numeric
    #  value
    # credit_limit: decimal.Decimal
    credit_limit: str
    salesperson_code: str
    terms: str
    credit_hold: bool


# SELECT cm.CUST, cm.TYPE, cm.ID, cm.NAME, cm.SEQ, cm.NAME_PREFIX,
# cm.NAME_FIRST, cm.NAME_MID_INT, cm.NAME_LAST, cm.NAME_PREFERRED,
# cm.NAME_SUFFIX, cm.PHONE_T1, cm.PHONE_T2, cm.PHONE_T3, cm.PHONE_T4,
# cm.PHONE1, cm.PHONE2, cm.PHONE3, cm.PHONE4, cm.EXT1, cm.EXT2, cm.EXT3,
# cm.EXT4, cm.FAX1, cm.FAX2, cm.FAX3, cm.FAX4, cm.TITLE, cm.JOB_FUNCTION,
# cm.EMAIL1, cm.EMAIL2, cm.EMAIL_T1, cm.EMAIL_T2, cm.ACTIVE, cm.AFFILIATION,
# cm.BIRTHDAY, cm.SPOUSE, cm.JOB_MGR, cm.JOB_ASST_MGR, cm.ADDRESS_1,
# cm.ADDRESS_2, cm.CITY, cm.STATE, cm.ZIP, cm.ADDRESS2_DESC, cm.ADDRESS2_1,
# cm.ADDRESS2_2, cm.CITY2, cm.STATE2, cm.ZIP2, cm.FC0, cm.FC1, cm.USER_1,
# cm.USER_2, cm.USER_3, cm.USER_4, cm.USER_5, cm.DATE_SYNC, cm.TIME_SYNC,
# cm.PRI_ADDRESS, cm.ALT_ID, cm.PRI_CNTCT, cm.LAST_CHG_DATE,
# cm.LAST_CHG_TIME, cm.LAST_CHG_PGM, cm.LAST_CHG_BY from V_CONTACT as cm

class Customer:

    @classmethod
    def get(cls, cus_id: str) -> CustomerRecord:
        """
        :param cus_id: 6 character unique string identifier of a customer
        record.
        :return: CustomerRecord that matches the customer id, else None
        """

        # Removed cm.FLAG_the_STATE,
        sql_cmd = f"""SELECT cm.CUSTOMER, cm.REC, cm.NAME_CUSTOMER,
        cm.ADDRESS1, cm.ADDRESS2, cm.CITY, cm.STATE, cm.ZIP, cm.COUNTRY,
        cm.COUNTY, cm.ATTENTION, cm.SALESPERSON, cm.INTL_ADDR, cm.TERRITORY,
        cm.CODE_AREA, cm.CREDIT, cm.TELEPHONE, cm.CRM_RES_LEV,
        cm.ASSGN_USR_GRP, cm.NORMAL_GL_ACCOUNT, cm.FLAG_BALANCE_FWD,
        cm.FLAG_CREDIT_HOLD, cm.CHANGE_MODE,
        cm.INTERCOMPANY from V_CUSTOMER_MASTER as cm where cm.CUSTOMER =
        '{cus_id}'
        """

        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()
        cursor.execute(sql_cmd)
        row = cursor.fetchone()
        cursor.commit()
        cursor.close()

        if row is None:
            return None
        logger.debug(row)
        (customer_id, rec, cust_name, addr1, addr2, city, state, zip,
         country,
         county, attn, salesperson, intl, terr, code_area, credit, phone,
         crm_res_lev, assgn_usr_grp, normal_gl_acct, flag_balance_fwd,
         # flag_print_state,
         flag_credit_hold, change_mode, intercompany) = row

        cus = CustomerRecord(
            # TODO: I think the PP external ID can be stored elsewhere, but we
            #  don't use ATM.
            account_id=None,
            gss_customer_number=safe_trim(customer_id),
            customer_name=safe_trim(cust_name), address_1=safe_trim(addr1),
            address_2=safe_trim(addr2), city=safe_trim(city),
            state=safe_trim(state), zip=safe_trim(zip),
            country=safe_trim(country), phone=safe_trim(phone),
            salesperson_code=safe_trim(salesperson),
            credit_hold=flag_credit_hold,
            credit_limit=credit,
            # TODO: Terms are not actually stored in V_CUSTOMER_MASTER,
            #  need a new SELECT to get if needed later
            terms=None
        )
        return cus

    @classmethod
    def select_ids(cls, where=None) -> List[str]:
        """
        Select all customer IDs
        :return: An iterable of string customer IDs
        """
        sql_cmd = """SELECT cm.CUSTOMER from V_CUSTOMER_MASTER cm INNER JOIN V_CUSTOMER_SALES css ON cm.CUSTOMER = css.CUSTOMER"""
        if where:
            sql_cmd += f" WHERE {where}"
        logger.info(sql_cmd)
        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()
        cursor.execute(sql_cmd)
        rows = cursor.fetchall()
        ids = [row[0] for row in rows]

        cursor.commit()
        cursor.close()
        logger.debug(f'customer ids selected: {ids}')
        return ids

    @classmethod
    def select(cls) -> [CustomerRecord]:
        """
        Select all customer records
        :return: A list of CustomerRecords
        """

        customers = []

        sql_cmd = """SELECT cm.CUSTOMER, cm.REC, cm.NAME_CUSTOMER,
        cm.ADDRESS1, cm.ADDRESS2, cm.CITY, cm.STATE, cm.ZIP, cm.COUNTRY,
        cm.COUNTY, cm.ATTENTION, cm.SALESPERSON, cm.INTL_ADDR, cm.TERRITORY,
        cm.CODE_AREA, cm.CREDIT, cm.TELEPHONE, cm.CRM_RES_LEV,
        cm.ASSGN_USR_GRP, cm.NORMAL_GL_ACCOUNT, cm.FLAG_BALANCE_FWD,
        cm.FLAG_PRINT_STATE, cm.FLAG_CREDIT_HOLD, cm.CHANGE_MODE,
        cm.INTERCOMPANY from V_CUSTOMER_MASTER as cm """
        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()
        cursor.execute(sql_cmd)

        # row = cursor.fetchone()
        rows = cursor.fetchall()
        # while row is not None:
        for row in rows:
            (customer_id, rec, cust_name, addr1, addr2, city, state, zip,
             country, county, attn, salesperson, intl, terr, code_area,
             credit,
             phone, crm_res_lev, assgn_usr_grp, normal_gl_acct,
             flag_balance_fwd,
             # flag_print_state,
             flag_credit_hold,
             change_mode,
             intercompany) = row
            cust = CustomerRecord(
                account_id=None, gss_customer_number=safe_trim(customer_id),
                customer_name=safe_trim(cust_name), address_1=safe_trim(addr1),
                address_2=safe_trim(addr2), city=safe_trim(city),
                state=safe_trim(state), zip=safe_trim(zip),
                country=safe_trim(country), phone=safe_trim(phone),
                salesperson_code=safe_trim(salesperson),
                credit_hold=flag_credit_hold,
                credit_limit=decimal.Decimal(credit) if credit else None,
                terms=None

            )
            customers.append(cust)

            # row = cursor.fetchone()

        cursor.commit()
        cursor.close()
        return customers

    @classmethod
    def insert_customer(cls, account_id: str, gss_customer_number: int,
                        customer_name: str, address_1: str,
                        address_2: str,
                        city: str, state: str, zip: str, country: str,
                        phone: str, ship_address_1: str,
                        ship_address_2: str,
                        ship_city: str, ship_state: str, ship_zip: str,
                        ship_country: str, web_address: str,
                        credit_limit: Decimal, salesperson_code: str,
                        currency_code: str, order_notes: str, terms: str,
                        credit_hold: str, set_credit_hold: bool = True,
                        set_shipping_hold: bool = True) -> CustomerRecord:
        """
        :param account_id: unique Paperless Parts account id
        """
        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()

        # https: // stackoverflow.com / questions / 9336270 / using - a -
        # python - dict - for -a - sql - insert - statement
        # cursor.execute(
        # f"INSERT INTO GCG_5807_CUST_STAGE (EXTERNAL_CUSTOMER_ID,
        # GSS_CUSTOMER_NUMBER, CUSTOMER_NAME, ADDRESS_1, " f"ADDRESS_2,
        # CITY, STATE, ZIP, COUNTRY,PHONE,SHIP_ADDRESS_1,SHIP_ADDRESS_2,
        # SHIP_CITY,SHIP_STATE,SHIP_ZIP," f"SHIP_COUNTRY, WEB_ADDRESS,
        # CREDIT_LIMIT," # f"SET_CREDIT_HOLD,SET_SHIPPING_HOLD,
        # " f"SALESPERSON_CODE," f"CURRENCY_CODE, ORDER_NOTES,TERMS,
        # " # f"CREDIT_HOLD" f") " f"VALUES ('{account_id}',
        # '{gss_customer_number}','{customer_name}','{address_1}',
        # '{address_2}'," f"'{city}','{state}','{zip}','{country}',
        # '{phone}'," f"'{ship_address_1}','{ship_address_2}','{ship_city}',
        # '{ship_state}','{ship_zip}', '{ship_country}'" f",'{web_address}',
        # {credit_limit}," # f"{'true' if set_credit_hold else 'false'},
        # {'true' if set_shipping_hold else 'false'}," f"'{
        # salesperson_code}','{currency_code}','{order_notes}','{terms}'" #
        # f",{'true' if credit_hold else 'false'}" f")" )

        sql_cmd = f"""INSERT INTO GCG_5807_CUST_STAGE (EXTERNAL_CUSTOMER_ID,
        GSS_CUSTOMER_NUMBER, CUSTOMER_NAME,
        ADDRESS_1, ADDRESS_2, CITY, STATE, ZIP, COUNTRY, PHONE, SHIP_ADDRESS_1,
        SHIP_ADDRESS_2, SHIP_CITY, SHIP_STATE,
        SHIP_ZIP, SHIP_COUNTRY,WEB_ADDRESS,CREDIT_LIMIT)
        VALUES ('{account_id}','{gss_customer_number}','{customer_name}',
        '{address_1}','{address_2}',
        '{city}','{state}','{zip}','{country}','{phone}',
        '{ship_address_1}','{ship_address_2}','{ship_city}','{ship_state}',
        '{ship_zip}', '{ship_country}'
        ,'{web_address}',{credit_limit}
        )"""
        # f",'{web_address}',{credit_limit}," # f"{'true' if set_credit_hold
        # else 'false'},{'true' if set_shipping_hold else 'false'},
        # " f"'{salesperson_code}','{currency_code}','{order_notes}',
        # '{terms}'" # f",{'true' if credit_hold else 'false'}" )
        # logger.debug(sql_cmd)
        cursor.execute(sql_cmd)
        cursor.commit()
        cursor.close()
        return CustomerRecord(account_id=account_id,
                              gss_customer_number=None,
                              customer_name=customer_name,
                              address_1=address_1, address_2=address_2,
                              city=city, state=state, zip=zip,
                              country=country, phone=phone,
                              # ship_address_1=ship_address_1,
                              # ship_address_2=ship_address_2,
                              # ship_city=ship_city, ship_state=ship_state,
                              # ship_zip=ship_zip,
                              # ship_country=ship_country,
                              # web_address=web_address,
                              credit_limit=credit_limit,
                              salesperson_code=salesperson_code,
                              # currency_code=currency_code,
                              # order_notes=order_notes,
                              terms=terms,
                              credit_hold=credit_hold,
                              # set_credit_hold=set_credit_hold,
                              # set_shipping_hold=set_shipping_hold
                              )


class CustomerShipToRecord(NamedTuple):
    customer: str
    name_customer_ship: str
    address1: str
    address2: str
    city: str
    state: str
    zip: str
    country: str
    attention: str
    # Ship SEQ is the 6 character numeric unique identifier to sepecify the
    # order the ship to address appear on the SHip to Screen in GS. We use
    # it as the unique ID of the Facility in PP using the erp_code
    ship_seq: str


class CustomerShipTo:

    @classmethod
    def select(cls, customer_id: str) -> List[CustomerShipToRecord]:
        """
        Get the ship_tos for a given customer
        """
        # sql_cmd = f"SELECT CUSTOMER, NAME_CUSTOMER_SHIP, ADDRESS1_SHIP," \
        #           f"ADDRESS2_SHIP,CITY_SHIP,STATE_SHIP,CODE_ZIP_SHIP, " \
        #           f"COUNTRY_SHIP,ATTENTION_SHIP FROM " \
        #           f"V_CUSTOMER_SHIPTO WHERE " \
        #           f"CUSTOMER='{customer_id}'"
        sql_cmd = f"SELECT CUSTOMER, CUSTOMER_NAME, SHIP_ADDRESS1," \
                  f"SHIP_ADDRESS2,SHIP_CITY,SHIP_STATE,SHIP_ZIP, " \
                  f"SHIP_COUNTRY,SHIP_ATTENTION, SHIP_SEQ FROM " \
                  f"V_OE_MULTI_SHIP WHERE " \
                  f"CUSTOMER='{customer_id}'"
        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()
        cursor.execute(sql_cmd)
        rows = cursor.fetchall()
        cursor.commit()
        cursor.close()

        results = []
        for row in rows:
            # There are lots of extra spaces in the values returned, need to
            # strip them out.
            row = (safe_trim(val) for val in row)
            st_rec = CustomerShipToRecord(*row)
            results.append(st_rec)
        return results


class ContactRecord(NamedTuple):
    customer_id: str
    contact_type: str
    contact_id: str
    name: str
    first_name: str
    last_name: str
    phone1: str
    ext1: str
    title: str
    job_function: str
    email1: str


class Contact:
    @classmethod
    def select(cls, customer_id: str = None) -> [ContactRecord]:
        # sql_cmd = 'SELECT cm.CUST, cm.TYPE, cm.ID, cm.NAME, cm.SEQ, ' \
        #           'cm.NAME_PREFIX, cm.NAME_FIRST, cm.NAME_MID_INT, ' \
        #           'cm.NAME_LAST, cm.NAME_PREFERRED, cm.NAME_SUFFIX, ' \
        #           'cm.PHONE_T1, cm.PHONE_T2, cm.PHONE_T3, cm.PHONE_T4,' \
        #           'cm.PHONE1, cm.PHONE2, cm.PHONE3, cm.PHONE4, cm.EXT1,'\
        #           'cm.EXT2, cm.EXT3, cm.EXT4, cm.FAX1, cm.FAX2, ' \
        #           'cm.FAX3, ' \
        #           'cm.FAX4, cm.TITLE, cm.JOB_FUNCTION, cm.EMAIL1, ' \
        #           'cm.EMAIL2, cm.EMAIL_T1, cm.EMAIL_T2, cm.ACTIVE, ' \
        #           'cm.AFFILIATION, cm.BIRTHDAY, cm.SPOUSE, cm.JOB_MGR, '\
        #           'cm.JOB_ASST_MGR, cm.ADDRESS_1, cm.ADDRESS_2, ' \
        #           'cm.CITY, ' \
        #           'cm.STATE, cm.ZIP, cm.ADDRESS2_DESC, cm.ADDRESS2_1, ' \
        #           'cm.ADDRESS2_2, cm.CITY2, cm.STATE2, cm.ZIP2, cm.FC0,'\
        #           'cm.FC1, cm.USER_1, cm.USER_2, cm.USER_3, cm.USER_4, '\
        #           'cm.USER_5, cm.DATE_SYNC, cm.TIME_SYNC, ' \
        #           'cm.PRI_ADDRESS, cm.ALT_ID, cm.PRI_CNTCT, ' \
        #           'cm.LAST_CHG_DATE, cm.LAST_CHG_TIME, cm.LAST_CHG_PGM,'\
        #           'cm.LAST_CHG_BY from V_CONTACT as cm '
        sql_cmd = 'SELECT cm.CUST, cm.TYPE, cm.ID, cm.NAME, cm.NAME_FIRST, ' \
                  'cm.NAME_LAST, ' \
                  'cm.PHONE1, cm.EXT1, ' \
                  'cm.TITLE, cm.JOB_FUNCTION, cm.EMAIL1 ' \
                  'from V_CONTACT as cm '
        if customer_id:
            sql_cmd += f" WHERE cm.CUST = '{customer_id}' AND cm.TYPE = 'C'"
        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()
        cursor.execute(sql_cmd)
        rows = cursor.fetchall()
        cursor.commit()
        cursor.close()

        contacts = []
        for row in rows:
            # There are lots of extra spaces in the values returned, need to
            # strip them out.
            row = (safe_trim(val) for val in row)

            (customer_id,
             contact_type,
             contact_id,
             name,
             first,
             last,
             phone1,
             ext1,
             title,
             job_function,
             email1) = row

            contact_record = ContactRecord(customer_id=customer_id,
                                           contact_type=contact_type,
                                           contact_id=contact_id, name=name,
                                           first_name=first, last_name=last,
                                           phone1=phone1, ext1=ext1,
                                           title=title,
                                           job_function=job_function,
                                           email1=email1)
            contacts.append(contact_record)
        return contacts

    @classmethod
    def select_customer_ids(cls, where=None) -> List[str]:
        """
        Select customer IDs from contacts
        :return: An iterable of string customer IDs
        """
        sql_cmd = """SELECT DISTINCT cm.CUST from V_CONTACT cm WHERE cm.TYPE = 'C'"""

        if where:
            sql_cmd += f" AND {where}"
        logger.info(sql_cmd)
        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()
        cursor.execute(sql_cmd)
        rows = cursor.fetchall()
        ids = [row[0] for row in rows]

        cursor.commit()
        cursor.close()
        logger.debug(f'customer ids selected: {ids}')
        return ids
