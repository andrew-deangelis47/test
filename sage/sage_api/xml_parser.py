import json
import xmltodict
from sage.sage_api.soap_constants import SoapConstants


class SageXmlParser:

    """
    returns raw o file data from a xml response from the Sage Api
    """
    @staticmethod
    def get_import_o_file_payload(raw_xml) -> str:
        json_decoder = json.JSONDecoder()
        xml_dict = xmltodict.parse(raw_xml)
        input_xml = xml_dict[SoapConstants.SOAP_ENV_ENVELOPE][SoapConstants.SOAP_ENV_BODY][SoapConstants.WSS_RUN_RESPONSE][SoapConstants.RUN_RETURN][SoapConstants.RESULT_XML][SoapConstants.RESULT_XML_TEXT]
        decoded = json_decoder.decode(input_xml)
        o_file_raw: str = decoded[SoapConstants.RESULT_XML_KEY_GRP3][SoapConstants.KEY_O_FILE]
        return o_file_raw
