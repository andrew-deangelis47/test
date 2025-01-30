from typing import List
from paperless.objects.orders import Order
from baseintegration.exporter.processor import BaseProcessor
from acumatica.utils import ProductionOrderData, StockItemData, Facility
from acumatica.api_models.acumatica_models import Operation


class OperationProcessor(BaseProcessor):

    def _process(self, order: Order, production_order_details: List[Operation],
                 production_order_data: List[ProductionOrderData], materials: List[StockItemData], facility: Facility):
        pass
