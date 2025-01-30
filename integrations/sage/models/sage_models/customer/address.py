import attr
from attr.validators import instance_of, optional
from sage.models.sage_models.base_object import BaseObject


"""
    This class will be generated from the payload from the BPC
    import template in Sage x3. The sequence is the index in the payload where
    the corresponding data point lives. Class instantiation is done by the PayloadParser
"""


class Address(BaseObject):
    SEQUENCE = [
        ('entity_type', 0),
        ('address_id', 1),
        ('description', 2),
        ('address_line_1', 3),
        ('address_line_2', 4),
        ('zip_code', 6),
        ('city', 7),
        ('country', 8),
        ('telephone', 9),
        ('state', 12),
        ('website', 13)
    ]

    # total elements in the sage export template
    TOTAL_ELEMENTS = 14

    entity_type = attr.ib(validator=optional(instance_of(str)), default=None)
    address_id = attr.ib(validator=optional(instance_of(str)), default=None)
    address_line_1 = attr.ib(validator=optional(instance_of(str)), default=None)
    address_line_2 = attr.ib(validator=optional(instance_of(str)), default=None)
    city = attr.ib(validator=optional(instance_of(str)), default=None)
    state = attr.ib(validator=optional(instance_of(str)), default=None)
    country = attr.ib(validator=optional(instance_of(str)), default=None)
    zip_code = attr.ib(validator=optional(instance_of(str)), default=None)
    description = attr.ib(validator=optional(instance_of(str)), default=None)
    telephone = attr.ib(validator=optional(instance_of(str)), default=None)
    website = attr.ib(validator=optional(instance_of(str)), default=None)

    def __init__(self):
        self.entity_type = 'A'
