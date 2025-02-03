import decimal

import pytest

from globalshop.order import OrderLineRecord


class TestOrder:

    @pytest.fixture
    def dummy_order(self):
        return OrderLineRecord(
            external_order_no='external_order_no',
            transaction_code='transaction_code',
            gss_customer_no='gss_customer_no',
            external_customer_no='external_customer_no',
            order_no='order_no',
            line_number=1,
            linetype='linetype',
            gss_partnumber='gss_partnumber',
            ext_partnumber='ext_partnumber',
            qty_ordered=1,
            line_total_price=decimal.Decimal('5.5'),
            line_unit_price=decimal.Decimal('5.5'),
            price_before_discount=decimal.Decimal('5.5'),
            # order_discount_percent:decimal.Decimal
            # part_loc:str
            order_due_date=None,
            # Defaults to today
            order_date=None,
            # only if different from order_date
            line_order_date=None,
            line_promise_date=None,
            freight=None,
            # freight_per_piece:decimal.Decimal
            user_field_1_head='qty_ordered',
            user_field_2_head='qty_ordered',
            user_field_3_head='qty_ordered',
            user_field_4_head='qty_ordered',
            user_field_5_head='qty_ordered',
            ship_via='qty_ordered',
            carrier='qty_ordered',
            # default empty
            part_loc='part_loc',
            ship_to_id='qty_ordered',
            # default False
            ship_to_intl_flag=False,
            ship_to_name='qty_ordered',
            ship_to_address_1='qty_ordered',
            ship_to_address_2='qty_ordered',
            ship_to_address_3='qty_ordered',
            ship_to_city='qty_ordered',
            ship_to_state='qty_ordered',
            ship_to_zip='qty_ordered',
            ship_to_country='qty_ordered',
            ship_to_attention='qty_ordered',
            ship_to_contact_name='qty_ordered',
            ship_to_contact_email='qty_ordered',
            bill_to_intl_flag=False,
            bill_to_name='qty_ordered',
            bill_to_address_1='qty_ordered',
            bill_to_address_2='qty_ordered',
            bill_to_address_3='qty_ordered',
            bill_to_city='qty_ordered',
            bill_to_state='qty_ordered',
            bill_to_zip='qty_ordered',
            bill_to_country='qty_ordered',
            bill_to_attention='qty_ordered',
            order_sort='qty_ordered',
            order_sort_2='qty_ordered',
            user_field_1_line='qty_ordered',
            user_field_2_line='qty_ordered',
            user_field_3_line='qty_ordered',
            user_field_4_line='qty_ordered',
            user_field_5_line='qty_ordered',
            addl_comments_head='qty_ordered',
            addl_comments_line='qty_ordered',
            customer_po='qty_ordered',
            order_loc='order_loc',
            # defaults to False
            # prosepect:bool
            # order_location:str
            # line_taxes:decimal.Decimal
            salesperson_code='qty_ordered',
            line_unit_cost=decimal.Decimal('5.5'),
            part_description='qty_ordered',
            terms='qty_ordered',
            # markshipment:?
            # Default False
            # shiphold:bool
            part_um='qty_ordered',
            quote_status='qty_ordered',
            approved=False,
            commission_type_code='qty_ordered',
            ship_to_address_4='qty_ordered',
            ship_to_address_5='qty_ordered',
            customer_part='')

    def test_create_rec(self, dummy_order):
        assert dummy_order
        assert dummy_order.external_order_no == 'external_order_no'
