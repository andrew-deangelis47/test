# https://omega-ep-03.opinc.com/epicorerptest/api/help/v2/odata/Erp.BO.WorkforceSearchSvc/index#/OData/GetRows_WorkforceSearches
from epicor.base import BaseObject
import attr


@attr.s
class Salesperson(BaseObject):
    base_url = 'Erp.BO.SalesRepSvc/'
    resource_name = 'SalesReps'

    Company = attr.ib(validator=attr.validators.instance_of(str))
    SalesRepCode = attr.ib(validator=attr.validators.instance_of(str))
    Name = attr.ib(validator=attr.validators.instance_of(str))
    EMailAddress = attr.ib(validator=attr.validators.instance_of(str))

    @classmethod
    def get_by_id(cls, sales_rep_code: str):
        """
        Get a Salesperson record with the given ID
        @param sales_rep_code: string value of the salesperson ID
        @return: the instance of the salesperson record matching the ID or None
        """
        sales_rep_code = sales_rep_code.replace("'", "") if sales_rep_code is not None else None
        return cls.get_by('SalesRepCode', sales_rep_code)
