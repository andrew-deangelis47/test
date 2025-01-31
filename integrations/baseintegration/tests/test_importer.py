from ...baseintegration.importer import BaseImporter
from ...baseintegration.importer.material_importer import MaterialImporter
from ...baseintegration.importer.account_importer import AccountImporter
from ...baseintegration.importer.purchased_component_importer import PurchasedComponentImporter
from ...baseintegration.importer.vendor_importer import VendorImporter
from ...baseintegration.importer.work_center_importer import WorkCenterImporter
from ...baseintegration.importer.outside_service_importer import OutsideServiceImporter
from ...baseintegration.importer.import_processor import BaseImportProcessor
from test_processor import ERPResource
import pytest
from ...baseintegration.integration import Integration
from ...baseintegration.exporter.exceptions import IntegrationNotImplementedError
import requests_mock
from typing import List


def register_mocks(mocker, int_id):
    mocker.post(
        f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}/integration_actions",
        text='{"type": '
             '"test",'
             '"uuid": '
             '"abc-123",'
             '"updated": "2021-11-30T17:09:39.052737Z",'
             '"created": "2021-11-30T17:08:41.811913Z",'
             '"status": "queued",'
             '"status_message": '
             'null,"entity_id": '
             '"1"}',
        status_code=200)
    mocker.get(
        "https://release.paperlessparts.com/api/integration_actions/public/abc-123",
        text='{"type": '
             '"test",'
             '"uuid": '
             '"abc-123",'
             '"updated": "2021-11-30T17:09:39.052737Z",'
             '"created": "2021-11-30T17:08:41.811913Z",'
             '"status": "queued",'
             '"status_message": '
             'null,"entity_id": '
             '"1"}',
        status_code=200)
    mocker.patch(
        "https://release.paperlessparts.com/api/integration_actions/public/abc-123",
        text='{"type": '
             '"test",'
             '"uuid": '
             '"abc-123",'
             '"status": "in_progress",'
             '"status_message": '
             'null,"entity_id": '
             '"1"}',
        status_code=200)
    return mocker


class UnchangedImportProcessor(BaseImportProcessor):
    pass


class ImplementedImportProcessor(BaseImportProcessor):
    def _process(self, *args, **kwargs):
        return 0


class RunnableImporter(BaseImporter):

    def __init__(self, integration):
        super().__init__(integration)

    def run(self):
        # shouldn't throw an error
        return 0

    def _register_listener(self):
        pass


class RunnableMaterialImporter(MaterialImporter):

    def __init__(self, integration):
        super().__init__(integration)

    def _register_listener(self):
        class Listener:
            def get_new(self, bulk=False):
                return ["blah"]

        self.listener = Listener()

    def _process_material(self, material_id: str) -> bool:
        return True

    def _bulk_process_material(self, material_ids: List[str]) -> bool:
        return True

    def check_custom_table_exists(self):
        return True


class RunnableVendorImporter(VendorImporter):

    def __init__(self, integration):
        super().__init__(integration)

    def _register_listener(self):
        class Listener:
            def get_new(self, bulk=False):
                return ["blah"]

        self.listener = Listener()

    def _process_vendor(self, vendor_id: str) -> bool:
        return True

    def _bulk_process_vendor(self, vendor_ids: List[str]) -> bool:
        return True

    def check_custom_table_exists(self):
        return True


class RunnableWorkCenterImporter(WorkCenterImporter):

    def __init__(self, integration):
        super().__init__(integration)

    def _register_listener(self):
        class Listener:
            def get_new(self, bulk=False):
                return ["blah"]

        self.listener = Listener()

    def _process_work_center(self, work_center_id: str) -> bool:
        return True

    def _bulk_process_work_center(self, work_center_ids: List[str]) -> bool:
        return True

    def check_custom_table_exists(self):
        return True


class RunnablePurchasedComponentImporter(PurchasedComponentImporter):

    def __init__(self, integration):
        super().__init__(integration)

    def _register_listener(self):
        class Listener:
            def get_new(self, bulk=False):
                return ["blah"]

        self.listener = Listener()

    def _process_purchased_component(self, purchased_component_id: str) -> bool:
        return True

    def _bulk_process_purchased_component(self, purchased_component_ids: List[str]) -> bool:
        return True


class RunnableAccountImporter(AccountImporter):

    def __init__(self, integration):
        super().__init__(integration)

    def _register_listener(self):
        class Listener:
            def get_new(self, bulk=False):
                return ["blah"]

        self.listener = Listener()

    def _process_account(self, account_id: str) -> bool:
        return True


class RunnableOutsideServiceImporter(OutsideServiceImporter):

    def __init__(self, integration):
        super().__init__(integration)

    def _register_listener(self):
        class Listener:
            def get_new(self, bulk=False):
                return ["blah"]

        self.listener = Listener()

    def check_custom_table_exists(self):
        return True

    def _process_outside_service(self, service_id: str) -> bool:
        return True

    def _bulk_process_outside_services(self, service_ids: List[str]) -> bool:
        return True


class TestImporter:

    def test_run_base_importer(self):
        with pytest.raises(IntegrationNotImplementedError):
            BaseImporter(Integration())

    def test_process_importer(self):
        importer = RunnableImporter(Integration())
        importer.register_processor(ERPResource, BaseImportProcessor)
        importer.run()

    def test_process_resource(self):
        importer = RunnableImporter(Integration())
        importer.register_processor(ERPResource, ImplementedImportProcessor)
        with importer.process_resource(ERPResource, 1) as resource:
            assert resource is not None

    def test_import_processor(self):
        importer = RunnableImporter(Integration())
        processor = BaseImportProcessor(importer)
        with pytest.raises(ValueError):
            processor.run()

    def test_material_importer(self):
        with pytest.raises(IntegrationNotImplementedError):
            MaterialImporter(Integration())
        runnable_material_importer = RunnableMaterialImporter(Integration())
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m, runnable_material_importer._integration.managed_integration_uuid)
            runnable_material_importer.run(material_id="blah")
            runnable_material_importer.run()
            runnable_material_importer._integration.config_yaml['Importers'] = {}
            runnable_material_importer._integration.config_yaml['Importers']['material'] = {}
            runnable_material_importer._integration.config_yaml['Importers']['material']['bulk_enable'] = True
            runnable_material_importer.run(material_id="blah")
            runnable_material_importer.run()

    def test_vendor_importer(self):
        with pytest.raises(IntegrationNotImplementedError):
            VendorImporter(Integration())
        runnable_vendor_importer = RunnableVendorImporter(Integration())
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m, runnable_vendor_importer._integration.managed_integration_uuid)
            runnable_vendor_importer.run(vendor_id="blah")
            runnable_vendor_importer.run()
            runnable_vendor_importer._integration.config_yaml['Importers'] = {}
            runnable_vendor_importer._integration.config_yaml['Importers']['vendor'] = {}
            runnable_vendor_importer._integration.config_yaml['Importers']['vendor']['bulk_enable'] = True
            runnable_vendor_importer.run(vendor_id="blah")
            runnable_vendor_importer.run()

    def test_work_center_importer(self):
        with pytest.raises(IntegrationNotImplementedError):
            WorkCenterImporter(Integration())
        runnable_work_center_importer = RunnableWorkCenterImporter(Integration())
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m, runnable_work_center_importer._integration.managed_integration_uuid)
            runnable_work_center_importer.run(work_center_id="blah")
            runnable_work_center_importer.run()
            runnable_work_center_importer._integration.config_yaml['Importers'] = {}
            runnable_work_center_importer._integration.config_yaml['Importers']['work_centers'] = {}
            runnable_work_center_importer._integration.config_yaml['Importers']['work_centers']['bulk_enable'] = True
            runnable_work_center_importer.run(work_center_id="blah")
            runnable_work_center_importer.run()

    def test_account_importer(self):
        with pytest.raises(IntegrationNotImplementedError):
            AccountImporter(Integration())
        runnable_account_importer = RunnableAccountImporter(Integration())
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m, runnable_account_importer._integration.managed_integration_uuid)
            runnable_account_importer.run(account_id="blah")
            runnable_account_importer.run()

    def test_purchased_component_importer(self):
        with pytest.raises(IntegrationNotImplementedError):
            PurchasedComponentImporter(Integration())
        runnable_purchased_component_importer = RunnablePurchasedComponentImporter(Integration())
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m, runnable_purchased_component_importer._integration.managed_integration_uuid)
            runnable_purchased_component_importer.run(purchased_component_id="blah")
            runnable_purchased_component_importer.run()
            runnable_purchased_component_importer._integration.config_yaml['Importers'] = {}
            runnable_purchased_component_importer._integration.config_yaml['Importers']['purchased_components'] = {}
            runnable_purchased_component_importer._integration.config_yaml['Importers']['purchased_components'][
                'bulk_enable'] = True
            runnable_purchased_component_importer.run(purchased_component_id="blah")
            runnable_purchased_component_importer.run()

    def test_outside_service_importer(self):
        with pytest.raises(IntegrationNotImplementedError):
            OutsideServiceImporter(Integration())
        runnable_outside_service_importer = RunnableOutsideServiceImporter(Integration())
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m, runnable_outside_service_importer._integration.managed_integration_uuid)
            runnable_outside_service_importer.run(service_id="blah")
            runnable_outside_service_importer.run()
            runnable_outside_service_importer._integration.config_yaml['Importers'] = {}
            runnable_outside_service_importer._integration.config_yaml['Importers']['outside_services'] = {}
            runnable_outside_service_importer._integration.config_yaml['Importers']['outside_services'][
                'bulk_enable'] = True
            runnable_outside_service_importer.run(service_id="blah")
            runnable_outside_service_importer.run()
