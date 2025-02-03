from types import SimpleNamespace
from typing import List

from baseintegration.integration import Integration
from dynamics.exceptions import RecognizedException
from dynamics.exporter.utils import get_failed_quote_instructions
from paperless.objects.quotes import Quote, QuoteComponent

from baseintegration.exporter.quote_exporter import QuoteExporter, logger

from dynamics.utils import DynamicsDataMigration
from dynamics.exporter.processors.customer import CustomerProcessor
from dynamics.exporter.processors.part import PartProcessor
from dynamics.exporter.processors.bom import BOMProcessor
from dynamics.exporter.processors.process_map import ProcessMapProcessor
from dynamics.exporter.processors.routing import RoutingProcessor
from dynamics.exporter.processors.sales_quote import SalesQuoteProcessor, SalesQuoteLineProcessor
from dynamics.objects.customer import Customer
from dynamics.client_factory import ClientFactory, ConfigFactory
from dynamics.objects.item import Item, Routing, ProductionBOM, ProcessMap, ProductionBOMItem
from dynamics.objects.sales_quote import SalesQuote, SalesQuoteLine
from dynamics.factories import ItemDataFactory
from baseintegration.utils.operations import OperationUtils
from dynamics.api_error_handler import DynamicsApiErrorHandler


class DynamicsQuoteExporter(QuoteExporter, DynamicsDataMigration):

    op_utils: OperationUtils = None
    item_data_factory: ItemDataFactory = None

    def __init__(self, integration: Integration):
        super().__init__(integration)
        self.salesperson = None

    def _register_default_processors(self):
        self.register_processor(Customer, CustomerProcessor)
        self.register_processor(Item, PartProcessor)
        self.register_processor(Routing, RoutingProcessor)
        self.register_processor(ProductionBOM, BOMProcessor)
        self.register_processor(ProcessMap, ProcessMapProcessor)
        self.register_processor(SalesQuote, SalesQuoteProcessor)
        self.register_processor(SalesQuoteLine, SalesQuoteLineProcessor)

    def process_part(self, customer: Customer, component: QuoteComponent, all_components: List[QuoteComponent]) -> Item:
        # setup API error handler
        api_error_handler = DynamicsApiErrorHandler()

        logger.info(f'Processing part {component.part_name} with part number {component.part_number}')

        with self.process_resource(Item, component) as part:
            if component.type != 'purchased':
                with self.process_resource(Routing, component, part, api_error_handler) as routing, \
                        self.process_resource(ProductionBOM, component, part, customer) as (bom, attempt_assembly):
                    if self.get_config_value('enable_ts_process_map'):
                        with self.process_resource(ProcessMap, customer, part, routing, bom):
                            pass
                    part: Item
                    bom: ProductionBOM

                    if attempt_assembly:
                        # recursively process child components, then add them to BOM
                        for child in component.children:
                            child_component = [
                                c for c in all_components if c.id == child.child_id
                            ][0]
                            child_part = self.process_part(customer, child_component, all_components)
                            component_type = "Item" if child_component.type == 'purchased' else "Production BOM"
                            ProductionBOMItem.create({
                                "Type": component_type,
                                "No": child_part.No,
                                "Production_BOM_No": bom.No,
                                "Quantity_per": child.quantity
                            })

            logger.info(f'Part {component.part_name} with part number {component.part_number} successfully processed!')
            return part

    def _process_quote(self, quote: Quote):

        try:
            self.salesperson = quote.salesperson and quote.salesperson.email
            with self.process_resource(Customer, quote.contact) as (customer, contact):
                # first process all the items
                quote_lines = []
                for quote_item in quote.quote_items:
                    component = quote_item.root_component
                    item = self.process_part(customer, component, quote_item.components)
                    quote_lines.append((item, component))
                # now create the quote and quote lines
                with self.process_resource(SalesQuote, quote, customer, contact) as sales_quote:
                    for (dynamics_item, item_component) in quote_lines:
                        with self.process_resource(SalesQuoteLine, sales_quote, dynamics_item, item_component):
                            pass
        except RecognizedException as e:
            self.send_error_email(e.email_message)
            raise e
        except Exception as e:
            email_message = f'An unknown error was encountered. Please {get_failed_quote_instructions()} If the issue' \
                            f' persists, please contact our support team.'
            self.send_error_email(email_message)
            raise e

        logger.info(f'Quote {self.quote_num} successfully exported!')

    def _setup_factories_and_utils(self):
        self.op_utils: OperationUtils = OperationUtils()
        self.item_data_factory: ItemDataFactory = ItemDataFactory(self.erp_config, self.op_utils)

    def _setup_erp_config(self):
        if self._integration.test_mode:
            self.erp_config = SimpleNamespace(
                should_create_customer=False,
                should_create_contact=False,
                enable_r_parts=True,
                enable_ts_processes_and_operations=True,
                enable_ts_process_map=True,
                pp_mat_id_variable='Material ID Selection',
                pp_coating_item_id_var='coating_no',
                pp_quantity_variable='Sheets Per Part',
                pp_machine_center_variable='workcenter',
                pp_process_selection_variable='Process Selection',
                pp_r_part_flag='Create R - Part in Dynamics?',
                pp_surface_area_variable='Surface Area, Sqft / pc',
                gen_bus_posting_group='DOMESTIC',
                customer_posting_group='DEFAULT',
                tax_area_code='NONTAX',
                base_unit_of_measure='PCS',
                gen_prod_posting_group='DEFAULT',
                inventory_posting_group='DEFAULT',
                tax_group_code='NONTAXABLE'
            )
        else:
            config_yaml = self._integration.config_yaml["Exporters"]["quotes"]
            self.erp_config = ConfigFactory.build_config(config_yaml)

        self.dynamics_client = ClientFactory.build_client_from_config(
            self._integration.secrets, self._integration.test_mode
        )

        # setup factories right after setting erp config
        self._setup_factories_and_utils()

    def send_error_email(self, msg):
        additional_recipients = []
        if self.salesperson:
            additional_recipients.append(self.salesperson)
        self.send_email(f"Integration for quote {self.quote_num} from Paperless Parts failed", msg,
                        additional_recipients=additional_recipients)
