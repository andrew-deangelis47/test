from baseintegration.exporter.quote_exporter import QuoteExporter
from baseintegration.integration import Integration
from baseintegration.exporter.exceptions import ProcessNotImplementedError
from baseintegration.exporter.order_exporter import OrderExporter


class ExcelQuoteExporter(QuoteExporter):
    def __init__(self, integration: Integration):
        super().__init__(integration)

    def _process_quote(self, quote):
        raise ProcessNotImplementedError(f"_process_quote() method not implemented on {self.__class__.__name__}")


class ExcelOrderExporter(OrderExporter):
    def __init__(self, integration: Integration):
        super().__init__(integration)

    def _process_order(self, order):
        raise ProcessNotImplementedError(f"_process_order() method not implemented on {self.__class__.__name__}")
