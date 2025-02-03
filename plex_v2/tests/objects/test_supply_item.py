import json
from unittest.mock import patch
from plex_v2.client import PlexClient
import os
from plex_v2.objects.supply_items import SupplyItem


class TestSupplyItem:
    def setup_method(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), "../data/supply_item_out.json"), 'r') as f:
            self.mock_part = json.load(f)
            PlexClient()  # Initialize the singleton
            self.maxDiff = 650

    def test_search(self):
        with patch.object(PlexClient, 'get_resource_list', return_value=self.mock_part):
            supply_item_result = SupplyItem.search()
            supply_item_data = supply_item_result[0]

            assert self.mock_part[0]['id'] == supply_item_data.id
            assert self.mock_part[0]['supplyItemNumber'] == supply_item_data.supplyItemNumber
            assert self.mock_part[0]['type'] == supply_item_data.type
            assert self.mock_part[0]['category'] == supply_item_data.category
            assert self.mock_part[0]['priority'] == supply_item_data.priority
            assert self.mock_part[0]['group'] == supply_item_data.group
            assert self.mock_part[0]['description'] == supply_item_data.description
            assert self.mock_part[0]['customerUnitPrice'] == supply_item_data.customerUnitPrice
            assert self.mock_part[0]['inventoryUnit'] == supply_item_data.inventoryUnit
            assert self.mock_part[0]['briefDescription'] == supply_item_data.briefDescription
            assert self.mock_part[0]['accountId'] == supply_item_data.accountId
            assert self.mock_part[0]['manufacturerCode'] == supply_item_data.manufacturerCode
            assert self.mock_part[0]['supplierId'] == supply_item_data.supplierId
            assert self.mock_part[0]['manufacturerItemNumber'] == supply_item_data.manufacturerItemNumber
            assert self.mock_part[0]['manufacturerItemRevision'] == supply_item_data.manufacturerItemRevision
            assert self.mock_part[0]['manufacturerText'] == supply_item_data.manufacturerText
            assert self.mock_part[0]['createdDate'] == supply_item_data.createdDate
            assert self.mock_part[0]['createdById'] == supply_item_data.createdById
            assert self.mock_part[0]['modifiedDate'] == supply_item_data.modifiedDate
            assert self.mock_part[0]['modifiedById'] == supply_item_data.modifiedById
            assert self.mock_part[0]['taxCodeNumber'] == supply_item_data.taxCodeNumber
            assert self.mock_part[0]['maxQuantity'] == supply_item_data.maxQuantity
            assert self.mock_part[0]['minQuantity'] == supply_item_data.minQuantity
            assert self.mock_part[0]['note'] == supply_item_data.note
            assert self.mock_part[0]['updateWhenReceived'] == supply_item_data.updateWhenReceived
            assert self.mock_part[0]['active'] == supply_item_data.active
            assert self.mock_part[0]['averageCost'] == supply_item_data.averageCost
            assert self.mock_part[0]['responsiblePersonId'] == supply_item_data.responsiblePersonId
            assert self.mock_part[0]['vendorManaged'] == supply_item_data.vendorManaged
            assert self.mock_part[0]['commodity'] == supply_item_data.commodity
            assert self.mock_part[0]['countryOfOrigin'] == supply_item_data.countryOfOrigin
            assert self.mock_part[0]['consignment'] == supply_item_data.consignment
