from baseintegration.utils.operations import OperationUtils
from paperless.objects.components import AssemblyComponent
from typing import List
from paperless.objects.orders import OrderComponent, OrderItem
from plex_v2.configuration import PlexConfig
from plex_v2.objects.bom import BOMComponent
from baseintegration.datamigration import logger
from plex_v2.objects.part import Part
from plex_v2.objects.component_pairing import PPComponentPlexComponentPairings
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from plex_v2.objects.sales_orders import SalesOrder, SalesOrder2Tier
from typing import Union
from plex_v2.objects.customer import Customer, CustomerAddress, CustomerPart
from paperless.objects.orders import Order, OrderOperation, OrderAccount
from plex_v2.objects.routing import PartOperation
from plex_v2.objects.operations_mapping import OperationsMapping, OperationMapping
from paperless.objects.address import AddressInfo
from plex_v2.objects.customer import CustomerContact


class ExportUtils:

    config: PlexConfig
    operation_utils: OperationUtils

    def __init__(self, config: PlexConfig, utils: OperationUtils):
        self.config = config
        self.operation_utils = utils

    # ------------------- Part Functions -------------------

    def get_plex_part_number_of_pp_component(self, component: OrderComponent) -> str:
        # return part no if exists
        if component.part_number is not None:
            return component.part_number

        # otherwise return massaged part name
        return component.part_name.rsplit('.', 1)[0]

    def is_new_rev_of_old_material_part(self, material_operation: OrderOperation):
        """
        if the part exists and the rev is different than what is existing in plex return True
        """

        # get number and rev
        part_number = self.operation_utils.get_variable_value_from_operation(
            material_operation,
            self.config.var_material_part_number
        )

        revision = self.get_plex_revision_from_material_operation(material_operation)

        existing_plex_materials_by_part_no: List[Part] = Part.search(number=part_number)

        # if no matching material by part number, return False
        if len(existing_plex_materials_by_part_no) == 0:
            return False

        # otherwise we know we have at least one part no match, search for a similar revision
        existing_plex_material: Part
        new_rev_of_existing_part = True
        for existing_plex_material in existing_plex_materials_by_part_no:
            if revision == existing_plex_material.revision:
                new_rev_of_existing_part = False

        return new_rev_of_existing_part

    def is_new_rev_of_old_part(self, component: OrderComponent):
        """
        if the part exists and the rev is different than what is existing in plex return True
        """

        part_num = component.part_number
        revision = self.get_plex_part_revision_from_paperless_component(component)

        # if there is no part num this is a problem, throw exception
        if part_num is None:
            raise CancelledIntegrationActionException(f'Unexpected null value for part number found. Please enter a part number where missing. Part name is "{component.part_name}"')

        existing_part: Part
        existing_parts_by_number: List[Part] = Part.search(number=part_num)
        for part in existing_parts_by_number:
            if part.revision != revision:
                return True

        return False

    def get_top_level_part_from_order_item(self, order_item: OrderItem):
        component: AssemblyComponent
        components: List[AssemblyComponent] = order_item.iterate_assembly()
        for component in components:
            order_component: OrderComponent = component.component
            if order_component.is_root_component:
                return order_component

        raise CancelledIntegrationActionException('Could not find top level part for order item')

    def does_material_exist(self, material_operation: OrderOperation) -> tuple:
        # get number and rev
        part_number = self.operation_utils.get_variable_value_from_operation(
            material_operation,
            self.config.var_material_part_number
        )

        revision = self.get_plex_revision_from_material_operation(material_operation)

        # match on number first, revision gets messy if we pass empty string in as filter
        parts = Part.search(number=part_number)

        # if we can match on revision then we know it's a match (need to check both uppercase and lowercase)
        part: Part
        for part in parts:
            if part.revision.lower() == revision.lower():
                return True, part

        return False, None

    def does_part_exist(self, component: OrderComponent) -> tuple:
        """
        - This function is intentionally very simple
        - If you need to check if the part exists just by part number, or
        any other way besides part number and revision, ovveride this function

        Returns if the part exists, and if it does exist is returns the part

        Note: Plex part numbers and revisions are not case-specific
        example: "PartA" = "Parta"
        """
        part_number = component.part_number
        revision = self.get_plex_part_revision_from_paperless_component(component)

        # match on number first, revision gets messy if we pass empty string in as filter
        parts = Part.search(number=part_number)

        # if we can match on revision then we know it's a match (need to check both uppercase and lowercase)
        part: Part
        for part in parts:
            if part.revision.lower() == revision.lower():
                return True, part

        return False, None

    def _get_plex_part_revision_from_paperless_hardware_component(self, component: OrderComponent) -> str:
        # if there is a rev on the component then use that
        if component.revision is not None and component.revision != "":
            return component.revision

        # otherwise check if there is a revision on the purchased components table
        rev = component.purchased_component.get_property('revision')
        if rev is None:
            return ''

        return rev

    def get_plex_revision_from_material_operation(self, operation: OrderOperation) -> str:
        revision = ""
        try:
            revision = self.operation_utils.get_variable_value_from_operation(
                operation,
                self.config.var_material_part_revision
            )
        except CancelledIntegrationActionException as e:
            logger.info(str(e))

        return revision

    def get_plex_part_revision_from_paperless_component(self, component: OrderComponent) -> str:
        # if it's hardware then we may need to check the PC table for rev
        if component.is_hardware:
            return self._get_plex_part_revision_from_paperless_hardware_component(component)[:8]

        """
        if None then return True
        """

        if component.revision is None:
            return ''

        return component.revision[:8]

    def get_plex_part_from_paperless_component(self, component: OrderComponent) -> Part:
        # get the part
        does_exist, plex_part = self.does_part_exist(component)

        if does_exist:
            return plex_part

        raise CancelledIntegrationActionException(
            f'Part not found in Plex: number="{component.part_number}", revision={self.get_plex_part_revision_from_paperless_component(component)}'
        )

    def get_customer_part_if_exists(self, part: Part, customer: Customer) -> Union[CustomerPart, None]:
        matching_customer_parts: List[CustomerPart] = CustomerPart.find_customer_parts(
            number=part.number,
            partId=part.id,
            customerId=customer.id
        )

        if len(matching_customer_parts) == 0:
            return None

        # plex API is bad, let's make sure it's actually a match
        customer_part: CustomerPart
        for customer_part in matching_customer_parts:
            if customer_part.number == part.number and \
               customer_part.partId == part.id and \
               customer_part.customerId == customer.id:
                return customer_part

        return None

    # ------------------- BOM Functions -------------------

    def get_first_plex_part_op_for_plex_part(self, plex_part: Part) -> PartOperation:
        """
        returns the plex op id of the first operation for this component (plex part op id, not plex op id)
        """

        # grab all the plex ops for this component
        plex_part_operations = PartOperation.search(partId=plex_part.id)

        # get the first pp op
        if len(plex_part_operations) == 0:
            raise CancelledIntegrationActionException(f'Unable to find any operations in plex for part "{plex_part.number}" while attempting to create bom component')

        return plex_part_operations[0]

    def get_sub_components_of_order_component(self, order_component: OrderComponent, order_item: OrderItem) -> List[OrderComponent]:
        components = []
        for child in order_component.children:
            components.append(self.get_component_by_id(child.child_id, order_item))
        return components

    def get_bottom_level_of_order_item_bom(self, order_item: OrderItem) -> int:
        max = 0
        for comp in order_item.iterate_assembly():
            if comp.level > max:
                max = comp.level

        return max

    def get_assembly_components_for_level(self, order_item: OrderItem, level: int) -> List[AssemblyComponent]:
        comps_for_level = []
        comp: AssemblyComponent
        for comp in order_item.iterate_assembly():
            if comp.level == level:
                comps_for_level.append(comp)

        return comps_for_level

    def get_component_by_id(self, id: str, order_item: OrderItem) -> OrderComponent:
        for comp in order_item.iterate_assembly():
            if comp.component.id == id:
                return comp.component

    def does_bom_component_already_exist(self, plex_parent_component: Part, plex_child_component: Union[Part, OrderOperation]) -> bool:
        bom_comp_exists = False

        # if material op get the corresponding plex part
        if isinstance(plex_child_component, OrderOperation):
            plex_child_component = self.get_plex_material_from_material_op(plex_child_component)

        # get bom components with the parent part id
        existing_bom_components: BOMComponent = \
            BOMComponent.get_with_filters(partId=plex_parent_component.id)

        # iterate and check for the component part id
        existing_bom_component: BOMComponent
        for existing_bom_component in existing_bom_components:
            if existing_bom_component.componentId == plex_child_component.id:
                bom_comp_exists = True
                break

        if bom_comp_exists:
            logger.info(f'partId={plex_parent_component.id}, componentPartId={plex_child_component.id}')
            logger.info(f'Component part {plex_child_component.number} already exists'
                        f' on bom of {plex_parent_component.number}.')
            return True

        return False

    def get_plex_material_from_material_op(self, material_operation: OrderOperation) -> Part:
        # get the part number from the material op
        material_part_number = self.operation_utils.get_variable_value_from_operation(
            material_operation,
            self.config.var_material_part_number
        )

        material_part_revision = self.get_plex_revision_from_material_operation(material_operation)

        plex_material: List[Part] = Part.search(number=material_part_number, revision=material_part_revision)

        if len(plex_material) == 0:
            raise CancelledIntegrationActionException(
                f'Unable to find matching Plex material using part number "{material_part_number}".')

        return plex_material[0]

    def get_pp_to_plex_components_mapping(self, pp_sub_components: List[OrderComponent]) -> PPComponentPlexComponentPairings:
        """
        returns a list of tuples, one being the paperless component and one being the plex representation of that part
        helps with bom component creation because both the plex part and the pp part are required in the factory
        """
        pairings: PPComponentPlexComponentPairings = PPComponentPlexComponentPairings()
        pp_sub_component: OrderComponent
        for pp_sub_component in pp_sub_components:
            plex_sub_component = self.get_plex_part_from_paperless_component(pp_sub_component)
            pairings.add_pairing(pp_sub_component, plex_sub_component)

        return pairings

    # ------------------- Customer/Contacts Functions -------------------

    def get_existing_plex_contact_and_sort_order(self, order: Order, customer: Customer) -> tuple:
        max_sort_order_existing = 0
        order_contact = order.contact
        list_contacts: [CustomerContact] = CustomerContact.find_customer_contacts(customer_id=customer.id)
        plex_contact: CustomerContact
        for plex_contact in list_contacts:
            max_sort_order_existing = max(max_sort_order_existing, plex_contact.sortOrder)
            if plex_contact.email.lower().strip() == order_contact.email.lower().strip():
                return plex_contact, max_sort_order_existing

        return None, 0

    def get_plex_address_alt_code_from_address_info(self, address_info: AddressInfo, code_suffix: str) -> str:
        return f'{address_info.city}, {address_info.state} - {code_suffix}'

    def has_facility_name(self, address_info: AddressInfo) -> bool:
        return getattr(address_info, 'facility_name', None) and address_info.facility_name is not None and address_info.facility_name != ''

    def get_plex_customer_by_code_or_name(self, account: OrderAccount) -> Union[Customer, None]:
        # if code is not None we use that, otherwise use the name
        if account.erp_code is not None:
            existing_customers = Customer.find_customers(code=account.erp_code)
        else:
            existing_customers = Customer.find_customers(name=account.name)

        if len(existing_customers) == 0:
            return None

        return existing_customers[0]

    def get_existing_plex_address(self, customer: Customer, address_functions: list, code_suffix):
        for add_type in address_functions:
            address_functions_kwarg = {func: True for func in [add_type]}
            customer_addresses: List[CustomerAddress] = CustomerAddress.find_customer_addresses(
                **address_functions_kwarg,
                resource_name_kwargs={
                    'customer_id': customer.id})

            # if no address in PP or Plex fail the order
            if len(customer_addresses) == 0:
                raise CancelledIntegrationActionException(
                    f'No addresses were found in Plex for this customer and there is no {code_suffix} address on the order. Stopping export.')

            # log the address we are using
            logger.info(f'No {code_suffix} address on the Paperless Parts order. Using address {customer_addresses[0].code}')

            # get the right one based on shipping or billing
            customer_address: CustomerAddress
            if code_suffix == 'Shipping':
                for customer_address in customer_addresses:
                    if customer_address.shipTo:
                        return customer_address

                raise CancelledIntegrationActionException('Cannot get a valid shipping address in Plex for the customer on this order. Please add a valid shipping address for this customer in Plex.')

            elif code_suffix == 'Billing':
                for customer_address in customer_addresses:
                    if customer_address.billTo:
                        return customer_address

                raise CancelledIntegrationActionException('Cannot get a valid billing address in Plex for the customer on this order. Please add a valid billing address for this customer in Plex.')

            else:
                raise Exception(f'Unrecognized address code suffix when searching for plex addresses: "{code_suffix}"')

    def use_facility_name_to_get_address(self, customer: Customer, address_info: AddressInfo, address_functions: list, billing_address_id: str):

        logger.info(f'This address has a facility name, "{address_info.facility_name}"! '
                    f'Using this to match an address')
        addresses = CustomerAddress.find_customer_addresses(
            code=address_info.facility_name,
            billTo=None,
            remitTo=None,
            shipTo=None,
            soldTo=None,
            resource_name_kwargs={
                'customer_id': customer.id
            }
        )
        address: CustomerAddress = addresses[0] if len(addresses) > 0 else None
        if address is not None and address.code.lower() == address_info.facility_name.lower():
            if address.shipTo is False and 'shipTo' in address_functions:
                address.shipTo = True
                address.customerId = customer.id
                address.update()
            if address.billTo is False and 'billTo' in address_functions:
                address.billTo = True
                address.customerId = customer.id
                address.update()
            logger.info('Matching address with facility name found')
            return address
        else:
            logger.info('Matching address with facility name was not found, creating one')
            address = CustomerAddress(
                customerId=customer.id,
                active=True,  # Hopefully this can tell the engineers that they need to go modify the code here?
                code=address_info.facility_name,
                address=f'{address_info.address1} {address_info.address2}',
                city=address_info.city,
                state=address_info.state,
                zip=address_info.postal_code,
                country=address_info.country,
                phone=address_info.phone,
                billToAddressId=billing_address_id,
                billTo=True,
                remitTo=True,
                shipTo=True,
                soldTo=True
            )

            return address.create()

    def get_customer_address_by_alt_code(self, customer: Customer, alt_code: str):
        logger.info('No facility name found, Checking for paperless parts formatted address names')
        addresses = CustomerAddress.find_customer_addresses(
            code=alt_code,
            billTo=None,
            remitTo=None,
            shipTo=None,
            soldTo=None,
            resource_name_kwargs={
                'customer_id': customer.id
            }
        )
        address: CustomerAddress = addresses[0] if len(addresses) > 0 else None

        if address is not None:
            code: str = address.code
            if code.lower() == alt_code.lower():
                logger.info('Matching address with formatted address names found')
                return address

    def create_address_if_no_match(self, customer: Customer, address: CustomerAddress, address_functions_kwargs: list):
        matching_address = address.fuzzy_extract_matching_address(
            CustomerAddress.find_customer_addresses(**address_functions_kwargs, resource_name_kwargs={
                'customer_id': customer.id
            })
        )
        if matching_address is None:
            logger.info('Creating new address {}'.format(repr(address)))
            return address.create()
        elif matching_address is None:
            logger.info('Creating new address {}'.format(repr(address)))
            return address
        else:
            logger.info('Found fuzzy matching address for {}'.format(repr(address)))
            return matching_address

    # ------------------- Routing Functions -------------------

    def get_material_op_no(self, material_op: OrderOperation) -> int:
        """
        typically this would be the first op, but this allows for some custimization
        """
        return self.config.part_operation_increment_step

    def get_supplier_codes_from_material_op(self, material_operation: OrderOperation, plex_op_code: str, operations_mapping: OperationsMapping) -> Union[str, None]:
        # 1) first try to get it from the operation
        try:
            supplier_code: str = self.operation_utils.get_variable_value_from_operation(
                material_operation,
                self.config.supplier_code_var
            )
        except CancelledIntegrationActionException:
            supplier_code = None

        # 2) If we couldn't get it, fall back to the operations mapping table
        if supplier_code is None:
            supplier_codes: List[str] = operations_mapping.get_approved_supplier_codes_by_plex_op_code(plex_op_code)
            return supplier_codes

        return [supplier_code]

    def get_non_ignored_operations_for_component(self, component: OrderComponent) -> List[OrderOperation]:
        valid_ops: List[OrderOperation] = []
        op: OrderOperation
        for op in component.shop_operations:
            if op.operation_definition_name not in self.config.routing_operation_to_ignore:
                valid_ops.append(op)

        return valid_ops

    def get_ignored_operations_for_component(self, component: OrderComponent) -> List[OrderOperation]:
        valid_ops: List[OrderOperation] = []
        op: OrderOperation
        for op in component.shop_operations:
            if op.operation_definition_name not in self.config.routing_operation_to_ignore:
                valid_ops.append(op)

        return valid_ops

    def get_plex_operation_id_from_paperless_operation(self, paperless_op: OrderOperation, mappings: OperationsMapping) -> str:
        op_name = paperless_op.operation_definition_name

        mapping: OperationMapping
        for mapping in mappings.mappings:
            if mapping.pp_op_name == op_name:
                return mapping.plex_operation_id

        raise CancelledIntegrationActionException(f'Could not find Plex op id for Paperless operation "{op_name}. '
                                                  f'Please ensure the Operations_Mapping table exists and the '
                                                  f'corresponding operation exists in plex"')

    def get_plex_operation_code_from_paperless_operation(self, paperless_op: OrderOperation, mappings: OperationsMapping) -> str:
        # 1) first check if there is an op in this operation for the plex op code
        plex_op_code_var_value = self.operation_utils.get_variable_value_from_operation(
            paperless_op,
            self.config.plex_op_code_var,
            None
        )
        if plex_op_code_var_value is not None:
            return plex_op_code_var_value

        # 2) if not found then use the paperless op name and map to plex op code via the operations mapping table
        return mappings.get_plex_op_code_from_pp_op_using_mapping_table(paperless_op)

    def get_plex_part_ops_from_plex_part(self, plex_part: Part) -> PartOperation:
        """
        if we are using data sources to create part operations then we can't use the plex api to check if they exist
        """
        routing_lines = PartOperation.search(partId=plex_part.id)

        if len(routing_lines) == 0:
            raise CancelledIntegrationActionException(f'No routing found for plex part {plex_part.number} - needed for '
                                                      f'bom creation')

        return routing_lines

    # ------------------- Sales Order Functions -------------------

    def get_existing_sales_order_by_po_number_and_customer(self, po_number: str, customer: Customer) -> Union[SalesOrder]:
        existing_sales_order = None
        existing_sales_orders = SalesOrder.find_sales_orders(poNumber=po_number, customerId=customer.id)
        if len(existing_sales_orders) > 0:
            existing_sales_order = existing_sales_orders[0]

        return existing_sales_order

    def get_plex_shipping_address_from_sales_order(self, sales_order: Union[SalesOrder, SalesOrder2Tier]) -> Union[CustomerAddress, None]:
        # tier 3 sales order
        if isinstance(sales_order, SalesOrder):
            addresses_for_customer: List[CustomerAddress] = CustomerAddress.find_customer_addresses(resource_name_kwargs={'customer_id': sales_order.customerId})
            # match on id
            address: CustomerAddress
            for address in addresses_for_customer:
                if address.id == sales_order.shipToAddressId:
                    return address

        # tier 2 sales order
        else:
            # match on code
            addresses_for_customer: List[CustomerAddress] = CustomerAddress.find_customer_addresses(resource_name_kwargs={'customer_id': sales_order.customerId})
            address: CustomerAddress
            for address in addresses_for_customer:
                if address.code == sales_order.Ship_To_Customer_Address_Code:
                    return address

    def get_plex_billing_address_from_sales_order(self, sales_order: Union[SalesOrder, SalesOrder2Tier]) -> Union[CustomerAddress, None]:
        # tier 3 sales order
        if isinstance(sales_order, SalesOrder):
            addresses_for_customer: List[CustomerAddress] = CustomerAddress.find_customer_addresses(resource_name_kwargs={'customer_id': sales_order.customerId})
            # match on id
            address: CustomerAddress
            for address in addresses_for_customer:
                if address.id == sales_order.billToAddressId:
                    return address

        # tier 2 sales order
        else:
            # match on code
            addresses_for_customer: List[CustomerAddress] = CustomerAddress.find_customer_addresses(resource_name_kwargs={'customer_id': sales_order.customerId})
            address: CustomerAddress
            for address in addresses_for_customer:
                if address.code == sales_order.Bill_To_Customer_Address_Code:
                    return address

    def create_sales_order_if_not_already_exists(self, sales_order: Union[SalesOrder, SalesOrder2Tier], existing_sales_order: Union[None, SalesOrder, SalesOrder2Tier], pp_order: Order, po_number: str) -> [SalesOrder, SalesOrder2Tier]:
        if existing_sales_order is not None:
            logger.warn(
                f'Customer PO with PO #{po_number} already exists. '
                f'Sales order lines from this order will not be created.')
            return sales_order

        # create if it does not exist
        logger.info('Creating new customer PO with PO number {}'.format(po_number))
        so_result = sales_order.create()

        # handle invalid inside sales
        if isinstance(so_result, str) and so_result == "Invalid Inside Sales.":
            sales_order.Inside_Sales = self.erp_config.default_sales_person.upper()
            so_result = sales_order.create()

        # handle general issues with sales order creation
        elif isinstance(sales_order, str):
            raise CancelledIntegrationActionException(f'Could not create Sales Order with '
                                                      f'PO #{po_number} for '
                                                      f'order {pp_order.number} get this error {so_result}')

        return so_result
