import json
from sage.models.sage_models import SalesQuote

"""
This is a soap api, so our request payload must come in the form of xml
"""


class SalesQuoteExportXmlGenerator:
    SAGE_API_SOAP_TAG_ENVELOPE_OPEN = '<soapenv:Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">'
    SAGE_AAPI_SOAP_TAG_ENVELOPE_OPEN_CUST_CREATION = '<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wss="http://www.adonix.com/WSS">'
    SAGE_API_SOAP_TAG_HEADER = '<soapenv:Header/>'
    SAGE_API_SOAP_TAG_BODY_OPEN = '<soapenv:Body>'
    SAGE_API_TAG_SAVE_OPEN = '<save xmlns="http://www.adonix.com/WSS">'
    SAGE_API_TAG_CALL_CONTEXT_OPEN = '<callContext xsi:type="wss:CAdxCallContext">'
    SAGE_API_TAG_CODE_LANG = '<codeLang xsi:type="wss:CAdxCallContext">ENG</codeLang>'
    SAGE_API_TAG_POOL_ALIAS = '<poolAlias xsi:type="xsd:string">PPTESTING</poolAlias>'
    SAGE_API_TAG_POOL_ID = '<poolId xsi:type="xsd:string"> PPTESTING </poolId>'
    SAGE_API_TAG_REQUEST_CONFIG_OPEN = '<requestConfig xsi:type="xsd:string">'
    SAGE_API_TAG_PUBLIC_NAME_OPEN = '<publicName xsi:type="xsd:string">'
    SAGE_API_TAG_OBJECT_XML_OPEN = '<objectXml xsi:type="xsd:string">'
    SAGE_API_TAG_INPUT_XML_OPEN = '<inputXml xsi:type="xsd:string">'

    SAGE_API_TAG_REQUEST_CONFIG_CLOSE = '</requestConfig>'
    SAGE_API_TAG_CALL_CONTEXT_CLOSE = '</callContext>'
    SAGE_API_TAG_PUBLIC_NAME_CLOSE = '</publicName>'
    SAGE_API_TAG_OBJECT_XML_CLOSE = '</objectXml>'
    SAGE_API_TAG_INPUT_XML_CLOSE = '</inputXml>'
    SAGE_API_TAG_SAVE_CLOSE = '</save>'
    SAGE_API_SOAP_TAG_BODY_CLOSE = '</soapenv:Body>'
    SAGE_API_SOAP_TAG_ENVELOPE_CLOSE = '</soapenv:Envelope>'

    REQUEST_CONFIG = '<![CDATA[adxwss.optreturn=JSON&adxwss.beautify=true&adxwss.trace.on=off]]>'
    PUBLIC_NAME_SALES_QUOTE = 'YSQH'

    SAGE_API_C_DATA_TAG_OPEN = '<![CDATA['
    SAGE_API_C_DATA_CLOSE = ']]>'

    # SALES QUOTE HEADER SECTION
    OBJECT_XML_KEY_QUOTE_HEADER_SECTION = "SQH0_1"
    OBJECT_XML_KEY_SALES_SITE = "SALFCY"
    OBJECT_XML_KEY_QUOTE_TYPE = "SQHTYP"
    OBJECT_XML_KEY_REFERENCE = "CUSQUOREF"
    OBJECT_XML_KEY_QUOTE_DATE = "QUODAT"
    OBJECT_XML_KEY_CUSTOMER_ID = "BPCORD"
    OBJECT_XML_KEY_CURRENCY = "CUR"

    # SALES QUOTE DELIVERY SECTION
    OBJECT_XML_KEY_QUOTE_DELIVERY_SECTION = "SQH1_1"
    OBJECT_XML_KEY_DELIVERY_ADDRESS = "BPAADD"

    # SALES QUOTE SHIPPING SECTION
    OBJECT_XML_KEY_QUOTE_SHIPPING_SECTION = "SQH1_2"
    OBJECT_XML_KEY_SHIPMENT_SITE = "STOFCY"

    # SALES QUOTE PRODUCT SECTION
    OBJECT_XML_KEY_QUOTE_PRODUCT_SECTION = "SQH2_1"
    OBJECT_XML_KEY_ITEM_REF = "ITMREF"
    OBJECT_XML_KEY_SAL = "SAU"
    OBJECT_XML_KEY_QUANTITY = "QTY"
    OBJECT_XML_KEY_SAL_STK_CONV = "SAUSTUCOE"
    OBJECT_XML_KEY_STOCK = "STU"
    OBJECT_XML_KEY_GROSS_PRICE = "GROPRI"
    OBJECT_XML_KEY_TAX_LEVEL_1 = "VACITM1"

    def get_sales_quote_request_xml(self, sales_quote: SalesQuote):
        req_xml = """"""
        req_xml += self.SAGE_API_SOAP_TAG_ENVELOPE_OPEN
        req_xml += self.SAGE_API_SOAP_TAG_HEADER
        req_xml += self.SAGE_API_SOAP_TAG_BODY_OPEN
        req_xml += self.SAGE_API_TAG_SAVE_OPEN
        req_xml += self.SAGE_API_TAG_CALL_CONTEXT_OPEN
        req_xml += self.SAGE_API_TAG_CODE_LANG
        req_xml += self.SAGE_API_TAG_POOL_ALIAS
        req_xml += self.SAGE_API_TAG_POOL_ID
        req_xml += self.SAGE_API_TAG_REQUEST_CONFIG_OPEN
        req_xml += self.REQUEST_CONFIG
        req_xml += self.SAGE_API_TAG_REQUEST_CONFIG_CLOSE
        req_xml += self.SAGE_API_TAG_CALL_CONTEXT_CLOSE
        req_xml += self.SAGE_API_TAG_PUBLIC_NAME_OPEN
        req_xml += self.PUBLIC_NAME_SALES_QUOTE
        req_xml += self.SAGE_API_TAG_PUBLIC_NAME_CLOSE
        req_xml += self.SAGE_API_TAG_OBJECT_XML_OPEN
        req_xml += self.SAGE_API_C_DATA_TAG_OPEN
        req_xml += self._generate_sales_quote_object_xml_json(sales_quote)
        req_xml += self.SAGE_API_C_DATA_CLOSE
        req_xml += self.SAGE_API_TAG_OBJECT_XML_CLOSE
        req_xml += self.SAGE_API_TAG_SAVE_CLOSE
        req_xml += self.SAGE_API_SOAP_TAG_BODY_CLOSE
        req_xml += self.SAGE_API_SOAP_TAG_ENVELOPE_CLOSE

        return req_xml

    def _generate_sales_quote_object_xml_json(self, sales_quote: SalesQuote):

        dictionary = {
            self.OBJECT_XML_KEY_QUOTE_HEADER_SECTION: {
                self.OBJECT_XML_KEY_SALES_SITE: sales_quote.sales_site,
                self.OBJECT_XML_KEY_QUOTE_TYPE: sales_quote.quote_type,
                self.OBJECT_XML_KEY_REFERENCE: sales_quote.reference,
                self.OBJECT_XML_KEY_QUOTE_DATE: sales_quote.quote_date,
                self.OBJECT_XML_KEY_CUSTOMER_ID: sales_quote.customer_id,
                self.OBJECT_XML_KEY_CURRENCY: sales_quote.currency
            },
            self.OBJECT_XML_KEY_QUOTE_DELIVERY_SECTION: {
                self.OBJECT_XML_KEY_DELIVERY_ADDRESS: sales_quote.delivery_address
            },
            self.OBJECT_XML_KEY_QUOTE_SHIPPING_SECTION: {
                self.OBJECT_XML_KEY_SHIPMENT_SITE: sales_quote.shipment_site
            },
            self.OBJECT_XML_KEY_QUOTE_PRODUCT_SECTION: []
        }

        # add the line items in a loop
        for line_item in sales_quote.line_items:
            line_dict = {
                self.OBJECT_XML_KEY_ITEM_REF: line_item.item_ref,
                self.OBJECT_XML_KEY_SAL: line_item.sal,
                self.OBJECT_XML_KEY_QUANTITY: line_item.quantity,
                self.OBJECT_XML_KEY_SAL_STK_CONV: line_item.sal_stk_conv,
                self.OBJECT_XML_KEY_STOCK: line_item.stock,
                self.OBJECT_XML_KEY_GROSS_PRICE: line_item.gross_price,
                self.OBJECT_XML_KEY_TAX_LEVEL_1: line_item.tax_level_1
            }
            dictionary[self.OBJECT_XML_KEY_QUOTE_PRODUCT_SECTION].append(line_dict)

        return json.dumps(dictionary)
