from paperless.objects.orders import Order
from baseintegration.exporter import BaseProcessor

from acumatica.utils import CustomerData


class CustomerProcessor(BaseProcessor):

    def _process(self, order: Order) -> CustomerData:
        pass
