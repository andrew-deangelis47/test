import datetime
from typing import Optional

from baseintegration.datamigration import logger
from paperless.objects.orders import Order
import m2m.models as mm
from m2m.configuration import M2MConfiguration
from m2m.exporter.processors.sales_orders import SalesOrderFactory
from m2m.utils.item_master import ItemMasterHelper

DEFAULT_DATE = datetime.datetime(1900, 1, 1, 0, 0, 0)


class SalesQuoteFactory:
    m2m_config = M2MConfiguration()

    def __init__(self, configuration: M2MConfiguration):
        self.m2m_config = configuration
        self.order_item_to_quote_item = {}
        self.item_number = 0

    def create_sales_quote(self, order: Order) -> (mm.Qtmast, dict):
        self.order_item_to_quote_item = {}

        notes_str = 'Paperless Parts Quote #{}\r\n' \
                    'https://app.paperlessparts.com/quotes/edit/{}\r\n' \
                    'Paperless Parts Order #{}\r\n' \
                    'https://app.paperlessparts.com/orders/edit/{}\r\n\r\n'.format(order.quote_number,
                                                                                   order.quote_number,
                                                                                   order.number,
                                                                                   order.number)
        company: Optional[mm.Slcdpmx] = None
        if order.contact.account and order.contact.account.erp_code:
            erp_code = order.contact.account.erp_code
            company = mm.Slcdpmx.objects.filter(fcustno=erp_code).first()
        if not company:
            default_erp_code = self.m2m_config.default_erp_code
            company = mm.Slcdpmx.objects.filter(fcustno=default_erp_code).first()

        payment_terms = SalesOrderFactory.get_payment_term_code(order.payment_details.payment_terms, company)
        estimator = ''
        if order.estimator:
            estimator = f'{order.estimator.first_name[0]}{order.estimator.last_name[0]}'

        order_ships_on_date = order.ships_on_dt.date()
        order_created_date = order.created_dt.replace(tzinfo=None).date()
        now = datetime.datetime.now()
        pp_quote_number = f'{order.quote_number}'
        if order.quote_revision_number:
            pp_quote_number += f'-{order.quote_revision_number}'

        quote_master: mm.Qtmast = mm.Qtmast(
            fcsoldto=company.fcsoldto,
            fcustno=company.fcustno,
            fcompany=company.fcompany,
            fackdate=DEFAULT_DATE,
            fccurid='USD',
            fcfname=order.contact.first_name,
            fquoteto=order.contact.last_name,
            fcshipto=company.fcshipto,
            fmstreet=company.fmstreet,
            fcity=company.fcity,
            fstate=company.fstate,
            fzip=company.fzip,
            fcountry=company.fcountry,
            festimator=estimator,
            fphone=company.fphone,
            fdatedue=order_ships_on_date,
            fcfactor=1.0000,
            fdaterecvd=DEFAULT_DATE,
            fdcurdate=DEFAULT_DATE,
            fdexpired=DEFAULT_DATE,
            fduplicate=False,
            fprint_dt=DEFAULT_DATE,
            fprinted=False,
            fquotecopy='N',
            fquotedate=order_created_date,
            frequestno=pp_quote_number,
            frevno='',
            fsalespn='',
            ftype='C',  # This quote is to a customer
            fnusrqty1=0.0,
            fnusrcur1=0.0,
            fdusrdate1=DEFAULT_DATE,
            fdisrate=0.0,
            fterm=payment_terms,
            fpaytype=company.fpaytype,
            fdeurodate=DEFAULT_DATE,
            feurofctr=0.0,
            fusercode=company.fusercode,
            fltotal=False,
            fclosmemo='',
            fmusermemo=notes_str,
            fsalumemo='',
            fccontkey='',
            flcontract=False,
            fndbrmod=0,
            contractnu='',
            opportunnum='',
            modifieddate=DEFAULT_DATE,
            oppcrtype='',
            createddate=now,
            fbilladdr=''
        )
        quote_master.save_with_autonumber()

        # data is modified/reformatted upon saving; use refresh_from_db to ensure we have accurate data
        quote_master.refresh_from_db()

        logger.info(f'Created sales quote {quote_master.fquoteno} for order {order.number}')
        self.create_sales_quote_items(order, quote_master)
        return quote_master, self.order_item_to_quote_item

    def create_sales_quote_items(self, order: Order, quote_master: mm.Qtmast):
        self.item_number = 1
        for item in order.order_items:
            item_master = ItemMasterHelper.get_item_record(item.root_component)
            if item_master and self.m2m_config.add_standard_parts_as_quote_items:
                # add sales quote line that references existing item master entry
                quote_item, price_summary, root_bom_line = self.create_sales_quote_item_from_item_master(
                    item_master=item_master, quote_master=quote_master, quantity=item.quantity,
                    price=float(item.unit_price.dollars)
                )
            else:
                # item not found in item master; add sales quote line that references new non-standard item
                component = item.root_component
                part_number, revision = ItemMasterHelper.get_part_num_rev(component)
                description = component.description[:34] if component.description is not None else ''
                memo = item.public_notes or ""

                # get product class from variable
                part_class = '01'
                for operation in component.shop_operations:
                    value = operation.get_variable("Product Class")
                    if value and value != 'Select a Product Class':
                        part_class = value

                # get group code from variable
                group_code = '01'
                for operation in component.shop_operations:
                    value = operation.get_variable("Group Code")
                    if value and value != 'Select a Group Code':
                        group_code = value

                quote_item, price_summary, root_bom_line = self.create_sales_quote_item(
                    quote_master=quote_master, part_number=part_number, rev='NS', customer_rev=revision, measure='EA',
                    source='M', description=description, memo=memo, group_code=group_code,
                    cud_rev='NS', production_class=part_class, quantity=item.quantity,
                    price=float(item.unit_price.dollars)
                )

            self.item_number += 1
            self.order_item_to_quote_item[item.id] = (quote_item, price_summary, root_bom_line)

            if item.ordered_add_ons:
                for add_on in item.ordered_add_ons:
                    notes = add_on.notes if add_on.notes else ''
                    split = add_on.name.split(' - ')
                    part_number = split[0]
                    item_master = mm.Inmastx.objects.filter(fpartno=part_number).first()
                    if item_master:
                        notes = f'{item_master.fdescript} : {notes}'
                    self.create_add_on_item(
                        quote_master=quote_master, item_master=item_master, notes=notes, add_on_name=add_on.name,
                        price=float(add_on.price.raw_amount)
                    )
                    self.item_number += 1
                self.item_number += 1
        quote_master.fnextinum = self.item_number
        quote_master.fnextenum = str(self.item_number).zfill(3)
        quote_master.save()

    def create_add_on_item(self, add_on_name: str, quote_master: mm.Qtmast, notes: str,
                           item_master: Optional[mm.Inmastx], price: float):
        if item_master:
            self.create_sales_quote_item_from_item_master(
                item_master=item_master, quote_master=quote_master, quantity=1, price=price
            )
        else:
            self.create_sales_quote_item(
                quote_master=quote_master, cud_rev='NS', quantity=1, rev='NS', measure='EA', source='',
                part_number=add_on_name, description=notes, memo='', production_class='01',
                price=price, group_code='01'
            )

    def create_sales_quote_item_from_item_master(self, item_master: mm.Inmastx, quote_master: mm.Qtmast,
                                                 quantity: int, price: float):
        return self.create_sales_quote_item(
            quote_master=quote_master, part_number=item_master.fpartno, rev=item_master.frev,
            measure=item_master.fmeasure, source=item_master.fsource, description=item_master.fdescript,
            memo=item_master.fstdmemo, fac=item_master.fac, sfac=item_master.sfac,
            cud_rev=item_master.fcudrev, production_class=item_master.fprodcl, quantity=quantity,
            price=price, group_code=item_master.fgroup
        )

    def create_sales_quote_item(self, quote_master: mm.Qtmast,
                                part_number: str, rev: str, measure: str, source: str, description: str, memo: str,
                                cud_rev: str, production_class: str, quantity: float,
                                price: float, group_code: str, fac: str = 'Default', sfac: str = 'Default',
                                customer_rev='') -> (mm.Qtitem, mm.Qtpest):
        # create the quote item
        quote_item = mm.Qtitem.objects.create(
            finumber=self.item_number,
            fpartno=part_number,
            fpartrev=rev,
            fcustptrev=customer_rev,
            fquoteno=quote_master.fquoteno,
            funetprice=price,
            funettxnpric=0.0,
            funeteuropr=0.0,
            fclotext=" ",
            fllotreqd=False,
            fcas_bom=False,
            fcas_rtg=False,
            fcustpart="",
            fdet_bom=True,
            fdet_rtg=True,
            fenumber=str(self.item_number).zfill(3),
            ffixact=0.0,
            fgroup=group_code,
            flabact=0.0,
            fmatlact=0.0,
            fovhdact=0.0,
            fothract=0.0,
            fsubact=0.0,
            ftoolact=0.0,
            fsetupact=0.0,
            fulabcost=0.0,
            fmeasure=measure,
            fnextinum=1,
            fprintmemo=False,
            flordered=False,
            fprodcl=production_class,
            fbomqty=0,
            festqty=quantity,
            fcfromtype="",
            fcfromno="",
            fcfromitem="",
            frtgsetupa=0.0,
            fschecode="",
            fsource=source,
            fstandpart=rev != 'NS',
            ftotptime=0.0,
            ftotstime=0.0,
            fcprodid="",
            fschedtype="",
            fdesc=description,
            fdescmemo=memo,
            fndbrmod=0,
            fac=fac,
            sfac=sfac,
            itccost=0.0,
            fcudrev=cud_rev,
            contractnu="",
            flrfqreqd=False,
            fcostfrom="",
            flistaxabl=False,
            fljrdif=False,
            fctpdate=DEFAULT_DATE,
            fctptrans=DEFAULT_DATE
        )

        # data is modified/reformatted upon saving; use refresh_from_db to ensure we have accurate data
        quote_item.refresh_from_db()

        # we need to create a hidden BOM line for the quote item; it doesn't show up in the UI
        root_bom_line = self.create_root_bom_item(quote_item)

        # now create the price summary
        price_summary = self.create_price_summary(quote_item)

        return quote_item, price_summary, root_bom_line

    def create_root_bom_item(self, quote_item: mm.Qtitem):
        root_bom_item = mm.Qtdbom.objects.create(
            fbompart=quote_item.fpartno,
            fbomrev=quote_item.fpartrev,
            fbominum='{: 4d}'.format(0),
            fbomlcost=0.0,
            fbommeas=quote_item.fmeasure,
            fbomocost=0.0,
            fbomsource=quote_item.fsource,
            fcostfrom='',
            fextqty=quote_item.festqty,
            ffixcost=0.0,
            finumber=quote_item.finumber,
            fitem='',
            flabcost=0,
            flastoper=0,
            flevel=' 0',
            flextend=True,
            fltooling=False,
            fmatlcost=0.0,
            fnonpro=0,
            fnumopers=0,
            forgbomqty=0,
            fothrcost=0.0,
            fovhdcost=0.0,
            fparinum='',
            fquoteno=quote_item.fquoteno,
            fsetupcost=0.0,
            fsubcost=0.0,
            ftotptime=0.0,
            ftotqty=float(quote_item.festqty),
            ftotstime=0.0,
            fuprice=0.0,
            fvendno='',
            fllotreqd=False,
            fclotext='',
            fnoperno=10,
            fbomdesc=quote_item.fdesc,
            fstdmemo=quote_item.fdescmemo,
            fac=quote_item.fac,
            fcbomudrev='',
            fndbrmod=0,
            flrfqreqd=False,
            fcsource=''
        )

        # data is modified/reformatted upon saving; use refresh_from_db to ensure we have accurate data
        root_bom_item.refresh_from_db()

        return root_bom_item

    def create_price_summary(self, quote_item: mm.Qtitem):
        price_summary = mm.Qtpest.objects.create(
            fenumber=quote_item.fenumber,
            finumber=quote_item.finumber,
            fquantity=quote_item.festqty,
            fquoteno=quote_item.fquoteno,
            fdiscount=0.,
            flabcost=0.,
            fmatlcost=0.,
            fpartno=quote_item.fpartno,
            fcpartrev=quote_item.fpartrev,
            funetprice=quote_item.funetprice,
            fnetprice=quote_item.festqty * quote_item.funetprice,
            fothrcost=0.,
            fovhdcost=0.,
            fsetupcost=0.,
            fsubcost=0.,
            ftoolcost=0.,
            fnettxnprice=0.,
            funettxnpric=0.,
            fneteuropr=0.,
            funeteuropr=0.,
            fdiscpct=0.,
            fcudrev=quote_item.fcudrev,
            fmatlpadj=0.,
            ftoolpadj=0.,
            flabpadj=0.,
            fovhdpadj=0.,
            fsubpadj=0.,
            fothrpadj=0.,
            fsetuppadj=0.
        )

        # data is modified/reformatted upon saving; use refresh_from_db to ensure we have accurate data
        price_summary.refresh_from_db()

        return price_summary
