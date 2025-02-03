from baseintegration.exporter.processor import BaseProcessor
from paperless.objects.customers import Account


class CustomerProcessor(BaseProcessor):

    def _process(self, acct: Account):
        pass
