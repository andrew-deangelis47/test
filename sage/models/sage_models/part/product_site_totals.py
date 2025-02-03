import attr
from attr.validators import instance_of, optional
from sage.models.sage_models.base_object import BaseObject


@attr.s
class ProductSiteTotals(BaseObject):
    SEQUENCE = [
        ('entity_type', 0),
        ('purchase_base_price', 1)
    ]

    TOTAL_ELEMENTS = 2

    entity_type = attr.ib(validator=optional(instance_of(str)), default='K')
    purchase_base_price = attr.ib(validator=optional(instance_of(str)), default='0.01')
