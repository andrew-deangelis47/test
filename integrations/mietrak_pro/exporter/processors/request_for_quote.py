from typing import Optional

from baseintegration.datamigration import logger
from mietrak_pro.exporter.processors import MietrakProProcessor
from paperless.objects.quotes import Quote
from mietrak_pro.query.request_for_quote import create_request_for_quote
import mietrak_pro.models
from baseintegration.utils import update_quote_erp_code


class RequestForQuoteProcessor(MietrakProProcessor):
    do_rollback = False

    def _process(self, quote: Quote, customer: mietrak_pro.models.Party, contact: mietrak_pro.models.Party,
                 estimator: Optional[mietrak_pro.models.User]):

        fob = self.get_fob(quote, customer)
        delivery = self.get_delivery(quote, customer)

        logger.info('Creating new Request for Quote record')
        request_for_quote = create_request_for_quote(customer, estimator, fob, delivery,
                                                     self._exporter.erp_config.company_division_pk)

        if self._exporter.erp_config.should_update_quote_erp_code_in_paperless_parts:
            new_erp_code = str(request_for_quote.requestforquotepk)
            update_quote_erp_code(self._exporter._integration, quote.number, quote.revision_number, new_erp_code)

        return request_for_quote

    def get_fob(self, quote: Quote, customer: mietrak_pro.models.Party):
        return None

    def get_delivery(self, quote: Quote, customer: mietrak_pro.models.Party):
        return '1'
