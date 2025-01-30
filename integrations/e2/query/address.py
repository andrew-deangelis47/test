from e2.models import CustomerCode, Shipto
import re
from typing import Optional
from baseintegration.utils import address_tokenize, set_blank_to_default_value
from e2.utils.utils import smart_truncate


def update_billing_address(customer_code: CustomerCode, addr_dict: dict):
    phone = addr_dict.get('phone')
    phone_ext = addr_dict.get('phone_ext')
    if phone:
        if phone_ext:
            apphone = f'{phone} x{phone_ext}'
        else:
            apphone = phone
    else:
        apphone = None

    ap_contact = addr_dict.get('attention')

    customer_code.b_addr1 = addr_dict.get('address1')
    customer_code.b_addr2 = addr_dict.get('address2')
    customer_code.apcontact = ap_contact
    customer_code.b_city = addr_dict.get('city')
    customer_code.b_country = addr_dict.get('country')
    customer_code.apphone = apphone
    customer_code.b_zip_code = addr_dict.get('postal_code')
    customer_code.b_state = addr_dict.get('state')
    customer_code.save()


def get_or_create_shipping_address(customer_code: CustomerCode, addr_dict: dict) -> Shipto:
    shipping_address = match_shipping_address(customer_code, addr_dict)
    if shipping_address is None:
        shipping_address = create_shipping_address(customer_code, addr_dict)
    return shipping_address


def create_shipping_address(customer_code: CustomerCode, addr_dict: dict):
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

    location = addr_dict.get('facility_name')
    if location is None:
        location = assign_location_for_shipping_address(customer_code)
    location = smart_truncate(location, 30)

    shipping_address = Shipto.objects.create(
        custcode=customer_code.customer_code,
        saddr1=saddr1,
        saddr2=saddr2,
        scity=scity,
        sstate=sstate,
        szipcode=szipcode,
        scountry=scountry,
        shipphone=shipphone,
        shipcontact=shipcontact,
        location=location,
    )
    return shipping_address


def assign_location_for_shipping_address(customer_code: CustomerCode):
    cust_code = customer_code.customer_code
    existing_shipping_address_count = Shipto.objects.filter(custcode=cust_code).count()
    location_name = f'LOCATION{existing_shipping_address_count+1}'
    return location_name


def get_shipping_address_by_location(customer_code: CustomerCode, location: str):
    cust_code = customer_code.customer_code
    shipping_address = Shipto.objects.filter(custcode=cust_code, location=location).first()
    return shipping_address


def match_shipping_address(customer_code: CustomerCode, addr_dict: dict) -> Optional[Shipto]:  # noqa: C901
    """
    Find a matching shipping address (case insensitive) for a given customer looking at
    concatenated name, address line 1 and 2, city, state, zip, country, and
    concatenated phone number. For address line 1 and 2, street suffix
    abbreviations are intuitively matched and punctuation is ignored. Zip code
    intuitively handles plus-4 extensions.

    :param customer_code: CustomerCode record
    :param addr_dict: Dictionary containing address fields. Generate using
    ``paperless.objects.Address.to_json()``.
    :return: Shipto if found; otherwise None
    """
    country_code = addr_dict.get('country')
    phone = addr_dict.get('phone')
    if phone and addr_dict.get('phone_ext'):
        phone += ' x{}'.format(addr_dict.get('phone_ext'))
    # first get the set of candidate addresses for this customer
    qs = Shipto.objects.filter(
        custcode=customer_code.customer_code,
        scity__iexact=addr_dict.get('city'),
        sstate__iexact=addr_dict.get('state'),
        scountry=country_code,
    ).order_by('-shipto_id')
    # next iterate through candidate address and return the first fuzzy match
    # we assume there will never be a very large number of addresses for a
    # single customer
    for candidate_address in qs.all():
        # address line 2
        if address_tokenize(candidate_address.saddr1) != address_tokenize(
                addr_dict.get('address1')):
            continue
        # address line 2
        if addr_dict.get('address2') and address_tokenize(
                candidate_address.saddr2) != address_tokenize(
                addr_dict.get('address2')
        ):
            continue
        # zip code
        if candidate_address.szipcode is None:
            continue
        if len(addr_dict.get('postal_code', '')) == 5:
            if addr_dict.get('postal_code') != set_blank_to_default_value(candidate_address.szipcode, '')[0:5]:
                continue
        elif len(addr_dict.get('postal_code', '')) == 10:
            if len(candidate_address.szipcode) == 5:
                if candidate_address.szipcode != addr_dict.get('postal_code', '')[0:5]:
                    continue
            else:
                if candidate_address.szipcode != addr_dict.get('postal_code'):
                    continue
        elif addr_dict.get('postal_code') != candidate_address.szipcode:
            continue
        # phone
        if phone and candidate_address.shipphone:
            if re.sub("[^0-9]", "", phone) != re.sub("[^0-9]", "",
                                                     candidate_address.shipphone):
                continue
        return candidate_address
    return None
