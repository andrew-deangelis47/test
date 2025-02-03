import requests
from base64 import b64encode
from sage.models.sage_models import BaseObject
from sage.models.sage_models.bom.bom_full_entity import BomFullEntity
from sage.models.sage_models.part import PartFullEntity
from sage.models.sage_models.vendor import SupplierFullEntity
from sage.sage_api.xml_generation.exports.bom_export_xml_generator import BomExportXmlGenerator
from sage.sage_api.xml_generation.exports.routing_export_xml_generator import RoutingExportXmlGenerator
from sage.sage_api.xml_parser import SageXmlParser
from sage.exceptions import SageInvalidResourceRequestedException, SageInvalidResponsePayloadException
from typing import List, Union
from sage.models.sage_models.work_center import WorkCenterFullEntity
from sage.models.sage_models.customer.customer_full_entity import SageCustomerFullEntity
from baseintegration.datamigration import logger
from sage.sage_api.xml_generation.imports.import_xml_generator import SageApiImportXmlGenerator
from sage.sage_api.xml_generation.exports.customer_export_xml_generator import CustomerExportXmlGenerator
from sage.sage_api.o_file_parsing import CustomerExtractor, PartExtractor, VendorExtractor, WorkCenterExtractor
import xml.etree.ElementTree as ET
from sage.models.sage_models.sales_quote import SalesQuote
from sage.sage_api.xml_generation.exports.sales_quote_export_xml_generator import SalesQuoteExportXmlGenerator
from sage.models.sage_models.standard_operations import StandardOperationFullEntity
from sage.sage_api.o_file_parsing.standard_operation_extractor import StandardOperationExtractor


class SageImportClient:
    VERSION_0 = 'v0.0'
    VALID_VERSIONS = [VERSION_0]

    _instance = None
    version = VERSION_0

    # these are common among all imports
    SOAP_ACTION = 'read'
    HTTP_METHOD = 'POST'

    # templates to get the data from the sage API
    SAGE_TEMPLATE_RAW_MATERIALS = 'ZITMPP'
    SAGE_TEMPLATE_SUPPLIERS = 'BPS'
    SAGE_TEMPLATE_PURCHASED_COMPONENTS = 'ZITMPP'
    SAGE_TEMPLATE_WORK_CENTERS = 'ZMWSPP'
    SAGE_TEMPLATE_CUSTOMERS = 'YBPCPPEXP'
    SAGE_TEMPLATE_STANDARD_OPERATIONS = 'ROT'
    # TODO add bom/router here, bom is ZBOMP, router is ZROUT

    def __new__(cls, **kwargs):
        """
        Create or return the SageImportClient Singleton.
        """
        if SageImportClient._instance is None:
            SageImportClient._instance = object.__new__(cls)
        instance = SageImportClient._instance

        instance.base_url = kwargs.get('base_url', None)
        instance.password = kwargs.get('password', None)
        instance.username = kwargs.get('username', None)
        instance.xml_generator = SageApiImportXmlGenerator()
        instance.customer_export_xml_generator = CustomerExportXmlGenerator()
        instance.sales_quote_xml_generator = SalesQuoteExportXmlGenerator()
        instance.bom_export_xml_generator = BomExportXmlGenerator()
        instance.routing_export_xml_generator = RoutingExportXmlGenerator()

        # extractors
        instance.customer_extractor = CustomerExtractor()
        instance.part_extractor = PartExtractor()
        instance.vendor_extractor = VendorExtractor()
        instance.work_center_extractor = WorkCenterExtractor()
        instance.standard_operation_extractor = StandardOperationExtractor()
        # TODO add bom/router here

        # TODO: ADD VERSION VALIDATION
        instance.version = kwargs.get('version', None)
        # By default, we will not verify the certificate on the SSL handshake
        instance.verify_ssl_cert = kwargs.get('verify_ssl_cert', False)
        return instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    def get_response_message(self, response_text: str) -> str:
        root = ET.fromstring(response_text)

        i = 1
        while True:
            try:
                logger.info(f'\nResponse code: {root[0][i][0].text}\nResponse message: {root[0][i][1].text}\n\n')
                i = i + 1
            except IndexError:
                break

        if i == 1:
            logger.info('No response message')

    def create_customer(self, i_file: str):
        payload = self.customer_export_xml_generator.generate_customer_creation_xml(i_file)
        response = self._make_request(payload)
        self.get_response_message(response)

    def create_part(self, part: PartFullEntity):
        payload = self.customer_export_xml_generator.generate_part_creation_xml(part.to_i_file())
        response = self._make_request(payload)
        self.get_response_message(response)

    def create_bom(self, bom: BomFullEntity):
        payload = self.bom_export_xml_generator.generate_bom_creation_xml(bom.to_i_file())
        response = self._make_request(payload)
        self.get_response_message(response)

    def create_routing(self, routing):
        payload = self.routing_export_xml_generator.generate_routing_creation_xml(routing)
        response = self._make_request(payload)
        self.get_response_message(response)

    def create_sales_quote(self, sales_quote: SalesQuote):
        payload = self.sales_quote_xml_generator.get_sales_quote_request_xml(sales_quote)
        response = self._make_request(payload)
        self.get_response_message(response)

    def get_resource(self, sage_object_requested: BaseObject, template_filter: str = None, bulk=True) -> Union[List[BaseObject], BaseObject]:
        """
        Makes a call to the sage api with the to get the data for the specified BaseObject, with the specified filter
        """

        # 1) this API works by accepting a xml formatted request body, get this first
        payload = self.xml_generator.get_request_xml(
            self._get_template_by_object(sage_object_requested),
            template_filter
        )

        # 2) Make the call and cross your fingers
        response_xml = self._make_request(payload)

        # 3) This API returns a xml doc as the response, parse this to get the data we care about
        try:
            raw_o_file = SageXmlParser.get_import_o_file_payload(response_xml)
        except (KeyError, TypeError):
            raise SageInvalidResponsePayloadException(sage_object_requested, template_filter)

        # 4) check if we get a result, the o file could be empty, in which case return None
        if len(raw_o_file) == 0:
            if bulk:
                return []
            return None

        # 5) there could be multiple entities in the response, parse it and grab them all
        entities = self.get_entities_by_object(sage_object_requested, raw_o_file)

        # 6) if bulk return whole list, otherwise return first value
        if bulk:
            return entities
        if not bulk and len(entities) == 0:
            logger.info('Did not find the requested resource in Sage')
            logger.info('Requested resource: ' + sage_object_requested)
            logger.info('API Filter: ' + template_filter)
            return None

        return entities[0]

    def _get_headers(self) -> dict:
        return {
            'Content-Type': 'application/xml',
            'soapAction': 'read',
            'Authorization': self._get_basic_auth()
        }

    def _make_request(self, xml_payload: str) -> str:
        """
        makes call to Sage API and returns raw xml response
        """
        response = requests.request(self.HTTP_METHOD, self.base_url, headers=self._get_headers(), data=xml_payload)
        return response.text

    def _get_basic_auth(self) -> str:
        token = b64encode(f"{self.username}:{self.password}".encode('utf-8')).decode("ascii")
        return f'Basic {token}'

    def _get_template_by_object(self, sage_model: BaseObject) -> str:
        if sage_model is SupplierFullEntity:
            return self.SAGE_TEMPLATE_SUPPLIERS

        if sage_model is PartFullEntity:
            return self.SAGE_TEMPLATE_PURCHASED_COMPONENTS

        if sage_model is WorkCenterFullEntity:
            return self.SAGE_TEMPLATE_WORK_CENTERS

        if sage_model is SageCustomerFullEntity:
            return self.SAGE_TEMPLATE_CUSTOMERS

        if sage_model is StandardOperationFullEntity:
            return self.SAGE_TEMPLATE_STANDARD_OPERATIONS

        # TODO need to add bom and router here

        raise SageInvalidResourceRequestedException(sage_model)

    def get_entities_by_object(self, sage_model: BaseObject, raw_o_file: str) -> list:
        if sage_model is SupplierFullEntity:
            return self.vendor_extractor.get_vendors(raw_o_file)

        if sage_model is PartFullEntity:
            return self.part_extractor.get_parts(raw_o_file)

        if sage_model is WorkCenterFullEntity:
            return self.work_center_extractor.get_work_centers(raw_o_file)

        if sage_model is SageCustomerFullEntity:
            return self.customer_extractor.get_customers(raw_o_file)

        if sage_model is StandardOperationFullEntity:
            return self.standard_operation_extractor.get_standard_operations(raw_o_file)

        # TODO need to add bom and router here

        raise SageInvalidResourceRequestedException(sage_model)
