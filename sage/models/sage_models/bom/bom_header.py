from sage.models.sage_models import BaseObject


class BomHeader(BaseObject):
    SEQUENCE = [
        ('entity_type', 0),
        ('parent_product', 1),
        ('bom_code', 2),
        ('header_title', 3),
        ('use_status', 4),
        ('valid_from', 5),
        ('valid_to', 6),
        ('base_quantity', 7),
        ('mgmt_unit', 8),
        ('header_text_0', 9),
        ('header_text_1', 10),
        ('header_text_2', 11),
        ('major_version', 12),
        ('minor_version', 13),
        ('default_bom_code', 14),
    ]

    TOTAL_ELEMENTS = 15

    def __init__(self):
        self._set_defaults()

    def _set_defaults(self):
        self.entity_type: str = 'E'
        self.header_title: str = '2'
        self.use_status: str = '1'  # can't set this, must be a calculated value based on another field
        self.valid_from: str = ''
        self.valid_to: str = ''
        self.mgmt_unit: str = ''
        self.header_text_0: str = ''  # not seeing this value on the front end even when given a value
        self.header_text_1: str = ''  # not seeing this value on the front end even when given a value
        self.header_text_2: str = ''  # not seeing this value on the front end even when given a value
        self.major_version: str = ''  # can't set this, must be a calculated value based on another field
        self.minor_version: str = ''  # can't set this, must be a calculated value based on another field
        self.default_bom_code: str = ''
