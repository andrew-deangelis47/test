from baseintegration.exporter.order_exporter import OrderExporter
from paperless.objects.orders import Order
from m2m.configuration import ERPDBConfigFactory, M2MConfiguration
from m2m.exporter.processors.orders import ProcessOrder
from m2m.models import Qtmast


class M2MOrderExporter(OrderExporter):
    """An integration config specific to m2m"""
    m2m_config = M2MConfiguration()

    def _setup_erp_config(self):
        self.erp_config, self.m2m_config = ERPDBConfigFactory.create_configs(self._integration)

    def _register_default_processors(self):
        self.register_processor(Qtmast, ProcessOrder)

    def _process_order(self, order: Order):
        with self.process_resource(Qtmast, order, self.m2m_config):
            return True
