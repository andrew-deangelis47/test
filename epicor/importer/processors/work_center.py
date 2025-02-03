from typing import List

from copy import deepcopy
from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.custom_table import ImportCustomTable
from epicor.exceptions import EpicorNotFoundException
from epicor.api_models.paperless_custom_tables import OperationCustomTableFormat, ResourceGroupCustomTableFormat, \
    ResourceCustomTableFormat, OperationDetailsCustomTableFormat, CustomTableFormat
from epicor.operation import Operation, ResourceGroup, Resource, OperationDetails


class EpicorWorkCenterBulkImportProcessor(BaseImportProcessor):

    def _process(self, work_center_strings: List[str]) -> bool:
        logger.info("Processing work centers")
        operations: List[dict] = []
        resource_groups: List[dict] = []
        resources: List[dict] = []
        operation_details: List[dict] = []
        for work_center_string in work_center_strings:
            new_table_row: CustomTableFormat
            work_center_id = work_center_string.split('::')[0]
            work_center_type = work_center_string.split('::')[-1]
            try:
                if work_center_type == "operation":
                    logger.info(f"Processing operation {work_center_id}")
                    epicor_operation = Operation.get_by("OpCode", work_center_id)
                    new_table_row = self.get_operation_table_row(epicor_operation)
                    row_data = self.remove_table_name(new_table_row.__dict__)
                    operations.append(row_data)
                elif work_center_type == "resource_group":
                    logger.info(f"Processing resource group {work_center_id}")
                    epicor_resource_group = ResourceGroup.get_by("ResourceGrpID", work_center_id)
                    new_table_row = self.get_resource_group_table_row(epicor_resource_group)
                    row_data = self.remove_table_name(new_table_row.__dict__)
                    resource_groups.append(row_data)
                elif work_center_type == "resource":
                    logger.info(f"Processing resource {work_center_id}")
                    epicor_resource = Resource.get_by("ResourceID", work_center_id)
                    new_table_row = self.get_resource_table_row(epicor_resource)
                    row_data = self.remove_table_name(new_table_row.__dict__)
                    resources.append(row_data)
                elif work_center_type == "operation_details":
                    logger.info(f"Processing operation details {work_center_id}")
                    op_details_op_code = work_center_id.split("~~")[0]
                    op_details_resource_id = work_center_id.split("~~")[1]
                    # Need to include the $top to ensure it gets ALL OpMasDtls, as Epicor is page based
                    op_details_filter = {"OpCode": op_details_op_code, "ResourceGrpID": op_details_resource_id}
                    op_details_params = {"$top": 1000}
                    epicor_resource = OperationDetails.get_first(op_details_filter, op_details_params)
                    new_table_row = self.get_operation_details_table_row(epicor_resource)
                    row_data = self.remove_table_name(new_table_row.__dict__)
                    operation_details.append(row_data)
                else:
                    logger.info("Invalid WorkCenterIDData type, skipping")
                    continue
            except EpicorNotFoundException:
                logger.info("Work center not found in Epicor, skipping")
                continue

        operation_result: dict = ImportCustomTable.upload_records(
            identifier=f'epicor-operation-bulk-upload-count-{len(operations)}',
            table_name=OperationCustomTableFormat._custom_table_name,
            records=operations)

        resource_group_result: dict = ImportCustomTable.upload_records(
            identifier=f'epicor-resource-group-bulk-upload-count-{len(resource_groups)}',
            table_name=ResourceGroupCustomTableFormat._custom_table_name,
            records=resource_groups)

        resource_result: dict = ImportCustomTable.upload_records(
            identifier=f'epicor-resource-bulk-upload-count-{len(resources)}',
            table_name=ResourceCustomTableFormat._custom_table_name,
            records=resources)

        operation_details_result: dict = ImportCustomTable.upload_records(
            identifier=f'epicor-operation-details-bulk-upload-count-{len(operation_details)}',
            table_name=OperationDetailsCustomTableFormat._custom_table_name,
            records=operation_details)

        return len(
            (operation_result["failures"] + resource_group_result["failures"]
             ) + resource_result["failures"] + operation_details_result["failures"]
        ) == 0

    def get_operation_table_row(self, epicor_operation: Operation) -> OperationCustomTableFormat:
        paperless_table: OperationCustomTableFormat = deepcopy(self._importer._paperless_operation_table_model)
        op_details = epicor_operation.get_details(self._importer.erp_config)
        paperless_table.operation_code = epicor_operation.OpCode
        paperless_table.description = epicor_operation.OpDesc
        paperless_table.type = epicor_operation.OPType
        paperless_table.resource_group_id = op_details.ResourceGrpID
        paperless_table.resource_id = op_details.ResourceID
        paperless_table.subcontract = epicor_operation.Subcontract
        paperless_table.vendor_num = epicor_operation.VendorNum
        return paperless_table

    def get_resource_group_table_row(self, epicor_resource_group: ResourceGroup) -> ResourceGroupCustomTableFormat:
        paperless_table: ResourceGroupCustomTableFormat = deepcopy(self._importer._paperless_resource_group_table_model)
        paperless_table.resource_group_id = epicor_resource_group.ResourceGrpID
        paperless_table.description = epicor_resource_group.Description
        paperless_table.operation_code = epicor_resource_group.OpCode
        paperless_table.plant = epicor_resource_group.Plant
        paperless_table.prod_burden_rate = float(epicor_resource_group.ProdBurRate)
        paperless_table.prod_labor_rate = float(epicor_resource_group.ProdLabRate)
        paperless_table.setup_burden_rate = float(epicor_resource_group.SetupBurRate)
        paperless_table.setup_labor_rate = float(epicor_resource_group.SetupLabRate)
        paperless_table.quoting_prod_burden_rate = float(epicor_resource_group.QProdBurRate)
        paperless_table.quoting_prod_labor_rate = float(epicor_resource_group.QProdLabRate)
        paperless_table.quoting_setup_burden_rate = float(epicor_resource_group.QSetupBurRate)
        paperless_table.quoting_setup_labor_rate = float(epicor_resource_group.QSetupLabRate)
        return paperless_table

    def get_resource_table_row(self, epicor_resource: Resource) -> ResourceCustomTableFormat:
        paperless_table: ResourceCustomTableFormat = deepcopy(self._importer._paperless_resource_table_model)
        paperless_table.resource_id = epicor_resource.ResourceID
        paperless_table.description = epicor_resource.Description
        paperless_table.resource_group_id = epicor_resource.ResourceGrpID
        paperless_table.operation_code = epicor_resource.OpCode
        paperless_table.prod_burden_rate = float(epicor_resource.ProdBurRate)
        paperless_table.prod_labor_rate = float(epicor_resource.ProdLabRate)
        paperless_table.setup_burden_rate = float(epicor_resource.SetupBurRate)
        paperless_table.setup_labor_rate = float(epicor_resource.SetupLabRate)
        paperless_table.quoting_prod_burden_rate = float(epicor_resource.QProdBurRate)
        paperless_table.quoting_prod_labor_rate = float(epicor_resource.QProdLabRate)
        paperless_table.quoting_setup_burden_rate = float(epicor_resource.QSetupBurRate)
        paperless_table.quoting_setup_labor_rate = float(epicor_resource.QSetupLabRate)
        return paperless_table

    def get_operation_details_table_row(self, epicor_operation_details: OperationDetails) \
            -> OperationDetailsCustomTableFormat:
        paperless_table: OperationDetailsCustomTableFormat \
            = deepcopy(self._importer._paperless_operation_details_table_model)
        paperless_table.operation_details_id = str(epicor_operation_details.OpCode) + str(epicor_operation_details.ResourceGrpID)
        paperless_table.operation_code = epicor_operation_details.OpCode
        paperless_table.resource_group_id = epicor_operation_details.ResourceGrpID
        paperless_table.plant = epicor_operation_details.Plant
        return paperless_table

    def remove_table_name(self, table_data):
        try:
            del table_data["_custom_table_name"]
        except Exception:
            return table_data
        return table_data


class EpicorWorkCenterImportProcessor(EpicorWorkCenterBulkImportProcessor):
    def _process(self, work_center_string: str) -> bool:
        return super()._process([work_center_string])


class WorkCenterBulkPlaceholder:
    pass
