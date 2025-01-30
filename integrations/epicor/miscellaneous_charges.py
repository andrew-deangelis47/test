from epicor.base import BaseObject
import attr
from decimal import Decimal


@attr.s
class MiscCharge(BaseObject):
    base_url = 'Erp.BO.MiscChrgSvc/'
    resource_name = 'MiscChrgs'

    Company = attr.ib(validator=attr.validators.instance_of(str))
    MiscCode = attr.ib(validator=attr.validators.instance_of(str))
    Description = attr.ib(validator=attr.validators.instance_of(str))
    FreqCode = attr.ib(validator=attr.validators.instance_of(str))
    MiscAmt = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    Type = attr.ib(validator=attr.validators.instance_of(str))


@attr.s
class QuoteMiscellaneousCharge(BaseObject):
    base_url = 'Erp.BO.QuoteSvc/'
    resource_name = 'QuoteMscs'

    Company = attr.ib(validator=attr.validators.instance_of(str))
    QuoteNum = attr.ib(validator=attr.validators.instance_of(int))
    MiscCode = attr.ib(validator=attr.validators.instance_of(str))
    Description = attr.ib(validator=attr.validators.instance_of(str))
    MiscAmt = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    DocMiscAmt = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    DspMiscAmt = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    DocDspMiscAmt = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    QuoteLine = attr.ib(validator=attr.validators.instance_of(int))
    FreqCode = attr.ib(validator=attr.validators.instance_of(str))
