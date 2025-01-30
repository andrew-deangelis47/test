import json
from unittest.mock import patch
from plex.objects.bom import BOMComponent
from plex.client import PlexClient
import os


class TestBOM:

    def setup(self) -> PlexClient:
        with open(os.path.join(os.path.dirname(__file__), "data/bom_in.json"), 'r') as f:
            self.mock_bom_in = json.load(f)
        with open(os.path.join(os.path.dirname(__file__), "data/bom_out.json"), 'r') as f:
            self.mock_bom_out = json.load(f)

        return PlexClient()  # Initialize the singleton

    def test_create(self):
        PlexClient = self.setup()
        with patch.object(PlexClient, 'create_resource', return_value=self.mock_bom_in) \
                as mock_post_resource:
            bom = BOMComponent.from_json(self.mock_bom_in)
            bom.create()

            mock_post_resource.assert_called_once()

            assert mock_post_resource.call_args.args[0] == BOMComponent.get_resource_name('create')

            created_json = json.loads(mock_post_resource.call_args.args[1])

            assert self.mock_bom_out == created_json

    def test_get(self):
        PlexClient = self.setup()
        with patch.object(PlexClient, 'get_resource', return_value=self.mock_bom_in):
            bom_component = BOMComponent.get('1')

            assert bom_component.componentId == self.mock_bom_in["componentPartId"]
            assert bom_component.id == self.mock_bom_in["id"]
            assert bom_component.partId == self.mock_bom_in["partId"]
            assert bom_component.partNumber == self.mock_bom_in["partNumber"]
            assert bom_component.partRevision == self.mock_bom_in["partRevision"]
            assert bom_component.partNumberRevision == self.mock_bom_in["partNumberRevision"]
            assert bom_component.partOperationId == self.mock_bom_in["partOperationId"]
            assert bom_component.partOperationCode == self.mock_bom_in["partOperationCode"]
            assert bom_component.partOperationNumber == self.mock_bom_in["partOperationNumber"]
            assert bom_component.partOperationType == self.mock_bom_in["partOperationType"]
            assert bom_component.componentPartId == self.mock_bom_in["componentPartId"]
            assert bom_component.componentPartNumber == self.mock_bom_in["componentPartNumber"]
            assert bom_component.componentPartRevision == self.mock_bom_in["componentPartRevision"]
            assert bom_component.componentPartNumberRevision == self.mock_bom_in["componentPartNumberRevision"]
            assert bom_component.componentSupplyItemId == self.mock_bom_in["componentSupplyItemId"]
            assert bom_component.componentSupplyItemNumber == self.mock_bom_in["componentSupplyItemNumber"]
            assert bom_component.componentUnitOfMeasure == self.mock_bom_in["componentUnitOfMeasure"]
            assert bom_component.quantity == self.mock_bom_in["quantity"]
            assert bom_component.minimumQuantity == self.mock_bom_in["minimumQuantity"]
            assert bom_component.maximumQuantity == self.mock_bom_in["maximumQuantity"]
            assert bom_component.quantityFixed == self.mock_bom_in["quantityFixed"]
            assert bom_component.depletionUnitOfMeasure == self.mock_bom_in["depletionUnitOfMeasure"]
            assert bom_component.depletionConversionFactor == self.mock_bom_in["depletionConversionFactor"]
            assert bom_component.sortOrder == self.mock_bom_in["sortOrder"]
            assert bom_component.active == self.mock_bom_in["active"]
            assert bom_component.position == self.mock_bom_in["position"]
            assert bom_component.side == self.mock_bom_in["side"]
            assert bom_component.scaling == self.mock_bom_in["scaling"]
            assert bom_component.validate == self.mock_bom_in["validate"]
            assert bom_component.autoDeplete == self.mock_bom_in["autoDeplete"]
            assert bom_component.transferHeat == self.mock_bom_in["transferHeat"]
            assert bom_component.note == self.mock_bom_in["note"]
