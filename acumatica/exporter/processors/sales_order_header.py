from paperless.objects.orders import Order
from baseintegration.exporter.processor import BaseProcessor

from acumatica.utils import CustomerData, Facility


class SalesOrderHeaderProcessor(BaseProcessor):

    def _process(self, order: Order, customer_data: CustomerData, facility: Facility):
        pass
