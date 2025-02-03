from paperless.objects.orders import Order, OrderItem, OrderComponent, OrderOperation
from baseintegration.datamigration import logger
from baseintegration.utils import safe_get
from epicor.utils import QuoteHeaderData, LineItemData, ItemData, MaterialData, get_part_number_and_name, \
    PurchasedComponentData, CustomerData
from epicor.part import Part
from typing import Union, List, Optional, Tuple
from epicor.part import XRefPart
from epicor.exporter.v2_processors.base import EpicorProcessor


class PartProcessor(EpicorProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'parts'

    def _process(self, order: Order, customer: CustomerData) -> QuoteHeaderData:
        logger.info("Processing all items -- manufactured components, purchased components, and raw materials")
        try:
            self.customer_data: CustomerData = customer
            self.order = order
            self.line_items = []
            self.all_line_item_part_numbers = []
            self.created_parts: List[Part] = []
            self.existing_parts: List[Part] = []

            # for each order item, iterate through all components and create a part if necessary
            for i, item in enumerate(order.order_items):
                new_line_item = self.get_parts_and_materials(item, i + 1)
                self.line_items.append(new_line_item)

            quote_header_data = QuoteHeaderData(line_items=self.line_items)
            created_parts_list = [x.PartNum for x in self.created_parts]
            existing_parts_list = [x.PartNum for x in self.existing_parts]
            if len(self.created_parts) > 0:
                self._add_report_message(f'Created parts: {", ".join(created_parts_list)}')
            if len(self.existing_parts) > 0:
                self._add_report_message(f'Existing parts: {", ".join(existing_parts_list)}')
        except Exception as e:
            logger.info(f'Unexpected exception: {e}')
            created_parts_list = [x.PartNum for x in self.created_parts]
            existing_parts_list = [x.PartNum for x in self.existing_parts]
            self._add_report_message(f'Unexpected error occured. Only created the following parts: {", ".join(created_parts_list)}')
            self._add_report_message(f'Existing parts: {", ".join(existing_parts_list)}')
            raise e

        return quote_header_data

    def get_parts_and_materials(self, order_item: OrderItem, quote_line: int) -> LineItemData:
        manufactured_components: List[ItemData] = []
        purchased_components: List[PurchasedComponentData] = []
        materials: List[MaterialData] = []

        # Create root component first to ensure that the root part number isn't de-duplicated
        self.create_root_component_part(order_item.components, order_item, quote_line, manufactured_components,
                                        purchased_components, materials)

        for component in order_item.components:
            logger.info(f"Processing {component.part_name}")

            # Skip hardware for later, skip root component (root comp. already created above)
            if component.is_hardware or component.is_root_component:
                continue

            part: ItemData = self.get_or_create_item(component, order_item, quote_line)
            logger.info(f"Item {part.part_number} is a manufactured component, going into mfg component list")
            manufactured_components.append(part)

            # add child purchased components to the list
            logger.info(f"Creating purchased components for {part.part_number}")
            purchased_components.extend(self.get_or_create_child_purchased_components(part, order_item, quote_line))

            # add materials to the list
            logger.info(f"Creating raw materials for {part.part_number}")
            materials.extend(self.get_or_create_materials(part, order_item, quote_line))

        # Clear the list of line item part numbers so that the same part numbers aren't de-duplicated across line items
        self.all_line_item_part_numbers.clear()

        return LineItemData(manufactured_components=manufactured_components, purchased_components=purchased_components,
                            materials=materials)

    def create_root_component_part(self, all_components, order_item: OrderItem, quote_line: int,
                                   manufactured_components: List[ItemData],
                                   purchased_components: List[PurchasedComponentData], materials: List[MaterialData]):
        logger.info("Creating root component part.")
        for component in all_components:
            if component.is_root_component:
                part: ItemData = self.get_or_create_item(component, order_item, quote_line)
                logger.info(f"Root component is going into mfg component list, part number: {part.part_number}")
                manufactured_components.append(part)

                # add child purchased components to the list
                logger.info(f"Creating purchased components for root component: {part.part_number}")
                purchased_components.extend(self.get_or_create_child_purchased_components(part, order_item, quote_line))

                # add materials to the list
                logger.info(f"Creating raw materials for root component: {part.part_number}")
                materials.extend(self.get_or_create_materials(part, order_item, quote_line))

                return part
            continue

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

    def get_or_create_materials(self, item_data: ItemData, item: OrderItem, quote_line: int) \
            -> List[MaterialData]:
        materials = []
        for material_op in item_data.component.material_operations:
            if material_op.get_variable(self._exporter.erp_config.pp_mat_id_variable) is None:
                logger.info(f"No material lookup for {material_op.name}, this must be an informational operation")
                continue
            found_material: ItemData = self.get_or_create_item(material_op, item, quote_line)
            # swizzle in component rather than orderoperation
            found_material = found_material._replace(component=item_data.component)
            materials.append(MaterialData(part_data=found_material, material_op=material_op,
                                          parent_item_no=item_data.part_number))
        return materials

    def get_or_create_item(self, component: Union[OrderComponent, OrderOperation], order_item: OrderItem,
                           quote_line: int) -> ItemData:

        if isinstance(component, OrderOperation):
            part_number, part_name = get_part_number_and_name(component, self._exporter.erp_config.pp_mat_id_variable)
        elif component.is_hardware:
            self.all_line_item_part_numbers.append(component.part_number)
            part_number, part_name = get_part_number_and_name(component,
                                                              self._exporter.erp_config.pp_mat_id_variable)
        else:
            part_number = component.part_number
            part_name = component.part_name
            if part_number is None:
                part_number = part_name

            if part_number not in self.all_line_item_part_numbers:
                self.all_line_item_part_numbers.append(component.part_number)
                part_number, part_name = get_part_number_and_name(component,
                                                                  self._exporter.erp_config.pp_mat_id_variable)
            else:
                # Duplicate part numbers cause a circular reference error in Epicor. De-duplicate them
                part_number = self.de_duplicate_part_number(part_number)

        if part_number is None or part_number == "":
            part_number = str(self._exporter.erp_config.default_raw_material_id)
            logger.info(f"Part number is missing! Assigning default material: '{part_number}'")

        part_is_new = False
        part_record_exists = True
        part = self.get_existing_part_record(part_number)

        # if part does not exist yet based on part number, create it in epicor
        if not part:
            part, was_created = self.create_new_epicor_part(part_number, part_name, component, order_item)
            part_record_exists = was_created
            part_is_new = True
        else:
            self.existing_parts.append(part)

        # Set key attributes for ItemData util
        unit_price = self.get_part_unit_price(part, order_item, component)
        part_class = safe_get(part, "ClassID", default_value=self._exporter.erp_config.default_non_root_mfg_class_id)
        part_description = safe_get(part, "PartDescription", default_value="None")

        # check if revision is here as component could potentially be an OrderOperation
        rev = None
        if part:
            autoassign = self._exporter.erp_config.should_use_customer_part_numbers
            rev = None if autoassign else self.get_or_create_part_rev(part, component)
            # Store the system-assigned part number on the ItemData. ItemData is access by component ID later and
            # therefore stores the mapping of Paperless Parts part numbers to Epicor Customer Part Numbers (XRefPart)
            part_number = part.PartNum
        return ItemData(part_number=part_number, component=component, item_is_new=part_is_new,
                        unit_price=float(unit_price), revision=rev, part_class=part_class,
                        part_description=part_description, quote_line=quote_line, epicor_part_record=part,
                        part_record_exists=part_record_exists)

    def create_order_operation_part(self, part_number: str, part_name: str, material_op: OrderOperation,
                                    item: OrderItem) -> (Union[Part, None], bool):
        """
        Creates a Part from an order operation, returning the Part object and whether it was actually posted to
        Epicor.
        """
        if not self._exporter.erp_config.should_create_raw_materials:
            logger.info("Creation of raw materials is disabled! Attempting to assign default part number.")
            part_number = self._exporter.erp_config.default_raw_material_id
            part = Part.get(self._exporter.erp_config.company_name, part_number)
            if not part:
                logger.info(f"No default part exists in Epicor for part number: {part_number}")
            return part, bool(Part)
        logger.info(f"Assigning attributes from material operation for part number: {part_number}")
        description = self._get_material_op_notes(material_op)
        non_stock_item = self._get_material_op_non_stock(material_op)
        part_type = self._get_material_op_part_type(material_op)
        class_id = self._get_material_op_class_id(material_op)
        unit_price = self._get_material_op_unit_price(material_op)
        unit_of_measure, uom_class = self._get_material_op_unit_of_measure(material_op)
        cost_method = self._get_material_operation_cost_method(material_op)

        part_data = {
            "UnitPrice": unit_price,
            "PartNum": part_number,
            "PartDescription": description,
            "Company": self._exporter.erp_config.company_name,
            "ClassID": class_id,
            "ProdCode": self._exporter.erp_config.default_non_root_mfg_product_code,
            "IUM": unit_of_measure,
            "UOMClassID": uom_class,
            "PUM": unit_of_measure,
            "SalesUM": unit_of_measure,
            "CostMethod": cost_method,
        }
        if not self._exporter.erp_config.disable_part_creation:
            # these fields do not exist in the Part class
            part_data.update({
                "TypeCode": part_type,
                "UsePartRev": True,
                "NonStock": non_stock_item,
                "QtyBearing": True,
            })
            return Part.create(part_data), True
        return Part(**part_data), False

    def create_order_component_part(self, part_number: str, part_name: str, order_component, order_item: OrderItem) \
            -> (Part, bool):
        """
        Creates a Part from an order component, returning the Part object and whether it was actually posted to
        Epicor.
        """
        logger.info(f"Assigning attributes from OrderComponent for part number: {part_number}")
        description = self._get_part_description(part_name, order_component)
        non_stock_item = self._get_non_stock(order_component)
        part_type = self._get_part_type(order_component)
        class_id = self._get_class_id(order_component)
        unit_price = self._get_component_unit_price(order_item, order_component)
        cost_method = self._get_order_component_cost_method(order_component)
        product_code = self._get_product_code(order_component)

        part_data = {
            "UnitPrice": unit_price,
            "PartNum": part_number,
            "PartDescription": description,
            "Company": self._exporter.erp_config.company_name,
            "ClassID": class_id,
            "ProdCode": product_code,
            "CostMethod": cost_method,
        }

        if not self._exporter.erp_config.disable_part_creation:
            # these fields do not exist in the Part class
            part_data.update({
                "TypeCode": part_type,
                "UsePartRev": True,
                "NonStock": non_stock_item,
                "QtyBearing": True,
            })
            return Part.create(part_data), True

        # these are required in the Part class
        part_data.update({
            "IUM": "EA",
            "UOMClassID": "Count",
            "PUM": "EA",
            "SalesUM": "EA",
        })
        return Part(**part_data), False

    def get_or_create_part_rev(self, part: Part, order_component: Union[OrderComponent, OrderOperation]) -> \
            Union[str, None, ]:
        """
        Get the part Rev if exists
        :param order_component:
        :return:
        """
        logger.info("Attempting to get or create a part revision.")
        if isinstance(order_component, OrderComponent) and order_component.revision:
            rev = str(order_component.revision[:12])
            if self._exporter.erp_config.disable_part_creation:
                return rev
        else:
            logger.info("Using default part revision")
            rev = self._exporter.erp_config.default_part_revision
        part_rev = part.get_rev(rev)
        if part_rev or self._exporter.erp_config.disable_part_creation:
            return rev
        else:
            logger.info(f"Creating new revision {rev}")
            part_rev_object = part.create_new_part_rev(rev)
            return part_rev_object.RevisionNum

    def _get_material_op_unit_price(self, material_op: OrderOperation):
        """
        - Gets material cost from P3L var `pp_mat_cost_variable`
        - If variable value cannot be located, price is calculated as the operation total cost divided by the firt
        quantity break, (which should result in the highest unit cost)
        """
        op_var_unit_cost = material_op.get_variable(str(self._exporter.erp_config.pp_mat_cost_variable))
        if op_var_unit_cost is not None:
            return op_var_unit_cost
        return round(material_op.cost.raw_amount / material_op.quantities[0].quantity, 3)

    def _get_class_id(self, order_component: OrderComponent) -> str:
        if safe_get(order_component, 'is_hardware'):
            return str(self._exporter.erp_config.default_hardware_class_id)
        else:
            if safe_get(order_component, "is_root_component"):
                return str(self._exporter.erp_config.default_root_component_class_id)
            else:
                return str(self._exporter.erp_config.default_non_root_mfg_class_id)

    def _get_product_code(self, order_component: OrderComponent) -> str:
        if safe_get(order_component, 'is_hardware'):
            return str(self._exporter.erp_config.default_hardware_product_code)
        else:
            if safe_get(order_component, "is_root_component"):
                return str(self._exporter.erp_config.default_root_component_product_code)
            else:
                return str(self._exporter.erp_config.default_non_root_mfg_product_code)

    def _get_material_op_class_id(self, material_op: OrderOperation):
        """
        Placeholder method for future use. Override this function to implement custom logic for how to assign
        raw material class ids
        """
        return self._exporter.erp_config.default_raw_material_class_id

    def _get_part_description(self, part_name: str, order_component: OrderComponent) -> str:
        if safe_get(order_component, 'description'):
            return order_component.description
        return part_name

    def _get_material_op_notes(self, material_op: OrderOperation):
        """
        Attempts to get description from op var, if no op var, then material operation notes, then default
        """
        notes = material_op.get_variable(self._exporter.erp_config.pp_mat_description_variable)
        if notes:
            return notes
        notes = safe_get(material_op, "notes", None)
        if notes is not None:
            return notes
        return "No description"

    def _get_non_stock(self, order_component: OrderComponent) -> bool:
        """
        Get if this should be marked as a stock/nonstock part
        :param order_component:
        :return:
        """
        if safe_get(order_component, 'is_hardware'):
            return bool(self._exporter.erp_config.set_hardware_components_as_non_stock)
        else:
            return bool(self._exporter.erp_config.set_mfg_components_as_non_stock)

    def _get_material_op_non_stock(self, material_op: OrderOperation):
        """
        Placeholder for future use - default True for now under the assumption that if we're creating a new raw
        material record, it's not a stocked item, (otherwise it should already exist).
        """
        return True

    def _get_part_type(self, order_component: OrderComponent) -> str:
        # part type P denotes purchased, part type M denotes manufactured
        if safe_get(order_component, 'is_hardware'):
            return 'P'
        else:
            return 'M'

    def _get_material_op_part_type(self, material_op: OrderOperation) -> str:
        """
        Placeholder for future use. (Additional type codes include "K" - kit, and "B" - BOM planning.
        """
        return str(self._exporter.erp_config.material_op_default_part_type)

    def _get_material_op_unit_of_measure(self, material_op: OrderOperation):
        """
        Attempts to get the cost unit of measure from material operation variable.
        Attempts to assign a Cost UOM so that non "EA" units can be posted.
        NOTE: This may need config development to create the dictionary to map Class UIM IDs if this is user-defined.
        If the variable does not exist, default to "EA".
        """
        if self._exporter.erp_config.custom_uom_class_dict:
            uom_class_dict = self._exporter.erp_config.custom_uom_class_dict
        else:
            uom_class_dict = {
                "SI": "AREA",
                "EA": "Count",
                "IN": "Length",
                "POUNDS": "WEIGHT"
            }
        cost_uom_variable = str(self._exporter.erp_config.pp_mat_UOMCode_variable)
        if cost_uom_variable:
            cost_uom = material_op.get_variable(cost_uom_variable)
            uom_class = uom_class_dict.get(cost_uom, None)
            if cost_uom is not None and uom_class is not None:
                return cost_uom, uom_class
        return "EA", "Count"

    def _get_component_unit_price(self, order_item: OrderItem, component: OrderComponent):
        """
        - If root component: the unit price should be equivalent to the order item unit price for the finished good.
        - If purchased component: the unit price should be the unit price from the purchased component.
        - If manufactured component: Paperless doesn't have mid-level component pricing captured in the API...
        """
        if component.is_root_component:
            return float(order_item.unit_price.raw_amount)
        elif component.is_hardware:
            return float(component.purchased_component.piece_price.raw_amount)
        return 0

    def _get_order_component_cost_method(self, order_component: OrderComponent):
        if order_component.type == "purchased":
            return str(self._exporter.erp_config.default_purchased_comp_cost_method)
        else:
            return str(self._exporter.erp_config.default_manufactured_comp_cost_method)

    def _get_material_operation_cost_method(self, material_op: OrderOperation):
        return str(self._exporter.erp_config.default_material_op_cost_method)

    def get_existing_part_record(self, part_number) -> Optional[Part]:
        logger.info(f"***Attempting to GET part number {str(part_number)}")

        # Check for exact match of part number in epicor Part Master first:
        part = Part.get(self._exporter.erp_config.company_name, part_number)
        if part:
            return part
        # If part does not exist, attempt to find XRefPart (if config enabled)
        elif self._exporter.erp_config.should_use_customer_part_numbers is True:
            logger.info("***Looking for existing customer part number XRefPart")
            customer_part_number = XRefPart.get_first_x_ref_part(part_number)
            if customer_part_number:
                logger.info(f"Customer Part Number (XRefPart) exists. Original PN: {part_number}"
                            f" -> Epicor PN: {customer_part_number.PartNum}")
                part = Part.get(self._exporter.erp_config.company_name, customer_part_number.PartNum)
                return part
            logger.info(f"Epicor Part {part_number} does not exist. Returning None")
        return None

    def create_new_epicor_part(self, part_number: str, part_name: str, component: OrderComponent, order_item: OrderItem
                               ) -> Tuple[Optional[Part], bool]:
        logger.info(f"Part {str(part_number)} does not yet exist.")
        if isinstance(component, OrderOperation):
            part, was_created = self.create_order_operation_part(part_number, part_name, component, order_item)

        else:
            if self._exporter.erp_config.should_use_customer_part_numbers is True:
                logger.info("***Attempting to use customer part numbers.")
                part, was_created = self.create_new_auto_assigned_part_and_x_ref_part(
                    part_number, part_name, component, order_item)
            else:
                part, was_created = self.create_order_component_part(part_number, part_name, component, order_item)

        if was_created and part is not None:
            self.created_parts.append(part)
        elif part is not None:
            self.existing_parts.append(part)

        return part, was_created

    def create_new_auto_assigned_part_and_x_ref_part(self, part_number: str, part_name: str, component: OrderComponent,
                                                     order_item: OrderItem) -> Tuple[Optional[Part], bool]:
        logger.info("***Creating new auto-assigned part number")
        # Assign customer part number auto-assignment part number from config
        auto_assign_part_num = self._exporter.erp_config.customer_part_number_auto_assignment_default
        part, was_created = self.create_order_component_part(auto_assign_part_num, part_name, component,
                                                             order_item)
        logger.info(f"***Created part: {part.PartNum}")
        # Create the customer XRefPart to maintain Epicor's mapping of part numbers
        x_ref_part = self.create_x_ref_part(part, part_number, component.revision[:12] if component.revision else None)
        logger.info(f"Created XRefPart: {x_ref_part}")
        return part, was_created

    def create_x_ref_part(self, new_epicor_part: Part, part_number: str, revision: str = None) -> XRefPart:
        logger.info("***Creating customer part number!")
        x_ref_part = XRefPart(
            Company=self._exporter.erp_config.company_name,
            PartNum=new_epicor_part.PartNum,  # Part master part num (system assigned)
            XPartNum=self.trim_part_number(part_number, ''),  # Paperless/original part num
            XRevisionNum=revision,  # Paperless/original part rev
            CustNum=self.customer_data.customer.CustNum,
            CustNumCustID=self.customer_data.customer.CustID
        ).create_instance()
        return x_ref_part

    def get_part_unit_price(self, part, order_item: OrderItem, component: OrderComponent) -> float:
        if isinstance(component, OrderOperation):
            unit_price = safe_get(part, "UnitPrice", default_value=0)
        else:
            unit_price = self._get_component_unit_price(order_item, component)
        return float(unit_price)
