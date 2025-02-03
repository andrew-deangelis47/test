from typing import List

from baseintegration.utils.data import safe_trim
from globalshop.client import GlobalShopClient
from baseintegration.integration import logger
from collections import namedtuple


opcode_record_field_names = (
    'operation', 'text',)
OpCodeNoteRecord = namedtuple('OpCodeRecord', opcode_record_field_names)


class OpCodeNote:
    @staticmethod
    def select_ids(where=None) -> List[str]:
        sql_cmd = """SELECT * from V_OPCODE_TEXT"""
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
        logger.debug(f'op code texts ids selected: {ids}')
        return ids

    @staticmethod
    def get(opcode: str) -> OpCodeNoteRecord:

        # This select is explicity setting every column of the 3 views so we
        # can guarantee the position of the data in each row, and if we want to
        # add more fields to the Named Tuple result later we can do so without
        # affecting the index used for the previous values.
        select_cmd = ("SELECT w.OPERATION,"
                      "w.TEXT"
                      " from V_OPCODE_TEXT as w")
        filters = {}
        # Add the formatting needed as well
        if opcode:
            filters['w.OPERATION'] = f"'{opcode}'"

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
        logger.debug(f'row length: {len(row)}')
        opcode_text = OpCodeNoteRecord(operation=row[0], text=row[1])
        cursor.commit()
        cursor.close()
        return opcode_text
