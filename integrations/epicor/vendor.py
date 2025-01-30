import attr
from epicor.base import BaseObject
from epicor.json_encoders.generic import NewGenericJsonEncoder


@attr.s
class Vendor(BaseObject):

    base_url = 'Erp.BO.VendorSvc/'
    resource_name = 'Vendors'
    encoder_class = NewGenericJsonEncoder

    VendorNum = attr.ib(validator=attr.validators.instance_of(int))
    Name = attr.ib(validator=attr.validators.instance_of(str))
    Approved = attr.ib(validator=attr.validators.instance_of(bool))
    EarlyBuffer = attr.ib(validator=attr.validators.instance_of(int))
    LateBuffer = attr.ib(validator=attr.validators.instance_of(int))
    MinOrderValue = attr.ib(validator=attr.validators.optional(
        attr.validators.instance_of(tuple([float, int]))), default=None)
    VendorID = attr.ib(default='', validator=attr.validators.instance_of(str))
    Comment = attr.ib(default='', validator=attr.validators.instance_of(str))
    Inactive = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    EMailAddress = attr.ib(default='', validator=attr.validators.instance_of(str))

    @classmethod
    def get_by_id(cls, vendor_id: str):
        return cls.get_by('VendorID', vendor_id)
