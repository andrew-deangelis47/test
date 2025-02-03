from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException


class DynamicsException(Exception):
    def __init__(self, message, error_code=None, detail=""):
        super(DynamicsException, self).__init__(message)
        self.detail = detail
        self.error_code = error_code
        self.message = message

        def __str__(self):
            return "Dynamics Exception: {}".format(self.message)


class DynamicsNotFoundException(DynamicsException):
    def __init__(self, message, error_code=404, detail=""):
        super().__init__(message, error_code, detail)


class RecognizedException(CancelledIntegrationActionException):
    """
    Raise this exception on a fatal error when we know exactly what's wrong, and can email a customer.
    """
    def __init__(self, message, email_message):
        super().__init__(message)
        self.email_message = email_message
