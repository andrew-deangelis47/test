from collections import defaultdict
from e2.exporter.configuration import E2Config
from paperless.objects.orders import Order
from e2.exporter.processors.account import AccountProcessor
from e2.exporter.processors.address import AddressProcessor
from e2.exporter.e2_shop_system_processors.address import E2ShopSystemAddressProcessor
from e2.exporter.processors.assembly import AssemblyProcessor
from e2.exporter.processors.contact import ContactProcessor
from e2.exporter.e2_shop_system_processors.contact import E2ShopSystemContactProcessor
from e2.exporter.processors.customer import CustomerProcessor
from e2.exporter.processors.job_requirement import JobRequirementProcessor
from e2.utils.utils import JobRequirementData
from e2.exporter.e2_shop_system_processors.order_header import E2ShopSystemOrderHeaderProcessor
from e2.exporter.processors.order_header import OrderHeaderProcessor
from e2.exporter.e2_shop_system_processors.order_line_item import E2ShopSystemOrderLineItemProcessor
from e2.exporter.processors.order_line_item import OrderLineItemProcessor
from e2.exporter.processors.part import PartProcessor
from e2.exporter.e2_shop_system_processors.routing import E2ShopSystemRoutingProcessor
from e2.exporter.processors.routing import RoutingProcessor
from e2.exporter.processors.salesperson import SalespersonProcessor
from baseintegration.exporter import logger
from baseintegration.exporter.order_exporter import OrderExporter
from baseintegration.exporter.quote_exporter import QuoteExporter
from baseintegration.integration import Integration
import e2.models as e2
import os


class E2QuoteExporter(QuoteExporter):
    def __init__(self, integration: Integration):
        super().__init__(integration)

    def _process_quote(self, quote):
        pass


class E2OrderExporter(OrderExporter):

    def __init__(self, integration: Integration):
        super().__init__(integration)

        # Create data members for caching custom table data to reduce the number of API calls
        self.operation_skip_list = None
        self.pp_op_to_e2_work_center_mapping = None

    def run(self, order_num: int = None):
        # Clear the cached custom tables to make sure they are refreshed for each scheduled run of this exporter
        self.operation_skip_list = None
        self.pp_op_to_e2_work_center_mapping = None

        super().run(order_num)

    def _setup_erp_config(self):

        if not self._integration.test_mode:
            logger.info('Reading config specific configuration file')
            parser = self._integration.config_yaml["Exporters"]["orders"]

            self.erp_config = E2Config(
                entered_by=parser.get('entered_by'),
                tax_exempt_code=parser.get('tax_exempt_code'),
                credit_card_terms_code=parser.get('credit_card_terms_code'),
                default_work_center_name=parser.get('default_work_center_name'),
                default_vendor_code_name=parser.get('default_vendor_code_name'),
                setup_time_units=parser.get('setup_time_units'),
                runtime_units=parser.get('runtime_units'),
                raw_material_part_number_variable_name=parser.get('raw_material_part_number_variable_name'),
                raw_material_row_lookup_variable_name=parser.get('raw_material_row_lookup_variable_name'),
                vendor_code_operation_variable_name=parser.get('vendor_code_operation_variable_name'),
                op_code_operation_variable_name=parser.get('op_code_operation_variable_name'),
                should_update_e2_billing_address=parser.get('should_update_e2_billing_address'),
                should_update_e2_payment_terms=parser.get('should_update_e2_payment_terms'),
                should_create_e2_shipping_address=parser.get('should_create_e2_shipping_address'),
                should_update_e2_customer_notes=parser.get('should_update_e2_customer_notes'),
                should_update_e2_customer_sales_id=parser.get('should_update_e2_customer_sales_id'),
                should_update_e2_part_revision=parser.get('should_update_e2_part_revision'),
                should_update_e2_part_description=parser.get('should_update_e2_part_description'),
                should_update_e2_purchased_components_data=parser.get('should_update_e2_purchased_components_data'),
                should_create_e2_raw_material_record=parser.get('should_create_e2_raw_material_record'),
                should_replace_e2_routing_for_existing_parts=parser.get('should_replace_e2_routing_for_existing_parts'),
                should_replace_e2_bom_for_existing_parts=parser.get('should_replace_e2_bom_for_existing_parts'),
                should_get_vend_code_from_operation_variable=parser.get('should_get_vend_code_from_operation_variable'),
                should_create_order_line_items_as_processed=parser.get('should_create_order_line_items_as_processed'),
                should_include_paperless_urls_in_job_notes=parser.get('should_include_paperless_urls_in_job_notes'),
                should_update_e2_part_quantity_and_price=parser.get('should_update_e2_part_quantity_and_price'),
                should_use_extended_part_quantity_and_price=parser.get('should_use_extended_part_quantity_and_price'),
                should_populate_order_routing_for_add_ons=parser.get('should_populate_order_routing_for_add_ons'),
                default_customer_currency_code=parser.get('default_customer_currency_code', 'USA'),
                default_sales_order_location=parser.get('default_sales_order_location'),
                default_work_code=parser.get('default_work_code'),
                default_routed_by_employee=parser.get('default_routed_by_employee'),
                default_sales_order_fob=parser.get('default_sales_order_fob'),
                should_export_assemblies_with_duplicate_components=parser.get(
                    'should_export_assemblies_with_duplicate_components', False
                ),
                should_use_new_multiple_material_logic=parser.get('should_use_new_multiple_material_logic', False),
                material_op_quantity_required_var=parser.get('material_op_quantity_required_var'),
                material_op_uom_var=parser.get('material_op_uom_var'),
                material_default_uom=parser.get('material_default_uom'),
                material_op_prod_code_var=parser.get('material_op_prod_code_var'),
                material_default_prod_code=parser.get('material_default_prod_code')
            )

        else:
            os.environ.setdefault('TEST', '1')
            self.erp_config = E2Config(
                entered_by="test",
                tax_exempt_code="test_code",
                credit_card_terms_code="credit_card_code",
                default_work_center_name="PAPER_WORK_CENTER",
                default_vendor_code_name="PAPER_VENDOR",
                raw_material_part_number_variable_name="RAW MAT",
                vendor_code_operation_variable_name="VEND",
                op_code_operation_variable_name='Operation Selection',
                should_update_e2_billing_address=True,
                should_update_e2_payment_terms=True,
                should_create_e2_shipping_address=True,
                should_update_e2_customer_notes=True,
                should_update_e2_customer_sales_id=True,
                should_update_e2_part_revision=True,
                should_update_e2_part_description=True,
                should_update_e2_purchased_components_data=True,
                should_create_e2_raw_material_record=True,
                should_replace_e2_routing_for_existing_parts=True,
                should_replace_e2_bom_for_existing_parts=True,
                should_get_vend_code_from_operation_variable=True,
                should_create_order_line_items_as_processed=True,
                should_include_paperless_urls_in_job_notes=True,
                should_update_e2_part_quantity_and_price=True,
                should_use_extended_part_quantity_and_price=True,
                should_populate_order_routing_for_add_ons=True,
                default_customer_currency_code="USA",
                default_sales_order_location=None,
                default_work_code=None,
                default_routed_by_employee=None,
                default_sales_order_fob=None,
                should_export_assemblies_with_duplicate_components=False,
                should_use_new_multiple_material_logic=False,
                material_op_quantity_required_var="Required Quantity",
                material_op_uom_var="Pricing Unit Of Measure",
                material_default_uom="EA",
                material_op_prod_code_var="Product Code",
                material_default_prod_code="BAR"
            )

    def _register_default_processors(self):
        self.register_processor(e2.CustomerCode, CustomerProcessor)
        self.register_processor(e2.JobReq, JobRequirementProcessor)
        self.register_processor(e2.Estim, PartProcessor)
        self.register_processor(e2.Materials, AssemblyProcessor)
        from e2.utils import get_version_number
        if get_version_number() == "default":
            self.register_processor(e2.Shipto, AddressProcessor)
            self.register_processor(e2.Contacts, ContactProcessor)
            self.register_processor(e2.Order, OrderHeaderProcessor)
            self.register_processor(e2.OrderDet, OrderLineItemProcessor)
            self.register_processor(e2.Routing, RoutingProcessor)
        else:
            self.register_processor(e2.Shipto, E2ShopSystemAddressProcessor)
            self.register_processor(e2.Contacts, E2ShopSystemContactProcessor)
            self.register_processor(e2.Order, E2ShopSystemOrderHeaderProcessor)
            self.register_processor(e2.OrderDet, E2ShopSystemOrderLineItemProcessor)
            self.register_processor(e2.Routing, E2ShopSystemRoutingProcessor)

    def _process_order(self, order: Order):  # noqa: C901
        logger.info(f'Processing order {order.number}')
        account_id, business_name, contact_id, customer_notes, erp_code, payment_terms, payment_terms_period = \
            self.get_account_data(order)
        sales_id = self.get_sales_id(order)

        with self.process_resource(e2.CustomerCode, business_name, erp_code, payment_terms, payment_terms_period,
                                   customer_notes, order, account_id, contact_id, sales_id) as customer_data:
            customer = customer_data.customer
            customer_is_new = customer_data.customer_is_new

            with self.process_resource(e2.Shipto, order, customer, customer_is_new) as ship_to, \
                    self.process_resource(e2.Contacts, order, customer) as contact, \
                    self.process_resource(e2.Order, order, customer, ship_to, business_name, contact, sales_id) as order_header:

                logger.info(f'New E2 order number {order_header.order_no}')

                order_item_number = 1
                for order_item in order.order_items:
                    # First, make sure that an Estim record exists for every unique part number in the BOM
                    component_to_part_mapping: dict = {}
                    component_to_job_requirement_data_mapping = defaultdict(list)
                    for component in order_item.components:
                        assembly_processor = self._registered_processors[e2.Materials.__name__](self)
                        with self.process_resource(e2.Estim, component, order_item, order, order_header, customer,
                                                   assembly_processor) as part_data:
                            part = part_data.part
                            is_part_new = part_data.is_part_new
                            component_to_part_mapping[component.id] = (part, is_part_new)

                            # We will need to create a JobReq record for the raw material, if applicable
                            job_req_data = part_data.job_requirement
                            if job_req_data is not None:
                                component_to_job_requirement_data_mapping[component.id].append(job_req_data)

                            # If there is a list of job requirements, add a JobReq record for each
                            job_req_list = part_data.job_requirement_list
                            for job_req_data in job_req_list:
                                component_to_job_requirement_data_mapping[component.id].append(job_req_data)

                    # Then, create the BOM linkages with Materials records, populate the Routing records for each component,
                    # and create OrderDet records for the jobs
                    component_to_job_number_mapping: dict = {}
                    component_to_order_details = defaultdict(list)
                    for assm_comp in self.iterate_assembly(order_item, self.erp_config.should_export_assemblies_with_duplicate_components):
                        component = assm_comp.component
                        part, is_part_new = component_to_part_mapping.get(component.id)
                        parent_component = assm_comp.parent
                        if parent_component is not None:
                            parent_part, is_parent_part_new = component_to_part_mapping.get(parent_component.id)

                            # BOM quantities in Paperless Parts are relative to the root component. In E2, they are relative to the
                            # immediate parent component. We need to normalize the Paperless Parts BOM quantity for the child component
                            # to account for this
                            if self.erp_config.should_export_assemblies_with_duplicate_components:
                                child_quantity = self.get_current_quantity_per_parent()
                            else:
                                child_quantity = component.innate_quantity / parent_component.innate_quantity
                        else:
                            parent_part = None
                            is_parent_part_new = False
                            child_quantity = component.innate_quantity

                        # Create or update the Materials records linking this component to its parent, if applicable
                        # By our convention (due to how the iterate_assembly() function works),
                        # Materials records are created to link a child component (the current component) to its parent
                        # As such, do nothing for the root component
                        if not component.is_root_component:
                            is_purchased = component.type == 'purchased'
                            with self.process_resource(e2.Materials, parent_part, part, child_quantity, is_parent_part_new, is_purchased):
                                pass

                        # Populate routing on the part based on the Paperless Parts operations, if applicable
                        with self.process_resource(e2.Routing, component, part, is_part_new):
                            pass

                        if component.type in {'assembled', 'manufactured'}:
                            # Create an order line item for this component
                            if not self.erp_config.should_create_order_line_items_as_processed and \
                                    not component.is_root_component:
                                continue
                            # If the order is brought over as "processed", then:
                            # Root components will become "standard" order line items with a unit price, a nonzero quantity ordered, and a job number
                            # All subcomponents will become special order line items with 0 unit price, quantity to stock instead
                            # of quantity ordered, a job number, and a reference to their parent subassembly's job number in the MasterJobNo column
                            # We are effectively creating a "flat BOM" of jobs based on the "nested BOM" representation of the Estim records
                            parent_job_number = component_to_job_number_mapping.get(parent_component.id) \
                                if parent_component is not None else None
                            with self.process_resource(e2.OrderDet, order_item, order, order_header, part,
                                                       component, order_item_number, parent_job_number) as order_line_item_data:
                                order_details = order_line_item_data.order_line_item
                                component_to_job_number_mapping[component.id] = order_details.job_no
                                component_to_order_details[component.id].append(order_details)
                                order_item_number += 1

                                # We will need to create a JobReq to link each outside service operations to the order line item (job)
                                for order_routing_line in order_line_item_data.order_routing_lines:
                                    if order_routing_line.work_or_vend == 1:  # Outside service operation
                                        job_req_data = JobRequirementData(outside_service_routing_line=order_routing_line,
                                                                          purchased_component=None,
                                                                          purchased_component_part_record=None,
                                                                          raw_material_part_record=None,
                                                                          raw_material_quantity=None,
                                                                          assembly_component=self.current_assm_comp,
                                                                          order_details=order_details)
                                        component_to_job_requirement_data_mapping[component.id].append(job_req_data)

                        # We will also need to create a JobReq to link each purchased component to its parent component's job
                        if component.type == 'purchased':
                            parent_component_order_details_list = component_to_order_details[parent_component.id]
                            parent_order_details = parent_component_order_details_list[-1] if parent_component_order_details_list else None
                            job_req_data = JobRequirementData(outside_service_routing_line=None,
                                                              purchased_component=component,
                                                              purchased_component_part_record=part,
                                                              raw_material_part_record=None,
                                                              raw_material_quantity=None,
                                                              assembly_component=self.current_assm_comp,
                                                              order_details=parent_order_details)
                            component_to_job_requirement_data_mapping[parent_component.id].append(job_req_data)

                    # Create the JobReq records for materials, outside service operations, and purchased components
                    for component in order_item.components:
                        order_details_list = component_to_order_details[component.id]
                        order_line_item = order_details_list[-1] if order_details_list else None
                        if order_line_item is None:
                            continue
                        job_req_data_objects = component_to_job_requirement_data_mapping[component.id]
                        for job_req_data in job_req_data_objects:
                            if self.erp_config.should_export_assemblies_with_duplicate_components:
                                self.current_assm_comp = job_req_data.assembly_component
                                order_detail_list = [job_req_data.order_details] if job_req_data.order_details else component_to_order_details[component.id]
                                for order_details in order_detail_list:
                                    with self.process_resource(e2.JobReq, component, order_details, job_req_data):
                                        pass
                            else:
                                with self.process_resource(e2.JobReq, component, order_line_item, job_req_data):
                                    pass

    def get_sales_id(self, order):
        sales_id = SalespersonProcessor().process_salesperson(order)
        return sales_id

    def get_account_data(self, order):
        business_name, erp_code, payment_terms, payment_terms_period, customer_notes, account_id, contact_id = \
            AccountProcessor.process_account_info(order)
        return account_id, business_name, contact_id, customer_notes, erp_code, payment_terms, payment_terms_period
