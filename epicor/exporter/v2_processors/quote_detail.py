from paperless.objects.orders import Order, OrderItem, OrderComponent
from baseintegration.exporter import logger
from epicor.quote import QuoteHeader, QuoteDetail
from epicor.part import Part
from typing import Optional, Union
from epicor.utils import QuoteHeaderData, CustomerData, get_item_data_by_component_id, ItemData
from math import ceil
from epicor.exporter.v2_processors.base import EpicorProcessor


class QuoteDetailProcessor(EpicorProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'quote_lines'

    def _process(self, order: Order, customer: CustomerData, quote_header: QuoteHeader,
                 quote_header_data: Optional[QuoteHeaderData] = None):
        try:
            logger.info(f"Processing quote detail for order: {order.number}")
            self.line_items: list = quote_header_data.line_items

            quote_details_list = []
            for i, order_item in enumerate(order.order_items):
                quote_detail = self.create_quote_detail(customer, order_item, quote_header, i)
                quote_details_list.append(quote_detail)
        except Exception as e:
            logger.info(f'Unexpected exception in quote detail processor: {e}')
            self._add_report_message(f'Unexpected error occured while creating quote lines. Created {len(quote_details_list)} quote lines. Please contact support.')
            raise e

        self._add_report_message(f'Created {len(quote_details_list)} quote line{"s" if len(quote_details_list) > 1 else ""}.')

        return quote_details_list

    def create_quote_detail(self, customer: CustomerData, order_item: OrderItem, quote_header: QuoteHeader, i: int)\
            -> QuoteDetail:

        customer_pk, customer_user_num = self.get_customer_code(customer)
        quote_num = quote_header.QuoteNum
        root_component_id = self._get_root_component_id(i)
        item_data: ItemData = get_item_data_by_component_id(self.line_items[i].manufactured_components,
                                                            root_component_id)
        epicor_part_record = item_data.epicor_part_record
        part_number = item_data.part_number

        prod_code = self._get_epicor_part_prod_code(epicor_part_record)
        if self._exporter.erp_config.set_quote_line_item_prod_code_from_first_pp_op is True:
            prod_code = self._get_epicor_prod_code_from_first_shop_operation(order_item, i, prod_code)

        sales_code = None
        if self._exporter.erp_config.set_quote_line_item_sales_code_from_first_pp_op is True:
            sales_code = self._get_epicor_sales_code_from_first_shop_operation(order_item, i, sales_code)

        quote_line_num = int(i + 1)
        quote_comments = self.get_quote_comments(order_item)
        lead_time = self._get_line_item_lead_time(order_item)

        quote_detail = QuoteDetail(
            Company=str(self._exporter.erp_config.company_name),
            CustNum=customer_pk,
            CustomerCustID=str(customer_user_num),
            QuoteNum=int(quote_num),
            QuoteLine=quote_line_num,
            PartNum=part_number,
            RevisionNum=item_data.revision,
            ProdCode=prod_code,
            SalesCatID=sales_code,
            LineDesc=str(order_item.root_component.description),
            OrderQty=int(order_item.root_component.deliver_quantity),
            SellingExpectedQty=int(order_item.root_component.deliver_quantity),
            Engineer=False,  # Must be False upon creation. This parameter is set after exporter processors are complete
            ReadyToQuote=False,  # Must also be False for the same reason^
            QuoteComment=quote_comments,
            Template=bool(self._exporter.erp_config.should_mark_quote_lines_as_template),
            LeadTime=lead_time,
        ).create_instance()
        logger.info(f"Created quote item: {quote_num} - {quote_detail.QuoteLine}")

        line_item_data = self.line_items[i]._replace(quote_detail_number=quote_line_num)
        self.line_items[i] = line_item_data

        return quote_detail

    def get_customer_code(self, cust: CustomerData) -> tuple:
        customer_pk = int(cust.customer.CustNum)  # Customer PK ID
        customer_user_num = str(cust.customer.CustID)  # User-defined customer number

        return customer_pk, customer_user_num

    def get_quote_comments(self, order_item: OrderItem) -> Union[str, None]:
        """
        - Combines the part viewer URL, public notes, and private notes into a single note -> Epicor quote line item quote comments
        """
        complete_note = ""
        if self._exporter.erp_config.should_add_pp_part_viewer_link_to_quote_comments:
            part_viewer_url = f"https://app.paperlessparts.com/parts/viewer/{order_item.root_component.part_uuid}"
            logger.info(f"Adding Paperless Parts Part Viewer URL to comments on quote detail: {part_viewer_url}")
            complete_note += f"Paperless Parts Part Viewer URL:\n{part_viewer_url}\n\n"
        if self._exporter.erp_config.should_add_public_pp_notes_to_quote_detail:
            public_notes = order_item.public_notes
            if public_notes is not None and public_notes != "":
                complete_note += f"Paperless Parts Public Notes:\n{public_notes}\n\n"
        if self._exporter.erp_config.should_add_private_pp_notes_to_quote_detail:
            private_notes = order_item.private_notes
            if private_notes is not None and private_notes != "":
                complete_note += f"Paperless Parts Private Notes:\n{private_notes}"
        return complete_note

    def _get_line_item_lead_time(self, order_item: OrderItem) -> str:
        """
        - Returns the converted lead days based on the input configuration preference
        - Paperless API only returns lead time in days, hence the concept of business weeks
        - The function will compute how many days or weeks are
        """
        logger.info("Getting lead time and lead time units for line item.")

        lead_time_preference = self._exporter.erp_config.lead_time_unit_preference
        lead_days_dict: dict = {
            "business_days": 1,
            "business_weeks": 5,
            "calendar_days": 1,
            "calendar_weeks": 7
        }

        # Convert lead time to correct number of days/weeks depending on preference. Format units to "days" or "weeks"
        converted_lead_time = ceil(order_item.lead_days / lead_days_dict.get(lead_time_preference, 1))
        formatted_units = lead_time_preference.replace("_", " ")

        # Remove the "business" vs. "calendar" from the weeks units so that it just says "weeks"
        if "weeks" in formatted_units:
            formatted_units = "weeks"

        return f"{converted_lead_time} {formatted_units}"[:20]

    def _get_root_component_id(self, i: int) -> Union[None, int]:
        for mfg_comp in self.line_items[i].manufactured_components:
            if mfg_comp.component.is_root_component:
                return mfg_comp.component.id
        return None

    def _get_epicor_part_prod_code(self, epicor_part_record: Part) -> str:
        if epicor_part_record is not None and epicor_part_record.ProdCode is not None:
            return str(epicor_part_record.ProdCode)
        return str(self._exporter.erp_config.default_non_root_mfg_product_code)

    def _get_epicor_prod_code_from_first_shop_operation(self, order_item: OrderItem, i: int, prod_code: str) -> str:
        for comp_number, component in enumerate(order_item.components):
            if comp_number == i:
                component: OrderComponent
                first_operation = component.shop_operations[0] if len(component.shop_operations) > 0 else None
                if first_operation is not None:
                    prod_code = first_operation.get_variable("epicor_line_item_prod_code")
                    if prod_code is not None:
                        return prod_code

        return prod_code

    def _get_epicor_sales_code_from_first_shop_operation(self, order_item: OrderItem, i: int,
                                                         sales_code: Union[str, None]) -> str:
        for comp_number, component in enumerate(order_item.components):
            if comp_number == i:
                component: OrderComponent
                first_operation = component.shop_operations[0] if len(component.shop_operations) > 0 else None
                if first_operation is not None:
                    sales_code = first_operation.get_variable("epicor_line_item_sales_code")
                    if sales_code is not None:
                        return sales_code

        return sales_code
