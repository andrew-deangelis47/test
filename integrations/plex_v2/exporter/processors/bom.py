from plex_v2.exporter.processors.base import PlexProcessor
from paperless.objects.orders import Order, OrderComponent, OrderItem
from paperless.objects.components import AssemblyComponent
from plex_v2.objects.part import Part
from plex_v2.objects.bom import BOMComponent
from typing import List
from plex_v2.objects.component_pairing import PPComponentPlexComponentPairings, Pairing
from plex_v2.utils.export import ExportUtils
from plex_v2.factories.plex.bom_component import BomComponentFactory
from plex_v2.exceptions import PlexException
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException


class BomProcessor(PlexProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'bom_components'

    def _process(self, order: Order, utils: ExportUtils, factory: BomComponentFactory):
        self.bom_components_created: List[BOMComponent] = []
        self.existing_bom_components: List[BOMComponent] = []

        # iterate order items
        order_item: OrderItem
        for order_item in order.order_items:

            # iterate levels of the bom starting at the bottom
            current_level = utils.get_bottom_level_of_order_item_bom(order_item)
            while current_level >= 0:

                # get assembly components at the current level
                assembly_components_at_level = utils.get_assembly_components_for_level(order_item, current_level)

                # iterate these, check for children and create boms
                assembly_component: AssemblyComponent
                for assembly_component in assembly_components_at_level:

                    # required objects for bom creation
                    pp_parent_component: OrderComponent = assembly_component.component
                    pp_sub_components = utils.get_sub_components_of_order_component(pp_parent_component, order_item)

                    plex_parent_component: Part = utils.get_plex_part_from_paperless_component(pp_parent_component)
                    component_pairings: PPComponentPlexComponentPairings = utils.get_pp_to_plex_components_mapping(pp_sub_components)

                    # process non material sub components
                    non_material_created_components, non_material_existing_components = self._process_non_material_sub_components(
                        plex_parent_component=plex_parent_component,
                        component_pairings=component_pairings,
                        utils=utils,
                        factory=factory
                    )

                    # process material components
                    material_created_components, material_existing_components = self._process_material_sub_components(
                        plex_parent_component=plex_parent_component,
                        pp_parent_component=pp_parent_component,
                        utils=utils,
                        factory=factory
                    )

                    # log what was created and already existing for this parent part
                    created_components: List[Part] = non_material_created_components + material_created_components
                    existing_components: List[Part] = non_material_existing_components + material_existing_components
                    self._log_created_components(created_components, plex_parent_component)
                    self._log_already_existing_components(existing_components, plex_parent_component)

                current_level -= 1

    def _process_material_sub_components(self, plex_parent_component: Part, pp_parent_component: OrderComponent, utils: ExportUtils, factory: BomComponentFactory) -> tuple:
        """
        creates bom components from material operations
        """
        created_components: List[Part] = []
        existing_components: List[Part] = []
        mat_op: OrderComponent
        for mat_op in pp_parent_component.material_operations:

            plex_material_part = utils.get_plex_material_from_material_op(mat_op)

            if utils.does_bom_component_already_exist(plex_parent_component, plex_material_part):
                existing_components.append(plex_material_part)
                continue

            bom_component: BOMComponent = factory.to_material_bom_component(
                plex_parent_component=plex_parent_component,
                material_operation=mat_op
            )

            try:
                bom_component.create()
                created_components.append(plex_material_part)
            except PlexException as e:
                if 'The Component Part cannot be produced using the selected Part' in str(e):
                    raise CancelledIntegrationActionException(f'Plex error: The component "{plex_parent_component.number}" cannot be produced using component "{plex_material_part.number}"')

        return created_components, existing_components

    def _process_non_material_sub_components(self, plex_parent_component: Part, component_pairings: PPComponentPlexComponentPairings, utils: ExportUtils, factory: BomComponentFactory) -> tuple:
        """
        creates bom components for non-material sub components (purchased parts, manufactured parts)
        """
        created_components: List[Part] = []
        existing_components: List[Part] = []
        component_pairing: Pairing
        for component_pairing in component_pairings.pairings:

            pp_child_component = component_pairing.pp_component
            plex_child_component = component_pairing.plex_component

            # check if this bom component already exists
            if utils.does_bom_component_already_exist(plex_parent_component, plex_child_component):
                existing_components.append(plex_child_component)
                continue

            bom_component: BOMComponent = factory.to_bom_component(
                plex_child_component=plex_child_component,
                pp_child_component=pp_child_component,
                plex_parent_component=plex_parent_component
            )

            bom_component.create()
            created_components.append(plex_child_component)

        return created_components, existing_components

    def _log_created_components(self, bom_components_created: List[Part], plex_parent_component: Part):
        if len(bom_components_created) > 0:
            list = [obj.number for obj in bom_components_created]
            self._add_report_message(
                f'Created the following bom components for part {plex_parent_component.number}: {", ".join(list)}')

    def _log_already_existing_components(self, bom_components_created: List[Part], plex_parent_component: Part):
        if len(bom_components_created) > 0:
            list = [obj.number for obj in bom_components_created]
            self._add_report_message(
                f'The following bom components already exist for part {plex_parent_component.number}: {", ".join(list)}')
