from typing import List
from plex_v2.objects.part import Part
from paperless.objects.purchased_components import PurchasedComponent as PaperlessPurchasedComponent
from baseintegration.datamigration import logger
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from plex_v2.importer.processors.base import PlexImportProcessor
import time


class PurchasedComponentBulkImportProcessor(PlexImportProcessor):

    def _process(self, purchased_comp_ids: List[int]):
        pc_list: List[PaperlessPurchasedComponent] = []
        for purchased_comp_id in purchased_comp_ids:

            # 0) get the parts for the part number
            logger.info(f"Processing purchased component: {str(purchased_comp_id)}")
            part_list: List[Part] = Part.search(number=purchased_comp_id)

            if len(part_list) == 0:
                logger.error(f'Did not find part {purchased_comp_id}, skipping import and removing if it is in Paperless PC list')
                continue

            part: Part
            for part in part_list:

                # 1) make sure status is valid
                if part.status not in self.config.part_statuses_active:
                    logger.info(f'Part {part.number} rev {part.revision} is not active (status is {part.status}), skipping')
                    continue

                # 2) make sure the type is valid
                if part.type not in self.config.purchased_component_types:
                    logger.info(f'Part {part.number} rev {part.revision} is not a valid type (type is {part.type}), skipping')
                    continue

                # 2) create the model
                paperless_pc: PaperlessPurchasedComponent = self._importer.purchased_component_factory.to_pp_purchased_component(part)

                # 3) make sure this oem part number is not already in the payload or else it will cause an error
                compare_list = [x.oem_part_number for x in pc_list]
                if paperless_pc.oem_part_number not in compare_list:
                    pc_list.append(paperless_pc)

            # 4) if we are using material pricing we need to update in chunks - otherwise the data sources used for pricing get overwhelmed
            if self.config.should_import_pc_pricing and len(pc_list) > 49:
                self._bulk_upload_pcs(pc_list)
                time.sleep(20)
                pc_list = []

        # if we are not importing pricing we can just upload all PCs in one go
        return self._bulk_upload_pcs(pc_list)

    def _bulk_upload_pcs(self, pc_list: List[PaperlessPurchasedComponent]) -> bool:
        """
        upload a set of purchased components
        """
        try:
            logger.info(f"Attemping to update/insert {len(pc_list)} components: {', '.join([pc.oem_part_number for pc in pc_list])}")
            result = PaperlessPurchasedComponent.upsert_many(pc_list)
        except Exception as e:
            logger.info('Error while bulk updating purchased components')
            logger.info(e)
            raise CancelledIntegrationActionException(e)

        if len(result.failures) > 0:
            raise CancelledIntegrationActionException(result.failures[0].error)

        return len(result.failures) == 0


class PurchasedComponentImportProcessor(PurchasedComponentBulkImportProcessor):

    def _process(self, component_id: str) -> bool:
        return super()._process([component_id])


class PurchasedComponentBulkPlaceholder:
    pass
