from typing import List, Union
from paperless.objects.orders import Order, OrderOperation, OrderItem, OrderComponent
from baseintegration.datamigration import logger
from epicor.operation import Operation
from epicor.quote import QuoteOperation, QuoteHeader
from epicor.utils import QuoteHeaderData, TreeNode, get_true_assembly_tree_nodes_by_line_number
from epicor.vendor import Vendor
from epicor.exceptions import EpicorNotFoundException
from epicor.exporter.v2_processors.base import EpicorProcessor
from paperless.custom_tables.custom_tables import CustomTable


class QuoteOperationProcessor(EpicorProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'quote_operations'

    def _process(self, order: Order, quote_header: QuoteHeader, quote_header_data: QuoteHeaderData):
        logger.info("Attempting to process all quote operations")
        self.line_items = quote_header_data.line_items
        self.component = None
        self.created_operations: dict = {}

        try:
            for order_item_sequence_num, order_item in enumerate(order.order_items, start=1):

                self.true_assembly_tree_nodes: List[TreeNode] = get_true_assembly_tree_nodes_by_line_number(
                    self.line_items, order_item_sequence_num
                )

                self.iterate_true_assembly_nodes(quote_header, order_item, order_item_sequence_num)
        except Exception as e:
            logger.info(f'Unexpected error in QuoteOperationProcessor processor: {e}')
            raise e

        # print to the integration export report
        if len(self.created_operations.keys()) > 0:
            self._add_report_message(f'Created the following quote operation: \n{self._get_integration_report_message()}')
        else:
            self._add_report_message('No operation created.')

    def iterate_true_assembly_nodes(self, quote_header: QuoteHeader, order_item: OrderItem,
                                    order_item_sequence_num: int):

        for node in self.true_assembly_tree_nodes:
            component = self.get_component(node.component_id, order_item)
            self.component = component

            # Don't add hardware operations to router - PC Piece Price op will never exist.
            if component.is_hardware:
                continue

            last_operation = None
            for operation in component.shop_operations:
                # Get a resource ID to assign to the quote operation
                operation_id = self.get_operation_id(operation)
                if operation_id is None:
                    logger.info(f"Skipped operation {operation.operation_definition_name}")
                    continue

                # Create the quote operation and add a quote operation detail when applicable
                quote_op = self.create_quote_operation(operation, quote_header, node, operation_id,
                                                       order_item_sequence_num, component)
                last_operation = quote_op

                if not self._exporter.erp_config.disable_quote_operation_details:
                    self.add_quote_operation_detail_resources(quote_op, operation)
                    self.add_quote_operation_detail_crew_size(quote_op, operation)
                else:
                    logger.info("Quote operation details are disabled for this integration.")

            self._set_last_operation_attributes(last_operation)

    def create_quote_operation(self, operation: OrderOperation, quote_header: QuoteHeader, node: TreeNode,
                               operation_id: str, order_item_sequence_num: int, component: OrderComponent
                               ) -> QuoteOperation:

        logger.info(f"Creating operation {order_item_sequence_num} - {operation.name} - {operation_id}")
        company_name = str(self._exporter.erp_config.company_name)
        vendor_num, vendor_num_vendor_id = None, None
        is_subcontract = False
        subcontract_lead_days = None
        subcontract_unit_cost = 0
        subcontract_min_charge = 0

        if operation.is_outside_service:
            is_subcontract = True
            vendor_num, vendor_num_vendor_id = self.get_subcontract_detail_info(operation)
            subcontract_lead_days = self.get_subcontract_lead_time(operation)
            subcontract_unit_cost = self.get_subcontract_unit_cost(operation, component.make_quantity)
            subcontract_min_charge = self.get_subcontract_min_charge(operation)

        comments = ''
        comments += self.get_operation_comments_from_id(operation_id)
        if operation.notes:
            comments += f'\n {operation.notes}'

        try:
            quote_op = QuoteOperation.create({
                "Company": company_name,
                "QuoteNum": quote_header.QuoteNum,
                "QuoteLine": int(order_item_sequence_num),
                "AssemblySeq": node.assembly_seq_num,
                "OpCode": operation_id,
                "OpDesc": self.get_operation_desc_from_id(operation_id),
                "CommentText": comments,
                "HoursPerMachine": operation.setup_time,
                "ProdStandard": self.get_runtime(operation),
                "StdFormat": self.get_runtime_format(operation),
                "StdBasis": self._exporter.erp_config.default_std_basis,
                "SubContract": is_subcontract,
                "VendorNum": vendor_num,
                "VendorNumVendorID": vendor_num_vendor_id,
                "PartNum": node.part_number,
                "Description": node.part_number,
                "DaysOut": subcontract_lead_days,
                "EstUnitCost": subcontract_unit_cost,
                "MinimumCost": subcontract_min_charge
            })
            self._add_to_created_ops_dict(quote_op)
            return quote_op

        except Exception as e:
            logger.info(f"Could not create operation - {operation_id} {e}")
            return self.assign_default_operation(operation, quote_header, node.assembly_seq_num, operation_id,
                                                 order_item_sequence_num)

    def assign_default_operation(self, operation, quote_header: QuoteHeader, assembly_seq_num: int, operation_id: str,
                                 order_item_sequence_num: int) -> QuoteOperation:

        company_name = str(self._exporter.erp_config.company_name)
        default_operation_name = str(self._exporter.erp_config.default_operation_id)
        logger.info(f"Attempting to assign default operation {default_operation_name} in place of {operation_id}.")

        try:
            quote_op = QuoteOperation.create({
                "Company": company_name,
                "QuoteNum": quote_header.QuoteNum,
                "QuoteLine": order_item_sequence_num,
                "AssemblySeq": assembly_seq_num,
                "OpCode": default_operation_name,
                "OpDesc": self.get_operation_desc_from_id(default_operation_name),
                "CommentText": operation.notes,
                "HoursPerMachine": operation.setup_time,
                "ProdStandard": self.get_runtime(operation),
                "StdFormat": self.get_runtime_format(operation)
            })
            self._add_to_created_ops_dict(quote_op)
            return quote_op

        except Exception as e:
            logger.info(f"Could not create operation. {e}. Skipping operation.")

    def add_quote_operation_detail_resources(self, quote_op: QuoteOperation, operation: OrderOperation):

        company_name = str(self._exporter.erp_config.company_name)
        resource_group_id = operation.get_variable(
            self._exporter.erp_config.pp_resource_group_id_variable
        ) or ""
        resource_id = operation.get_variable(self._exporter.erp_config.pp_resource_id_variable) or ""

        if resource_id or resource_group_id:
            logger.info(f"Adding quote detail with resource group id: {resource_group_id} or resource id: "
                        f"{resource_id}")
            quote_op.update_detail(company_name, {
                "ResourceGrpID": resource_group_id,
                "ResourceID": resource_id,
            })

    def add_quote_operation_detail_crew_size(self, quote_op: QuoteOperation, operation: OrderOperation):
        company_name = str(self._exporter.erp_config.company_name)
        prod_crew_size, setup_crew_size = self._get_crew_size(operation)

        quote_op.update_detail(company_name, {
            "ProdCrewSize": prod_crew_size,
            "SetUpCrewSize": setup_crew_size,
        })

    def get_runtime_format(self, operation: OrderOperation):
        valid_units = ['HP', 'PH', 'PM', 'MP', 'HR']
        try:
            operation_name = operation.operation_definition_name
            logger.info('Fetching operation to runtime units mapping')
            operation_units_mapping = CustomTable.get('operation_runtime_units_mapping')
            rows = operation_units_mapping['rows']
            for row in rows:
                if operation_name == row['operation']:
                    runtime_unit = row['runtime_units']
                    if runtime_unit not in valid_units:
                        raise ValueError(f'Invalid runtime unit: {runtime_unit} for operation {operation_name}')
                    logger.info(f'RUNTIME UNITS FETCHED FROM TABLE: {runtime_unit}')
                    return runtime_unit
        except Exception as e:
            logger.error(f'Encountered an error fetching operation units mapping: {e}')
            return self._exporter.erp_config.default_std_format

    def get_runtime(self, operation: OrderOperation) -> Union[float, int]:
        """
        If a customer requests different units, add the units and the respective runtime name and unit conversion to the
        runtime conversion calculation dictionary.
        """
        runtime_format = self.get_runtime_format(operation)
        runtime_hrs_per_part = operation.runtime

        if operation.runtime is None or runtime_hrs_per_part == 0:
            return 0

        runtime_conversion_calc_dict: dict = {
            "HP": runtime_hrs_per_part,  # Hrs/Part (standard Paperless runtime units)
            "PH": 1 / runtime_hrs_per_part,  # Parts/Hr (rounded down to int)
            "PM": (1 / runtime_hrs_per_part) / 60,  # Parts/Min (rounded down to int)
            "MP": runtime_hrs_per_part * 60,  # min / piece
            "HR": runtime_hrs_per_part * self.component.make_quantity
        }
        converted_runtime = runtime_conversion_calc_dict.get(runtime_format, 0)

        return round(converted_runtime, 2)

    def get_operation_id(self, operation: OrderOperation) -> Union[str, None]:
        operation_id = self.get_operation_mapping_from_op_variable(operation)
        if operation_id is None:
            operation_id = self.get_operation_mapping_from_op_def(operation)
        if operation_id in ("IGNORE", "ignore", "Ignore"):
            logger.info(f"Ignoring this operation - operation id indicates: {operation_id}")
            return None
        return operation_id

    def get_operation_mapping_from_op_variable(self, operation: OrderOperation) -> str:
        op_variable = self._exporter.erp_config.pp_op_id_variable
        logger.info(f"Attempting to get operation ID from operation variable: {op_variable}")
        operation_id = operation.get_variable(op_variable)
        return operation_id

    def get_operation_mapping_from_op_def(self, operation: OrderOperation) -> str:
        op_def_name = operation.operation_definition_name
        logger.info(f"Attempting to get OpCode ID from Paperless Parts operation definition name for {op_def_name}")
        return op_def_name

    def get_operation_desc_from_id(self, operation_id: str) -> str:
        logger.info("Attempting to GET OpDesc from existing OpMaster by OpCode ID.")
        return Operation.get_by('OpCode', operation_id).OpDesc

    def get_operation_comments_from_id(self, operation_id: str) -> str:
        logger.info("Attempting to GET CommentText from existing OpMaster by OpCode ID.")
        try:
            return Operation.get_by('OpCode', operation_id).CommentText
        except:
            logger.error('Could not find operation code, so no default comments being added')
            return ''

    def _get_crew_size(self, operation: OrderOperation):
        """
        Maps crew size from P3L operation to the Epicor quote operation's crew size.
        """

        crew_size_destination = self._exporter.erp_config.crew_size_destination
        crew_size = operation.get_variable(self._exporter.erp_config.crew_size_variable)
        logger.info("Attempting to get crew size.")

        if crew_size_destination == "both":
            return crew_size, crew_size
        elif crew_size_destination == "prod":
            return crew_size, None
        elif crew_size_destination == "setup":
            return None, crew_size
        return None, None

    def get_component(self, comp_id: int, order_item: OrderItem) -> OrderComponent:
        for comp in order_item.components:
            if comp.id == comp_id:
                return comp
            continue
        raise ValueError(f"Could not find component: {comp_id} in the node tree.")

    def get_subcontract_detail_info(self, pp_operation: OrderOperation):
        logger.info("Attempting to get subcontract information.")
        vendor_id = pp_operation.get_variable(self._exporter.erp_config.pp_vendor_id_variable)
        epicor_vendor_num = None
        epicor_vendor_id = None
        try:
            epicor_vendor: Vendor = Vendor.get_by_id(vendor_id)
            epicor_vendor_num = epicor_vendor.VendorNum
            epicor_vendor_id = epicor_vendor.VendorID
        except EpicorNotFoundException as e:
            logger.info(f"No vendor could be found based on vendor id: {vendor_id}. Error message: {e}")
        return epicor_vendor_num, epicor_vendor_id

    def get_subcontract_lead_time(self, pp_operation: OrderOperation) -> float:
        logger.info("Attempting to get subcontract lead days.")
        subcontract_vendor_lead_days = pp_operation.quantities[0].lead_time
        return round(float(subcontract_vendor_lead_days), 2)

    def get_subcontract_unit_cost(self, pp_operation: OrderOperation, make_quantity: int):
        logger.info("Attempting to get subcontract unit cost.")
        unit_cost = pp_operation.get_variable(self._exporter.erp_config.pp_vendor_unit_cost_variable)
        if unit_cost and unit_cost > 0:
            return unit_cost
        return round(pp_operation.cost.dollars / make_quantity, 2)

    def get_subcontract_min_charge(self, pp_operation: OrderOperation):
        logger.info("Attempting to get subcontract min charge.")
        min_charge = pp_operation.get_variable(self._exporter.erp_config.pp_vendor_lot_charge_variable)
        if min_charge:
            return min_charge
        return 0

    def _set_last_operation_attributes(self, operation: QuoteOperation):
        if operation:
            logger.info("Attempting to set final operation parameters, (AutoReceive, FinalOpr).")
            params = [
                f"'{self._exporter.erp_config.company_name}'",
                operation.QuoteNum,
                operation.QuoteLine,
                operation.AssemblySeq,
                operation.OprSeq,
            ]
            data = {
                "AutoReceive": True,
                "FinalOpr": True
            }
            operation.update_resource(params, data)
        return None

    def _add_to_created_ops_dict(self, quote_op: QuoteOperation):
        if quote_op.PartNum not in self.created_operations.keys():
            self.created_operations[quote_op.PartNum] = []
        self.created_operations[quote_op.PartNum].append(quote_op)

    def _get_integration_report_message(self):
        message = ""
        part_number: str
        for part_number in self.created_operations.keys():
            ops_for_part_str = [x.OpCode for x in self.created_operations[part_number]]
            message += f'Part {part_number}: {ops_for_part_str}\n'

        return message
