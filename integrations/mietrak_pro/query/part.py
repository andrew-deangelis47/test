from typing import Optional

from mietrak_pro.models import Item, Itemdivision, Iteminventory, Division, Itemtype, Calculationtype, Unitofmeasureset, \
    Pricetype, Iteminventorylocation, Location, Itemclass, Generalledgeraccount, Activitylogtype, ActivityLog
from django.db import transaction
from datetime import datetime
from django.db.models import Q
from mietrak_pro.utils import get_version_number, VERSION_2019


def create_item(part_number, revision, description, customer, is_itar, item_type,
                calculation_type, general_ledger_account, item_class: Optional[Itemclass], unit_of_measure_set,
                division_pk: int = 1, purchase_general_ledger_account=None, estimator=None, stocklength=0, stockwidth=0,
                thickness=0
                ) -> Item:
    with transaction.atomic():
        item_inventory = Iteminventory.objects.create(
            quantityonhand=0.,
            quantityreserved=0.,
            quantitydemand=0.,
            quantityworkinprocess=0.,
            quantitypull=0.,
            quantityordered=0.,
            standardcost=0.,
            lastcost=0.,
            averagecost=0.,
            otherexpenses=0.,
        )

        price_type = Pricetype.objects.filter(description='Base Price').first()

        is_manufactured_item = item_type.description == 'Standard'
        inventoriable = 1  # All items could potentially be inventory items, so set this to true by default

        item = Item(
            calculationtypefk=calculation_type,
            defaultrequestforquotepricetypefk=price_type,  # TODO - ask Chad about this
            generalledgeraccountfk=general_ledger_account,
            purchasegeneralledgeraccountfk=purchase_general_ledger_account,
            itemclassfk=item_class,
            iteminventoryfk=item_inventory,
            itemtypefk=item_type,
            partyfk=customer,  # TODO - should this be the vendor if it's a purchased component?
            unitofmeasuresetfk=unit_of_measure_set,
            expectreleasedays=0 if is_manufactured_item else None,
            # TODO - this appears to be 0 for manufactured components and NULL otherwise
            projecteddays=0,
            productdays=0 if is_manufactured_item else None,
            # TODO - this appears to be 0 for manufactured components and NULL otherwise
            allownegativeinventory=0,
            backflush=0,
            donotprintwithwo=0,
            forecastonmrp=0,
            graindirection=0,
            inventoriable=inventoriable,
            isintegrateitem=0,
            makefromitem=0,
            maketostock=0,
            manufactureditem=is_manufactured_item,
            metric=0,
            mpsitem=0,
            mpsonmrp=0,
            newrevisedflag=0,
            nonnestable=0,
            nonrohscompliant=0,
            reach=0,
            onecnhold=0,
            onhold=0,
            ondockinspectionrequired=0,
            popupnotify=0,
            pull=0,
            purchase=0,
            purchasetojob=0,
            qcholdppap=0,
            quoteitem=0,
            serialnumbertracking=0,
            serviceitem=0,
            taxable=0,
            stockinventory=0,
            certificationsrequiredbysupplier=0,
            poautocreatelotnumber=0,
            woautocreatelotnumber=0,
            vendorunit=1.,
            revision=revision,
            partnumber=part_number,
            vendorpartnumber=None,  # TODO - should this be set for purchased components?
            description=description,
            enablesyncing=0,
            itar=is_itar,
            cannotinvoice=0,
            stocklength=stocklength,
            stockwidth=stockwidth,
            thickness=thickness
        )
        if get_version_number() != VERSION_2019:
            item.approveditemsupplieronly = 0
            item.isdefault = 0
            item.phantomitem = 0
            item.shiploose = 0
            item.bulkship = 0
            item.remnant = 0
            item.cannotcreateworkorder = 0
        item.save()

        division = Division.objects.get(divisionpk=division_pk)

        Itemdivision.objects.create(
            itemfk=item,
            divisionfk=division,
            kanban=0,
        )

        location = Location.objects.first()

        iteminventorylocation = Iteminventorylocation(
            itemfk=item,
            locationfk=location,
            divisionfk=division,
            batchnumber='',
            container='',
            lotnumber='',
            revision='',
            comment='',
            quantity=0.,
            quantityreserved=0.,
            createdate=datetime.now(),
            lasttransactiondate=datetime.now(),
            defaultlocation=1,
            defaultdivisionlocation=1,
            donotdelete=0
        )
        if get_version_number() != VERSION_2019:
            iteminventorylocation.remnant = 0
        iteminventorylocation.save()

        log_type = Activitylogtype.objects.get(activitylogtypepk=11)

        activitylog = ActivityLog(
            itemfk=item,
            datestamp=datetime.now(),
            comment=f'Paperless created item  - {estimator.email if estimator else ""}',
            activitylogtypefk=log_type
        )
        activitylog.save()

        return item


def get_item(part_number, revision):
    item_instance = Item.objects.filter(partnumber=part_number, revision=revision, isdefault=True).first()
    if item_instance is not None:
        return item_instance
    if revision:
        return Item.objects.filter(partnumber=part_number, revision=revision).first()
    else:
        item_instance = Item.objects.filter(partnumber=part_number, isdefault=True).filter(Q(revision="") | Q(revision=None)).first()
        if item_instance is not None:
            return item_instance
        return Item.objects.filter(partnumber=part_number).filter(Q(revision="") | Q(revision=None)).first()


def get_item_type(component_type, is_raw_material, is_outside_process):
    if is_raw_material:
        return Itemtype.objects.filter(description='Material').first()
    elif is_outside_process:
        return Itemtype.objects.filter(description='Outside Process').first()
    elif component_type == 'assembled':
        return Itemtype.objects.filter(description='Standard').first()
    elif component_type == 'manufactured':
        return Itemtype.objects.filter(description='Standard').first()
    elif component_type == 'purchased':
        return Itemtype.objects.filter(description='Hardware/Supplies').first()
    else:
        return None


def get_calculation_type(item_type):
    if item_type.description == 'Material':
        return Calculationtype.objects.filter(itemtypefk=item_type, description='Single Part Price').first()
    elif item_type.description == 'Standard':
        return Calculationtype.objects.filter(itemtypefk=item_type, description='Piece Price').first()
    elif item_type.description == 'Hardware/Supplies':
        return Calculationtype.objects.filter(itemtypefk=item_type, description='Piece Price').first()
    else:
        return None


def get_unit_of_measure_set(unit_of_measure_code):
    return Unitofmeasureset.objects.filter(code=unit_of_measure_code).first()


def get_general_ledger_account_from_num(account_num):
    return Generalledgeraccount.objects.filter(accountnumber=account_num).first()
