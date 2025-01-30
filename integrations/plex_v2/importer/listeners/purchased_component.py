from plex_v2.objects.part import Part
from plex_v2.configuration import PlexConfig
from baseintegration.utils import get_last_action_datetime
from pendulum.datetime import DateTime
from datetime import datetime
from baseintegration.datamigration import logger
from plex_v2.utils.import_utils import ImportUtils
from paperless.objects.purchased_components import PurchasedComponent
from typing import Union, List


class PLEXPurchasedComponentListener:
    identifier = "purchased_component_import"

    def __init__(self, integration, erp_config: PlexConfig, utils: ImportUtils):
        self._integration = integration
        self._erp_config = erp_config
        self.utils = utils
        self.existing_pc_list = []

    def get_new(self, bulk=False):

        # audit the existing PP PCs for valid status and type
        if self._erp_config.should_audit_existing_pcs:
            self.existing_pc_list: List[PurchasedComponent] = PurchasedComponent.list()
            self.utils.audit_pp_pc_list(self.existing_pc_list)

        now: str = datetime.now().isoformat()
        last_action_date: DateTime = get_last_action_datetime(self._integration.managed_integration_uuid,
                                                              self.identifier,
                                                              bulk=bulk)

        # get all updated PCs
        purchased_component_ids = []
        for purchased_component_class in self._erp_config.purchased_component_types:
            purchased_components = Part.search(type=purchased_component_class)
            component: Part
            for component in purchased_components:
                # only process updated parts
                if self._was_updated_since_last_run(component, last_action_date, now):
                    # check for valid status
                    if self._is_valid_status(component):
                        # check for valid type
                        if self._is_valid_type(component):
                            purchased_component_ids.append(component.number)

        return purchased_component_ids

    def _was_updated_since_last_run(self, material: Part, last_action_date: DateTime, now: str) -> bool:
        # if there is no update time then just include it
        if material.createdDate is None or material.modifiedDate is None:
            return True

        material_update_date: str = now
        if material.modifiedDate is not None and material.modifiedDate != '':
            material_update_date = material.modifiedDate
        elif material.createdDate is not None and material.createdDate != '':
            material_update_date = material.createdDate

        modified_date = datetime.fromisoformat(material_update_date.replace('Z', ''))  # Zulu Timestamp conversion

        return modified_date > last_action_date

    def _is_valid_status(self, component: Part) -> bool:
        if component.status not in self._erp_config.part_statuses_active:
            logger.info(f'Component {component.number} does not have a valid status ("{component.status}"), skipping')
            self._remove_matching_pc(component)
            return False
        return True

    def _is_valid_type(self, component: Part) -> bool:
        if component.type not in self._erp_config.purchased_component_types:
            logger.info(f'Component {component.number} does not have a valid type ("{component.type}"), skipping')
            self._remove_matching_pc(component)
            return False
        return True

    def _get_matching_existing_pc(self, part: Part) -> Union[None, PurchasedComponent]:
        pc: PurchasedComponent
        for pc in self.existing_pc_list:
            # treat None rev the same as blank string
            revision = "" if pc.get_property('revision') is None else pc.get_property('revision')
            if pc.oem_part_number == part.number and revision == part.revision:
                return pc

        return None

    def _remove_matching_pc(self, part: Part) -> None:
        """
        - we need this because there could be an existing PC in the list with a valid
        status or type, but in Plex it is not so we should remove
        - the audit only captures whats in the list - not the corresponding list in Plex
        """
        matching_pc: PurchasedComponent = self._get_matching_existing_pc(part)
        if matching_pc is not None:
            matching_pc.delete()
