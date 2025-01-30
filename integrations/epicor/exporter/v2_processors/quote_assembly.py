from typing import List
from epicor.quote import QuoteAssembly, QuoteHeader
from epicor.utils import QuoteHeaderData, ItemData
from epicor.utils import get_manufactured_components_by_line_number, get_item_data_by_component_id, \
    get_purchased_components_by_line_number
from epicor.utils import TreeNode, PurchasedComponentData
from baseintegration.datamigration import logger
from paperless.objects.orders import Order, OrderItem, OrderComponent
from typing import Union
from uuid import uuid4
from epicor.exporter.v2_processors.base import EpicorProcessor


class QuoteAssemblyProcessor(EpicorProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'quote_assemblies'

    def _process(self, order: Order, quote_header: QuoteHeader, quote_header_data: QuoteHeaderData
                 ) -> List[QuoteAssembly]:
        logger.info(f"Generating quote assembly structure for order number: {order.number}")

        try:
            self.line_items = quote_header_data.line_items

            for line_item_num, order_item in enumerate(order.order_items, start=1):
                self.node_list = []
                self.assembly_seq_num = 0
                self.line_item_mfg_components: List[ItemData] = \
                    get_manufactured_components_by_line_number(self.line_items, line_item_num)

                line_item_purchased_components: List[PurchasedComponentData] = get_purchased_components_by_line_number(
                    self.line_items, line_item_num)
                self.line_item_purchased_component_items: List[ItemData] = []
                for pc_object in line_item_purchased_components:
                    self.line_item_purchased_component_items.append(pc_object.component_data)

                for comp in order_item.components:
                    if comp.is_root_component:
                        self.iterate_child_components(quote_header, comp, order_item, line_item_num)
                    else:
                        continue

                # Find the existing line item data in the list of line item data objects, add the true assembly tree nodes
                line_item_data = self.line_items[line_item_num - 1]._replace(true_assembly_tree_nodes=self.node_list)
                # Replace the old line item data with the updated line item data that includes the true assembly tree
                self.line_items[line_item_num - 1] = line_item_data
        except Exception as e:
            logger.info(f'Error occured in QuoteAssemblyProcessor processor: {e}')
            self._add_report_message('Error occured while processor quote assembly. Please contact support.')
            raise e

        self._add_report_message('Succesfully processed quote assemblies.')
        return self.node_list

    def iterate_child_components(self, quote_header: QuoteHeader, this_comp: OrderComponent, order_item: OrderItem,
                                 line_item_num: int, parent_node: Union[TreeNode, None] = None,
                                 qty_per_parent: int = 1):

        parent_uuid = parent_node.component_instance_uuid if parent_node is not None else None
        parent_node = self.get_parent_node(parent_uuid)

        if this_comp.is_hardware:
            item_data = get_item_data_by_component_id(self.line_item_purchased_component_items, this_comp.id)
        else:
            # Get ItemData associated with this ID for normalized part numbers
            item_data = get_item_data_by_component_id(self.line_item_mfg_components, this_comp.id)
            if this_comp.is_root_component:
                self.get_root_component_quote_assembly(quote_header, line_item_num)
            else:
                self.create_quote_assembly(quote_header, parent_node, item_data, qty_per_parent)

        node = self.create_node(this_comp, item_data, parent_node, qty_per_parent, line_item_num)
        self.node_list.append(node)

        # Call function recursively for all child ids
        for child_id in this_comp.child_ids:
            qty_per_parent = self.get_child_quantity_per(this_comp.children, child_id)
            child_comp = self.get_component(child_id, order_item)
            self.iterate_child_components(quote_header, child_comp, order_item, line_item_num, node, qty_per_parent)

    def get_root_component_quote_assembly(self, quote_header: QuoteHeader, line_item_num: int)\
            -> Union[QuoteAssembly, None]:
        quote_assembly = None
        try:
            quote_assembly = QuoteAssembly.get_first({
                "Company": str(self._exporter.erp_config.company_name),
                "QuoteNum": int(quote_header.QuoteNum),
                "QuoteLine": int(line_item_num),
                "AssemblySeq": self.assembly_seq_num
            })
        except Exception as e:
            logger.info(f"Could not locate Epicor root QuoteAssembly component. \nError Message: {e}")
        return quote_assembly

    def create_quote_assembly(self, quote_header: QuoteHeader, parent_node: TreeNode, item_data: ItemData,
                              qty_per_parent: int) -> Union[QuoteAssembly, None]:
        quote_assembly = None
        self.assembly_seq_num += 1
        try:
            quote_assembly = QuoteAssembly(
                Company=str(self._exporter.erp_config.company_name),
                QuoteNum=int(quote_header.QuoteNum),  # PK to the quote header
                QuoteLine=int(parent_node.line_item_num),  # Quote detail line number, (not a zero based index)
                AssemblySeq=int(self.assembly_seq_num),
                BomLevel=int(parent_node.bom_level + 1),
                PartNum=item_data.part_number,
                RevisionNum=item_data.revision,
                Description="None",
                Template=bool(self._exporter.erp_config.should_mark_quote_lines_as_template),
                QtyPer=qty_per_parent,
                Parent=int(parent_node.assembly_seq_num),
                IUM="EA",
                ParentAssemblySeq=int(parent_node.assembly_seq_num),
                ParentPartNum=str(parent_node.part_number),
                ParentDescription=str(parent_node.part_description),
                ParentRevisionNum=str(parent_node.part_revision),
            )
            quote_assembly.create_instance()
        except Exception as e:
            logger.info(f"Could not post quote assembly component for unknown reasons. Part number: "
                        f"{item_data.part_number}\nError Message: {e}")
        return quote_assembly

    def get_parent_node(self, parent_uuid: uuid4) -> Union[TreeNode, None]:
        for node in self.node_list:
            if node.component_instance_uuid == parent_uuid:
                return node
        return None

    def get_child_quantity_per(self, child_quantities: list, child_id: int) -> int:
        for quantity in child_quantities:
            if quantity.child_id == child_id:
                return quantity.quantity
        return 1

    def get_component(self, comp_id: int, order_item: OrderItem) -> OrderComponent:
        for comp in order_item.components:
            if comp.id == comp_id:
                return comp
        logger.error(f"Could not find component: {comp_id} in the node tree.")

    def create_node(self, comp: OrderComponent, item_data: ItemData, parent_component_node: Union[TreeNode, None],
                    qty_per_parent: int, line_item_num: int) -> TreeNode:
        node = TreeNode(
            component_id=comp.id,
            component_instance_uuid=uuid4(),
            assembly_seq_num=self.assembly_seq_num,
            bom_level=parent_component_node.bom_level + 1 if parent_component_node else 0,
            parent_instance_uuid=parent_component_node.component_instance_uuid if parent_component_node else None,
            parent_id=parent_component_node.component_id if parent_component_node else None,
            quantity_per_parent=qty_per_parent,
            part_number=item_data.part_number,
            part_revision=item_data.revision,
            part_description=item_data.part_description,
            line_item_num=line_item_num,
        )
        return node
