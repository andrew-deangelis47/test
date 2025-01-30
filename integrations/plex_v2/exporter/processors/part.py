from plex_v2.exporter.processors.base import PlexProcessor
from paperless.objects.orders import Order, OrderItem, OrderComponent
from paperless.objects.components import AssemblyComponent
from plex_v2.objects.part import Part
from typing import List
from plex_v2.utils.export import ExportUtils
from plex_v2.factories.plex.part import PlexPartFactory
from paperless.objects.orders import OrderOperation
from baseintegration.datamigration import logger
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException


class PartProcessor(PlexProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'parts'

    def _process(self, order: Order, utils: ExportUtils, part_factory: PlexPartFactory) -> Part:
        try:
            processed_parts: List[Part] = []
            existing_parts: List[Part] = []
            created_parts: List[Part] = []

            # iterate order items
            order_item: OrderItem
            for order_item in order.order_items:

                # process manufactured components and hardware and add to appropriate list
                processed_components, created_components, existing_components = self._process_components_and_hardware(order, order_item, utils, part_factory)
                processed_parts.extend(processed_components)
                created_parts.extend(created_components)
                existing_parts.extend(existing_components)

                # process non-stock material and add to appropriate list
                processed_components, created_components, existing_components = self._process_material(order, order_item, utils, part_factory)
                processed_parts.extend(processed_components)
                created_parts.extend(created_components)
                existing_parts.extend(existing_components)

        # update the report if errored out
        except Exception as e:
            # if recognized error we can print it to the report
            if isinstance(e, CancelledIntegrationActionException):
                self._add_report_message(f'Error occured while processing parts: {str(e)}')
            # otherwise give generic error
            else:
                self._add_report_message('Error occured while processing parts.')
            raise e

        self._log_created_and_existing_parts(created_parts, existing_parts)

        # return the processed parts
        return processed_parts

    def _process_material(self, order: Order, order_item: OrderItem, utils: ExportUtils, factory: PlexPartFactory) -> tuple:
        processed_parts: List[Part] = []
        existing_parts: List[Part] = []
        created_parts: List[Part] = []

        # get all components of this order item
        assembly_components: List[AssemblyComponent] = order_item.iterate_assembly()

        # iterate components
        assembly_component: AssemblyComponent
        for assembly_component in assembly_components:

            order_component: OrderComponent = assembly_component.component

            # iterate material operations
            material_operation: OrderOperation
            for material_operation in order_component.material_operations:

                part_exists, material_part = utils.does_material_exist(material_operation)

                # skip if existing
                if part_exists:
                    logger.info(f'Part exists already number="{material_part.number}", rev="{material_part.revision}"')
                    processed_parts.append(material_part)
                    existing_parts.append(material_part)
                    continue

                # otherwise create
                material_part = factory.to_plex_material_part(order, material_operation)
                material_part.create()
                created_parts.append(material_part)

                # if configured set the grade property or cycle time frequency
                if self.config.should_export_part_grade or self.config.should_export_part_cycle_frequency or self.config.should_export_part_building_code or self.config.should_export_internal_note:
                    part_update_datasource = factory.to_plex_part_update_datasource(material_operation)
                    part_update_datasource.create()

        return processed_parts, created_parts, existing_parts

    def _process_components_and_hardware(self, order: Order, order_item: OrderItem, utils: ExportUtils, part_factory: PlexPartFactory) -> tuple:
        processed_parts: List[Part] = []
        existing_parts: List[Part] = []
        created_parts: List[Part] = []

        # get all components of this order item
        assembly_components: List[AssemblyComponent] = order_item.iterate_assembly()

        # iterate components
        assembly_component: AssemblyComponent
        for assembly_component in assembly_components:

            order_component: OrderComponent = assembly_component.component

            # check if part exists in plex
            plex_part_exists, part = utils.does_part_exist(order_component)

            # skip creation if already exists
            if plex_part_exists:
                logger.info(f'Part exists already number="{part.number}", rev="{part.revision}"')
                processed_parts.append(part)
                existing_parts.append(part)
                continue

            # otherwise create the part
            part = part_factory.to_plex_part(
                order,
                order_item,
                order_component
            )

            part.create()

            # if configured set the grade property or cycle time frequency
            if self.config.should_export_part_grade or self.config.should_export_part_cycle_frequency or self.config.should_export_part_building_code or self.config.should_export_internal_note or self.config.should_export_part_weight:
                part_update_datasource = part_factory.to_plex_part_update_datasource(order_component)
                part_update_datasource.create()

            created_parts.append(part)
            processed_parts.append(part)

        return processed_parts, created_parts, existing_parts

    def _log_created_and_existing_parts(self, created_parts: List[Part], existing_parts: List[Part]) -> None:
        if len(created_parts) > 0:
            list = [obj.number for obj in created_parts]
            self._add_report_message(f'Created parts: {", ".join(list)}')

        if len(existing_parts) > 0:
            list = [obj.number for obj in existing_parts]
            self._add_report_message(f'Existing parts in Plex: {", ".join(list)}')
