import json
from unittest.mock import patch
from plex.objects.part import Part
from plex.exporter.processors.part import PartProcessor
from paperless.objects.orders import OrderComponent
from types import SimpleNamespace
import os


class TestPartProcessor:
    def setup(self) -> None:
        self.processor = PartProcessor(SimpleNamespace(
            erp_config=SimpleNamespace(
                default_part_type='part_type',
                default_part_group='part_group',
                default_part_status='part_status',
                default_part_source='part_source',
                default_product_type='product_type',
                default_part_building_code='test building'
            )
        ))
        with open(os.path.join(os.path.dirname(__file__), "data/order_component.json"), 'r') as f:
            self.mock_order_component_json = json.load(f)
        self.mock_order_component = OrderComponent(**self.mock_order_component_json)
        with open(os.path.join(os.path.dirname(__file__), "data/part.json"), 'r') as f:
            self.mock_part = json.load(f)

    # TODO: Verify that the part returned by _process looks good
    def test_process_with_nonexistent_part(self):
        self.setup()
        with patch.object(Part, 'search', return_value=[]) as search, \
                patch.object(Part, 'create', return_value=None):
            self.processor._process(self.mock_order_component, "1-1")
            search.assert_called_once_with(
                number=self.mock_order_component.part_number,
                rev=self.mock_order_component.revision,
            )

    def test_process_with_existent_part(self):
        self.setup()
        self.mock_part['number'] = self.mock_order_component.part_number
        self.mock_part['revision'] = self.mock_order_component.revision
        with patch.object(Part, 'search', return_value=[
            Part.from_json(self.mock_part)
        ]) as search, patch.object(Part, 'create', return_value=None):
            self.processor._process(self.mock_order_component, "1-1")
            search.assert_called_once_with(
                number=self.mock_order_component.part_number,
                rev=self.mock_order_component.revision,
            )

    def test_process_with_new_rev_of_existent_part(self):
        self.setup()
        self.mock_part['number'] = self.mock_order_component.part_number
        self.mock_part['revision'] = 'A'
        with patch.object(Part, 'search', return_value=[
            Part.from_json(self.mock_part)
        ]) as search, patch.object(Part, 'create', return_value=None):
            self.processor._process(self.mock_order_component, "1-1")
            search.assert_called_once_with(
                number=self.mock_order_component.part_number,
                rev=self.mock_order_component.revision,
            )

    def test_process_when_search_result_does_not_match(self):
        self.setup()
        self.mock_part['number'] = 'random_part_no'
        self.mock_part['revision'] = 'A'
        with patch.object(Part, 'search', return_value=[
            Part.from_json(self.mock_part)
        ]) as search, patch.object(Part, 'create', return_value=None):
            self.processor._process(self.mock_order_component, "1-1")
            search.assert_called_once_with(
                number=self.mock_order_component.part_number,
                rev=self.mock_order_component.revision
            )
