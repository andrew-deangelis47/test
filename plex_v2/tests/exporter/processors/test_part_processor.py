from plex_v2.exporter.processors.part import PartProcessor
from plex_v2.configuration import PlexConfig
from types import SimpleNamespace
from unittest.mock import create_autospec
from baseintegration.integration.integration_export_report import IntegrationExportReport
from paperless.objects.components import AssemblyComponent
from paperless.objects.orders import Order, OrderItem, OrderComponent
from plex_v2.objects.part import Part
from plex_v2.utils.export import ExportUtils
from plex_v2.factories.plex.part import PlexPartFactory


class TestPartProcessor:

    def setup_method(self):
        integration_report = create_autospec(IntegrationExportReport)
        integration_report.update_table.return_value = True

        self.processor = PartProcessor(SimpleNamespace(
            erp_config=PlexConfig(),
            integration_report=integration_report
        ))

        self.utils = create_autospec(ExportUtils)

        self.part_factory = create_autospec(PlexPartFactory)

        order_component = create_autospec(spec=OrderComponent, name='order_component')
        order_component.material_operations = []

        assembly_component = create_autospec(AssemblyComponent)
        assembly_component.component = order_component

        order_item = create_autospec(spec=OrderItem, name='order_item')
        order_item.iterate_assembly.return_value = [assembly_component]

        order = create_autospec(Order)
        order.order_items = [order_item]

        self.order = order

        return order

    def test_part_processor_creates_parts_if_not_existing(self):
        self.utils.does_part_exist.return_value = False, None
        plex_part = create_autospec(spec=Part, name='plex_part')
        plex_part.number = '1'
        plex_part.revision = 'rev'
        self.part_factory.to_plex_part.return_value = plex_part

        self.processor._process(
            self.order,
            self.utils,
            self.part_factory
        )

        plex_part.create.assert_called_once()

    def test_part_processor_does_not_create_parts_if_existing(self):
        plex_part = create_autospec(Part)
        plex_part.number = '1'
        plex_part.revision = 'rev'
        self.utils.does_part_exist.return_value = True, plex_part

        self.processor._process(
            self.order,
            self.utils,
            self.part_factory
        )

        self.part_factory.to_plex_part.assert_not_called()
        plex_part.create.assert_not_called()
