"""
Errors taken from Acumatica developer docs:
"""


class AcumaticaException(Exception):
    def __init__(self, message, error_code=None, detail=""):
        super(AcumaticaException, self).__init__(message)
        self.detail = detail
        self.error_code = error_code
        self.message = message

        def __str__(self):
            return f"Acumatica Exception: {self.message}"


class AcumaticaMalformedRequestException(AcumaticaException):
    """
    400 - Malformed request
    400 errors generally indicate that the body of the request does not match the resource being requested.
    """

    def __init__(self, message, error_code=None, detail=""):
        super(AcumaticaMalformedRequestException, self).__init__(message, error_code, detail)

    def __str__(self):
        return f"Acumatica Malformed Request Exception: {self.message}  \n\n {self.detail}"


class AcumaticaValidationFailureException(AcumaticaException):
    """
    400 - Validation failure
    One or more of the parameters use an incorrect format or are omitted from the request.
    """

    def __init__(self, message, error_code=None, detail=""):
        super(AcumaticaValidationFailureException, self).__init__(message, error_code, detail)

    def __str__(self):
        return f"Acumatica Validation Failure Exception: {self.message}  \n\n {self.detail}"


class AcumaticaRequestNotAuthenticatedException(AcumaticaException):
    """
    401 - Request not authenticated
    A 401 error can occur when you try to access the system using an expired api key, an invalid api key, or without an
    api key at all. If you receive this error, verify that the X-Acumatica-Connect-Api-Key header is specified on the request
    and that the key matches the value in the Acumatica Developer Portal.
    """

    def __init__(self, message, error_code=None, detail=""):
        super(AcumaticaRequestNotAuthenticatedException, self).__init__(message, error_code, detail)

    def __str__(self):
        return f"Acumatica Request Not Authenticated Exception: {self.message}  \n\n {self.detail}"


class AcumaticaResourceNotFoundException(AcumaticaException):
    """
    404 - Resource not found
    A 404 error can occur when your application attempts to access Acumatica functionality using an incorrect request URL or
    if no data exists to return.
    """

    def __init__(self, message, error_code=None, detail=""):
        super(AcumaticaResourceNotFoundException, self).__init__(message, error_code, detail)

    def __str__(self):
        return f"Acumatica Resource Not Found Exception: {self.message}  \n\n {self.detail}"


class AcumaticaRequestProcessingErrorException(AcumaticaException):
    """
    500 - Request processing error
    500 errors are unexpected. If you can reproduce the error, submit a support ticket to Acumatica. Include the steps to
    duplicate the issue, but do not include client secrets, passwords, or subscription keys.
    """

    def __init__(self, message, error_code=None, detail=""):
        super(AcumaticaRequestProcessingErrorException, self).__init__(message, error_code, detail)

    def __str__(self):
        return f"Acumatica Request Processing Error Exception: {self.message}  \n\n {self.detail}"
