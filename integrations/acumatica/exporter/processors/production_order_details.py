from typing import List
from paperless.objects.orders import Order
from baseintegration.exporter.processor import BaseProcessor
from acumatica.utils import ProductionOrderData, Facility


class ProductionOrderDetailProcessor(BaseProcessor):

    def _process(self, order: Order, production_order_data: List[ProductionOrderData], facility: Facility):
        pass
