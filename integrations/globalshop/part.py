import decimal

from baseintegration.utils.data import sqlize_str, sqlize_value, sqlize_bool
from typing import List, Optional

from globalshop.client import GlobalShopClient
from baseintegration.integration import logger
from collections import namedtuple

# Using a Named Tuple to represent an immutable state of data rather than a
# true class, as this will not have a save(), create(), delete() interface that
# relies on updating fields
part_record_field_names = (
    'part', 'product_line', 'description', 'um_purchasing', 'um_inventory',
    'amt_cost', 'date_last_usage', 'amt_price', 'code_sort', 'date_last_audit', 'qty_on_hand',
    'prim_dim', 'sec_dim', 'on_order_po', 'date_exception', 'amt_alt_cost', 'date_last_chg',
    'time_last_change', 'who_chg_last', 'trm_chg_last', 'length_raw_matl',
    'width_raw_matl', 'density_raw_matl', 'code_rm_shape', 'qty_last_onhand',
    'date_last_verify', 'flag_inactive', 'description_2', 'description_3', 'amt_cost_1', 'amt_cost_2',
    'amt_cost_3', 'date_cycle', 'lifo_base', 'six_decimal_cost', 'wt_per_foot',
    'cutting_charge', 'length', 'width', 'warranty_type', 'prop_code',
    'issue_um', 'matl_schrg_date', 'part_create_date', 'cost_date',
    'thickness', 'part_create_user', 'use_dimension_calc', 'extra_description', 'inactive')
PartRecord = namedtuple('PartRecord', part_record_field_names)


class Part:
    """
    This is an abstraction of the Inventory Master tables we are able to pull
    data from:
    - V_INVENTORY_MSTR
    - V_INVENTORY_MST2
    - V_INVENTORY_MST3

    We have not mapped every possible field, but have added the ones we need
    over time.

    To add a part, this is done by inserting into the staging table:
    CGC_5807_PART_STAGE
    """

    @staticmethod
    def select_ids(where=None) -> List[str]:
        """
        Select all part IDs
        :return: An iterable of string part IDs
        """
        sql_cmd = """SELECT PART from V_INVENTORY_MSTR"""
        if where:
            sql_cmd += f" WHERE {where}"
        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()
        logger.info(f'running sql: {sql_cmd}')
        cursor.execute(sql_cmd)
        rows = cursor.fetchall()
        ids = [row[0] for row in rows]

        cursor.commit()
        cursor.close()
        # logger.debug(f'part ids selected: {ids}')
        return ids

    @staticmethod
    def select(product_line: str = None) -> [PartRecord]:
        """
        Select part data using the provided kwargs as filters. Return a list of
        PartRecords as the results.

        :param product_line  - 'PP' == Purchased Parts, 'RM' == Raw materials,
                        'FG' == Finished Good:
        """

        # This select is explicity setting every column of the 3 views so we
        # can guarantee the position of the data in each row, and if we want to
        # add more fields to the Named Tuple result later we can do so without
        # affecting the index used for the previous values.
        select_cmd = ("SELECT m.PART, m.LOCATION, m.CODE_ABC,"
                      "m.PRODUCT_LINE, m.BIN, m.DESCRIPTION, m.UM_PURCHASING,"
                      "m.UM_INVENTORY, m.FACTOR_CONVERSION, m.QTY_ORDER, "
                      "m.QTY_SAFETY,"
                      "m.QTY_ONHAND, m.QTY_REORDER, m.QTY_ONORDER_PO, "
                      "m.QTY_ONORDER_WO,"
                      "m.QTY_REQUIRED, m.AMT_COST, m.QTY_USAGE_MO_01, "
                      "m.QTY_USAGE_MO_02,"
                      "m.QTY_USAGE_MO_03, m.QTY_USAGE_MO_04, "
                      "m.QTY_USAGE_MO_05, "
                      "m.QTY_USAGE_MO_06, m.QTY_USAGE_MO_07, "
                      "m.QTY_USAGE_MO_08, "
                      "m.QTY_USAGE_MO_09, m.QTY_USAGE_MO_10, "
                      "m.QTY_USAGE_MO_11, "
                      "m.QTY_USAGE_MO_12, m.PRIOR_USAGE, m.DATE_LAST_USAGE, "
                      "m.AMT_PRICE,"
                      "m.OBSOLETE_FLAG, m.CODE_BOM, m.CODE_DISCOUNT, "
                      "m.CODE_TOTAL, "
                      "m.CODE_SORT, m.QTY_RECVD_NOT_INSP, "
                      "m.QTY_MFG_REQMTS, "
                      "m.QTY_CURRENT_USAGE, m.YEAR_LAST_ROLL, "
                      "m.DATE_LAST_AUDIT,"
                      "m.CODE_EXTRA_DESC, m.PCT_ORDER_DISC, "
                      "m.TIME_MATERIAL_LEAD,"
                      "m.PRIM_DIM, m.SEC_DIM, m.QTY_BEGINNING, "
                      "m.AMT_BEG_COST, "
                      "m.CODE_EXCEPTION, m.CODE_PERM_FIX, m.DATE_EXCEPTION, "
                      "m.CTR_BACK_ORDER, m.AMT_ALT_COST, m.DATE_LAST_CHG, "
                      "m.TIME_LAST_CHG, "
                      "m.WHO_CHG_LAST, m.TRM_CHG_LAST, m.LENGTH_RAW_MATL, "
                      "m.WIDTH_RAW_MATL,"
                      "m.DENSITY_RAW_MATL, m.CODE_RM_SHAPE, "
                      "m.QTY_LAST_ONHAND, "
                      "m.DATE_LAST_VERIFY, m.FLAG_LOT, m.FLAG_DROP, "
                      "m.FLAG_6_COST,"
                      "m.FLAG_SERIALIZE, m.FLAG_INACTIVE, m.FLAG_WARRANTY, "
                      "m.USE_ZERO_LEAD,"
                      "m2.PART, m2.LOCATION, m2.QTY_MAXIMUM, "
                      "m2.HRS_STANDARD, m2.LBS, "
                      "m2.CODE_SOURCE, m2.NAME_VENDOR, m2.TEXT_INFO1, "
                      "m2.TEXT_INFO2, "
                      "m2.DESCRIPTION_2, m2.DESCRIPTION_3, m2.AMT_COST_1, "
                      "m2.AMT_COST_2,"
                      "m2.AMT_COST_3, m2.DATE_CYCLE, m2.LIFO_BASE, "
                      "m2.SIX_DECIMAL_COST, "
                      "m2.WT_PER_FOOT, m2.CUTTING_CHARGE, m2.SHP_CNV_FACTOR, "
                      "m2.SHIP_UM, "
                      "m2.LENGTH, m2.WIDTH, m2.WARRANTY_TYPE, m2.PROP_CODE, "
                      "m2.REQUIRES_INSP, m2.BASE_PART, m2.PRICE_CATG, "
                      "m2.ISSUE_UM,"
                      "m2.PART_PRICE_CODE, m3.PART, m3.LOCATION, m3.HM_FLAG, "
                      "m3.FRT_CLASS,"
                      "m3.PALLET_FLAG, m3.CNTNRS_PER_PALLET, m3.PKGD_BY, "
                      "m3.PCS_PER_CNTNR, "
                      "m3.DFLT_CARTON_CD, m3.DFLT_PALLET_CD, m3.COMM_DESCR, "
                      "m3.NMFC_NO, "
                      "m3.PKGD_WEIGHT, m3.PKG_COMPONENTS, m3.LOT_TO_LOT, "
                      "m3.DROP_SHIP, "
                      "m3.CONSUMP_CONV, m3.BOM_REF, m3.STOCK_BIN, "
                      "m3.GEN_PART_SEQ, "
                      "m3.GEN_PART_NBR, m3.NMFC_SUB_NO, m3.IC_VENDOR, "
                      "m3.MATL_SCHRG_DATE,"
                      "m3.PART_CREATE_DATE, m3.SHELF_LIFE, "
                      "m3.REQUIRES_TESTING, "
                      "m3.BIZ_WEB_PART_FLG, m3.AUTO_LOT_NUM, m3.COST_DATE, "
                      "m3.AGING,"
                      "m3.PROJECT_GROUP, m3.TEMP_PURCH, "
                      "m3.CONSUMPTION_PERCENT, "
                      "m3.DO_NOT_CALC_ABC, m3.EXCL_MULTI_PART_WO, "
                      "m3.LABEL_RPT_ID,"
                      "m3.PO_CERTS_REQD, m3.THICKNESS, m3.ROLL, "
                      "m3.INCL_SPCD, m3.NO_DISC, "
                      "m3.COST_NO_OVHD, m3.STANDARD_COST_QTY, "
                      "m3.TRIGGER_PART, "
                      "m3.VAT_PRODUCT_TYP, m3.TAX_EXEMPT_FLG, "
                      "m3.PART_CREATE_USER,"
                      "m3.DO_NOT_BACKFLUSH, m3.MODEL_BOM_FLAG, m3.MFG_LEAD, "
                      "m3.MFG_QTY_MINIMUM, m3.MFG_QTY_MULTIPLE, "
                      "m3.USE_DIMENSION_CALC,"
                      "m3.CARTON_BAG_QTY, NULL AS HARMONIZE_CODE, "
                      "NULL AS ORIGIN_COUNTRY, "
                      "m3.MATL_SCHRG_TYPE from V_INVENTORY_MSTR as m LEFT JOIN"
                      "V_INVENTORY_MST2 as m2 on m.PART = m2.PART  LEFT JOIN "
                      "V_INVENTORY_MST3 as m3 on m.PART = m3.PART ")
        # 'WHERE m.PRODUCT_LINE = 'RM'
        filters = {}
        # Add the formatting needed as well
        if product_line:
            filters['m.PRODUCT_LINE'] = f"'{product_line}'"

        first = True
        for k, v in filters.items():
            #             For each filter add a "Where" clause, if not the
            #             first, concatenate with an "AND"
            if not first:
                select_cmd += ' AND'
            select_cmd += f' WHERE {k} = {v}'
        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()
        cursor.execute(select_cmd)

        parts = []

        rows = cursor.fetchall()
        cnt = len(rows)
        logger.debug(f'{cnt} records selected')
        # while row is not None:
        #     cnt += 1
        for row in rows:
            # writer.writerow(row)
            logger.debug(f'row length: {len(row)}')
            part = PartRecord(part=row[0],
                              product_line=row[3],
                              description=row[5],
                              um_purchasing=row[6],
                              um_inventory=row[7],
                              qty_on_hand=row[11],
                              on_order_po=row[13],
                              amt_cost=row[16],
                              date_last_usage=row[30],
                              amt_price=row[31],
                              code_sort=row[36],
                              date_last_audit=row[41],
                              prim_dim=row[45],
                              sec_dim=row[46],
                              date_exception=row[51],
                              amt_alt_cost=row[53],
                              date_last_chg=row[54],
                              time_last_change=row[55],
                              who_chg_last=row[56],
                              trm_chg_last=row[57],
                              length_raw_matl=row[58],
                              width_raw_matl=row[59],
                              density_raw_matl=row[60],
                              code_rm_shape=row[61],
                              qty_last_onhand=row[62],
                              date_last_verify=row[63],
                              flag_inactive=row[68],
                              description_2=row[80],
                              description_3=row[81],
                              amt_cost_1=row[82],
                              amt_cost_2=row[83],
                              amt_cost_3=row[84],
                              date_cycle=row[85],
                              lifo_base=row[86],
                              six_decimal_cost=row[87],
                              wt_per_foot=row[88],
                              cutting_charge=row[89],
                              length=row[92],
                              width=row[93],
                              warranty_type=row[94],
                              prop_code=row[95],
                              issue_um=row[99],
                              matl_schrg_date=row[124],
                              part_create_date=row[125],
                              cost_date=row[130],
                              thickness=row[139],
                              part_create_user=row[148],
                              use_dimension_calc=row[154],
                              # It is not clear which column the
                              # _extra_description we insert into the
                              # Staging table comes from. For now stubbing out
                              extra_description='',
                              inactive=row[68]
                              )
            # row = clean_row(cursor.fetchone())
            parts.append(part)
            # row = cursor.fetchone()

        cursor.commit()
        cursor.close()
        return parts

    @staticmethod
    def insert(external_partnumber: str, partnumber: str, revision: str,
               location: str, product_line: str, description: str,
               unit_of_measure: str, source: str, default_bin: str,
               abc_code: str, purchasing_um: str, lead_time: int,
               safety_stock: decimal.Decimal, order_quantity: decimal.Decimal,
               sort_code: str, vendor_sort: str, user_field_1: str,
               user_field_2: str, maximum: decimal.Decimal,
               reorder_point: decimal.Decimal, length: decimal.Decimal,
               width: decimal.Decimal, thickness: decimal.Decimal,
               density: decimal.Decimal, weight: decimal.Decimal,
               alt_description_1: str, alt_description_2: str,
               price: decimal.Decimal = 0, cost: decimal.Decimal = 0,
               alternate_cost: decimal.Decimal = 0,
               extra_description: str = '', inactive: bool = False):

        """
        Insert or update a part record in Global Shop by inserting into the
        Part staging table. Behavior of the data inserted into the staging
        table is determined by the settings in GlobalShop.

        param source - part's source code. There are 6 options. Manufacture
        to Stock [MS](M), Manufacture to Job [MJ](F), Purchase to Stock [
        PS](P), Purchase to Job [PJ](J), Consign to Stock [CS](C), Consign
        to Job [CJ](G):
        """

        sql_cmd = f"""
              INSERT INTO GCG_5807_PART_STAGE (
          EXTERNAL_PARTNUMBER,
         PARTNUMBER,
         REVISION,
         LOCATION,
         PRODUCT_LINE,
         DESCRIPTION,
         UNIT_OF_MEASURE,
         SOURCE,
         DEFAULT_BIN,
         PRICE,
         COST,
         ALTERNATE_COST,
         ABC_CODE,
         PURCHASING_UM,
         LEAD_TIME,
         SAFETY_STOCK,
         ORDER_QUANTITY,
         SORT_CODE,
         VENDOR_SORT,
         USER_FIELD_1,
         USER_FIELD_2,
         MAXIMUM,
         REORDER_POINT,
         LENGTH,
         WIDTH,
         THICKNESS,
         DENSITY,
         WEIGHT,
         ALT_DESCRIPTION_1,
         ALT_DESCRIPTION_2,
         EXTRA_DESCRIPTION,
         INACTIVE
               )
               VALUES (
               {sqlize_str(external_partnumber)},{sqlize_str(partnumber)}
               ,{sqlize_str(revision)} ,{sqlize_str(location)}
               ,{sqlize_str(product_line)},{sqlize_str(description)}
               ,{sqlize_str(unit_of_measure)}, {sqlize_str(source)}
               ,{sqlize_str(default_bin)},{sqlize_value(str(price))}
               ,{sqlize_value(cost)},{sqlize_value(alternate_cost)}
               ,{sqlize_str(abc_code)},{sqlize_str(purchasing_um)}
               ,{sqlize_value(lead_time)},{sqlize_value(safety_stock)}
               ,{sqlize_value(order_quantity)},{sqlize_str(sort_code)}
               ,{sqlize_str(vendor_sort)},{sqlize_str(user_field_1)}
               ,{sqlize_str(user_field_2)},{sqlize_value(maximum)}
               ,{sqlize_value(reorder_point)},{sqlize_value(length)}
               ,{sqlize_value(width)},{sqlize_value(thickness)}
               ,{sqlize_value(density)},{sqlize_value(weight)}
               ,{sqlize_str(alt_description_1)},{sqlize_str(alt_description_2)}
               ,{sqlize_str(extra_description, remove_newlines=False, replace_newline_char='***N***')}
               ,{sqlize_bool(inactive)}
               ); """

        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()
        logger.debug(f'INSERT PART: "{sql_cmd}"')
        cursor.execute(sql_cmd)
        cursor.commit()
        cursor.close()

#         TODO: Return part Record

    @staticmethod
    def get(part_id: str) -> Optional[PartRecord]:

        # This select is explicity setting every column of the 3 views so we
        # can guarantee the position of the data in each row, and if we want to
        # add more fields to the Named Tuple result later we can do so without
        # affecting the index used for the previous values.
        select_cmd = ("SELECT m.PART, m.LOCATION, m.CODE_ABC,"
                      "m.PRODUCT_LINE, m.BIN, m.DESCRIPTION, m.UM_PURCHASING,"
                      "m.UM_INVENTORY, m.FACTOR_CONVERSION, m.QTY_ORDER, "
                      "m.QTY_SAFETY,"
                      "m.QTY_ONHAND, m.QTY_REORDER, m.QTY_ONORDER_PO, "
                      "m.QTY_ONORDER_WO,"
                      "m.QTY_REQUIRED, m.AMT_COST, m.QTY_USAGE_MO_01, "
                      "m.QTY_USAGE_MO_02,"
                      "m.QTY_USAGE_MO_03, m.QTY_USAGE_MO_04, "
                      "m.QTY_USAGE_MO_05, "
                      "m.QTY_USAGE_MO_06, m.QTY_USAGE_MO_07, "
                      "m.QTY_USAGE_MO_08, "
                      "m.QTY_USAGE_MO_09, m.QTY_USAGE_MO_10, "
                      "m.QTY_USAGE_MO_11, "
                      "m.QTY_USAGE_MO_12, m.PRIOR_USAGE, m.DATE_LAST_USAGE, "
                      "m.AMT_PRICE,"
                      "m.OBSOLETE_FLAG, m.CODE_BOM, m.CODE_DISCOUNT, "
                      "m.CODE_TOTAL, "
                      "m.CODE_SORT, m.QTY_RECVD_NOT_INSP, "
                      "m.QTY_MFG_REQMTS, "
                      "m.QTY_CURRENT_USAGE, m.YEAR_LAST_ROLL, "
                      "m.DATE_LAST_AUDIT,"
                      "m.CODE_EXTRA_DESC, m.PCT_ORDER_DISC, "
                      "m.TIME_MATERIAL_LEAD,"
                      "m.PRIM_DIM, m.SEC_DIM, m.QTY_BEGINNING, "
                      "m.AMT_BEG_COST, "
                      "m.CODE_EXCEPTION, m.CODE_PERM_FIX, m.DATE_EXCEPTION, "
                      "m.CTR_BACK_ORDER, m.AMT_ALT_COST, m.DATE_LAST_CHG, "
                      "m.TIME_LAST_CHG, "
                      "m.WHO_CHG_LAST, m.TRM_CHG_LAST, m.LENGTH_RAW_MATL, "
                      "m.WIDTH_RAW_MATL,"
                      "m.DENSITY_RAW_MATL, m.CODE_RM_SHAPE, "
                      "m.QTY_LAST_ONHAND, "
                      "m.DATE_LAST_VERIFY, m.FLAG_LOT, m.FLAG_DROP, "
                      "m.FLAG_6_COST,"
                      "m.FLAG_SERIALIZE, m.FLAG_INACTIVE, m.FLAG_WARRANTY, "
                      "m.USE_ZERO_LEAD,"
                      "m2.PART, m2.LOCATION, m2.QTY_MAXIMUM, "
                      "m2.HRS_STANDARD, m2.LBS, "
                      "m2.CODE_SOURCE, m2.NAME_VENDOR, m2.TEXT_INFO1, "
                      "m2.TEXT_INFO2, "
                      "m2.DESCRIPTION_2, m2.DESCRIPTION_3, m2.AMT_COST_1, "
                      "m2.AMT_COST_2,"
                      "m2.AMT_COST_3, m2.DATE_CYCLE, m2.LIFO_BASE, "
                      "m2.SIX_DECIMAL_COST, "
                      "m2.WT_PER_FOOT, m2.CUTTING_CHARGE, m2.SHP_CNV_FACTOR, "
                      "m2.SHIP_UM, "
                      "m2.LENGTH, m2.WIDTH, m2.WARRANTY_TYPE, m2.PROP_CODE, "
                      "m2.REQUIRES_INSP, m2.BASE_PART, m2.PRICE_CATG, "
                      "m2.ISSUE_UM,"
                      "m2.PART_PRICE_CODE, m3.PART, m3.LOCATION, m3.HM_FLAG, "
                      "m3.FRT_CLASS,"
                      "m3.PALLET_FLAG, m3.CNTNRS_PER_PALLET, m3.PKGD_BY, "
                      "m3.PCS_PER_CNTNR, "
                      "m3.DFLT_CARTON_CD, m3.DFLT_PALLET_CD, m3.COMM_DESCR, "
                      "m3.NMFC_NO, "
                      "m3.PKGD_WEIGHT, m3.PKG_COMPONENTS, m3.LOT_TO_LOT, "
                      "m3.DROP_SHIP, "
                      "m3.CONSUMP_CONV, m3.BOM_REF, m3.STOCK_BIN, "
                      "m3.GEN_PART_SEQ, "
                      "m3.GEN_PART_NBR, m3.NMFC_SUB_NO, m3.IC_VENDOR, "
                      "m3.MATL_SCHRG_DATE,"
                      "m3.PART_CREATE_DATE, m3.SHELF_LIFE, "
                      "m3.REQUIRES_TESTING, "
                      "m3.BIZ_WEB_PART_FLG, m3.AUTO_LOT_NUM, m3.COST_DATE, "
                      "m3.AGING,"
                      "m3.PROJECT_GROUP, m3.TEMP_PURCH, "
                      "m3.CONSUMPTION_PERCENT, "
                      "m3.DO_NOT_CALC_ABC, m3.EXCL_MULTI_PART_WO, "
                      "m3.LABEL_RPT_ID,"
                      "m3.PO_CERTS_REQD, m3.THICKNESS, m3.ROLL, "
                      "m3.INCL_SPCD, m3.NO_DISC, "
                      "m3.COST_NO_OVHD, m3.STANDARD_COST_QTY, "
                      "m3.TRIGGER_PART, "
                      "m3.VAT_PRODUCT_TYP, m3.TAX_EXEMPT_FLG, "
                      "m3.PART_CREATE_USER,"
                      "m3.DO_NOT_BACKFLUSH, m3.MODEL_BOM_FLAG, m3.MFG_LEAD, "
                      "m3.MFG_QTY_MINIMUM, m3.MFG_QTY_MULTIPLE, "
                      "m3.USE_DIMENSION_CALC,"
                      "m3.CARTON_BAG_QTY, NULL AS HARMONIZE_CODE, "
                      "NULL AS ORIGIN_COUNTRY, "
                      "m3.MATL_SCHRG_TYPE from V_INVENTORY_MSTR as m LEFT JOIN "
                      "V_INVENTORY_MST2 as m2 on m.PART = m2.PART LEFT JOIN "
                      "V_INVENTORY_MST3 as m3 on m.PART = m3.PART ")

        # 'WHERE m.PRODUCT_LINE = 'RM'
        filters = {}
        # Add the formatting needed as well
        if part_id:
            filters['m.PART'] = f"'{part_id}'"

        first = True
        for k, v in filters.items():
            #             For each filter add a "Where" clause, if not the
            #             first, concatenate with an "AND"
            if not first:
                select_cmd += ' AND'
            select_cmd += f' WHERE {k} = {v}'
        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()
        cursor.execute(select_cmd)

        row = cursor.fetchone()
        if row is None:
            return None

        # writer.writerow(row)
        logger.debug(f'row length: {len(row)}')
        part = PartRecord(part=row[0],
                          product_line=row[3],
                          description=row[5],
                          um_purchasing=row[6],
                          um_inventory=row[7],
                          qty_on_hand=row[11],
                          on_order_po=row[13],
                          amt_cost=row[16],
                          date_last_usage=row[30],
                          amt_price=row[31],
                          code_sort=row[36],
                          date_last_audit=row[41],
                          prim_dim=row[45],
                          sec_dim=row[46],
                          date_exception=row[51],
                          amt_alt_cost=row[53],
                          date_last_chg=row[54],
                          time_last_change=row[55],
                          who_chg_last=row[56],
                          trm_chg_last=row[57],
                          length_raw_matl=row[58],
                          width_raw_matl=row[59],
                          density_raw_matl=row[60],
                          code_rm_shape=row[61],
                          qty_last_onhand=row[62],
                          date_last_verify=row[63],
                          flag_inactive=row[68],
                          description_2=row[80],
                          description_3=row[81],
                          amt_cost_1=row[82],
                          amt_cost_2=row[83],
                          amt_cost_3=row[84],
                          date_cycle=row[85],
                          lifo_base=row[86],
                          six_decimal_cost=row[87],
                          wt_per_foot=row[88],
                          cutting_charge=row[89],
                          length=row[92],
                          width=row[93],
                          warranty_type=row[94],
                          prop_code=row[95],
                          issue_um=row[99],
                          matl_schrg_date=row[124],
                          part_create_date=row[125],
                          cost_date=row[130],
                          thickness=row[139],
                          part_create_user=row[148],
                          use_dimension_calc=row[154],
                          # It is not clear which column the
                          # _extra_description we insert into the
                          # Staging table comes from. For now stubbing out
                          extra_description='',
                          inactive=row[68])

        cursor.commit()
        cursor.close()
        return part


class InventoryHist:
    @staticmethod
    def select_ids(where=None) -> List[str]:
        """
        Select all part IDs
        :return: An iterable of string part IDs
        """
        sql_cmd = """SELECT PART from V_INVENTORY_HIST"""
        if where:
            sql_cmd += f" WHERE {where}"
        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()
        logger.info(f'running sql: {sql_cmd}')
        cursor.execute(sql_cmd)
        rows = cursor.fetchall()
        ids = [row[0] for row in rows]

        cursor.commit()
        cursor.close()
        # logger.debug(f'part ids selected: {ids}')
        return ids


class ItemHist:
    @staticmethod
    def select_ids(where=None) -> List[str]:
        """
        Select all part IDs
        :return: An iterable of string part IDs
        """
        sql_cmd = """SELECT PART from V_ITEM_HISTORY"""
        if where:
            sql_cmd += f" WHERE {where}"
        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()
        logger.info(f'running sql: {sql_cmd}')
        cursor.execute(sql_cmd)
        rows = cursor.fetchall()
        ids = [row[0] for row in rows]
        cursor.commit()
        cursor.close()
        return ids
