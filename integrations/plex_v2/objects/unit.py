import attr
from attr.validators import instance_of, optional
from plex_v2.objects.base import BaseObject, RetrieveMixin, SearchMixin


@attr.s(kw_only=True, repr=False)
class Unit(BaseObject, RetrieveMixin, SearchMixin):
    _resource_name = 'edi/v1/units'
    id = attr.ib(validator=optional(instance_of(str)), default="00000000-0000-0000-0000-000000000000")
    unit = attr.ib(validator=optional(instance_of(str)), default=None)
    denominatorUnit = attr.ib(validator=optional(instance_of(str)), default=None)
    ediCode = attr.ib(validator=optional(instance_of(str)), default=None)
    weightUnit = attr.ib(validator=optional(instance_of(bool)), default=None)
    pieceUnit = attr.ib(validator=optional(instance_of(bool)), default=None)
    hourUnit = attr.ib(validator=optional(instance_of(bool)), default=None)
    dayUnit = attr.ib(validator=optional(instance_of(bool)), default=None)
    weekUnit = attr.ib(validator=optional(instance_of(bool)), default=None)
    monthUnit = attr.ib(validator=optional(instance_of(bool)), default=None)
    yearUnit = attr.ib(validator=optional(instance_of(bool)), default=None)
    unitStandard = attr.ib(validator=optional(instance_of(str)), default=None)
    areaUnit = attr.ib(validator=optional(instance_of(bool)), default=None)
    reference = attr.ib(validator=optional(instance_of(str)), default=None)

    @classmethod
    def find_units(
            cls,
            unit_name=None,
            resource_name_kwargs=None,
    ):
        return cls.search(
            unit=unit_name,
            exclude_if_null=['unit'],
            resource_name_kwargs=resource_name_kwargs,
        )
