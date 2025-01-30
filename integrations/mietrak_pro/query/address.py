from mietrak_pro.models import Party, Address, Addresstype, Country, State, Division, Salestaxtype
import re
from typing import Optional
from baseintegration.utils import address_tokenize, set_blank_to_default_value


def create_address(customer, addr_dict, address_type, address_name, division_pk: int = 1):
    phone_with_ext = get_phone_with_ext(addr_dict)

    country_code = addr_dict.get('country')
    country = get_country(country_code)

    state_code = addr_dict.get('state')
    state = get_state(state_code, country)

    division = Division.objects.get(divisionpk=division_pk)
    sales_tax_type = Salestaxtype.objects.get(salestaxtypepk=1)

    address = Address.objects.create(
        addresstypefk=address_type,
        statefk=state,
        countryfk=country,
        divisionfk=division,
        partyfk=customer,
        salestax1typefk=sales_tax_type,
        salestax2typefk=sales_tax_type,
        salestax3typefk=sales_tax_type,
        salestax4typefk=sales_tax_type,
        address1=addr_dict.get('address1'),
        address2=addr_dict.get('address2'),
        city=addr_dict.get('city'),
        zipcode=addr_dict.get('postal_code'),
        phone=phone_with_ext,
        contact=addr_dict.get('attention'),
        name=address_name,
        defaultshipping=0,
        remitaddress=0,
        archived=0,
        exported=0,
    )
    return address


def get_phone_with_ext(addr_dict):
    phone = addr_dict.get('phone')
    phone_ext = addr_dict.get('phone_ext')
    if phone:
        if phone_ext:
            phone_with_ext = f'{phone} x{phone_ext}'
        else:
            phone_with_ext = phone
    else:
        phone_with_ext = None
    return phone_with_ext


def assign_name_for_shipping_address(customer, address_type, addr_dict):
    """ Use the facility name as the shipping address name if it exists, otherwise use an incrementing placeholder """
    existing_shipping_address_count = Address.objects.filter(partyfk=customer, addresstypefk=address_type).count()
    name = f'Shipping Address {existing_shipping_address_count + 1}'
    facility_name = addr_dict.get('facility_name')
    if facility_name is not None:
        name = facility_name
    return name


def assign_name_for_billing_address(customer, address_type):
    existing_billing_address_count = Address.objects.filter(partyfk=customer, addresstypefk=address_type).count()
    name = f'Billing Address {existing_billing_address_count + 1}'
    return name


def create_shipping_address(customer, addr_dict, division_pk: int = 1):
    address_type = Addresstype.objects.get(description='Shipping')
    address_name = assign_name_for_shipping_address(customer, address_type, addr_dict)
    return create_address(customer, addr_dict, address_type, address_name, division_pk)


def create_billing_address(customer, addr_dict, division_pk: int = 1):
    address_type = Addresstype.objects.get(description='Billing')
    address_name = assign_name_for_billing_address(customer, address_type)
    return create_address(customer, addr_dict, address_type, address_name, division_pk)


def match_address(customer: Party, addr_dict: dict, address_type: Addresstype) -> Optional[Address]:
    """
    Find a matching address (case insensitive) for a given customer looking at
    concatenated name, address line 1 and 2, city, state, zip, country, and
    concatenated phone number. For address line 1 and 2, street suffix
    abbreviations are intuitively matched and punctuation is ignored. Zip code
    intuitively handles plus-4 extensions.

    :param customer: Party record
    :param addr_dict: Dictionary containing address fields.
    :return: Address if found; otherwise None
    """

    phone = get_phone_with_ext(addr_dict)

    country_code = addr_dict.get('country')
    country = get_country(country_code)

    state_code = addr_dict.get('state')
    state = get_state(state_code, country)

    # first get the set of candidate addresses for this customer
    qs = Address.objects.filter(
        partyfk=customer,
        addresstypefk=address_type,
        city__iexact=addr_dict.get('city'),
        statefk=state,
        countryfk=country,
    ).order_by('-addresspk')
    # next iterate through candidate address and return the first fuzzy match
    # we assume there will never be a very large number of addresses for a
    # single customer
    for candidate_address in qs.all():
        if skip_address(candidate_address, addr_dict, phone):
            continue
        return candidate_address
    return None


def skip_address(candidate_address: Address, addr_dict: dict, phone: str):  # noqa: C901
    """
    Determines if 2 addresses are a match and if then don't skip False else skip True.

    :param candidate_address: address from Django Models
    :param addr_dict: Dictionary containing address fields from Paperless Parts.
    :param phone: is the phone number plus extension from this function 'get_phone_with_ext'
    :return: True if to Skip; otherwise False
    """
    # address line 2
    if address_tokenize(candidate_address.address1) != address_tokenize(addr_dict.get('address1')):
        return True
    # address line 2
    if addr_dict.get('address2') and \
            address_tokenize(candidate_address.address2) != address_tokenize(addr_dict.get('address2')):
        return True
    # zip code
    if len(addr_dict.get('postal_code', '')) == 5 and addr_dict.get('postal_code') != set_blank_to_default_value(candidate_address.zipcode, '')[0:5]:
        return True
    elif len(addr_dict.get('postal_code', '')) == 10:
        if len(candidate_address.zipcode) == 5 and candidate_address.zipcode != addr_dict.get('postal_code', '')[0:5]:
            return True
        elif candidate_address.zipcode != addr_dict.get('postal_code'):
            return True
    elif addr_dict.get('postal_code') != candidate_address.zipcode:
        return True
    # phone
    if phone and candidate_address.phone and \
            re.sub("[^0-9]", "", phone) != re.sub("[^0-9]", "", candidate_address.phone):
        return True
    return False


def match_shipping_address(customer, addr_dict):
    address_type = Addresstype.objects.get(description='Shipping')
    return match_address(customer, addr_dict, address_type)


def match_billing_address(customer, addr_dict):
    address_type = Addresstype.objects.get(description='Billing')
    return match_address(customer, addr_dict, address_type)


def get_country(country_code):
    country = Country.objects.filter(alpha3code=country_code).first()
    return country


def get_state(state_code, country):
    state = State.objects.filter(code=state_code, countryfk=country).first()
    return state
