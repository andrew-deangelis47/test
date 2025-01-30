from plex_v2.factories.plex.approved_ship_to import ApprovedShipToFactory
from plex_v2.configuration import PlexConfig
from unittest.mock import create_autospec
from plex_v2.objects.sales_orders import SalesOrderLine
from plex_v2.utils.export import ExportUtils


class TestApprovedShipToFactory:

    VALID_SHIP_TO_ADDR = 'ship_to_addr_id'
    VALID_SHIP_FROM_BUILDING_CODE = 'valid_ship_from_building_code'
    VALID_SALES_ORDER_ID = 'valid_sales_order_id'
    VALID_SALES_ORDER_LINE_ID = 'valid_sales_order_line_id'

    def setup_method(self):
        self.config = create_autospec(PlexConfig)
        self.config.default_ship_from_building_code = self.VALID_SHIP_FROM_BUILDING_CODE

        self.utils = create_autospec(ExportUtils)

        self.ship_to_addr_id = self.VALID_SHIP_TO_ADDR

        self.sales_order_line = create_autospec(SalesOrderLine)
        self.sales_order_line.order_id = self.VALID_SALES_ORDER_ID
        self.sales_order_line.id = self.VALID_SALES_ORDER_LINE_ID

        self.factory = ApprovedShipToFactory(
            config=self.config,
            utils=self.utils
        )

    def test_approved_ship_to_factory_sets_ship_to_addr_id_to_what_is_passed_as_argument(self):
        approved_ship_to = self.factory.to_approved_ship_to(
            self.ship_to_addr_id,
            self.sales_order_line
        )

        assert approved_ship_to.shipToAddressId == self.ship_to_addr_id

    def test_approved_ship_to_factory_sets_default_ship_from_code_to_config_value(self):
        approved_ship_to = self.factory.to_approved_ship_to(
            self.ship_to_addr_id,
            self.sales_order_line
        )

        assert approved_ship_to.defaultShipFromCode == self.config.default_ship_from_building_code

    def test_approved_ship_to_factory_sets_order_id_to_order_line_order_id(self):
        approved_ship_to = self.factory.to_approved_ship_to(
            self.ship_to_addr_id,
            self.sales_order_line
        )

        assert approved_ship_to.order_id == self.sales_order_line.order_id

    def test_approved_ship_to_factory_sets_line_id_to_id_of_order_line_passed_in(self):
        approved_ship_to = self.factory.to_approved_ship_to(
            self.ship_to_addr_id,
            self.sales_order_line
        )

        assert approved_ship_to.line_id == self.sales_order_line.id
