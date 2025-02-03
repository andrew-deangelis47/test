from baseintegration.datamigration import logger
from baseintegration.utils.custom_table import HexImportCustomTable
from baseintegration.importer.repeat_part_importer import RepeatPartImporter

from baseintegration.utils.repeat_work_objects import Part, Header, MethodOfManufacture
from mietrak_pro.importer.repeat_work_processors.header import HeaderProcessor
from mietrak_pro.importer.repeat_work_processors.method_of_manufacture import MethodOfManufactureProcessor
from mietrak_pro.importer.repeat_work_processors.repeat_part import RepeatPartProcessor
from mietrak_pro.importer.utils import MietrakProImportListener

REFERENCED_BY = "REFERENCED_BY"
REFERENCES = "REFERENCES"
TOP_LEVEL = "TOP_LEVEL"


class MieTrakProRepeatWorkImportListener:

    def __init__(self, integration):
        self.identifier = "import_repeat_part"
        self._integration = integration
        self.total_part_objects = 0
        logger.info("MieTrak Pro repeat import listener was instantiated")

    def get_new(self, bulk=False, date_to_search=None):
        ids = set()
        logger.info("Checking for new repeat work")
        if bulk:
            last_processed_hex_counter = '0x0000000000000000'
        else:
            last_processed_hex_counter = HexImportCustomTable.get_last_processed_hex_counter(self.identifier)
        new_hex_counter = last_processed_hex_counter
        last_processed_decimal_counter = int(last_processed_hex_counter, 16)

        new_hex_counter = self._add_new_ids(ids, new_hex_counter, last_processed_decimal_counter)

        HexImportCustomTable.update_last_processed_hex_counter(self.identifier, new_hex_counter)

        self.total_part_objects = len(ids)
        logger.info(f"Found {self.total_part_objects} records to update")
        return ids

    def _get_queries_from_table_map(self, table_map: dict, last_processed_decimal_counter,
                                    previous_joins: str = "", parent_table: str = ""):
        """
        See comment by "relevant_table_map" for background on this function.
        """
        all_queries = []
        for (type_of_relation, table_name), child_table_map in table_map.items():
            new_joins = ""
            if type_of_relation == REFERENCED_BY:
                # table_name references parent_table
                new_joins = f"{previous_joins} INNER JOIN {table_name} " \
                            f"ON {table_name}.{parent_table}FK = {parent_table}.{parent_table}PK"
            elif type_of_relation == REFERENCES:
                # parent_table references table_name
                new_joins = f"{previous_joins} INNER JOIN {table_name} " \
                            f"ON {table_name}.{table_name}PK = {parent_table}.{table_name}FK"
            query = f"SELECT Item.ItemPK, {table_name}.LastAccess FROM Item " \
                    f"{new_joins} " \
                    f"WHERE {table_name}.LastAccess > {last_processed_decimal_counter}"
            all_queries.append(query)
            child_queries = self._get_queries_from_table_map(child_table_map, last_processed_decimal_counter,
                                                             new_joins, table_name)
            all_queries.extend(child_queries)
        return all_queries

    def _add_new_ids(self, ids, new_hex_counter: str, last_processed_decimal_counter: int) -> str:
        """
        The dictionary below stores all tables that need to be checked for updates, and how they relate to other
        tables. For example, we need to know all items tied to updated Operation instances. Below, the "Item" table is
        referenced by the "Quote" table, the "Quote" table is referenced by the "QuoteAssembly" table,
        the "QuoteAssembly" table references the "Operation" table. Thus can we automatically form a lengthy
        INNER JOIN statement to relate updated operations to items.
        """
        relevant_table_map = {
            (TOP_LEVEL, "Item"): {
                (REFERENCED_BY, "RequestForQuoteLine"): {},
                (REFERENCED_BY, "Quote"): {
                    (REFERENCED_BY, "QuoteAssembly"): {
                        (REFERENCES, "Operation"): {},
                        (REFERENCES, "UnitOfMeasureSet"): {}
                    },
                    (REFERENCED_BY, "QuoteQuantity"): {}
                },
                (REFERENCED_BY, "WorkOrderCompletion"): {},
                (REFERENCED_BY, "WorkOrder"): {
                    (REFERENCES, "WorkOrderTotal"): {}
                },
                (REFERENCED_BY, "WorkOrderRelease"): {
                    (REFERENCED_BY, "WorkOrderAssembly"): {
                        (REFERENCES, "WorkCenter"): {}
                    }
                }
            }
        }

        all_queries = self._get_queries_from_table_map(relevant_table_map, last_processed_decimal_counter)
        for query in all_queries:
            try:
                new_hex_counter = MietrakProImportListener._add_ids_from_query(ids, new_hex_counter, query)
            except Exception as e:
                logger.info("Unable to execute query: " + str(e))

        return new_hex_counter


class MieTrakProRepeatPartImporter(RepeatPartImporter):

    def _register_listener(self):
        self.listener = MieTrakProRepeatWorkImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(Part, RepeatPartProcessor)
        self.register_processor(Header, HeaderProcessor)
        self.register_processor(MethodOfManufacture, MethodOfManufactureProcessor)
        logger.info('Registered all repeat part processors.')

    def _process_repeat_part(self, repeat_part_id: str, create_child_parts: bool = False, is_root: bool = True):  # noqa: C901
        logger.info(f"Attempting to process {str(repeat_part_id)}")
        self.total_parts_processed += 1

        if repeat_part_id in self.processed_children_list:
            logger.info(
                f"Part id: {repeat_part_id} matches an existing part number that has already been processed."
                f" Skipping this component to prevent infinite loop."
            )
        else:
            self.processed_children_list.append(repeat_part_id)
            with self.process_resource(Part, repeat_part_id) as (repeat_part, item):
                pass
            with self.process_resource(MethodOfManufacture, repeat_part, item, create_child_parts) as methods_of_manufacture:
                pass
            with self.process_resource(Header, repeat_part, item, methods_of_manufacture) as repeat_part:
                pass

            repeat_part_json = repeat_part.to_json()
            self.post_repeat_part(repeat_part_json)
