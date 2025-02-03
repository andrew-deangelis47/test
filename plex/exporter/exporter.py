import re

from baseintegration.exporter.order_exporter import OrderExporter
from paperless.objects.orders import Order, OrderComponent, OrderOperation, OrderItem
from baseintegration.datamigration import logger
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from plex.exporter.processors.part import PartProcessor
from plex.exporter.processors.operation import OperationProcessor
from plex.exporter.processors.customer import CustomerProcessor, CustomerAddressProcessor, CustomerPartProcessor, CustomerContactProcessor
from plex.exporter.processors.sales_order_tier_2 import SalesOrderTier2LineProcessor
from plex.exporter.processors.work_centers import WorkCenterProcessorV2
from plex.exporter.processors.suppliers import SupplierProcessor
from plex.objects.work_center import ApprovedWorkcenter
from plex.objects.supplier import ApprovedSupplier
from plex.exporter.processors.sales_order import SalesOrderProcessor, SalesOrderLineProcessor, \
    SalesOrderReleaseProcessor
from plex.objects.part import Part
from plex.objects.routing import PartOperation
from paperless.custom_tables.custom_tables import CustomTable
from plex.objects.customer import Customer, CustomerPart, CustomerAddress, CustomerContacts
from plex.objects.sales_orders import SalesOrder, SalesOrderLine, SalesOrderRelease, SalesOrderLineDataSource
from plex.configuration import ERPConfigFactory
from plex.exceptions import PlexException, PlexValidationFailureException
from typing import List
from datetime import timedelta, timezone


class PlexOrderExporter(OrderExporter):

    def _register_default_processors(self):
        self.register_processor(Part, PartProcessor)
        self.register_processor(ApprovedWorkcenter, WorkCenterProcessorV2)
        self.register_processor(ApprovedSupplier, SupplierProcessor)
        self.register_processor(PartOperation, OperationProcessor)
        self.register_processor(Customer, CustomerProcessor)
        self.register_processor(CustomerAddress, CustomerAddressProcessor)
        self.register_processor(CustomerPart, CustomerPartProcessor)
        self.register_processor(CustomerContacts, CustomerContactProcessor)
        self.register_processor(SalesOrder, SalesOrderProcessor)
        self.register_processor(SalesOrderLine, SalesOrderLineProcessor)
        self.register_processor(SalesOrderRelease, SalesOrderReleaseProcessor)
        self.register_processor(SalesOrderLineDataSource, SalesOrderTier2LineProcessor)

    def _process_order(self, order: Order) -> bool:  # noqa: C901
        """
        This method exports Paperless Parts order to PLEX orders via a configuration setting we can choose which
        type of PLEX order to facilitate. Plex Part, BOM, ROUTER objects are created if needed to support
        the PLEX order.

        tier - This dictates what type of order we are try to facilitate in PLEX while export an a
        Paperless Parts order.  A 2 tier 2 order requires a data source endpoint since the PLEX rest api can
        only make tier 3 orders.  Tier 2 order can be made tier 3 order but tier 3 order cannot be made tier
        2 orders in PLEX.  Tier 2 orders allow for duplicate customer POs but tier 3 orders do not.

        :param order: This is the Paperless Parts object for the order to be exported
        :type order: Order object from PaperlessParts SDK
        :return: We tern True or False depending on export success
        :rtype: bool
        """
        try:
            tier = f'{self.erp_config.order_tier}'
            if order.payment_details.payment_type == 'credit_card':
                logger.warn('Received an order paid by credit card. Aborting gracefully.')
                raise CancelledIntegrationActionException
            if order.contact.account is None:
                logger.warn('Received an order without an account. Aborting gracefully.')
                raise CancelledIntegrationActionException
            quote_number_with_revision = \
                f'{order.quote_number}{f"-{order.quote_revision_number}" if order.quote_revision_number is not None else ""} '
            operations_mapping = []
            if self.erp_config.operation_code_map_table is not None:
                operations_mapping_table: dict = CustomTable.get(self.erp_config.operation_code_map_table)
                operations_mapping = operations_mapping_table.get('rows', [])

            with self.process_resource(
                    Customer,
                    order.contact.account,
                    order.billing_info,
                    order.shipping_info,
                    create=self.erp_config.can_creat_new_customers,
            ) as customer:
                if customer is None:
                    logger.warn('We were unable to get and/or create a customer in PLEX. Aborting gracefully.')
                    return False
                with self.process_resource(
                    CustomerContacts,
                    customer,
                    order.contact,
                    create=self.erp_config.can_creat_new_customers,
                ):
                    pass
                with self.process_resource(
                        CustomerAddress,
                        customer,
                        order.billing_info,
                        ['billTo', 'remitTo', 'soldTo'],
                        'Billing',
                        create=True,
                ) as billing_address, self.process_resource(
                    CustomerAddress,
                    customer,
                    order.shipping_info,
                    ['shipTo'],
                    'Shipping',
                    billing_address_id=billing_address.id if billing_address is not None else None,
                    create=True,
                ) as shipping_address:

                    if shipping_address is None:
                        logger.warn(f'Shipping information is not filled out for order {order.number}. '
                                    f'Skipping processing for this order.')
                        raise CancelledIntegrationActionException

                    if billing_address is None:
                        logger.warn(f'Billing information is not filled out for order {order.number}. '
                                    f'Billing processing for this order.')
                        raise CancelledIntegrationActionException
                    with self.process_resource(
                            SalesOrder,
                            order,
                            order.payment_details,
                            billing_address.code if billing_address is not None else '',
                            shipping_address.code if shipping_address is not None else '',
                            customer,
                            quote_number_with_revision,
                            tier,
                            create=False,
                    ) as sales_order:

                        order_was_new = not sales_order.is_created()
                        # TODO: This logic may not always be what we want, because
                        # one PO could span multiple orders. We need to do a
                        #  comparison of the contents of the order lines, similar
                        #  to customer addresses
                        if order_was_new:
                            so_result = sales_order.create()
                            if isinstance(so_result, str) and so_result == "Invalid Inside Sales.":
                                sales_order.Inside_Sales = self.erp_config.default_sales_person.upper()
                                so_result = sales_order.create()
                            elif isinstance(sales_order, str):
                                logger.error(f'Could not create Sales Order with '
                                             f'PO #{order.payment_details.purchase_order_number} for '
                                             f'order {order.number} get this error {so_result}')
                                return False
                            sales_order = so_result
                        else:
                            logger.warn(
                                f'Customer PO with PO #{order.payment_details.purchase_order_number} already exists. '
                                f'Sales order lines from this order will not be created.')

                        for order_item in order.order_items:
                            logger.info('Processing the part tree')
                            part = self._process_part_tree_rec(
                                order_item.root_component,
                                order_item.components,
                                operations_mapping,
                                quote_number_with_revision,
                                order_item
                            )
                            if order_was_new:
                                if tier == '2':
                                    with self.process_resource(CustomerPart, part, customer) \
                                            as customer_part, self.process_resource(
                                        SalesOrderLineDataSource,
                                        order_item,
                                        part,
                                        customer_part,
                                        sales_order,
                                        (order_item.ships_on_dt + timedelta(hours=23, minutes=59, seconds=59))
                                                .replace(tzinfo=timezone(timedelta())).isoformat(),
                                        customer
                                    ):
                                        pass
                                else:
                                    with self.process_resource(CustomerPart, part, customer) \
                                            as customer_part, self.process_resource(
                                        SalesOrderLine,
                                        order_item,
                                        part,
                                        customer_part,
                                        sales_order,
                                        create=True,
                                    ) as order_line:
                                        with self.process_resource(
                                                SalesOrderRelease,
                                                order_item.quantity,
                                                shipping_address.id if shipping_address is not None else None,
                                                (order_item.ships_on_dt + timedelta(hours=23, minutes=59,
                                                                                    seconds=59)).replace(
                                                    tzinfo=timezone(timedelta())).isoformat(),
                                                sales_order.id,
                                                order_line.id,
                                                create=True,
                                        ):
                                            pass
                logger.info(f'Processed order: {order.number}')
                return True
        except Exception as e:
            logger.exception(e)
        return False

    def _process_part_tree_rec(  # noqa: C901
            self,
            component: OrderComponent,
            all_components: List[OrderComponent],
            operations_mapping: list,
            quote_number_with_revision,
            order_item: OrderItem = None
    ) -> Part:
        """
        Recursively processes a part tree, completing the following steps:
        1. Traverse component tree based on assembly structure in Paperless
        2. Create uncreated parts and add their process routings
        3. For all parts that were created in step 2, add BOM entries to the relevant operations
        :param component: The root component of the tree
        :param all_components: All components in the order item
        :param operations_mapping: The Operations Mapping custom table that controls how operations map from
          Paperless to Plex
        """

        ops = component.shop_operations
        m_ops = component.material_operations
        c_m_ops = []
        child_part_quantities = []
        bom_depletion_unit_type = self.erp_config.default_bom_depletion_unit_type
        bom_depletion_conversion_factor = self.erp_config.default_bom_depletion_conversion_factor

        for child in component.children:
            qty = child.quantity
            child_component = [c for c in all_components if c.id == child.child_id][0]
            # TODO: Make a distinction between purchased and manufactured components here so that the
            #  part type is set correctly
            child_part = self._process_part_tree_rec(
                child_component,
                all_components,
                operations_mapping,
                quote_number_with_revision
            )
            if child_part and isinstance(child_part, Part):
                continue
            child_part_quantities.append((child_part, qty))

        for material in m_ops:
            material_search_var = self.erp_config.costing_variable_material_search
            material_search = material.get_variable_obj(material_search_var)
            if material_search and material_search.row:
                column_name = self.erp_config.material_table_part_number_header
                material_part_number = material_search.row.get(column_name)
                material_parts = Part.find_part(number=material_part_number)
                material_qty = 1
                for variable in material.costing_variables:
                    if 'Parts Per' in variable.label and variable.value is not None and variable.value != 0.:
                        material_qty = 1 / variable.value
                if len(material_parts) > 0:
                    child_part_quantities.append((material_parts[0], material_qty))
        for op in ops:
            if (op.name and self.erp_config.powder_op_sub_string in op.name) \
                    or (op.operation_definition_name and self.erp_config.powder_op_sub_string
                        in op.operation_definition_name):
                var_obj = op.get_variable_obj('Powder Coat Selection')
                if var_obj and var_obj.row:
                    power_part_number = var_obj.row.get('PartNo')
                    powered_qty = op.get_variable('Powder Usage, lbs') / component.deliver_quantity
                    powder_parts = Part.find_part(number=power_part_number)
                    if len(powder_parts) > 0:
                        child_part_quantities.append((powder_parts[0], powered_qty))
        lead_days = 0
        if order_item:
            lead_days = order_item.lead_days
        with self.process_resource(Part, component, quote_number_with_revision, False, lead_days) as part:
            if (not part.is_created() and not part.is_new_rev()) or (not part.is_created() and part.is_new_rev()):
                for child_part, qty in child_part_quantities:
                    part.add_child_component(part=child_part,
                                             quantity=qty,
                                             depletion_units=bom_depletion_unit_type,
                                             depletion_conversion_factor=bom_depletion_conversion_factor)
                try:
                    created_part = part.create()
                except PlexValidationFailureException as e:
                    logger.warn(f'One or more part information variables did not pass validation, falling back to '
                                f'default values...: {e}')
                    message = f'{e.message}'.lower()
                    if '"field":"type' in message:
                        part.type = self.erp_config.default_part_type
                    if '"field":"producttype' in message:
                        part.productType = self.erp_config.default_product_type
                    if '"field":"group' in message:
                        part.group = self.erp_config.default_part_group
                    if '"field":"status' in message:
                        part.status = self.erp_config.default_part_status
                    if '"field":"buildingcode' in message:
                        part.buildingCode = self.erp_config.default_part_building_code
                    if '"field":"source' in message:
                        part.source = self.erp_config.default_part_source
                    created_part = part.create()

                routing_steps = []
                idx = 1
                multi_op_indices = {}
                parser = self._integration.config_yaml.get("Exporters", {}).get("orders", {})
                excluded_operations = parser.get('excluded_operations', [])
                hardware_ops: dict = {}

                for op in ops:
                    if op.name in excluded_operations \
                            or op.operation_definition_name in excluded_operations:
                        continue
                    try:
                        with self.process_resource(
                                PartOperation,
                                op,
                                operations_mapping,
                                created_part.id,
                                idx,
                                multi_op_indices,
                                create=True,
                        ) as part_op:
                            if part_op is not None:
                                if (op.name and self.erp_config.powder_op_sub_string in op.name) \
                                        or (op.operation_definition_name and self.erp_config.powder_op_sub_string
                                            in op.operation_definition_name):
                                    var_obj = op.get_variable_obj('Powder Coat Selection')
                                    if var_obj and var_obj.row:
                                        power_part_number = var_obj.row.get('Part_No')
                                        hardware_ops[power_part_number] = part_op.id
                                routing_steps.append(part_op)
                                idx += 1
                                with self.process_resource(ApprovedWorkcenter,
                                                           op,
                                                           part_op,
                                                           created_part
                                                           ):
                                    pass
                                with self.process_resource(ApprovedSupplier,
                                                           op,
                                                           part_op,
                                                           created_part
                                                           ):
                                    pass
                    except PlexException:
                        logger.exception('An exception was caught with create a PLEX operation.  Moving on ...')

                # If there are children, attach bom
                if len(child_part_quantities) > 0 and len(routing_steps) > 0:
                    routing_step_id = routing_steps[0].id
                    for c_m_op in c_m_ops:
                        material_part_number = c_m_op.name.split(' | ')
                        if material_part_number[1]:
                            hardware_ops[material_part_number[1]] = routing_step_id
                    for routing_step in routing_steps:
                        bom_id = 0
                        if created_part.bill_of_materials.part_quantities:
                            for bom in created_part.bill_of_materials.part_quantities:
                                if bom[0].number and bom[0].number in hardware_ops.keys():
                                    new = (bom[0], bom[1], hardware_ops[bom[0].number], bom[3], bom[4])
                                    created_part.bill_of_materials.part_quantities[bom_id] = new
                                bom_id += 1

                        if any(substring in routing_step.operation.code
                               for substring in self.erp_config.children_go_to_op):
                            routing_step_id = routing_step.id
                            break
                    created_part.create_component_bom(routing_step_id)
                    return created_part

                    # if here, it means that no suitable operation code was found
                    if not part.bill_of_materials.is_created():
                        # TODO: Maybe there should be some rollback procedure here
                        logger.warn('Could not create BOM.')
                return created_part
            else:
                return part

    def _setup_erp_config(self):
        logger.info("setting up erp config")
        self.erp_config, self.plex_client = ERPConfigFactory.create_config(self._integration)

    @staticmethod
    def is_excluded_operation(op: OrderOperation, excluded_operations: list) -> bool:
        for string in excluded_operations:
            found_by_name = re.search(string, op.name, re.IGNORECASE)
            found_by_definition = re.search(string, op.operation_definition_name, re.IGNORECASE)
            if found_by_name is not None or found_by_definition is not None:
                return True
        return False
