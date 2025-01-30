from plex_v2.objects.part import Part
from paperless.objects.orders import OrderOperation
from plex_v2.factories.base import BaseFactory
from plex_v2.objects.routing_upload_datasource import RoutingUploadDataSource
from plex_v2.objects.operations_mapping import OperationsMapping
from plex_v2.configuration import PlexConfig
from plex_v2.utils.export import ExportUtils
from baseintegration.exporter.exceptions import IntegrationNotImplementedError


class RoutingUpdateDatasourceFactory(BaseFactory):

    operations_mapping: OperationsMapping

    def __init__(self, config: PlexConfig, operations_mapping: OperationsMapping, utils: ExportUtils):
        self.config = config
        self.operations_mapping = operations_mapping
        self.utils = utils

    def to_material_operation_datasource(self, material_operation: OrderOperation, operation_number: int) -> RoutingUploadDataSource:
        plex_material: Part = self.utils.get_plex_material_from_material_op(material_operation)

        routing_upload_datasource = RoutingUploadDataSource(
            Active=1,
            Part_No=plex_material.number,
            Revision=plex_material.revision,
            Operation_No=operation_number,
            Operation_Code=self.utils.get_plex_operation_code_from_paperless_operation(material_operation, self.operations_mapping),
            Part_Op_Type=self._get_type(material_operation)
        )

        # set configurable properties
        if 'Label_Name' in self.config.routing_datasource_properties_required_material:
            routing_upload_datasource.Label_Name = self._get_label_name_for_material(material_operation)
        if 'Net_Weight' in self.config.routing_datasource_properties_required_material:
            routing_upload_datasource.Net_Weight = self._get_net_weight_for_material(material_operation)
        if 'Note' in self.config.routing_datasource_properties_required_material:
            routing_upload_datasource.Note = self._get_note_for_material(material_operation)
        if 'Description' in self.config.routing_datasource_properties_required_material:
            routing_upload_datasource.Description = self._get_description_for_material(material_operation)

        return routing_upload_datasource

    def to_part_operation_datasource(self, plex_part: Part, pp_op: OrderOperation, operation_number: int) -> RoutingUploadDataSource:
        routing_upload_datasource = RoutingUploadDataSource(
            Active=1,
            Part_No=plex_part.number,
            Revision=plex_part.revision,
            Operation_No=operation_number,
            Operation_Code=self.utils.get_plex_operation_code_from_paperless_operation(pp_op, self.operations_mapping),
            Part_Op_Type=self._get_type(pp_op)
        )

        # set configurable properties
        if 'Label_Name' in self.config.routing_datasource_properties_required:
            routing_upload_datasource.Label_Name = self._get_label_name(plex_part, pp_op)
        if 'Net_Weight' in self.config.routing_datasource_properties_required:
            routing_upload_datasource.Net_Weight = self._get_net_weight(plex_part, pp_op)
        if 'Note' in self.config.routing_datasource_properties_required:
            routing_upload_datasource.Note = self._get_note(plex_part, pp_op)
        if 'Description' in self.config.routing_datasource_properties_required:
            routing_upload_datasource.Description = self._get_description(plex_part, pp_op)

        return routing_upload_datasource

    def _get_note(self, plex_part: Part, pp_op: OrderOperation):
        raise IntegrationNotImplementedError('_get_note is not implemented in a custom part operation factory')

    def _get_description(self, plex_part: Part, pp_op: OrderOperation):
        raise IntegrationNotImplementedError('_get_description is not implemented in a custom part operation factory')

    def _get_net_weight(self, plex_part: Part, pp_op: OrderOperation):
        raise IntegrationNotImplementedError('_get_net_weight is not implemented in a custom part operation factory')

    def _get_label_name(self, plex_part: Part, pp_op: OrderOperation):
        raise IntegrationNotImplementedError('_get_label_name is not implemented in a custom part operation factory')

    def _get_note_for_material(self, material_op: OrderOperation):
        raise IntegrationNotImplementedError('_get_note is not implemented in a custom part operation factory')

    def _get_description_for_material(self, material_op: OrderOperation):
        raise IntegrationNotImplementedError('_get_description_for_material is not implemented in a custom part operation factory')

    def _get_net_weight_for_material(self, material_op: OrderOperation):
        raise IntegrationNotImplementedError('_get_net_weight is not implemented in a custom part operation factory')

    def _get_label_name_for_material(self, material_op: OrderOperation):
        raise IntegrationNotImplementedError('_get_label_name is not implemented in a custom part operation factory')

    def _get_type(self, operation: OrderOperation):
        """
        tries to get type from operation, defaults to configured value
        """
        return self.utils.operation_utils.get_variable_value_from_operation(
            operation=operation,
            variable_name=self.config.part_operation_type_var_name,
            default=self.config.default_part_operation_type
        )
