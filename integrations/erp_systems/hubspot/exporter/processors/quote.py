from baseintegration.exporter.processor import BaseProcessor
from paperless.objects.quotes import Quote


class QuoteProcessor(BaseProcessor):

    def _process(self, quote: Quote):
        pass
