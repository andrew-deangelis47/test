from typing import Optional

from mietrak_pro.models import Requestforquote, Requestforquotestatus, Requestforquoteline, \
    Requestforquotelinequantity, Division, Party, Item, Pricetype, Unitofmeasureset, User
from datetime import datetime
from mietrak_pro.utils import get_version_number, VERSION_2019


def create_request_for_quote(customer: Party, assigned_estimator: Optional[User], fob: str,
                             delivery: str, division_pk: int = 1):

    division = Division.objects.get(divisionpk=division_pk)

    rfq_status = Requestforquotestatus.objects.filter(description='Submitted').first()

    today = datetime.now().replace(microsecond=0, second=0, minute=0, hour=0)
    rfq = Requestforquote.objects.create(
        customerfk=customer,
        assignedestimatorfk=assigned_estimator,
        divisionfk=division,
        requestforquotestatusfk=rfq_status,
        daysvalid=3,  # TODO - is this correct?
        createdate=today,
        duedate=today,  # TODO - is this correct?
        inquirydate=today,
        delivery=delivery,
        freightonboard=fob,
        prepaidorcollection='',
        freightamount=0.,
        totalcost=0.,
        totalamount=0.,
        totaltax=0.,
        totalcommission=0.,
        totalweight=0.,
        totalextendedamount=0.,
        taxrate=0.,
        receivedpurchaseorder=0,
        nobid=0,
        didnotget=0,
        mieexchange=0,
        salestaxonfreight=0,
        printed=0,
        emailed=0
    )
    if get_version_number() != VERSION_2019:
        rfq.userdefinedbit1 = 0
        rfq.userdefinedbit2 = 0
        rfq.userdefinedbit3 = 0
        rfq.userdefinedbit4 = 0
        rfq.userdefinedbit5 = 0
        rfq.userdefinedbit6 = 0
        rfq.userdefinedbit7 = 0
        rfq.userdefinedbit8 = 0
        rfq.userdefinedbit9 = 0
        rfq.userdefinedbit10 = 0
        rfq.userdefinedbit11 = 0
        rfq.userdefinedbit12 = 0

    rfq.requestforquotenumber = rfq.requestforquotepk
    rfq.save()
    return rfq


def create_request_for_quote_line(rfq_line_reference_number: int,
                                  quantity: float,
                                  request_for_quote: Requestforquote,
                                  item: Item,
                                  assigned_estimator: Optional[User]):

    price_type = Pricetype.objects.filter(description='Base Price').first()
    unit_of_measure_set = Unitofmeasureset.objects.filter(code='EACH').first()

    rfq_line = Requestforquoteline.objects.create(
        assignedestimatorfk=assigned_estimator,
        itemfk=item,
        pricetypefk=price_type,
        requestforquotefk=request_for_quote,
        unitofmeasuresetfk=unit_of_measure_set,
        linereferencenumber=rfq_line_reference_number,
        quoterequired=0,
        quotecompleted=0,
        quoteapproved=0,
        didnotget=0,
        capture=0,
        requote=0,
        kitprice=0.,
        taxable=0,
        commissionable=1,
        discount=0,
        nobid=0,
        lastdateupdated=datetime.now(),
        partnumberrevision=item.revision,
        quantity=quantity,  # This should match the quantity from the first Requestforquotelinequantity record
        markuppercentage=0.,
        cost=0.,
        price=0.,
        msrp=0.,
        surcharge=0.,
        extendedprice=0.,
        estimatedhours=0.,
        setuptime=0.,
        setuplaborcost=0.,
        setupequipmentcharge=0.,
        miscellaneousprice=0.,
        standardprice=0.,
        miscellaneouscost=0.,
        standardcost=0.,
        kitcost=0.,
        setupcost=0.,
        setupprice=0.,
        runtime=0.,
        runlaborcost=0.,
        runequipmentcharge=0.,
        runcost=0.,
        runprice=0.,
        materialunitcost=0.,
        materialunitprice=0.,
        hardwareunitcost=0.,
        hardwareunitprice=0.,
        outsideprocessingunitcost=0.,
        outsideprocessingunitprice=0.,
        toolingcharge=0.,
        vendorunit=1.,
        foreignprice=0.,
    )
    return rfq_line


def create_request_for_quote_line_quantity(rfq_line: Requestforquoteline,
                                           quantity: float,
                                           unit_price: float,
                                           total_price: float,
                                           is_first_quantity: bool):
    price_type = Pricetype.objects.filter(description='Base Price').first()

    rfq_line_quantity = Requestforquotelinequantity.objects.create(
        requestforquotelinefk=rfq_line,
        pricetypefk=price_type,
        quantity=quantity,
        cutquantity=0.,
        delivery=1.,  # TODO - what is this? It must be > 0, and is entered in the UI along with the quantity
        cost=None,
        price=unit_price,
        surcharge=0.,
        extendedprice=total_price,
        primaryprice=is_first_quantity,
        vendorunit=1.,
    )
    return rfq_line_quantity
