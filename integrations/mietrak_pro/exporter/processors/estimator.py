from mietrak_pro.exporter.processors import MietrakProProcessor
from paperless.objects.quotes import Quote
from mietrak_pro.query.estimator import get_assigned_estimator_by_id


class EstimatorProcessor(MietrakProProcessor):

    def _process(self, quote: Quote):
        estimator = None
        estimator_id = self.get_quote_estimator_id(quote)
        if estimator_id is not None:
            estimator = self.get_estimator(estimator_id)
        return estimator

    def get_estimator(self, estimator_id):
        return get_assigned_estimator_by_id(estimator_id)

    def get_quote_estimator_id(self, quote: Quote):
        estimator_id = None
        if quote.estimator is not None:
            estimator_id = quote.estimator.erp_code
        return estimator_id
