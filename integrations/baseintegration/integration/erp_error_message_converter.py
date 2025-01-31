from typing import List, Union
from ...baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException


class ConvertedErrorException(CancelledIntegrationActionException):
    """
    this is so that we know when we are catching a known error
    """
    pass


class ErrorMessageMapping:

    erp_error_message: str
    paperless_error_message: str

    def __init__(self, erp_error_message: str, paperless_error_message: str):
        self.erp_error_message = erp_error_message
        self.paperless_error_message = paperless_error_message

    def error_message_matches(self, erp_error_message: str):
        """
        returns True if it's erp error message is contained in the incoming error message
        """
        if self.erp_error_message in erp_error_message:
            return True
        return False


class ERPErrorMessageConverter:
    """
    1) ingests config file which says what error message that the integration can translate
    2) given an error message, this class can return a more readable message to display in the integration manager
    """
    """
    This class is used to make all calls to the plex API.
    """
    _instance = None

    def __new__(cls, config_dict: dict):
        """
        Create or return the ERPErrorMessageConverter Singleton.
        """
        if ERPErrorMessageConverter._instance is None:
            ERPErrorMessageConverter._instance = object.__new__(cls)

        instance = ERPErrorMessageConverter._instance

        mappings: List[ErrorMessageMapping] = []
        for key in config_dict.keys():
            mappings.append(ErrorMessageMapping(key, config_dict[key]))
        instance.mappings = mappings
        cls._instance = instance
        return instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    __instance = None

    def get_clean_message(self, erp_error_message: str) -> Union[str, None]:
        """
        if this is a know error then return the converted message, otherwise return None
        """
        mapping: ErrorMessageMapping
        for mapping in self.mappings:
            if mapping.error_message_matches(erp_error_message):
                return mapping.paperless_error_message

        return None
