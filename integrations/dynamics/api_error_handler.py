from dynamics.exceptions import DynamicsException
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from paperless.objects.quotes import QuoteComponent


class DynamicsApiErrorHandler:
    """
    the idea here is that this class can consume Dynamics exceptions, determine if we know what the error means, then return a more readable error to
    the integration manager
    """

    # these are substrings we can look for in error messages to know what they mean and make it more readable for the end user
    ROUTING_ERROR_INVALID_PROCESS_NAME_ERROR_MESSAGES = [
        'The field Process Name of table Routing Header contains a value (',
        ') that cannot be found in the related table (',
        ').  CorrelationId'
    ]

    def handle_routing_update_error(self, ex: DynamicsException, component: QuoteComponent):

        # as we build this out we can add more 'recognized exceptions' like below
        is_routing_invalid_process, process_name, table_name = self._is_routing_invalid_process_error(ex)
        if is_routing_invalid_process:
            raise CancelledIntegrationActionException(f'Error trying to update routing for part {component.part_number}. The process "{process_name}"'
                                                      f' does not exist in the Dynamics table "{table_name}"')

        # if it's not a recognized error just throw the normal exception with the error
        raise CancelledIntegrationActionException(str(ex))

    def _is_routing_invalid_process_error(self, ex: DynamicsException) -> bool:
        """
        returns True if the exception message contains known substrings for invalid process error
        if True it also returns the process and the db table
        """
        for substring in self.ROUTING_ERROR_INVALID_PROCESS_NAME_ERROR_MESSAGES:
            if substring not in str(ex):
                return False, None, None

        # if we cant get the process name we will just treat it as an unrecognized error
        process_name = self.get_substring_between(str(ex), self.ROUTING_ERROR_INVALID_PROCESS_NAME_ERROR_MESSAGES[0], self.ROUTING_ERROR_INVALID_PROCESS_NAME_ERROR_MESSAGES[1])
        if process_name is None:
            return False, None, None

        # if we cant get the table name we will just treat it as an unrecognized error
        table_name = self.get_substring_between(str(ex), self.ROUTING_ERROR_INVALID_PROCESS_NAME_ERROR_MESSAGES[1], self.ROUTING_ERROR_INVALID_PROCESS_NAME_ERROR_MESSAGES[2])

        if table_name is None:
            return False, None, None

        return True, process_name, table_name

    def get_substring_between(self, original_string: str, start_str: str, end_str: str):
        """
        this is helpful for getting meaningful values out of the exception string
        """
        start_index = original_string.find(start_str)
        if start_index == -1:
            return None

        start_index += len(start_str)
        end_index = original_string.find(end_str, start_index)
        if end_index == -1:
            return None

        return original_string[start_index:end_index]
