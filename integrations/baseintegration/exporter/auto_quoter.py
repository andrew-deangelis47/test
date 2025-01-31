from ...baseintegration.datamigration import logger
from ...baseintegration.exporter.exceptions import IntegrationNotImplementedError
from ...baseintegration.exporter import BaseExporter
from ...baseintegration.exporter.mixins.order_assembly_traversal_mixin import AssemblyTraversalMixin
from ...baseintegration.integration import Integration
from paperless.objects.quotes import Quote


class AutoQuoteResult:

    ELIGIBLE = 'ELIGIBLE'
    NOT_ELIGIBLE = 'NOT_ELIGIBLE'
    NOT_DETERMINED = 'NOT_DETERMINED'

    result: str  # E (eligible), NE (not eligible), ND (not determined)
    message: str
    is_error: bool

    def __init__(self, type: str, is_error: bool, message: str):
        # make sure the type is valid
        if type not in [self.ELIGIBLE, self.NOT_ELIGIBLE, self.NOT_DETERMINED]:
            raise Exception(f"Only {self.ELIGIBLE}, {self.NOT_ELIGIBLE}, and {self.NOT_DETERMINED} can be used as the "
                            f" AutoQuoteResult's type property.")

        self.result: self = type
        self.message: str = message
        self.is_error: bool = is_error


class AutoQuoter(AssemblyTraversalMixin, BaseExporter):
    """
    Defines how to move an order from Paperless to an ERP system. This should be overridden by a specific ERPOrderExporter
    """

    paperless_config = None

    def __init__(self, integration: Integration):
        super().__init__(integration)
        self.quote = None
        self.is_auto_quotable = False
        logger.info("Instantiated the auto quoter")

    def run(self, auto_quote_num: str) -> Quote:
        """
        calling this method is what runs the auto quoter
        """
        logger.info("Running auto quoter")
        self.is_auto_quotable = False
        quote: Quote = Quote.get(
            auto_quote_num.split("-")[0],
            auto_quote_num.split("-")[1] if len(auto_quote_num.split("-")) > 1 else None
        )
        quote_num_and_revision: str = f'{quote.number}{("-" + str(quote.revision_number)) if quote.revision_number else ""}'
        logger.info(f'Quote number and revision is "{quote_num_and_revision}"')

        # get the result and log it
        auto_quote_result: AutoQuoteResult = self._process_quote(quote, quote_num_and_revision)
        logger.info(f'Result: {auto_quote_result.result}')
        logger.info(f'Error: {auto_quote_result.is_error}')
        logger.info(f'Message: {auto_quote_result.message}')

    def _process_quote(self, quote: Quote, quote_num_and_rev: str) -> AutoQuoteResult:
        """
        This is the main driver of the whole integration process. This needs to be overridden by the base class
        :return: The success status of the order processing
        """
        raise IntegrationNotImplementedError
