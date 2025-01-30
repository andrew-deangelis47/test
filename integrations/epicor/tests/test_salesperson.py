from epicor.salesperson import Salesperson
from epicor.exporter.exporter import EpicorOrderExporter
from baseintegration.integration import Integration
import os
import json
import requests_mock


def test_get_salesperson():
    EpicorOrderExporter(Integration())
    with requests_mock.Mocker() as m:
        with open(os.path.join(os.path.dirname(__file__), 'data/get_salesperson_response.json')) as f:
            sp_data = f.read()
        json.loads(sp_data)

        m.get('https://localurl/EpicorERPTest/api/v2/odata/ABC/Erp.BO'
              '.SalesRepSvc/SalesReps?%24filter=SalesRepCode+eq+%27bingus%27',
              text=sp_data)
        sp = Salesperson.get_by_id('bingus')
        assert sp is not None
        assert sp.SalesRepCode == 'bingus'
