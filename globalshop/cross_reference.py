from typing import Optional

from baseintegration.utils.data import sqlize_str
from globalshop.client import GlobalShopClient
from baseintegration.integration import logger
from collections import namedtuple

# Using a Named Tuple to represent an immutable state of data rather than a
# true class, as this will not have a save(), create(), delete() interface that
# relies on updating fields
cross_reference_record_field_names = (
    'external_partnumber', 'partnumber', 'revision', 'customer', 'customer_part', 'vendor', 'manufacturer_part',
    'manufacturer_name', 'status', 'user_default_title', 'comment')
CrossReferenceRecord = namedtuple('CrossReferenceRecord', cross_reference_record_field_names)


class CrossReference:
    """
    To add a cross reference, this is done by inserting into the staging table:
    GCG_5807_XREF_STAGE
    """
    @staticmethod
    def insert(external_partnumber: str, partnumber: str, revision: Optional[str] = None,
               customer: Optional[str] = None, customer_part: Optional[str] = None, vendor: Optional[str] = None,
               manufacturer_part: Optional[str] = None, manufacturer_name: Optional[str] = None,
               status: Optional[str] = None, user_default_title: Optional[str] = None, comment: Optional[str] = None):
        """
        Insert or update a cross reference record in Global Shop by inserting into the
        Xref staging table. Behavior of the data inserted into the staging
        table is determined by the settings in GlobalShop.
        """

        sql_cmd = f"""
         INSERT INTO GCG_5807_XREF_STAGE (
             EXTERNAL_PARTNUMBER,
             PARTNUMBER,
             REVISION,
             CUSTOMER,
             CUSTOMER_PART,
             VENDOR,
             MANUFACTURER_PART,
             MANUFACTURER_NAME,
             STATUS,
             USER_DEFAULT_TITLE,
             COMMENT
            )
            VALUES (
                {sqlize_str(external_partnumber)},{sqlize_str(partnumber)}
                ,{sqlize_str(revision)},{sqlize_str(customer)}
                ,{sqlize_str(customer_part)},{sqlize_str(vendor)}
                ,{sqlize_str(manufacturer_part)}, {sqlize_str(manufacturer_name)}
                ,{sqlize_str(status)},{sqlize_str(user_default_title)}
                ,{sqlize_str(comment)}
            ); """

        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()
        logger.debug(f'INSERT XREF: "{sql_cmd}"')
        cursor.execute(sql_cmd)
        cursor.commit()
        cursor.close()

        return CrossReferenceRecord(external_partnumber=external_partnumber, partnumber=partnumber, revision=revision,
                                    customer=customer, customer_part=customer_part, vendor=vendor,
                                    manufacturer_part=manufacturer_part, manufacturer_name=manufacturer_name,
                                    status=status, user_default_title=user_default_title, comment=comment)
