from typing import Union
from baseintegration.importer import BaseImporter
from baseintegration.exporter.exceptions import IntegrationNotImplementedError
from baseintegration.datamigration import logger
from baseintegration.integration import Integration
from datetime import datetime
from paperless.client import PaperlessClient, PaperlessException
from baseintegration.utils import repeat_part_bulk_post, get_string_size, BULK_IMPORT_ENTITY_ID_STRING
import json
import os

from baseintegration.utils.custom_table import MAX_UPLOAD_SIZE_MB, MAX_BATCH_SIZE


class RepeatPartImporter(BaseImporter):
    """Imports repeat work from ERP to Paperless. Should be overriden by an ERP specific importer.
    Requires an ERP specific listener with a "get_new" function"""

    def __init__(self, integration: Integration):
        super().__init__(integration)
        logger.info("Instantiated the repeat_work importer")
        self.listener = None
        self.bulk_mode = False
        self.bulk_repeat_work_batch_list = []
        self.bulk_repeat_work_batch_list_path = os.path.join(os.path.dirname(__file__), "../../../logs/bulk_repeat_work_batch_list.json")
        self.repeat_part_batch = list()
        self.total_part_count = 0
        self.total_payload_size = 0
        self.total_parts_processed = 0
        self.start_time = datetime.now()
        self.current_time = datetime.now()
        self.previous_time = datetime.now()
        self._register_listener()
        self.failed_part_dict = {"total_count": 0, "errors": []}
        self.processed_children_list = list()
        self.source_database = None
        self.parts_remaining = 0

    def importer_run(self, run_type: str, run_method, integration_action_type: str,
                     custom_table_import: bool = False, single_id: Union[str, tuple] = None):
        if single_id and single_id != "first":
            single_id = self.split_id_if_needed(single_id)
            logger.info(f"Running single {run_type}")
            self.source_database = "default"
            run_method(single_id, create_child_parts=True, is_root=True)
        else:
            self.bulk_mode = True
            action = self.create_integration_action(integration_action_type, single_id)
            if single_id == "first":
                logger.info("Doing a first time repeat work import, using local SQLite DB")
                self.source_database = "sqlite_copy"
                first_time_import = True
            else:
                logger.info("Doing a continous listening repeat work import, using actual customer SQL database")
                self.source_database = "default"
                first_time_import = False
                single_id = BULK_IMPORT_ENTITY_ID_STRING
            self.initialize_bulk_repeat_work_batch_list()
            # log back in if expiring token
            try:
                self._setup_erp_config()
            except:
                pass
            if first_time_import and self.bulk_repeat_work_batch_list and len(self.bulk_repeat_work_batch_list) > 100:
                # if we're in first time mode, and there's a lot of stuff remaining to process, start there. Otherwise, go back to the start
                new_ids = self.bulk_repeat_work_batch_list
                logger.info(f"Using the stored batch list, {len(new_ids)} left to process")
            else:
                logger.info("Not using the stored batch list, going out to DB to find parts")
                new_ids = self.listener.get_new(bulk=first_time_import)
                # if we're in first time mode, store these new ids in the batch list
                if first_time_import:
                    self.bulk_repeat_work_batch_list = list(new_ids)
                    self.write_repeat_work_batch_list_to_memory()
            self.total_part_count = len(new_ids)
            logger.info(f"{self.total_part_count} new {run_type} were found to import")
            action = self.create_integration_action(integration_action_type, BULK_IMPORT_ENTITY_ID_STRING)
            action.current_record_count = len(new_ids)
            action.status = "in_progress"
            action.update()
            batch_counter = 0
            for new_id in new_ids:
                self.bulk_repeat_work_batch_list.remove(new_id) if new_id in self.bulk_repeat_work_batch_list else None
                batch_counter += 1
                # if the value is a list, convert it back to a tuple
                new_id = tuple(new_id) if isinstance(new_id, list) else new_id
                self.bulk_integration_action_import(integration_action_type, new_id, run_method, run_type)
                # every 100, write the new list to memory
                if batch_counter > 100:
                    self.write_repeat_work_batch_list_to_memory()
                    batch_counter = 0

    def write_repeat_work_batch_list_to_memory(self):
        logger.info("Writing repeat work batch list to memory")
        with open(self.bulk_repeat_work_batch_list_path, 'w') as fp:
            json.dump(self.bulk_repeat_work_batch_list, fp)

    def initialize_bulk_repeat_work_batch_list(self) -> None:
        logger.info("Initializing bulk repeat work batch list to keep track of how far through the batch we get")
        if os.path.exists(self.bulk_repeat_work_batch_list_path):
            with open(self.bulk_repeat_work_batch_list_path) as fp:
                try:
                    self.bulk_repeat_work_batch_list = json.load(fp)
                except:
                    self.bulk_repeat_work_batch_list = []
        else:
            self.bulk_repeat_work_batch_list = []

    def run(self, repeat_work_id: Union[str, tuple] = None):
        logger.info("Calling run for the RepeatWorkImporter")
        method_to_call = getattr(self, '_process_repeat_part')
        self.importer_run("repeat_part", method_to_call, "import_repeat_part", False, repeat_work_id)

    def _process_repeat_part(self, repeat_work_id: str, create_child_parts: bool = False):
        """
        This is the main driver of the whole integration process. This needs to be overridden by the base class
        :return: The success status of the order processing
        """
        raise IntegrationNotImplementedError(f"_process_repeat_work() is not implemented for {self.__class__.__name__}")

    def post_repeat_part(self, repeat_part_json):
        json_string = json.dumps(repeat_part_json, indent=2)
        if self.bulk_mode:
            payload_size = self.total_payload_size + self.get_json_payload_size(json_string)
            parts_in_payload = len(self.repeat_part_batch)
            if payload_size <= MAX_UPLOAD_SIZE_MB and parts_in_payload < MAX_BATCH_SIZE:  # Django API framework limit
                logger.info("Part does not exceed allowable API payload size limit. Adding to batch.")
            else:  # If the size is going to exceed 250 MB, post the batch before adding the new part to the batch
                logger.info("Attempting to post batch of repeat parts.")
                self.post_repeat_part_batch()
            self.repeat_part_batch.append(repeat_part_json)
            self.total_payload_size += self.get_json_payload_size(json_string)
            self.parts_remaining = self.total_part_count - self.total_parts_processed
            self.current_time = datetime.now()
            total_time_elapsed, time_since_last_post, est_time_remaining = self.get_time_metrics()
            logger.info(f"BATCH DATA:"
                        f"\nTotal part count:\t\t{self.total_part_count}\tParts"
                        f"\nParts in this batch:\t\t{len(self.repeat_part_batch)}\tParts"
                        f"\nThis payload size:\t\t{round(self.total_payload_size, 3)}\tMB"
                        f"\nParts remaining:\t\t{self.parts_remaining}\tParts"
                        f"\nTotal time elapsed:\t\t{total_time_elapsed}\t"
                        f"\nTime since last post:\t{time_since_last_post}\t"
                        f"\nEst. time remaining:\t{est_time_remaining}\t")
            # Post the final batch when the importer is done running
            if self.parts_remaining == 0:
                self.post_repeat_part_batch()
        elif self._integration.config_yaml["Importers"]["repeat_part"].get("is_post_enabled", False):
            logger.info("Posting individual repeat part.")
            self.repeat_part_batch.append(repeat_part_json)
            self.post_repeat_part_batch()
        else:
            logger.info("Not posting repeat part batch. Config option 'is_post_enabled' is set to False.")

    def post_repeat_part_batch(self):
        try:
            client = PaperlessClient.get_instance()
            url = "v2/erp_stores/public/bulk_insert_historical_work"
            data = {"historical_parts": self.repeat_part_batch}
            response = repeat_part_bulk_post(client, url, data)
            try:
                if response.status_code == 200 or response.status_code == 201:
                    logger.info("Processed repeat part bulk post successfully")
                    self.collect_errors(response)
                elif response.status_code == 502:
                    response = client.request(url, data=json.dumps(data), method="post")
                    if response.status_code == 200 or response.status_code == 201:
                        logger.info("Processed repeat part bulk post successfully")
                        self.collect_errors(response)
                    else:
                        raise Exception("Did not process repeat part bulk post successfully")
                else:
                    raise Exception("Did not process repeat part bulk post successfully")
            except PaperlessException as e:
                if e.error_code == 502:
                    response = client.request(url, data=json.dumps(data), method="post")
                    if response.status_code == 200 or response.status_code == 201:
                        logger.info("Processed repeat part bulk post successfully")
                        self.collect_errors(response)
                    else:
                        raise Exception("Did not process repeat part bulk upsert successfully")
                else:
                    raise Exception("Did not process repeat part bulk upsert successfully")
        except Exception as e:
            logger.info(f"Bulk post failed. Clearing batch and moving on. Error shown below:\n\n{e}")

        logger.info(
            f"Total successfully posted parts: {self.failed_part_dict['total_count']}\n"
            f"All errors: {self.failed_part_dict['errors']}\n"
        )
        self.repeat_part_batch = []
        self.total_payload_size = 0

    def collect_errors(self, response):
        response_json = json.loads(response.text)
        self.failed_part_dict["total_count"] += int(response_json["message"].split(" ")[0])
        for error in response_json["errors"]:
            self.failed_part_dict["errors"].append(error)

    def get_json_payload_size(self, json_string):
        """Returns JSON payload size in MB"""
        payload_size = get_string_size(json_string)
        print(f"Individual part payload size: {payload_size} MB")
        return payload_size

    def get_time_metrics(self):
        total_time_elapsed = self.current_time - self.start_time
        time_since_last_post = self.current_time - self.previous_time
        est_time_remaining = (total_time_elapsed / self.total_parts_processed) * self.parts_remaining
        self.previous_time = self.current_time
        return total_time_elapsed, time_since_last_post, est_time_remaining
