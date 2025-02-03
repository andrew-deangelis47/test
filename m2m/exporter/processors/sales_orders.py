import datetime

from paperless.objects.orders import Order, OrderItem

import m2m.models as mm
from baseintegration.datamigration import logger
from m2m.configuration import M2MConfiguration
from m2m.utils.address import AddressHelper
from m2m.utils.item_master import ItemMasterHelper

DEFAULT_DATE = datetime.datetime(1900, 1, 1, 0, 0, 0)


class SalesOrderFactory:
    m2m_config = M2MConfiguration()

    def __init__(self, configuration: M2MConfiguration):
        self.m2m_config = configuration

    def create_sales_order(self, order: Order, expedite_part_number: str = None) -> mm.Somast:

        notes_str = 'Paperless Parts Quote #{}\r\n' \
                    'https://app.paperlessparts.com/quotes/edit/{}\r\n' \
                    'Paperless Parts Order #{}\r\n' \
                    'https://app.paperlessparts.com/orders/edit/{}\r\n\r\n'.format(order.quote_number,
                                                                                   order.quote_number,
                                                                                   order.number,
                                                                                   order.number)
        erp_code = order.contact.account.erp_code if order.contact.account and order.contact.account.erp_code \
            else self.m2m_config.default_erp_code
        company: mm.Slcdpmx = mm.Slcdpmx.objects.filter(fcustno=erp_code).first()
        if company is None:
            raise ValueError(f'Could not find a company record for the Paperless Parts account erp code for order '
                             f'{order.number}, Bailing...')
        created_by = 'PP'
        by_po = '3'
        payment_terms = self.get_payment_term_code(order.payment_details.payment_terms, company)
        estimator = ''
        if order.estimator:
            estimator = f'{order.estimator.first_name[0]}{order.estimator.last_name[0]}'

        order_date = order.created_dt.date()
        due_date = order.ships_on_dt.date()

        default_sold_to: mm.Syaddr = mm.Syaddr.objects.filter(fcaliaskey=company.fcustno, fcaddrtype='O').first()

        shipping_info_addr = self.get_create_shipping_address(order=order, company=company)

        po_number = f'PP-{order.number}-no-po'
        if order.payment_details.purchase_order_number:
            po_number = order.payment_details.purchase_order_number

        so_master: mm.Somast = mm.Somast(fcustno=company.fcustno,
                                         fcompany=company.fcompany,
                                         fcity=company.fcity,
                                         fcustpono=po_number,
                                         fackdate=DEFAULT_DATE,
                                         fcanc_dt=DEFAULT_DATE,
                                         fccurid='USD',
                                         fcfactor=1.0000,
                                         fcfname=order.contact.first_name,
                                         fcfromno="",
                                         fcfromtype="",
                                         fcontact=order.contact.last_name,
                                         fclos_dt=DEFAULT_DATE,
                                         fcountry=company.fcountry,
                                         fcusrchr1="",
                                         fcusrchr2="",
                                         fcusrchr3="",
                                         fdcurdate=DEFAULT_DATE,
                                         fdisrate=0.000,
                                         fdistno="",
                                         fduedate=due_date,
                                         fduplicate=False,
                                         fdusrdate1=DEFAULT_DATE,
                                         festimator=estimator,
                                         ffax='',
                                         ffob=company.ffob,
                                         fnextenum="001",
                                         fnextinum="  1",
                                         fnusrqty1=0.00000,
                                         fnusrcur1=0.00000,
                                         forderdate=order_date,
                                         fordername="",
                                         fordrevdt=DEFAULT_DATE,
                                         fpaytype=by_po,
                                         fphone=company.fphone,
                                         fprint_dt=DEFAULT_DATE,
                                         fprinted=False,
                                         fsalcompct=0.000,
                                         fsalecom=False,
                                         fshipvia=company.fshipvia,
                                         fshptoaddr=shipping_info_addr.fcaddrkey,
                                         fsocoord=created_by,
                                         fsoldaddr=default_sold_to.fcaddrkey,
                                         fsoldby=company.fsalespn,
                                         fsorev="00",
                                         fstate=company.fstate,
                                         fstatus="Started",
                                         ftaxcode="",
                                         ftaxrate=0.000,
                                         fterm=payment_terms,
                                         fterr=company.fterr,
                                         fzip=company.fzip,
                                         flprofprtd=False,
                                         flprofrqd=False,
                                         fndpstrcvd=0.00000,
                                         fndpstrqd=0.00000,
                                         fdeurodate=DEFAULT_DATE,
                                         feurofctr=0.00000,
                                         fsalescode="       ",
                                         fusercode=company.fusercode,
                                         fncancchrge=0.00000,
                                         flchgpnd=False,
                                         fllasteco="",
                                         fackmemo="",
                                         fmstreet=company.fmstreet,
                                         fmusrmemo1=notes_str,
                                         fndbrmod=0,
                                         fccontkey="",
                                         flcontract=False,
                                         fccommcode="0",
                                         fpriority=4,
                                         contractnu="",
                                         fbilladdr="",
                                         opportunnum="",
                                         oppcrtype="",
                                         quotenumber="",
                                         contactnum="",
                                         flpaybycc=False
                                         )
        so_master.save_with_autonumber()
        logger.info(f'Created SO {so_master.fsono} for order {order.number}')
        self.create_sales_order_items(order, so_master, company, shipping_info_addr, expedite_part_number)
        return so_master

    def get_create_shipping_address(self, order: Order, company: mm.Slcdpmx):

        default_shipping: mm.Syaddr = mm.Syaddr.objects.filter(fcaliaskey=company.fcustno, fcaddrtype='S').first()
        shipping_info_addr = default_shipping

        if order.shipping_info:
            if order.shipping_info.facility_name and order.shipping_info.facility_name != '':
                slices = order.shipping_info.facility_name.split('-')
                if len(slices) == 3:
                    shipping_addr: mm.Syaddr = mm.Syaddr.objects.filter(fcaliaskey=company.fcustno, fcaddrtype='S',
                                                                        fcaddrkey=slices[2]).first()
                    if shipping_addr and shipping_addr.fcaddrkey:
                        shipping_info_addr = shipping_addr
                    else:
                        shipping_info_addr: mm.Syaddr = AddressHelper.create_address(address_info=order.shipping_info,
                                                                                     company=company,
                                                                                     addr_type='S')
            else:
                shipping_info_addr: mm.Syaddr = AddressHelper.create_address(address_info=order.shipping_info,
                                                                             company=company,
                                                                             addr_type='S')

        return shipping_info_addr

    def create_sales_order_items(self, order: Order, so_master: mm.Somast, company: mm.Slcdpmx,
                                 default_shipping: mm.Syaddr, expedite_part_number: str = None):
        order_date = order.created_dt.date()
        due_date = order.ships_on_dt.date()
        idx = 1
        for item in order.order_items:
            item_master = ItemMasterHelper.get_item_record(item.root_component)
            self.create_sales_order_item(so_master=so_master, idx=idx, part_number=item_master.fpartno,
                                         rev=item_master.frev, measure=item_master.fmeasure, source=item_master.fsource,
                                         description=item_master.fdescript, memo=item_master.fstdmemo, company=company,
                                         fac=item_master.fac, sfac=item_master.sfac, cud_rev=item_master.fcudrev,
                                         production_class=item_master.fprodcl, due_date=due_date, order_date=order_date,
                                         quantity=item.quantity)
            self.create_sales_order_release_item(so_master=so_master, idx=idx, rev=item_master.frev,
                                                 part_number=item_master.fpartno, due_date=due_date,
                                                 quantity=item.quantity, total_price=item.total_price.raw_amount,
                                                 shipping_address_key=default_shipping.fcaddrkey, order_date=order_date,
                                                 location=item_master.flocate1, unit_price=item.unit_price.raw_amount)
            self.create_sales_order_bom_item(so_master=so_master, idx=idx, part_number=item_master.fpartno,
                                             rev=item_master.frev, measure=item_master.fmeasure, fac=item_master.fac,
                                             source=item_master.fsource, description=item_master.fdescript,
                                             memo=item_master.fstdmemo, quantity=item.quantity)
            idx += 1

            if item.ordered_add_ons:
                for add_on in item.ordered_add_ons:
                    notes = add_on.notes if add_on.notes else ''
                    split = add_on.name.split(' - ')
                    part_number = split[0]
                    item_master = mm.Inmastx.objects.filter(fpartno=part_number).first()
                    if item_master:
                        notes = f'{item_master.fdescript} : {notes}'
                    self.create_add_on_item(so_master=so_master, item=item, idx=idx, item_master=item_master,
                                            notes=notes, due_date=due_date, order_date=order_date, company=company,
                                            add_on_name=add_on.name, shipping_key=default_shipping.fcaddrkey,
                                            price=add_on.price.raw_amount)
                    idx += 1

            if expedite_part_number and item.expedite_revenue:
                notes = f'This is an expedite from Paperless Parts Order {order.number}'
                add_on_name = 'PP Expedite Revenue'
                item_master = mm.Inmastx.objects.filter(fpartno=expedite_part_number).first()
                if item_master:
                    notes = f'{item_master.fdescript} : {notes}'
                self.create_add_on_item(so_master=so_master, item=item, idx=idx, item_master=item_master, notes=notes,
                                        due_date=due_date, order_date=order_date, add_on_name=add_on_name, price=0.000,
                                        shipping_key=default_shipping.fcaddrkey, company=company)
                idx += 1
        so_master.fnextinum = idx
        so_master.fnextenum = str(idx).zfill(3)
        so_master.save()

    def create_add_on_item(self, add_on_name: str, so_master: mm.Somast, item: OrderItem, idx: int, notes: str,
                           shipping_key: str, due_date: datetime.date, order_date: datetime.date,
                           item_master: mm.Inmastx, company: mm.Slcdpmx, price: float):
        part_number = add_on_name
        rev = 'NS'
        measure = 'EA'
        description = notes
        memo = ''
        fac = ''
        sfac = ''
        cud_rev = 'NS'
        p_class = ''
        source = ''
        location = ''
        if item_master:
            part_number = item_master.fpartno
            rev = item_master.frev
            measure = item_master.fmeasure
            memo = item_master.fstdmemo
            fac = item_master.fac
            sfac = item_master.sfac
            cud_rev = item_master.fcudrev
            p_class = item_master.fprodcl
            source = item_master.fsource
            location = item_master.flocate1
        self.create_sales_order_item(so_master=so_master, idx=idx, cud_rev=cud_rev, quantity=1, rev=rev,
                                     measure=measure, source=source, part_number=part_number, description=description,
                                     memo=memo, fac=fac, sfac=sfac, company=company, production_class=p_class,
                                     due_date=due_date, order_date=order_date)
        self.create_sales_order_release_item(so_master=so_master, idx=idx, rev=rev, quantity=1,
                                             part_number=part_number, due_date=due_date, location=location,
                                             shipping_address_key=shipping_key, order_date=order_date,
                                             total_price=price, unit_price=price)
        self.create_sales_order_bom_item(so_master=so_master, idx=idx, part_number=part_number,
                                         rev=rev, measure=measure, fac=fac, source=source, memo=memo, quantity=1,
                                         description=description)

    def create_sales_order_item(self, so_master: mm.Somast, idx: int, company: mm.Slcdpmx,
                                part_number: str, rev: str, measure: str, source: str, description: str, memo: str,
                                fac: str, sfac: str, cud_rev: str, production_class: str, quantity: float,
                                due_date: datetime.date, order_date: datetime.date):
        mm.Soitem.objects.create(finumber=self.format_finumber(f"{idx}"),
                                 fpartno=part_number,
                                 fpartrev=rev,
                                 fsono=so_master.fsono,
                                 fclotext=" ",
                                 fllotreqd=False,
                                 fautocreat=False,
                                 fcas_bom=False,
                                 fcas_rtg=False,
                                 fcommpct=0.00,
                                 fcustpart="",
                                 fcustptrev="",
                                 fdet_bom=False,
                                 fdet_rtg=False,
                                 fduedate=due_date,
                                 fenumber=str(idx).zfill(3),
                                 ffixact=0.00000,
                                 fgroup=company.fcustno,
                                 flabact=0.00000,
                                 fmatlact=0.00000,
                                 fmeasure=measure,
                                 fmultiple=False,
                                 fnextinum=1,
                                 fnextrel='001',
                                 fnunder=0.00000,
                                 fnover=0.00000,
                                 fordertype="Fix",
                                 fothract=0.00000,
                                 fovhdact=0.00000,
                                 fprice=False,
                                 fprintmemo=False,
                                 fprodcl=production_class,
                                 fquantity=quantity,
                                 fcfromtype="",
                                 fcfromno="",
                                 fcfromitem="",
                                 fquoteqty=0.00000,
                                 frtgsetupa=0.00000,
                                 fschecode="",
                                 fshipitem=True,
                                 fsoldby=company.fsalespn,
                                 fsource=source,
                                 fstandpart=True,
                                 fsubact=0.00000,
                                 fsummary=False,
                                 ftaxcode="   ",
                                 ftaxrate=0.000,
                                 ftoolact=0.00000,
                                 ftnumoper=0,
                                 ftotnonpr=0,
                                 ftotptime=0.00000,
                                 ftotstime=0.00000,
                                 fulabcost1=0.00000,
                                 fviewprice=False,
                                 fcprodid="",
                                 fschedtype="",
                                 fdesc=description,
                                 fdescmemo=memo,
                                 fndbrmod=0,
                                 fac=fac,
                                 sfac=sfac,
                                 itccost=0.00000,
                                 fcaltum=measure,
                                 fnaltqty=quantity,
                                 fcudrev=cud_rev,
                                 fnlatefact=0.00,
                                 fnsobuf=0,
                                 manualplan=False,
                                 contractnu="",
                                 flrfqreqd=False,
                                 fcostfrom="",
                                 fcitemstatus="Started",
                                 fdrequestdate=order_date,
                                 fdcreateddate=order_date,
                                 forigreqdt=DEFAULT_DATE,
                                 ffinalschd=False)

    def create_sales_order_release_item(self, so_master: mm.Somast, idx: int, part_number: str, quantity: float,
                                        rev: str, shipping_address_key: str = '', due_date: datetime.date = None,
                                        order_date: datetime.date = None, location: str = '', total_price: float = 0.00,
                                        unit_price: float = 0.00):
        mm.Sorels.objects.create(fenumber=str(idx).zfill(3),
                                 finumber=self.format_finumber(f"{idx}"),
                                 fpartno=part_number,
                                 fpartrev=rev,
                                 frelease="000",
                                 fshptoaddr=shipping_address_key,
                                 fsono=so_master.fsono,
                                 favailship=True,
                                 fbook=0.00000,
                                 fbqty=0.00000,
                                 fdiscount=0.00000,
                                 fduedate=due_date,
                                 finvamount=0.00000,
                                 finvqty=0.00000,
                                 fjob=False,
                                 fjoqty=0.00000,
                                 flabcost=0.00000,
                                 flngth=0.00000,
                                 flshipdate=DEFAULT_DATE,
                                 fmasterrel=False,
                                 fmatlcost=0.00000,
                                 fmaxqty=0.00000,
                                 fmqty=0.00000,
                                 fmsi=0.00000,
                                 fnetprice=total_price,
                                 fninvship=0.00000,
                                 fnpurvar=0.0000,
                                 forderqty=quantity,
                                 fothrcost=0.00000,
                                 fovhdcost=0.00000,
                                 fpoqty=0.00000,
                                 fpostatus="",
                                 fquant=0.00000,
                                 fsetupcost=0.00000,
                                 fshipbook=0.00000,
                                 fshipbuy=0.00000,
                                 fshipmake=0.00000,
                                 fshpbefdue=True,
                                 fsplitshp=True,
                                 fstatus="",
                                 fstkqty=0.00000,
                                 fsubcost=0.00000,
                                 ftoolcost=0.00000,
                                 ftoshpbook=0.00000,
                                 ftoshpbuy=0.00000,
                                 ftoshpmake=0.00000,
                                 funetprice=unit_price,
                                 fvendno="",
                                 fwidth=0.00000,
                                 fnretpoqty=0.00000,
                                 fnettxnprice=0.00000,
                                 funettxnpric=0.00000,
                                 fneteuropr=0.00000,
                                 funeteuropr=0.00000,
                                 fdiscpct=0.00000,
                                 fljrdif=False,
                                 flistaxabl=False,
                                 flatp=False,
                                 fcbin="",
                                 fcloc=location,
                                 fdelivery="",
                                 fndbrmod=0,
                                 fcpbtype="",
                                 fcudrev="",
                                 fpriority=4,
                                 scheddate=DEFAULT_DATE,
                                 flinvcposs=False,
                                 fmatlpadj=0.00000,
                                 ftoolpadj=0.00000,
                                 flabpadj=0.00000,
                                 fovhdpadj=0.00000,
                                 fsubpadj=0.00000,
                                 fothrpadj=0.00000,
                                 fsetuppadj=0.00000,
                                 fnisoqty=0.00000,
                                 earlydays=0,
                                 fcrelsstatus="Started",
                                 fdrequestdate=order_date,
                                 fdcreateddate=order_date,
                                 forigreqdt=DEFAULT_DATE,
                                 ffinalschd=False, )

    def create_sales_order_bom_item(self, so_master: mm.Somast, idx: int, part_number: str, rev: str, quantity: float,
                                    measure: str, source: str, description: str, memo: str, fac: str):
        mm.Sodbom.objects.create(fbominum="   0",
                                 fbompart=part_number,
                                 fbomrev=rev,
                                 finumber=self.format_finumber(f"{idx}"),
                                 fitem="",
                                 fparinum="",
                                 fsono=so_master.fsono,
                                 fbomlcost=0.00000000,
                                 fbommeas=measure,
                                 fbomocost=0.00000000,
                                 fbomsource=source,
                                 fcostfrom="",
                                 fextqty=quantity,
                                 ffixcost=0.00000000,
                                 flabcost=0.00000000,
                                 flabsetcos=0.00000000,
                                 flastoper=0,
                                 flevel=" 0",
                                 flextend=False,
                                 fltooling=False,
                                 fmatlcost=0.00000,
                                 fnonpro=0,
                                 fnumopers=0,
                                 fothrcost=0.00000000,
                                 fovhdcost=0.00000000,
                                 fovrhdsetc=0.00000000,
                                 fsubcost=0.00000000,
                                 ftotptime=0.0000000,
                                 ftotqty=0.00000,
                                 ftotstime=0.0000000,
                                 fvendno="",
                                 fllotreqd=False,
                                 fclotext="",
                                 fnoperno=0,
                                 fbomdesc=description,
                                 fstdmemo=memo,
                                 fndbrmod=0,
                                 fac=fac,
                                 fcbomudrev=rev,
                                 flrfqreqd=False,
                                 fcsource="",
                                 )

    @staticmethod
    def get_payment_term_code(term_desc: str, company: mm.Slcdpmx) -> str:

        from django.db import connection
        cursor = connection.cursor()
        try:
            terms_query = f"SELECT fctermsid FROM UTTERMS WHERE fcdescr = '{term_desc}'"
            cursor.execute(terms_query)
            terms = cursor.fetchone()
        finally:
            cursor.close()
            connection.close()
        term_code = company.fterm
        if terms is not None:
            term_code = terms[0]
        return term_code

    @staticmethod
    def get_last_so_master() -> int:
        from django.db import connection
        cursor = connection.cursor()
        try:
            query = "SELECT fsono from somast ORDER BY identity_column DESC"
            cursor.execute(query)
            result = cursor.fetchall()
            last_so_no = int(result[0][0])
        finally:
            cursor.close()
            connection.close()
        return last_so_no

    def format_finumber(self, number) -> str:
        # M2M Requires that the 'finumber' field be a string of length 3. We need to include white spaces so that the
        # field always has a length of 3.
        finumber = number.rjust(3)
        return finumber
