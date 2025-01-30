from sage.models.sage_models import BaseObject


class BomDetail(BaseObject):
    SEQUENCE = [
        ('entity_type', 0),
        ('sequence', 1),
        ('revision_group', 2),
        ('component', 3),
        ('major_version', 4),
        ('minor_version', 5),
        ('link_description', 6),
        ('component_type', 7),
        ('uom', 8),
        ('link_quantity_code', 9),
        ('quantity_rounding', 10),
        ('link_quantity', 11),
        ('scrap_factor_percentage', 12),
        ('valid_from', 13),
        ('valid_to', 14),
        ('routing_operation', 15),
        ('operation_lead_time', 16),
        ('mat_slip_printing', 17),
        ('first_valid_lot', 18),
        ('last_valid_lot', 19),
        ('valuation', 20),
        ('pick_list_code', 21),
        ('setup_level', 22),
        ('weighing_tolerance_percent_plus', 23),
        ('weighing_tolerance_percent_minus', 24)
    ]

    component: str

    TOTAL_ELEMENTS = 28

    def __init__(self):
        self._set_defaults()

    def _set_defaults(self):
        self.entity_type: str = 'L'
        self.sequence: str = '10'
        self.major_version: str = ''
        self.minor_version: str = ''
        self.link_description: str = ''
        self.component_type: str = '1'
        self.uom: str = 'SHT'
        self.quantity_rounding: str = '1'
        self.link_quantity: str = '0.0018'
        self.link_quantity_code: str = ''
        self.scrap_factor_percentage: str = '25'
        self.valid_from: str = ''
        self.valid_to: str = ''
        self.routing_operation: str = '0'
        self.operation_lead_time: str = '0'
        self.mat_slip_printing: str = '2'
        self.first_valid_lot: str = ''
        self.last_valid_lot: str = ''
        self.valuation: str = '2'
        self.pick_list_code: str = '0'
        self.setup_level: str = '0'
        self.weighing_tolerance_percent_plus: str = '0'
        self.weighing_tolerance_percent_minus: str = '0'
