from baseintegration.datamigration import logger
from baseintegration.exporter.processor import BaseProcessor
from paperless.objects.orders import Order
from sage.models.converters.quote_order_export.paperless_quote_to_sage_quote import PaperlessOrderToSageQuote
from sage.sage_api.client import SageImportClient
from sage.models.converters.quote_order_export.paperless_quote_line_item import PaperlessLineItemToSageLineItem
from paperless.objects.quotes import Quote
from sage.utils import ItemData


class SalesQuoteProcessor(BaseProcessor):

    def _process(self, order: Order, line_item_data) -> list:
        client = SageImportClient.get_instance()
        self.order = order
        self.manufactured_components = []
        self.purchased_components = []

        sales_quote_header = self.create_sales_quote_header(order)
        order_components = self.get_all_components_on_order(line_item_data)
        for order_component in order_components:
            if order_component is None:
                order_components.remove(order_component)
        sales_quote_line_items_converted_sage_quote_line_items = self.convert_to_sage_line_items(order_components)
        sage_sales_quote_header_with_line_items = PaperlessOrderToSageQuote.create_sales_quote_model(self,
                                                                                                     sales_quote_header,
                                                                                                     sales_quote_line_items_converted_sage_quote_line_items)
        client.create_sales_quote(sage_sales_quote_header_with_line_items)

    def create_sales_quote_header(self, order):
        created_date = str(order.created_dt).split()[0].replace('-', '')
        erp_code = Quote.get(order.quote_number, order.quote_revision_number).customer.company.erp_code
        sales_quote_header = {
            'sales_site': 'ARC01',
            'quote_type': 'SQN',
            'reference': 'ITS WORKING',
            'quote_date': created_date,
            'customer_id': erp_code,
            'currency': 'USD',
            'delivery_address': 'BILL',
            'shipment_site': 'ARC01',
            'line_items': []
        }
        return sales_quote_header

    def get_all_components_on_order(self, line_item_data):
        components_to_add_as_quote_line_items = []

        amount_of_line_item_data_to_process = len(line_item_data)
        if amount_of_line_item_data_to_process == 1:
            logger.info('1 line item to process')
            manufactured_components = line_item_data[0].manufactured_components
            purchased_components = line_item_data[0].purchased_components

            for manufactured_component in manufactured_components:
                stripped_component = self.get_information_about_manufactured_component(manufactured_component)
                components_to_add_as_quote_line_items.append(stripped_component)

            for purchased_component in purchased_components:
                stripped_component = self.get_information_about_purchased_component(purchased_component)
                components_to_add_as_quote_line_items.append(stripped_component)
        else:
            logger.info(f'------multiple line items to process, {len(line_item_data)}----------')
            for line_item in line_item_data:
                manufactured_components = line_item.manufactured_components
                purchased_components = line_item.purchased_components

                for manufactured_component in manufactured_components:
                    stripped_component = self.get_information_about_manufactured_component(manufactured_component)
                    components_to_add_as_quote_line_items.append(stripped_component)

                for purchased_component in purchased_components:
                    stripped_component = self.get_information_about_purchased_component(purchased_component)
                    components_to_add_as_quote_line_items.append(stripped_component)

        return components_to_add_as_quote_line_items

    def get_information_about_manufactured_component(self, item):
        type_of_item = type(item)
        stripped_component_as_obj = {}

        if type_of_item is ItemData:
            unit_price = item.unit_price
            make_quantity = item.component.make_quantity
            part_number = item.part_number
            sales_unit = item[9].product.sales_unit

            stripped_component_as_obj['unit_price'] = unit_price
            stripped_component_as_obj['make_quantity'] = make_quantity
            stripped_component_as_obj['part_number'] = part_number
            stripped_component_as_obj['sales_unit'] = sales_unit

            return stripped_component_as_obj

        if type_of_item is list and len(item) != 0:
            logger.info('----------is a list, nothing in it--------------')
            return

        if type_of_item is list and len(item) != 0:
            logger.info('---------is a list and has length more then 0--------------')

            unit_price = item[0].unit_price
            make_quantity = item[0].component.make_quantity
            part_number = item[0].part_number
            sales_unit = item[0].sage_part_record.product.sales_unit

            stripped_component_as_obj['unit_price'] = unit_price
            stripped_component_as_obj['make_quantity'] = make_quantity
            stripped_component_as_obj['part_number'] = part_number
            stripped_component_as_obj['sales_unit'] = sales_unit

            return stripped_component_as_obj

    def get_information_about_purchased_component(self, item):

        stripped_component_as_obj = {}

        part_number = item.component_data.part_number
        unit_price = item.component_data.unit_price
        make_quantity = item.component_data.component.make_quantity
        sales_unit = item[0].sage_part_record.product.sales_unit

        stripped_component_as_obj['unit_price'] = unit_price
        stripped_component_as_obj['make_quantity'] = make_quantity
        stripped_component_as_obj['part_number'] = part_number
        stripped_component_as_obj['sales_unit'] = sales_unit

        return stripped_component_as_obj

    def convert_to_sage_line_items(self, sales_quote_line_items):
        converted_line_items = []
        for quote_line_item in sales_quote_line_items:
            line_item = PaperlessLineItemToSageLineItem.create_quote_line_item_model(self, quote_line_item)
            converted_line_items.append(line_item)
        return converted_line_items
