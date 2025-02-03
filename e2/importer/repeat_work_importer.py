from dataclasses import dataclass
from typing import List, Set

from baseintegration.datamigration import logger
from baseintegration.integration import Integration
from baseintegration.utils import get_last_action_datetime_value
from baseintegration.utils.repeat_work_objects import (
    Part as RepeatPart,
    Header,
    MethodOfManufacture,
    Operation,
    RequiredMaterials,
    Child
)
from baseintegration.importer.repeat_part_importer import RepeatPartImporter
from e2.importer.utils import create_all_sqlite_tables_if_not_exists, create_indexes_on_all_sqlite_tables
from e2.models import (
    OrderRouting,
    JobReq,
    Quote,
    Quotedet,
    Estim
)
from e2.importer.repeat_work_processors.repeat_part import RepeatPartImportProcessor
from e2.importer.repeat_work_processors.header import HeaderImportProcessor
from e2.importer.repeat_work_processors.method_of_manufacture import MethodOfManufactureProcessor
from e2.importer.repeat_work_processors.operation import OperationProcessor
from e2.importer.repeat_work_processors.required_material import RequiredMaterialProcessor
from e2.importer.repeat_work_processors.child import ChildProcessor
from e2.importer.configuration import E2RepeatWorkConfig
from e2.utils import get_version_number


@dataclass
class E2RepeatWorkImportListener:

    def __init__(self, integration: Integration):
        self.identifier = "import_repeat_part"
        self._integration = integration
        self.total_part_objects = 0
        logger.info("E2 repeat work import listener was instantiated")

    def get_new(self, bulk: bool = False) -> List[str]:
        """
        - For E2 Default, listens for changes to order routing, job requirements, quotes, and estims based on the date and time of last processing action.
        - For E2 Shop System, runs a full import of parts as collected based on order routing, job requirements, quotes, and estims.
        - Returns a list of unique part numbers (as strings) to process as repeat work.
        """

        if bulk:
            create_all_sqlite_tables_if_not_exists()
            create_indexes_on_all_sqlite_tables()

        # Collect set of repeat work part ids
        new_part_ids: Set[str] = set()
        if get_version_number() == "default":
            self._get_new_default(new_part_ids, bulk)
        else:
            self._get_new_shop_system(new_part_ids)

        # Return list of repeat work part ids to process
        self.total_part_objects = len(new_part_ids)
        logger.info(f"Found {len(new_part_ids)} total unique repeat work parts to process for import into Paperless Parts")
        return list(new_part_ids)

    def _get_new_default(self, new_part_ids: Set[str], bulk: bool = False):
        logger.info("Searching for recently updated order routing, job requirements, quotes, and estims in E2 Default to import repeat work parts")
        date_to_search = get_last_action_datetime_value(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)

        # Get parts associated with recently updated order routing
        logger.info("Searching for recently updated order routing in E2 Default")
        updated_order_routing_query_set = OrderRouting.objects.filter(last_mod_date__gt=date_to_search)
        before_len: int = len(new_part_ids)
        order_routing_part_ids: List[str] = updated_order_routing_query_set.values_list('part_no', flat=True)
        logger.info(f"Updating part id set with parts from {updated_order_routing_query_set.count()} order routings detected to have been changed")
        for part_number in order_routing_part_ids:
            new_part_ids.add(part_number)
        logger.info(f"Added {len(new_part_ids) - before_len} unique parts based on order routings")

        # Get parts associated with recently updated job requirements
        logger.info("Searching for recently updated job requirements in E2 Default")
        updated_job_requirements_query_set = JobReq.objects.filter(lastmoddate__gt=date_to_search)
        before_len: int = len(new_part_ids)
        job_requirement_part_ids: List[str] = updated_job_requirements_query_set.values_list('partno', flat=True)
        logger.info(f"Updating part id set with parts from {updated_job_requirements_query_set.count()} job requirements detected to have been changed")
        for part_number in job_requirement_part_ids:
            new_part_ids.add(part_number)
        logger.info(f"Added {len(new_part_ids) - before_len} unique parts based on job requirements")

        # Get parts associated with recently updated quotes
        logger.info("Searching for recently updated quotes in E2 Default")
        updated_quotes_query_set = Quote.objects.filter(lastmoddate__gt=date_to_search)
        before_len: int = len(new_part_ids)
        updated_quote_ids: List[str] = updated_quotes_query_set.values_list('quoteno', flat=True)
        updated_quote_details_query_set = Quotedet.objects.filter(quoteno__in=updated_quote_ids)
        quote_detail_part_ids: List[str] = updated_quote_details_query_set.values_list('partno', flat=True)
        logger.info(f"Updating part id set with parts from {updated_quote_details_query_set.count()} quote details detected to have been changed")
        for part_number in quote_detail_part_ids:
            new_part_ids.add(part_number)
        logger.info(f"Added {len(new_part_ids) - before_len} unique parts based on quote details")

        # Get parts associated with recently updated estims
        logger.info("Searching for recently updated estims in E2 Default")
        updated_estims_query_set = Estim.objects.filter(lastmoddate__gt=date_to_search)
        before_len: int = len(new_part_ids)
        estim_part_ids: List[str] = updated_estims_query_set.values_list('partno', flat=True)
        logger.info(f"Updating part id set with parts from {updated_estims_query_set.count()} estims detected to have been changed")
        for part_number in estim_part_ids:
            new_part_ids.add(part_number)
        logger.info(f"Added {len(new_part_ids) - before_len} unique parts based on estims")

    def _get_new_shop_system(self, new_part_ids: Set[str]):
        logger.info("Searching for all order routing, job requirements, quotes, and estims in E2 Shop System to run a full import of repeat work parts")

        # Get parts associated with all order routing
        logger.info("Searching for all order routing in E2 Shop System")
        all_order_routing_query_set = OrderRouting.objects.all()
        before_len: int = len(new_part_ids)
        order_routing_part_ids: List[str] = all_order_routing_query_set.values_list('part_no', flat=True)
        logger.info(f"Updating part id set with parts from {all_order_routing_query_set.count()} order routings")
        for part_number in order_routing_part_ids:
            new_part_ids.add(part_number)
        logger.info(f"Added {len(new_part_ids) - before_len} unique parts based on order routings")

        # Get parts associated with all job requirements
        logger.info("Searching for all job requirements in E2 Shop System")
        all_job_requirements_query_set = JobReq.objects.all()
        before_len: int = len(new_part_ids)
        job_requirement_part_ids: List[str] = all_job_requirements_query_set.values_list('partno', flat=True)
        logger.info(f"Updating part id set with parts from {all_job_requirements_query_set.count()} job requirements")
        for part_number in job_requirement_part_ids:
            new_part_ids.add(part_number)
        logger.info(f"Added {len(new_part_ids) - before_len} unique parts based on job requirements")

        # Get parts associated with all quote details
        logger.info("Searching for all quote details in E2 Shop System")
        all_quote_details_query_set = Quotedet.objects.all()
        quote_detail_part_ids: List[str] = all_quote_details_query_set.values_list('partno', flat=True)
        logger.info(f"Updating part id set with parts from {all_quote_details_query_set.count()} quote details")
        for part_number in quote_detail_part_ids:
            new_part_ids.add(part_number)
        logger.info(f"Added {len(new_part_ids) - before_len} unique parts based on quote details")

        # Get parts associated with all estims
        logger.info("Searching for all estims in E2 Shop System")
        all_estims_query_set = Estim.objects.all()
        before_len: int = len(new_part_ids)
        estim_part_ids: List[str] = all_estims_query_set.values_list('partno', flat=True)
        logger.info(f"Updating part id set with parts from {all_estims_query_set.count()} estims")
        for part_number in estim_part_ids:
            new_part_ids.add(part_number)
        logger.info(f"Added {len(new_part_ids) - before_len} unique parts based on estims")


class E2RepeatWorkImporter(RepeatPartImporter):

    def _register_listener(self):
        self.listener = E2RepeatWorkImportListener(self._integration)
        logger.info("E2 repeat work import listener was registered")

    def _register_default_processors(self):
        self.register_processor(RepeatPart, RepeatPartImportProcessor)
        self.register_processor(MethodOfManufacture, MethodOfManufactureProcessor)
        self.register_processor(Operation, OperationProcessor)
        self.register_processor(RequiredMaterials, RequiredMaterialProcessor)
        self.register_processor(Child, ChildProcessor)
        self.register_processor(Header, HeaderImportProcessor)
        logger.info('Registered all E2 repeat work import processors')

    def _setup_erp_config(self):
        self.erp_config = E2RepeatWorkConfig(self._integration.config_yaml)

    def _process_repeat_part(self, repeat_part_id: str, create_child_parts: bool = False, is_root: bool = True):  # noqa: C901
        logger.info(f"Attempting to process E2 repeat work part with part number {repeat_part_id}")
        self.total_parts_processed += 1
        if repeat_part_id in self.processed_children_list:
            logger.info(
                f"Part ID {repeat_part_id} matches an existing part number that has already been processed."
                f" Skipping this component to prevent infinite loop."
            )
        else:
            self.processed_children_list.append(repeat_part_id)
            with self.process_resource(RepeatPart, repeat_part_id) as repeat_part_util_object:
                pass
            with self.process_resource(MethodOfManufacture, repeat_part_util_object) as repeat_part_util_object:
                pass
            with self.process_resource(Operation, repeat_part_util_object) as repeat_part_util_object:
                pass
            with self.process_resource(RequiredMaterials, repeat_part_util_object) as repeat_part_util_object:
                pass
            with self.process_resource(Child, repeat_part_util_object, create_child_parts) as repeat_part_util_object:
                pass
            with self.process_resource(Header, repeat_part_util_object) as repeat_part_util_object:
                pass

            repeat_part_json = repeat_part_util_object.repeat_part.to_json()
            self.post_repeat_part(repeat_part_json)
