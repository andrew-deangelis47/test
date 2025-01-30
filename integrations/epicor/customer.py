import attr
from epicor.client import EpicorClient
from typing import Optional, List
from epicor.base import BaseObject


@attr.s
class Contact(BaseObject):
    base_url = 'Erp.BO.CustCntSvc/'
    resource_name = 'CustCnts'

    Company = attr.ib(validator=attr.validators.instance_of(str))
    CustNum = attr.ib(validator=attr.validators.instance_of(int))
    Name = attr.ib(validator=attr.validators.instance_of(str))
    Inactive = attr.ib(validator=attr.validators.instance_of(bool))
    CustNumCustID = attr.ib(default='', validator=attr.validators.instance_of(str))
    PhoneNum: Optional[str] = attr.ib(default='',
                                      validator=attr.validators.optional(
                                          attr.validators.instance_of(str)))
    EMailAddress: Optional[str] = attr.ib(default='',
                                          validator=attr.validators.optional(
                                              attr.validators.instance_of(
                                                  str)))
    Comment: Optional[str] = attr.ib(default='',
                                     validator=attr.validators.optional(
                                         attr.validators.instance_of(str)))
    FirstName: Optional[str] = attr.ib(default='',
                                       validator=attr.validators.optional(
                                           attr.validators.instance_of(str)))
    LastName: Optional[str] = attr.ib(default='',
                                      validator=attr.validators.optional(
                                          attr.validators.instance_of(str)))
    ConNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    PerConID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)

    @classmethod
    def get_by_cust_and_email(cls, email_addr: str, cust_num: int):
        """
        Check if there exists a contact with the provided email and is assigned to the given customer.
        """
        return cls.get_first({'EMailAddress': email_addr, 'CustNum': cust_num})

    @classmethod
    def get_by_cust_name(cls, first_name: str, last_name: str, cust_num: int):
        """
        Check if there exists a contact with the provided first name/last name from Paperless Parts, assigned to the
        given customer.
        """
        name = f"{first_name} {last_name}"
        return cls.get_first({'Name': name, 'CustNum': cust_num})


@attr.s
class ShipTo(BaseObject):
    base_url = 'Erp.BO.ShipToSvc/'
    resource_name = 'ShipToes'

    Company: str = attr.ib(validator=attr.validators.instance_of(str))
    CustNum: int = attr.ib(validator=attr.validators.instance_of(int))
    ShipToNum: str = attr.ib(validator=attr.validators.instance_of(str))
    Name: Optional[str] = attr.ib(default='',
                                  validator=attr.validators.optional(
                                      attr.validators.instance_of(str)))
    Address1: Optional[str] = attr.ib(default='',
                                      validator=attr.validators.optional(
                                          attr.validators.instance_of(str)))
    Address2: Optional[str] = attr.ib(default='',
                                      validator=attr.validators.optional(
                                          attr.validators.instance_of(str)))
    Address3: Optional[str] = attr.ib(default='',
                                      validator=attr.validators.optional(
                                          attr.validators.instance_of(str)))
    City: Optional[str] = attr.ib(default='',
                                  validator=attr.validators.optional(
                                      attr.validators.instance_of(str)))
    State: Optional[str] = attr.ib(default='',
                                   validator=attr.validators.optional(
                                       attr.validators.instance_of(str)))
    ZIP: Optional[str] = attr.ib(default='',
                                 validator=attr.validators.optional(
                                     attr.validators.instance_of(str)))
    Country: Optional[str] = attr.ib(default='',
                                     validator=attr.validators.optional(
                                         attr.validators.instance_of(str)))
    SalesRepCode: Optional[str] = attr.ib(default='',
                                          validator=attr.validators.optional(
                                              attr.validators.instance_of(
                                                  str)))
    TerritoryID: Optional[str] = attr.ib(default='',
                                         validator=attr.validators.optional(
                                             attr.validators.instance_of(str)))
    ShipViaCode: Optional[str] = attr.ib(default='',
                                         validator=attr.validators.optional(
                                             attr.validators.instance_of(str)))


@attr.s
class Country(BaseObject):
    base_url = 'Erp.BO.CountrySvc/'
    resource_name = 'Countries'

    Company = attr.ib(validator=attr.validators.instance_of(str))
    CountryNum = attr.ib(validator=attr.validators.instance_of(int))
    Description = attr.ib(validator=attr.validators.instance_of(str))


@attr.s
class Customer(BaseObject):
    base_url = 'Erp.BO.CustomerSvc/'
    resource_name = 'Customers'

    Company = attr.ib(validator=attr.validators.instance_of(str))
    CustID = attr.ib(validator=attr.validators.instance_of(str))
    Name = attr.ib(validator=attr.validators.instance_of(str))
    Address1 = attr.ib(validator=attr.validators.instance_of(str))
    City = attr.ib(validator=attr.validators.instance_of(str))
    State = attr.ib(validator=attr.validators.instance_of(str))
    Zip = attr.ib(validator=attr.validators.instance_of(str))
    Country = attr.ib(validator=attr.validators.instance_of(str))
    TermsCode = attr.ib(validator=attr.validators.instance_of(str))
    Inactive: Optional[int] = attr.ib(default=None,
                                      validator=attr.validators.optional(attr.validators.instance_of(bool)))
    CustNum: Optional[int] = attr.ib(default=None,
                                     validator=attr.validators.optional(
                                         attr.validators.instance_of(int)))
    CustURL: Optional[str] = attr.ib(default='',
                                     validator=attr.validators.optional(
                                         attr.validators.instance_of(str)))
    Comment: Optional[str] = attr.ib(default='',
                                     validator=attr.validators.optional(
                                         attr.validators.instance_of(str)))
    Address2: Optional[str] = attr.ib(default='',
                                      validator=attr.validators.optional(
                                          attr.validators.instance_of(str)))
    Address3: Optional[str] = attr.ib(default='',
                                      validator=attr.validators.optional(
                                          attr.validators.instance_of(str)))
    EMailAddress: Optional[str] = attr.ib(default='',
                                          validator=attr.validators.optional(
                                              attr.validators.instance_of(
                                                  str)))
    PhoneNum: Optional[str] = attr.ib(default='',
                                      validator=attr.validators.optional(
                                          attr.validators.instance_of(str)))
    TerritoryID: Optional[str] = attr.ib(default='',
                                         validator=attr.validators.optional(
                                             attr.validators.instance_of(str)))
    SalesRepCode: Optional[str] = attr.ib(default='',
                                          validator=attr.validators.optional(
                                              attr.validators.instance_of(
                                                  str)))
    # Bill To
    BTName: Optional[str] = attr.ib(default='',
                                    validator=attr.validators.optional(
                                        attr.validators.instance_of(str)))
    BTAddress1: Optional[str] = attr.ib(default='',
                                        validator=attr.validators.optional(
                                            attr.validators.instance_of(str)))
    BTAddress2: Optional[str] = attr.ib(default='',
                                        validator=attr.validators.optional(
                                            attr.validators.instance_of(str)))
    BTAddress3: Optional[str] = attr.ib(default='',
                                        validator=attr.validators.optional(
                                            attr.validators.instance_of(str)))
    BTCity: Optional[str] = attr.ib(default='',
                                    validator=attr.validators.optional(
                                        attr.validators.instance_of(str)))
    BTState: Optional[str] = attr.ib(default='',
                                     validator=attr.validators.optional(
                                         attr.validators.instance_of(str)))
    BTZip: Optional[str] = attr.ib(default='',
                                   validator=attr.validators.optional(
                                       attr.validators.instance_of(str)))
    BTCountry: Optional[str] = attr.ib(default='',
                                       validator=attr.validators.optional(
                                           attr.validators.instance_of(str)))
    BTPhoneNum: Optional[str] = attr.ib(default='',
                                        validator=attr.validators.optional(
                                            attr.validators.instance_of(str)))

    @classmethod
    def get_by_id(cls, cust_id: str):
        """
        Get a Customer record with the given ID
        @param cust_id: string value of the customer ID
        @return: the instance of the customer record matching the ID or None
        """
        cust_id = cust_id.replace("'", "") if cust_id is not None else None
        return cls.get_by('CustID', cust_id)

    @classmethod
    def get_by_name(cls, cust_name: str):
        return cls.get_by('Name', cust_name)

    def add_price_list(self, price_list_id: str) -> bool:
        """
        Add a price list to the customer.
        @returns success/failure
        """

        client: EpicorClient = EpicorClient.get_instance()
        url = f'{self.base_url}CustomerPriceLsts'
        data = {
            "Company": self.Company,
            "CustNum": self.CustNum,
            "ShipToNum": "",
            "SeqNum": 0,
            "ListCode": price_list_id

        }
        resp_json = client.post_resource(url, data=data)
        # TODO: I don't think there is a good way to check if this worked,
        #  but maybe we can check based on if the sequence returned is not 1
        return resp_json.get('SeqNum', 0) > 0

    def get_contacts(self) -> List[Contact]:
        """
        Get a list of contacts associated with this customer
        """
        return Contact.get_all({'CustNum': self.CustNum}, {'$top': '1000'})

    def ship_toes(self):
        return ShipTo.get_all({'CustNum': self.CustNum}, {'$top': '1000'})


@attr.s
class PaymentTerms(BaseObject):
    base_url = 'Erp.BO.TermsSvc/'
    resource_name = 'Terms'

    TermsCode = attr.ib(validator=attr.validators.instance_of(str))
    TermsType = attr.ib(validator=attr.validators.instance_of(str))
    Description = attr.ib(validator=attr.validators.instance_of(str))
    NumberOfDays = attr.ib(validator=attr.validators.instance_of(int))

    @classmethod
    def get_by_code(cls, code: str):
        return cls.get_by('TermsCode', code)

    @classmethod
    def get_code_by_description(cls, description: str):
        return cls.get_by('Description', description)
