class SageInvalidResourceRequestedException(BaseException):
    def __init__(self, class_requested):
        self.class_requested = class_requested

    def __str__(self):
        return "\nInvalid Sage Resource Requested: {}".format(self.class_requested)


class SageInvalidResponsePayloadException(BaseException):
    def __init__(self, class_requested, api_filter: str):
        self.class_requested = class_requested
        self.api_filter = api_filter

    def __str__(self):
        return "\nSage API response is invalid, likely caused by a bad call to the service \n Resource Requested: {} \n Filter: {}".format(self.class_requested, self.api_filter)
