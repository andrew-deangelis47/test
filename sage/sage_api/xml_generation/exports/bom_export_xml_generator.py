import json

"""
This is a soap api, so our request payload must come in the form of xml
"""


class BomExportXmlGenerator:

    SOAP_TAG_ENVELOPE_OPEN = '<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wss="http://www.adonix.com/WSS">'
    SOAP_TAG_HEADER = '<soapenv:Header/>'
    SOAP_TAG_BODY_OPEN = '<soapenv:Body>'
    TAG_CALL_CONTEXT_OPEN = '<callContext xsi:type="wss:CAdxCallContext">'
    TAG_CODE_LANG = '<codeLang xsi:type="xsd:string">ENG</codeLang>'
    TAG_POOL_ALIAS = '<poolAlias xsi:type="xsd:string">PPTESTING</poolAlias>'
    TAG_POOL_ID = '<poolId xsi:type="xsd:string"> PPTESTING </poolId>'
    TAG_REQUEST_CONFIG_OPEN = '<requestConfig xsi:type="xsd:string">'
    TAG_PUBLIC_NAME_OPEN = '<publicName xsi:type="xsd:string">'
    TAG_INPUT_XML_OPEN = '<inputXml xsi:type="xsd:string">'

    SAGE_API_TAG_REQUEST_CONFIG_CLOSE = '</requestConfig>'
    SAGE_API_TAG_CALL_CONTEXT_CLOSE = '</callContext>'
    SAGE_API_TAG_PUBLIC_NAME_CLOSE = '</publicName>'
    SAGE_API_TAG_INPUT_XML_CLOSE = '</inputXml>'
    SAGE_API_SOAP_TAG_BODY_CLOSE = '</soapenv:Body>'
    SAGE_API_SOAP_TAG_ENVELOPE_CLOSE = '</soapenv:Envelope>'

    REQUEST_CONFIG = '<![CDATA[adxwss.optreturn=JSON&adxwss.beautify=true&adxwss.trace.on=off]]>'
    PUBLIC_NAME_CUSTOMER = 'AOWSIMPORT'

    SAGE_API_C_DATA_TAG_OPEN = '<![CDATA['
    SAGE_API_C_DATA_CLOSE = ']]>'

    # customer export
    INPUT_XML_KEY_GRP1 = "GRP1"
    INPUT_XML_KEY_TEMPLATE_IMPORT = "I_MODIMP"
    INPUT_XML_KEY_I_AOWSTA = "I_AOWSTA"
    INPUT_XML_KEY_I_FILE = "I_FILE"
    INPUT_XML_KEY_RECORD_SEPERATOR = "I_RECORDSEP"
    XML_TAG_WSS_RUN_OPEN = '<wss:run soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
    XML_TAG_WSS_RUN_CLOSE = '</wss:run>'
    INPUT_KEY_I_EXEC = 'I_EXEC'

    def generate_bom_creation_xml(self, i_file):
        req_xml = """"""
        req_xml += self.SOAP_TAG_ENVELOPE_OPEN
        req_xml += self.SOAP_TAG_HEADER
        req_xml += self.SOAP_TAG_BODY_OPEN
        req_xml += self.XML_TAG_WSS_RUN_OPEN
        req_xml += self.TAG_CALL_CONTEXT_OPEN
        req_xml += self.TAG_CODE_LANG
        req_xml += self.TAG_POOL_ALIAS
        req_xml += self.TAG_POOL_ID
        req_xml += self.TAG_REQUEST_CONFIG_OPEN
        req_xml += self.REQUEST_CONFIG
        req_xml += self.SAGE_API_TAG_REQUEST_CONFIG_CLOSE
        req_xml += self.SAGE_API_TAG_CALL_CONTEXT_CLOSE
        req_xml += self.TAG_PUBLIC_NAME_OPEN
        req_xml += self.PUBLIC_NAME_CUSTOMER
        req_xml += self.SAGE_API_TAG_PUBLIC_NAME_CLOSE
        req_xml += self.TAG_INPUT_XML_OPEN
        req_xml += self.SAGE_API_C_DATA_TAG_OPEN
        req_xml += self._generate_input_xml_for_bom_creation(i_file)
        req_xml += self.SAGE_API_C_DATA_CLOSE
        req_xml += self.SAGE_API_TAG_INPUT_XML_CLOSE
        req_xml += self.XML_TAG_WSS_RUN_CLOSE
        req_xml += self.SAGE_API_SOAP_TAG_BODY_CLOSE
        req_xml += self.SAGE_API_SOAP_TAG_ENVELOPE_CLOSE

        return req_xml

    def _generate_input_xml_for_bom_creation(self, i_file: str):
        dictionary = {
            self.INPUT_XML_KEY_GRP1: {
                self.INPUT_XML_KEY_TEMPLATE_IMPORT: "ZBOMP",
                self.INPUT_XML_KEY_I_AOWSTA: "NO",
                self.INPUT_KEY_I_EXEC: "REALTIME",
                self.INPUT_XML_KEY_RECORD_SEPERATOR: "|",
                self.INPUT_XML_KEY_I_FILE: i_file
            }
        }

        return json.dumps(dictionary)
