
"""
constants that the soap client, and xml parser will rely on to ingest response
"""


class SoapConstants:

    _SOAP_ENV_PREFIX = 'soapenv'
    _WSS_PREFIX = 'wss'

    SOAP_ENV_ENVELOPE = f'{_SOAP_ENV_PREFIX}:Envelope'
    SOAP_ENV_BODY = f'{_SOAP_ENV_PREFIX}:Body'
    WSS_RUN_RESPONSE = f'{_WSS_PREFIX}:runResponse'
    RUN_RETURN = 'runReturn'
    RESULT_XML = 'resultXml'
    RESULT_XML_TEXT = '#text'

    RESULT_XML_KEY_GRP3 = 'GRP3'
    KEY_O_FILE = 'O_FILE'
