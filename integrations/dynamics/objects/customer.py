import attr

from baseintegration.exporter.order_exporter import logger

from dynamics.exceptions import DynamicsNotFoundException
from dynamics.objects.base import BaseObject, str_type


@attr.s
class AddressMixin:
    Address = attr.ib(**str_type)
    Address_2 = attr.ib(**str_type)
    City = attr.ib(**str_type)
    County = attr.ib(**str_type)
    Post_Code = attr.ib(**str_type)
    Country_Region_Code = attr.ib(**str_type)

    def get_country(self):
        try:
            return CountryCode.get_first({
                "Code": self.Country_Region_Code
            }).Name
        except DynamicsNotFoundException:
            return None

    def address_exists(self):
        """
        Determine whether the address has been filled in.
        """
        if self.Address and self.City and self.County and self.Country_Region_Code and self.Post_Code:
            return True
        else:
            return False


@attr.s
class ContactInfoMixin:
    E_Mail = attr.ib(**str_type)
    Phone_No = attr.ib(**str_type)


@attr.s
class Contact(BaseObject, AddressMixin, ContactInfoMixin):

    resource_name = 'Contact_Card'

    No = attr.ib(**str_type)
    Company_Name = attr.ib(**str_type)
    Type = attr.ib(**str_type)
    Name = attr.ib(**str_type)
    First_Name = attr.ib(**str_type)
    Surname = attr.ib(**str_type)

    def get_customer_num(self):
        customer = Customer.get_first({
            'Name': self.Company_Name
        })
        return customer.No


@attr.s
class Customer(BaseObject, AddressMixin, ContactInfoMixin):

    resource_name = 'Customer_Card'

    No = attr.ib(**str_type)
    Name = attr.ib(**str_type)
    Home_Page = attr.ib(**str_type)
    Payment_Terms_Code = attr.ib(**str_type)
    Gen_Bus_Posting_Group = attr.ib(**str_type)
    Customer_Posting_Group = attr.ib(**str_type)
    Tax_Area_Code = attr.ib(**str_type)

    def get_payment_terms_period(self):
        try:
            period = PaymentTerm.get_first({
                "Code": self.Payment_Terms_Code
            }).Due_Date_Calculation
            try:
                assert period.endswith('D')
                payment_days = period[0:-1]
                return int(payment_days)
            except:
                logger.info(f'Could not parse due date calculation {period} as a payment terms period.')
                return None
        except DynamicsNotFoundException:
            return None


@attr.s
class PaymentTerm(BaseObject):

    resource_name = 'Payment_Terms'

    Code = attr.ib(**str_type)
    Due_Date_Calculation = attr.ib(**str_type)


@attr.s
class CountryCode(BaseObject):

    resource_name = 'Country_Region'

    Code = attr.ib(**str_type)
    Name = attr.ib(**str_type)
