from mietrak_pro.exporter.processors import MietrakProProcessor
from baseintegration.datamigration import logger

from mietrak_pro.query.sales_order import create_sales_order_line
import mietrak_pro.models
from datetime import datetime
from paperless.objects.orders import OrderItem, Order, OrderedAddOn


class AddOnSalesOrderLineProcessor(MietrakProProcessor):
    do_rollback = False

    def _process(self, sales_order: mietrak_pro.models.Salesorder,
                 order: Order,
                 order_item: OrderItem,
                 add_on: OrderedAddOn,
                 customer: mietrak_pro.models.Party,
                 part: mietrak_pro.models.Item,
                 shipping_address: mietrak_pro.models.Address,
                 sales_order_line_reference_number: int):

        unit_price = self.get_unit_price(order, order_item, add_on)
        quantity = self.get_quantity(order, order_item, add_on)
        due_date = self.get_due_date(order, order_item, add_on)
        gl_account = self.get_general_ledger_account(order, order_item, customer)

        router = None
        is_part_new = False  # It's not obvious what this field is for, set it to False by default

        logger.info(f'Creating Sales Order Line for part number {part.partnumber} and revision {part.revision}')
        sales_order_line, sales_order_line_lot = create_sales_order_line(sales_order, sales_order_line_reference_number,
                                                                         unit_price, quantity, customer, gl_account,
                                                                         part, router, shipping_address, is_part_new,
                                                                         due_date)

        # There appears to be a stored procedure that runs upon record creation and sets the due date and promise date
        # to the current date. Manually setting these fields overrides that behavior
        sales_order_line_lot.duedate = due_date
        sales_order_line_lot.promisedate = due_date
        sales_order_line_lot.save()

        return sales_order_line

    def get_unit_price(self, order: Order, order_item: OrderItem, add_on: OrderedAddOn):
        return add_on.price.dollars

    def get_quantity(self, order: Order, order_item: OrderItem, add_on: OrderedAddOn):
        return 1

    def get_due_date(self, order: Order, order_item: OrderItem, add_on: OrderedAddOn):
        due_date = datetime.strptime(order_item.ships_on, '%Y-%m-%d')
        return due_date

    def get_general_ledger_account(self, order: Order, order_item: OrderItem, customer: mietrak_pro.models.Party):
        return customer.defaultgeneralledgeraccountfk
