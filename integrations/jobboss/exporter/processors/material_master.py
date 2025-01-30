from baseintegration.datamigration import logger
from jobboss.query.job import get_material
import jobboss.models as jb
import datetime
import uuid
from . import JobBossProcessor
from paperless.objects.orders import OrderComponent, OrderItem, OrderOperation
from django.utils.timezone import make_aware


class MaterialProcessor(JobBossProcessor):
    do_rollback = False

    def _process(self, order_item: OrderItem, comp: OrderComponent):  # noqa: C901
        # Check if Material records should be generated at all
        material = None
        if not self._exporter.erp_config.import_material:
            logger.info('[Material Master] - Material generation is disabled. Check config.yaml options.')
            return material

        # Get material attributes if material generation is enabled
        comp_type = self.get_comp_type(comp)
        selling_price = self.get_selling_price(order_item, comp_type)
        desc, ext_desc = self.get_descriptions(comp)

        # Generate finished goods first if enabled
        if self.should_generate_finished_good(order_item, comp):
            self.generate_finished_good(comp, selling_price, desc, ext_desc)

        # Log info on each of the raw material operations (if enabled)
        if self._exporter.erp_config.generate_material_ops and comp_type == 'R':
            self.process_raw_material_operations(order_item, comp)

        # Get or create hardware materials (if enabled)
        if comp_type == "H":
            material = self.process_hardware_materials(order_item, comp, selling_price, comp_type, desc, ext_desc)

        return material

    def get_comp_type(self, comp: OrderComponent) -> str:
        """
        Returns type="R" unless the component is hardware.
        """
        if comp.is_hardware:
            return 'H'
        return 'R'

    def get_selling_price(self, order_item: OrderItem, comp_type):
        # Depending on component type, assign a price
        return {
            'H': 0,
            'R': order_item.unit_price.dollars,
            'F': order_item.unit_price.dollars
        }.get(comp_type, 0)

    def get_descriptions(self, comp: OrderComponent):
        desc = None
        ext_desc = None
        if comp.description:
            if len(comp.description) <= 30:
                desc = comp.description
            else:
                desc = comp.description[0:30]
                ext_desc = comp.description
        return desc, ext_desc

    def should_generate_finished_good(self, order_item: OrderItem, comp: OrderComponent):
        if self._exporter.erp_config.generate_finished_good_material and comp.type == "manufactured":
            return True
        if self._exporter.erp_config.generate_finished_good_material and comp.type == "assembled":
            return True
        return False

    def generate_finished_good(self, comp: OrderComponent, selling_price: float, desc=None, ext_desc=None):
        part_number = comp.part_number
        if not part_number:
            logger.error("[Material Master] - No Finished Good was created (component has no part number).")
            return None
        material_code = part_number.strip()[:30]
        pick_buy = 'P'
        comp_type = 'F'
        fg_material = jb.Material.objects.filter(material=material_code).last()
        if not fg_material and material_code is not None:
            fg_material = self.create_material_object(material_code, comp, selling_price, comp_type, desc, ext_desc, pick_buy)
            return fg_material
        return fg_material

    def process_raw_material_operations(self, order_item: OrderItem, comp: OrderComponent):
        if len(comp.material_operations) > 0:
            for mat_op in comp.material_operations:
                material_code = self.get_pp_material_code(mat_op)
                material = get_material(material_code) if material_code is not None else None
                if material is not None:
                    logger.info(f'[Material Master] - Material exists: {material.material}')
                elif self._exporter.erp_config.use_default_materials:
                    self.get_default_material(self._exporter.erp_config.default_raw_material)
                else:
                    logger.info('[Material Master] - No Material found or created.')
        else:
            logger.info("This component does not have any material operations.")

    def get_pp_material_code(self, mat_op: OrderOperation):
        material_code_operations = self._exporter.erp_config.pp_material_code_ops.split(",")
        if mat_op.operation_definition_name not in material_code_operations:
            return None
        material_code = mat_op.get_variable(self._exporter.erp_config.pp_mat_id_variable)
        if material_code is not None:
            material_code = material_code[0:30]
        return material_code

    @staticmethod
    def get_default_material(material_name: str):
        default_material = get_material(material_name)
        if default_material is None:
            logger.info("[Material Maser] - Default material does not yet exist! Configure this with your shop.")
        else:
            logger.info(f'[Material Master] - Default Material enabled: {default_material.material}')
        return default_material

    def process_hardware_materials(self, order_item: OrderItem, comp: OrderComponent, selling_price, comp_type,
                                   desc, ext_desc):
        material = None
        if comp.part_number and get_material(comp.part_number.strip()[:30]) is not None:
            material = get_material(comp.part_number.strip()[:30])
            logger.info(f'[Material Master] - Material exists: {material.material}')
        elif self._exporter.erp_config.should_create_new_hardware_materials is False:
            logger.info(f"[Material Master] - Hardware generation is disabled."
                        f"Part number not created for {comp.part_number}")
            return None
        elif comp.part_number is not None:
            material_code = comp.part_number.strip()[:30]
            material = self.create_material_object(material_code, comp, selling_price, comp_type, desc, ext_desc)
        else:
            logger.info('[Material Master] - No part number provided. No Material created.')
        return material

    def create_material_object(self, material_code, comp, selling_price=0.0, comp_type="M", desc=None, ext_desc=None, pick_buy=None, job=None):
        material = jb.Material.objects.create(
            material=material_code,
            description=desc,
            drawing=comp.part_name,
            ext_description=ext_desc,
            sales_code=self._exporter.erp_config.sales_code,
            rev=comp.revision,
            location_id=self._exporter.erp_config.default_location,
            type=comp_type,
            status='Active',
            pick_buy_indicator=pick_buy if pick_buy is not None else "B",
            stocked_uofm='ea',
            purchase_uofm='ea',
            cost_uofm='ea',
            price_uofm='ea',
            selling_price=selling_price,
            standard_cost=selling_price,
            last_cost=selling_price,
            average_cost=selling_price,
            on_order_qty=0,
            order_point=0,
            reorder_qty=0,
            lead_days=0,
            uofm_conv_factor=1,
            lot_trace=False,
            rd_whole_unit=1,
            price_unit_conv=1,
            make_buy='M',
            use_price_breaks=True,
            last_updated=make_aware(datetime.datetime.utcnow()),
            taxable=False,
            affects_schedule=0,
            tooling=False,
            isserialized=False,
            maxusage=0,
            shelflife=0,
            objectid=uuid.uuid4()
        )
        try:
            material.save()
            logger.info(f"[Material Master] - Saved Material {material.material}")
        except Exception as e:
            logger.error(f'[Material Master] - Failed to save Material: {material.material}. [ERROR] - {e}')
            logger.error(material.__dict__)
        return material
