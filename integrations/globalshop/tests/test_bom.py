from globalshop.bom import BOMRecord, BOM
from globalshop.client import GlobalShopClient
from globalshop.tests.test_connection import mock_conn_client
# from globalshop.tests.test_connection import FakeCursor

dummy_client = GlobalShopClient(server_name='test', database='dbq',
                                username='user1', password='pwd1')


class TestBom:
    def test_create_bom_record(self, mocker):
        rec = BOMRecord(external_id='external_id', top_bom='top_bom',
                        top_bom_rev='top_bom_rev',
                        parent_part='parent_part', parent_rev='parent_rev',
                        level=1, sequence=10,
                        part_number='part_number',
                        part_number_rev='part_number_rev',
                        description='description',
                        alt_description_1='alt_description_1',
                        alt_description_2='alt_description_2',
                        quantity=123, uom='uom',
                        product_line='product_line', cost=456, source='source',
                        sort_code='sort_code', lead_time=55,
                        category='category', tag='tag', drawing='drawing',
                        memo_1='memo_1', memo_2='memo_2',
                        bom_complete='bom_complete',
                        extra_description='extra_description',
                        comments='comments')
        assert rec

    def test_insert_bom_record(self, mocker):
        mock_conn_client(mocker)
        rec = BOM.insert(external_id='external_id', top_bom='top_bom',
                         top_bom_rev='top_bom_rev',
                         parent_part='parent_part', parent_rev='parent_rev',
                         level=1, sequence=10,
                         part_number='part_number',
                         part_number_rev='part_number_rev',
                         description='description',
                         alt_description_1='alt_description_1',
                         alt_description_2='alt_description_2',
                         quantity=123, uom='uom',
                         product_line='product_line', cost=456,
                         source='source',
                         sort_code='sort_code', lead_time=55,
                         category='category', tag='tag', drawing='drawing',
                         memo_1='memo_1', memo_2='memo_2',
                         bom_complete='bom_complete',
                         extra_description='extra_description',
                         comments='comments')
        assert rec
        assert rec.external_id == 'external_id'
