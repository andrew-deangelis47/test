from ...baseintegration.integration import Integration
import signal
from ...baseintegration.datamigration import logger
import sys
import types


def handler(signum, frame):
    print("Forever is over!")
    raise TimeoutError("end of time")


def generate_bogus_module(module_name, obj):
    bogus_module = types.ModuleType(module_name)
    sys.modules[module_name] = bogus_module
    setattr(bogus_module, obj.__name__, obj)


class TestIntegration:

    def test_integration(self, caplog):
        int = Integration()
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(5)
        int.run()
        assert "Scheduling tasks" in caplog.text

    def test_schedule_tasks(self, caplog):  # noqa: C901
        class CustomMaterialImporter:
            def __init__(self, integration):
                self.integration = integration

            def run(self):
                logger.info("Running material importer")

        class CustomAccountImporter:
            def __init__(self, integration):
                self.integration = integration

            def run(self):
                logger.info("Running account importer")

        class CustomPurchasedComponentImporter:
            def __init__(self, integration):
                self.integration = integration

            def run(self):
                logger.info("Running purchased component importer")

        class CustomWorkCenterImporter:
            def __init__(self, integration):
                self.integration = integration

            def run(self):
                logger.info("Running work center importer")

        class CustomVendorImporter:
            def __init__(self, integration):
                self.integration = integration

            def run(self):
                logger.info("Running vendor importer")

        class CustomOutsideServiceImporter:
            def __init__(self, integration):
                self.integration = integration

            def run(self):
                logger.info("Running outside service importer")

        class CustomQuoteExporter:
            def __init__(self, integration):
                self.integration = integration

            def run(self):
                logger.info("Running quote exporter")

        class CustomOrderExporter:
            def __init__(self, integration):
                self.integration = integration

            def run(self):
                logger.info("Running order exporter")

        generate_bogus_module("custom_material_importer", CustomMaterialImporter)
        generate_bogus_module("custom_purchased_component_importer", CustomPurchasedComponentImporter)
        generate_bogus_module("custom_account_importer", CustomAccountImporter)
        generate_bogus_module("custom_work_center_importer", CustomWorkCenterImporter)
        generate_bogus_module("custom_vendor_importer", CustomVendorImporter)
        generate_bogus_module("custom_outside_service_importer", CustomOutsideServiceImporter)
        generate_bogus_module("custom_quote_exporter", CustomQuoteExporter)
        generate_bogus_module("custom_order_exporter", CustomOrderExporter)
        int = Integration()
        int.config_yaml["Importers"] = {}
        int.config_yaml["Exporters"] = {}
        int.config_yaml["Importers"].update({"materials": {"interval": 0.1}})
        int.config_yaml["Importers"].update({"accounts": {"interval": 0.1}})
        int.config_yaml["Importers"].update({"purchased_components": {"interval": 0.1}})
        int.config_yaml["Importers"].update({"vendors": {"interval": 0.1}})
        int.config_yaml["Importers"].update({"work_centers": {"interval": 0.1}})
        int.config_yaml["Importers"].update({"outside_services": {"interval": 0.1}})
        int.config_yaml["Exporters"].update({"orders": {"interval": 0.1}})
        int.config_yaml["Exporters"].update({"quotes": {"interval": 0.1}})
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(10)
        int.run()
        assert "Running material importer" in caplog.text
        assert "Running account importer" in caplog.text
        assert "Running purchased component importer" in caplog.text
        assert "Running vendor importer" in caplog.text
        assert "Running work center importer" in caplog.text
        assert "Running outside service importer" in caplog.text
        assert "Running quote exporter" in caplog.text
        assert "Running order exporter" in caplog.text
