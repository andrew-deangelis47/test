from baseintegration.exporter import BaseProcessor, logger
from paperless.objects.orders import Order
from jobscope.client import JobscopeClient
from paperless.objects.customers import Account


class CustomerProcessor(BaseProcessor):

    def _process(self, order: Order) -> dict:
        logger.info("Processing customer")
        logger.info("Getting customer by ERP code")
        customer = None
        if order.contact and order.contact.account and order.contact.account.id:
            customer = self.get_customer(order.contact.account.id)
        if not customer:
            logger.info("Customer not found!")
            customer = {}
        else:
            logger.info(f"Customer {customer.get('customerName')} was found!")
        return customer

    def get_customer(self, customer_id: int) -> dict:
        client: JobscopeClient = self._exporter.client
        customer = None
        try:
            account: Account = Account.get(customer_id)
            erp_code = account.erp_code
            logger.info(f"Getting customer by erp_code {str(erp_code)}")
            customer = client.get_customer(erp_code)
        except Exception as e:
            logger.info("Not bringing over customer")
            logger.info(e)
        return customer
