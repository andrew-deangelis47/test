import decimal

# from globalshop.tests.test_connection import mock_conn_client
from globalshop.client import GlobalShopClient
from globalshop.part import PartRecord
from globalshop.tests.test_connection import FakeCursor

from baseintegration.integration import logger

dummy_client = GlobalShopClient(server_name='test', database='dbq',
                                username='user1', password='pwd1')


def unpack_part_rec(part_rec) -> tuple:
    """
    Convert named tuple to sql response positioned row for reverse
    engineering fun
    """
    row = [None] * 155
    logger.debug(f'row len: {len(row)}: {row}')
    row[0] = part_rec.part,
    row[3] = part_rec.product_line,
    row[5] = part_rec.description,
    row[6] = part_rec.um_purchasing,
    row[7] = part_rec.um_inventory,
    row[16] = part_rec.amt_cost,
    row[30] = part_rec.date_last_usage,
    row[31] = part_rec.amt_price,
    row[36] = part_rec.code_sort,
    row[41] = part_rec.date_last_audit,
    row[45] = part_rec.prim_dim,
    row[46] = part_rec.sec_dim,
    row[51] = part_rec.date_exception,
    row[53] = part_rec.amt_alt_cost,
    row[54] = part_rec.date_last_chg,
    row[55] = part_rec.time_last_change,
    row[56] = part_rec.who_chg_last,
    row[57] = part_rec.trm_chg_last,
    row[58] = part_rec.length_raw_matl,
    row[59] = part_rec.width_raw_matl,
    row[60] = part_rec.density_raw_matl,
    row[61] = part_rec.code_rm_shape,
    row[62] = part_rec.qty_last_onhand,
    row[63] = part_rec.date_last_verify,
    row[80] = part_rec.description_2,
    row[81] = part_rec.description_3,
    row[82] = part_rec.amt_cost_1,
    row[83] = part_rec.amt_cost_2,
    row[84] = part_rec.amt_cost_3,
    row[85] = part_rec.date_cycle,
    row[86] = part_rec.lifo_base,
    row[87] = part_rec.six_decimal_cost,
    row[88] = part_rec.wt_per_foot,
    row[89] = part_rec.cutting_charge,
    row[92] = part_rec.length,
    row[93] = part_rec.width,
    row[94] = part_rec.warranty_type,
    row[95] = part_rec.prop_code,
    row[99] = part_rec.issue_um,
    row[124] = part_rec.matl_schrg_date,
    row[125] = part_rec.part_create_date,
    row[130] = part_rec.cost_date,
    row[139] = part_rec.thickness,
    row[148] = part_rec.part_create_user,
    row[154] = part_rec.use_dimension_calc
    return tuple(row)


def dummy_cus_rows() -> [PartRecord]:
    return [unpack_part_rec(get_dummy_part()) for _ in range(10)]


def mock_fetchall(mocker, dummy_rows):
    mocker.patch.object(FakeCursor,
                        'fetchall',
                        return_value=dummy_rows)


def get_dummy_part():
    part_rec = PartRecord(part='abc123',
                          product_line='RM', description='test part',
                          um_purchasing='ea', um_inventory='ea',
                          amt_cost=decimal.Decimal('1.11'),
                          date_last_usage='2020-01-01',
                          amt_price=decimal.Decimal('2.22'),
                          code_sort='ZZZ', date_last_audit='2020-01-01',
                          prim_dim='??', sec_dim='???',
                          date_exception='2021-01-01',
                          amt_alt_cost=decimal.Decimal('3.33'),
                          date_last_chg='2020-01-01',
                          time_last_change='12345', who_chg_last='SANTA',
                          trm_chg_last='???',
                          length_raw_matl=123, width_raw_matl=456,
                          density_raw_matl=decimal.Decimal('789.0123'),
                          code_rm_shape='123', qty_last_onhand=444,
                          date_last_verify='2020-01-01',
                          description_2='desc 2', description_3='desc_3',
                          amt_cost_1=decimal.Decimal('234'),
                          amt_cost_2=decimal.Decimal('123'),
                          amt_cost_3=decimal.Decimal('456'), date_cycle='???',
                          lifo_base='???',
                          six_decimal_cost=decimal.Decimal('123.456789'),
                          wt_per_foot='???',
                          cutting_charge='???', length=123, width=456,
                          warranty_type='XYZ', prop_code='ZZZ',
                          issue_um='EA', matl_schrg_date='2020-01-01',
                          part_create_date='2020-01-01',
                          cost_date='2020-01-01', thickness=444,
                          part_create_user='SANTA', use_dimension_calc=True,
                          extra_description='Extra Extra!'
                          )
    return part_rec


class TestPart:
    def test_create_part(self, mocker):
        pass
        # """
        # Create a part rec
        # """
        #
        # return get_dummy_part()

    def test_select(self, mocker):
        pass
        # mock_conn_client(mocker)
        #
        # rows = dummy_cus_rows()
        # mock_fetchall(mocker, rows)
        # parts = Part.select()
        # assert parts
