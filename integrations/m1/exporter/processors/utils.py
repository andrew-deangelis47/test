from baseintegration.datamigration import logger
from paperless.objects.orders import OrderComponent, OrderItem
from m1.models import Salesorders, Salesorderlines, Salesorderdeliveries
from m1.models import Parts, Partrevisions
from decimal import Decimal
from datetime import datetime


class PartUtils:

    MANUFACTURED = '2'
    PURCHASED = '1'

    @staticmethod
    def get_create_component_part(component: OrderComponent, long_description: str = '') -> [Parts, Partrevisions]:
        number = component.part_number
        split = component.part_name.rsplit('.', 1)
        name = split[0]
        if number is None:
            number = name
            logger.info(f'M1Exporter: part number was empty for component {component.id}. Falling back to'
                        f'part name {component.part_name}')

        parts = Parts.objects.filter(imppartid=number)
        part: Parts = None

        if len(parts) > 0:
            part = parts[0]

        if not isinstance(part, Parts):
            part_type = PartUtils.MANUFACTURED
            if component.type == "purchased":
                part_type = PartUtils.PURCHASED
            short_description = component.description if component.description else name
            part = PartUtils.create_part(part_number=number, short_description=short_description,
                                         long_description=long_description, part_type=part_type)
            rev = PartUtils.create_part_rev(rev=component.revision if component.revision else '',
                                            part=part)
        else:
            revs: [Partrevisions] = Partrevisions.objects.filter(imrpartid=number,
                                                                 imrpartrevisionid=component.revision)
            rev: Partrevisions = None
            item: Partrevisions
            for item in revs:
                if item.imrpartrevisionid == component.revision:
                    rev = item
            if not isinstance(rev, Partrevisions):
                rev = PartUtils.create_part_rev(rev=component.revision if component.revision else '',
                                                part=part)
        return part, rev

    @staticmethod
    def get_create_placeholder_parts(part_number: str, short_description: str = '',
                                     long_description: str = '') -> [Parts, Partrevisions]:

        parts = Parts.objects.filter(imppartid=part_number)
        part: Parts = None
        rev: Partrevisions = None

        if len(parts) > 0:
            part = parts[0]
            revs: [Partrevisions] = Partrevisions.objects.filter(imrpartid=part_number, imrpartrevisionid='')
            rev = revs[0]

        if not isinstance(part, Parts):
            part = PartUtils.create_part(part_number=part_number, short_description=short_description,
                                         long_description=long_description)
            rev = PartUtils.create_part_rev(rev='', part=part)
        return part, rev

    @staticmethod
    def create_part(part_number: str, short_description: str, long_description: str = '',
                    part_type: str = MANUFACTURED) -> Parts:
        return Parts.objects.create(imppartid=part_number,
                                    impparttype=part_type,
                                    impreordermethod='1',
                                    impshortdescription=short_description,
                                    implongdescriptionrtf=long_description,
                                    implongdescriptiontext=long_description,
                                    impnonstockeditem=False,
                                    impwebsellabletoall=False,
                                    impalwaysnontaxable=False,
                                    imptrackserialnumbers=False,
                                    imptracklotnumbers=False,
                                    impnonphysicalshipment=False,
                                    impphantomorkitpart=False,
                                    impbuyforinventory=False,
                                    impinactive=False,
                                    impcreatedby='ppadmin',
                                    impcontractlength=0,
                                    impdeliverytype=0
                                    )

    @staticmethod
    def create_part_rev(rev: str, part: Parts) -> Partrevisions:
        return Partrevisions.objects.create(imrpartid=part.imppartid,
                                            imrpartrevisionid=rev,
                                            imrconversionfactor='1',  # 1 for EA
                                            imrshortdescription=part.impshortdescription,
                                            imrwebsuppresswhensold=False,
                                            imrquantityonhand=0.00,
                                            imrquantityallocated=0.00,
                                            imrquantitytoinspect=0.00,
                                            imrquantitytoreturn=0.00,
                                            imrminimumquantity=0.00,
                                            imrmaximumquantity=0.00,
                                            imrmanufacturinglotsize=0.00,
                                            imraveragelaborcost=0.00,
                                            imraverageoverheadcost=0.00,
                                            imraveragematerialcost=0.00,
                                            imraveragesubcontractcost=0.00,
                                            imrlastlaborcost=0.00,
                                            imrlastoverheadcost=0.00,
                                            imrlastmaterialcost=0.00,
                                            imrlastsubcontractcost=0.00,
                                            imrstandardlaborcost=0.00,
                                            imrstandardoverheadcost=0.00,
                                            imrstandardmaterialcost=0.00,
                                            imrstandardsubcontractcost=0.00,
                                            imrleadtime=0.00,
                                            imrconfigured=False,
                                            imrusequoteprice=False,
                                            imrpreferredrefexists=False,
                                            imrinactive=False,
                                            imrsheetsizex=0.00,
                                            imrsheetsizey=0.00,
                                            imrbarlength=0.00,
                                            imrweight=0.00,
                                            imrfdxpackaging=0.00,
                                            imrfdxhandlingcost=0.00,
                                            imrfdxpackagingcost=0.00,
                                            imrfdxshipcostmarkuppct=0.00,
                                            imrfdxoneitempershipment=False,
                                            imrfdxnonstandardcontainer=False,
                                            imrquantityonordersales=0.00,
                                            imrquantityonorderpurchases=0.00,
                                            imrwebshowtopartorgref=False,
                                            imrpurchasableitem=False,
                                            imrwebsellabletoall=False,
                                            imraveragedutycost=0.00,
                                            imraveragefreightcost=0.00,
                                            imraveragemisccost=0.00,
                                            imrlastdutycost=0.00,
                                            imrlastfreightcost=0.00,
                                            imrlastmisccost=0.00,
                                            imrstandarddutycost=0.00,
                                            imrstandardfreightcost=0.00,
                                            imrstandardmisccost=0.00,
                                            imrvolume=0.00,
                                            imrexpensesplitpercenttotal=0.00,
                                            imrwebconfigmode=False,
                                            imrsuppressshortdescription=False,
                                            imrwebconfigpricerule=False,
                                            imrfdxpackagelength=0,
                                            imrfdxpackagewidth=0,
                                            imrfdxpackageheight=0,
                                            imrproductcategorylineid=0,
                                            imrrequiresinspection=0,
                                            imrquantitytoreturnjob=0.00
                                            )


class SalesOrderUtils:
    @staticmethod
    def create_line_item(idx: int, new_sales_order: Salesorders, part: Parts, rev: Partrevisions,
                         unit_cost: Decimal, qty: int) -> Salesorderlines:
        full_cost = float(qty) * float(unit_cost)
        new_sales_order_line = Salesorderlines.objects.create(omlsalesorderid=new_sales_order.ompsalesorderid,
                                                              omlsalesorderlineid=idx,
                                                              omlorderquantity=qty,
                                                              omlfullunitpricebase=unit_cost,
                                                              omlunitpricebase=unit_cost,
                                                              omlpartid=part.imppartid,
                                                              omlorgpartid=part.imppartgroupid,
                                                              omlpartshortdescription=part.impshortdescription,
                                                              omlpartlongdescriptionrtf=part.implongdescriptionrtf,
                                                              omlpartlongdescriptiontext=part.implongdescriptiontext,
                                                              omlpartrevisionid=rev.imrpartrevisionid,
                                                              omlfullunitpriceforeign=unit_cost,
                                                              omldiscountpercent=0.00,
                                                              omlunitdiscountbase=0.0000,
                                                              omlunitdiscountforeign=0.0000,
                                                              omlunitpriceforeign=unit_cost,
                                                              omlfullextendedpricebase=full_cost,
                                                              omlfullextendedpriceforeign=full_cost,
                                                              omlextendeddiscountbase=0.0000,
                                                              omlextendeddiscountforeign=0.0000,
                                                              omlextendedpricebase=full_cost,
                                                              omlextendedpriceforeign=full_cost,
                                                              omlfreightamountbase=0.0000,
                                                              omlfreightamountforeign=0.0000,
                                                              omltaxamountbase=0.0000,
                                                              omltaxamountforeign=0.0000,
                                                              omlsecondtaxamountbase=0.0000,
                                                              omlsecondtaxamountforeign=0.0000,
                                                              omlpaycommission=True,
                                                              omltimeandmaterial=False,
                                                              omlquantityshipped=0.0000,
                                                              omlquotelineid=0,
                                                              omlquotequantityid=0,
                                                              omlleadlineid=0,
                                                              omlrmaclaimlineid=0,
                                                              omlconfigured=False,
                                                              omlweight=0.0000,
                                                              omlpostransactionlineid=0,
                                                              omlclosed=False,
                                                              omlpriceoverride=False,
                                                              omldeposit=False,
                                                              omldepositpercent=0.00,
                                                              omldepositamountbase=0.0000,
                                                              omldepositamountforeign=0.0000,
                                                              omldepositcreated=False,
                                                              omldepositcredited=False,
                                                              omlavalaraignoreline=False,
                                                              omlcreatedby='ppadmin',
                                                              omlextendedweight=0.0000,
                                                              omldeliveryquantitytotal=qty,
                                                              omlunitofmeasure='EA'
                                                              )
        return new_sales_order_line

    @staticmethod
    def create_delivery(idx: int, new_sales_order: Salesorders, part: Parts, rev: Partrevisions, qty: int,
                        delivery_date: datetime) -> Salesorderdeliveries:
        new_sales_delivery = Salesorderdeliveries.objects.create(omdsalesorderid=new_sales_order.ompsalesorderid,
                                                                 omdsalesorderlineid=idx,
                                                                 omdsalesorderdeliveryid=1,
                                                                 omdpartid=part.imppartid,
                                                                 omdpartrevisionid=rev.imrpartrevisionid,
                                                                 omdpartwarehouselocationid='MAIN',
                                                                 omdpartbinid='NONE',
                                                                 omddeliveryquantity=qty,
                                                                 omddeliverydate=delivery_date,
                                                                 omddeliverytype=1,
                                                                 omdfirm=True,
                                                                 omdamounttoinvoice=0.0000,
                                                                 omdamounttoinvoiceforeign=0.0000,
                                                                 omddifferentlocation=False,
                                                                 omdfreightamountbase=0.0000,
                                                                 omdfreightamountforeign=0.0000,
                                                                 omdquantityshipped=0.0000,
                                                                 omdquantityinvoiced=0.0000,
                                                                 omdshippedcomplete=False,
                                                                 omdinvoicedcomplete=False,
                                                                 omdclosed=False,
                                                                 omdrequiresinspection=False,
                                                                 omdpurchaseunitcostbase=0.0000,
                                                                 omdpickinprogress=False,
                                                                 omdpurchaseunitcostforeign=0.0000,
                                                                 omdquantityreceived=0.0000,
                                                                 omdreceivedcomplete=False,
                                                                 omdcreatedby='ppadmin',
                                                                 omdkitpart=False,
                                                                 omdquantityallocated=0.0000,
                                                                 omdquantityonorder=qty,
                                                                 omdweight=0.0000,
                                                                 omdextendedweight=0.0000
                                                                 )
        return new_sales_delivery


class NoteUtils:
    @staticmethod
    def get_line_item_notes(item: OrderItem):
        line_item_notes = ''
        if item.public_notes is not None and item.public_notes != '':
            line_item_notes += f'{item.public_notes}'
        if item.private_notes is not None and item.private_notes != '':
            if line_item_notes != '':
                line_item_notes += '\r\n'
            line_item_notes += f'{item.private_notes}'
        return line_item_notes
