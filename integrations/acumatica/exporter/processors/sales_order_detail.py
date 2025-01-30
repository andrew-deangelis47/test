from typing import List

from baseintegration.exporter.processor import BaseProcessor
from paperless.objects.orders import Order

from acumatica.utils import StockItemData, Facility


class SalesOrderDetailProcessor(BaseProcessor):

    def _process(self, order: Order, sales_order: dict, stock_item_data: List[StockItemData], facility: Facility):
        pass
