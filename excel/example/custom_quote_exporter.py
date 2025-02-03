from excel.exporter.exporter import ExcelQuoteExporter
from paperless.objects.quotes import Quote
from baseintegration.utils import logger


class CustomQuoteExporter(ExcelQuoteExporter):
    def _process_quote(self, quote: Quote):  # noqa: C901
        logger.info(f'Processing quote {quote.number}')
        return quote.number
