from plex_v2.exporter.processors.bom import BomProcessor
from plex_v2.configuration import PlexConfig
from types import SimpleNamespace
from unittest.mock import create_autospec
from plex_v2.factories.plex.bom_component import BomComponentFactory
from baseintegration.integration.integration_export_report import IntegrationExportReport
from paperless.objects.components import AssemblyComponent
from paperless.objects.orders import Order, OrderItem, OrderComponent, OrderOperation
from plex_v2.objects.component_pairing import PPComponentPlexComponentPairings, Pairing
from plex_v2.objects.part import Part
from plex_v2.objects.bom import BOMComponent
from plex_v2.utils.export import ExportUtils


class TestBomProcessor:

    def setup_method(self):
        integration_report = create_autospec(IntegrationExportReport)
        integration_report.update_table.return_value = True

        self.processor = BomProcessor(SimpleNamespace(
            erp_config=PlexConfig(),
            integration_report=integration_report
        ))

    def _get_required_mocks(self):
        order = self.setup_mock_order()

        pp_parent_component, pp_sub_component, plex_parent_component, plex_sub_component = self.setup_mock_plex_and_pp_components()

        utils = self.setup_mock_utils(pp_parent_component, pp_sub_component, plex_parent_component)

        bom_component, bom_material_component, bom_factory = self.setup_bom_factory()

        return order, utils, bom_factory, bom_component, bom_material_component

    def setup_bom_factory(self):
        bom_component = create_autospec(spec=BOMComponent, _name='bomcomponent')
        bom_component.number = 'bom_num_0'
        bom_material_component = create_autospec(spec=BOMComponent, name='bom_material_component')
        bom_material_component.number = 'bom_num_1'

        bom_factory = create_autospec(spec=BomComponentFactory, name='bom_factory')
        bom_factory.to_bom_component.return_value = bom_component
        bom_factory.to_material_bom_component.return_value = bom_material_component

        return bom_component, bom_material_component, bom_factory

    def setup_mock_utils(self, pp_parent_component, pp_sub_component, plex_sub_component):

        assembly_component = create_autospec(spec=AssemblyComponent, name='assembly_component')
        assembly_component.component = pp_parent_component

        component_pairing = create_autospec(spec=Pairing, name='component_pairing')
        component_pairing.pp_component = pp_sub_component
        component_pairing.plex_component = plex_sub_component

        component_pairings = create_autospec(spec=PPComponentPlexComponentPairings, name='component_pairings')
        component_pairings.pairings = [component_pairing]

        plex_material_part = create_autospec(spec=Part, name='plex_material_part')
        plex_material_part.number = 'material_part_number'

        utils = create_autospec(spec=ExportUtils, name='utils')
        utils.get_bottom_level_of_order_item_bom.return_value = 0
        utils.get_assembly_components_for_level.return_value = [assembly_component]
        utils.get_sub_components_of_order_component.return_value = [pp_sub_component]
        utils.get_pp_to_plex_components_mapping.return_value = component_pairings
        utils.get_plex_material_from_material_op.return_value = plex_material_part

        return utils

    def setup_mock_order(self):
        order = create_autospec(Order)
        order_item = create_autospec(OrderItem)
        order.order_items = [order_item]

        return order

    def setup_mock_plex_and_pp_components(self):
        pp_parent_component = create_autospec(spec=OrderComponent, _name='pp_parent_component')
        pp_parent_component.number = 'parent'

        mock_material_op = create_autospec(spec=OrderOperation, _name='mock_material_op')
        pp_parent_component.material_operations = [mock_material_op]

        plex_parent_component = create_autospec(spec=Part, name='plex_parent_component')
        plex_parent_component.number = 'parent'

        pp_sub_component = create_autospec(spec=OrderComponent, name='pp_sub_component')
        pp_sub_component.number = 'child'

        plex_sub_component = create_autospec(spec=Part, name='plex_sub_component')
        plex_sub_component.number = 'child'

        return pp_parent_component, pp_sub_component, plex_parent_component, plex_sub_component

    def test_processor_creates_boms_for_material_and_sub_components_if_not_already_exist(self):
        order, utils, bom_factory, bom_component, bom_material_component = self._get_required_mocks()
        utils.does_bom_component_already_exist.return_value = False

        self.processor._process(
            order,
            utils,
            bom_factory
        )

        bom_component.create.assert_called_once()
        bom_material_component.create.assert_called_once()

    def test_processor_does_not_create_if_boms_already_exist(self):
        order, utils, bom_factory, bom_component, bom_material_component = self._get_required_mocks()
        utils.does_bom_component_already_exist.return_value = True

        self.processor._process(
            order,
            utils,
            bom_factory
        )

        bom_component.create.assert_not_called()
        bom_material_component.assert_not_called()
