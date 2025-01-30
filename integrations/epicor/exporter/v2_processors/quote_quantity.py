from baseintegration.utils import logger
from epicor.quote import QuoteQuantity, QuoteHeader, QuoteDetail
from epicor.utils import QuoteHeaderData, ItemData
from typing import List
from epicor.utils import get_item_data_by_part_number, get_manufactured_components_by_line_number
from decimal import Decimal
from epicor.exporter.v2_processors.base import EpicorProcessor


class QuoteQuantityProcessor(EpicorProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'quote_quantity'

    def _process(self, quote_header: QuoteHeader, quote_details_list: List[QuoteDetail],
                 quote_header_data: QuoteHeaderData
                 ) -> List[QuoteQuantity]:

        logger.info("Instantiated process method on the Quote Quantity Processor")

        try:
            self.line_items = quote_header_data.line_items
            quote_quantities_list: list = []

            for quote_detail in quote_details_list:

                line_item_mfg_components: List[ItemData] = \
                    get_manufactured_components_by_line_number(self.line_items, quote_detail.QuoteLine)
                mfg_item_data: ItemData = get_item_data_by_part_number(line_item_mfg_components, quote_detail.PartNum)

                quote_quantity = QuoteQuantity(
                    Company=str(self._exporter.erp_config.company_name),
                    QuoteNum=quote_header.QuoteNum,
                    QuoteLine=quote_detail.QuoteLine,
                    QtyNum=1,
                    OurQuantity=quote_detail.OrderQty,
                    UnitPrice=Decimal(round(mfg_item_data.unit_price, 4))
                ).create_instance()

                quote_quantities_list.append(quote_quantity)

        except Exception as e:
            logger.info(f'Error occured in the quote quantity processor: {e}')
            self._add_report_message(f'Unexpected error occured. Created {len(quote_quantities_list)} quote {"quantities" if len(quote_quantities_list) > 1 else "quantity"}')
            raise e

        logger.info(f"Created quote : {quote_header}")
        self._add_report_message(
            f'Created {len(quote_quantities_list)} quote {"quantities" if len(quote_quantities_list) > 1 else "quantity"}')
        return quote_quantities_list
