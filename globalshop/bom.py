"""
The BOM staging table represents the Bill of Materials for a part. We write out
the values to a staging table which is imported by a GAB script. If the part
doesn't exist beforehand, then it will create the part with the minimal info
provided before adding the BOM items to it.
"""
import decimal
from collections import namedtuple
from typing import Union

from globalshop.client import GlobalShopClient
from baseintegration.integration import logger
# Using a Named Tuple to represent an immutable state of data rather than a
# true class, as this will not have a save(), create(), delete() interface
# that relies on updating fields
from baseintegration.utils.data import sqlize_str, sqlize_bool

BOMRecord = namedtuple('BOMRecord', (
    'external_id',
    'top_bom',
    'top_bom_rev',
    'parent_part',
    'parent_rev',
    'level',
    'sequence',
    'part_number',
    'part_number_rev',
    'description',
    'alt_description_1',
    'alt_description_2',
    'quantity',
    'uom',
    'product_line',
    'cost',
    'source',
    'sort_code',
    'lead_time',
    'category',
    'tag',
    'drawing',
    'memo_1',
    'memo_2',
    'bom_complete',
    'extra_description',
    'comments'
))


class BOM:

    @classmethod
    def insert(cls,
               external_id: str,
               top_bom: str,
               parent_part: str,
               part_number: str,
               level: int = 0,
               sequence: int = 0,
               top_bom_rev: str = None,
               parent_rev: str = None,
               part_number_rev: str = None,
               description: str = None,
               alt_description_1: str = None,
               alt_description_2: str = None,
               quantity: Union[decimal.Decimal, int] = 0,
               uom: str = 'ea',
               product_line: str = None,
               cost: decimal.Decimal = None,
               source: str = None,
               sort_code: str = None,
               lead_time: decimal.Decimal = None,
               category: str = None,
               tag: str = None,
               drawing: str = None,
               memo_1: str = None,
               memo_2: str = None,
               bom_complete: bool = False,
               extra_description: str = None,
               comments: str = None, batch_process=True
               ) -> BOMRecord:
        """
        Write out a single line to a BOM of a part.
        :param external_id: The part identifier of the BOM item part used in PP
        :param top_bom: the top_most BOM part. In PP's case, it is the line
        item part
        :param top_bom_rev: the rev of the top_bom part
        :param parent_part: The immediate parent part the BOM is associate
        with
        :param parent_rev: The revision of the parent_part
        :param level: The 0 index depth of the BOM, used for nested BOMs
        :param sequence: 10's based iterative sequence to order the BOM
        items by
        :param batch_process: Defaults to True. When set, will cache the SQL
        INSERT statements on the client's cache. The caller is then
        responsible for executing the cache and commiting the results. This
        ensures that the WHOLE BOM is written out at once, and is not
        partially imported by GS.

        """

        """
        Schema of BOM staging table:
         CREATE TABLE "GCG_5807_BOM_STAGE" (
         "RECORD_ID" IDENTITY DEFAULT '0'
         CONSTRAINT "UK_RECORD_ID" UNIQUE USING 0,
         "RECORD_TIMESTAMP" DATETIME DEFAULT NOW(),
         "PROCESSED" BIT DEFAULT '0' NOT NULL,
         "FAILED" BIT DEFAULT '0' NOT NULL,
         "PROCESSED_TIMESTAMP" DATETIME,
         "FEEDBACK" LONGVARCHAR,
         "EXTERNAL_ID" CHAR(50) NOT NULL,
         "TOP_BOM" CHAR(20) NOT NULL,
         "TOP_BOM_REVISION" CHAR(3),
         "PARENT" CHAR(20),
         "PARENT_REVISION" CHAR(3),
         "LEVEL" INTEGER DEFAULT '0' NOT NULL,
         "SEQUENCE" INTEGER DEFAULT '0' NOT NULL,
         "PART_NUMBER" CHAR(20) NOT NULL,
         "PART_NUMBER_REVISION" CHAR(3),
         "DESCRIPTION" CHAR(30),

         TODO: DESCRIPTION_ROUTER -- set actual router header description

         "ALT_DESCRIPTION_1" CHAR(30),
         "ALT_DESCRIPTION_2" CHAR(30),
         "QUANTITY" DOUBLE DEFAULT '0' NOT NULL,
         "UNIT_OF_MEASURE" CHAR(2),
         "PRODUCT_LINE" CHAR(2),
         "COST" DOUBLE,
         "SOURCE" CHAR(1),
         "SORT_CODE" CHAR(12),
         "LEAD_TIME" DOUBLE,
         "CATEGORY" CHAR(1),
         "TAG" CHAR(6),
         "DRAWING" CHAR(20),
         "MEMO_1" CHAR(30),
         "MEMO_2" CHAR(30),
         "BOM_COMPLETE" BIT DEFAULT '0' NOT NULL,
         "EXTRA_DESCRIPTION" LONGVARCHAR,
         "COMMENTS" LONGVARCHAR );
        """

        """
        FIXME: Removing LEAD_TIME for now:

         ,{str(lead_time) if lead_time else 'null'}
        """
        # TODO add runtime column
        if part_number is None:
            raise ValueError('Part number cannot be none')
        sql_cmd = f"""
        INSERT INTO GCG_5807_BOM_STAGE (
         EXTERNAL_ID,
         PARENT_EXTERNAL_ID,
         PART_EXTERNAL_ID,
         TOP_BOM,
         TOP_BOM_REVISION,
         PARENT,
         PARENT_REVISION,
         LEVEL,
         SEQUENCE,
         PART_NUMBER,
         PART_NUMBER_REVISION,
         DESCRIPTION,
         ALT_DESCRIPTION_1,
         ALT_DESCRIPTION_2,
         QUANTITY,
         UNIT_OF_MEASURE,
         PRODUCT_LINE,
         COST,
         SOURCE,
         SORT_CODE,
         CATEGORY,
         TAG,
         DRAWING,
         MEMO_1,
         MEMO_2,
         BOM_COMPLETE,
         EXTRA_DESCRIPTION,
         COMMENTS )
         VALUES (
         {sqlize_str(external_id)},{sqlize_str(external_id)}
         ,{sqlize_str(external_id)} ,{sqlize_str(top_bom)}
         ,{sqlize_str(top_bom_rev)},{sqlize_str(parent_part)}
         ,{sqlize_str(parent_rev)},{level},{sequence},{sqlize_str(part_number)}
         ,{sqlize_str(part_number_rev)},{sqlize_str(description)}
         ,{sqlize_str(alt_description_1)},{sqlize_str(alt_description_2)},{str(quantity)}
         ,{sqlize_str(uom)},{sqlize_str(product_line)}
         ,{str(cost) if cost else 'null'}
         ,{sqlize_str(source)},{sqlize_str(sort_code)}
         ,{sqlize_str(category)},{sqlize_str(tag)}
         ,{sqlize_str(drawing)},{sqlize_str(memo_1)}
         ,{sqlize_str(memo_2)},{sqlize_bool(bom_complete)},{sqlize_str(extra_description)}
         ,{sqlize_str(comments,remove_newlines=False, replace_newline_char='***N***')}); """

        client: GlobalShopClient = GlobalShopClient.get_instance()

        logger.debug(f'INSERT BOM: "{sql_cmd}"')
        if batch_process:
            client.cache(sql_cmd=sql_cmd)
        else:
            cursor = client.cursor()
            cursor.execute(sql_cmd)
            cursor.commit()
            cursor.close()
        return BOMRecord(external_id=external_id, top_bom=top_bom,
                         top_bom_rev=top_bom_rev,
                         parent_part=parent_part, parent_rev=parent_rev,
                         level=level, sequence=sequence,
                         part_number=part_number,
                         part_number_rev=part_number_rev,
                         description=description,
                         alt_description_1=alt_description_1,
                         alt_description_2=alt_description_2,
                         quantity=quantity, uom=uom,
                         product_line=product_line, cost=cost, source=source,
                         sort_code=sort_code, lead_time=lead_time,
                         category=category, tag=tag, drawing=drawing,
                         memo_1=memo_1, memo_2=memo_2,
                         bom_complete=bom_complete,
                         extra_description=extra_description,
                         comments=comments)
