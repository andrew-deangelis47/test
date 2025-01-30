import attr
from attr.validators import instance_of, optional
from sage.models.sage_models import BaseObject


class StandardOperation(BaseObject):
    SEQUENCE = [
        ('entity_type', 0),
        ('standard_operation', 1),
        ('description', 3),
        ('main_work_center', 4),
        ('rate', 28)
    ]

    TOTAL_ELEMENTS = 34
    FIELD_DELIMITER = ','

    entity_type = attr.ib(validator=optional(instance_of(str)), default='E')
    standard_operation = attr.ib(validator=optional(instance_of(str)))
    description = attr.ib(validator=optional(instance_of(str)))
    main_work_center = attr.ib(validator=optional(instance_of(str)))
    rate = attr.ib(validator=optional(instance_of(str)))
