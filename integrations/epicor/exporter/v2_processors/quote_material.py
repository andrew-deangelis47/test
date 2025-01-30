from baseintegration.datamigration import logger
from epicor.exporter.v2_processors.base import EpicorProcessor
from epicor.quote import QuoteHeader, QuoteMaterial
from epicor.part import Part
from epicor.utils import QuoteHeaderData, get_purchased_components_by_line_number, ItemData, PurchasedComponentData, \
    get_true_assembly_tree_nodes_by_line_number
from paperless.objects.orders import Order, OrderItem, OrderComponent, OrderOperation
from epicor.utils import get_materials_by_line_number, MaterialData, TreeNode
from typing import List, Union
from decimal import Decimal
from uuid import uuid4
from epicor.vendor import Vendor
from baseintegration.utils import safe_get
from epicor.exceptions import EpicorNotFoundException, EpicorException
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException


class QuoteMaterialProcessor(EpicorProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'quote_material'

    def _process(self, order: Order, quote_header: QuoteHeader, quote_header_data: QuoteHeaderData):

        logger.info("Adding quote materials to quote.")
        self.line_items = quote_header_data.line_items
        self.created_material: dict = {}

        for order_item_sequence_num, order_item in enumerate(order.order_items):

            self.true_assembly_tree_nodes: List[TreeNode] = get_true_assembly_tree_nodes_by_line_number(
                self.line_items, order_item_sequence_num + 1
            )

            self.line_item_materials: List[MaterialData] = \
                get_materials_by_line_number(self.line_items, order_item_sequence_num + 1)

            self.line_item_purchased_components: List[PurchasedComponentData] = get_purchased_components_by_line_number(
                self.line_items, order_item_sequence_num + 1)

            self.iterate_true_assembly_nodes(quote_header, order_item)

        # print to the integration export report
        if len(self.created_material.keys()) > 0:
            self._add_report_message(f'Created the following quote materials: \n{self._get_integration_report_message()}')
        else:
            self._add_report_message('No operation created.')

    def iterate_true_assembly_nodes(self, quote_header: QuoteHeader, order_item: OrderItem):

        for node in self.true_assembly_tree_nodes:
            component = self.get_component(node.component_id, order_item)

            # PP material operations will belong to the current node
            if not component.is_hardware:
                logger.info(f"processing PP material operations for part number: {node.part_number}")
                material_data_list = self.get_pp_material_operation_item_data_by_component(component)
                for material_data in material_data_list:
                    self.create_quote_material_from_pp_mat_op(quote_header, material_data, node)

            # PP purchased components will belong to a parent tree node
            else:
                logger.info(f"processing PP purchased components for part number: {node.part_number}")
                parent_instance_uuid = node.parent_instance_uuid
                parent_node = self.get_parent_node(parent_instance_uuid)
                pc_data = self.get_pp_pc_item_data_by_component(component)
                self.create_quote_material_from_pp_pc(quote_header, pc_data, node, parent_node)

    def get_parent_node(self, parent_instance_uuid: uuid4) -> Union[TreeNode, None]:
        for node in self.true_assembly_tree_nodes:
            if node.component_instance_uuid == parent_instance_uuid:
                return node
        return None

    def get_pp_material_operation_item_data_by_component(self, component: OrderComponent):
        material_data_list = []
        for material_data in self.line_item_materials:
            if material_data.part_data.component.id == component.id:
                material_data_list.append(material_data)
        return material_data_list

    def get_pp_pc_item_data_by_component(self, component: OrderComponent):
        if not component.is_hardware:
            logger.error("This component is not a hardware component.")
        for pc_data in self.line_item_purchased_components:
            if pc_data.component_data.component.id == component.id:
                return pc_data
        raise ValueError("No component exists")

    def create_quote_material_from_pp_mat_op(self, quote_header: QuoteHeader, part_util_object: MaterialData,
                                             node: TreeNode):
        logger.info("Creating Epicor quote material from Paperless Parts Material Operation")
        part_data: ItemData = part_util_object.part_data
        epicor_part_record = part_data.epicor_part_record
        quantity_per = self._get_raw_material_quantity_per(part_util_object)
        quantity_unit_of_measure = self._get_cost_unit_of_measure(part_util_object, epicor_part_record)
        material_notes = self._get_material_operation_notes(part_util_object)
        unit_cost = self._get_raw_material_unit_price(part_util_object, epicor_part_record)
        vendor_num, vendor_num_vendor_id = self._get_material_operation_supplier_id(part_util_object)
        lead_time = self._get_lead_time(part_util_object)
        purchase_direct = self._get_purchase_direct(part_data)
        related_operation_num = self._exporter.erp_config.default_related_operation_num
        epicor_part_number = safe_get(epicor_part_record, "PartNum")
        try:
            quote_material = QuoteMaterial(
                Company=str(self._exporter.erp_config.company_name),
                QuoteNum=quote_header.QuoteNum,
                QuoteLine=part_data.quote_line,
                AssemblySeq=node.assembly_seq_num,
                PartNum=epicor_part_number,
                Class=part_data.part_class,
                Description=part_data.part_description,
                QtyPer=quantity_per,
                EstUnitCost=unit_cost,
                MfgComment=material_notes,
                PurComment=material_notes,
                IUM=quantity_unit_of_measure,
                VendorNum=vendor_num,
                VendorNumVendorID=vendor_num_vendor_id,
                LeadTime=lead_time,
                BuyIt=purchase_direct,
                RelatedOperation=related_operation_num,
                FixedQty=self._get_fixed_qty_boolean_from_pp_operation(part_util_object.material_op)
            ).create_instance()
            self._add_to_created_materials_dict(quote_material, node)
        except EpicorException as e:
            epicor_error_message = e.message.split('"ErrorMessage":"')[-1].split('"')[0]
            raise CancelledIntegrationActionException(f"Could not export order because of material operation "
                                                      f"containing part number: {epicor_part_number}. Reason: "
                                                      f"{epicor_error_message}")

    def create_quote_material_from_pp_pc(self, quote_header: QuoteHeader, part_util_object: PurchasedComponentData,
                                         node: TreeNode, parent_node: TreeNode):
        logger.info("Creating Epicor quote material from Paperless Parts Purchased Component")
        part_data: ItemData = part_util_object.component_data
        epicor_part_record = part_data.epicor_part_record
        material_notes = self._get_purchased_component_notes(part_util_object)
        unit_cost = self._get_purchased_component_unit_cost(part_data)
        est_scrap = self._get_est_scrap_percentage(part_util_object)
        related_operation_num = self._exporter.erp_config.default_related_operation_num
        quote_material = QuoteMaterial(
            Company=str(self._exporter.erp_config.company_name),
            QuoteNum=quote_header.QuoteNum,
            QuoteLine=part_data.quote_line,
            AssemblySeq=parent_node.assembly_seq_num,
            PartNum=epicor_part_record.PartNum,
            Class=part_data.part_class,
            Description=part_data.part_description,
            QtyPer=node.quantity_per_parent,
            EstUnitCost=unit_cost,
            MfgComment=material_notes,
            PurComment=material_notes,
            IUM=epicor_part_record.IUM,
            EstScrap=est_scrap,
            RelatedOperation=related_operation_num
        ).create_instance()

        self._add_to_created_materials_dict(quote_material, parent_node)

    def _get_raw_material_quantity_per(self, raw_material_util_object: MaterialData):
        """
        - Gets the 'material_op_quantity_per_parent_var' value from P3L
        - Maps to the QtyPer field in Epicor
        """
        logger.info("Attempting to get raw material quantity per value")
        material_op = raw_material_util_object.material_op
        qty_per = material_op.get_variable(self._exporter.erp_config.material_op_quantity_per_parent_var)
        if not qty_per:
            return 1
        return round(qty_per, 4)

    def _get_raw_material_unit_price(self, raw_material_util_object: MaterialData, epicor_part: Union[Part, None]
                                     ) -> Union[float, Decimal]:
        """
        - Attempts to get unit price from P3L variable configured in config, 'pp_mat_cost_variable'
        - If no value is found for that P3L variable, attempts to assign unit price from the Epicor part master record
        - If no epicor part record exists - assigns unit price to 0 as a last resort
        """
        logger.info("Attempting to get raw material unit price")
        material_op = raw_material_util_object.material_op
        unit_price = material_op.get_variable(self._exporter.erp_config.pp_mat_cost_variable)
        if not unit_price:
            if not epicor_part:
                return 0
            return epicor_part.UnitPrice
        return float(unit_price)

    def _get_cost_unit_of_measure(self, raw_material_util_object: MaterialData, epicor_part: Union[Part, None]) -> str:
        """
        - Attempts to assign unit of measure from P3L variable on the operation
        - If no P3L var value is returned, assigns it to whatever is on the Epicor part master record
        - If no epicor part record, default is set to "EA"
        """
        logger.info("Attempting to get cost unit of measure")
        material_op = raw_material_util_object.material_op
        unit_of_measure = material_op.get_variable(self._exporter.erp_config.pp_mat_UOMCode_variable)
        if not unit_of_measure:
            if not epicor_part:
                return "EA"
            return epicor_part.IUM
        return str(unit_of_measure)

    def _get_material_operation_notes(self, raw_material_util_object: MaterialData) -> str:
        """
        Gets Paperless Parts material operation notes so that they can be assigned to the Epicor Quote
        """
        logger.info("Attempting to get material operation notes")
        pp_mat_op = raw_material_util_object.material_op
        if not self._exporter.erp_config.write_material_operation_notes_to_purchasing_comments:
            return ""
        return str(pp_mat_op.notes)

    def _get_purchased_component_notes(self, pc_util_object: PurchasedComponentData) -> str:
        logger.info("Attempting to get purchased component notes")
        if not self._exporter.erp_config.write_pc_part_description_to_purchasing_comments:
            return ""
        return str(pc_util_object.component_data.part_description)

    def _get_purchased_component_unit_cost(self, part_data: ItemData):
        """
        Returns piece price from standard PC Piece Price op that is created by default on customers accounts.
        """
        logger.info("Attempting to get purchased component unit price")
        unit_cost = part_data.unit_price
        component = part_data.component
        for op in component.shop_operations:
            if op.operation_definition_name == self._exporter.erp_config.pp_purchased_component_op_def_name:
                p3l_piece_price = op.get_variable(
                    self._exporter.erp_config.pp_purchased_component_op_piece_price_var
                )
                if p3l_piece_price:
                    return p3l_piece_price
            return float(component.purchased_component.piece_price.raw_amount)
        return unit_cost

    def _get_est_scrap_percentage(self, pc_util_object: PurchasedComponentData):
        """
        - Compares the selected quantity field preference as indicated in the standard PC operation to the deliver qty
        - If deliver qty matches the op variable quantity, scrap = 0%
        - If deliver qty does not match, the difference is used to determine the scrap % and scrap % is returned
        - NOTE: Assumes the first operation is the standard PC operation
        """
        logger.info("Attempting to get purchased component scrap percentage.")
        purchased_component = pc_util_object.component_data.component
        pc_operation = None
        if purchased_component.material_operations:
            pc_operation = purchased_component.material_operations[0]
        elif purchased_component.shop_operations:
            pc_operation = purchased_component.shop_operations[0]
        if pc_operation:
            pc_op_quantity = pc_operation.get_variable("integration_quantity")
            if pc_op_quantity and pc_op_quantity != purchased_component.deliver_quantity:
                deliver_qty = purchased_component.deliver_quantity
                scrap_pct = ((pc_op_quantity - deliver_qty) / deliver_qty) * 100
                return scrap_pct
        logger.info("No material operation values present, or scrap percentage is calculated as 0.")
        return 0

    def get_component(self, comp_id: int, order_item: OrderItem) -> OrderComponent:
        for comp in order_item.components:
            if comp.id == comp_id:
                return comp
        logger.error(f"Could not find component: {comp_id} in the node tree.")

    def _get_material_operation_supplier_id(self, raw_material_util_object: MaterialData):
        pp_material_op = raw_material_util_object.material_op
        logger.info(f"Attempting to get material supplier ID from operation: {pp_material_op.name}")
        supplier_id = pp_material_op.get_variable(self._exporter.erp_config.pp_mat_op_vendor_num)
        if supplier_id:
            try:
                epicor_vendor: Vendor = Vendor.get_by_id(supplier_id)
                return epicor_vendor.VendorNum, epicor_vendor.VendorID
            except EpicorNotFoundException:
                logger.info("Could not assign vendor.")
        return None, None

    def _get_lead_time(self, raw_material_util_object: MaterialData):
        pp_material_op = raw_material_util_object.material_op
        logger.info(f"Attempting to get material lead time for operation: {pp_material_op.name}")
        lead_days = pp_material_op.get_variable(self._exporter.erp_config.pp_mat_op_lead_time)
        if lead_days:
            return int(lead_days)
        return 0

    @classmethod
    def _get_purchase_direct(cls, part_data: ItemData):
        if not part_data.epicor_part_record:
            return False
        return not part_data.part_record_exists

    def _get_fixed_qty_boolean_from_pp_operation(self, pp_material_op: OrderOperation) -> bool:
        fixed_quantity = pp_material_op.get_variable('is_fixed_quantity')
        if fixed_quantity is not None and fixed_quantity.upper() == "TRUE":
            return True
        return False

    def _add_to_created_materials_dict(self, quote_material: QuoteMaterial, node: TreeNode):
        if node.part_number not in self.created_material.keys():
            self.created_material[node.part_number] = []
        self.created_material[node.part_number].append(quote_material)

    def _get_integration_report_message(self):
        message = ""
        part_number: str
        for part_number in self.created_material.keys():
            mat_for_part_str = [x.PartNum for x in self.created_material[part_number]]
            message += f'Part {part_number}: {mat_for_part_str}\n'

        return message
