from typing import List, Optional, Union

from baseintegration.exporter.processor import BaseProcessor
from baseintegration.datamigration import logger
from baseintegration.utils import safe_get

from paperless.objects.orders import Order, OrderItem, OrderComponent, OrderOperation

from sage.models.sage_models.part import PartFullEntity, Product, ProductSiteTotals
from sage.models.converters.part_export import PaperlessOrderItemToSageProductsConverter


from sage.sage_api.client import SageImportClient
from sage.sage_api.filter_generation.part_filter_generator import PartFilterGenerator
from sage.utils import ItemData, PurchasedComponentData, LineItemData


class PartProcessor(BaseProcessor):

    def _process(self, order: Order) -> List[LineItemData]:
        self.client = SageImportClient.get_instance()
        logger.info("Processing all items -- manufactured components, purchased components, and raw materials\n")
        self.order = order
        self.line_items = []
        self.all_line_item_part_numbers = []

        for i, item in enumerate(order.order_items):
            new_line_item = self.get_parts_and_materials(item, i + 1)

            # removing non-existent manufactured items, not sure why this happens, some bug
            for part in new_line_item.manufactured_components:
                if not isinstance(part, ItemData):
                    new_line_item.manufactured_components.remove(part)
            self.line_items.append(new_line_item)

        self.log_all_line_items()

        return self.line_items

    def get_or_create_materials(self, item_data: ItemData, item: OrderItem, quote_line: int) \
            -> List[PartFullEntity]:
        materials = []
        for material_op in item_data.component.material_operations:
            part = self.create_default_raw_material_from_mat_op()
            self.client.create_part(part)
            materials.append(part)
        return materials

    def get_parts_and_materials(self, order_item: OrderItem, quote_line: int) -> LineItemData:
        manufactured_components: List[ItemData] = []
        purchased_components: List[PurchasedComponentData] = []
        materials: List[PartFullEntity] = []

        for component in order_item.components:
            logger.info(f"Processing {component.part_name}")

            # Skip hardware for later, skip root component (root comp. already created above)
            if component.is_hardware or component.is_root_component:
                continue

            part: ItemData = self.get_or_create_item(component, order_item, quote_line)
            logger.info(f"Part {part.part_number} is a manufactured component, going into mfg component list")
            manufactured_components.append(part)

            # add child purchased components to the list
            logger.info(f"Creating purchased components for {part.part_number}")
            logger.info(f"Part {part.part_number} is a manufactured component, going into mfg component list")
            purchased_components.extend(self.get_or_create_child_purchased_components(part, order_item, quote_line))

            # add materials to the list
            logger.info(f"Creating raw materials for {part.part_number}")
            logger.info(f"Part {part.part_number} is a manufactured component, going into mfg component list")
            materials.extend(self.get_or_create_materials(part, order_item, quote_line))

        # Clear the list of line item part numbers so that the same part numbers aren't de-duplicated across line items
        self.all_line_item_part_numbers.clear()

        return LineItemData(manufactured_components=manufactured_components, purchased_components=purchased_components,
                            materials=materials)

    def create_root_component_part(self, all_components, order_item: OrderItem, quote_line: int,
                                   manufactured_components: List[ItemData],
                                   purchased_components: List[PurchasedComponentData], materials: List[PartFullEntity]):
        # logger.info("Creating root component part.")
        for component in all_components:
            if component.is_root_component:
                part: ItemData = self.get_or_create_item(component, order_item, quote_line)
                # logger.info(f"Root component is going into mfg component list, part number: {part.part_number}")
                manufactured_components.append(part)

                # add sub-manufactured parts from root component
                # logger.info(f"Creating manufactured components for root component: {part.part_number}")
                manufactured_components.append(self.get_or_create_child_manufactured_components(part, order_item, quote_line))

                # add child purchased components to the list
                # logger.info(f"Creating purchased components for root component: {part.part_number}")
                purchased_components.extend(self.get_or_create_child_purchased_components(part, order_item, quote_line))

                # add materials to the list
                # logger.info(f"Creating raw materials for root component: {part.part_number}")
                materials.extend(self.get_or_create_materials(part, order_item, quote_line))

                return part
            continue

    def get_or_create_item(self, component: Union[OrderComponent, OrderOperation], order_item: OrderItem,
                           quote_line: int) -> ItemData:

        # if the component is an OrderOperation, get the part num and part name
        if isinstance(component, OrderOperation):
            part_number, part_name = self.get_part_number_and_name(component, self._exporter.erp_config.pp_mat_id_variable)
            logger.debug('component is order operation: ' + component.operation_definition_name)

        # if the component is hardware, get the part num and part name, and add to line item part nums
        elif component.is_hardware:
            self.all_line_item_part_numbers.append(component.part_number)
            part_number, part_name = self.get_part_number_and_name(component, self._exporter.erp_config.pp_mat_id_variable)
            logger.debug('component is hardware: ' + component.part_number)

        elif component.part_number not in self.all_line_item_part_numbers:
            self.all_line_item_part_numbers.append(component.part_number)
            part_number, part_name = self.get_part_number_and_name(component, self._exporter.erp_config.pp_mat_id_variable)
            # logger.debug('this part is not in the list so far, add it: ' + component.part_number)

        else:
            part_number, part_name = self.get_part_number_and_name(component,
                                                                   self._exporter.erp_config.pp_mat_id_variable)
            # Duplicate part numbers cause a circular reference error in Epicor
            # TODO: Make sure PCs aren't getting adjusted. Make sure child components get changed, not sub assm.
            # logger.debug('DE-DEPLUCATING?????')
            # part_number = self.de_duplicate_part_number(component.part_number)
            # part_name = component.part_name

        if part_number is None or part_number == "":
            part_number = str(self._exporter.erp_config.default_raw_material_id)
            logger.info(f"Part number is missing! Assigning default material: '{part_number}'")

        # logger.info(f"Attempting to GET part number {str(part_number)}")
        part = self.client.get_resource(PartFullEntity, PartFilterGenerator.get_filter_by_id(part_number), False)
        part_is_new = False

        # if part does not exist yet based on part number, create it in epicor
        if not part:
            logger.info(f"Part {str(part_number)} does not yet exist.")
            part_is_new = True
            if isinstance(component, OrderOperation):
                part = self.create_order_operation_part(part_number, part_name, component, order_item)
            else:
                part = self.create_order_component_part(part_number, part_name, component, order_item)
        unit_price = safe_get(part, "UnitPrice", default_value=0)
        part_class = safe_get(part, "ClassID", default_value=self._exporter.erp_config.default_manufactured_class_id)
        part_description = safe_get(part, "PartDescription", default_value="None")
        logger.info(f"Item {part_number} found, do not need to create a new item")
        # check if revision is here as component could potentially be an OrderOperation
        rev = self.get_or_create_part_rev(part, component)
        logger.info('\n')
        return ItemData(part_number=part_number, component=component, item_is_new=part_is_new,
                        unit_price=float(unit_price), revision=rev, part_class=part_class,
                        part_description=part_description, quote_line=quote_line, sage_part_record=part)

    def de_duplicate_part_number(self, original_part_number: str):
        """
        - Iterates until a unique part number + appended character + integer is found
        - Adds the unique part number to the array of unique part numbers
        """
        logger.info("Attempting to remove duplicate part number.")
        duplicate_count = 0
        while duplicate_count <= 99:
            duplicate_count += 1
            append_char = f"-{self._exporter.erp_config.duplicate_part_number_append_character}{duplicate_count}"
            new_part_number = f"{original_part_number}{append_char}"
            new_part_number = self.trim_part_number(new_part_number, append_char)
            if new_part_number not in self.all_line_item_part_numbers:
                self.all_line_item_part_numbers.append(new_part_number)
                return new_part_number

    def get_or_create_part_rev(self, part: PartFullEntity, order_component: Union[OrderComponent, OrderOperation]) -> \
            Union[str, None, ]:
        """
        Get the part Rev if exists
        :param order_component:
        :return:
        """
        logger.info("Attempting to get or create a part revision.")
        if isinstance(order_component, OrderComponent) and order_component.revision:
            # get part rev in pp vs sage
            part_rev_in_pp = str(order_component.revision[:12])
            part_rev_in_sage = self.get_part_revision_in_sage(part)

            # create revision if needed
            if part_rev_in_sage != part_rev_in_pp:
                self.create_part_revision_in_sage(part, part_rev_in_pp)
            return part_rev_in_pp

        logger.info("No revision number provided.")
        return None

    def get_or_create_child_purchased_components(self, parent_item_data: ItemData, order_item: OrderItem,
                                                 quote_line: int) \
            -> List[PurchasedComponentData]:
        purchased_components = []
        for child_id in parent_item_data.component.child_ids:
            # Get the child component by matching the child component ID
            child_component = [comp for comp in order_item.components if comp.id == child_id][0]

            if child_component.is_hardware:
                purchased_part: ItemData = self.get_or_create_item(child_component, order_item, quote_line)
                logger.info(f"Item {purchased_part.part_number} is a purchased component, going into purchased "
                            f"component list")
                purchased_component_data = PurchasedComponentData(component_data=purchased_part,
                                                                  parent_item_no=parent_item_data.part_number)
                purchased_components.append(purchased_component_data)
        return purchased_components

    def get_or_create_child_manufactured_components(self, parent_item_data: ItemData, order_item: OrderItem,
                                                    quote_line: int) -> List[ItemData]:
        manufactured_components = []
        for child_id in parent_item_data.component.child_ids:
            # Get the child component by matching the child component ID
            child_component = [comp for comp in order_item.components if comp.id == child_id][0]

            if child_component.type == "manufactured":
                manufactured_part: ItemData = self.get_or_create_item(child_component, order_item, quote_line)
                logger.info(f"Item {manufactured_part.part_number} is a manufactured part, going into manufactured "
                            f"component list")
                manufactured_components.append(manufactured_part)
        return manufactured_components

    def create_order_component_part(self, part_number: str, part_name: str, order_component, order_item: OrderItem) -> dict:
        part = PaperlessOrderItemToSageProductsConverter.to_sage_product(part_number, part_name, order_component, order_item)
        self.client.create_part(part)
        return part

    def get_part_number_and_name(self, component, pp_mat_id_variable: Optional[str] = None):
        # Could be either a component or operation - based on whether we're creating a component or material item
        if isinstance(component, OrderOperation) and pp_mat_id_variable is not None:
            logger.info("Getting part number out of material operation")
            part_number = component.get_variable(pp_mat_id_variable)
            part_name = part_number
        else:
            part_number = component.part_number.strip() if component.part_number is not None else None
            if not part_number:
                part_number = str(component.part_name)[0:50]
            part_name = component.part_name
        logger.info(f"Processing part with part number '{part_number}'")
        return part_number, part_name

    def get_part_revision_in_sage(self, part: PartFullEntity):
        part_in_sage = self.client.get_resource(PartFullEntity,
                                                PartFilterGenerator.get_filter_by_id(part.product.product_code), False)
        if part_in_sage is not None:
            return part_in_sage.product.revision_number
        return None

    def create_part_revision_in_sage(self, part: PartFullEntity, part_rev: str):
        product = part.product
        product.revision_number = part_rev
        part.product = product
        self.client.create_part(part)

    def trim_part_number(self, part_number: str, appended_string: str):
        """
        - Trims the part number to the allowed max length of 50 characters, in the event that the appended string
        causes the part number to go over Epicor's limit.
        - This function will only be called in the event that a duplicate part number is identified.
        """
        logger.info("Checking for valid part number length.")
        if not len(part_number) <= 50:
            logger.info(f"Part number: {part_number} exceeds character limit. Cutting.")
            part_number = f"{part_number[:(50 - len(appended_string))]}{appended_string}"

        return part_number

    def log_all_line_items(self):
        logger.error('<=================== all thats being returned ==============>')
        for item in self.line_items:

            logger.error('manufactured:')
            for manufactured_comp in item.manufactured_components:
                logger.error(manufactured_comp.sage_part_record.product.product_category + '-' + manufactured_comp.part_number)

            logger.error('purchased:')
            for purchased_comp in item.purchased_components:
                logger.error(purchased_comp.component_data.part_number)

            logger.error('material:')
            for mat in item.materials:
                logger.error(mat.product.product_code)

    def create_default_raw_material_from_mat_op(self):
        product = Product()
        product.product_code = 'default-material'
        product.description = 'default material from material operation'
        product.product_category = 'RML'
        prod_site_totals = ProductSiteTotals()
        return PartFullEntity(
            product=product,
            prod_site_totals=prod_site_totals
        )
