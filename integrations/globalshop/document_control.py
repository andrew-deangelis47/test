from typing import Optional

from baseintegration.utils.data import sqlize_str
from globalshop.client import GlobalShopClient
from baseintegration.integration import logger
from collections import namedtuple

# Using a Named Tuple to represent an immutable state of data rather than a
# true class, as this will not have a save(), create(), delete() interface that
# relies on updating fields
document_control_record_field_names = (
    'external_id', 'link_type', 'group_name', 'link_key', 'file_path', 'description')
DocumentControlRecord = namedtuple('DocumentControlRecord', document_control_record_field_names)


class DocumentControl:
    """
    To add a document_control, this is done by inserting into the staging table:
    GCG_5807_DOC_STAGE
    """
    @staticmethod
    def insert_with_type_inventory_master(external_id: str, file_path: str, partnumber: str,
                                          revision: Optional[str] = None, location: Optional[str] = None,
                                          group_name: Optional[str] = None, description: Optional[str] = None):
        link_type = '30'
        link_key = partnumber
        if revision is not None:
            link_key = f'{link_key.ljust(17)}{revision}'
        if location is not None:
            link_key = f'{link_key.ljust(20)}{location}'

        return DocumentControl.insert(external_id, link_type, link_key, file_path, group_name, description)

    @staticmethod
    def insert(external_id: str, link_type: str, link_key: str, file_path: str, group_name: Optional[str] = None,
               description: Optional[str] = None) -> DocumentControlRecord:
        """
        Insert or update a document_control record in Global Shop by inserting into the staging table.
        Behavior of the data inserted into the staging table is determined by the settings in GlobalShop.
        """

        sql_cmd = f"""
         INSERT INTO GCG_5807_DOC_STAGE (
             EXTERNAL_ID,
             LINK_TYPE,
             GROUP_NAME,
             LINK_KEY,
             FILE_PATH,
             DESCRIPTION
            )
            VALUES (
                {sqlize_str(external_id)},{sqlize_str(link_type)}
                ,{sqlize_str(group_name)},{sqlize_str(link_key)}
                ,{sqlize_str(file_path)},{sqlize_str(description)}
            ); """

        client: GlobalShopClient = GlobalShopClient.get_instance()
        cursor = client.cursor()
        logger.debug(f'INSERT DOCUMENT CONTROL: "{sql_cmd}"')
        cursor.execute(sql_cmd)
        cursor.commit()
        cursor.close()

        return DocumentControlRecord(external_id=external_id, link_type=link_type, group_name=group_name,
                                     link_key=link_key, file_path=file_path, description=description)
