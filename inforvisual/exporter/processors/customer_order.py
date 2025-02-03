from baseintegration.exporter import BaseProcessor
from paperless.objects.orders import Order
from inforvisual.models import Customer
from baseintegration.datamigration import logger


class CustomerOrderProcessor(BaseProcessor):

    def _process(self, order: Order, customer: Customer, part_data: list, order_item_data: list):
        # note this code was removed because it creates a new order for each line item due to Metalcraft's requirements.
        # You can check out Metalcraft's code for an example
        logger.info("Bringing over customer orders")
