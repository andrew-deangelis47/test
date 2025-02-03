from baseintegration.exporter import BaseProcessor
from inforvisual.models import Part, PartSite, TraceProfile
from paperless.objects.orders import Order, OrderItem, OrderComponent, OrderOperation
from baseintegration.datamigration import logger
import datetime
from inforvisual.exporter.utils import PartData, MaterialData, OrderItemData, PartProcessorData


class PartProcessor(BaseProcessor):

    def _process(self, order: Order):
        logger.info("Processing parts")
        self.order = order
        self.parts = []
        self.materials = []
        self.order_items = []
        logger.info("Iterating through each order item")
        # for each order item, iterate through all components and create a part if necessary
        for item in order.order_items:
            try:
                self.get_parts_and_materials(item)
                self.order_items.append(OrderItemData(item, should_process=True))
            except ValueError:
                self.order_items.append(OrderItemData(item, should_process=False))
        return PartProcessorData(part_data=self.parts, material_data=self.materials, order_item_data=self.order_items)

    def get_parts_and_materials(self, item: OrderItem):
        for component in item.components:
            logger.info(f"Checking component {component.part_name}")
            part: PartData = self.get_or_create_part(component)
            self.parts.append(part)
            # check if part is new. If yes, add its materials to the list
            if part.part_is_new:
                self.get_materials(component)

    def get_materials(self, component: OrderComponent):
        for material in component.material_operations:
            # skip the manual operations that are added to material operations
            if "Manual Operation" not in material.name.title():
                logger.info(f"Material {material.name} found, adding to materials list")
                if material.get_variable(self._exporter.erp_config.pp_mat_id_variable) is None:
                    logger.info(f"No material lookup for {material.name}, this must be an informational operation")
                    continue
                found_material: PartData = self.get_or_create_part(material)
                # swizzle in component rather than orderoperation
                found_material = found_material._replace(component=component)
                self.parts.append(found_material)
                self.materials.append(MaterialData(part_data=found_material, material_op=material))

    def get_part_number_and_name(self, component):
        if isinstance(component, OrderOperation):
            logger.info("Getting part number out of material")
            part_number = component.get_variable(self._exporter.erp_config.pp_mat_id_variable)
            part_name = part_number
        else:
            part_number = component.part_number
            if not part_number:
                part_number = str(component.part_name)[0:30]
            part_name = component.part_name
        logger.info(f"Processing part with part number {part_number}")
        return part_number, part_name

    def check_missing_materials_and_purchased_components(self, component: OrderComponent, part_name: str, part_number):
        # if purchased component or material and this wasn't found, fail and send an email
        if isinstance(component, OrderOperation) and not self._exporter.erp_config.create_material:
            self._exporter.send_email(f"Integration for order {str(self.order.number)} from Paperless Parts failed",
                                      f"{part_name} with number {part_number} not found in Infor Visual parts table. "
                                      f"This is required to bring an order over. Please check if this material is a new material")
            raise ValueError(
                f"Material {part_number} not found in parts database. This is required to bring an order over")
        elif isinstance(component,
                        OrderComponent) and component.purchased_component and not self._exporter.erp_config.create_purchased_component:
            self._exporter.send_email(f"Integration for order {str(self.order.number)} did not bring over one of the order items.",
                                      f"{part_name} with number {part_number} not found in Infor Visual parts table. "
                                      f"This is required to bring an order over. Please check if this part is a new purchased component."
                                      f"Other order items should be brought over successfully")
            raise ValueError(
                f"Purchased component {part_number} not found in parts database. This is required to bring an order over")
        else:
            return

    def get_or_create_part(self, component) -> PartData:
        part_number, part_name = self.get_part_number_and_name(component)
        logger.info(f"Checking for part with part number {str(part_number)}")
        part_number = str(part_number)[0:30]
        part = Part.objects.filter(id=part_number).first()
        part_is_new = False
        # if part does not exist yet based on part number, create it in infor visual
        if not part:
            logger.info(f"Part {part_number} not found, need to create a new part")
            part_is_new = True
            self.check_missing_materials_and_purchased_components(component, part_name, part_number)
            # if not purchased component, search operations for the product and commodity code. default to customer
            prod_code, commodity_code = self.get_product_and_commodity_code(component)
            logger.info(f"Part not found, creating part with part number {str(part_number)}")
            part = Part.objects.create(id=part_number,
                                       description=component.description[0:120] if hasattr(component, 'description') and component.description is not None else None,
                                       stock_um="EA",
                                       minimum_order_qty=1,
                                       product_code=prod_code,
                                       commodity_code=commodity_code,
                                       planning_leadtime=40,
                                       order_policy="D",
                                       fabricated="Y",
                                       purchased="N",
                                       stocked="N",
                                       detail_only="N",
                                       demand_history="N",
                                       tool_or_fixture="N",
                                       inspection_reqd="N",
                                       mrp_required="N",
                                       mrp_exceptions="N",
                                       inventory_locked="N",
                                       use_supply_bef_lt="Y",
                                       ecn_rev_control="N",
                                       is_kit="N",
                                       controlled_by_ics="N",
                                       qty_committed=0,
                                       intrastat_exempt="N",
                                       consumable="N",
                                       status_eff_date=datetime.datetime.now(),
                                       create_date=datetime.datetime.now())
            logger.info("Part was created")
            logger.info("Creating PartSite record")
            # we must create an object in both part and partsite
            PartSite.objects.create(site_id=self._exporter.erp_config.default_site_id,
                                    part_id=part_number,
                                    intrastat_exempt="N",
                                    status="A",
                                    engineering_mstr="0",
                                    is_rate_based="N",
                                    primary_whs_id=self._exporter.erp_config.default_site_id,
                                    primary_loc_id="STAGING",
                                    create_date=datetime.datetime.now())
            logger.info("Creating trace profile")
            TraceProfile.objects.create(part_id=part_number,
                                        apply_to_rec="Y",
                                        apply_to_issue="Y",
                                        apply_to_adj="Y",
                                        apply_to_labor="N",
                                        pre_assign="N",
                                        assign_method="U",
                                        trace_id_label="LOT#",
                                        aproperty_1_reqd="N",
                                        aproperty_2_reqd="N",
                                        aproperty_3_reqd="N",
                                        aproperty_4_reqd="N",
                                        aproperty_5_reqd="N",
                                        nproperty_1_reqd="N",
                                        nproperty_2_reqd="N",
                                        nproperty_3_reqd="N",
                                        nproperty_4_reqd="N",
                                        nproperty_5_reqd="N",
                                        aproperty_1_edit="N",
                                        aproperty_2_edit="N",
                                        aproperty_3_edit="N",
                                        aproperty_4_edit="N",
                                        aproperty_5_edit="N",
                                        nproperty_1_edit="N",
                                        nproperty_2_edit="N",
                                        nproperty_3_edit="N",
                                        nproperty_4_edit="N",
                                        nproperty_5_edit="N",
                                        aproperty_1_vis="N",
                                        aproperty_2_vis="N",
                                        aproperty_3_vis="N",
                                        aproperty_4_vis="N",
                                        aproperty_5_vis="N",
                                        nproperty_1_vis="N",
                                        nproperty_2_vis="N",
                                        nproperty_3_vis="N",
                                        nproperty_4_vis="N",
                                        nproperty_5_vis="N",
                                        edit_exp_date="Y",
                                        auto_fill_trace="A",
                                        apply_to_servdisp="N",
                                        apply_to_servrec="N",
                                        ownership="N",
                                        lot="N",
                                        serial="N",
                                        colocate_lots="N",
                                        expiration="N",
                                        colocate_alphas="N",
                                        colocate_numerics="N",
                                        accept_expired_rcv="N",
                                        ownership_known="N",
                                        lot_known="N",
                                        serial_known="N",
                                        expiration_known="N",
                                        aproperty_1_known="N",
                                        aproperty_2_known="N",
                                        aproperty_3_known="N",
                                        aproperty_4_known="N",
                                        aproperty_5_known="N",
                                        nproperty_1_known="N",
                                        nproperty_2_known="N",
                                        nproperty_3_known="N",
                                        nproperty_4_known="N",
                                        nproperty_5_known="N",
                                        count_detail="N",
                                        production="N",
                                        production_known="N",
                                        colocate_prod="N",
                                        receive_by="N",
                                        receive_by_known="N",
                                        colocate_rec_by="N",
                                        available="N",
                                        available_known="N",
                                        colocate_available="N",
                                        ship_by="N",
                                        ship_by_known="N",
                                        colocate_ship_by="N",
                                        site_id=self._exporter.erp_config.default_site_id
                                        )
        else:
            logger.info(f"Part {part_number} found, do not need to create a new part")
        return PartData(part=part, component=component, part_is_new=part_is_new)

    def get_product_and_commodity_code_operation(self, component) -> OrderOperation:
        if isinstance(component, OrderComponent) and component.shop_operations:
            for operation in component.shop_operations:
                if "PRODUCT AND COMMODITY CODE" in operation.name.upper().replace("_", ""):
                    return operation
        return None

    def get_product_code_from_costing_variables(self, costing_variables: list) -> str:
        for variable in costing_variables:
            if variable.label.title() == "Product Code":
                try:
                    return variable.value
                except:
                    return "CUSTOMER"
        return "CUSTOMER"

    def get_commodity_code_from_costing_variables(self, costing_variables: list) -> str:
        for variable in costing_variables:
            if variable.label.title() == "Commodity Code":
                try:
                    return variable.value
                except:
                    return "CUSTOMER"
        return "CUSTOMER"

    def get_product_and_commodity_code(self, component: OrderComponent):
        logger.info("Searching for prod and commodity code")
        prod_code = "CUSTOMER"
        commodity_code = "CUSTOMER"
        op = self.get_product_and_commodity_code_operation(component)
        if op:
            prod_code = self.get_product_code_from_costing_variables(op.costing_variables)
            commodity_code = self.get_commodity_code_from_costing_variables(op.costing_variables)
        return prod_code, commodity_code
