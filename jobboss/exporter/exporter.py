from baseintegration.datamigration import logger
from baseintegration.integration import Integration
from baseintegration.utils import safe_get
from jobboss.exporter.configuration import JobBOSSConfig
from paperless.objects.orders import Order, OrderComponent
from paperless.objects.quotes import Quote
from jobboss.exporter.processors.so_header import SoHeaderProcessor
from jobboss.exporter.processors.material_master import MaterialProcessor
from jobboss.exporter.processors.job import JobProcessor
from jobboss.exporter.processors.attachment import AttachmentProcessor
from jobboss.exporter.processors.assembly import AssemblyProcessor
from jobboss.exporter.processors.material_req import MaterialReqProcessor
from jobboss.exporter.processors.so_detail import SoDetailProcessor
from jobboss.exporter.processors.delivery import DeliveryProcessor
from jobboss.exporter.processors.job_operation import JobOperationProcessor
from jobboss.exporter.processors.customer import CustomerProcessor
from jobboss.exporter.processors.address import AddressProcessor
from jobboss.exporter.processors.contact import ContactProcessor
from jobboss.exporter.processors.additional_charge import AddOnProcessor
from jobboss.exporter.processors.quote import QuoteProcessor
from baseintegration.exporter.order_exporter import OrderExporter
from baseintegration.exporter.quote_exporter import QuoteExporter
import jobboss.models as jb
import os
from jobboss.utils.utils import SuffixPosition
from jobboss.query.job import get_template_job, get_most_recent_job


class JobBossQuoteExporter(QuoteExporter):
    def _setup_erp_config(self):
        if not self._integration.test_mode:
            quote_parser = self._integration.config_yaml["Exporters"]["quotes"]
            self.erp_config = JobBOSSConfig(
                should_update_quote_erp_code_in_paperless_parts=quote_parser.get(
                    "should_update_quote_erp_code_in_paperless_parts", False
                )
            )
        else:
            self.erp_config = JobBOSSConfig(
                should_update_quote_erp_code_in_paperless_parts=False
            )
            os.environ.setdefault('TEST', "1")

    def _register_default_processors(self):
        self.register_processor(jb.Quote, QuoteProcessor)

    def _process_quote(self, quote: Quote):
        logger.info(f"Processing {quote.number}")
        with self.process_resource(jb.Quote, quote):
            logger.info(f"Quote {quote.number} was processed")


class JobBossOrderExporter(OrderExporter):
    def __init__(self, integration: Integration):
        super().__init__(integration)
        self.current_assm_comp = None

    def _setup_erp_config(self):
        logger.info('Reading config specific configuration file')
        if not self._integration.test_mode:
            parser = self._integration.config_yaml["Exporters"]["orders"]
            self.erp_config = JobBOSSConfig(
                sales_orders_active=parser.get('sales_orders_active', False),
                sales_order_default_status=parser.get('sales_order_default_status', "Hold"),
                should_link_addl_charge_to_sales_order_detail=parser.get(
                    'should_link_addl_charge_to_sales_order_detail', False
                ),
                sales_code=parser.get('sales_code', "PAPERLESS"),
                import_material=parser.get('import_material', True),
                default_location=parser.get('default_location', "SHOP"),
                import_operations=parser.get('import_operations', True),
                assign_runtime_and_setup_time_from_standard_op_variables=parser.get(
                    'assign_runtime_and_setup_time_from_standard_op_variables', False
                ),
                generate_material_ops=parser.get('generate_material_ops', True),
                use_default_materials=parser.get('use_default_materials', True),
                default_raw_material=parser.get('default_raw_material', "PPARTSDEFAULT"),
                default_hardware_material=parser.get('default_hardware_material', "PPARTS_PC"),
                pp_mat_id_variable=parser.get('pp_mat_id_variable', "Material ID"),
                pp_material_code_ops=parser.get('pp_material_code_ops', "Material Operation"),
                material_req_default_pick_or_buy=parser.get('material_req_default_pick_or_buy', "B"),
                import_job_as=parser.get('import_job_as', "Pending"),
                op_ignore=parser.get('op_ignore', "Part Level"),
                solo_mfg_comp_assembly=parser.get('solo_mfg_comp_assembly', False),
                assembly_conversion_should_adopt_top_level_part_number=parser.get(
                    'assembly_conversion_should_adopt_top_level_part_number', False
                ),
                hardware_is_top_level_only=parser.get('hardware_is_top_level_only', False),
                should_create_new_hardware_materials=parser.get('should_create_new_hardware_materials', False),
                generate_finished_good_material=parser.get('generate_finished_good_material', False),
                part_length_variable=parser.get('part_length_variable', "Part Length, in"),
                part_width_variable=parser.get('part_width_variable', "Part Width, in"),
                cutoff_variable=parser.get('cutoff_variable', "Cutoff, in"),
                facing_variable=parser.get('facing_variable', "Jobboss Facing"),
                standard_bar_end_variable=parser.get('standard_bar_end_variable', "Bar End in"),
                buy_item_description_variables=parser.get('buy_item_description_variables', "Joboss Bar Description"),
                buy_item_unit_cost=parser.get('buy_item_unit_cost', "Jobboss Unit Cost"),
                new_osv_method_enabled=parser.get('new_osv_method_enabled', True),  # note this has been deprecated
                osv_operations=parser.get('osv_operations', "Outside Services"),
                vendor_variable=parser.get('vendor_variable', "Vendor ID"),
                service_variable=parser.get('service_variable', "Service ID"),
                select_default_vendor=parser.get('select_default_vendor', "PPARTS"),
                parts_per_bar_variable=parser.get('parts_per_bar_variable', "Parts Per Sheet"),
                jb_calculator_qty=parser.get('jb_calculator_qty', "Jobboss Required Quantity"),
                is_rounded_variable=parser.get('is_rounded_variable', "Yes"),
                custom_table_op_map_enabled=parser.get('custom_table_op_map_enabled', True),
                default_work_center_name=parser.get('default_work_center_name', "WORKCENTER"),  # note this has been deprecated
                standard_work_center_variable_name=parser.get('standard_work_center_variable_name', "Jobboss Workcenter"),
                assembly_suffix_use_letters=parser.get('assembly_suffix_use_letters'),
                assembly_suffix_separator=parser.get('assembly_suffix_separator'),
                template_job_matching_enabled=parser.get('template_job_matching_enabled', False),
                part_number_job_matching_enabled=parser.get('part_number_job_matching_enabled', False),
                revision_must_match=parser.get('revision_must_match', False),
                enable_estimator_mapping=parser.get('enable_estimator_mapping', False),
                default_estimator=parser.get("default_estimator", "None"),
                estimator_mapping_table_name=parser.get("estimator_mapping_table_name", "estimator_mapping"),
                estimator_email_column_name=parser.get("estimator_email_column_name", "email"),
                estimator_jb_id_column_name=parser.get("estimator_jb_id_column_name", "jb_estimator_id"),
                should_assign_fg_to_parent=parser.get('should_assign_fg_to_parent', False),
                should_email_when_job_created=parser.get("should_email_when_job_created", False),
                email_subject=parser.get("email_subject", "Job Created"),
                email_body=parser.get("email_body", "A Job has been created from Paperless Parts into JobBOSS"),
                should_export_assemblies_with_duplicate_components=parser.get(
                    "should_export_assemblies_with_duplicate_components", False
                ),
                should_update_quote_line_status=parser.get('should_update_quote_line_status', False)
            )
        else:
            self.erp_config = JobBOSSConfig(
                sales_order_active=False,
                sales_orders_active=True,
                sales_order_default_status="Active",
                should_link_addl_charge_to_sales_order_detail=False,
                sales_code="PARTS",
                import_material=True,
                default_location="SHOP",
                import_operations=True,
                assign_runtime_and_setup_time_from_standard_op_variables=True,
                generate_material_ops=True,
                use_default_materials=False,
                default_raw_material="PPARTSDEFAULT",
                default_hardware_material="PPARTS_PC",
                pp_mat_id_variable="Material",
                pp_material_code_ops="Sheet | Laser",
                material_req_default_pick_or_buy="P",
                import_job_as="Active",
                op_ignore="DON'T IGNORE ANYTHING",
                solo_mfg_comp_assembly=False,
                assembly_conversion_should_adopt_top_level_part_number=False,
                hardware_is_top_level_only=False,
                should_create_new_hardware_materials=False,
                generate_finished_good_material=False,
                should_assign_fg_to_parent=False,
                part_length_variable="Part Len, In",
                part_width_variable="Part Width, In",
                cutoff_variable="Cutoff",
                facing_variable="Jobboss Facing",
                standard_bar_end_variable="Bar End",
                buy_item_description_variables="Joboss Bar Description",
                buy_item_unit_cost="Jobboss Unit Cost",
                new_osv_method_enabled=True,
                osv_operations="OUTSIDE SERVICE",
                vendor_variable="VENDOR",
                service_variable="SERVICE",
                select_default_vendor="PPARTS",
                parts_per_bar_variable="SHEET ALLOWANCE",
                jb_calculator_qty="Jobboss Required Quantity",
                is_rounded_variable="Jobboss Is Rounded",
                custom_table_op_map_enabled=False,
                default_work_center_name="WORKCENTER",
                standard_work_center_variable_name="Jobboss Workcenter",
                template_job_matching_enabled=False,
                part_number_job_matching_enabled=False,
                revision_must_match=False,
                enable_estimator_mapping=True,
                default_estimator="RLANCE",
                estimator_mapping_table_name="estimator_mapping",
                estimator_email_column_name="estim_email",
                estimator_jb_id_column_name="jb_employee_id",
                assembly_suffix_separator="-",
                should_email_when_job_created=False,
                email_subject="Job Created",
                email_body="A Job has been created",
                should_export_assemblies_with_duplicate_components=False,
                should_update_quote_line_status=False
            )
            os.environ.setdefault('TEST', "1")

    def _register_default_processors(self):
        self.register_processor(jb.Customer, CustomerProcessor)
        self.register_processor(jb.Address, AddressProcessor)
        self.register_processor(jb.Contact, ContactProcessor)
        self.register_processor(jb.SoHeader, SoHeaderProcessor)
        self.register_processor(jb.Attachment, AttachmentProcessor)
        self.register_processor(jb.Material, MaterialProcessor)
        self.register_processor(jb.Job, JobProcessor)
        self.register_processor(jb.BillOfJobs, AssemblyProcessor)
        self.register_processor(jb.MaterialReq, MaterialReqProcessor)
        self.register_processor(jb.SoDetail, SoDetailProcessor)
        self.register_processor(jb.Delivery, DeliveryProcessor)
        self.register_processor(jb.JobOperation, JobOperationProcessor)
        self.register_processor(jb.AdditionalCharge, AddOnProcessor)

    def process_top_level_job_only(self, order: Order, customer: jb.Customer, so_header: jb.SoHeader, comp, order_item, assm_comp, i,
                                   contact, top_level_job, top_level_router, processed_parents, ship_to=None, parent_price=0):
        logger.info('Creating top-level job only.')
        if not comp.type == 'manufactured':
            return None
        else:
            solo_mfg = True
            with self.process_resource(jb.Job, order, order_item, assm_comp, comp, so_header, top_level_job, customer,
                                       contact, processed_parents, i, ship_to, solo_mfg, parent_price) as job:
                suffix_position = SuffixPosition(assm_comp.level, assm_comp.level_index, assm_comp.level_count, job)
                processed_parents[comp.id] = suffix_position
                # Add order link and quote link to root component job
                with self.process_resource(jb.Attachment, order, None, job):

                    with self.process_resource(jb.MaterialReq, order_item, assm_comp, comp, job, top_level_job, processed_parents):
                        with self.process_resource(jb.SoDetail, comp, i, job, order_item,
                                                   so_header) as so_detail, \
                                self.process_resource(jb.Delivery, order_item, job, so_detail):
                            pass

                # now insert routing for operations
                if self.erp_config.import_operations:
                    with self.process_resource(jb.JobOperation, order_item, comp, job, top_level_router):
                        pass
                # Process add-ons for the order item
                with self.process_resource(jb.AdditionalCharge, order_item, comp, job, so_detail):
                    pass

                # Check if hardware should be added based on template matching features
                should_add_materials = self.should_add_materials(comp)

                # add hardware items as MaterialReqs (all remaining comps will be hardware)
                comp: OrderComponent
                for comp in order_item.components:
                    if not comp.is_hardware:
                        continue
                    # If template job matched above, do not add hardware twice for the matched mfg component.
                    if should_add_materials:
                        with self.process_resource(jb.MaterialReq, order_item, assm_comp, comp, job, top_level_job,
                                                   processed_parents):
                            pass

    def _process_order(self, order: Order):  # noqa: C901
        logger.info(f'Processing order {order.number}')
        with self.process_resource(jb.Customer, order) as customer:
            with self.process_resource(jb.Address, order, customer) as addresses:
                bill_to, ship_to = addresses
                with self.process_resource(jb.Contact, order, customer, bill_to) as contact, \
                        self.process_resource(jb.SoHeader, order, customer, ship_to, contact) as so_header:
                    pass

            parent_price = 0
            for i, order_item in enumerate(order.order_items):
                logger.debug(f'Starting order item {i}')
                top_level_job = None
                root_job = None
                comp_uuid = {}  # component ID -> JB object ID
                comp_job = {}  # component ID -> JB job instance
                processed_parents = {}

                # Get component counts to determine assembly handling
                mfg_comp_count, assm_comp_count, prch_comp_count = self.get_component_counts(order_item)

                if self.should_skip_order_item(order, order_item, customer, addresses, contact, so_header, i):
                    logger.info(f'Skipping order item {i} due to special condition.')
                    continue

                # create jobs for each mfg component and assembly
                top_level_router = []
                for assm_comp in self.iterate_assembly(order_item, self.erp_config.should_export_assemblies_with_duplicate_components):
                    comp: OrderComponent = assm_comp.component

                    with self.process_resource(jb.Material, order_item, comp):
                        pass

                    # Create the top-level job only
                    if mfg_comp_count == 1 and assm_comp_count == 1 and self.erp_config.solo_mfg_comp_assembly:
                        if comp.type == "assembled":
                            parent_price = order_item.unit_price.dollars
                            for op in comp.shop_operations:
                                top_level_router.append(op)
                        self.process_top_level_job_only(order, customer, so_header, comp,
                                                        order_item, assm_comp, i, contact,
                                                        top_level_job, top_level_router,
                                                        processed_parents, ship_to, parent_price)
                    # Create the standard routing structure
                    else:
                        logger.info('Creating standard assembly structure.')
                        # Run all manufactured component-related processors first, then handle materials/hardware
                        if not comp.is_hardware:
                            # Check if materials should be added based on template matching features
                            should_add_materials = self.should_add_materials(comp)
                            with self.process_resource(jb.Job, order, order_item, assm_comp, comp, so_header, top_level_job,
                                                       customer, contact, processed_parents, i, ship_to) as job:
                                with self.process_resource(jb.Attachment, order, so_header, job):
                                    pass

                                # Add namedtuple to dict of parent_ids for assembly naming and assigning finished goods
                                suffix_position = SuffixPosition(assm_comp.level, assm_comp.level_index, assm_comp.level_count, job)
                                processed_parents[comp.id] = suffix_position

                                if comp.is_root_component:
                                    root_job = job
                                # Iterate assembly guarantees first component is root component
                                if len(comp.child_ids) > 0:
                                    top_level_job = root_job
                                    # Add order link and quote link to root component job
                                    with self.process_resource(jb.Attachment, order, None, job):
                                        pass
                                comp_uuid[comp.id] = safe_get(job, 'objectid')
                                comp_job[comp.id] = job
                                with self.process_resource(jb.BillOfJobs, assm_comp, comp, comp_job, comp_uuid, job, root_job):

                                    # now insert routing for operations
                                    if self.erp_config.import_operations:
                                        with self.process_resource(jb.JobOperation, order_item, comp, job,
                                                                   top_level_router):
                                            pass
                            # For MFG components always add materials
                            # If template matching enabled, this will include hardware and it should be skipped below)
                            with self.process_resource(jb.MaterialReq, order_item, assm_comp, comp, job,
                                                       top_level_job, processed_parents):
                                pass

                        elif len(comp.parent_ids) > 0 and comp.parent_ids[0] in comp_job:
                            # For purchased component use parent id to find job -
                            # sometimes iterate_assembly is returning sub-assembly before purchased components that
                            # belong on root assembly.
                            logger.info(f'{comp.part_number} process resource using job with id {comp.parent_ids[0]}')
                            job = comp_job[comp.parent_ids[0]]

                        # Add hardware if the previous component did not already copy from a template job
                        if comp.is_hardware and should_add_materials:
                            with self.process_resource(jb.MaterialReq, order_item, assm_comp, comp, job, top_level_job,
                                                       processed_parents):
                                pass
                        if comp.is_root_component:
                            with self.process_resource(jb.SoDetail, comp, i, job, order_item,
                                                       so_header) as so_detail, \
                                    self.process_resource(jb.Delivery, order_item, job, so_detail):
                                with self.process_resource(jb.AdditionalCharge, order_item, comp, job, so_detail):
                                    pass

    @staticmethod
    def get_component_counts(order_item):
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
        return mfg_comp_count, assm_comp_count, prch_comp_count

    def should_skip_order_item(self, order, order_item, customer, addresses, contact, so_header, i):
        """
        Override this function in the custom_order_exporter.py if customer requires logic to skip order items:
        Example: "Skip the order item if the root component matches with a template job."
        Example: "Skip the order item if the process assigned to the quote is 'XYZ'."
        Return True for the condition in which you want the order item to skip.
        """
        return False

    def should_add_materials(self, comp: OrderComponent):
        """
        Check if any kind of template matching is enabled.
        If yes, check if a specific component returns a match.
        If yes, use the output to control whether or not hardware should be added to the mfg comp.
        """
        matching_part_number_job = None
        template_job = None
        if self.erp_config.template_job_matching_enabled:
            template_job = get_template_job(comp, self.erp_config)
        if self.erp_config.part_number_job_matching_enabled:
            matching_part_number_job = get_most_recent_job(comp, self.erp_config)
        if matching_part_number_job is not None or template_job is not None:
            return False
        return True
