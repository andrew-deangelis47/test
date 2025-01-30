import decimal
import datetime
from typing import Optional

from baseintegration.utils.data import sqlize_str, sqlize_value
from globalshop.client import GlobalShopClient
from baseintegration.integration import logger
from collections import namedtuple

# Using a Named Tuple to represent an immutable state of data rather than a
# true class, as this will not have a save(), create(), delete() interface that
# relies on updating fields
discount_table_record_field_names = (
    'type', 'external_id', 'partnumber', 'revision', 'location', 'price_date', 'description', 'quantity_1', 'price_1',
    'quantity_2', 'price_2', 'quantity_3', 'price_3', 'quantity_4', 'price_4', 'quantity_5', 'price_5', 'quantity_6',
    'price_6', 'quantity_7', 'price_7', 'quantity_8', 'price_8', 'quantity_9', 'price_9', 'quantity_10', 'price_10')
DiscountTableRecord = namedtuple('DiscountTableRecord', discount_table_record_field_names)


class DiscountTable:
    """
    To add a discount table, this is done by inserting into the staging table:
    GCG_5807_PRICE_STAGE
    """
    @staticmethod
    def insert(type: str, external_id: str, partnumber: str, revision: Optional[str] = None, location: str = None,
               price_date: datetime.date = None, description: Optional[str] = None, quantity_1: Optional[int] = None,
               price_1: decimal.Decimal = 0, quantity_2: Optional[int] = None, price_2: decimal.Decimal = 0,
               quantity_3: Optional[int] = None, price_3: decimal.Decimal = 0, quantity_4: Optional[int] = None,
               price_4: decimal.Decimal = 0, quantity_5: Optional[int] = None, price_5: decimal.Decimal = 0,
               quantity_6: Optional[int] = None, price_6: decimal.Decimal = 0, quantity_7: Optional[int] = None,
               price_7: decimal.Decimal = 0, quantity_8: Optional[int] = None, price_8: decimal.Decimal = 0,
               quantity_9: Optional[int] = None, price_9: decimal.Decimal = 0, quantity_10: Optional[int] = None,
               price_10: decimal.Decimal = 0):
        """
        Insert or update a discount table record in Global Shop by inserting into the
        GCG_5807_PRICE_STAGE staging table. Behavior of the data inserted into the staging
        table is determined by the settings in GlobalShop.
        """

        sql_cmd = f"""
         INSERT INTO GCG_5807_PRICE_STAGE (
             TYPE,
             EXTERNAL_ID,
             PART_NUMBER,
             REVISION,
             LOCATION,
             PRICE_DATE,
             DESCRIPTION,
             QUANTITY_1,
             PRICE_1,
             QUANTITY_2,
             PRICE_2,
             QUANTITY_3,
             PRICE_3,
             QUANTITY_4,
             PRICE_4,
             QUANTITY_5,
             PRICE_5,
             QUANTITY_6,
             PRICE_6,
             QUANTITY_7,
             PRICE_7,
             QUANTITY_8,
             PRICE_8,
             QUANTITY_9,
             PRICE_9,
             QUANTITY_10,
             PRICE_10
            )
            VALUES (
                {sqlize_str(type)},{sqlize_str(external_id)},
                {sqlize_str(partnumber)},{sqlize_str(revision)},
                {sqlize_str(location)},{sqlize_value(price_date)},
                {sqlize_str(description)},{sqlize_value(quantity_1)},
                {sqlize_value(price_1)},{sqlize_value(quantity_2)},
                {sqlize_value(price_2)},{sqlize_value(quantity_3)},
                {sqlize_value(price_3)},{sqlize_value(quantity_4)},
                {sqlize_value(price_4)},{sqlize_value(quantity_5)},
                {sqlize_value(price_5)},{sqlize_value(quantity_6)},
                {sqlize_value(price_6)},{sqlize_value(quantity_7)},
                {sqlize_value(price_7)},{sqlize_value(quantity_8)},
                {sqlize_value(price_8)},{sqlize_value(quantity_9)},
                {sqlize_value(price_9)},{sqlize_value(quantity_10)},
                {sqlize_value(price_10)}
            ); """

        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()
        logger.debug(f'INSERT DISCOUNT TABLE: "{sql_cmd}"')
        cursor.execute(sql_cmd)
        cursor.commit()
        cursor.close()

        return DiscountTableRecord(type=type, external_id=external_id, partnumber=partnumber, revision=revision,
                                   location=location, price_date=price_date, description=description,
                                   quantity_1=quantity_1, price_1=price_1, quantity_2=quantity_2, price_2=price_2,
                                   quantity_3=quantity_3, price_3=price_3, quantity_4=quantity_4, price_4=price_4,
                                   quantity_5=quantity_5, price_5=price_5, quantity_6=quantity_6, price_6=price_6,
                                   quantity_7=quantity_7, price_7=price_7, quantity_8=quantity_8, price_8=price_8,
                                   quantity_9=quantity_9, price_9=price_9, quantity_10=quantity_10, price_10=price_10)
