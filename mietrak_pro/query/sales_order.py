from typing import Optional

from mietrak_pro.models import Salesorder, Salesorderstatus, Salesorderline, Salesorderlinelot, \
    Salesorderlinelotstatus, Salesorderlineitemtype, Division, Party, Item, Router, Address, Generalledgeraccount, \
    ActivityLog, Activitylogtype
from datetime import datetime

from mietrak_pro.utils import get_version_number, VERSION_2020, VERSION_2019


def create_sales_order(customer: Party,
                       contact: Party,
                       billing_address: Optional[Address],
                       shipping_address: Optional[Address],
                       po_number: str,
                       fob: str,
                       private_notes: str,
                       request_for_quote_number: Optional[str],
                       division_pk: int = 1, estimator=None, quote_num_rev=None, pp_quote_reference_field=None):
    division = Division.objects.get(divisionpk=division_pk)
    sales_order_status = Salesorderstatus.objects.get(description='Open')

    sales_order = Salesorder(
        buyerfk=contact,
        billingaddressfk=billing_address,
        customerfk=customer,
        divisionfk=division,
        shippingaddressfk=shipping_address,
        shipviafk=customer.shipviafk,
        freightcodefk=customer.freightcodefk,
        salesorderstatusfk=sales_order_status,
        termfk=customer.termfk,
        changeno=0,  # This gets incremented by a trigger any time the sales order or associated table is modified
        expediternumber=0,
        chargefreight=0,
        codprepayedflag=0,
        ediorder=0,
        mieexchangeorder=0,
        receivedpurchaseorder=0,
        rma=0,
        popupnotifycomment=0,
        holdshipmentforpayment=0,
        shipcompleteonly=0,
        emailed=0,
        createdate=datetime.today(),
        prepaidorcollection='',
        purchaseordernumber=po_number,
        requestforquotenumber=request_for_quote_number,
        userdefinedpo='',
        freightonboard=fob,
        depositamount=0.,
        depositamountapplied=0.,
        discountpercentage=0.,
        freightcharge=0.,
        shippingnotes='',
        manufacturingnotes='',
        notifycomment=private_notes,
        billingaddressname=billing_address.name if billing_address is not None else None,
        billingaddress1=billing_address.address1 if billing_address is not None else None,
        billingaddress2=billing_address.address2 if billing_address is not None else None,
        billingaddressalt=billing_address.addressalt if billing_address is not None else None,
        billingaddresscity=billing_address.city if billing_address is not None else None,
        billingaddresszipcode=billing_address.zipcode if billing_address is not None else None,
        billingaddressstatedescription=find_description(
            billing_address.statefk) if billing_address is not None else None,
        billingaddresscountrydescription=find_description(
            billing_address.countryfk) if billing_address is not None else None,
        shippingaddressname=shipping_address.name if shipping_address is not None else None,
        shippingaddress1=shipping_address.address1 if shipping_address is not None else None,
        shippingaddress2=shipping_address.address2 if shipping_address is not None else None,
        shippingaddressalt=shipping_address.addressalt if shipping_address is not None else None,
        shippingaddresscity=shipping_address.city if shipping_address is not None else None,
        shippingaddresszipcode=shipping_address.zipcode if shipping_address is not None else None,
        shippingaddressstatedescription=find_description(
            shipping_address.statefk) if shipping_address is not None else None,
        shippingaddresscountrydescription=find_description(
            shipping_address.countryfk) if shipping_address is not None else None,
        edi855exported=0,
        taxamount=0.
    )
    if get_version_number() != VERSION_2020:
        sales_order.userdefinedbit1 = 0
        sales_order.userdefinedbit2 = 0
        sales_order.userdefinedbit3 = 0

    if pp_quote_reference_field:
        setattr(sales_order, pp_quote_reference_field, quote_num_rev)
    sales_order.save()
    sales_order.salesordernumber = sales_order.salesorderpk
    sales_order.save()

    log_type = Activitylogtype.objects.get(activitylogtypepk=7)

    activitylog = ActivityLog(
        salesorderfk=sales_order,
        datestamp=datetime.now(),
        comment=f'https://app.paperlessparts.com/quotes/edit/{quote_num_rev}',
        activitylogtypefk=log_type
    )
    activitylog.save()

    return sales_order


def find_description(obj):
    if hasattr(obj, 'description'):
        return obj.description
    return None


def create_sales_order_line(sales_order: Salesorder,
                            sales_order_line_reference_number: int,
                            unit_price: float,
                            quantity: float,
                            customer: Party,
                            gl_account: Optional[Generalledgeraccount],
                            item: Item,
                            router: Optional[Router],
                            shipping_address: Optional[Address],
                            is_item_new: bool,
                            due_date: datetime, private_notes: str = None):
    sales_order_line_status = Salesorderstatus.objects.get(description='Open')
    sales_order_line_item_type = Salesorderlineitemtype.objects.get(description='Standard Item')

    router_id = router.routerpk if router is not None else None
    extended_price = unit_price * quantity

    sales_order_line = Salesorderline(
        customerfk=customer,
        firstarticlefk=customer.firstarticlefk,
        generalledgerfk=gl_account,
        hardwarecertificationfk=customer.hardwarecertificationfk,
        itemfk=item,
        materialcertificationfk=customer.materialcertificationfk,
        outsideprocessingcertificationfk=customer.outsideprocessingcertificationfk,
        salesorderfk=sales_order,
        salesorderlineitemtypefk=sales_order_line_item_type,
        salesorderlinestatusfk=sales_order_line_status,
        shippingaddressfk=shipping_address,
        shipviafk=customer.shipviafk,
        unitofmeasuresetfk=item.unitofmeasuresetfk,
        expeditor=0,
        linereferencenumber=sales_order_line_reference_number,
        priority=customer.priority,
        blanketorderflag=0,
        certificationofperformancerequired=customer.certificationofperformancerequired,
        certificationsrequired=0,
        exploded=0,
        firstarticlerequired=item.firstarticlerequired,
        hardwareapprovedsupplierrequired=customer.hardwareapprovedsupplierrequired,
        lotprice=0,
        materialapprovedsupplierrequired=customer.materialapprovedsupplierrequired,
        neworderflag=is_item_new,  # TODO - Chad is looking into whether we need to bother with this
        newrevision=0,  # TODO - Chad is looking into whether we need to bother with this
        noncommissionable=item.noncommissionable,
        noninventoriablecharge=0,
        outsideprocessingapprovedsupplierrequired=customer.outsideprocessingapprovedsupplierrequired,
        purchaseorderreceivedflag=0,
        requiressource=customer.requiressource,
        readytoshipflag=0,
        shiponeveryshipmentoneitemflag=0,
        shiponfirstsalesordershipmentonly=0,
        taxable=0,
        resale=0,
        timeandmaterialjob=0,
        userdefinedflag=0,
        fair=0,
        popupnotifycomment=0,
        shipcompleteonly=0,
        partnumber=item.partnumber,
        revision=item.revision,
        vendorunit=item.vendorunit,
        cost=None,  # TODO - verify we don't need to populate this
        markuppercentage=None,
        msrp=None,
        price=unit_price,
        extendedamount=extended_price,
        openamount=extended_price,
        quantityordered=quantity,
        quantityshipped=0.,
        releasedquantity=0.,
        shippedamount=0.,
        createdate=datetime.today(),
        shippingaddressname=shipping_address.name if shipping_address is not None else None,
        shippingaddress1=shipping_address.address1 if shipping_address is not None else None,
        shippingaddress2=shipping_address.address2 if shipping_address is not None else None,
        shippingaddressalt=shipping_address.addressalt if shipping_address is not None else None,
        shippingaddresscity=shipping_address.city if shipping_address is not None else None,
        shippingaddresszipcode=shipping_address.zipcode if shipping_address is not None else None,
        shippingaddressstatedescription=find_description(
            shipping_address.statefk) if shipping_address is not None else None,
        shippingaddresscountrydescription=find_description(
            shipping_address.countryfk) if shipping_address is not None else None,
        nextduedate=None,  # TODO - may not need to be set, this comes from the Salesorderlinelot
        nextpromisedate=None,  # TODO - may not need to be set, this comes from the Salesorderlinelot
        notes=None,  # TODO - should this be set?
        manufacturingnotes=private_notes,  # TODO - should this be set?
    )
    if get_version_number() != VERSION_2019:
        sales_order_line.routerfk = router_id

    # TODO - verify that the created date gets set automatically upon insertion
    sales_order_line.jobnumber = sales_order_line.salesorderlinepk
    sales_order_line.save()

    # Since Paperless Parts does not have a concept of releases, create a single sales order line lot with
    # the full quantity
    sales_order_line_lot_status = Salesorderlinelotstatus.objects.get(description='Firm')

    # Make sure the due date is no more specific than the day
    due_date = due_date.replace(microsecond=0, second=0, minute=0, hour=0)

    sales_order_line_lot = Salesorderlinelot.objects.create(
        salesorderlinefk=sales_order_line,
        salesorderlinelotstatusfk=sales_order_line_lot_status,
        userdefined='',
        datestamp=datetime.today(),
        originalduedate=due_date,
        expectedreleasedate=None,  # TODO - what to do here?
        purchaseordernumber='',
        quantitydue=quantity,
        quantityshipped=0.,
        originalquantity=quantity,
        quantitytofabricate=quantity,  # TODO - is this right?
        quantitytopull=0.,
        plannedflag=0,
        progresspayment=0,
        cancelled=0,
    )
    return sales_order_line, sales_order_line_lot
