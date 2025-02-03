"""
Errors taken from Plex developer docs:
https://new.developers.plex.com/getstarted#ErrCodes
"""


class PlexException(Exception):
    def __init__(self, message, error_code=None, detail=""):
        super(PlexException, self).__init__(message)
        self.detail = detail
        self.error_code = error_code
        self.message = message

        def __str__(self):
            return f"Plex Exception: {self.message}"


class PlexMalformedRequestException(PlexException):
    """
    400 - Malformed request
    400 errors generally indicate that the body of the request does not match the resource being requested.
    """

    def __init__(self, message, error_code=None, detail=""):
        super(PlexMalformedRequestException, self).__init__(message, error_code, detail)

    def __str__(self):
        return f"Plex Malformed Request Exception: {self.message}  \n\n {self.detail}"


class PlexValidationFailureException(PlexException):
    """
    400 - Validation failure
    One or more of the parameters use an incorrect format or are omitted from the request.
    """

    def __init__(self, message, error_code=None, detail=""):
        super(PlexValidationFailureException, self).__init__(message, error_code, detail)

    def __str__(self):
        return f"Plex Validation Failure Exception: {self.message}  \n\n {self.detail}"


class PlexRequestNotAuthenticatedException(PlexException):
    """
    401 - Request not authenticated
    A 401 error can occur when you try to access the system using an expired api key, an invalid api key, or without an
    api key at all. If you receive this error, verify that the X-Plex-Connect-Api-Key header is specified on the request
    and that the key matches the value in the Plex Developer Portal.
    """

    def __init__(self, message, error_code=None, detail=""):
        super(PlexRequestNotAuthenticatedException, self).__init__(message, error_code, detail)

    def __str__(self):
        return f"Plex Request Not Authenticated Exception: {self.message}  \n\n {self.detail}"


class PlexResourceNotFoundException(PlexException):
    """
    404 - Resource not found
    A 404 error can occur when your application attempts to access Plex functionality using an incorrect request URL or
    if no data exists to return.
    """

    def __init__(self, message, error_code=None, detail=""):
        super(PlexResourceNotFoundException, self).__init__(message, error_code, detail)

    def __str__(self):
        return f"Plex Resource Not Found Exception: {self.message}  \n\n {self.detail}"


class PlexRequestProcessingErrorException(PlexException):
    """
    500 - Request processing error
    500 errors are unexpected. If you can reproduce the error, submit a support ticket to Plex. Include the steps to
    duplicate the issue, but do not include client secrets, passwords, or subscription keys.
    """

    def __init__(self, message, error_code=None, detail=""):
        super(PlexRequestProcessingErrorException, self).__init__(message, error_code, detail)

    def __str__(self):
        return f"Plex Request Processing Error Exception: {self.message}  \n\n {self.detail}"
