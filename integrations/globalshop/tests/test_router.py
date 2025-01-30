import decimal

from globalshop.router import RouterRecord


class TestRouter:

    def test_create_router_record(self, mocker):
        rec = RouterRecord(external_id='external_id',
                           router_number='router_number', revision='revision',
                           router_description='router_description',
                           product_line='product_line', uom='uom',
                           commission_percent=decimal.Decimal('10.2'),
                           scrap_percent=decimal.Decimal('9.9'),
                           customer_id='customer_id',
                           qty_1=decimal.Decimal('1.1'),
                           qty_2=decimal.Decimal('2.2'),
                           qty_3=decimal.Decimal('3.3'),
                           qty_4=decimal.Decimal('4.4'),
                           qty_5=decimal.Decimal('5.5'),
                           qty_6=decimal.Decimal('6.6'),
                           qty_7=decimal.Decimal('7.7'),
                           qty_8=decimal.Decimal('8.8'),
                           qty_9=decimal.Decimal('9.9'),
                           qty_10=decimal.Decimal('10.10'),
                           extra_description_1='extra_description_1',
                           extra_description_2='extra_description_2',
                           extra_description_3='extra_description_3',
                           part_id='part_id', drawing_number='drawing_number',
                           user_field_1='user_field_1',
                           user_field_2='user_field_2', line_type='line_type',
                           line_number=1, material='material',
                           material_rev='material_rev', op_code='op_code',
                           setup=decimal.Decimal('4.0'), line_qty=4,
                           rate=decimal.Decimal('6.66'),
                           minimum=decimal.Decimal('2'), lead_hours=5,
                           overlap=decimal.Decimal('2'),
                           frequency=decimal.Decimal('2'),
                           sequence_group='sequence_group',
                           line_description='line_description',
                           sort_code='sort_code', workcenter='workcenter',
                           crew_size='crew_size',
                           workcenter_factor=decimal.Decimal('2'),
                           yield_amt=decimal.Decimal('222'),
                           vendor_id='vendor_id',
                           signoff_type='signoff_type',
                           signoff_by='signoff_by',
                           line_cmts='line_cmts', runtime=123,
                           outside_code='THING1',
                           line_unit_of_measure='EA',
                           project_group="ABC",
                           router_complete=True,
                           omit_from_wo=False)
        assert rec
