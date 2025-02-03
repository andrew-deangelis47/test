from paperless.objects.orders import Order
from baseintegration.exporter import logger
from epicor.quote import QuoteHeader, QuoteDetail, QuoteQuantity
from epicor.miscellaneous_charges import QuoteMiscellaneousCharge, MiscCharge
from typing import Optional, List
from epicor.utils import QuoteHeaderData
from decimal import Decimal
from epicor.exporter.v2_processors.base import EpicorProcessor


class QuoteAddOnChargeProcessor(EpicorProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'add_ons'

    def _process(self, order: Order, quote_header: QuoteHeader, quote_details_list: List[QuoteDetail],
                 quote_header_data: Optional[QuoteHeaderData] = None):
        logger.info(f"Processing additional charge for order: {order.number}")
        self.line_items: list = quote_header_data.line_items
        add_on_list: list = []

        try:
            for i, order_item in enumerate(order.order_items):
                for pp_add_on_charge in order_item.ordered_add_ons:
                    if self._exporter.erp_config.add_ons_should_create_line_items:
                        line_item_misc_charge = self.create_line_item_from_add_on(pp_add_on_charge, quote_details_list, i)
                    else:
                        # Get or create Epicor add on charge, associate it with the quote detail.
                        epicor_misc_charge = self.get_or_create_add_on_charge(pp_add_on_charge)
                        # get_or_create_add_on_charge can return None - in this case, it will error if we try to create it
                        line_item_misc_charge = None
                        if epicor_misc_charge:
                            line_item_misc_charge = self.associate_epicor_misc_charge_with_quote_detail(
                                epicor_misc_charge, quote_header, i, pp_add_on_charge)

                    if line_item_misc_charge:
                        add_on_list.append(line_item_misc_charge)
        except Exception as e:
            logger.info(f'Unexpected error in QuoteAddOnChargeProcessor: {e}')
            self._add_report_message(f'Error occured while creating add on charges. Created {len(add_on_list)} add on{"s" if len(add_on_list) > 1 or len(add_on_list) == 0 else ""}. Please contact support.')
            raise e

        self._add_report_message(f'Created {len(add_on_list)} add on{"s" if len(add_on_list) > 1 or len(add_on_list) == 0 else ""}.')
        return add_on_list

    def get_or_create_add_on_charge(self, pp_add_on):
        # Attempt to GET Epicor Misc Charge object - check for ERP CODE first, then check by name
        epicor_misc_charge = None
        if pp_add_on.add_on_definition_erp_code:
            epicor_misc_charge = self.get_epicor_misc_charge(pp_add_on.add_on_definition_erp_code)
        if not epicor_misc_charge:
            epicor_misc_charge = self.get_epicor_misc_charge(pp_add_on.name)
        if not epicor_misc_charge and self._exporter.erp_config.add_ons_should_create_new_misc_charges:
            epicor_misc_charge = self.create_epicor_misc_charge(pp_add_on)
        elif not epicor_misc_charge:
            default_misc_charge = self._exporter.erp_config.default_misc_charge_code
            epicor_misc_charge = self.get_epicor_misc_charge(default_misc_charge)
        return epicor_misc_charge

    def get_epicor_misc_charge(self, pp_add_on_name):
        try:
            # Get by Epicor misc charge code
            epicor_misc_charge = MiscCharge.get_by(field_name="MiscCode", value=str(pp_add_on_name[:4]))
            return epicor_misc_charge
        except Exception as e:
            misc_code_error = e
        try:
            # Get by Epicor misc charge description
            epicor_misc_charge = MiscCharge.get_by(field_name="Description", value=str(pp_add_on_name))
            return epicor_misc_charge
        except Exception as e:
            logger.info(f"Could not find Epicor MiscCharge by MiscCode or Description: {misc_code_error}, {e}")
            return None

    def create_epicor_misc_charge(self, pp_add_on):
        logger.info(f"Attempting to create new Epicor MiscCharge from Paperless Add On: {pp_add_on.name}")
        epicor_misc_charge = None
        description = self.get_misc_charge_description(pp_add_on)

        try:
            epicor_misc_charge = MiscCharge(
                Company=str(self._exporter.erp_config.company_name),
                MiscCode=str(pp_add_on.name[:4]),
                Description=description,
                FreqCode="F",  # "First time only"
                MiscAmt=pp_add_on.price.raw_amount,
                Type="A",  # "Amount"
            ).create_instance()
        except Exception as e:
            logger.info(f"Could not create additional charge object in Epicor. {e}")

        return epicor_misc_charge

    def get_misc_charge_description(self, pp_add_on):
        if not pp_add_on.notes:
            return str(pp_add_on.name[:30])
        return str(pp_add_on.notes[:30])

    def associate_epicor_misc_charge_with_quote_detail(self, epicor_misc_charge, quote_header: QuoteHeader, i,
                                                       pp_add_on):
        epicor_quote_misc_charge = None
        try:
            epicor_quote_misc_charge = QuoteMiscellaneousCharge(
                Company=str(self._exporter.erp_config.company_name),
                QuoteNum=quote_header.QuoteNum,
                QuoteLine=int(i + 1),
                MiscCode=epicor_misc_charge.MiscCode,
                Description=epicor_misc_charge.Description,
                MiscAmt=pp_add_on.price.raw_amount,
                DocMiscAmt=pp_add_on.price.raw_amount,
                DspMiscAmt=pp_add_on.price.raw_amount,
                DocDspMiscAmt=pp_add_on.price.raw_amount,
                FreqCode="F",
            ).create_instance()
        except Exception as e:
            logger.info(f"Could not associate MiscCharge with epicor quote header: {quote_header.QuoteNum}\n{e}")
        return epicor_quote_misc_charge

    def create_line_item_from_add_on(self, pp_add_on_charge, quote_details_list, i):
        logger.info("Attempting to create line item from add on...")
        copy_from_quote_detail = quote_details_list[i]

        quote_detail = QuoteDetail(
            Company=str(self._exporter.erp_config.company_name),
            CustNum=int(copy_from_quote_detail.CustNum),
            CustomerCustID=str(copy_from_quote_detail.CustomerCustID),
            QuoteNum=int(copy_from_quote_detail.QuoteNum),
            QuoteLine=int(len(quote_details_list) + 1),
            PartNum=str(self._exporter.erp_config.default_line_item_add_on_part_number),
            ProdCode=copy_from_quote_detail.ProdCode,
            LineDesc=str(pp_add_on_charge.name),
            OrderQty=1,
            SellingExpectedQty=1,
            Engineer=bool(copy_from_quote_detail.Engineer),
            ReadyToQuote=bool(copy_from_quote_detail.ReadyToQuote),
            QuoteComment=str(pp_add_on_charge.notes),
            Template=bool(copy_from_quote_detail.Template),
        ).create_instance()

        QuoteQuantity(
            Company=str(self._exporter.erp_config.company_name),
            QuoteNum=quote_detail.QuoteNum,
            QuoteLine=quote_detail.QuoteLine,
            QtyNum=1,
            OurQuantity=1,  # Add-on qty is always 1 because it applies independently of quantity
            UnitPrice=Decimal(pp_add_on_charge.price.raw_amount)
        ).create_instance()

        logger.info(f"Created line item {copy_from_quote_detail.QuoteNum} - {quote_detail.QuoteLine} "
                    f"from Paperless Parts Add On: {pp_add_on_charge.name}")
        quote_details_list.append(quote_detail)

        return quote_detail
