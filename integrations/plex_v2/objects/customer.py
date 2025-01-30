# https://developers.plex.com/customers-api/apis
import attr
from attr.validators import optional, instance_of
from plex_v2.objects.base import BaseObject, CreateMixin, RetrieveMixin, SearchMixin
from fuzzywuzzy import fuzz, process


@attr.s(kw_only=True)
class Customer(BaseObject, CreateMixin, RetrieveMixin, SearchMixin):
    _resource_name = 'mdm/v1/customers'

    @classmethod
    def get_serialization_schema(cls, mode):
        if mode == 'out':
            schema = super().get_serialization_schema('out')
            del schema['id']
            return schema
        elif mode == 'in':
            return super().get_serialization_schema('in')

    code = attr.ib(validator=instance_of(str))
    name = attr.ib(validator=instance_of(str))
    status = attr.ib(validator=instance_of(str))
    type = attr.ib(validator=instance_of(str))
    note = attr.ib(default='')
    businessType = attr.ib(validator=instance_of(str), default='')
    createdDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default='')
    modifiedDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default='')

    @classmethod
    def find_customers(cls, id=None, code=None, name=None, status=None):
        return cls.search(
            id=id,
            code=code,
            name=name,
            status=status
        )


@attr.s(kw_only=True, repr=False)
class CustomerAddress(BaseObject, CreateMixin, RetrieveMixin, SearchMixin):
    code = attr.ib(validator=instance_of(str))

    phone = attr.ib(validator=optional(instance_of(str)), default=None)
    fax = attr.ib(validator=optional(instance_of(str)), default=None)
    email = attr.ib(validator=optional(instance_of(str)), default=None)
    name = attr.ib(validator=optional(instance_of(str)), default=None)

    # Address Functions
    quoteTo = attr.ib(validator=instance_of(bool), default=False)
    shipTo = attr.ib(validator=instance_of(bool), default=False)
    billTo = attr.ib(validator=instance_of(bool), default=False)
    remitTo = attr.ib(validator=instance_of(bool), default=False)
    thirdPartyShipTo = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    soldTo = attr.ib(validator=instance_of(bool), default=False)
    active = attr.ib(validator=instance_of(bool), default=False)

    note = attr.ib(validator=optional(instance_of(str)), default=None)

    address = attr.ib(validator=optional(instance_of(str)), default=None)
    city = attr.ib(validator=optional(instance_of(str)), default=None)
    state = attr.ib(validator=optional(instance_of(str)), default=None)
    zip = attr.ib(validator=optional(instance_of(str)), default=None)
    country = attr.ib(validator=optional(instance_of(str)), default=None)

    billToAddressId = attr.ib(validator=optional(instance_of(str)), default=None)

    customerId = attr.ib(validator=optional(instance_of(str)), default=None)

    _customer = None

    def __repr__(self):
        return f'{self.address} {self.city} {self.state} {self.zip} {self.country}'

    @classmethod
    def get_serialization_schema(cls, mode):  # TODO: have id not in schema BY DEFAULT
        if mode == 'out':
            schema = super().get_serialization_schema('out')
            del schema['id']
            del schema['customerId']
            return schema
        elif mode == 'in':
            return super().get_serialization_schema('in')

    @classmethod
    def get_resource_name(cls, action, instance=None, **kwargs):
        if instance is not None:
            customer_id = instance.customerId
            if customer_id is not None:
                return f'mdm/v1/customers/{customer_id}/addresses'
        if 'customer_id' not in kwargs:
            raise KeyError('customer_id must supplied as an entry to resource_name_kwargs')
        customer_id = kwargs['customer_id']
        return f'mdm/v1/customers/{customer_id}/addresses'

    def fuzzy_extract_matching_address(self, other_customer_addresses):
        if len(other_customer_addresses) == 0:
            return None
        customer_address, score = process.extractOne(
            self,
            other_customer_addresses,
            processor=lambda x: repr(x),
            scorer=fuzz.token_sort_ratio,
        )
        if score < 100:
            return None
        else:
            return customer_address

    @property
    def customer(self):
        if self._customer is not None:
            return self._customer
        else:
            customer = Customer.get(self.customerId)
            self._customer = customer
            return customer

    @customer.setter
    def customer(self, value):
        self._customer = value

    @classmethod
    def find_customer_addresses(
            cls,
            billTo=None,
            remitTo=None,
            shipTo=None,
            soldTo=None,
            code=None,
            resource_name_kwargs=None,
    ):
        return cls.search(
            billTo=billTo,
            remitTo=remitTo,
            shipTo=shipTo,
            soldTo=soldTo,
            code=code,
            exclude_if_null=['code', 'billTo', 'remitTo', 'shipTo', 'soldTo'],
            resource_name_kwargs=resource_name_kwargs,
        )


@attr.s(kw_only=True)
class CustomerPart(BaseObject, CreateMixin, RetrieveMixin, SearchMixin):
    _resource_name = 'mdm/v1/customer-parts'

    number = attr.ib(validator=instance_of(str))

    partId = attr.ib(validator=optional(instance_of(str)), default=None)
    customerId = attr.ib(validator=optional(instance_of(str)), default=None)
    description = attr.ib(validator=optional(instance_of(str)), default=None)
    revision = attr.ib(validator=optional(instance_of(str)), default=None)

    @classmethod
    def get_serialization_schema(cls, mode):  # TODO: have id not in schema BY DEFAULT
        if mode == 'out':
            schema = super().get_serialization_schema('out')
            del schema['id']
            return schema
        elif mode == 'in':
            return super().get_serialization_schema('in')

    @classmethod
    def find_customer_parts(cls, number=None, partId=None, customerId=None):
        return cls.search(
            number=number,
            partId=partId,
            customerId=customerId,
            exclude_if_null=['number', 'partId', 'customerId']
        )


@attr.s(kw_only=True, repr=False)
class CustomerContact(BaseObject, CreateMixin, RetrieveMixin, SearchMixin):
    _resource_name = 'mdm/v1/contacts'
    customerId = attr.ib(validator=optional(instance_of(str)), default=None)
    firstName = attr.ib(validator=optional(instance_of(str)), default=None)
    lastName = attr.ib(validator=optional(instance_of(str)), default=None)
    supplierId = attr.ib(validator=optional(instance_of(str)), default=None)
    phone = attr.ib(validator=optional(instance_of(str)), default=None)
    fax = attr.ib(validator=optional(instance_of(str)), default=None)
    mobilePhone = attr.ib(validator=optional(instance_of(str)), default=None)
    title = attr.ib(validator=optional(instance_of(str)), default=None)
    note = attr.ib(validator=optional(instance_of(str)), default=None)
    email = attr.ib(validator=optional(instance_of(str)), default=None)
    companyName = attr.ib(validator=optional(instance_of(str)), default=None)
    officeAddress = attr.ib(validator=optional(instance_of(str)), default=None)
    homeAddress = attr.ib(validator=optional(instance_of(str)), default=None)
    private = attr.ib(validator=optional(instance_of(int)), default=None)
    description = attr.ib(validator=optional(instance_of(str)), default=None)
    url = attr.ib(validator=optional(instance_of(str)), default=None)
    sortOrder = attr.ib(validator=optional(instance_of(int)), default=None)
    type = attr.ib(validator=optional(instance_of(str)), default=None)
    associatedWithId = attr.ib(validator=optional(instance_of(str)), default=None)

    @classmethod
    def get_serialization_schema(cls, mode):
        if mode == 'out':
            schema = super().get_serialization_schema('out')
            del schema['id']
            return schema
        elif mode == 'in':
            return super().get_serialization_schema('in')

    @classmethod
    def find_customer_contacts(
            cls,
            customer_id=None,
            resource_name_kwargs=None,
    ):
        return cls.search(
            customerId=customer_id,
            exclude_if_null=['customerId'],
            resource_name_kwargs=resource_name_kwargs,
        )
