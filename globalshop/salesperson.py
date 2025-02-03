from typing import NamedTuple

from baseintegration.integration import logger
from baseintegration.utils.data import sqlize_str, safe_trim
from globalshop.client import GlobalShopClient


class SalespersonRecord(NamedTuple):
    id: str
    name: str
    email: str


class Salesperson:

    @classmethod
    def get(cls, sales_person_id: str) -> SalespersonRecord:
        sql_cmd = f"""SELECT ID, NAME, EMAIL FROM V_SALESPERSONS WHERE ID =\
         {sqlize_str(sales_person_id)} """
        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()
        logger.debug(sql_cmd)
        cursor.execute(sql_cmd)
        row = cursor.fetchone()
        cursor.commit()
        cursor.close()

        # There are lots of extra spaces in the values returned, need to
        # strip them out.
        if row is None:
            return None

        row = (safe_trim(val) for val in row)
        logger.debug(f'Get Salesperson row: {row}')

        sales_person_id, name, email = row
        return SalespersonRecord(id=sales_person_id, name=name, email=email)
