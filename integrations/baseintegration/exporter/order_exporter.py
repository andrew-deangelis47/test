from ...baseintegration.datamigration import logger
from ...baseintegration.exporter.exceptions import IntegrationNotImplementedError
from ...baseintegration.exporter import BaseExporter
from ...baseintegration.exporter.mixins.order_assembly_traversal_mixin import OrderAssemblyTraversalMixin
from ...baseintegration.integration import Integration
from ...baseintegration.utils import set_custom_formatter, reset_custom_formatter, should_time_out_integration_action_from_event, mark_action_as_failed, mark_action_as_completed, mark_action_as_cancelled
from ...baseintegration.integration.integration_export_report import IntegrationExportReport
from paperless.objects.integration_actions import IntegrationAction, ManagedIntegration
from paperless.objects.orders import Order


class OrderExporter(OrderAssemblyTraversalMixin, BaseExporter):
    """
    Defines how to move an order from Paperless to an ERP system. This should be overridden by a specific ERPOrderExporter
    """

    paperless_config = None

    def __init__(self, integration: Integration):
        super().__init__(integration)
        self.workcenter_mapping = None
        self.order = None
        self.success_message = ""
        logger.info("Instantiated the order exporter")
        self.listener = None
        self.integration_report: IntegrationExportReport = None
        self._register_listener()

    def run(self, order_num: int = None):
        """
        calling this method is what runs the exporter
        """
        if order_num:
            logger.info("Running single order")
            order: Order = Order.get(order_num)
            self.integration_report: IntegrationExportReport = IntegrationExportReport(self._integration, order)
            self._process_order(order)
        else:
            logger.info("Running order listener")
            new_order_number_action_uuid_pairs = self.listener.get_new()
            logger.info(f"{len(new_order_number_action_uuid_pairs)} new orders were found to export")
            for (order_num, uuid) in new_order_number_action_uuid_pairs:
                action = IntegrationAction.get(uuid)
                if not self._integration.integration_enabled:
                    logger.info("Integration currently disabled - skipping this run")
                    mark_action_as_cancelled(action, "Integration is currently off, skipping this run")
                    return
                try:
                    order = Order.get(order_num)
                    set_custom_formatter(self._integration, "order", str(order_num))
                    self.integration_report: IntegrationExportReport = IntegrationExportReport(self._integration, order)
                    self._process_order(order)
                    mark_action_as_completed(action, self.success_message)
                except Exception as e:
                    mark_action_as_failed(action, e, order_num)
                reset_custom_formatter(self._integration)

    def _process_order(self, order: Order) -> bool:
        """
        This is the main driver of the whole integration process. This needs to be overridden by the base class
        :return: The success status of the order processing
        """
        raise IntegrationNotImplementedError(f"_process_order() is not implemented for {self.__class__.__name__}")

    def _register_listener(self):
        self.listener = OrderIntegrationListener(self._integration)
        logger.info("Order listener was registered")


class OrderIntegrationListener:

    def __init__(self, integration):
        self.identifier = "export_order"
        self._integration = integration
        logger.info("Order export listener was instantiated")

    def get_new(self) -> list:
        logger.info("Checking for new orders")
        new_order_created_events = ManagedIntegration.event_list(uuid=self._integration.managed_integration_uuid, params={"event_type_in": "order.created"})
        new_order_created_events = sorted(
            new_order_created_events,
            key=lambda x: x.created_dt
        )
        new_order_number_action_uuid_pairs = []
        for event in new_order_created_events:
            logger.info("Creating integration action for new orders")
            entity_id = str(event.data["number"])

            ia = IntegrationAction(type=self.identifier, entity_id=entity_id)
            ia.create(managed_integration_uuid=self._integration.managed_integration_uuid)

            uuid = ia.uuid
            # get new integration action
            action = IntegrationAction.get(uuid)
            action.current_record_count = 1
            if not self._integration.test_mode and should_time_out_integration_action_from_event(event):
                message = f"NOTICE: Integration action export_order with order {action.entity_id} and action UUID {action.uuid} is older than 3 days, it will be timed out and not processed."
                action.status = "timed_out"
                action.status_message = message
                action.update()
                continue
            action.status = "in_progress"
            action.update()
            new_order_number_action_uuid_pairs.append((action.entity_id, action.uuid))
        return new_order_number_action_uuid_pairs
