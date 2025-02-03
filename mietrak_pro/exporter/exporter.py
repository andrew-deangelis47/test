from typing import Union, List
from mietrak_pro.exporter.configuration import MietrakProConfig
from paperless.objects.orders import Order
from paperless.objects.quotes import Quote
from mietrak_pro.exporter.processors.account import AccountProcessor
from mietrak_pro.exporter.processors.shipping_address import ShippingAddressProcessor
from mietrak_pro.exporter.processors.billing_address import BillingAddressProcessor
from mietrak_pro.exporter.processors.contact import ContactProcessor
from mietrak_pro.exporter.processors.customer import CustomerProcessor
from mietrak_pro.exporter.processors.part import PartProcessor
from mietrak_pro.exporter.processors.router import RouterProcessor
from mietrak_pro.exporter.processors.bill_of_material import BOMProcessor
from mietrak_pro.exporter.processors.routing_line import RoutingLineProcessor
from mietrak_pro.exporter.processors.sales_order import SalesOrderProcessor
from mietrak_pro.exporter.processors.sales_order_line import SalesOrderLineProcessor
from mietrak_pro.exporter.processors.salesperson import PartySalespersonProcessor, OrderSalespersonProcessor
from mietrak_pro.exporter.processors.estimator import EstimatorProcessor
from mietrak_pro.exporter.processors.request_for_quote import RequestForQuoteProcessor
from mietrak_pro.exporter.processors.request_for_quote_line import RequestForQuoteLineProcessor
from mietrak_pro.exporter.processors.add_on import OrderAddOnProcessor, QuoteAddOnProcessor
from mietrak_pro.exporter.processors.add_on_sales_order_line import AddOnSalesOrderLineProcessor
from baseintegration.exporter import logger
from baseintegration.exporter.order_exporter import OrderExporter
from baseintegration.exporter.quote_exporter import QuoteExporter
from mietrak_pro.exporter.utils import BillOfMaterial, RoutingLine, Estimator, AdditionalCharge, \
    AdditionalChargeSalesOrderLine, PartData
import mietrak_pro.models
import os
from datetime import datetime


def create_config_object(parser):
    erp_config = MietrakProConfig(
        tax_exempt_code=parser.get('tax_exempt_code'),
        credit_card_terms_code=parser.get('credit_card_terms_code'),
        company_division_pk=parser.get('company_division_pk', 1),
        default_work_center_name=parser.get('default_work_center_name'),
        default_work_center_code=parser.get('default_work_center_code'),
        pp_work_center_pk_var=parser.get("pp_work_center_pk_var"),
        pp_operation_pk_var=parser.get("pp_operation_pk_var"),
        pp_revenue_account_num_var=parser.get("pp_revenue_account_num_var"),
        pp_purchase_account_num_var=parser.get("pp_purchase_account_num_var"),
        pp_outside_process_var=parser.get("pp_outside_process_var"),
        default_outside_service_work_center_name=parser.get('default_outside_service_work_center_name'),
        default_outside_service_work_center_code=parser.get('default_outside_service_work_center_code'),
        default_outside_service_item_vendor_name=parser.get('default_outside_service_item_vendor_name'),
        default_purchased_item_vendor_name=parser.get('default_purchased_item_vendor_name'),
        default_terms=parser.get('default_terms_when_purchase_orders_disabled'),
        default_terms_period=parser.get('default_terms_period_when_purchase_orders_disabled'),
        default_assembly_operation_name=parser.get('default_assembly_operation_name'),
        raw_material_part_number_variable_name=parser.get('raw_material_part_number_variable_name'),
        raw_material_blank_width_variable_name=parser.get('raw_material_blank_width_variable_name'),
        raw_material_blank_length_variable_name=parser.get('raw_material_blank_length_variable_name'),
        should_perform_assembly_conversion=parser.get('should_perform_assembly_conversion'),
        should_create_mietrak_pro_billing_address=parser.get('should_create_mietrak_pro_billing_address'),
        should_update_mietrak_pro_payment_terms=parser.get('should_update_mietrak_pro_payment_terms'),
        should_create_mietrak_pro_shipping_address=parser.get('should_create_mietrak_pro_shipping_address'),
        should_update_mietrak_pro_customer_notes=parser.get('should_update_mietrak_pro_customer_notes'),
        should_update_mietrak_pro_contact_notes=parser.get('should_update_mietrak_pro_contact_notes'),
        should_update_mietrak_pro_customer_misc_data=parser.get('should_update_mietrak_pro_customer_misc_data'),
        should_update_mietrak_pro_contact_misc_data=parser.get('should_update_mietrak_pro_contact_misc_data'),
        should_update_mietrak_pro_part_description=parser.get('should_update_mietrak_pro_part_description'),
        should_update_mietrak_pro_purchased_components_data=parser.get(
            'should_update_mietrak_pro_purchased_components_data'),
        should_create_mietrak_pro_raw_material_record=parser.get(
            'should_create_mietrak_pro_raw_material_record'),
        should_use_default_raw_material=parser.get('should_use_default_raw_material', True),
        should_rebuild_existing_mietrak_pro_routers=parser.get('should_rebuild_existing_mietrak_pro_routers'),
        should_send_email_when_new_customer_is_created=parser.get(
            'should_send_email_when_new_customer_is_created'),
        should_update_quote_erp_code_in_paperless_parts=parser.get(
            'should_update_quote_erp_code_in_paperless_parts'),
        should_associate_purchased_components_with_assembly_operation=parser.get(
            'should_associate_purchased_components_with_assembly_operation'),
        should_associate_subrouters_with_assembly_operation=parser.get(
            'should_associate_subrouters_with_assembly_operation'),
        default_sales_order_fob=parser.get('default_sales_order_fob'),
        parts_per_blank_variable_name=parser.get('parts_per_blank_variable_name'),
        part_length_variable_name=parser.get('part_length_variable_name'),
        part_width_variable_name=parser.get('part_width_variable_name'),
        stock_length_variable_name=parser.get('stock_length_variable_name'),
        stock_width_variable_name=parser.get('stock_width_variable_name'),
        stock_thickness_variable_name=parser.get('stock_thickness_variable_name'),
        density_variable_name=parser.get('density_variable_name'),
        raw_material_quantity_variable_name=parser.get('raw_material_quantity_variable_name'),
        outside_service_item_vendor_variable=parser.get('outside_service_item_vendor_variable'),
        should_export_assemblies_with_duplicate_components=parser.get(
            'should_export_assemblies_with_duplicate_components', False),
        division_map=parser.get('division_map'),
        pp_quote_reference_field=parser.get('pp_quote_reference_field'),
        should_use_mietrak_salesperson=parser.get('should_use_mietrak_salesperson'),
        overage_percentage_variable_name=parser.get('overage_percentage_variable_name'),
        vendor_variable_name=parser.get('vendor_variable_name'),
        leadtime_variable_name=parser.get('leadtime_variable_name'),
        setup_charge_variable_name=parser.get('setup_charge_variable_name'),
        quantity_per_inverse_variable_name=parser.get('quantity_per_inverse_variable_name'),
        use_exact_material_calc_variable_name=parser.get('use_exact_material_calc_variable_name'),
        osv_minimum_variable_name=parser.get('osv_minimum_variable_name'),
        osv_piece_price_variable_name=parser.get('osv_piece_price_variable_name')
    )
    return erp_config


def create_test_config_object():
    test_erp_config = MietrakProConfig(
        tax_exempt_code="test",
        credit_card_terms_code="test",
        company_division_pk=1,
        default_work_center_name="test",
        pp_work_center_pk_var="test",
        pp_operation_pk_var="test",
        pp_revenue_account_num_var="test",
        pp_purchase_account_num_var="test",
        pp_outside_process_var="test",
        default_vendor_code_name="test",
        default_work_center_code="test",
        default_outside_service_work_center_name="test",
        default_outside_service_work_center_code="test",
        default_outside_service_item_vendor_name="test",
        default_purchased_item_vendor_name="test",
        default_terms="prepaid",
        default_terms_period=0,
        default_assembly_operation_name="ASSEMBLY",
        raw_material_part_number_variable_name='Material Lookup',
        raw_material_blank_width_variable_name='Part Width, in',
        raw_material_blank_length_variable_name='Part Length, in',
        should_perform_assembly_conversion=False,
        should_create_mietrak_pro_billing_address=True,
        should_update_mietrak_pro_payment_terms=True,
        should_create_mietrak_pro_shipping_address=True,
        should_update_mietrak_pro_customer_notes=True,
        should_update_mietrak_pro_contact_notes=True,
        should_update_mietrak_pro_customer_misc_data=True,
        should_update_mietrak_pro_contact_misc_data=True,
        should_update_mietrak_pro_part_description=True,
        should_update_mietrak_pro_purchased_components_data=True,
        should_create_mietrak_pro_raw_material_record=True,
        should_use_default_raw_material=True,
        should_rebuild_existing_mietrak_pro_routers=False,
        should_send_email_when_new_customer_is_created=False,
        should_update_quote_erp_code_in_paperless_parts=False,
        should_associate_purchased_components_with_assembly_operation=True,
        default_sales_order_fob=None,
        outside_service_item_vendor_variable=None,
        should_export_assemblies_with_duplicate_components=False,
        division_map=None,
        pp_quote_reference_field='externalreferencenumber',
        should_use_mietrak_salesperson=False,
        overage_percentage_variable_name='Overage Percent (%)',
        vendor_variable_name='Vendor Name',
        leadtime_variable_name='Lead Time',
        setup_charge_variable_name='Setup Charge',
        quantity_per_inverse_variable_name='Quantity Per Inverse',
        use_exact_material_calc_variable_name='Price Calculation',
        osv_minimum_variable_name='Minimum',
        osv_piece_price_variable_name='Piece Price'
    )
    return test_erp_config


def get_account_data(quote_or_order: Union[Quote, Order]):
    account, business_name, erp_code, customer_notes, contact_id = \
        AccountProcessor.process_account_info(quote_or_order)
    return account, business_name, contact_id, customer_notes, erp_code


def get_division_pk(exporter):
    if not exporter.erp_config.division_map:
        return exporter.erp_config.company_division_pk or 1
    elif exporter.send_from_facility:
        division_map = exporter.erp_config.division_map
        return next(filter(lambda x: x.name == exporter.send_from_facility.name, division_map)).division_pk
    else:
        return exporter.erp_config.division_map[0].division_pk


class MieTrakProOrderExporter(OrderExporter):
    estimator = None

    def _setup_erp_config(self):
        if not self._integration.test_mode:  # pragma: NO COVER
            logger.info('Reading config specific configuration file')
            # This should preserve backwards compatibility for integrations that do not have a refactored config file
            parser = self._integration.config_yaml["Exporters"].get("general", dict())
            parser.update(self._integration.config_yaml["Exporters"]["orders"])
            erp_config = create_config_object(parser)
            self.erp_config = erp_config
        else:
            os.environ.setdefault('TEST', '1')
            test_erp_config = create_test_config_object()
            self.erp_config = test_erp_config

    def _register_default_processors(self):
        self.register_processor(mietrak_pro.models.CustomerParty, CustomerProcessor)
        self.register_processor(mietrak_pro.models.ShippingAddress, ShippingAddressProcessor)
        self.register_processor(mietrak_pro.models.BillingAddress, BillingAddressProcessor)
        self.register_processor(mietrak_pro.models.ContactParty, ContactProcessor)
        self.register_processor(mietrak_pro.models.Partysalesperson, PartySalespersonProcessor)
        self.register_processor(mietrak_pro.models.Salesorder, SalesOrderProcessor)
        self.register_processor(mietrak_pro.models.Salesorderline, SalesOrderLineProcessor)
        self.register_processor(mietrak_pro.models.Salesordersalesperson, OrderSalespersonProcessor)
        self.register_processor(mietrak_pro.models.Item, PartProcessor)
        self.register_processor(mietrak_pro.models.Router, RouterProcessor)
        self.register_processor(BillOfMaterial, BOMProcessor)
        self.register_processor(RoutingLine, RoutingLineProcessor)
        self.register_processor(AdditionalCharge, OrderAddOnProcessor)
        self.register_processor(AdditionalChargeSalesOrderLine, AddOnSalesOrderLineProcessor)

    def _process_order(self, order: Order):  # noqa: C901
        logger.info(f'Processing order {order.number}')
        account, business_name, contact_id, customer_notes, erp_code = get_account_data(order)
        self.estimator = order.estimator
        if self.erp_config.division_map:
            self.send_from_facility = order.send_from_facility
        self.division_pk = get_division_pk(self)

        with self.process_resource(mietrak_pro.models.CustomerParty, business_name, erp_code, customer_notes,
                                   account, contact_id) as customer_data:
            customer = customer_data.customer
            is_customer_new = customer_data.is_customer_new

            with self.process_resource(mietrak_pro.models.ShippingAddress, order, customer,
                                       is_customer_new) as shipping_address, \
                    self.process_resource(mietrak_pro.models.BillingAddress, order, customer,
                                          is_customer_new) as billing_address, \
                    self.process_resource(mietrak_pro.models.ContactParty, order, customer) as contact, \
                    self.process_resource(mietrak_pro.models.Partysalesperson, account, customer), \
                    self.process_resource(mietrak_pro.models.Salesorder, order, customer, contact, billing_address,
                                          shipping_address) as sales_order:
                logger.info(f'New MIE Trak Pro order number {sales_order.salesordernumber}')
                try:
                    self.success_message = f"Associated MieTrak Pro order number is {sales_order.salesordernumber}"
                except Exception:
                    pass

                with self.process_resource(mietrak_pro.models.Salesordersalesperson, order, sales_order):
                    pass

                sales_order_line_reference_number = 1
                for i, order_item in enumerate(order.order_items):
                    # First, make sure that an Item record exists for every unique part number in the BOM
                    component_to_part_mapping = {}
                    root_component_part = None
                    is_root_component_part_new = False
                    for component in order_item.components:
                        with self.process_resource(mietrak_pro.models.Item, component, order_item, order, customer) \
                                as part_data:
                            component_to_part_mapping[component.id]: List[PartData] = part_data
                            if component.is_root_component:
                                root_component_part = part_data.part
                                is_root_component_part_new = part_data.is_part_new

                    # Next, gather any Add-on Items for this order line item
                    add_on_items = []
                    for add_on in order_item.ordered_add_ons:
                        with self.process_resource(AdditionalCharge, add_on) as add_on_item_data:
                            add_on_items.append(add_on_item_data)

                    # Then, create the Routers for each manufactured or assembled component, associate the purchased
                    # components and raw materials to the corresponding Router, and add the routing steps
                    component_to_router_mapping = {}
                    root_component_router = None
                    # Check if assembly contains only a single mfg comp. and whether the config option is enabled
                    if self.should_perform_assembly_conversion(order_item):
                        sales_order_line_reference_number = \
                            self.process_assembly_conversion(
                                order,
                                customer_data,
                                customer,
                                is_customer_new,
                                shipping_address,
                                billing_address,
                                contact,
                                sales_order,
                                sales_order_line_reference_number,
                                order_item,
                                component_to_part_mapping,
                                root_component_part,
                                is_root_component_part_new,
                                component_to_router_mapping,
                                root_component_router,
                                add_on_items,
                                order_item_position=i
                            )
                    else:
                        for assm_comp in self.iterate_assembly(order_item, self.erp_config.should_export_assemblies_with_duplicate_components):

                            component = assm_comp.component

                            part, is_part_new, raw_material_part_data = \
                                component_to_part_mapping.get(component.id)
                            logger.info(f'Iterate assembly: current component part number {part.partnumber} '
                                        f'and revision {part.revision}')
                            parent_component = assm_comp.parent
                            if parent_component is not None:
                                parent_router, is_parent_router_new = component_to_router_mapping.get(parent_component.id)
                                # BOM quantities in Paperless Parts are relative to the root component. In MIE Trak Pro, they are relative to the
                                # immediate parent component. We need to normalize the Paperless Parts BOM quantity for the child component
                                # to account for this
                                if self.erp_config.should_export_assemblies_with_duplicate_components:
                                    child_quantity = self.get_current_quantity_per_parent()
                                else:
                                    child_quantity = component.innate_quantity / parent_component.innate_quantity
                            else:
                                parent_router = None
                                is_parent_router_new = False  # noqa: F841
                                child_quantity = component.innate_quantity

                            # Create a router for the current component
                            router = None
                            is_router_new = False
                            if component.type in {'manufactured', 'assembled'}:
                                with self.process_resource(mietrak_pro.models.Router, part, customer) as router_data:
                                    component_to_router_mapping[component.id] = router_data
                                    router, is_router_new = router_data

                                    log_type = mietrak_pro.models.Activitylogtype.objects.get(activitylogtypepk=46)
                                    activitylog = mietrak_pro.models.ActivityLog(
                                        routerfk=router,
                                        datestamp=datetime.now(),
                                        comment=f'https://app.paperlessparts.com/orders/edit/{order.number}',
                                        activitylogtypefk=log_type
                                    )
                                    activitylog.save()

                                    # Populate the routing lines for this component
                                    if (is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                                        with self.process_resource(RoutingLine, router, component, customer):
                                            pass
                            if component.is_root_component:
                                root_component_router = router

                            # Link the current router to the parent router as a subrouter
                            if (parent_router is not None and router is not None) and \
                                    (is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                                with self.process_resource(BillOfMaterial, parent_router, None,
                                                           router, child_quantity, component):
                                    pass

                            # Create a BOM link for the raw material(s) if this is an assembled component
                            if component.type == 'assembled':
                                if (router is not None and raw_material_part_data is not None) and \
                                        (is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                                    with self.process_resource(BillOfMaterial, router, raw_material_part_data, None,
                                                               None, component):
                                        pass

                            # Create a BOM link for the raw material if this is a manufactured component
                            if component.type == 'manufactured':
                                if (router is not None and raw_material_part_data is not None) and \
                                        (is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                                    with self.process_resource(BillOfMaterial, router, raw_material_part_data, None,
                                                               None, component):
                                        pass

                            # Create a BOM link for the current part if this is a purchased component
                            if component.type == 'purchased':
                                if (parent_router is not None) and \
                                        (is_parent_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                                    with self.process_resource(BillOfMaterial, parent_router, part,
                                                               None, child_quantity, component):
                                        pass

                            # If this is the root component, create a BOM link for any add-on items that should be included
                            # in the BOM
                            if component.is_root_component:
                                if (router is not None) and \
                                        (is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                                    for add_on_item_data in add_on_items:
                                        if add_on_item_data is None:
                                            continue
                                        _, add_on_item, should_include_add_on_item_in_bom = add_on_item_data
                                        if should_include_add_on_item_in_bom:
                                            add_on_bom_quantity = 1.
                                            with self.process_resource(BillOfMaterial, router, add_on_item,
                                                                       None, add_on_bom_quantity, None):
                                                pass

                        # Finally, create the sales order line for this order item
                        with self.process_resource(mietrak_pro.models.Salesorderline, sales_order, order, order_item,
                                                   customer, root_component_part, root_component_router, shipping_address,
                                                   is_root_component_part_new, sales_order_line_reference_number):
                            sales_order_line_reference_number += 1

                        # And, if applicable, create a distinct sales order line for each add-on
                        for add_on_item_data in add_on_items:
                            if add_on_item_data is None:
                                continue
                            add_on, add_on_item, should_include_add_on_item_in_bom = add_on_item_data
                            with self.process_resource(AdditionalChargeSalesOrderLine, sales_order, order, order_item,
                                                       add_on, customer, add_on_item, shipping_address,
                                                       sales_order_line_reference_number):
                                sales_order_line_reference_number += 1

    def process_assembly_conversion(  # noqa: C901
            self,
            order,
            customer_data,
            customer,
            is_customer_new,
            shipping_address,
            billing_address,
            contact,
            sales_order,
            sales_order_line_reference_number,
            order_item,
            component_to_part_mapping,
            root_component_part,
            is_root_component_part_new,
            component_to_router_mapping,
            root_component_router,
            add_on_items,
            order_item_position
    ):
        """ Our data model currently only allows assembled components to have children. This means that a part with
            inserts needs to be modeled as an assembled component with two children: a manufactured component and a
            purchased component. This is an artificial constraint imposed by our data model. A part with inserts should
            be brought into MIE Trak Pro as a single Router. As such, we need special handling for this case to produce
            the desired result.

            Assumptions:
            - The assembled component and manufactured component are in fact the same part in this situation. Use the
              part number from the assembled component for the final Item/Router.
            - The routing steps from the manufactured component should show up before the routing steps from the
              assembled component in the final Router.
        """
        logger.info("Processing assembly conversion - creating a single router for the single mfg. component.")
        top_level_assembly_component = None
        router = None
        is_router_new = False
        for assm_comp in self.iterate_assembly(order_item, self.erp_config.should_export_assemblies_with_duplicate_components):
            component = assm_comp.component

            # Locate and hold onto the top level assembly component in a separate variable
            if component.type == "assembled":
                top_level_assembly_component = component

            # Process mfg. comp. first so that it can act as the root component router.
            # Hardware BOM items will be added later.
            if not component.type == "manufactured":
                continue

            # Part parameters are dictated by the root assembly (Part number should be top-lvl comp.)
            part, is_part_new, raw_material_part_data = \
                component_to_part_mapping.get(top_level_assembly_component.id)
            logger.info(f'Iterate assembly: current component part number {part.partnumber} '
                        f'and revision {part.revision}')

            # Create a router for the manufactured component
            if component.type in {'manufactured'}:
                with self.process_resource(mietrak_pro.models.Router, part, customer) as router_data:
                    component_to_router_mapping[component.id] = router_data
                    router, is_router_new = router_data

                    # Populate the routing lines for this component
                    if is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers:
                        # Add all mfg. component routing lines
                        with self.process_resource(RoutingLine, router, component, customer):
                            pass
                        # Add top level assembly routing lines to router first if there are any
                        if (top_level_assembly_component is not None)\
                                and len(top_level_assembly_component.shop_operations) > 0:
                            with self.process_resource(RoutingLine, router, top_level_assembly_component, customer):
                                pass

            # Artificially force the manufactured component to act as the root component router
            if component.type == "manufactured":
                root_component_router = router

            # Create a BOM link for the raw material if this is a manufactured component
            if component.type == 'manufactured':
                # The raw material should be specified on the manufactured component (i.e. the current component), not
                # the top-level component
                _, _, raw_material_part_data = \
                    component_to_part_mapping.get(component.id)
                if (router is not None and raw_material_part_data is not None) and \
                        (is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                    with self.process_resource(BillOfMaterial, router, raw_material_part_data, None, None, component):
                        pass

            # Create a BOM link for any add-on items that should be included in the BOM
            if (router is not None) and \
                    (is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                for add_on_item_data in add_on_items:
                    if add_on_item_data is None:
                        continue
                    _, add_on_item, should_include_add_on_item_in_bom = add_on_item_data
                    if should_include_add_on_item_in_bom:
                        add_on_bom_quantity = 1.
                        with self.process_resource(BillOfMaterial, router, add_on_item,
                                                   None, add_on_bom_quantity, None):
                            pass

        for assm_comp in self.iterate_assembly(order_item, self.erp_config.should_export_assemblies_with_duplicate_components):
            component = assm_comp.component

            # Add hardware components to the single manufactured component router
            if component.type == 'purchased':
                part, is_part_new, raw_material_part_data = \
                    component_to_part_mapping.get(component.id)
                logger.info(f'Iterate assembly (for purchased components only): current component part number '
                            f'{part.partnumber} and revision {part.revision}')

                if top_level_assembly_component is not None:
                    # BOM quantities in Paperless Parts are relative to the root component. In MIE Trak Pro, they are relative to the
                    # immediate parent component. We need to normalize the Paperless Parts BOM quantity for the child component
                    # to account for this. (Parent will always be the single top lvl assembly in this case).
                    child_quantity = component.innate_quantity / top_level_assembly_component.innate_quantity
                else:
                    child_quantity = component.innate_quantity

                # Create a BOM link for the current part if this is a purchased component
                if (router is not None) and \
                        (is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                    with self.process_resource(BillOfMaterial, router, part, None, child_quantity, component):
                        pass

        # Finally, create the sales order line for this order item
        with self.process_resource(mietrak_pro.models.Salesorderline, sales_order, order, order_item,
                                   customer, root_component_part, root_component_router, shipping_address,
                                   is_root_component_part_new, sales_order_line_reference_number):
            sales_order_line_reference_number += 1

        # And, if applicable, create a distinct sales order line for each add-on
        for add_on_item_data in add_on_items:
            if add_on_item_data is None:
                continue
            add_on, add_on_item, should_include_add_on_item_in_bom = add_on_item_data
            with self.process_resource(AdditionalChargeSalesOrderLine, sales_order, order, order_item,
                                       add_on, customer, add_on_item, shipping_address,
                                       sales_order_line_reference_number):
                sales_order_line_reference_number += 1
        return sales_order_line_reference_number

    def should_perform_assembly_conversion(self, order_item):
        mfg_comp_count = 0
        assm_comp_count = 0
        prch_comp_count = 0
        for comp in order_item.components:
            if comp.type == 'manufactured':
                mfg_comp_count += 1
            elif comp.type == 'assembled':
                assm_comp_count += 1
            elif comp.type == 'purchased':
                prch_comp_count += 1
        logger.info(f'MFG-{mfg_comp_count}, ASSM-{assm_comp_count}, PC-{prch_comp_count}')
        if mfg_comp_count == 1 and assm_comp_count == 1 and self.erp_config.should_perform_assembly_conversion:
            return True
        return False


class MieTrakProQuoteExporter(QuoteExporter):
    estimator = None

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            logger.info('Reading config specific configuration file')
            # This should preserve backwards compatibility for integrations that do not have a refactored config file
            parser = self._integration.config_yaml["Exporters"].get("general", dict())
            parser.update(self._integration.config_yaml["Exporters"]["quotes"])
            erp_config = create_config_object(parser)
            self.erp_config = erp_config
        else:
            os.environ.setdefault('TEST', '1')
            test_erp_config = create_test_config_object()
            self.erp_config = test_erp_config

    def _register_default_processors(self):
        self.register_processor(mietrak_pro.models.Requestforquote, RequestForQuoteProcessor)
        self.register_processor(mietrak_pro.models.Requestforquoteline, RequestForQuoteLineProcessor)
        self.register_processor(mietrak_pro.models.CustomerParty, CustomerProcessor)
        self.register_processor(mietrak_pro.models.ContactParty, ContactProcessor)
        self.register_processor(Estimator, EstimatorProcessor)
        self.register_processor(mietrak_pro.models.Item, PartProcessor)
        self.register_processor(mietrak_pro.models.Router, RouterProcessor)
        self.register_processor(BillOfMaterial, BOMProcessor)
        self.register_processor(RoutingLine, RoutingLineProcessor)
        self.register_processor(AdditionalCharge, QuoteAddOnProcessor)

    def _process_quote(self, quote: Quote):  # noqa: C901
        logger.info(f"Processing {quote.number}")
        account, business_name, contact_id, customer_notes, erp_code = get_account_data(quote)
        self.estimator = quote.estimator
        if self.erp_config.division_map:
            self.send_from_facility = quote.send_from_facility
        self.division_pk = get_division_pk(self)

        with self.process_resource(mietrak_pro.models.CustomerParty, business_name, erp_code, customer_notes,
                                   account, contact_id) as customer_data:
            customer = customer_data.customer

            with self.process_resource(mietrak_pro.models.ContactParty, quote, customer) as contact, \
                    self.process_resource(Estimator, quote) as estimator, \
                    self.process_resource(mietrak_pro.models.Requestforquote, quote, customer, contact, estimator) as mietrak_pro_rfq:
                logger.info(f'New MIE Trak Pro Request for Quote number {mietrak_pro_rfq.requestforquotenumber}')
                try:
                    self.success_message = f"Associated MieTrak Pro Request for Quote number is {mietrak_pro_rfq.requestforquotenumber}"
                except Exception:
                    pass
                for i, quote_item in enumerate(quote.quote_items):
                    quote_line_reference_number = i + 1
                    # First, make sure that an Item record exists for every unique part number in the BOM
                    component_to_part_mapping = {}
                    root_component_part = None
                    for component in quote_item.components:
                        with self.process_resource(mietrak_pro.models.Item, component, quote_item, quote, customer) \
                                as part_data:
                            component_to_part_mapping[component.id] = part_data
                            if component.is_root_component:
                                root_component_part = part_data.part

                    # Next, gather any Add-on Items for this quote line item
                    add_on_items = []
                    for add_on in quote_item.root_component.add_ons:
                        with self.process_resource(AdditionalCharge, add_on) as add_on_item_data:
                            add_on_items.append(add_on_item_data)

                    # Then, create the Routers for each manufactured or assembled component, associate the purchased
                    # components and raw materials to the corresponding Router, and add the routing steps
                    component_to_router_mapping = {}
                    # Check if assembly contains only a single mfg comp. and whether the config option is enabled
                    if self.should_perform_assembly_conversion(quote_item):
                        self.process_assembly_conversion(
                            quote,
                            customer_data,
                            customer,
                            contact,
                            estimator,
                            mietrak_pro_rfq,
                            quote_line_reference_number,
                            quote_item,
                            component_to_part_mapping,
                            root_component_part,
                            component_to_router_mapping,
                            add_on_items,
                            quote_item_position=i
                        )
                    else:
                        for assm_comp in self.iterate_assembly(quote_item, self.erp_config.should_export_assemblies_with_duplicate_components):
                            component = assm_comp.component
                            part, is_part_new, raw_material_part_data = \
                                component_to_part_mapping.get(component.id)
                            parent_component = assm_comp.parent
                            if parent_component is not None:
                                parent_router, is_parent_router_new = component_to_router_mapping.get(parent_component.id)
                                # BOM quantities in Paperless Parts are relative to the root component. In MIE Trak Pro, they are relative to the
                                # immediate parent component. We need to normalize the Paperless Parts BOM quantity for the child component
                                # to account for this
                                if self.erp_config.should_export_assemblies_with_duplicate_components:
                                    child_quantity = self.get_current_quantity_per_parent()
                                else:
                                    child_quantity = component.innate_quantity / parent_component.innate_quantity
                            else:
                                parent_router = None
                                is_parent_router_new = False  # noqa: F841
                                child_quantity = component.innate_quantity

                            # Create a router for the current component
                            router = None
                            is_router_new = False
                            if component.type in {'manufactured', 'assembled'}:
                                with self.process_resource(mietrak_pro.models.Router, part, customer) as router_data:
                                    component_to_router_mapping[component.id] = router_data
                                    router, is_router_new = router_data

                                    # Populate the routing lines for this component
                                    if (is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                                        with self.process_resource(RoutingLine, router, component, customer):
                                            pass

                            # Link the current router to the parent router as a subrouter
                            if (parent_router is not None and router is not None) and \
                                    (is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                                with self.process_resource(BillOfMaterial, parent_router, None,
                                                           router, child_quantity, component):
                                    pass

                            # Create a BOM link for the raw material(s) if this is an assembled component
                            if component.type == 'assembled':
                                if (router is not None and raw_material_part_data is not None) and \
                                        (is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                                    with self.process_resource(BillOfMaterial, router, raw_material_part_data,
                                                               None, None, component):
                                        pass

                            # Create a BOM link for the raw material if this is a manufactured component
                            if component.type == 'manufactured':
                                if (router is not None and raw_material_part_data is not None) and \
                                        (is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                                    with self.process_resource(BillOfMaterial, router, raw_material_part_data,
                                                               None, None, component):
                                        pass

                            # Create a BOM link for the current part if this is a purchased component
                            if component.type == 'purchased':
                                if (parent_router is not None) and \
                                        (is_parent_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                                    with self.process_resource(BillOfMaterial, parent_router, part,
                                                               None, child_quantity, component):
                                        pass

                            # If this is the root component, create a BOM link for any add-on items that should be included
                            # in the BOM
                            if component.is_root_component:
                                if (router is not None) and \
                                        (is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                                    for add_on_item_data in add_on_items:
                                        if add_on_item_data is None:
                                            continue
                                        _, add_on_item, should_include_add_on_item_in_bom = add_on_item_data
                                        if should_include_add_on_item_in_bom:
                                            add_on_bom_quantity = 1.
                                            with self.process_resource(BillOfMaterial, router, add_on_item,
                                                                       None, add_on_bom_quantity, None):
                                                pass

                        # Finally, create the request for quote line for this quote item
                        with self.process_resource(mietrak_pro.models.Requestforquoteline, mietrak_pro_rfq, quote_item,
                                                   root_component_part, quote_line_reference_number, estimator):
                            pass

    def process_assembly_conversion(  # noqa: C901
        self,
        quote,
        customer_data,
        customer,
        contact,
        estimator,
        request_for_quote,
        quote_line_reference_number,
        quote_item,
        component_to_part_mapping,
        root_component_part,
        component_to_router_mapping,
        add_on_items,
        quote_item_position
    ):
        """ Our data model currently only allows assembled components to have children. This means that a part with
            inserts needs to be modeled as an assembled component with two children: a manufactured component and a
            purchased component. This is an artificial constraint imposed by our data model. A part with inserts should
            be brought into MIE Trak Pro as a single Router. As such, we need special handling for this case to produce
            the desired result.

            Assumptions:
            - The assembled component and manufactured component are in fact the same part in this situation. Use the
              part number from the assembled component for the final Item/Router.
            - The routing steps from the manufactured component should show up before the routing steps from the
              assembled component in the final Router.
        """
        logger.info("Processing assembly conversion - creating a single router for the single mfg. component.")
        top_level_assembly_component = None
        router = None
        is_router_new = False
        for assm_comp in self.iterate_assembly(quote_item, self.erp_config.should_export_assemblies_with_duplicate_components):
            component = assm_comp.component

            # Locate and hold onto the top level assembly component in a separate variable
            if component.type == "assembled":
                top_level_assembly_component = component

            # Process mfg. comp. first so that it can act as the root component router.
            # Hardware BOM items will be added later.
            if not component.type == "manufactured":
                continue

            # Part parameters are dictated by the root assembly (Part number should be top-lvl comp.)
            part, is_part_new, raw_material_part_data = \
                component_to_part_mapping.get(top_level_assembly_component.id)
            logger.info(f'Iterate assembly: current component part number {part.partnumber} '
                        f'and revision {part.revision}')

            # Create a router for the manufactured component
            if component.type in {'manufactured'}:
                with self.process_resource(mietrak_pro.models.Router, part, customer) as router_data:
                    component_to_router_mapping[component.id] = router_data
                    router, is_router_new = router_data

                    # Populate the routing lines for this component
                    if is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers:
                        # Add all mfg. component routing lines
                        with self.process_resource(RoutingLine, router, component, customer):
                            pass
                        # Add top level assembly routing lines to router first if there are any
                        if (top_level_assembly_component is not None) \
                                and len(top_level_assembly_component.shop_operations) > 0:
                            with self.process_resource(RoutingLine, router, top_level_assembly_component, customer):
                                pass

            # Create a BOM link for the raw material if this is a manufactured component
            if component.type == 'manufactured':
                # The raw material should be specified on the manufactured component (i.e. the current component), not
                # the top-level component
                _, _, raw_material_part_data = component_to_part_mapping.get(component.id)
                if raw_material_part_data:
                    raw_material_part_data = [raw_material_part_data[0]]

                if (router is not None and raw_material_part_data is not None) and \
                        (is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                    with self.process_resource(BillOfMaterial, router, raw_material_part_data, None, None, component):
                        pass

            # Create a BOM link for any add-on items that should be included in the BOM
            if (router is not None) and \
                    (is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                for add_on_item_data in add_on_items:
                    if add_on_item_data is None:
                        continue
                    _, add_on_item, should_include_add_on_item_in_bom = add_on_item_data
                    if should_include_add_on_item_in_bom:
                        add_on_bom_quantity = 1.
                        with self.process_resource(BillOfMaterial, router, add_on_item,
                                                   None, add_on_bom_quantity, None):
                            pass

        for assm_comp in self.iterate_assembly(quote_item, self.erp_config.should_export_assemblies_with_duplicate_components):
            component = assm_comp.component

            # Add hardware components to the single manufactured component router
            if component.type == 'purchased':
                part, is_part_new, raw_material_part_data = component_to_part_mapping.get(component.id)
                logger.info(f'Iterate assembly (for purchased components only): current component part number '
                            f'{part.partnumber} and revision {part.revision}')

                if top_level_assembly_component is not None:
                    # BOM quantities in Paperless Parts are relative to the root component. In MIE Trak Pro, they are relative to the
                    # immediate parent component. We need to normalize the Paperless Parts BOM quantity for the child component
                    # to account for this. (Parent will always be the single top lvl assembly in this case).
                    child_quantity = component.innate_quantity / top_level_assembly_component.innate_quantity
                else:
                    child_quantity = component.innate_quantity

                # Create a BOM link for the current part if this is a purchased component
                if (router is not None) and \
                        (is_router_new or self.erp_config.should_rebuild_existing_mietrak_pro_routers):
                    with self.process_resource(BillOfMaterial, router, part, None, child_quantity, component):
                        pass

        # Finally, create the request for quote line for this quote item
        with self.process_resource(mietrak_pro.models.Requestforquoteline, request_for_quote, quote_item,
                                   root_component_part, quote_line_reference_number, estimator):
            pass

    def should_perform_assembly_conversion(self, quote_item):
        mfg_comp_count = 0
        assm_comp_count = 0
        prch_comp_count = 0
        for comp in quote_item.components:
            if comp.type == 'manufactured':
                mfg_comp_count += 1
            elif comp.type == 'assembled':
                assm_comp_count += 1
            elif comp.type == 'purchased':
                prch_comp_count += 1
        logger.info(f'MFG-{mfg_comp_count}, ASSM-{assm_comp_count}, PC-{prch_comp_count}')
        if mfg_comp_count == 1 and assm_comp_count == 1 and self.erp_config.should_perform_assembly_conversion:
            return True
        return False
