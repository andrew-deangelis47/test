from plex_v2.factories.plex.sales_order_release import SalesOrderReleaseFactory
from plex_v2.configuration import PlexConfig
from unittest.mock import create_autospec
from plex_v2.utils.export import ExportUtils
from paperless.objects.orders import OrderItem
from plex_v2.objects.sales_orders import SalesOrderLine
import datetime


class TestPlexCustomerFactory:

    # required config values
    DEFAULT_SHIP_FROM_BUILDING_CODE = 'DEFAULT_SHIP_FROM_BUILDING_CODE'
    DEFAULT_SALES_ORDER_RELEASE_STATUS = 'DEFAULT_SALES_ORDER_RELEASE_STATUS'
    DEFAULT_SALES_ORDER_RELEASE_TYPE = 'DEFAULT_SALES_ORDER_RELEASE_TYPE'

    # required for parameters of function
    ORDER_ITEM_QUANTITY = 2
    ORDER_ITEM_SHIPS_ON_DATE = '2024-06-13'
    EXPECTED_SHIPS_ON_DATE_STR = '2024-06-13T23:59:59+00:00'
    DATE_FMT = '%Y-%m-%d'

    SHIP_TO_ADDRESS_ID = 'SHIP_TO_ADDRESS_ID'

    SALES_ORDER_LINE_ID = 'SALES_ORDER_LINE_ID'

    def setup_method(self):

        def ships_on_side_effect():
            return self.ORDER_ITEM_SHIPS_ON_DATE

        # setup required config values
        config = create_autospec(PlexConfig)
        config.default_ship_from_building_code = self.DEFAULT_SHIP_FROM_BUILDING_CODE
        config.default_sales_order_release_status = self.DEFAULT_SALES_ORDER_RELEASE_STATUS
        config.default_sales_order_release_type = self.DEFAULT_SALES_ORDER_RELEASE_TYPE

        # setup required utils value
        utils = create_autospec(ExportUtils)

        # get required parameters for the function
        order_item = create_autospec(OrderItem)
        order_item.quantity = self.ORDER_ITEM_QUANTITY
        # this is how date is calculated in the real object - we want to replicate that
        order_item.ships_on_dt = datetime.datetime.strptime(self.ORDER_ITEM_SHIPS_ON_DATE, self.DATE_FMT)

        sales_order_line = create_autospec(SalesOrderLine)
        sales_order_line.id = self.SALES_ORDER_LINE_ID

        # setup class and make function call
        factory = SalesOrderReleaseFactory(config, utils)
        self.sales_order_release = factory.to_sales_order_release(
            order_item,
            self.SHIP_TO_ADDRESS_ID,
            sales_order_line
        )

    def test_to_sales_order_release_sets_quantity_to_order_item_qty(self):
        assert self.sales_order_release.quantity == self.ORDER_ITEM_QUANTITY

    def test_to_sales_order_release_sets_ships_from_to_config_default(self):
        assert self.sales_order_release.shipFrom == self.DEFAULT_SHIP_FROM_BUILDING_CODE

    def test_to_sales_order_release_sets_status_to_config_default(self):
        assert self.sales_order_release.status == self.DEFAULT_SALES_ORDER_RELEASE_STATUS

    def test_to_sales_order_release_sets_type_to_config_default(self):
        assert self.sales_order_release.type == self.DEFAULT_SALES_ORDER_RELEASE_TYPE

    def test_to_sales_order_release_sets_ship_to_addr_id_to_what_is_passed_to_function(self):
        assert self.sales_order_release.shipToAddressId == self.SHIP_TO_ADDRESS_ID

    def test_to_sales_order_release_sets_due_date_to_one_day_from_order_item_ship_date(self):
        assert self.sales_order_release.dueDate == self.EXPECTED_SHIPS_ON_DATE_STR

    def test_to_sales_order_release_sets_order_line_id_to_id_of_order_line_passed_to_function(self):
        assert self.sales_order_release.dueDate == self.EXPECTED_SHIPS_ON_DATE_STR
