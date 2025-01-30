import attr
from attr.validators import instance_of, optional
from sage.models.sage_models.base_object import BaseObject


class Supplier(BaseObject):
    SEQUENCE = [
        ('vendor_id', 2),
        ('name', 4)
    ]

    vendor_id = attr.ib(validator=optional(instance_of(str)), default=None)
    name = attr.ib(validator=optional(instance_of(str)), default=None)
