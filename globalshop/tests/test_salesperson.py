from typing import Tuple
from globalshop.tests.test_connection import mock_conn_client, \
    mock_fetchone, dummy_client
from globalshop.salesperson import Salesperson, SalespersonRecord

client = dummy_client()


class TestSalesperson:

    def dummy_salesperson_rec(self) -> SalespersonRecord:
        dummy_salesperson = SalespersonRecord(id='MRZ',
                                              name='Mister Zed',
                                              email='mrz@zed.com')
        return dummy_salesperson

    def dummy_salesperson_row(self) -> Tuple[str, str, str]:
        return 'MRZ', 'Mister Zed', 'mrz@zed.com'

    def test_create_salesperson_rec(self):
        dummy_salesperson = self.dummy_salesperson_rec()
        assert dummy_salesperson
        assert dummy_salesperson.id == 'MRZ'

    def test_get_salesperson(self, mocker):
        mock_conn_client(mocker)
        mock_fetchone(mocker, self.dummy_salesperson_row())
        sp = Salesperson.get('MRZ')
        assert sp
        assert sp.name == 'Mister Zed'
