from .supplier import Supplier
import attr
from attr.validators import instance_of, optional
from sage.models.sage_models.base_object import BaseObject


class SupplierFullEntity(BaseObject):

    def __init__(self, supplier: Supplier = None):
        self.supplier = supplier

    supplier = attr.ib(validator=optional(instance_of(Supplier)), default=None)
