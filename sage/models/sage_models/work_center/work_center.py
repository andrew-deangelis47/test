import attr
from attr.validators import instance_of, optional
from sage.models.sage_models.base_object import BaseObject


class WorkCenter(BaseObject):
    SEQUENCE = [
        ('work_center_id', 1),
        ('description', 5),
        ('site', 3),
        ('work_center_type', 6),
        ('cost_dimension', 7),
        ('full_description', 8)
    ]
    work_center_id = attr.ib(validator=optional(instance_of(str)))
    description = attr.ib(validator=optional(instance_of(str)))
    site = attr.ib(validator=optional(instance_of(str)))
    cost_dimension = attr.ib(validator=optional(instance_of(str)))
    work_center_type = attr.ib(validator=optional(instance_of(str)))
    full_description = attr.ib(validator=optional(instance_of(str)))
