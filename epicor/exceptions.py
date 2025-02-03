class EpicorException(Exception):
    def __init__(self, message, error_code=None, detail=""):
        super(EpicorException, self).__init__(message)
        self.detail = detail
        self.error_code = error_code
        self.message = message

        def __str__(self):
            return "Epicor Exception: {}".format(self.message)


class EpicorAuthorizationException(EpicorException):
    def __init__(self, message, error_code=None, detail=""):
        super(EpicorAuthorizationException, self).__init__(message, error_code, detail)

    def __str__(self):
        return "Epicor Auth Exception: {}  \n\n {}".format(self.message, self.detail)


class EpicorNotFoundException(EpicorException):
    def __init__(self, message, error_code=404, detail=""):
        super(EpicorNotFoundException, self).__init__(message, error_code, detail)

        self.detail = detail
        self.error_code = error_code
        self.message = message

    def __str__(self):
        return "Epicor Resource Not Found: {}  \n\n {}".format(self.message, self.detail)
