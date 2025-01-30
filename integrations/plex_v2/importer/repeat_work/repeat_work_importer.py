from baseintegration.datamigration import logger
from baseintegration.importer.repeat_part_importer import RepeatPartImporter
from .repeat_work_listener import PlexRepeatWorkImportListener
from plex_v2.configuration import ERPConfigFactory


class PlexRepeatWorkImporter(RepeatPartImporter):

    def _register_listener(self):
        self.listener = PlexRepeatWorkImportListener(self._integration)
        logger.info("Plex repeat work import listener was registered")

    def _register_default_processors(self):
        pass

    def _setup_erp_config(self):
        self.erp_config, self.plex_client = ERPConfigFactory.create_importer_config(self._integration, 'repeat_part')

    def _process_repeat_part(self, repeat_part_id: str, create_child_parts: bool = False, is_root: bool = True,
                             child_client_cache=None):  # noqa: C901
        logger.info('made it to repeat work processor')
        # logger.info(f"Attempting to process repeat work part with part number {repeat_part_id}")
        #
        # if self.epicor_client_cache is None:
        #     self.create_epicor_client_cache(first=True, child_client_cache=child_client_cache)
        #
        # if is_root is True:
        #     self.bulk_mode = self.listener.bulk
        #     self.processed_children_list = []
        #     self.create_epicor_client_cache_from_next_batch_of_ids()
        #
        # if repeat_part_id in self.processed_children_list:
        #     logger.info(
        #         f"Part id: {repeat_part_id} matches an existing part number that has already been processed."
        #         f" Skipping this component to prevent infinite loop."
        #     )
        # else:
        #     self.processed_children_list.append(repeat_part_id)
        #     with self.process_resource(RepeatPart, repeat_part_id, self.epicor_client_cache,
        #                                bulk=self.bulk_mode, is_root=is_root) as repeat_part_util_object:
        #         pass
        #     with self.process_resource(MethodOfManufacture, repeat_part_util_object, self.epicor_client_cache
        #                                ) as repeat_part_util_object:
        #         pass
        #     with self.process_resource(Operation, repeat_part_util_object, self.epicor_client_cache, bulk=self.bulk_mode
        #                                ) as repeat_part_util_object:
        #         pass
        #     with self.process_resource(RequiredMaterials, repeat_part_util_object, self.epicor_client_cache,
        #                                bulk=self.bulk_mode) as repeat_part_util_object:
        #         pass
        #     with self.process_resource(Child, repeat_part_util_object) as repeat_part_util_object:
        #         pass
        #     with self.process_resource(AddOn, repeat_part_util_object) as repeat_part_util_object:
        #         pass
        #     with self.process_resource(Header, repeat_part_util_object) as repeat_part_util_object:
        #         pass
        #
        #     self.add_part_to_batch_and_post(repeat_part_util_object)
