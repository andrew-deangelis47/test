from dataclasses import dataclass
from typing import List, Set, Dict
from datetime import datetime, timedelta
import json
from baseintegration.datamigration import logger
from baseintegration.importer.repeat_part_importer import RepeatPartImporter
from baseintegration.utils import get_last_action_datetime
from baseintegration.utils.repeat_work_objects import (
    Part as RepeatPart,
    Header,
    MethodOfManufacture,
    Operation,
    RequiredMaterials,
    Child,
    AddOn
)
from epicor.importer.importer import EpicorImporter
from epicor.importer.configuration import EpicorRepeatWorkConfig
from epicor.importer.repeat_work_processors.repeat_part import RepeatPartImportProcessor
from epicor.importer.repeat_work_processors.header import HeaderImportProcessor
from epicor.importer.repeat_work_processors.method_of_manufacture import MethodOfManufactureProcessor
from epicor.importer.repeat_work_processors.operation import OperationProcessor
from epicor.importer.repeat_work_processors.required_material import RequiredMaterialProcessor
from epicor.importer.repeat_work_processors.child import ChildProcessor
from epicor.importer.repeat_work_processors.add_on import AddOnProcessor
from epicor.job import JobEntry
from epicor.engineering_workbench import EWBRev
from epicor.quote import QuoteDetailSearch
from epicor.importer.epicor_client_cache import EpicorClientCache
from epicor.importer.epicor_client_cache_util import create_epicor_client_cache
from epicor.importer.utils import create_id_separated_part_number_and_revision_string


@dataclass
class EpicorRepeatWorkImportListener:

    def __init__(self, integration):
        self.identifier = "import_repeat_part"
        self._integration = integration
        self.total_part_objects = 0
        self.batch_size = 25
        self.batch_count = 1
        self.list_of_new_parts: List = []
        self.batch_of_new_parts: List[str] = list()
        self.batch_of_new_quote_numbers: Set[int] = set()
        self.bulk = False
        self.invalid_parts = []
        logger.info("Epicor repeat work import listener was instantiated")

    def get_new(self, bulk=False) -> List[str]:
        """
        - Listens for changes to jobs, quotes, and part masters based on the date and time of last processing action.
        - Returns a list of unique part numbers (as strings) to process as repeat work.
        """
        logger.info("Searching for recently updated job entries, quote details, to import repeat work parts")
        self.erp_config = EpicorRepeatWorkConfig(self._integration.config_yaml)
        self.batch_size = self._integration.config_yaml.get(
            "Importers", {}).get("repeat_part", {}).get("repeat_part_batch_size", 25)
        self.bulk = True
        self.new_parts: Set[str] = set()
        self.part_number_to_quote_number_mapping: Dict[str, Set[int]] = {}
        self.part_number_to_job_number_mapping: Dict[str, Set[str]] = {}
        self.part_number_to_ewb_rev_sys_row_id_mapping: Dict[str, Set[str]] = {}
        self.date_to_search = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier,
                                                       bulk=bulk)
        # Get config date - or default to 5 years of data if not set
        self.date_to_search = self._integration.config_yaml.get("Importers", {}).get("repeat_part", {}).get(
            "import_objects_newer_than", datetime.now() - timedelta(days=5 * 365))
        self.get_updated_job_entry_part_ids()
        self.get_updated_quote_detail_part_ids()
        self.get_updated_ewb_rev_part_ids()

        # Return list of repeat work parts to process
        self.total_part_objects = len(self.new_parts)
        logger.info(f"Found {len(self.new_parts)} total unique repeat work parts to process for import into Paperless "
                    f"Parts: {self.new_parts}")

        self.list_of_new_parts = list(self.new_parts)
        self.batch_of_new_parts = self.list_of_new_parts[:self.batch_size]

        # Set parameters for building epicor client cache from batch-relevant job numbers and quote numbers
        self.batch_of_new_quote_numbers = self.get_batch_of_new_quote_numbers()
        self.batch_of_new_job_numbers = self.get_batch_of_new_job_numbers()
        self.batch_of_new_ewb_sys_row_ids = self.get_batch_of_new_ewb_sys_row_ids()

        self.job_id_count_filter_limit = self.erp_config.job_id_count_filter_limit
        self.quote_id_count_filter_limit = self.erp_config.quote_id_count_filter_limit
        self.ewb_id_count_filter_limit = self.erp_config.ewb_id_count_filter_limit
        self.page_size = self.erp_config.page_size

        return self.list_of_new_parts

    def get_updated_job_entry_part_ids(self):
        # Get parts associated with recently updated job entries
        logger.info("Searching for recently updated job entries in Epicor")
        job_entries: List[JobEntry] = JobEntry.get_changed(self.date_to_search, self.bulk)
        job_entry_part_ids: List[str] = self.create_mapping_of_part_numbers_to_job_numbers(job_entries)
        self.get_count_of_additional_repeat_part_ids(job_entry_part_ids)

    def create_mapping_of_part_numbers_to_job_numbers(self, job_entries: List[JobEntry]):
        job_entry_part_ids: List[str] = []
        for job_entry in job_entries:
            part_number = create_id_separated_part_number_and_revision_string(job_entry)
            job_entry_part_ids.append(part_number)
            if self.part_number_to_job_number_mapping.get(part_number, None):
                self.part_number_to_job_number_mapping[part_number].update([job_entry.JobNum])
            else:
                self.part_number_to_job_number_mapping[part_number] = set()
                self.part_number_to_job_number_mapping[part_number].update([job_entry.JobNum])
        return job_entry_part_ids

    def get_batch_of_new_job_numbers(self):
        final_set_of_job_numbers: Set[str] = set()
        for part_number in self.batch_of_new_parts:
            job_set = self.part_number_to_job_number_mapping.get(part_number, None)
            if job_set is not None:
                final_set_of_job_numbers.update(job_set)
        return final_set_of_job_numbers

    def get_updated_quote_detail_part_ids(self):
        # Get parts associated with recently updated quote details
        logger.info("Searching for recently updated quote details in Epicor")
        quote_details: List[QuoteDetailSearch] = QuoteDetailSearch.get_changed(self.date_to_search, self.bulk)
        quote_detail_part_ids: List[str] = self.create_mapping_of_part_numbers_to_quote_numbers(quote_details)
        self.get_count_of_additional_repeat_part_ids(quote_detail_part_ids)

    def create_mapping_of_part_numbers_to_quote_numbers(self, quote_details: List[QuoteDetailSearch]):
        quote_detail_part_ids: List[str] = []
        for quote_detail in quote_details:
            part_number = create_id_separated_part_number_and_revision_string(quote_detail)
            quote_detail_part_ids.append(part_number)
            if self.part_number_to_quote_number_mapping.get(part_number, None):
                self.part_number_to_quote_number_mapping[part_number].update([quote_detail.QuoteNum])
            else:
                self.part_number_to_quote_number_mapping[part_number] = set()
                self.part_number_to_quote_number_mapping[part_number].update([quote_detail.QuoteNum])
        return quote_detail_part_ids

    def get_batch_of_new_quote_numbers(self):
        final_set_of_quote_numbers: Set[int] = set()
        for part_number in self.batch_of_new_parts:
            quote_set = self.part_number_to_quote_number_mapping.get(part_number, None)
            if quote_set is not None:
                final_set_of_quote_numbers.update(quote_set)
        return final_set_of_quote_numbers

    def get_updated_ewb_rev_part_ids(self):
        # Get parts associated with recently update EWB parts
        logger.info("Searching for recently updated Engineering Workbench ECO Revisions in Epicor")
        ewb_parts: List[EWBRev] = EWBRev.get_changed(self.date_to_search, self.bulk)
        ewb_rev_part_ids: List[str] = self.create_mapping_of_part_numbers_to_ewb_sys_row_ids(ewb_parts)
        self.get_count_of_additional_repeat_part_ids(ewb_rev_part_ids)

    def create_mapping_of_part_numbers_to_ewb_sys_row_ids(self, ewb_revs: List[EWBRev]):
        ewb_rev_part_ids: List[str] = []
        for ewb_rev in ewb_revs:
            part_number = create_id_separated_part_number_and_revision_string(ewb_rev)
            ewb_rev_part_ids.append(part_number)
            if self.part_number_to_ewb_rev_sys_row_id_mapping.get(part_number, None):
                self.part_number_to_ewb_rev_sys_row_id_mapping[part_number].update([ewb_rev.SysRowID])
            else:
                self.part_number_to_ewb_rev_sys_row_id_mapping[part_number] = set()
                self.part_number_to_ewb_rev_sys_row_id_mapping[part_number].update([ewb_rev.SysRowID])
        return ewb_rev_part_ids

    def get_batch_of_new_ewb_sys_row_ids(self):
        final_set_of_ewb_sys_row_ids: Set[str] = set()
        for part_number in self.batch_of_new_parts:
            ewb_rev_set = self.part_number_to_ewb_rev_sys_row_id_mapping.get(part_number, None)
            if ewb_rev_set is not None:
                final_set_of_ewb_sys_row_ids.update(ewb_rev_set)
        return final_set_of_ewb_sys_row_ids

    def get_count_of_additional_repeat_part_ids(self, new_ids_list: List[str]):
        previous_len = len(self.new_parts)
        self.new_parts.update(new_ids_list)
        logger.info(f"Added {len(self.new_parts) - previous_len} unique parts.")


class EpicorRepeatWorkImporter(RepeatPartImporter, EpicorImporter):

    def _register_listener(self):
        self.listener = EpicorRepeatWorkImportListener(self._integration)
        logger.info("Epicor repeat work import listener was registered")

    def _register_default_processors(self):
        self.register_processor(RepeatPart, RepeatPartImportProcessor)
        self.register_processor(MethodOfManufacture, MethodOfManufactureProcessor)
        self.register_processor(Operation, OperationProcessor)
        self.register_processor(RequiredMaterials, RequiredMaterialProcessor)
        self.register_processor(Child, ChildProcessor)
        self.register_processor(AddOn, AddOnProcessor)
        self.register_processor(Header, HeaderImportProcessor)
        logger.info('Registered all Epicor repeat work import processors')

    def _setup_erp_config(self):
        self.erp_config = EpicorRepeatWorkConfig(self._integration.config_yaml)

    def _process_repeat_part(self, repeat_part_id: str, create_child_parts: bool = False, is_root: bool = True,
                             child_client_cache=None):  # noqa: C901
        logger.info(f"Attempting to process repeat work part with part number {repeat_part_id}")

        if self.epicor_client_cache is None:
            self.create_epicor_client_cache(first=True, child_client_cache=child_client_cache)

        if is_root is True:
            self.bulk_mode = self.listener.bulk
            self.processed_children_list = []
            self.create_epicor_client_cache_from_next_batch_of_ids()

        if repeat_part_id in self.processed_children_list:
            logger.info(
                f"Part id: {repeat_part_id} matches an existing part number that has already been processed."
                f" Skipping this component to prevent infinite loop."
            )
        else:
            self.processed_children_list.append(repeat_part_id)
            with self.process_resource(RepeatPart, repeat_part_id, self.epicor_client_cache,
                                       bulk=self.bulk_mode, is_root=is_root) as repeat_part_util_object:
                pass
            with self.process_resource(MethodOfManufacture, repeat_part_util_object, self.epicor_client_cache
                                       ) as repeat_part_util_object:
                pass
            with self.process_resource(Operation, repeat_part_util_object, self.epicor_client_cache, bulk=self.bulk_mode
                                       ) as repeat_part_util_object:
                pass
            with self.process_resource(RequiredMaterials, repeat_part_util_object, self.epicor_client_cache,
                                       bulk=self.bulk_mode) as repeat_part_util_object:
                pass
            with self.process_resource(Child, repeat_part_util_object) as repeat_part_util_object:
                pass
            with self.process_resource(AddOn, repeat_part_util_object) as repeat_part_util_object:
                pass
            with self.process_resource(Header, repeat_part_util_object) as repeat_part_util_object:
                pass

            self.add_part_to_batch_and_post(repeat_part_util_object)

    def create_epicor_client_cache_from_next_batch_of_ids(self):
        # If this part id is out of the index range of the cached data, cache the next batch of data
        if self.total_parts_processed == (self.listener.batch_count * self.listener.batch_size):

            # Create the next batch of unique part ids
            self.listener.batch_of_new_parts = self.listener.list_of_new_parts[self.total_parts_processed:(
                self.total_parts_processed + self.listener.batch_size)]

            # Use the next batch of unique part ids to create the cached data for subsequent processing
            self.listener.batch_of_new_quote_numbers = self.listener.get_batch_of_new_quote_numbers()
            self.listener.batch_of_new_job_numbers = self.listener.get_batch_of_new_job_numbers()
            self.listener.batch_of_new_ewb_sys_row_ids = self.listener.get_batch_of_new_ewb_sys_row_ids()
            self.create_epicor_client_cache(first=False)
            self.listener.batch_count += 1

    def create_epicor_client_cache(self, first=False, child_client_cache=None):
        if first is True:
            # Instantiate the EpicorClientCache for the first part only.
            epicor_client_cache = EpicorClientCache()
        else:
            epicor_client_cache = self.epicor_client_cache

        try:
            self.epicor_client_cache = create_epicor_client_cache(
                epicor_client_cache,
                self.listener.batch_of_new_job_numbers,
                self.listener.batch_of_new_quote_numbers,
                self.listener.batch_of_new_ewb_sys_row_ids,
                self.listener.quote_id_count_filter_limit,
                self.listener.job_id_count_filter_limit,
                self.listener.ewb_id_count_filter_limit,
                self.listener.page_size
            )
        except AttributeError:
            # The run method is called directly for single parts, therefore the listener attributes don't exist.
            self.epicor_client_cache = child_client_cache
            # Alternatively, cache is created in the repeat_part.py processor

    def add_part_to_batch_and_post(self, repeat_part_util_object):
        repeat_part_json = repeat_part_util_object.repeat_part.to_json()
        json_string = json.dumps(repeat_part_json, indent=2)
        self.validate_repeat_part(repeat_part_json, json_string)

        if self._integration.config_yaml.get("Importers", {}).get("repeat_part", {}).get("print_out_json", False):
            logger.info(f"{json_string}")

        self.total_parts_processed += 1
        is_post_enabled = self._integration.config_yaml.get(
            "Importers", {}).get("repeat_part", {}).get("is_post_enabled", False)
        if self.bulk_mode:
            json_payload_size = self.get_json_payload_size(json_string)
            if self.total_payload_size + json_payload_size <= 2.5:  # Django API framework limit
                logger.info("Part does not exceed allowable API payload size limit. Adding to batch.")
                self.repeat_part_batch.append(repeat_part_json)
                self.total_payload_size += json_payload_size
            else:  # If the size is going to exceed 250 MB, post the batch before adding the new part to the batch
                if is_post_enabled:
                    logger.info("Attempting to post batch of repeat parts.")
                    self.post_repeat_part_batch()
                    self.repeat_part_batch.append(repeat_part_json)
                    self.total_payload_size += json_payload_size

            self.parts_remaining = self.listener.total_part_objects - self.total_parts_processed
            self.current_time = datetime.now()
            total_time_elapsed, time_since_last_post, est_time_remaining = self.get_time_metrics()
            logger.info(f"BATCH DATA:"
                        f"\nTotal part count:\t\t{self.listener.total_part_objects}\tParts"
                        f"\nParts in this batch:\t\t{len(self.repeat_part_batch)}\tParts"
                        f"\nThis payload size:\t\t{round(self.total_payload_size, 3)}\tMB"
                        f"\nParts remaining:\t\t{self.parts_remaining}\tParts"
                        f"\nTotal time elapsed:\t\t{total_time_elapsed}\t"
                        f"\nTime since last post:\t{time_since_last_post}\t"
                        f"\nEst. time remaining:\t{est_time_remaining}\t"
                        f"\nTotal invalid parts: {len(self.listener.invalid_parts)}")
            # Post the final batch when the importer is done running
            if self.parts_remaining == 0 and is_post_enabled:
                logger.info("Attempting to post batch of repeat parts.")
                self.post_repeat_part_batch()
        elif is_post_enabled:
            logger.info("Posting individual repeat part.")
            self.repeat_part_batch.append(repeat_part_json)
            self.post_repeat_part_batch()

    def validate_repeat_part(self, repeat_part_json, json_string):
        """
        Validates that, if posted, the part will show up in Paperless Parts UI search functionality.
        """
        headers = repeat_part_json.get("headers", False)
        if len(headers) > 0:
            for header in headers:
                methods_of_manufacture = header.get("methods_of_manufacture", False)
                if not methods_of_manufacture:
                    logger.info("Missing MOM.")
                return True
        else:
            logger.info(f"Invalid part! Missing headers: {json_string}")
            self.listener.invalid_parts.append(repeat_part_json)
            return False
