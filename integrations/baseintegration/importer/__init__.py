from contextlib import contextmanager
import re
from typing import Callable, List, Union
from ...baseintegration.datamigration import BaseDataMigration
from ...baseintegration.datamigration import logger
from ...baseintegration.exporter.exceptions import IntegrationNotImplementedError
from ...baseintegration.integration import Integration
from ...baseintegration.utils import set_custom_formatter, reset_custom_formatter, mark_action_as_completed, \
    mark_action_as_cancelled, BULK_IMPORT_ENTITY_ID_STRING


class BaseImporter(BaseDataMigration):
    """
    This is the base class to transfer data from an ERP to Paperless Parts. This should be overriden by a importer of
    X type (for example AccountImporter)
    """

    table_name = None

    split_id = False
    """Determines whether IDs should attempt to be parsed as tuples. Set to true for importers of objects that are
    identified by multiple fields (e.g. sometimes parts are identified by part number and revision)."""

    id_separator = ":_:"
    """If split_id is true, this is the separator used to split an ID into a tuple."""

    def __init__(self, integration: Integration):
        super().__init__(integration)
        self.header_dict = None
        self.success_message = ""
        self.listener = None
        self._register_listener()
        self.bulk_mode = False
        logger.info("Instantiated the baseimporter")

    def run(self):
        """
        calling this method is what runs the import.
        """
        raise IntegrationNotImplementedError(f"run() is not implemented for {self.__class__.__name__}")

    def importer_run(self, run_type: str, run_method: Callable, integration_action_type: str,
                     custom_table_import: bool = False, single_id: Union[str, tuple] = None,
                     bulk_enabled: bool = False):
        if custom_table_import:
            self.check_custom_table_exists()
        if single_id and single_id == "first":
            bulk = True
            action = self.create_integration_action(integration_action_type, single_id)
        else:
            bulk = False
        if single_id and single_id != "first":
            logger.info(f"Running single {run_type}")
            clean_single_id = self.clean_id(single_id)
            clean_single_id = self.split_id_if_needed(clean_single_id)
            if bulk_enabled:
                run_method([clean_single_id])
            else:
                run_method(clean_single_id)
        else:
            # log back in if expiring token
            try:
                self._setup_erp_config()
            except:
                pass
            new_ids = self.listener.get_new(bulk=bulk)
            action = self.create_integration_action(integration_action_type, BULK_IMPORT_ENTITY_ID_STRING)
            logger.info(f"{len(new_ids)} new {run_type} were found to import")
            action.status = "in_progress"
            action.current_record_count = len(new_ids)
            action.update()
            if not self._integration.integration_enabled:
                logger.info("Integration currently disabled - skipping this run")
                mark_action_as_cancelled(action, "Integration is currently off, skipping this run")
                return
            if bulk_enabled:
                new_ids = self.clean_ids(new_ids)
                self.bulk_integration_action_import(integration_action_type, new_ids, run_method, run_type)
            else:
                for new_id in new_ids:
                    new_id = self.clean_id(new_id)
                    self.single_integration_action_import(integration_action_type, new_id, run_method, run_type, bulk)
            mark_action_as_completed(action, "Bulk import was completed")

    def bulk_integration_action_import(self, integration_action_type: str, new_ids: List[str], run_method: Callable,
                                       run_type: str):
        if not self._integration.integration_enabled:
            logger.info("Integration currently disabled - skipping this run")
            return
        try:
            logger.info(f"Running bulk import as part of bulk import for {integration_action_type}")
            set_custom_formatter(self._integration, run_type, 'bulk')
            run_method(new_ids)
        except Exception as e:
            logger.info(e)
        reset_custom_formatter(self._integration)

    def single_integration_action_import(self, integration_action_type: str, new_id: Union[str, tuple],
                                         run_method: Callable, run_type: str, part_of_bulk: bool = False):
        if not self._integration.integration_enabled:
            logger.info("Integration currently disabled - skipping this run")
            return
        if part_of_bulk:
            logger.info(f"Running {new_id} import as part of bulk import for {integration_action_type}")
        try:
            set_custom_formatter(self._integration, run_type, new_id)
            run_method(new_id)
        except Exception as e:
            logger.info(e)
        reset_custom_formatter(self._integration)

    def clean_ids(self, new_ids) -> List[str]:
        clean_ids = []
        for new_id in new_ids:
            clean_ids.append(self.clean_id(new_id))
        return clean_ids

    def clean_id(self, new_id) -> str:
        str_new_id = str(new_id)
        clean_new_id = re.sub(r"(\\n|\\r|\\t|\\)", "", str_new_id).strip()
        return clean_new_id

    def split_id_if_needed(self, new_id: Union[str, tuple]) -> Union[str, tuple]:
        if self.split_id and not isinstance(new_id, tuple):
            split_id = str(new_id).split(self.id_separator)
            if len(split_id) > 1:
                return tuple(split_id)
        return new_id

    def check_custom_table_exists(self):
        pass

    def _register_listener(self):
        logger.info("registering listener")
        raise IntegrationNotImplementedError(f"register_listener() is not implemented for {self.__class__.__name__}")

    def register_processor(self, cls, processor_cls):
        """
        Register which Processor subclass will handle the creation and updating of the cls passed in. Can be used to
        override an existing processor.
        :param cls: The ERP wrapper class whose object will be output
        :param processor_cls: The processor who will produce an instance of the cls. Should be inherited class from baseintegration.integration.processor.BaseProcessor
        :return:
        """
        self._registered_processors[cls.__name__] = processor_cls

    def remove_processor(self, cls):
        """
        Register which Processor subclass will handle the creation and updating of the cls passed in.
        :param cls: The ERP wrapper class whose processor should be removed
        :return:
        """
        self._registered_processors.pop(cls.__name__, None)

    @contextmanager
    def process_resource(self, cls, *args, **kwargs):
        """
        This will process the provided inputs and output a resource by calling the registered processor of a class
        :return:
        """
        # TODO: Should we throw an error if no processor is registered for class? Seems like silently failing here
        # Could make more bugs later.
        processor_cls = self._registered_processors.get(cls.__name__, None)
        if processor_cls:
            # TODO: consider storing the list of processor() objects produced to ensure a many/many rollback at runtime.
            logger.info(f'processing_resource {cls.__name__}')
            val = None
            res_processor = None
            try:
                res_processor = processor_cls(self)
                val = res_processor.run(*args, **kwargs)
            except Exception as e:
                if res_processor.do_rollback:
                    logger.exception(f"Error in processor {cls.__name__}, calling .rollback()!")
                    res_processor.rollback(val, *args, **kwargs)
                else:
                    logger.exception(f'Error in processor {cls.__name__}! Skipping .rollback()!')
                raise e
            # Once we have the value, we will yield it out
            try:
                yield val
            except StopIteration as e:
                logger.info(e)

        else:
            # TODO: add sentry logger.error, maybe replace raising the error...
            raise ValueError(f"No processor was registered for provided resource: {str(cls)}")

    def bulk_import_enable(self, process_type: str):
        bulk_enable = self._integration.config_yaml.get("Importers", {}).get(process_type, {}).get('bulk_enable', False)
        if bulk_enable or (isinstance(bulk_enable, str) and bulk_enable.lower() == 'true'):
            return True
        return False
