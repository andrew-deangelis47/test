from baseintegration.utils import logger, safe_get
from typing import List
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.repeat_work_objects import AddOn
from epicor.quote import QuoteDetail
from epicor.importer.utils import (
    RepeatPartUtilObject,
    QuoteMOMUtil
)


class AddOnProcessor(BaseImportProcessor):

    def _process(self, repeat_part_util_object: RepeatPartUtilObject) -> RepeatPartUtilObject:
        logger.info("Add On Processor - Attempting to create Add Ons")

        for quote_mom_util in repeat_part_util_object.quote_mom_utils:
            quote_mom_util: QuoteMOMUtil = quote_mom_util
            quote_mom_util.add_ons = self.create_quote_add_ons(quote_mom_util)

        return repeat_part_util_object

    def create_quote_add_ons(self, quote_mom_util: QuoteMOMUtil):
        quote_detail: QuoteDetail = quote_mom_util.epicor_quote_detail

        quote_add_ons: List[AddOn] = []
        for misc_charge in quote_detail.QuoteMscs:
            add_on = AddOn(
                is_required=False,
                name=str(safe_get(misc_charge, "MiscCode", "Unknown")),
                notes=str(safe_get(misc_charge, "Description", "")),
                unit_price=float(safe_get(misc_charge, "MiscAmt", 0)),
                use_component_quantities=False,
            )
            quote_add_ons.append(add_on)

        return quote_add_ons
