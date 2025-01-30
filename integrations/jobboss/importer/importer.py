from baseintegration.datamigration import logger
from baseintegration.importer.account_importer import AccountImporter
from baseintegration.importer.material_importer import MaterialImporter
from baseintegration.importer.purchased_component_importer import PurchasedComponentImporter
import jobboss.models as jb
from baseintegration.importer.vendor_importer import VendorImporter
from baseintegration.utils.custom_table import ImportCustomTable
from django.db.models import Q
from jobboss.importer.processors.vendor import VendorImportProcessor
from paperless.objects.components import Material
from jobboss.importer.processors.raw_material import MaterialImportProcessor, MaterialBulkPlaceholder, \
    MaterialBulkImportProcessor
from paperless.objects.customers import Account
from jobboss.importer.processors.accounts_contacts import AccountImportProcessor
from paperless.objects.components import PurchasedComponent
from jobboss.importer.processors.purchased_component import PurchasedComponentImportProcessor, \
    PurchasedComponentBulkPlaceholder, PurchasedComponentBulkImportProcessor
from baseintegration.importer.work_center_importer import WorkCenterImporter
from baseintegration.utils import Workcenter, OutsideService, Vendor
from jobboss.importer.processors.workcenter import WorkCenterImportProcessor
from baseintegration.importer.outside_service_importer import OutsideServiceImporter
from jobboss.importer.processors.outside_service import OutsideServiceImportProcessor
from baseintegration.utils import get_last_action_datetime_sql
from baseintegration.importer.repeat_part_importer import RepeatPartImporter
from typing import List, Set, Union
from baseintegration.utils.repeat_work_objects import Part, Header, MethodOfManufacture, Operation, \
    RequiredMaterials, Child, AddOn
from jobboss.importer.repeat_work_processors.repeat_part import RepeatPartProcessor
from jobboss.importer.repeat_work_processors.header import HeaderProcessor
from jobboss.importer.repeat_work_processors.account_contact import AccountContactProcessor
from jobboss.importer.repeat_work_processors.add_on import AddOnProcessor
from jobboss.importer.repeat_work_processors.method_of_manufacture import MethodOfManufactureProcessor
from jobboss.importer.repeat_work_processors.operation import OperationProcessor
from jobboss.importer.repeat_work_processors.required_material import RequiredMaterialProcessor
from jobboss.importer.repeat_work_processors.child import ChildProcessor
from datetime import datetime, timedelta
import json
from jobboss.utils.repeat_work_utils import create_all_sqlite_tables_if_not_exists, \
    insert_data_into_all_sqlite_tables, create_indexes_on_all_sqlite_tables
from .configuration import AccountImportConfig


class JobBossAccountImportListener:

    def __init__(self, integration):
        self.identifier = "import_account"
        self._integration = integration
        logger.info("Jobboss account import listener was instantiated")

    def get_new(self, bulk=False):
        logger.info("Checking for new accounts")
        customer_ids = set()
        date_to_search = get_last_action_datetime_sql(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        updated_customers_query_set = jb.Customer.objects.filter(last_updated__gt=date_to_search)
        for customer_id in updated_customers_query_set.values_list('customer', flat=True):
            customer_ids.add(customer_id)

        updated_address_query_set = jb.Address.objects.filter(last_updated__gt=date_to_search)
        for customer_id in updated_address_query_set.values_list('customer', flat=True):
            customer_ids.add(customer_id)

        updated_contacts_query_set = jb.Contact.objects.filter(last_updated__gt=date_to_search)
        for customer_id in updated_contacts_query_set.values_list('customer', flat=True):
            customer_ids.add(customer_id)
        # contacts can have no customers
        customer_ids.discard(None)
        logger.info(f"Found {str(len(customer_ids))} records to update")
        return customer_ids


class JobBossAccountImporter(AccountImporter):

    def _register_listener(self):
        self.listener = JobBossAccountImportListener(self._integration)
        logger.info("Registered JobBossAccountImportListener")

    def _register_default_processors(self):
        self.register_processor(Account, AccountImportProcessor)
        logger.info("Registered AccountImportProcessor")

    def _setup_erp_config(self):
        self.erp_config = AccountImportConfig(self._integration.config_yaml)

    def _process_account(self, account_id: str):  # noqa: C901
        logger.info(f"Processing JobBOSS customer id: {account_id}")
        with self.process_resource(Account, account_id):
            pass


class JobBossMaterialImportListener:

    def __init__(self, integration):
        self.identifier = "import_material"
        self._integration = integration

    def get_new(self, bulk=False):
        date_to_search = get_last_action_datetime_sql(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        material_codes = set()

        # Check for updated Material records
        updated_material_query_set = jb.Material.objects.filter(last_updated__gt=date_to_search)
        for material_id in updated_material_query_set.values_list('material', flat=True):
            material_codes.add(material_id)

        # Check for updated StockItem records
        stock_item_query_set = jb.StockItem.objects.filter(last_updated__gt=date_to_search)
        for stock_item in stock_item_query_set:
            logger.info("Found changes on the StockItem record. Querying parent Material id.")
            material_record = jb.Material.objects.filter(stock_item=stock_item.stock_item).first()
            if material_record is not None:
                material_codes.add(material_record.material)

        raw_stock_weight_query_set = jb.RawStockWeight.objects.filter(last_updated__gt=date_to_search)

        for raw_stock_weight in raw_stock_weight_query_set:
            logger.info(f"Underlying RawStockWeight:{raw_stock_weight.class_field} changed. "
                        f"Reimporting all related Material records")
            material_records = jb.Material.objects.filter(class_field=raw_stock_weight.class_field)
            """
            NOTE: RawStockWeight updates apply to the whole material "class" and therefore all materials that fall
            into the same class need their density updated.
            """
            if material_records is not None:
                for material_id in material_records.values_list('material', flat=True):
                    material_codes.add(material_id)

        return material_codes


class JobBossMaterialImporter(MaterialImporter):

    def _register_listener(self):
        self.listener = JobBossMaterialImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(Material, MaterialImportProcessor)
        self.register_processor(MaterialBulkPlaceholder, MaterialBulkImportProcessor)

    def check_custom_table_exists(self):
        materials_config = self._integration.config_yaml["Importers"]["materials"]
        should_include_material_dimensions = materials_config.get("should_include_material_dimensions", False)
        should_include_costs = materials_config.get("should_include_costs", False)
        should_include_vendor = materials_config.get("should_include_vendor", False)
        should_include_stock_item_dimensions = materials_config.get("should_include_stock_item_dimensions", False)
        should_include_shape_data = materials_config.get("should_include_shape_data", False)
        should_include_alloy_data = materials_config.get("should_include_alloy_data", False)
        should_include_densities = materials_config.get("should_include_densities", False)
        should_include_revision = materials_config.get("should_include_revision", False)
        should_include_pick_buy_indicator = materials_config.get("should_include_pick_buy_indicator", False)
        logger.info("We're creating a dictionary.")
        self.header_dict = {
            'jb_material_id': "Material",
            'mat_desc': "Description",
            'last_updated': "Date",
        }
        if should_include_material_dimensions:
            mat_dims_dict = {
                'IS_length': 0,
                'IS_width': 0,
                'IS_thickness': 0,
            }
            self.header_dict.update(mat_dims_dict)
        if should_include_costs:
            cost_dict = {
                'standard_cost': 0,
                'avg_cost': 0,
                'last_cost': 0,
                'cost_uofm': "Units",
                'stocked_uofm': "Units",
            }
            self.header_dict.update(cost_dict)
        if should_include_vendor:
            vendor_dict = {
                'primary_vendor': "Vendor",
            }
            self.header_dict.update(vendor_dict)
        if should_include_stock_item_dimensions:
            stock_item_dict = {
                'dimension1_name': "None",
                'dimension1': 0,
                'dimension2_name': "None",
                'dimension2': 0,
                'dimension3_name': "None",
                'dimension3': 0,
            }
            self.header_dict.update(stock_item_dict)
        if should_include_shape_data:
            shape_dict = {
                'mat_shape': "Shape",
                'mat_type': "Type",
                'shape': "Shape",
            }
            self.header_dict.update(shape_dict)
        if should_include_alloy_data:
            alloy_dict = {
                'alloy': "Alloy",
                'class': "Class",
            }
            self.header_dict.update(alloy_dict)
        if should_include_densities:
            alloy_dict = {
                'density': 0
            }
            self.header_dict.update(alloy_dict)
        if should_include_revision:
            revision_dict = {
                'rev': "Rev"
            }
            self.header_dict.update(revision_dict)
        if should_include_pick_buy_indicator:
            pick_buy_dict = {
                'pick_buy_indicator': "Pick_Buy_Indicator"
            }
            self.header_dict.update(pick_buy_dict)
        return ImportCustomTable.check_custom_header_custom_table_exists("jobboss_materials", self.header_dict, "jb_material_id")

    def _process_material(self, material_id: str):
        logger.info(f"Material id is {str(material_id)}")
        with self.process_resource(Material, material_id) as material:
            logger.info(f"Processed material {material}")
            pass

    def _bulk_process_material(self, material_ids: List[str]):
        with self.process_resource(MaterialBulkPlaceholder, material_ids) as success:
            logger.info(f"Bulk processed {len(material_ids)} materials")
            return success


class JobBossPurchasedComponentImportListener:

    def __init__(self, integration):
        self.identifier = "import_purchased_component"
        self._integration = integration

    def get_new(self, bulk=False):
        date_to_search = get_last_action_datetime_sql(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        updated_query_set = jb.Material.objects.filter(last_updated__gt=date_to_search)\
            .filter(Q(type='H') | Q(type='F') | Q(type='S'))
        return updated_query_set.values_list('material', flat=True)


class JobBossPurchasedComponentImporter(PurchasedComponentImporter):

    def _register_listener(self):
        self.listener = JobBossPurchasedComponentImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(PurchasedComponent, PurchasedComponentImportProcessor)
        self.register_processor(PurchasedComponentBulkPlaceholder, PurchasedComponentBulkImportProcessor)
        logger.info('Registered purchased component processor.')

    def _process_purchased_component(self, purchased_component_id: str):  # noqa: C901
        logger.info(f"Purchased component id is {str(purchased_component_id)}")
        with self.process_resource(PurchasedComponent, purchased_component_id):
            logger.info(f"Processed purchased component id: {purchased_component_id}")

    def _bulk_process_purchased_component(self, purchased_component_ids: List[str]):
        with self.process_resource(PurchasedComponentBulkPlaceholder, purchased_component_ids) as success:
            logger.info(f"Bulk processed {len(purchased_component_ids)} purchased components")
            return success


class JobBossWorkCenterImportListener:

    def __init__(self, integration):
        self.identifier = "import_work_center"
        self._integration = integration

    def get_new(self, bulk=False):
        date_to_search = get_last_action_datetime_sql(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        updated_query_set = jb.WorkCenter.objects.filter(last_updated__gt=date_to_search)
        return updated_query_set.values_list('work_center', flat=True)


class JobBossWorkCenterImporter(WorkCenterImporter):

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            self.table_name = "workcenters"
        else:
            self.table_name = "jobboss_workcenters"

    def _register_listener(self):
        self.listener = JobBossWorkCenterImportListener(self._integration)
        logger.info("Jobboss work center listener was registered")

    def _register_default_processors(self):
        self.register_processor(Workcenter, WorkCenterImportProcessor)
        logger.info('Registered work center processor.')

    def check_custom_table_exists(self):
        logger.info("We're creating a dictionary.")
        self.header_dict = {
            'work_center': "N/A",
            'type': "Indirect",
            'setup_labor_rate': 0,
            'run_labor_rate': 0,
            'labor_burden': 0,
            'machine_burden': 0,
            'ga_burden': 0
        }
        return ImportCustomTable.check_custom_header_custom_table_exists(self.table_name, self.header_dict,
                                                                         "work_center")

    def _process_work_center(self, work_center_id: str):
        logger.info(f"Work center id is {str(work_center_id)}")
        with self.process_resource(Workcenter, work_center_id):
            logger.info(f"Processed work center id: {work_center_id}")


class JobBossOutsideServiceImportListener:

    def __init__(self, integration):
        self.identifier = "import_service"
        self._integration = integration

    def get_new(self, bulk=False):
        date_to_search = get_last_action_datetime_sql(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        service_ids = set()

        updated_service_query_set = jb.Service.objects.filter(last_updated__gt=date_to_search)
        for service_id in updated_service_query_set.values_list('service', flat=True):
            service_ids.add(service_id)

        updated_vendor_service_query_set = jb.VendorService.objects.filter(last_updated__gt=date_to_search)
        for service_id in updated_vendor_service_query_set.values_list('service', flat=True):
            service_ids.add(service_id)

        return service_ids


class JobBossOutsideServiceImporter(OutsideServiceImporter):

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            self.table_name = "outside_services"
        else:
            self.table_name = "jobboss_outside_services"

    def _register_listener(self):
        self.listener = JobBossOutsideServiceImportListener(self._integration)
        logger.info("Jobboss outside service listener was registered")

    def _register_default_processors(self):
        self.register_processor(OutsideService, OutsideServiceImportProcessor)
        logger.info('Registered outside service processor.')

    def check_custom_table_exists(self):
        logger.info("We're creating a dictionary.")
        self.header_dict = {
            'jb_service': "No Service Id",
            'jb_vendor': "No Vendor Id",
            'lead_days': 0,
            'min_charge': 0,
            "service_description": "No Description",
            'osv_unique_key': "No Unique Key"
        }
        return ImportCustomTable.check_custom_header_custom_table_exists(self.table_name, self.header_dict,
                                                                         "osv_unique_key")

    def _process_outside_service(self, service_id: str):
        logger.info(f"Service id is {str(service_id)}")
        with self.process_resource(OutsideService, service_id):
            logger.info(f"Processed Service id: {service_id}")


class JobBossVendorImportListener:

    def __init__(self, integration):
        self.identifier = "import_vendor"
        self._integration = integration

    def get_new(self, bulk=False):
        date_to_search = get_last_action_datetime_sql(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        vendor_ids = set()

        updated_vendor_query_set = jb.Vendor.objects.filter(last_updated__gt=date_to_search)
        for vendor_id in updated_vendor_query_set.values_list('vendor', flat=True):
            vendor_ids.add(vendor_id)

        return vendor_ids


class JobBossVendorImporter(VendorImporter):

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            self.table_name = "vendors"
        else:
            self.table_name = "jobboss_vendors"

    def _register_listener(self):
        self.listener = JobBossVendorImportListener(self._integration)
        logger.info("Jobboss vendor listener was registered")

    def _register_default_processors(self):
        self.register_processor(Vendor, VendorImportProcessor)
        logger.info('Registered vendor processor.')

    def check_custom_table_exists(self):
        logger.info("We're creating a dictionary.")
        self.header_dict = {
            'jb_vendor_id': "No Vendor Id",
            'jb_vendor_name': "No Vendor Id",
        }
        return ImportCustomTable.check_custom_header_custom_table_exists(self.table_name, self.header_dict,
                                                                         "jb_vendor_id")

    def _process_vendor(self, vendor_id: str):
        logger.info(f"Vendor id is {str(vendor_id)}")
        with self.process_resource(Vendor, vendor_id):
            logger.info(f"Processed Vendor id: {vendor_id}")


class JobBossRepeatPartImportListener:

    def __init__(self, integration):
        self.identifier = "import_repeat_part"
        self._integration = integration
        self.total_part_objects = 0
        logger.info("Jobboss repeat import listener was instantiated")

    def get_new(self, bulk=False):  # noqa: C901
        date_to_search = get_last_action_datetime_sql(
            self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        hardware_date_to_search = datetime(year=1970, month=1, day=1)

        # If bulk mode, get everything, write everything to SQL
        if bulk is True:
            date_to_search = self._integration.config_yaml["Importers"]["repeat_part"].get(
                "get_quotes_and_jobs_newer_than", datetime.now() - timedelta(days=5 * 365))
            create_all_sqlite_tables_if_not_exists()
            insert_data_into_all_sqlite_tables()
            create_indexes_on_all_sqlite_tables()

        logger.info('Querying all new or updated Job and Quote records.')
        updated_quote_objects = jb.Quote.objects.filter(last_updated__gt=date_to_search).all()
        updated_job_objects = jb.Job.objects.filter(last_updated__gt=date_to_search).all()
        updated_quote_hardware_objects = jb.QuoteReq.objects.filter(last_updated__gt=hardware_date_to_search
                                                                    ).exclude(type="R").all()
        updated_job_hardware_objects = jb.MaterialReq.objects.filter(last_updated__gt=hardware_date_to_search
                                                                     ).exclude(type="R").all()

        unique_part_numbers_set = set()
        unique_part_numbers_set = self.get_updated_job_or_quote_part_numbers_list(unique_part_numbers_set, updated_quote_objects)
        unique_part_numbers_set = self.get_updated_job_or_quote_part_numbers_list(unique_part_numbers_set, updated_job_objects)
        unique_part_numbers_set = self.get_material_part_numbers_list(unique_part_numbers_set, updated_quote_hardware_objects)
        unique_part_numbers_set = self.get_material_part_numbers_list(unique_part_numbers_set, updated_job_hardware_objects)

        # "Continuous" mode listeners - need to listen for changes on associated records as well
        if bulk is False:
            updated_rfqs = jb.Rfq.objects.filter(last_updated__gt=date_to_search).all()
            if len(updated_rfqs) > 0:
                for rfq in updated_rfqs:
                    updated_quote_objects = jb.Quote.objects.filter(rfq=rfq.rfq).all()
                    unique_part_numbers_set = self.get_updated_job_or_quote_part_numbers_list(unique_part_numbers_set,
                                                                                              updated_quote_objects)

            updated_quote_qtys = jb.QuoteQty.objects.filter(last_updated__gt=date_to_search).all()
            if len(updated_quote_qtys) > 0:
                for quote_qty in updated_quote_qtys:
                    updated_quote_objects = jb.Quote.objects.filter(rfq=quote_qty.quote).all()
                    unique_part_numbers_set = self.get_updated_job_or_quote_part_numbers_list(unique_part_numbers_set,
                                                                                              updated_quote_objects)

            updated_quote_ops = jb.QuoteOperation.objects.filter(last_updated__gt=date_to_search).all()
            if len(updated_quote_ops) > 0:
                for quote_op in updated_quote_ops:
                    updated_quote_objects = jb.Quote.objects.filter(rfq=quote_op.quote).all()
                    unique_part_numbers_set = self.get_updated_job_or_quote_part_numbers_list(unique_part_numbers_set,
                                                                                              updated_quote_objects)

            updated_quote_op_qtys = jb.QuoteOperationQty.objects.filter(last_updated__gt=date_to_search).all()
            if len(updated_quote_op_qtys) > 0:
                updated_quote_ops = []
                for quote_op_qty in updated_quote_op_qtys:
                    updated_quote_ops.append(
                        jb.QuoteOperation.objects.filter(quote_operation=quote_op_qty.quote_operation).first()
                    )
                    if len(updated_quote_ops) > 0:
                        for quote_op in updated_quote_ops:
                            if quote_op is None:
                                continue
                            updated_quote_objects = jb.Quote.objects.filter(rfq=quote_op.quote).all()
                            unique_part_numbers_set = self.get_updated_job_or_quote_part_numbers_list(
                                unique_part_numbers_set,
                                updated_quote_objects)

            updated_quote_req_qtys = jb.QuoteReqQty.objects.filter(last_updated__gt=date_to_search).all()
            if len(updated_quote_req_qtys) > 0:
                updated_quote_reqs = []
                for quote_req_qty in updated_quote_req_qtys:
                    updated_quote_reqs.append(
                        jb.QuoteReq.objects.filter(quote_req=quote_req_qty.quote_req).first()
                    )
                    unique_part_numbers_set = self.get_material_part_numbers_list(unique_part_numbers_set,
                                                                                  updated_quote_reqs)

            updated_quote_addl_charges = jb.QuoteAddlCharge.objects.filter(last_updated__gt=date_to_search).all()
            if len(updated_quote_addl_charges) > 0:
                for quote_addl_charge in updated_quote_addl_charges:
                    updated_quote_objects = jb.Quote.objects.filter(quote=quote_addl_charge.quote).all()
                    unique_part_numbers_set = self.get_updated_job_or_quote_part_numbers_list(unique_part_numbers_set,
                                                                                              updated_quote_objects)

            updated_job_ops = jb.JobOperation.objects.filter(last_updated__gt=date_to_search).all()
            if len(updated_job_ops) > 0:
                for job_op in updated_job_ops:
                    updated_job_objects = jb.Job.objects.filter(job=job_op.job).all()
                    unique_part_numbers_set = self.get_updated_job_or_quote_part_numbers_list(unique_part_numbers_set,
                                                                                              updated_job_objects)

            updated_addl_charges = jb.AdditionalCharge.objects.filter(last_updated__gt=date_to_search).all()
            if len(updated_addl_charges) > 0:
                for addl_charge in updated_addl_charges:
                    updated_job_objects = jb.Job.objects.filter(job=addl_charge.job).all()
                    unique_part_numbers_set = self.get_updated_job_or_quote_part_numbers_list(unique_part_numbers_set,
                                                                                              updated_job_objects)

        self.total_part_objects = len(unique_part_numbers_set)
        logger.info(f"Found {self.total_part_objects} records to update")
        return unique_part_numbers_set

    def get_updated_job_or_quote_part_numbers_list(self, unique_part_numbers_set, quotes_jobs_list) -> Set[str]:
        updated_part_numbers_list = []
        for obj in quotes_jobs_list:
            updated_part_numbers_list.append((obj.part_number, obj.rev))
        self.update_unique_part_number_set(updated_part_numbers_list, unique_part_numbers_set)
        return unique_part_numbers_set

    def get_material_part_numbers_list(self, unique_part_numbers_set, material_req_list):
        updated_material_part_numbers_list = []
        for obj in material_req_list:
            if obj is None:
                continue
            updated_material_part_numbers_list.append(obj.material)
        self.update_unique_part_number_set(updated_material_part_numbers_list, unique_part_numbers_set)
        return unique_part_numbers_set

    def update_unique_part_number_set(self, part_numbers_list: List, unique_part_numbers_set: set):
        for part_number in part_numbers_list:
            unique_part_numbers_set.add(part_number)
        return unique_part_numbers_set


class JobBossRepeatPartImporter(RepeatPartImporter):
    split_id = True

    def _register_listener(self):
        self.listener = JobBossRepeatPartImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(Part, RepeatPartProcessor)
        self.register_processor(Header, HeaderProcessor)
        self.register_processor(Account, AccountContactProcessor)
        self.register_processor(AddOn, AddOnProcessor)
        self.register_processor(MethodOfManufacture, MethodOfManufactureProcessor)
        self.register_processor(Operation, OperationProcessor)
        self.register_processor(RequiredMaterials, RequiredMaterialProcessor)
        self.register_processor(Child, ChildProcessor)
        logger.info('Registered all repeat part processors.')

    def _process_repeat_part(self, repeat_part_id: Union[str, tuple[str, str]], create_child_parts: bool = False, is_root: bool = True):  # noqa: C901
        logger.info(f"Attempting to process {str(repeat_part_id)}")
        self.total_parts_processed += 1

        if repeat_part_id in self.processed_children_list:
            logger.info(
                f"Part id: {repeat_part_id} matches an existing part number that has already been processed."
                f" Skipping this component to prevent infinite loop."
            )
        else:
            self.processed_children_list.append(repeat_part_id)
            with self.process_resource(Part, repeat_part_id) as repeat_part_util_object:
                pass
            with self.process_resource(Header, repeat_part_util_object) as repeat_part_util_object:
                pass
            with self.process_resource(Account, repeat_part_util_object) as repeat_part_util_object:
                pass
            with self.process_resource(AddOn, repeat_part_util_object) as repeat_part_util_object:
                pass
            with self.process_resource(MethodOfManufacture, repeat_part_util_object) as repeat_part_util_object:
                pass
            with self.process_resource(Operation, repeat_part_util_object) as repeat_part_util_object:
                pass
            with self.process_resource(RequiredMaterials, repeat_part_util_object) as repeat_part_util_object:
                pass
            with self.process_resource(Child, repeat_part_util_object, create_child_parts) as repeat_part_json:
                pass

            json_string = json.dumps(repeat_part_json, indent=2)
            # print(json_string)  # This is only here as a util when needed for testing.

            if self.bulk_mode:
                if self.total_payload_size + self.get_json_payload_size(json_string) <= 2.5:  # Django API framework limit
                    logger.info("Part does not exceed allowable API payload size limit. Adding to batch.")
                    self.repeat_part_batch.append(repeat_part_json)
                    self.total_payload_size += self.get_json_payload_size(json_string)
                else:  # If the size is going to exceed 250 MB, post the batch before adding the new part to the batch
                    logger.info("Attempting to post batch of repeat parts.")
                    self.post_repeat_part_batch()
                    self.repeat_part_batch.append(repeat_part_json)
                    self.total_payload_size += self.get_json_payload_size(json_string)

                self.parts_remaining = self.listener.total_part_objects - self.total_parts_processed
                self.current_time = datetime.now()
                total_time_elapsed, time_since_last_post, est_time_remaining = self.get_time_metrics()
                logger.info(f"BATCH DATA:"
                            f"\nTotal part count:\t\t{self.listener.total_part_objects}\tParts"
                            f"\nParts in this batch:\t\t{len(self.repeat_part_batch)}\tParts"
                            f"\nThis payload size:\t\t{round(self.total_payload_size, 3)}\tMB"
                            f"\nParts remaining:\t\t{self.parts_remaining}\tParts"
                            f"\nTotal time elapsed:\t\t{total_time_elapsed}\t"
                            f"\nTime since last post:\t{time_since_last_post}\t"
                            f"\nEst. time remaining:\t{est_time_remaining}\t")
                # Post the final batch when the importer is done running
                if self.parts_remaining == 0:
                    self.post_repeat_part_batch()
                    should_persist_database_after_run = self._integration.config_yaml["Importers"]["repeat_part"].get(
                        "should_persist_database_after_run", False)
                    if should_persist_database_after_run is False:
                        self.delete_all_data()

            elif self._integration.config_yaml["Importers"]["repeat_part"].get("is_post_enabled", False):
                logger.info("Posting individual repeat part.")
                self.repeat_part_batch.append(repeat_part_json)
                self.post_repeat_part_batch()

            else:
                logger.info("Not posting repeat part batch. Config option 'is_post_enabled' is set to False.")

    def delete_all_data(self):
        logger.info("Data is not being dropped yet. Fix this.")
        # x = jb.QuoteOperationQty.objects.using('sqlite_copy').all()
        # x.delete()
        # x = jb.QuoteReqQty.objects.using('sqlite_copy').all()
        # x.delete()
        # x = jb.QuoteAddlCharge.objects.using('sqlite_copy').all()
        # x.delete()
        # x = jb.QuoteQty.objects.using('sqlite_copy').all()
        # x.delete()
        # x = jb.QuoteReq.objects.using('sqlite_copy').all()
        # x.delete()
        # x = jb.QuoteOperation.objects.using('sqlite_copy').all()
        # x.delete()
        # x = jb.BillOfQuotes.objects.using('sqlite_copy').all()
        # x.delete()
        # x = jb.Quote.objects.using('sqlite_copy').all()
        # x.delete()
        # x = jb.Rfq.objects.using('sqlite_copy').all()
        # x.delete()
        # logger.info("Dropped all quote related data.")
        #
        # x = jb.JobOperation.objects.using('sqlite_copy').all()
        # x.delete()
        # x = jb.MaterialReq.objects.using('sqlite_copy').all()
        # x.delete()
        # x = jb.AdditionalCharge.objects.using('sqlite_copy').all()
        # x.delete()
        # x = jb.BillOfJobs.objects.using('sqlite_copy').all()
        # x.delete()
        # x = jb.Job.objects.using('sqlite_copy').all()
        # x.delete()
        # logger.info("Dropped all job related data.")
        #
        # x = jb.Customer.objects.using('sqlite_copy').all()
        # x.delete()
        # x = jb.Material.objects.using('sqlite_copy').all()
        # x.delete()
        # logger.info("Dropped all materials and customers.")
