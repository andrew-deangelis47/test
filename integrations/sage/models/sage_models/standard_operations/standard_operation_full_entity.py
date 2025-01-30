import attr
from .standard_operation import StandardOperation
from attr.validators import instance_of, optional
from sage.models.sage_models.base_object import BaseObject


class StandardOperationFullEntity(BaseObject):

    def __init__(self, standard_operation: StandardOperation):
        self.standard_operation = standard_operation

    standard_operation = attr.ib(validator=optional(instance_of(StandardOperation)), default=None)
