from sage.models.sage_models import BaseObject


class RoutingScheduling(BaseObject):
    SEQUENCE = [
        ('entity_type', 0),
        ('operation', 1),
        ('downstream_operation', 2),
        ('milestone', 3),
        ('production_step', 4),
        ('scheduling', 5),
        ('overlapping_time', 6),
        ('overlapping_qty', 7),
        ('number_of_overlap_lots', 8)
    ]

    # 30 elements in the L section
    TOTAL_ELEMENTS = 9

    entity_type = str
    operation = str
    downstream_operation = str
    milestone = str
    production_step = str
    scheduling = str
    overlapping_time = str
    overlapping_qty = str
    number_of_overlap_lots = str

    def __init__(self):
        self.entity_type: str = 'S'
        self.operation: str = '10'
        self.downstream_operation: str = '20'
        self.milestone: str = 'Normal Tracking'
        self.production_step: str = 'No'
        self.scheduling: str = 'Absolute Successor'
        self.overlapping_time: str = ''
        self.overlapping_qty: str = ''
        self.number_of_overlap_lots: str = ''
