from sage.models.sage_models import BaseObject


class RoutingHeader(BaseObject):
    SEQUENCE = [
        ('entity_type', 0),
        ('routing', 1),
        ('routing_code', 2),
        ('site', 3),
        ('header_title', 4),
        ('use_status', 5),
        ('valid_from', 6),
        ('valid_to', 7),
        ('time_unit', 8),
        ('wo_management_mode', 9),
        ('header_text_0', 10),
        ('header_text_1', 11),
        ('header_text_2', 12),
        ('major_version', 13),
        ('minor_version', 14),
        ('default_rou_code', 15),
        ('option', 16),
    ]

    # 17 elements in the E section
    TOTAL_ELEMENTS = 17

    entity_type: str
    routing: str
    routing_code: str
    site: str
    header_title: str
    use_status: str
    valid_from: str
    valid_to: str
    time_unit: str
    wo_management_mode: str
    header_text_0: str
    header_text_1: str
    header_text_2: str
    major_version: str
    minor_version: str
    default_rou_code: str
    option: str

    def __init__(self):
        self.entity_type: str = 'E'
        self.routing: str = '000-101-002'
        self.routing_code: str = '40'
        self.site: str = 'ARC01'
        self.header_title: str = 'HANDLE BRACKET #002'
        self.use_status: str = '2'
        self.valid_from: str = ''
        self.valid_to: str = ''
        self.time_unit: str = '1'
        self.wo_management_mode: str = '4'
        self.header_text_0: str = ''
        self.header_text_1: str = ''
        self.header_text_2: str = ''
        self.major_version: str = ''
        self.minor_version: str = ''
        self.default_rou_code: str = ''
        self.option: str = ''
