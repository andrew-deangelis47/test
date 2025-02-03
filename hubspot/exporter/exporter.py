from baseintegration.datamigration import logger
from baseintegration.exporter.quote_exporter import QuoteExporter
from paperless.objects.quotes import Quote
from hubspot.utils import HubspotQuote
from hubspot.exporter.processors.quote import QuoteProcessor


class HubspotQuoteExporter(QuoteExporter):

    def _setup_erp_config(self):
        pass

    def _register_default_processors(self):
        self.register_processor(HubspotQuote, QuoteProcessor)

    def _process_quote(self, quote: Quote):
        logger.info(f"Processing quote {quote.number}")
        with self.process_resource(HubspotQuote, quote):
            logger.info(f"Quote {quote.number} was processed")
