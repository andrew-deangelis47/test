from ...baseintegration.exporter import BaseExporter
from ...baseintegration.datamigration import logger
from ...baseintegration.exporter.exceptions import IntegrationNotImplementedError
from ...baseintegration.exporter.mixins.assembly_traversal_mixin import AssemblyTraversalMixin
from ...baseintegration.integration import Integration
from ...baseintegration.utils import set_custom_formatter, reset_custom_formatter, should_time_out_integration_action_from_event, mark_action_as_failed, mark_action_as_completed, mark_action_as_cancelled
from ...baseintegration.integration.integration_export_report import IntegrationExportReport
from paperless.objects.quotes import Quote
from paperless.objects.integration_actions import IntegrationAction, ManagedIntegration


class QuoteExporter(AssemblyTraversalMixin, BaseExporter):
    """
    Defines how to move a quote from Paperless to an ERP system. This should be overridden by a specific ERPOrderExporter
    """

    def __init__(self, integration: Integration):
        super().__init__(integration)
        logger.info("Instantiated the quote exporter")
        self.quote_num = 'UNKNOWN'
        self.success_message = ""
        self.listener = None
        self._register_listener()
        self.integration_report: IntegrationExportReport = None

    def _process_quote(self, quote: Quote):
        """
        This is the main driver of the whole integration process. This needs to be overridden by the base class
        :return:
        """
        raise IntegrationNotImplementedError(f"_process_quote is not implemented for {self.__class__.__name__}")

    def _extract_quote_from_string(self, quote_num: str) -> Quote:
        # check if revision
        try:
            num = int(quote_num.split("-")[0])
            quote_revision = int(quote_num.split("-")[1])
            return Quote.get(id=num, revision=quote_revision)
        except:
            return Quote.get(int(quote_num))

    def run(self, quote_num: str = None):
        if quote_num and quote_num.startswith('Daterange:'):
            return self._process_quote(quote_num)

        # you must pass in quote_num to the runner as "120-1" if you would like a revision
        if quote_num:
            quote = self._extract_quote_from_string(quote_num)
            logger.info("Running single quote")
            self.integration_report: IntegrationExportReport = IntegrationExportReport(self._integration, quote)
            self.quote_num = quote_num
            self._process_quote(quote)
        else:
            logger.info("Running quote listener")
            new_quote_number_action_uuid_pairs = self.listener.get_new()
            logger.info(f"{len(new_quote_number_action_uuid_pairs)} new quotes were found to export")
            for (quote_num, uuid) in new_quote_number_action_uuid_pairs:
                action = IntegrationAction.get(uuid)
                if not self._integration.integration_enabled:
                    logger.info("Integration currently disabled - skipping this run")
                    mark_action_as_cancelled(action, "Integration is currently off, skipping this run")
                    return
                try:
                    quote = self._extract_quote_from_string(quote_num)
                    set_custom_formatter(self._integration, "quote", str(quote_num))
                    self.quote_num = quote_num
                    self.integration_report: IntegrationExportReport = IntegrationExportReport(self._integration, quote)
                    self._process_quote(quote)
                    mark_action_as_completed(action, self.success_message)
                except Exception as e:
                    mark_action_as_failed(action, e, quote_num)
                reset_custom_formatter(self._integration)

    def _register_listener(self):
        self.listener = QuoteIntegrationListener(self._integration)
        logger.info("Quote listener was registered")


class QuoteIntegrationListener:

    def __init__(self, integration):
        self.identifier = "export_quote"
        self._integration = integration
        logger.info("Quote export listener was instantiated")

    def get_new(self) -> list:
        new_quote_sent_events = ManagedIntegration.event_list(uuid=self._integration.managed_integration_uuid, params={"event_type_in": "quote.sent"})
        new_quote_sent_events = sorted(
            new_quote_sent_events,
            key=lambda x: x.created_dt
        )
        new_quote_action_uuid_pairs = []
        for event in new_quote_sent_events:
            logger.info("Creating integration action for new quotes")
            if event.data["revision_number"]:
                entity_id = str(event.data["number"]) + "-" + str(event.data["revision_number"])
            else:
                entity_id = str(event.data["number"])

            ia = IntegrationAction(type=self.identifier, entity_id=str(entity_id))
            ia.create(managed_integration_uuid=self._integration.managed_integration_uuid)

            uuid = ia.uuid
            # get new integration action
            action = IntegrationAction.get(uuid)
            action.current_record_count = 1
            if not self._integration.test_mode and should_time_out_integration_action_from_event(event):
                message = f"NOTICE: Integration action export_quote with quote {action.entity_id} and action UUID {action.uuid} is older than 3 days, it will be timed out and not processed."
                action.status = "timed_out"
                action.status_message = message
                action.update()
                continue
            action.status = "in_progress"
            action.update()
            new_quote_action_uuid_pairs.append((action.entity_id, action.uuid))
        return new_quote_action_uuid_pairs
