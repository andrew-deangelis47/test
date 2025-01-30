from sage.models.sage_models.customer.address import Address
from sage.models.sage_models.customer.contact import Contact
from sage.models.sage_models.customer.customer import Customer
from typing import List
import attr
from attr.validators import instance_of, optional
from sage.models.sage_models.base_object import BaseObject

# this class represents a customer object, as well as associated contacts and addresses


class SageCustomerFullEntity(BaseObject):

    def __init__(self, customer: Customer = None, contacts: list = None, addresses: list = None):
        self.customer = customer
        self.contacts = contacts
        self.addresses = addresses

    customer = attr.ib(validator=optional(instance_of(Customer)), default=None)
    contacts = attr.ib(validator=optional(instance_of(List[Contact])), default=None)
    addresses = attr.ib(validator=optional(instance_of(List[Address])), default=None)
