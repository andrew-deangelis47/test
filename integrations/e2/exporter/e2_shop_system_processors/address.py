from e2.exporter.processors.address import AddressProcessor
from paperless.objects.orders import Order
from e2.models import CustomerCode, Shipto
from e2.query.address import match_shipping_address
from e2.utils.utils import smart_truncate


class E2ShopSystemAddressProcessor(AddressProcessor):

    @staticmethod
    def get_shipping_address(customer_code: CustomerCode):
        cust_code = customer_code.customer_code
        shipping_address = Shipto.objects.filter(custcode=cust_code).first()
        return shipping_address

    def get_or_create_shipping_address(self, customer: CustomerCode, addr_dict: dict):
        """ Try to match on the facility name first. If that doesn't work, try matching based on the address fields. """
        shipping_address = None
        facility_name = addr_dict.get('facility_name')
        if facility_name is not None:
            shipping_address = self.get_shipping_address(customer)
        if shipping_address is None:
            shipping_address = self.create_shipping_address(customer, addr_dict)
        return shipping_address

    def create_shipping_address(self, customer_code: CustomerCode, addr_dict: dict):
        phone = addr_dict.get('phone')
        phone_ext = addr_dict.get('phone_ext')
        if phone:
            if phone_ext:
                shipphone = f'{phone} x{phone_ext}'
            else:
                shipphone = phone
        else:
            shipphone = None

        saddr1 = smart_truncate(addr_dict.get('address1'), 50)
        saddr2 = smart_truncate(addr_dict.get('address2'), 50)
        scity = smart_truncate(addr_dict.get('city'), 50)
        sstate = smart_truncate(addr_dict.get('state'), 2)
        szipcode = smart_truncate(addr_dict.get('postal_code'), 10)
        scountry = smart_truncate(addr_dict.get('country'), 30)
        shipcontact = smart_truncate(addr_dict.get('attention'), 30)

        shipping_address = Shipto.objects.create(
            custcode=customer_code.customer_code,
            saddr1=saddr1,
            saddr2=saddr2,
            scity=scity,
            sstate=sstate,
            szipcode=szipcode,
            scountry=scountry,
            shipphone=shipphone,
            shipcontact=shipcontact
        )
        return shipping_address

    def get_shipping_info(self, order: Order, customer: CustomerCode, customer_is_new: bool):
        if order.shipping_info is not None:
            shipping_addr_dict = self.create_shipping_addr_dict(order.shipping_info)
            should_create_shipping_address = self.should_create_e2_shipping_address(customer_is_new)
            if should_create_shipping_address:
                ship_to: Shipto = self.get_or_create_shipping_address(
                    customer,
                    shipping_addr_dict,
                )
            else:
                # If the user doesn't want us to create new shipping addresses in E2, just try to match on existing ones
                ship_to = match_shipping_address(
                    customer,
                    shipping_addr_dict
                )
            return ship_to
        else:
            # If a shipping address is not supplied on the Paperless Parts order, try to use the default shipping
            # address for this customer in E2
            default_ship_to = None
            default_location = customer.location
            if default_location is not None:
                default_ship_to = self.get_shipping_address(customer)
            return default_ship_to
