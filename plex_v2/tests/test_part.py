import json
from unittest.mock import patch
from plex_v2.objects.part import Part
from plex_v2.client import PlexClient
import os


class TestPart:
    def setup_method(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), "data/part.json"), 'r') as f:
            self.mock_part = json.load(f)

        PlexClient()  # Initialize the singleton
        self.maxDiff = 650

    def test_create(self):
        with patch.object(PlexClient, 'create_resource', return_value=self.mock_part) as mock_post_resource:
            mock_part = self.mock_part
            print('MOCK PART')
            print(mock_part)
            part = Part(**mock_part)
            part.create()

            mock_post_resource.assert_called_once()

            assert mock_post_resource.call_args.args[0] == Part.get_resource_name('create')

            created_json = json.loads(mock_post_resource.call_args.args[1])

            assert {k: mock_part[k] for k in mock_part if k != 'id'} == created_json

            assert part.number == mock_part['number']
            assert part.name == mock_part['name']
            assert part.revision == mock_part['revision']
            assert part.description == mock_part['description']
            assert part.type == mock_part['type']
            assert part.group == mock_part['group']
            assert part.source == mock_part['source']
            assert part.productType == mock_part['productType']
            assert part.status == mock_part['status']
            assert part.note == mock_part['note']
            assert part.leadTimeDays == mock_part['leadTimeDays']
            assert part.buildingCode == mock_part['buildingCode']
            assert part.createdById == mock_part['createdById']
            assert part.createdDate == mock_part['createdDate']
            assert part.modifiedById == mock_part['modifiedById']
            assert part.modifiedDate == mock_part['modifiedDate']

    def test_get(self):
        with patch.object(PlexClient, 'get_resource', return_value=self.mock_part):
            part = Part.get(1)
            mock_part = self.mock_part

            assert part.id == mock_part['id']
            assert part.number == mock_part['number']
            assert part.name == mock_part['name']
            assert part.revision == mock_part['revision']
            assert part.description == mock_part['description']
            assert part.type == mock_part['type']
            assert part.group == mock_part['group']
            assert part.source == mock_part['source']
            assert part.productType == mock_part['productType']
            assert part.status == mock_part['status']
            assert part.note == mock_part['note']
            assert part.leadTimeDays == mock_part['leadTimeDays']
            assert part.buildingCode == mock_part['buildingCode']
            assert part.createdById == mock_part['createdById']
            assert part.createdDate == mock_part['createdDate']
            assert part.modifiedById == mock_part['modifiedById']
            assert part.modifiedDate == mock_part['modifiedDate']

    def test_search(self):
        with patch.object(PlexClient, 'get_resource_list', return_value=[self.mock_part]):
            part_number = self.mock_part['number']
            search_results = Part.search(number=part_number)

            mock_part = self.mock_part
            part = search_results[0]

            assert part.id == mock_part['id']
            assert part.number == mock_part['number']
            assert part.name == mock_part['name']
            assert part.revision == mock_part['revision']
            assert part.description == mock_part['description']
            assert part.type == mock_part['type']
            assert part.group == mock_part['group']
            assert part.source == mock_part['source']
            assert part.productType == mock_part['productType']
            assert part.status == mock_part['status']
            assert part.note == mock_part['note']
            assert part.leadTimeDays == mock_part['leadTimeDays']
            assert part.buildingCode == mock_part['buildingCode']
            assert part.createdById == mock_part['createdById']
            assert part.createdDate == mock_part['createdDate']
            assert part.modifiedById == mock_part['modifiedById']
            assert part.modifiedDate == mock_part['modifiedDate']
