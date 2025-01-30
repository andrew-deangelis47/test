from typing import List

from baseintegration.datamigration import logger
from inforvisual.importer.repeat_part_processors.repeat_work_utils import create_all_sqlite_tables_if_not_exists, \
    create_indexes_on_all_sqlite_tables, get_part_id_from_requirement
from inforvisual.models import Part, PartSite, WorkOrder, QuoteLine, Requirement
from django.db.models import Q
from baseintegration.utils.repeat_work_objects import (
    Part as RepeatPart,
    Header,
    MethodOfManufacture,
)
from baseintegration.utils import get_last_action_datetime_sql
from baseintegration.importer.repeat_part_importer import RepeatPartImporter
from inforvisual.importer.repeat_part_processors.repeat_part import (
    RepeatPartImportProcessor,
)
from inforvisual.importer.repeat_part_processors.header import HeaderImportProcessor
from inforvisual.importer.repeat_part_processors.method_of_manufacture import (
    MOMImportProcessor,
)


class InforVisualRepeatPartImportListener:
    def __init__(self, integration):
        self.identifier = "import_repeat_part"
        self._integration = integration
        self.total_part_objects = 0
        logger.info("Infor Visual repeat part import listener was instantiated")

    def get_new(self, bulk=False) -> List[str]:
        logger.info("Checking for new accounts")
        if bulk:
            create_all_sqlite_tables_if_not_exists()
            create_indexes_on_all_sqlite_tables()

        date_to_search = get_last_action_datetime_sql(
            self._integration.managed_integration_uuid, self.identifier, bulk=bulk
        )

        # get parts
        updated_parts_query_set = Part.objects.filter(modify_date__gt=date_to_search)
        part_id_set = set(updated_parts_query_set.values_list("id", flat=True))
        part_site_set = set(
            PartSite.objects.filter(modify_date__gt=date_to_search).values_list(
                "part__id", flat=True
            )
        )
        part_id_set.update(part_site_set)

        # get work orders
        updated_wo_set = set(
            WorkOrder.objects.filter(create_date__gt=date_to_search).values_list(
                "part__id", flat=True
            )
        )
        part_id_set.update(updated_wo_set)

        # get quotes
        updated_quote_line_set = set(
            QuoteLine.objects.filter(
                Q(create_date__gt=date_to_search) | Q(quote__create_date__gt=date_to_search)
            ).values_list("part__id", flat=True)
        )
        part_id_set.update(updated_quote_line_set)

        # get child requirements that are not tied to parts - they should be treated as their own part
        requirements_without_parts = Requirement.objects.exclude(subord_wo_sub=None)\
            .filter(part=None, status_eff_date__gt=date_to_search).all()
        for requirement in requirements_without_parts:
            part_id = get_part_id_from_requirement(requirement)
            part_id_set.add(part_id)

        self.total_part_objects = len(part_id_set)

        logger.info(f"Got {self.total_part_objects} parts to process")
        return list(part_id_set)


class InforVisualRepeatPartImporter(RepeatPartImporter):
    def _register_listener(self):
        self.listener = InforVisualRepeatPartImportListener(self._integration)
        logger.info("Infor Visual repeat part listener was registered")

    def _register_default_processors(self):
        self.register_processor(RepeatPart, RepeatPartImportProcessor)
        self.register_processor(Header, HeaderImportProcessor)
        self.register_processor(MethodOfManufacture, MOMImportProcessor)

    def _process_repeat_part(
        self, repeat_part_id: str, create_child_parts=False, is_root=False
    ):  # noqa: C901
        logger.info(f"Part id is {str(repeat_part_id)}")
        self.total_parts_processed += 1

        if repeat_part_id in self.processed_children_list:
            logger.info(
                f"Part id: {repeat_part_id} matches an existing part number that has already been processed."
                f" Skipping this component to prevent infinite loop."
            )
        else:
            self.processed_children_list.append(repeat_part_id)
            with self.process_resource(MethodOfManufacture, repeat_part_id, create_child_parts) as (moms, part_data):
                pass
            with self.process_resource(Header, repeat_part_id, moms) as headers:
                pass
            with self.process_resource(
                Part, repeat_part_id, headers, part_data
            ) as repeat_part_json:
                logger.info(f"Part id {str(repeat_part_id)} was processed!")
            # json_string = json.dumps(repeat_part_json, indent=2)
            # print(json_string)
            self.post_repeat_part(repeat_part_json)
