from plex_v2.exporter.processors.approved_supplier_datasource import ApprovedSupplierDatasourceProcessor
from plex_v2.configuration import PlexConfig
from types import SimpleNamespace
from unittest.mock import create_autospec
from baseintegration.integration.integration_export_report import IntegrationExportReport
from paperless.objects.orders import Order, OrderItem, OrderComponent, OrderOperation
from plex_v2.factories.plex.approved_supplier_datasource import ApprovedSupplierDatasourceFactory
from plex_v2.objects.operations_mapping import OperationsMapping
from plex_v2.objects.approved_supplier_upload_datasource import ApprovedSupplierAddUpdateDatasource
from plex_v2.utils.export import ExportUtils


class TestApprovedSupplierDatasourceProcessor:

    def setup_method(self):
        integration_report = create_autospec(IntegrationExportReport)
        integration_report.update_table.return_value = True

        self.processor = ApprovedSupplierDatasourceProcessor(SimpleNamespace(
            erp_config=PlexConfig(),
            integration_report=integration_report
        ))

        self.approved_supplier = create_autospec(ApprovedSupplierAddUpdateDatasource)
        self.approved_supplier.Part_No = 'Part_No'
        self.approved_supplier.Operation_Code = 'Operation_Code'
        self.approved_supplier.Supplier_Code = 'Supplier_Code'
        self.component = create_autospec(OrderComponent)
        self.component.material_operations = []
        self.order_item = create_autospec(OrderItem)
        self.order_item.components = [self.component]
        self.order_item.order_items = [self.order_item]
        self.order = create_autospec(Order)
        self.order.order_items = [self.order_item]
        self.factory = create_autospec(ApprovedSupplierDatasourceFactory)
        self.factory.to_approved_suppliers.return_value = [self.approved_supplier]
        self.factory.to_approved_suppliers_from_material_op.return_value = [self.approved_supplier]
        self.operations_mapping = create_autospec(OperationsMapping)
        self.utils = create_autospec(ExportUtils)

        self.outside_operation = create_autospec(OrderOperation)
        self.outside_operation.is_outside_service = True
        self.inside_operation = create_autospec(OrderOperation)
        self.inside_operation.is_outside_service = False

    def test_approved_supplier_processor_creates_approved_supplier_if_outside_service_for_component(self):
        outside_operation = create_autospec(OrderOperation)
        outside_operation.is_outside_service = True
        self.utils.get_non_ignored_operations_for_component.return_value = [self.outside_operation]

        self.processor._process(
            self.order,
            self.factory,
            self.operations_mapping,
            self.utils
        )

        self.approved_supplier.create.assert_called_once()

    def test_approved_supplier_processor_does_not_create_approved_supplier_if_inside_service_for_component(self):
        self.utils.get_non_ignored_operations_for_component.return_value = []
        self.processor._process(
            self.order,
            self.factory,
            self.operations_mapping,
            self.utils
        )

        self.approved_supplier.create.assert_not_called()

    def test_approved_supplier_processor_creates_approved_supplier_for_material(self):
        material_op = create_autospec(OrderOperation)
        self.component.material_operations = [material_op]

        self.processor._process(
            self.order,
            self.factory,
            self.operations_mapping,
            self.utils
        )

        self.approved_supplier.create.assert_called_once()
