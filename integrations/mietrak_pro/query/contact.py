from typing import Optional
from mietrak_pro.models import Party, Partydivision, Division, Partybuyer
from datetime import datetime
from mietrak_pro.utils import get_version_number, VERSION_2019


def create_contact(customer, contact_name, email, division_pk: int = 1):
    contact = Party(
        customerorsuppliersincedate=datetime.now(),
        buyer=True,
        customer=False,
        salesperson=False,
        supplier=False,
        prospect=False,
        certificationofperformancerequired=False,
        hardwareapprovedsupplierrequired=False,
        materialapprovedsupplierrequired=False,
        outsideprocessingapprovedsupplierrequired=False,
        requiressource=False,
        name=contact_name,
        email=email
    )
    if get_version_number() != VERSION_2019:
        contact.donotallowovershippinghardstop = False
    contact.save()

    division = Division.objects.get(divisionpk=division_pk)

    Partydivision.objects.create(
        partyfk=contact,
        divisionfk=division,
    )

    party_buyer = Partybuyer.objects.create(
        partyfk=customer,
        buyerfk=contact,
        description='',
        defaultbuyer=False,
    )

    return contact, party_buyer


def get_contact_by_email(email: str) -> Optional[Party]:
    """
    Searches MIE Trak Pro for contacts with the same email address.

    Returns the most recently updated one.
    :param email: str
    :return: Contacts
    """
    return Party.objects.filter(email__iexact=email) \
        .order_by('-partypk') \
        .first()


def get_contact_for_customer_by_email(customer: Party, email: str) -> Optional[Party]:
    """
    Searches MIE Trak Pro for contacts with the same email address belonging to a specific customer code.

    :param customer:
    :param email:
    :return:
    """
    party_buyers = Partybuyer.objects.filter(partyfk=customer)
    contact = None
    party_buyer_to_return = None
    for party_buyer in party_buyers:
        buyer = party_buyer.buyerfk
        if buyer.email == email:
            contact = buyer
            party_buyer_to_return = party_buyer
    return contact, party_buyer_to_return
