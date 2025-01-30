import datetime
from typing import Tuple
from paperless.objects.orders import OrderComponent
import m2m.models as mm

DEFAULT_DATE = datetime.datetime(1900, 1, 1, 0, 0, 0)


class ItemMasterHelper:

    @staticmethod
    def check_create_item_for_make(comp: OrderComponent, customer_erp: str, memo: str = '') -> mm.Inmastx:
        item: mm.Inmastx = ItemMasterHelper.get_item_record(comp)
        if not isinstance(item, mm.Inmastx):
            item = ItemMasterHelper.create_item_for_make(comp, customer_erp, memo)
        return item

    @staticmethod
    def get_item_record(comp: OrderComponent) -> mm.Inmastx:
        if comp.type == "purchased":
            part_number = comp.purchased_component.internal_part_number
            return mm.Inmastx.objects.filter(fpartno=part_number).first()
        part_number, revision = ItemMasterHelper.get_part_num_rev(comp)
        return mm.Inmastx.objects.filter(fpartno=part_number, frev=revision).first()

    @staticmethod
    def create_item_for_make(comp: OrderComponent, customer_erp, memo: str = '') -> mm.Inmastx:
        part_number, revision = ItemMasterHelper.get_part_num_rev(comp)
        description = comp.description
        part_class = 'P1'
        for material_op in comp.material_operations:
            value = material_op.get_variable("Product Class")
            if value and value != 'Select a Product Class':
                part_class = value
        if customer_erp is None:
            customer_erp = 'MFX100'
        item: mm.Inmastx = mm.Inmastx.objects.create(fpartno=part_number,
                                                     frev=revision,
                                                     fcstscode='A',
                                                     fdescript=description[:34] if description is not None else '',
                                                     flchgpnd=False,
                                                     fmeasure='EA',
                                                     fsource='M',
                                                     fleadtime=0.0,
                                                     fprice=0.00000,
                                                     fstdcost=0.00000,
                                                     f2totcost=0.00000,
                                                     flastcost=0.00000,
                                                     flocate1='01',
                                                     fbin1='',
                                                     f2costcode='F',
                                                     f2displcst=0.00000,
                                                     f2dispmcst=0.00000,
                                                     f2dispocst=0.00000,
                                                     f2disptcst=0.00000,
                                                     f2labcost=0.00000,
                                                     f2matlcost=0.00000,
                                                     f2ovhdcost=0.00000,
                                                     favgcost=0.00000,
                                                     fbulkissue='',
                                                     fbuyer='',
                                                     fcalc_lead='',
                                                     fcbackflsh='',
                                                     fcnts=0,
                                                     fcopymemo='Y',
                                                     fcostcode='R',
                                                     fcpurchase='',
                                                     fcstperinv=1.000000000,
                                                     fdisplcost=0.00000,
                                                     fdispmcost=0.00000,
                                                     fdispocost=0.00000,
                                                     fdispprice=0.00000,
                                                     fdisptcost=0.00000,
                                                     fdrawno='',
                                                     fdrawsize='',
                                                     fendqty1=0.00000,
                                                     fendqty10=0.00000,
                                                     fendqty11=0.00000,
                                                     fendqty12=0.00000,
                                                     fendqty2=0.00000,
                                                     fendqty3=0.00000,
                                                     fendqty4=0.00000,
                                                     fendqty5=0.00000,
                                                     fendqty6=0.00000,
                                                     fendqty7=0.00000,
                                                     fendqty8=0.00000,
                                                     fendqty9=0.00000,
                                                     fgroup=customer_erp,
                                                     finspect='',
                                                     flabcost=0.00000,
                                                     flasteoc='',
                                                     fllotreqd=0,
                                                     fmatlcost=0.00000,
                                                     fmeasure2='EA',
                                                     fnweight=0.000,
                                                     fovhdcost=0.00000,
                                                     fprodcl=part_class,
                                                     freordqty=0.00000,
                                                     frolledup=' ',
                                                     fsafety=0.00000,
                                                     fschecode='',
                                                     fuprodtime=0.000,
                                                     fyield=100.000,
                                                     fabccode='C',
                                                     ftaxable=0,
                                                     fcusrchr1='',
                                                     fcusrchr2='',
                                                     fcusrchr3='',
                                                     fnusrqty1=0.00000,
                                                     fnusrcur1=0.00000,
                                                     fcdncfile='',
                                                     fccadfile1='',
                                                     fccadfile2='',
                                                     fccadfile3='',
                                                     fclotext=' ',
                                                     flexpreqd=0,
                                                     fschedtype='',
                                                     fldctracke=1,
                                                     fndctax=0.00000,
                                                     fndcduty=0.00000,
                                                     fndcfreigh=0.00000,
                                                     fndcmisc=0.00000,
                                                     fcratedisc='',
                                                     flconstrnt=1,
                                                     flistaxabl=0,
                                                     fcjrdict='',
                                                     flaplpart=1,
                                                     flfanpart=1,
                                                     fnfanaglvl=0,
                                                     fcplnclass='',
                                                     fcclass='',
                                                     fidims=0,
                                                     fcomment='Created By Paperless Parts',
                                                     fmusrmemo1='',
                                                     fstdmemo=memo,
                                                     fndbrmod=0,
                                                     fac='Default',
                                                     sfac='Default',
                                                     itcfixed=0.00000,
                                                     itcunit=0.00000,
                                                     fnponhand=0.00000,
                                                     fnlndtomfg=0.00000,
                                                     fipcsonhd=0,
                                                     fcudrev=revision,
                                                     fluseudrev=0,
                                                     flsendslx=1,
                                                     fcslxprod='',
                                                     flfsrtn=1,
                                                     fnlatefact=0.00,
                                                     fnsobuf=0,
                                                     fnpurbuf=0,
                                                     flcnstrpur=1,
                                                     fllatefact=1,
                                                     flsobuf=1,
                                                     flpurbuf=1,
                                                     flholdstoc=1,
                                                     fnholdstoc=0.00,
                                                     manualplan=1,
                                                     flocbfdef='01',
                                                     fbinbfdef='',
                                                     docktime=0,
                                                     fnifttime=0.0,
                                                     flsynchon=0,
                                                     flct=DEFAULT_DATE,
                                                     fdusrdate1=DEFAULT_DATE,
                                                     fdlastpc=DEFAULT_DATE,
                                                     fddcrefdat=DEFAULT_DATE,
                                                     fdvenfence=DEFAULT_DATE,
                                                     scheddate=DEFAULT_DATE,
                                                     )
        ItemMasterHelper.set_current_rev(part_number, revision)
        return item

    @staticmethod
    def set_current_rev(part_number: str, revision: str):
        inv: mm.Invcur = mm.Invcur.objects.filter(fcpartno=part_number).first()
        if isinstance(inv, mm.Invcur):
            inv.fcpartrev = revision
            inv.save()
        else:
            mm.Invcur.objects.create(
                fcpartno=part_number,
                fcpartrev=revision,
                flanycur=True,
                fac='Default',
                fcudrev=revision
            )

    @staticmethod
    def get_part_num_rev(comp: OrderComponent) -> Tuple[str, str]:
        part_number = comp.part_number
        if part_number is None:
            split = comp.part_name.split('.')
            part_number = split[0]
        part_number = part_number[:25]
        revision = comp.revision[:3] if comp.revision is not None else ''
        return part_number, revision
