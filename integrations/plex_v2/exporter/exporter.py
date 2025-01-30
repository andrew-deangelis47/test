from baseintegration.exporter.order_exporter import OrderExporter
from paperless.objects.orders import Order, OrderItem
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from plex_v2.objects.customer import Customer
from plex_v2.objects.operations_mapping import OperationsMapping, OperationMapping
from plex_v2.configuration import ERPConfigFactory
from plex_v2.exporter.processors import CustomerProcessor, SalesOrderProcessor, PartProcessor, RoutingProcessor
from plex_v2.factories.plex import PlexCustomerFactory, SalesOrderFactory, PlexPartFactory, ApprovedShipToFactory, PartOperationFactory
from plex_v2.factories.paperless.operations_mapping_factory import OperationsMappingFactory, OperationMappingFactory
from plex_v2.objects.sales_orders import SalesOrder
from plex_v2.objects.part import Part
from plex_v2.objects.bom import BOMComponent
from plex_v2.objects.routing import PartOperation
from plex_v2.exporter.processors.bom import BomProcessor
from plex_v2.factories.plex.bom_component import BomComponentFactory
from plex_v2.factories.plex.customer_part import CustomerPartFactory
from plex_v2.exporter.processors.customer_part import CustomerPartProcessor
from plex_v2.objects.customer import CustomerPart
from plex_v2.factories.plex.approved_workcenter import ApprovedWorkCenterFactory
from plex_v2.exporter.processors.approved_workcenter import ApprovedWorkcenterProcessor
from plex_v2.objects.work_center_export import ApprovedWorkcenter
from plex_v2.factories.plex.sales_order_line import SalesOrderLineFactory
from plex_v2.factories.plex.sales_order_release import SalesOrderReleaseFactory
from plex_v2.objects.sales_orders import SalesOrderLine
from plex_v2.objects.plex_part_to_plex_customer_part_mapping import PlexPartToPlexCustomerPartMappings
from plex_v2.exporter.processors.sales_order_line import SalesOrderLineProcessor
from plex_v2.factories.plex.customer_contact import PlexCustomerContactFactory
from plex_v2.exporter.processors.customer_contact import ContactProcessor
from plex_v2.objects.customer import CustomerContact
from plex_v2.factories.plex.customer_address import PlexCustomerAddressFactory
from plex_v2.exporter.processors.customer_address import CustomerAddressProcessor
from plex_v2.objects.customer import CustomerAddress
from baseintegration.datamigration import logger
from plex_v2.exporter.processors.sales_order_release import SalesOrderReleaseProcessor
from plex_v2.objects.sales_orders import SalesOrderRelease
from plex_v2.factories.plex.sales_order_line_price import SalesOrderLinePriceFactory
from plex_v2.objects.sales_orders import SalesOrderLineApprovedShipTo
from plex_v2.exporter.processors.approved_ship_to import ApprovedShipToProcessor
from plex_v2.objects.approved_supplier_upload_datasource import ApprovedSupplierAddUpdateDatasource
from plex_v2.factories.plex.approved_supplier_datasource import ApprovedSupplierDatasourceFactory
from plex_v2.exporter.processors.approved_supplier_datasource import ApprovedSupplierDatasourceProcessor
from plex_v2.utils.export import ExportUtils
from baseintegration.utils.operations import OperationUtils
from plex_v2.factories.plex.part_operation_update_datasource import RoutingUpdateDatasourceFactory
from typing import List


class PlexV2OrderExporter(OrderExporter):

    def _register_default_processors(self):
        self.register_processor(Customer, CustomerProcessor)
        self.register_processor(SalesOrder, SalesOrderProcessor)
        self.register_processor(SalesOrderLine, SalesOrderLineProcessor)
        self.register_processor(Part, PartProcessor)
        self.register_processor(PartOperation, RoutingProcessor)
        self.register_processor(BOMComponent, BomProcessor)
        self.register_processor(CustomerPart, CustomerPartProcessor)
        self.register_processor(ApprovedWorkcenter, ApprovedWorkcenterProcessor)
        self.register_processor(CustomerContact, ContactProcessor)
        self.register_processor(CustomerAddress, CustomerAddressProcessor)
        self.register_processor(SalesOrderRelease, SalesOrderReleaseProcessor)
        self.register_processor(SalesOrderLineApprovedShipTo, ApprovedShipToProcessor)
        self.register_processor(ApprovedSupplierAddUpdateDatasource, ApprovedSupplierDatasourceProcessor)

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

        # 2) make sure payments are correct, account is there, and operations mapping table exists
        self.quote_number_with_revision = self._get_quote_number_with_revision(order)
        self.po_number = self._get_order_po_number(order)
        self.order_tier = self._get_plex_order_tier()
        self._ensure_contact_and_account_on_quote(order)

        # 3) set up util class
        self._setup_util_classes()

        # 4) get operations mapping object for easy access throughout export
        self.operations_mapping: OperationsMapping = self._get_operations_mapping()

        # 5) add the ignored operations list to config for easy access throughout export
        self.erp_config.routing_operation_to_ignore: List[str] = self._get_ignored_operation_definition_names()

        # 5) set up factories
        self._setup_factories()

        # 6) instantiate variables that the export process will be populating and referencing
        self.order = order
        self.customer: Customer
        self.customer_contact: CustomerContact
        self.sales_order: SalesOrder
        self.does_sales_order_already_exist: bool = False
        self.part_customer_part_mappings: PlexPartToPlexCustomerPartMappings
        self.plex_billing_address: CustomerAddress
        self.plex_shipping_address: CustomerAddress

        try:
            # Run any custom validation that should happen before the integration creates anything
            self._run_validation(order)

            self._process_customer()
            logger.info(f'Customer is {self.customer.code}\n')

            # get the existing sales order based on PO if it exists
            self.sales_order: SalesOrder = self.utils.get_existing_sales_order_by_po_number_and_customer(
                self.po_number,
                self.customer
            )

            if self.sales_order is not None:
                self.does_sales_order_already_exist = True
                logger.info(f'Found existing sales order po={self.sales_order.poNumber}, orderNo={self.sales_order.orderNumber}')

            self._process_shipping_and_billing_addresses()

            self._process_customer_contact()
            logger.info(f'Customer contact is {self.customer_contact.email}')

            self._process_parts()
            self._process_part_operations()
            self._process_approved_workcenters()
            self._process_approved_suppliers()
            self._process_bom_components()
            self._process_sales_order_and_sales_order_lines()

            # last but not least, write to the integration report table
            self.integration_report.update_table()

        except Exception as e:
            # if we get a failure we still want to make sure we write to the integration report
            logger.info(f'Unexpected exception: {str(e)}')
            self.integration_report.update_table()
            raise e

    def _get_ignored_operation_definition_names(self):
        """
        return list of ignored ops based on Operations_Mapping table
        """
        ignored_op_def_names: List[str] = []
        mapping: OperationMapping
        for mapping in self.operations_mapping.mappings:
            if mapping.paperless_only:
                ignored_op_def_names.append(mapping.pp_op_name)

        return ignored_op_def_names

    def _process_shipping_and_billing_addresses(self):
        # if there is an existing sales order use those addresses
        if self.sales_order is not None:

            self.plex_billing_address = self.utils.get_plex_billing_address_from_sales_order(self.sales_order)
            if self.plex_billing_address is None:
                self._process_billing_address()
            else:
                logger.info(f'Found matching billing address on order: {self.plex_billing_address.code if self.plex_billing_address is not None else None}')

            self.plex_shipping_address = self.utils.get_plex_shipping_address_from_sales_order(self.sales_order)
            if self.plex_shipping_address is None:
                self._process_shipping_address()
            else:
                logger.info(f'Found matching shipping address on order: {self.plex_shipping_address.code}')

        # otherwise grab shipping and billing from existing customer addresses
        else:
            self._process_billing_address()
            logger.info(f'Billing address code is "{self.plex_billing_address.code}"\n')

            self._process_shipping_address()
            logger.info(f'Shipping address code is {self.plex_shipping_address.code}')

        # ensure shipping address is valid - this would only be if we get them from an existing sales order
        if self.plex_shipping_address is not None:
            if not self.plex_shipping_address.shipTo:
                raise CancelledIntegrationActionException(f'The shipping address on the existing Plex order is not marked as ship to in Plex, code is "{self.plex_shipping_address}". Order number is {self.sales_order.orderNumber}. Please mark this address as ship to in order to add to this existing order.')

    def _process_sales_order_and_sales_order_lines(self):
        self._process_sales_order()

        if self._should_process_order_lines():
            self._process_sales_order_lines()
            if self.does_sales_order_already_exist:
                self.success_message = f'Did not create order, using existing order number {self.sales_order.orderNumber} because PO number matched and customer matched.'
            else:
                self.success_message = f'Sales order number {self.sales_order.orderNumber} was created in Plex.'
        else:
            self.success_message = f'Po Number for order already exists po number="{self.sales_order.poNumber}", order number="{self.sales_order.orderNumber}". Parts, Routing, and BOM were still processed for the parts in this order.'

    def _should_process_order_lines(self):
        """
        - determines whether or not the integration should process order lines
        - different customers want different behavior
        - if the order does not exist we always create the order line, otherwise it depends on the config
        """

        # 1) if the sales order does not already exist then always try to create
        if not self.does_sales_order_already_exist:
            return True

        # 2) otherwise the config option must be turned off to not create them
        if self.erp_config.should_create_order_lines_on_existing_order:
            logger.info('Creating order lines on existing order because should_create_order_lines_on_existing_order config option is turned on.')
        else:
            message = 'Not creating any order lines because it is turned off for existing orders. Contact support if you would like to turn this feature on.'
            logger.info(message)
            self.integration_report.add_message(SalesOrderLineProcessor.INTEGRATION_EXPORT_REPORT_COLUMN_NAME, message)

        return self.erp_config.should_create_order_lines_on_existing_order

    def _run_validation(self, order: Order) -> None:
        """
        If anything should be validated before the integration runs it should go here
        Example: check all part numbers to make sure they are not too long for Plex
        """
        pass

    def _ensure_contact_and_account_on_quote(self, order: Order):
        """
        simply ensuring we have a contact with an account with an ERP code before the integration runs
        the integration needs all of these
        """
        if order.contact is None:
            raise CancelledIntegrationActionException('No contact found on the order. Please add a contact to export this order to Plex.')
        if order.contact.account is None:
            raise CancelledIntegrationActionException('No account found for the contact on the order. Please associate the contact with an account to export this order.')
        if order.contact.account.erp_code is None:
            raise CancelledIntegrationActionException('No erp code found for the contact\'s account on the order. Please add an erp code to this account that matches the Plex customer code. Alternatively you can impport this account'
                                                      'to update the account\'s information. If a customer code is on the account in Plex, it will populate to the erp code field in the Paperless account during the import.')

    def _get_operations_mapping(self):
        operation_mapping_factory: OperationMappingFactory = OperationMappingFactory(self.erp_config, self.utils)
        operations_mapping_factory: OperationsMappingFactory = OperationsMappingFactory(self.erp_config, self.utils, operation_mapping_factory)
        return operations_mapping_factory.get_operations_mapping()

    def _setup_erp_config(self):
        self.erp_config, self.plex_client = ERPConfigFactory.create_config(self._integration)

    def _setup_util_classes(self):
        operations_utils = OperationUtils()
        self.utils: ExportUtils = ExportUtils(self.erp_config, operations_utils)

    def _setup_factories(self):
        self.customer_factory: PlexCustomerFactory = PlexCustomerFactory(self.erp_config, self.utils)
        self.sales_order_factory: SalesOrderFactory = SalesOrderFactory(self.erp_config, self.utils)
        self.approved_ship_to_factory: ApprovedShipToFactory = ApprovedShipToFactory(self.erp_config, self.utils)
        self.part_factory: PlexPartFactory = PlexPartFactory(self.erp_config, self.utils)
        self.operation_factory: PartOperationFactory = PartOperationFactory(self.erp_config, self.operations_mapping, self.utils)
        self.bom_component_factory: BomComponentFactory = BomComponentFactory(self.erp_config, self.utils)
        self.customer_part_factory: CustomerPartFactory = CustomerPartFactory(self.erp_config, self.utils)
        self.approved_workcenter_factory: ApprovedWorkCenterFactory = ApprovedWorkCenterFactory(self.erp_config, self.utils)
        self.sales_order_line_factory: SalesOrderLineFactory = SalesOrderLineFactory(self.erp_config, self.utils)
        self.sales_order_line_price_factory: SalesOrderLinePriceFactory = SalesOrderLinePriceFactory(self.erp_config, self.utils)
        self.sales_order_release_factory: SalesOrderReleaseFactory = SalesOrderReleaseFactory(self.erp_config, self.utils)
        self.customer_contact_factory: PlexCustomerContactFactory = PlexCustomerContactFactory(self.erp_config, self.utils)
        self.customer_address_factory: PlexCustomerAddressFactory = PlexCustomerAddressFactory(self.erp_config, self.utils)
        self.approved_supplier_factory: ApprovedSupplierDatasourceFactory = ApprovedSupplierDatasourceFactory(self.erp_config, self.utils)
        self.routing_update_datasource_factory: RoutingUpdateDatasourceFactory = RoutingUpdateDatasourceFactory(self.erp_config, self.operations_mapping, self.utils)

    def _get_quote_number_with_revision(self, order: Order) -> str:
        return f'{order.quote_number}{f"-{order.quote_revision_number}" if order.quote_revision_number is not None else ""} '

    def _get_order_po_number(self, order: Order) -> str:
        po_no = order.payment_details.purchase_order_number
        if po_no is None:
            return f'PO Missing (PP Order {order.number})'

        return po_no

    def _get_plex_order_tier(self) -> int:
        tier = self.erp_config.order_tier
        if tier == 2 or tier == 3:
            return int(tier)

        raise CancelledIntegrationActionException(f'Unrecognized Plex Sales Order tier in config: {tier}')

    def _process_customer(self) -> Customer:
        with self.process_resource(
                Customer,
                self.order.contact.account,
                self.utils,
                self.customer_factory
        ) as customer:
            self.customer = customer

    def _process_billing_address(self) -> CustomerAddress:
        billing_address: CustomerAddress
        with self.process_resource(
                CustomerAddress,
                self.customer,
                self.utils,
                self.customer_address_factory,
                self.order.billing_info,
                ['billTo', 'remitTo', 'soldTo'],
                'Billing'
        ) as billing_address:
            self.plex_billing_address = billing_address

    def _process_shipping_address(self) -> CustomerAddress:
        shipping_address: CustomerAddress
        with self.process_resource(
                CustomerAddress,
                self.customer,
                self.utils,
                self.customer_address_factory,
                self.order.shipping_info,
                ['shipTo'],
                'Shipping',
                self.plex_billing_address.id
        ) as shipping_address:
            self.plex_shipping_address = shipping_address

    def _process_customer_contact(self) -> CustomerContact:
        customer_contact: CustomerContact
        with self.process_resource(
                CustomerContact,
                self.order,
                self.customer,
                self.customer_contact_factory,
                self.utils
        ) as customer_contact:
            self.customer_contact = customer_contact

    def _process_sales_order(self):
        sales_order: SalesOrder
        with self.process_resource(
            SalesOrder,
            self.order,
            self.customer,
            self.order_tier,
            self.po_number,
            self.quote_number_with_revision,
            self.plex_billing_address.code,
            self.plex_shipping_address.code,
            self.utils,
            self.sales_order_factory
        ) as sales_order:
            self.sales_order = sales_order

    def _process_parts(self):
        try:
            with self.process_resource(
                    Part,
                    self.order,
                    self.utils,
                    self.part_factory
            ):
                pass
        except Exception as e:
            raise e

    def _process_part_operations(self):
        with self.process_resource(
            PartOperation,
            self.order,
            self.utils,
            self.operation_factory,
            self.routing_update_datasource_factory,
            self.operations_mapping
        ):
            pass

    def _process_approved_workcenters(self):
        if self.erp_config.should_create_approved_workcenters:
            with self.process_resource(
                    ApprovedWorkcenter,
                    self.order,
                    self.utils,
                    self.approved_workcenter_factory,
                    self.operations_mapping
            ):
                pass

    def _process_approved_suppliers(self):
        if self.erp_config.should_create_approved_suppliers:
            with self.process_resource(
                ApprovedSupplierAddUpdateDatasource,
                self.order,
                self.approved_supplier_factory,
                self.operations_mapping,
                self.utils
            ):
                pass

    def _process_bom_components(self):
        with self.process_resource(
                BOMComponent,
                self.order,
                self.utils,
                self.bom_component_factory
        ):
            pass

    def _process_sales_order_lines(self):
        # iterate order items - need all of these objects created for a succesful sales order export
        order_item: OrderItem
        line_no = 1
        for order_item in self.order.order_items:

            # customer part
            with self.process_resource(
                CustomerPart,
                order_item,
                self.customer,
                self.utils,
                self.customer_part_factory
            ) as part_customer_part_mapping:

                # sales order line + sales order line price
                with self.process_resource(
                    SalesOrderLine,
                    part_customer_part_mapping,
                    self.sales_order,
                    line_no,
                    self.sales_order_line_factory,
                    self.sales_order_line_price_factory
                ) as sales_order_line:

                    # sales order line approved ship to
                    with self.process_resource(
                        SalesOrderLineApprovedShipTo,
                        self.plex_shipping_address.id,
                        sales_order_line,
                        self.approved_ship_to_factory
                    ) as approved_ship_to:

                        # sales order release
                        with self.process_resource(
                            SalesOrderRelease,
                            order_item,
                            approved_ship_to.shipToAddressId,
                            sales_order_line,
                            self.sales_order_release_factory
                        ):
                            pass

            line_no += 1
