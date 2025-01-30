from typing import List

from baseintegration.datamigration import logger
from paperless.objects.purchased_components import PurchasedComponent
from m2m.configuration import M2MConfiguration
from m2m.importer.processors.base import BaseM2MImportProcessor

import m2m.models as mm


class M2MPurchasedComponentBulkImportProcessor(BaseM2MImportProcessor):
    def _process(self, part_numbers: List[str]) -> bool:
        return self.bulk_import(part_numbers=part_numbers)

    def bulk_import(self, part_numbers: List[str]) -> bool:
        purchase_component_list = []
        for part_number in part_numbers:
            item: mm.Inmastx = mm.Inmastx.objects.filter(fpartno=part_number).first()
            config: M2MConfiguration = self._importer._m2m_config

            if config.purchase_use_total_cost:
                piece_price = f'{round(item.f2totcost, 4)}'
            else:
                piece_price = f'{round(item.fstdcost, 4)}'
            description = f'{item.fdescript}'
            q_part_number = f'{item.fpartno}'.strip()
            purchased_component = PurchasedComponent(piece_price=piece_price, oem_part_number=q_part_number,
                                                     internal_part_number=q_part_number, description=description)
            purchase_component_list.append(purchased_component)
            logger.debug(f'added {purchased_component.oem_part_number} to bulk list.')
        result = PurchasedComponent.upsert_many(purchase_component_list)
        if len(result.failures) > 0:
            return False
        return True


class M2MPurchasedComponentImportProcessor(M2MPurchasedComponentBulkImportProcessor):
    def _process(self, part_number: str) -> bool:
        return self.bulk_import(part_numbers=[part_number])


class M2MPurchasedComponentBulkPlaceholder:
    pass
