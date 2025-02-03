from sage.models.sage_models import QuoteLineItem


class PaperlessLineItemToSageLineItem:

    def create_quote_line_item_model(self, order_item) -> QuoteLineItem:

        item_ref = str(order_item['part_number'])
        sal = str(order_item['sales_unit'])
        quantity = int(order_item['make_quantity'])
        unit_price = int(order_item['unit_price'])
        sal_stk_conv = "1"
        stock = "EA"
        gross_price = unit_price
        tax_level_1 = "NTX"

        # instantiate the item model
        sage_quote_line_item = QuoteLineItem()

        # set the models vals
        sage_quote_line_item.item_ref = item_ref
        sage_quote_line_item.sal = sal
        sage_quote_line_item.quantity = quantity
        sage_quote_line_item.sal_stk_conv = sal_stk_conv
        sage_quote_line_item.stock = stock
        sage_quote_line_item.gross_price = gross_price
        sage_quote_line_item.tax_level_1 = tax_level_1

        return sage_quote_line_item
