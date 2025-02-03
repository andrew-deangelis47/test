"""
Errors taken from M2M developer docs:
https://new.developers.M2M.com/getstarted#ErrCodes
"""


class M2MException(Exception):
    def __init__(self, message, error_code=None, detail=""):
        super(M2MException, self).__init__(message)
        self.detail = detail
        self.error_code = error_code
        self.message = message

        def __str__(self):
            return f"M2M Exception: {self.message}"


class M2MMalformedRequestException(M2MException):
    """
    400 - Malformed request
    400 errors generally indicate that the body of the request does not match the resource being requested.
    """

    def __init__(self, message, error_code=None, detail=""):
        super(M2MMalformedRequestException, self).__init__(message, error_code, detail)

    def __str__(self):
        return f"M2M Malformed Request Exception: {self.message}  \n\n {self.detail}"


class M2MValidationFailureException(M2MException):
    """
    400 - Validation failure
    One or more of the parameters use an incorrect format or are omitted from the request.
    """

    def __init__(self, message, error_code=None, detail=""):
        super(M2MValidationFailureException, self).__init__(message, error_code, detail)

    def __str__(self):
        return f"M2M Validation Failure Exception: {self.message}  \n\n {self.detail}"


class M2MRequestNotAuthenticatedException(M2MException):
    """
    401 - Request not authenticated
    A 401 error can occur when you try to access the system using an expired api key, an invalid api key, or without an
    api key at all. If you receive this error, verify that the X-M2M-Connect-Api-Key header is specified on the request
    and that the key matches the value in the M2M Developer Portal.
    """

    def __init__(self, message, error_code=None, detail=""):
        super(M2MRequestNotAuthenticatedException, self).__init__(message, error_code, detail)

    def __str__(self):
        return f"M2M Request Not Authenticated Exception: {self.message}  \n\n {self.detail}"


class M2MResourceNotFoundException(M2MException):
    """
    404 - Resource not found
    A 404 error can occur when your application attempts to access M2M functionality using an incorrect request URL or
    if no data exists to return.
    """

    def __init__(self, message, error_code=None, detail=""):
        super(M2MResourceNotFoundException, self).__init__(message, error_code, detail)

    def __str__(self):
        return f"M2M Resource Not Found Exception: {self.message}  \n\n {self.detail}"


class M2MRequestProcessingErrorException(M2MException):
    """
    500 - Request processing error
    500 errors are unexpected. If you can reproduce the error, submit a support ticket to M2M. Include the steps to
    duplicate the issue, but do not include client secrets, passwords, or subscription keys.
    """

    def __init__(self, message, error_code=None, detail=""):
        super(M2MRequestProcessingErrorException, self).__init__(message, error_code, detail)

    def __str__(self):
        return f"M2M Request Processing Error Exception: {self.message}  \n\n {self.detail}"


class M2MInvalidAddressException(M2MException):
    """
    500 - Request processing error
    500 errors are unexpected. If you can reproduce the error, submit a support ticket to M2M. Include the steps to
    duplicate the issue, but do not include client secrets, passwords, or subscription keys.
    """

    def __init__(self, message, error_code=None, detail=""):
        super(M2MInvalidAddressException, self).__init__(message, error_code, detail)

    def __str__(self):
        return f"Invalid address: {self.message}  \n\n {self.detail}"
