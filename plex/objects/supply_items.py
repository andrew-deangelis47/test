import attr
from attr.validators import instance_of, optional
from plex.objects.base import BaseObject, SearchMixin


@attr.s(kw_only=True)
class SupplyItem(BaseObject, SearchMixin):
    _resource_name = 'mdm/v1/supply-items'

    supplyItemNumber = attr.ib(validator=optional(instance_of(str)), default=None)
    type = attr.ib(validator=optional(instance_of(str)), default=None)
    category = attr.ib(validator=optional(instance_of(str)), default=None)
    priority = attr.ib(validator=optional(instance_of(str)), default=None)
    group = attr.ib(validator=optional(instance_of(str)), default=None)
    description = attr.ib(validator=optional(instance_of(str)), default=None)
    customerUnitPrice = attr.ib(validator=optional(instance_of((int, float))), default=None)
    inventoryUnit = attr.ib(validator=optional(instance_of(str)), default=None)
    briefDescription = attr.ib(validator=optional(instance_of(str)), default=None)
    accountId = attr.ib(validator=optional(instance_of(str)), default=None)
    manufacturerCode = attr.ib(validator=optional(instance_of(str)), default=None)
    supplierId = attr.ib(validator=optional(instance_of(str)), default=None)
    manufacturerItemNumber = attr.ib(validator=optional(instance_of(str)), default=None)
    manufacturerItemRevision = attr.ib(validator=optional(instance_of(str)), default=None)
    manufacturerText = attr.ib(validator=optional(instance_of(str)), default=None)
    createdDate = attr.ib(validator=optional(instance_of(str)), default=None)
    createdById = attr.ib(validator=optional(instance_of(str)), default=None)
    modifiedDate = attr.ib(validator=optional(instance_of(str)), default=None)
    modifiedById = attr.ib(validator=optional(instance_of(str)), default=None)
    taxCodeNumber = attr.ib(validator=optional(instance_of((int, float))), default=None)
    maxQuantity = attr.ib(validator=optional(instance_of((int, float))), default=None)
    minQuantity = attr.ib(validator=optional(instance_of((int, float))), default=None)
    note = attr.ib(validator=optional(instance_of(str)), default=None)
    updateWhenReceived = attr.ib(validator=optional(instance_of(bool)), default=None)
    active = attr.ib(validator=optional(instance_of(bool)), default=None)
    averageCost = attr.ib(validator=optional(instance_of((int, float))), default=None)
    responsiblePersonId = attr.ib(validator=optional(instance_of(str)), default=None)
    vendorManaged = attr.ib(validator=optional(instance_of(bool)), default=None)
    commodity = attr.ib(validator=optional(instance_of(str)), default=None)
    countryOfOrigin = attr.ib(validator=optional(instance_of(str)), default=None)
    consignment = attr.ib(validator=optional(instance_of(bool)), default=None)

    @classmethod
    def find_supply_items(cls, supply_item_number=None, type=None, category=None, group=None):
        return cls.search(
            supplyItemNumber=supply_item_number,
            type=type,
            category=category,
            group=group,
            exclude_if_null=['supplyItemNumber', 'type', 'category', 'group']
        )
