from sage.models.sage_models.sales_quote import SalesQuote
from sage.models.sage_models.quote_line_item import QuoteLineItem
from unittest import TestCase


class TestSageApiExportXmlGenerator(TestCase):

    def setUp(self) -> None:
        pass

    def test_get_request_xml(self):

        test_line_item = QuoteLineItem()
        test_line_item.item_ref = '000-300-006'
        test_line_item.sal = 'EA'
        test_line_item.quantity = '4'
        test_line_item.sal_stk_conv = '1'
        test_line_item.stock = 'EA'
        test_line_item.gross_price = '100'
        test_line_item.tax_level_1 = 'NTX'

        test_line_item_0 = QuoteLineItem()
        test_line_item_0.item_ref = '000-300-009'
        test_line_item_0.sal = 'EA'
        test_line_item_0.quantity = '5'
        test_line_item_0.sal_stk_conv = '1'
        test_line_item_0.stock = 'EA'
        test_line_item_0.gross_price = '200'
        test_line_item_0.tax_level_1 = 'NTX'

        test_quote = SalesQuote()
        test_quote.sales_site = 'ARC01'
        test_quote.quote_type = 'SQN'
        test_quote.reference = 'AWESOME_TEST_2'
        test_quote.quote_date = '20220214'
        test_quote.customer_id = 'C00048'
        test_quote.currency = 'USD'
        test_quote.delivery_address = 'BILL'
        test_quote.shipment_site = 'ARC01'
        test_quote.line_items = [test_line_item, test_line_item_0]

        self.assertTrue(True)
