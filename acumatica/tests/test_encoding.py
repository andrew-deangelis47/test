
from acumatica.api_models.acumatica_models import StockItem
import os
import json


class TestJsonEncoding:

    def test_encoder(self, ):
        with open(os.path.join(os.path.dirname(__file__), "data/get_purchased_component.json"), 'r') as f:
            mock_data = json.load(f)
            stock = StockItem.from_json(mock_data[0])
            assert stock.VendorDetails[0].VendorID == 'V101277'
