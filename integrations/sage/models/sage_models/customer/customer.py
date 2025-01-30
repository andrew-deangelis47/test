import attr
from attr.validators import instance_of, optional
from sage.models.sage_models.base_object import BaseObject


@attr.s
class Customer(BaseObject):
    SEQUENCE = [
        ('entity_type', 0),
        ('category', 1),
        ('code', 2),
        ('company_name', 3),
        ('bill_to_customer_address', 7),
        ('default_address', 8),
        ('default_ship_to_address', 9),
        ('currency', 10),
        ('tax_rule', 15),
        ('payment_days', 16),
        ('accounting_code', 17)
    ]

    TOTAL_ELEMENTS = 27

    entity_type = attr.ib(validator=optional(instance_of(str)), default='B')
    category = attr.ib(validator=optional(instance_of(str)), default=None)
    code = attr.ib(validator=optional(instance_of(str)), default=None)
    company_name = attr.ib(validator=optional(instance_of(str)), default=None)
    default_address = attr.ib(validator=optional(instance_of(str)), default=None)
    bill_to_customer_address = attr.ib(validator=optional(instance_of(str)), default=None)
    default_ship_to_address = attr.ib(validator=optional(instance_of(str)), default=None)
    payment_days = attr.ib(validator=optional(instance_of(str)), default=None)
    address = attr.ib(validator=optional(instance_of(str)), default=None)
    currency = attr.ib(validator=optional(instance_of(str)), default=None)
    tax_rule = attr.ib(validator=optional(instance_of(str)), default=None)
    accounting_code = attr.ib(validator=optional(instance_of(str)), default=None)
