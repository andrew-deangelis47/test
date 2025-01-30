class PaperlessIntegrationError(Exception):
    pass


class ProcessorNotRegisteredError(PaperlessIntegrationError):
    pass


class IntegrationNotImplementedError(PaperlessIntegrationError):
    pass


class PaperlessProcessorError(PaperlessIntegrationError):
    pass


class ProcessNotImplementedError(PaperlessProcessorError):
    pass
