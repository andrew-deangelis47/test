import datetime
import re

from baseintegration.datamigration import logger
from paperless.objects.orders import OrderComponent, OrderOperation
import m2m.models as mm
from m2m.configuration import PurchaseToWorkCenterMap, M2MConfiguration
from m2m.utils.item_master import ItemMasterHelper

DEFAULT_DATE = datetime.datetime(1900, 1, 1, 0, 0, 0)


class StandardBOMFactory:
    m2m_config = M2MConfiguration()

    def __init__(self, configuration: M2MConfiguration):
        self.m2m_config = configuration

    def check_create_standard_bom(self, item_record: mm.Inmastx, root: OrderComponent, components: {OrderComponent},
                                  ops: [mm.Inrtgs], consolidate: int = None):
        bom: mm.Inbomm = mm.Inbomm.objects.filter(fpartno=item_record.fpartno, fcpartrev=item_record.frev).first()
        if not isinstance(bom, mm.Inbomm):
            mm.Inbomm.objects.create(fpartno=item_record.fpartno,
                                     fcpartrev=item_record.frev,
                                     fnbommax=0,
                                     fnbommin=0,
                                     fdlastrev=item_record.frevdt,
                                     facilityid="Default",
                                     fcudrev=item_record.frev)
            child: OrderComponent
            for child_id in root.child_ids:
                child = components[child_id]
                if child.parent_ids[0] != root.id:
                    continue
                if consolidate == child.id:
                    self.create_material_bom_record(item_record, child, ops)
                    continue
                op_num = 10
                item_record_child = ItemMasterHelper.get_item_record(child)
                if child.type == "purchased":
                    op_num = self.get_op_number_for_item(item_record_child, ops)
                else:
                    for operation in child.shop_operations:
                        # "ROLLS TO" tell you were in the parent router the the child BOM item goes.
                        if "ROLLS TO" in operation.name:
                            assembly_roll_up = operation.name.split("ROLLS TO")[1].strip()
                            op: mm.Inrtgs
                            for op in ops:
                                if assembly_roll_up in op.fopermemo and "ROLLS TO" not in op.fopermemo:
                                    op_num = op.foperno
                                    break
                part_number, rev = ItemMasterHelper.get_part_num_rev(child)
                rev = 'NS'
                memo = child.description if child.description else ''
                if isinstance(item_record_child, mm.Inmastx):
                    part_number = item_record_child.fpartno
                    rev = item_record_child.frev
                    memo = item_record_child.fstdmemo

                mm.Inboms.objects.create(fcomponent=part_number,
                                         fcomprev=rev,
                                         fitem="",
                                         fparent=item_record.fpartno,
                                         fparentrev=item_record.frev,
                                         fend_ef_dt=DEFAULT_DATE,
                                         fmemoexist=" ",
                                         fqty=child.innate_quantity,
                                         freqd=" ",
                                         fst_ef_dt=DEFAULT_DATE,
                                         flextend=True,
                                         fltooling=False,
                                         fnoperno=op_num,
                                         fbommemo=memo,
                                         fndbrmod=0,
                                         cfacilityid="Default",
                                         pfacilityid="Default",
                                         fcompudrev=rev,
                                         fcparudrev="   ",
                                         flfssvc=False,
                                         forigqty=0.00000,
                                         fcsource="")
            self.create_material_bom_record(item_record, root, ops)
        logger.info('existing bom found')

    def get_op_number_for_item(self, item_record: mm.Inmastx, ops: [mm.Inrtgs]):
        if ops is None:
            ops = []
        op_number = 10
        if isinstance(item_record, mm.Inmastx):
            work_centers = []
            p_map: PurchaseToWorkCenterMap
            for p_map in self.m2m_config.purchase_work_center_maps:
                if re.search(p_map.search, item_record.fpartno):
                    work_centers = p_map.work_centers
                    break
            op: mm.Inrtgs
            for op in ops:
                if op.fpro_id in work_centers or op.fcstddesc in work_centers:
                    op_number = op.foperno
                    break
        return op_number

    def create_material_bom_record(self, item_record: mm.Inmastx, comp: OrderComponent, ops: [mm.Inrtgs]):
        item_mater_number_var = self.m2m_config.material_item_mater_number_costing_variable
        for material_op in comp.material_operations:
            material_item = material_op.get_variable(item_mater_number_var)
            if material_item is None or material_item == '':
                continue
            qty = self.get_quantity_for_material(material_op)
            if qty is None or qty == '':
                qty = 1
            material_quantity = qty
            item_record_child: mm.Inmastx = mm.Inmastx.objects.filter(fpartno=material_item).first()
            if item_record_child is None:
                logger.info(f'Did not add {material_item} to the Standard BOM since the item master record was missing')
                continue
            op_num = self.get_op_number_for_item(item_record_child, ops)
            mm.Inboms.objects.create(fcomponent=item_record_child.fpartno,
                                     fcomprev=item_record_child.frev,
                                     fitem="      ",
                                     fparent=item_record.fpartno,
                                     fparentrev=item_record.frev,
                                     fend_ef_dt=DEFAULT_DATE,
                                     fmemoexist=" ",
                                     fqty=material_quantity,
                                     freqd=" ",
                                     fst_ef_dt=DEFAULT_DATE,
                                     flextend=True,
                                     fltooling=False,
                                     fnoperno=op_num,
                                     fbommemo=item_record_child.fstdmemo,
                                     fndbrmod=0,
                                     cfacilityid="Default",
                                     pfacilityid="Default",
                                     fcompudrev='',
                                     fcparudrev="   ",
                                     flfssvc=False,
                                     forigqty=0.00000,
                                     fcsource="")

    def get_quantity_for_material(self, material_op: OrderOperation) -> float:
        """
        This method is for finding quantities for materials.  'Parts Per' will be for raw stock items.  'QTY -' will be
        for powder coat and pint.
        """
        quantity = 1.0
        uom = material_op.get_variable(self.m2m_config.material_unit_of_measure_costing_variable)
        if not uom:
            uom = ''
        for variable in material_op.costing_variables:
            if variable.label == self.m2m_config.material_quantity_per_part_costing_variable:
                quantity = variable.value
                break
            if variable.label.startswith("QTY -") and uom.lower() in variable.label.lower():
                quantity = variable.value
            if variable.label.startswith("Parts Per") and variable.value != 0.:
                quantity = 1 / float(variable.value)
        return float(quantity)
