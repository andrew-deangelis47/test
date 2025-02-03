from typing import List

from baseintegration.utils.data import safe_trim
from globalshop.client import GlobalShopClient
from baseintegration.integration import logger
from collections import namedtuple

# Using a Named Tuple to represent an immutable state of data rather than a
# true class, as this will not have a save(), create(), delete() interface that
# relies on updating fields
vendor_record_field_names = (
    'vendor', 'name_vendor')
VendorRecord = namedtuple('VendorRecord', vendor_record_field_names)


class Vendor:
    """
    - V_VENDOR_MASTER

    We have not mapped every possible field, but have added the ones we need
    over time.

    To add a vendor, this is done by inserting into the staging table:
    To Be Determined
    """

    @staticmethod
    def select_ids(where=None) -> List[str]:
        sql_cmd = """SELECT vm.VENDOR from V_VENDOR_MASTER vm INNER JOIN V_VENDOR_ADDL va ON vm.VENDOR = va.VENDOR"""
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
        logger.debug(f'vendor ids selected: {ids}')
        return ids

    @staticmethod
    def get(vendor_id: str) -> VendorRecord:

        # This select is explicity setting every column of the 3 views so we
        # can guarantee the position of the data in each row, and if we want to
        # add more fields to the Named Tuple result later we can do so without
        # affecting the index used for the previous values.
        select_cmd = ("SELECT w.VENDOR,"
                      "w.NAME_VENDOR"
                      " from V_VENDOR_MASTER as w")
        filters = {}
        # Add the formatting needed as well
        if vendor_id:
            filters['w.VENDOR'] = f"'{vendor_id}'"

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
        # writer.writerow(row)
        logger.debug(f'row length: {len(row)}')
        vendor = VendorRecord(vendor=safe_trim(row[0]),
                              name_vendor=safe_trim(row[1])
                              )

        cursor.commit()
        cursor.close()
        return vendor
