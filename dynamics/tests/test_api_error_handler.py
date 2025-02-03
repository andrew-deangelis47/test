from unittest.mock import create_autospec
from unittest import TestCase
from dynamics.exceptions import DynamicsException
from dynamics.api_error_handler import DynamicsApiErrorHandler
from paperless.objects.quotes import QuoteComponent
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException


class TestApiErrorHandler(TestCase):

    def setUp(self) -> None:
        self.error_handler = DynamicsApiErrorHandler()
        self.quote_component = create_autospec(QuoteComponent)
        self.quote_component.part_number = '123'
        self.process_name = 'process_name'
        self.table_name = 'table_name'
        self.invalid_process_error = f"'The field Process Name of table Routing Header contains a value ({self.process_name}) that cannot be found in the related table ({self.table_name}).  CorrelationId:  567.'}}"
        self.unrecognized_exception_message = 'test unrecognized exception message'

    def test_returns_readable_error_if_invalid_process_on_routing(self):

        exception = DynamicsException(self.invalid_process_error)

        # this should throw an error with a readable message
        expected_exception_message = f'Error trying to update routing for part {self.quote_component.part_number}. The process "{self.process_name}" does not exist in the Dynamics table "{self.table_name}"'
        try:
            self.error_handler.handle_routing_update_error(exception, self.quote_component)
        except CancelledIntegrationActionException as ex:
            assert expected_exception_message == str(ex)

    def test_returns_original_error_message_if_error_not_recognized(self):
        exception = DynamicsException(self.unrecognized_exception_message)

        # this should throw an exception with the same message as what's in the exception
        try:
            self.error_handler.handle_routing_update_error(exception, self.quote_component)
        except CancelledIntegrationActionException as ex:
            assert self.unrecognized_exception_message == str(ex)
