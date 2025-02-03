from typing import List

from baseintegration.importer.import_processor import BaseImportProcessor
from inforsyteline.models import ItemMst
from baseintegration.datamigration import logger
from paperless.objects.purchased_components import PurchasedComponent


class PurchasedComponentBulkImportProcessor(BaseImportProcessor):

    def _process(self, purchased_component_ids: List[str]) -> bool:
        purchased_component_list = []
        for purchased_component_id in purchased_component_ids:
            logger.info(f"Processing {purchased_component_id}")
            estim_row: ItemMst = ItemMst.objects.filter(item=purchased_component_id).first()

            if not estim_row:
                logger.info(f"Object w ID {purchased_component_id} could not be found in E2. Skipping")
                continue

            piece_price = self.get_piece_price(estim_row)
            oem_part_number = self.get_oem_part_number(estim_row)
            description = self.get_description(estim_row)

            purchased_component = PurchasedComponent(
                piece_price=piece_price,
                oem_part_number=oem_part_number,
                internal_part_number=None,
                description=description)
            purchased_component_list.append(purchased_component)

        result = PurchasedComponent.upsert_many(purchased_component_list)
        return len(result.failures) == 0

    def get_piece_price(self, estim_row):
        try:
            piece_price = estim_row.unit_cost
            if piece_price < 0:
                piece_price = 0.0
        except (ZeroDivisionError, TypeError):
            piece_price = 0.0
        piece_price = str(round(piece_price, 4))[0:10]
        return piece_price

    def get_oem_part_number(self, estim_row):
        oem_part_number = estim_row.item
        return oem_part_number

    def get_description(self, estim_row):
        # The Open API does not currently allow blank values for this field, but it does allow None
        description = estim_row.description if estim_row.description else None
        if description is not None:
            description = description[:100]  # The API allows a max length of 100 for this field
        return description


class PurchasedComponentImportProcessor(PurchasedComponentBulkImportProcessor):
    def _process(self, purchased_component_id: str) -> bool:
        return super()._process([purchased_component_id])


class PurchasedComponentBulkPlaceholder:
    pass
