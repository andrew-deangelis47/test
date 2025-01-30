import attr
from attr.validators import instance_of, optional
from sage.models.sage_models import BaseObject


class WorkCenterExtraInfo(BaseObject):
    SEQUENCE = [
        ('description', 1)
    ]

    description = attr.ib(validator=optional(instance_of(str)), default=None)
