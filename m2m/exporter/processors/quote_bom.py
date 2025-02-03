import datetime
from typing import Optional, List

from baseintegration.datamigration import logger
from paperless.objects.orders import OrderComponent, OrderItem
import m2m.models as mm
from m2m.configuration import M2MConfiguration
from m2m.utils.item_master import ItemMasterHelper

DEFAULT_DATE = datetime.datetime(1900, 1, 1, 0, 0, 0)


class QuoteBOMFactory:
    m2m_config = M2MConfiguration()

    def __init__(self, configuration: M2MConfiguration):
        self.m2m_config = configuration
        self.bom_line: Optional[mm.Qtdbom] = None
        self.last_bom_item_num = 0
        self.quote_item: Optional[mm.Qtitem] = None
        self.level = 0
        self.order_item: Optional[OrderItem] = None
        self.price_summary: Optional[mm.Qtpest] = None

    def check_create_quote_bom(self, bom_line: mm.Qtdbom, root: OrderComponent, components: {OrderComponent},
                               order_item: OrderItem, m2m_quote_item: mm.Qtitem, level: int, price_summary: mm.Qtpest,
                               last_bom_item_num=0, consolidate: int = None) -> (int, List[tuple[int, mm.Qtdbom]]):
        self.price_summary = price_summary
        self.bom_line = bom_line
        self.last_bom_item_num = last_bom_item_num
        self.quote_item = m2m_quote_item
        self.level = level
        self.order_item = order_item

        # first, create BOM records for child components

        child_component_bom_lines = []

        for child_data in root.children:
            child: OrderComponent = components[child_data.child_id]
            logger.info(f'Adding component {child.part_name} to BOM')
            if consolidate == child.id:
                self.create_material_bom_record(child)
                continue
            item_record_child = ItemMasterHelper.get_item_record(child)
            source = 'B' if child.is_hardware else 'M'  # 'B' == 'BUY', 'M' == 'MAKE'
            if isinstance(item_record_child, mm.Inmastx):
                part_number = item_record_child.fpartno
                rev = item_record_child.frev
                memo = item_record_child.fstdmemo
                description = item_record_child.fdescript
            else:
                part_number, rev = ItemMasterHelper.get_part_num_rev(child)
                rev = 'NS'
                memo = child.description or ''
                description = child.description or ''

            material_cost = 0.0
            if child.is_hardware and child.purchased_component:
                op_costs = [float(op.cost.raw_amount) for op in child.shop_operations]
                material_cost = sum(op_costs) / child.make_quantity

            bom_line = self.create_bom_line(
                part_number=part_number, rev=rev, source=source, unit_quantity=float(child_data.quantity),
                bom_quantity=float(self.bom_line.fextqty),
                material_cost=material_cost, description=description, memo=memo,
                num_operations=len(child.shop_operations)
            )

            child_component_bom_lines.append((child.id, bom_line))

        # next, create BOM records for materials
        self.create_material_bom_record(root)

        return self.last_bom_item_num, child_component_bom_lines

    def create_material_bom_record(self, comp: OrderComponent):
        for material_op in comp.material_operations:
            material_item = material_op.get_variable("Item Master Number")
            if material_item is None or material_item == '':
                logger.info(f'Material part number not found on {material_op.name}, not adding to BOM')
                continue
            logger.info(f'Adding material {material_item} to BOM')
            qty = material_op.get_variable("Unit Material Qty")
            if qty is None or qty == '' or float(qty) == 0.0:
                qty = 1
            unit_material_quantity = float(qty)
            item_record_child: mm.Inmastx = mm.Inmastx.objects.filter(fpartno=material_item).first()
            description = material_op.notes or ''
            source = 'B'
            if item_record_child:
                part_number = item_record_child.fpartno
                rev = item_record_child.frev
                memo = item_record_child.fstdmemo
                unit_of_measure = item_record_child.fmeasure
            else:
                part_number = material_item
                rev = 'NS'
                memo = ''
                unit_of_measure = material_op.get_variable("Unit of Measure") or 'EA'

            unit_material_cost = 0.0
            bom_quantity = 1.0
            for q in material_op.quantities:
                if q.quantity == self.order_item.quantity:
                    total_material_cost = q.manual_price.raw_amount if q.manual_price is not None \
                        else q.price.raw_amount
                    bom_quantity = float(self.bom_line.fextqty)
                    total_material_quantity = bom_quantity * unit_material_quantity
                    unit_material_cost = float(total_material_cost) / total_material_quantity

            self.create_bom_line(
                part_number=part_number, rev=rev, source=source,
                unit_quantity=unit_material_quantity, bom_quantity=bom_quantity,
                material_cost=unit_material_cost, description=description, memo=memo, unit_of_measure=unit_of_measure
            )

    def create_bom_line(self, part_number: str, rev: str, source: str, unit_quantity: float, bom_quantity: float,
                        material_cost: float, description: str, memo: str, op_num: int = 10,
                        num_operations: int = 0, unit_of_measure: str = 'EA'):
        self.last_bom_item_num += 1
        bom_line = mm.Qtdbom.objects.create(
            fbompart=part_number,
            fbomrev=rev,
            fbominum='{: 4d}'.format(self.last_bom_item_num),
            fbomlcost=0.0,
            fbommeas=unit_of_measure,
            fbomocost=0.0,
            fbomsource=source,
            fcostfrom='',
            fextqty=unit_quantity * bom_quantity,
            ffixcost=0.0,
            finumber=self.quote_item.finumber,
            fitem='',
            flabcost=0.0,
            flastoper=0,
            flevel='{: 2d}'.format(self.level),
            flextend=True,
            fltooling=False,
            fmatlcost=material_cost,
            fnonpro=0,
            fnumopers=num_operations,
            forgbomqty=unit_quantity,
            fothrcost=0.0,
            fovhdcost=0.0,
            fparinum=self.bom_line.fbominum,
            fquoteno=self.quote_item.fquoteno,
            fsetupcost=0.0,
            fsubcost=0.0,
            ftotptime=0.0,
            ftotqty=unit_quantity,
            ftotstime=0.0,
            fuprice=0.0,
            fvendno='',  # vendor number chosen to buy this component from
            fllotreqd=False,  # lot required?
            fclotext='',  # extent of lot control
            fnoperno=op_num,  # routing operation number where this material is needed
            fbomdesc=description,
            fstdmemo=memo,
            fac='Default',
            fcbomudrev='',
            fndbrmod=0,
            flrfqreqd=False,
            fcsource=''
        )

        # data is modified/reformatted upon saving; use refresh_from_db to ensure we have accurate data
        bom_line.refresh_from_db()

        self.update_price_summary_with_bom_line(bom_line)
        return bom_line

    def update_price_summary_with_bom_line(self, bom_line: mm.Qtdbom):
        # data is modified/reformatted upon saving; use refresh_from_db to ensure we have accurate data
        self.price_summary.refresh_from_db()

        bom_line_mat_cost = bom_line.fmatlcost
        if bom_line.flextend:
            bom_line_mat_cost *= bom_line.fextqty
        if bom_line.fltooling:
            self.price_summary.ftoolcost += bom_line_mat_cost
        else:
            self.price_summary.fmatlcost += bom_line_mat_cost

        self.price_summary.save()
