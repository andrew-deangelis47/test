from plex_v2.factories.plex.bom_component import BomComponentFactory
from plex_v2.configuration import PlexConfig
from unittest.mock import create_autospec
from plex_v2.utils.export import ExportUtils
from paperless.objects.orders import OrderComponent
from plex_v2.objects.part import Part
from plex_v2.objects.routing import PartOperation


class TestBomComponentFactory:

    VALID_PLEX_PARENT_COMPONENT_ID = 'VALID_PLEX_PARENT_COMPONENT_ID'
    VALID_PLEX_CHILD_COMPONENT_ID = 'VALID_PLEX_CHILD_COMPONENT_ID'
    VALID_PART_OPERATION_ID = 'VALID_PART_OPERATION_ID'
    VALID_INNATE_QUANTITY = 5

    def setup_method(self):
        self.config = create_autospec(PlexConfig)

        self.plex_part_operation = create_autospec(PartOperation)
        self.plex_part_operation.id = self.VALID_PART_OPERATION_ID

        self.utils = create_autospec(ExportUtils)
        self.utils.get_first_plex_part_op_for_plex_part.return_value = self.plex_part_operation

        self.plex_parent_component = create_autospec(Part)
        self.plex_parent_component.id = self.VALID_PLEX_PARENT_COMPONENT_ID

        self.plex_child_component = create_autospec(Part)
        self.plex_child_component.id = self.VALID_PLEX_CHILD_COMPONENT_ID

        self.pp_child_component = create_autospec(OrderComponent)
        self.pp_child_component.innate_quantity = self.VALID_INNATE_QUANTITY

        self.factory = BomComponentFactory(
            config=self.config,
            utils=self.utils
        )

    def test_bom_component_factory_sets_component_id_to_plex_child_component_id(self):
        bom_component = self.factory.to_bom_component(
            self.plex_parent_component,
            self.plex_child_component,
            self.pp_child_component
        )

        assert bom_component.componentId == self.plex_child_component.id

    def test_bom_component_factory_sets_component_part_id_to_plex_parent_component_id(self):
        bom_component = self.factory.to_bom_component(
            self.plex_parent_component,
            self.plex_child_component,
            self.pp_child_component
        )

        assert bom_component.componentPartId == self.plex_parent_component.id

    def test_bom_component_factory_sets_part_operation_id_to_id_of_passed_in_part_operation(self):
        bom_component = self.factory.to_bom_component(
            self.plex_parent_component,
            self.plex_child_component,
            self.pp_child_component
        )

        assert bom_component.partOperationId == self.plex_part_operation.id

    def test_bom_component_factory_sets_quantity_to_innate_quantity_of_pp_child_component(self):
        bom_component = self.factory.to_bom_component(
            self.plex_parent_component,
            self.plex_child_component,
            self.pp_child_component
        )

        assert bom_component.quantity == self.pp_child_component.innate_quantity

    def test_bom_component_factory_sets_max_quantity_to_double_the_innate_quantity_of_pp_child_component(self):
        bom_component = self.factory.to_bom_component(
            self.plex_parent_component,
            self.plex_child_component,
            self.pp_child_component
        )

        assert bom_component.maximumQuantity == self.pp_child_component.innate_quantity * 2
