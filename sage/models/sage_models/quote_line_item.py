import attr
from attr.validators import instance_of, optional


class QuoteLineItem:
    item_ref = attr.ib(validator=optional(instance_of(str)), default=None)
    sal = attr.ib(validator=optional(instance_of(str)), default=None)
    quantity = attr.ib(validator=optional(instance_of(str)), default=None)
    sal_stk_conv = attr.ib(validator=optional(instance_of(str)), default=None)
    stock = attr.ib(validator=optional(instance_of(str)), default=None)
    gross_price = attr.ib(validator=optional(instance_of(str)), default=None)
    tax_level_1 = attr.ib(validator=optional(instance_of(str)), default=None)
