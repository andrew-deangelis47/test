import json

"""
This is a soap api, so our request payload must come in the form of xml
"""


class SageApiImportXmlGenerator:
    SAGE_API_SOAP_TAG_ENVELOPE_OPEN = '<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:wss=\"http://www.adonix.com/WSS\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">'
    SAGE_API_SOAP_TAG_HEADER = '<soapenv:Header/>'
    SAGE_API_SOAP_TAG_BODY_OPEN = '<soapenv:Body>'
    SAGE_API_TAG_WSS_RUN_OPEN = '<wss:run soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
    SAGE_API_TAG_CALL_CONTEXT_OPEN = '<callContext xsi:type="wss:CAdxCallContext">'
    # these two below are technically configurable, but we will always be using the same vals
    SAGE_API_TAG_CODE_LANG = '<codeLang xsi:type="wss:CAdxCallContext">ENG</codeLang>'
    SAGE_API_TAG_POOL_ALIAS = '<poolAlias xsi:type="xsd:string">PPTESTING</poolAlias>'
    SAGE_API_TAG_POOL_ID = '<poolId xsi:type="xsd:string"/>'
    SAGE_API_TAG_REQUEST_CONFIG_OPEN = '<requestConfig xsi:type="xsd:string">'
    SAGE_API_TAG_PUBLIC_NAME_OPEN = '<publicName xsi:type="xsd:string">'
    SAGE_API_TAG_INPUT_XML_OPEN = '<inputXml xsi:type="xsd:string">'

    SAGE_API_TAG_REQUEST_CONFIG_CLOSE = '</requestConfig>'
    SAGE_API_TAG_CALL_CONTEXT_CLOSE = '</callContext>'
    SAGE_API_TAG_PUBLIC_NAME_CLOSE = '</publicName>'
    SAGE_API_TAG_INPUT_XML_CLOSE = '</inputXml>'
    SAGE_API_TAG_WSS_RUN_CLOSE = '</wss:run>'
    SAGE_API_SOAP_TAG_BODY_CLOSE = '</soapenv:Body>'
    SAGE_API_SOAP_TAG_ENVELOPE_CLOSE = '</soapenv:Envelope>'

    REQUEST_CONFIG = '<![CDATA[adxwss.optreturn=JSON&adxwss.beautify=true&adxwss.trace.on=off]]>'
    PUBLIC_NAME_EXPORT = 'AOWSEXPORT'

    SAGE_API_C_DATA_TAG_OPEN = '<![CDATA['
    SAGE_API_C_DATA_CLOSE = ']]>'

    # data for input xml, identifies the template and any filters
    INPUT_XML_KEY_GRP1 = "GRP1"
    INPUT_XML_KEY_GRP2 = "GRP2"
    INPUT_XML_KEY_GRP3 = "GRP3"
    INPUT_XML_KEY_TEMPLATE = "I_MODEXP"
    INPUT_XML_KEY_I_CHRONO = "I_CHRONO"
    INPUT_XML_VALUE_I_CHRONO = "NO"
    INPUT_XML_KEY_FILTER = "I_TCRITERE"
    INPUT_XML_KEY_I_EXEC = "I_EXEC"
    INPUT_XML_VALUE_I_EXEC = "REALTIME"
    INPUT_XML_KEY_RECORD_SEPERATOR = "I_RECORDSEP"
    INPUT_XML_VALUE_RECORD_SEPERATOR = "|"

    def get_request_xml(self, template: str, template_filter: str = None):
        req_xml = """"""
        req_xml += self.SAGE_API_SOAP_TAG_ENVELOPE_OPEN
        req_xml += self.SAGE_API_SOAP_TAG_HEADER
        req_xml += self.SAGE_API_SOAP_TAG_BODY_OPEN
        req_xml += self.SAGE_API_TAG_WSS_RUN_OPEN
        req_xml += self.SAGE_API_TAG_CALL_CONTEXT_OPEN
        req_xml += self.SAGE_API_TAG_CODE_LANG
        req_xml += self.SAGE_API_TAG_POOL_ALIAS
        req_xml += self.SAGE_API_TAG_POOL_ID
        req_xml += self.SAGE_API_TAG_REQUEST_CONFIG_OPEN
        req_xml += self.REQUEST_CONFIG
        req_xml += self.SAGE_API_TAG_REQUEST_CONFIG_CLOSE
        req_xml += self.SAGE_API_TAG_CALL_CONTEXT_CLOSE
        req_xml += self.SAGE_API_TAG_PUBLIC_NAME_OPEN
        req_xml += self.PUBLIC_NAME_EXPORT
        req_xml += self.SAGE_API_TAG_PUBLIC_NAME_CLOSE
        req_xml += self.SAGE_API_TAG_INPUT_XML_OPEN
        req_xml += self.SAGE_API_C_DATA_TAG_OPEN
        req_xml += self._generate_input_xml_json(template, template_filter)
        req_xml += self.SAGE_API_C_DATA_CLOSE
        req_xml += self.SAGE_API_TAG_INPUT_XML_CLOSE
        req_xml += self.SAGE_API_TAG_WSS_RUN_CLOSE
        req_xml += self.SAGE_API_SOAP_TAG_BODY_CLOSE
        req_xml += self.SAGE_API_SOAP_TAG_ENVELOPE_CLOSE

        return req_xml

    def _generate_input_xml_json(self, template: str, template_filter: str = None):
        # if there's no filter just grab everything
        if template_filter is None:
            template_filter = "1=1"

        dictionary = {
            self.INPUT_XML_KEY_GRP1: {
                self.INPUT_XML_KEY_TEMPLATE: template,
                self.INPUT_XML_KEY_I_CHRONO: self.INPUT_XML_VALUE_I_CHRONO
            },
            self.INPUT_XML_KEY_GRP2: [
                {
                    # self.INPUT_XML_KEY_FILTER: template_filter
                }
            ],
            self.INPUT_XML_KEY_GRP3: {
                self.INPUT_XML_KEY_I_EXEC: self.INPUT_XML_VALUE_I_EXEC,
                self.INPUT_XML_KEY_RECORD_SEPERATOR: self.INPUT_XML_VALUE_RECORD_SEPERATOR
            }
        }

        # TODO: this is so dumb but the json.dump does not handle the sage filters well
        #       we have to add the filters after the json dump processes the above dictionary
        #       Is there a better way to do this? Maybe? At min we can break out into own function
        json_dump = json.dumps(dictionary)
        json_dump = json_dump.replace("[{}]", "[{" + '"' + self.INPUT_XML_KEY_FILTER + '"' + ':' + template_filter + "}]")

        return json_dump
