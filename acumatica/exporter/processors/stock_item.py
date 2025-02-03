from typing import List
from paperless.objects.orders import Order
from baseintegration.exporter.processor import BaseProcessor
from acumatica.utils import StockItemData, Facility


class StockItemProcessor(BaseProcessor):

    def _process(self, order: Order, facility: Facility) -> List[StockItemData]:
        pass
