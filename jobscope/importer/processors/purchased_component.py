from typing import List

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.datamigration import logger
from paperless.objects.purchased_components import PurchasedComponent


class PurchasedComponentBulkImportProcessor(BaseImportProcessor):

    def _process(self, purchased_component_ids: List[str]):  # noqa: C901
        for purchased_component_id in purchased_component_ids:
            logger.info(f"Processing {purchased_component_id}")
            client = self._importer.client
            logger.info(f"Processing {purchased_component_id}")
            part: dict = client.get_part(purchased_component_id)
            if part:
                purchased_components: list = PurchasedComponent.search(purchased_component_id)
                purchased_component = None
                for pc in purchased_components:
                    purchased_component = pc if pc.oem_part_number == purchased_component_id else None
                piece_price = part["unitCost"]
                if purchased_component:
                    logger.info(f"Purchased component {purchased_component_id} was found in Paperless")
                    is_new = False
                else:
                    logger.info(f"Purchased component {purchased_component_id} was not found in Paperless")
                    purchased_component = PurchasedComponent(piece_price=str(piece_price),
                                                             oem_part_number=purchased_component_id)
                    is_new = True

                purchased_component.piece_price = str(round(piece_price, 4))[0:10]
                purchased_component.oem_part_number = purchased_component_id
                purchased_component.internal_part_number = purchased_component_id
                purchased_component.description = part["description1"] if part["description1"] else 'N/A'
                try:
                    if is_new:
                        purchased_component.create()
                    else:
                        purchased_component.update()
                except Exception as e:
                    logger.info(e)
                    raise Exception(f"Could not import {purchased_component_id}")
            else:
                logger.info(f"Object w ID {purchased_component_id} could not be found in Jobscope. Returning")
                return


class PurchasedComponentImportProcessor(PurchasedComponentBulkImportProcessor):
    def _process(self, purchased_component_id: str):
        return super()._process([purchased_component_id])


class PurchasedComponentBulkPlaceholder:
    pass
