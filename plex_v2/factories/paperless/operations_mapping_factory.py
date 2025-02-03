from paperless.client import PaperlessClient
from plex_v2.objects.operations_mapping import OperationMapping, OperationsMapping
from plex_v2.objects.routing import Operation
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from typing import List
from plex_v2.factories.base import BaseFactory
from plex_v2.configuration import PlexConfig
from plex_v2.utils.export import ExportUtils
from baseintegration.integration.erp_error_message_converter import ConvertedErrorException


class OperationMappingFactory(BaseFactory):

    KEY_PP_OP_NAME: str
    KEY_PLEX_OP_CODE: str
    KEY_APPROVED_WORKCENTERS: str
    KEY_APPROVED_SUPPLIERS: str
    KEY_PAPERLESS_ONLY: str

    def __init__(self, config: PlexConfig, utils: ExportUtils):
        super().__init__(config, utils)
        self.KEY_PP_OP_NAME = config.paperless_operation_name_column_header
        self.KEY_PLEX_OP_CODE = config.plex_operation_code_column_header
        self.KEY_APPROVED_WORKCENTERS = config.plex_approved_workcenters_column_header
        self.KEY_APPROVED_SUPPLIERS = config.plex_approved_suppliers_column_header
        self.KEY_PAPERLESS_ONLY = config.paperless_only_column_header

    def from_custom_table_row(self, row: dict, plex_ops: List[Operation]):
        plex_op_id = self._get_plex_op_id_by_code(plex_ops, row[self.KEY_PLEX_OP_CODE])

        return OperationMapping(
            pp_op_name=row[self.KEY_PP_OP_NAME],
            plex_op_code=row[self.KEY_PLEX_OP_CODE],
            plex_approved_workcenters=self._get_approved_workcenters_for_op_row(row),
            plex_approved_suppliers=self._get_approved_suppliers_for_op_row(row),
            paperless_only=row[self.KEY_PAPERLESS_ONLY],
            plex_op_id=plex_op_id
        )

    def _get_approved_workcenters_for_op_row(self, row: dict) -> List[str]:
        # there is not necesarily a col for approved workcenters - not everyone will use this
        if self.KEY_APPROVED_WORKCENTERS not in row.keys():
            return []

        return self._parse_pipe_delimited_string(row[self.KEY_APPROVED_WORKCENTERS])

    def _get_approved_suppliers_for_op_row(self, row: dict) -> List[str]:
        # there is not necesarily a col for approved suppliers - not everyone will use this
        if self.KEY_APPROVED_SUPPLIERS not in row.keys():
            return []

        return self._parse_pipe_delimited_string(row[self.KEY_APPROVED_SUPPLIERS])

    def _get_plex_op_id_by_code(self, plex_ops: List[Operation], op_code: str):
        plex_op: Operation
        for plex_op in plex_ops:
            if plex_op.code == op_code:
                return plex_op.id

        return None
        # raise CancelledIntegrationActionException(f'Could not find a matching plex operation with code "{op_code}"')

    def _parse_pipe_delimited_string(self, pipe_delimited_string: str):
        # Create a StringIO object to simulate a file-like object
        elements = pipe_delimited_string.split('|')

        # make sure it doesnt include this breaking space character, sometimes happens when parsing the custom table
        cleaned_values = [element.replace('\xa0', ' ') for element in elements]
        cleaned_values_0 = []
        for cleaned_value in cleaned_values:
            if len(cleaned_value) > 0:
                cleaned_values_0.append(cleaned_value)

        return cleaned_values_0


class OperationsMappingFactory(BaseFactory):

    op_mapping_factory: OperationMappingFactory

    def __init__(self, config: PlexConfig, utils: ExportUtils, op_mapping_factory: OperationMappingFactory):
        super().__init__(config, utils)
        self.op_mapping_factory = op_mapping_factory

    def get_operations_mapping(self):
        # 0) establish the url of the custom table
        url = f"suppliers/public/custom_tables/{self.config.operation_code_map_table}"

        # 1) get the custom table info
        rows = self._get_custom_table_rows(url)

        # 2) get the plex operations
        plex_operations: List[Operation] = Operation.search()

        # 3) create mapping objects and add to list
        operation_mappings: List[OperationMapping] = []
        for row in rows:
            operation_mappings.append(self.op_mapping_factory.from_custom_table_row(row, plex_operations))

        # instantiate and return OperationsMapping with the list of operation mappings
        return OperationsMapping(operation_mappings=operation_mappings)

    def _get_custom_table_rows(self, url: str):
        client = PaperlessClient.get_instance()

        try:
            response = client.request(url, data={}, method="get")
            return response.json()["rows"]
        except ConvertedErrorException as e:
            raise e
        except Exception as e:
            raise CancelledIntegrationActionException(f'Error reading from "Operations_Mapping" table: {str(e)}')
