import attr
from typing import List
from ...baseintegration.utils import current_datetime_utc
from ...baseintegration.utils.repeat_work_base import BaseObject


@attr.s
class Part(BaseObject):
    part_number = attr.ib(validator=attr.validators.instance_of(str))
    erp_name = attr.ib(attr.validators.instance_of(str))
    revision = attr.ib(validator=attr.validators.instance_of(str), default=None,
                       converter=attr.converters.default_if_none(""))
    is_root = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    import_date = attr.ib(validator=attr.validators.instance_of(int), default=None,
                          converter=attr.converters.default_if_none(factory=current_datetime_utc))
    headers = attr.ib(validator=attr.validators.instance_of(List), default=None,
                      converter=attr.converters.default_if_none(factory=list))
    type = attr.ib(validator=attr.validators.in_(["assembled", "manufactured", "purchased"]), default=None,
                   converter=attr.converters.default_if_none("manufactured"))
    units = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default="in")
    size_x = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=0,
                     converter=attr.converters.optional(float))
    size_y = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=0,
                     converter=attr.converters.optional(float))
    size_z = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=0,
                     converter=attr.converters.optional(float))
    thickness = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=0,
                        converter=attr.converters.optional(float))
    area = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=0,
                   converter=attr.converters.optional(float))
    filename = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    description = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None,
                          converter=attr.converters.default_if_none(default=""))

    def __attrs_post_init__(self):
        if self.filename is None:
            self.filename = self.part_number


@attr.s
class MethodOfManufacture(BaseObject):
    make_qty = attr.ib(validator=attr.validators.instance_of(int), converter=attr.converters.optional(int))
    requested_qty = attr.ib(validator=attr.validators.instance_of(int), converter=attr.converters.optional(int))
    requires_yield_adjustment = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)),
                                        default=False)
    requires_markup_adjustment = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)),
                                         default=False)
    unit_price = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=0,
                         converter=attr.converters.optional(float))
    total_price = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=0,
                          converter=attr.converters.optional(float))
    operations = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(List)), factory=list)
    required_materials = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(List)), factory=list)
    children = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(List)), factory=list)


@attr.s
class Operation(BaseObject):
    is_finish = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    is_outside_service = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    name = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    notes = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None,
                    converter=attr.converters.default_if_none(default=""))
    position = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    runtime = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=0,
                      converter=attr.converters.optional(float))  # is overridden by runtime in costing_variables
    setup_time = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=0,
                         converter=attr.converters.optional(float))  # is overridden by setup_time in costing_variables
    total_cost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=0,
                         converter=attr.converters.optional(float))
    costing_variables = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(List)), factory=list)


@attr.s
class CostingVariable(BaseObject):
    label = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    value = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([str, int, float, bool]))),
                    default=None)


@attr.s
class RequiredMaterials(BaseObject):
    name = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    notes = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None,
                    converter=attr.converters.default_if_none(default=""))
    total_cost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=0,
                         converter=attr.converters.optional(float))
    costing_variables = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(List)), default=None)


@attr.s
class Child(BaseObject):
    part_number = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    revision = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None,
                       converter=attr.converters.default_if_none(""))
    qty_per_parent = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None,
                             converter=attr.converters.optional(int))


@attr.s
class AddOn(BaseObject):
    is_required = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    name = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    notes = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None,
                    converter=attr.converters.default_if_none(default=""))
    unit_price = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=None,
                         converter=attr.converters.optional(float))
    use_component_quantities = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)),
                                       default=False)


@attr.s
class Contact(BaseObject):
    email = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    first_name = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    last_name = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    notes = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None,
                    converter=attr.converters.default_if_none(default=""))
    phone = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)


@attr.s
class Account(BaseObject):
    name = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    erp_code = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    phone = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    url = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)


@attr.s
class Header(BaseObject):  # should only be created for root parts
    erp_code = attr.ib(validator=attr.validators.instance_of(str))
    type = attr.ib(attr.validators.in_(["template", "template_quote", "template_job", "estimated", "engineered",
                                        "executed"]))
    created_date = attr.ib(validator=attr.validators.instance_of(int), default=None,
                           converter=attr.converters.default_if_none(factory=current_datetime_utc))
    account = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Account)), default=None)
    contact = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Contact)), default=None)
    public_notes = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None,
                           converter=attr.converters.default_if_none(default=""))
    private_notes = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None,
                            converter=attr.converters.default_if_none(default=""))
    add_ons = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(List)), factory=list)
    methods_of_manufacture = attr.ib(validator=attr.validators.instance_of(List), default=None,
                                     converter=attr.converters.default_if_none(factory=list))
