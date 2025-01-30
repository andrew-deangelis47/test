from typing import List

from paperless.objects.orders import Order
from baseintegration.exporter.processor import BaseProcessor
from acumatica.utils import StockItemData, Facility, SalesOrderDetailData


class ProductionOrderProcessor(BaseProcessor):

    def _process(self, order: Order, stock_item_data: List[StockItemData], sales_order_data: List[SalesOrderDetailData],
                 facility: Facility):
        pass
