import attr
from attr.validators import instance_of, optional
from sage.models.sage_models.base_object import BaseObject

"""
expected format of contact data via the "BPC" export template (string):
'type of data id, code, title, first name, last name, telephone, function
"""


class Contact(BaseObject):
    SEQUENCE = [
        ('entity_type', 0),
        ('first_name', 3),
        ('last_name', 4),
        ('email', 7)
    ]

    TOTAL_ELEMENTS = 8

    entity_type = attr.ib(validator=optional(instance_of(str)), default=None)
    first_name = attr.ib(validator=optional(instance_of(str)), default=None)
    last_name = attr.ib(validator=optional(instance_of(str)), default=None)
    email = attr.ib(validator=optional(instance_of(str)), default=None)

    def __init__(self):
        self.entity_type = 'C'
