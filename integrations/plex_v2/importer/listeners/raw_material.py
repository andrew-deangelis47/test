from plex_v2.objects.part import Part
from plex_v2.configuration import PlexConfig
from baseintegration.utils import get_last_action_datetime
from pendulum.datetime import DateTime
from datetime import datetime
from baseintegration.datamigration import logger


class PLEXRawMaterialListener:
    identifier = "raw_material"

    def __init__(self, integration, erp_config: PlexConfig):
        self._integration = integration
        self._erp_config = erp_config

    def get_new(self, bulk=False):

        now: str = datetime.now().isoformat()
        last_action_date: DateTime = get_last_action_datetime(self._integration.managed_integration_uuid,
                                                              self.identifier,
                                                              bulk=bulk)

        material_ids = []
        for raw_material_class in self._erp_config.raw_material_classes:
            materials = Part.search(type=raw_material_class)
            material: Part
            for material in materials:
                # only process updated parts
                if self._was_updated_since_last_run(material, last_action_date, now):
                    # only process parts with valid status
                    if self._is_valid_status(material):
                        material_ids.append(material.number)

        return material_ids

    def _was_updated_since_last_run(self, material: Part, last_action_date: DateTime, now: str) -> bool:
        material_update_date: str = now
        if material.modifiedDate is not None and material.modifiedDate != '':
            material_update_date = material.modifiedDate
        elif material.createdDate is not None and material.createdDate != '':
            material_update_date = material.createdDate

        modified_date = datetime.fromisoformat(material_update_date.replace('Z', ''))  # Zulu Timestamp conversion

        return modified_date > last_action_date

    def _is_valid_status(self, component: Part) -> bool:
        if component.status not in self._erp_config.part_statuses_active:
            logger.debug(f'Skipping {component.number} - status filter exclusion, current status is {component.status}')
            return False
        return True
