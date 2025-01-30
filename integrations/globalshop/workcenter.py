from typing import List

from baseintegration.utils.data import safe_trim
from globalshop.client import GlobalShopClient
from baseintegration.integration import logger
from collections import namedtuple

# Using a Named Tuple to represent an immutable state of data rather than a
# true class, as this will not have a save(), create(), delete() interface that
# relies on updating fields
workcenter_record_field_names = (
    'workcenter', 'wc_dept', 'standard_bill', 'standard_cost', 'standard_overhead', 'fixed_ovhd', 'wc_name',
    'workgroup', 'workgroup_descr', 'prototype_wc')
WorkCenterRecord = namedtuple('WorkCenterRecord', workcenter_record_field_names)


class WorkCenter:
    """
    - V_WORKCENTERS

    We have not mapped every possible field, but have added the ones we need
    over time.

    To add a workcenter, this is done by inserting into the staging table:
    To Be Determined
    """

    @staticmethod
    def select_ids(where=None) -> List[str]:
        sql_cmd = """SELECT MACHINE from V_WORKCENTERS"""
        if where:
            sql_cmd += f" WHERE {where}"
        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()
        logger.info(f'running sql: {sql_cmd}')
        cursor.execute(sql_cmd)
        rows = cursor.fetchall()
        ids = [safe_trim(row[0]) for row in rows]

        cursor.commit()
        cursor.close()
        logger.debug(f'workcenter ids selected: {ids}')
        return ids

    @staticmethod
    def get(workcenter_id: str) -> WorkCenterRecord:

        # This select is explicity setting every column of the 3 views so we
        # can guarantee the position of the data in each row, and if we want to
        # add more fields to the Named Tuple result later we can do so without
        # affecting the index used for the previous values.
        select_cmd = ("SELECT w.MACHINE,"
                      "w.WC_DEPT,"
                      "w.STANDARD_BILL,"
                      "w.STANDARD_COST,"
                      "w.STANDARD_OVHD,"
                      "w.FIXED_OVHD,"
                      "w.WC_NAME,"
                      "wgl.WORKGROUP,"
                      "wgh.DESCR,"
                      "wgh.PROTOTYPE_WC"
                      " from V_WORKCENTERS as w"
                      " left outer join V_WORKGROUP_LINE as wgl ON w.MACHINE = wgl.WORKCENTER"
                      " left outer join V_WORKGROUP_HEAD as wgh ON wgl.WORKGROUP = wgh.WORK_GROUP")
        filters = {}
        # Add the formatting needed as well
        if workcenter_id:
            filters['w.MACHINE'] = f"'{workcenter_id}'"

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
        workcenter = WorkCenterRecord(workcenter=row[0],
                                      wc_dept=row[1],
                                      standard_bill=row[2],
                                      standard_cost=row[3],
                                      standard_overhead=row[4],
                                      fixed_ovhd=row[5],
                                      wc_name=row[6],
                                      workgroup=row[7],
                                      workgroup_descr=row[8],
                                      prototype_wc=row[9])

        cursor.commit()
        cursor.close()
        return workcenter
