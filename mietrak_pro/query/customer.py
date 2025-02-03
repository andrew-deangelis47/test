from mietrak_pro.models import Party, Partydivision, Division, Term
from datetime import datetime
from mietrak_pro.utils import get_version_number, VERSION_2019


def get_customer(customer_code: int) -> Party:
    party = Party.objects.filter(partypk=customer_code).first()
    return party


def create_customer(name: str, division_pk: int = 1) -> Party:
    party = Party(
        customerorsuppliersincedate=datetime.now(),
        buyer=False,
        customer=True,
        salesperson=False,
        supplier=False,
        prospect=False,
        invoicetobeemailed=False,
        form1099tobemailed=False,
        certificationofperformancerequired=False,
        hardwareapprovedsupplierrequired=False,
        materialapprovedsupplierrequired=False,
        outsideprocessingapprovedsupplierrequired=False,
        ppapcustomer=False,
        requiressource=False,
        visitor=False,
        resale=False,
        isocertification=False,
        allowovershipping=False,
        metric=False,
        popupnotifycomment=False,
        name=name,
        priority=500,
        taxable=False,
        keepdocumentonfile=True,
    )
    if get_version_number() != VERSION_2019:
        party.donotallowovershippinghardstop = False

    party.save()

    division = Division.objects.get(divisionpk=division_pk)

    Partydivision.objects.create(
        partyfk=party,
        divisionfk=division,
    )

    return party


def get_or_create_terms(terms_description, net_due_days):
    term = Term.objects.filter(description=terms_description).first()
    if term is None:
        term = Term.objects.create(
            description=terms_description,
            duedays=net_due_days
        )
    return term
