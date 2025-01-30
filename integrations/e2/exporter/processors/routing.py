import e2.models as e2
from e2.exporter.processors import E2Processor
from baseintegration.datamigration import logger
from datetime import datetime
from paperless.custom_tables.custom_tables import CustomTable

from e2.utils.utils import RoutingLinesData

MINUTES_PER_HOUR = 60.
SECONDS_PER_MINUTE = 60.


class RoutingProcessor(E2Processor):
    do_rollback = False

    def _process(self, component, part, is_part_new):
        should_populate_routing = self.should_populate_routing_on_part_from_paperless_operations(component, is_part_new)
        if should_populate_routing:
            routing_lines = self.populate_routing_on_part_from_paperless_operations(component, part)
            return RoutingLinesData(routing_lines=routing_lines)

    def should_populate_routing_on_part_from_paperless_operations(self, component, is_part_new):
        should_populate_routing = False
        if is_part_new:
            should_populate_routing = True
        else:
            if self._exporter.erp_config.should_replace_e2_routing_for_existing_parts:
                should_populate_routing = True
        if component.type == 'purchased':
            should_populate_routing = False
        return should_populate_routing

    def populate_routing_on_part_from_paperless_operations(self, component, part):
        self.clear_routing_for_part(part)

        routing_lines = []
        step_number = 10
        for operation in component.shop_operations:
            if self.should_skip_operation(operation):
                continue

            if operation.is_outside_service:
                routing_line = self.create_routing_line_from_outside_operation(part, operation, step_number, component)
            else:
                routing_line = self.create_routing_line_from_inside_operation(part, operation, step_number, component)

            routing_lines.append(routing_line)
            step_number += 10
        return tuple(routing_lines)

    def clear_routing_for_part(self, part):
        part_number = part.partno
        # Clear the existing Routing records for part_number
        existing_routing_records = e2.Routing.objects.filter(partno=part_number)
        if existing_routing_records:
            logger.info(f'Deleting {len(existing_routing_records)} Routing records for part number {part_number}')
            existing_routing_records.delete()

    def create_routing_line_from_inside_operation(self, part, operation, step_number, component):
        work_center_short_name, is_default_work_center_name = self.get_work_center_name(operation)

        default_work_center = self.get_or_create_default_work_center()

        # Get the WorkCntr record and accompanying default OperCode record
        # The E2 UI enforces uniqueness of the WorkCntr ShortName field, so we can use this in place of a primary key
        work_center = e2.Workcntr.objects.filter(shortname=work_center_short_name).first()
        if work_center is None:
            logger.info(f'Could not find a WorkCntr record with ShortName {work_center_short_name} - assigning to '
                        f'default work center {default_work_center.shortname}')
            work_center = default_work_center
            is_default_work_center_name = True

        op_code = self.map_pp_op_to_e2_op_code_from_op_var(operation)
        if op_code is not None:
            oper_code = e2.Opercode.objects.filter(opercode=op_code).first()
        else:
            oper_code = e2.Opercode.objects.filter(opercode=work_center.opercode).first()
        if oper_code is not None:
            routing_oper_code = oper_code.opercode
            team_size = oper_code.teamsize
            scrap_pct = oper_code.scrappct
            pct_eff = oper_code.pcteff
            unattend_op = oper_code.unattendop
            num_mach_for_job = oper_code.nummach
            descrip = oper_code.newdescrip
        else:
            logger.info('Could not find an OperCode record for this work center')
            routing_oper_code = None
            team_size = None
            scrap_pct = None
            pct_eff = None
            unattend_op = None
            num_mach_for_job = None
            descrip = self.get_inside_operation_description(is_default_work_center_name, operation)

        # Get the Estim record
        estim = part
        part_number = part.partno

        # Create the Routing record
        setup_time = operation.setup_time if operation.setup_time is not None else 0.
        setup_time = self._exporter.get_value_relative_to_current_node(setup_time)
        setup_rate = work_center.setup1 if work_center.setup1 is not None else 0.
        setup_price = setup_time * setup_rate  # TODO - should we fill this out if we're just using the operation.cost for the total field?
        runtime = operation.runtime if operation.runtime is not None else 0.
        cycle_rate = work_center.cycle1 if work_center.cycle1 is not None else 0.
        cycle_price = runtime * cycle_rate  # TODO - should we fill this out if we're just using the operation.cost for the total field?
        work_or_vend = 0

        display_setup_time, display_setup_time_units = self.get_display_setup_time(setup_time)
        display_runtime, display_runtime_units = self.get_display_runtime_units(runtime)

        routing_line = e2.Routing.objects.create(
            partno=part_number,
            stepno=step_number,
            workorvend=work_or_vend,
            workcntr=work_center.shortname,
            vendcode=None,
            opercode=routing_oper_code,
            descrip=descrip,
            setuptime=display_setup_time,
            timeunit=display_setup_time_units,
            cycletime=display_runtime,
            cycleunit=display_runtime_units,
            machrun=1,  # TODO - what to do here? Is this nummach from Opercode?
            teamsize=team_size,
            scrappct=scrap_pct,
            pcteff=pct_eff,
            laboracct=work_center.laboracct,
            setuprate=setup_rate,
            cyclerate=cycle_rate,
            burdenrate=work_center.burdenrate,
            laborrate=work_center.laborrate,
            unattendop=unattend_op,
            leadtime=estim.leadtime,
            markuppct=estim.markuppct,
            certreq='N',
            glacct=None,
            cost1=0.,
            unit1='EA',
            setup1=0.,
            cost2=0.,
            unit2='EA',
            setup2=0.,
            cost3=0.,
            unit3='EA',
            setup3=0.,
            cost4=0.,
            unit4='EA',
            setup4=0.,
            cost5=0.,
            unit5='EA',
            setup5=0.,
            cost6=0.,
            unit6='EA',
            setup6=0.,
            cost7=0.,
            unit7='EA',
            setup7=0.,
            cost8=0.,
            unit8='EA',
            setup8=0.,
            setupprice=setup_price,
            cycleprice=cycle_price,
            total=self._exporter.get_value_relative_to_current_node(operation.cost.dollars),
            estimqty=None,
            actualpiecesgood=None,
            actualpiecesscrapped=None,
            ignorevendmin=None,
            nummachforjob=num_mach_for_job,
            lastmoddate=None,
            lastmoduser=None,
        )
        return routing_line

    def get_inside_operation_description(self, is_default_work_center_name, operation):
        # If we are assigning to the default work center, indicate what the PP Operation was called in the description
        descrip = operation.notes if operation.notes is not None else ''
        if is_default_work_center_name:
            preamble = f'Could not find PP op {operation.name} - please update the mapping.'
            descrip = f'{preamble} \n\n{descrip}'
        return descrip

    def get_display_runtime_units(self, runtime):
        if self._exporter.erp_config.runtime_units == 'M':
            display_runtime = runtime * MINUTES_PER_HOUR
            display_runtime_units = 'M'
        elif self._exporter.erp_config.runtime_units == 'S':
            display_runtime = runtime * MINUTES_PER_HOUR * SECONDS_PER_MINUTE
            display_runtime_units = 'S'
        else:
            display_runtime = runtime
            display_runtime_units = 'H'

        return display_runtime, display_runtime_units

    def get_display_setup_time(self, setup_time):
        if self._exporter.erp_config.setup_time_units == 'M':
            display_setup_time = setup_time * MINUTES_PER_HOUR
            display_setup_time_units = 'M'
        else:
            display_setup_time = setup_time
            display_setup_time_units = 'H'
        return display_setup_time, display_setup_time_units

    def get_work_center_name(self, operation):
        is_default_work_center_name = False
        work_center_short_name = self.map_pp_op_to_e2_work_center(operation)
        if work_center_short_name is None:
            logger.info(f'Did not find {operation.name} or {operation.operation_definition_name} in '
                        f'PAPERLESS_PARTS_OPERATION_TO_E2_WORK_CENTER_MAPPING - assigning default work center')
            is_default_work_center_name = True
            work_center_short_name = self._exporter.erp_config.default_work_center_name
        return work_center_short_name, is_default_work_center_name

    def map_pp_op_to_e2_work_center(self, operation):
        PAPERLESS_PARTS_OPERATION_TO_E2_WORK_CENTER_MAPPING = \
            self.get_paperless_parts_operation_to_e2_work_center_mapping()
        work_center_short_name = PAPERLESS_PARTS_OPERATION_TO_E2_WORK_CENTER_MAPPING.get(operation.name, None)
        if work_center_short_name is None:
            work_center_short_name = PAPERLESS_PARTS_OPERATION_TO_E2_WORK_CENTER_MAPPING.get(
                operation.operation_definition_name, None)
        return work_center_short_name

    def create_routing_line_from_outside_operation(self, part, operation, step_number, component):
        vendor_code, is_default_vendor_code = self.get_vendor_code(operation)

        default_vendor_code = self.get_or_create_default_vendor_code()

        # Get the VendCode record
        vend_code = e2.Vendcode.objects.filter(vendcode=vendor_code).first()
        if vend_code is None:
            logger.info(f'Could not find a VendCode record with vendor code {vendor_code} - assigning to '
                        f'default vendor code {default_vendor_code.vendcode}')
            vend_code = default_vendor_code
            is_default_vendor_code = True

        descrip = self.get_outside_operation_description(is_default_vendor_code, operation)

        # Create the Routing record
        part_number = part.partno
        routing_line = e2.Routing.objects.create(
            partno=part_number,
            stepno=step_number,
            workorvend=1,
            workcntr=None,
            vendcode=vend_code.vendcode,
            opercode=None,
            descrip=descrip,
            setuptime=None,
            timeunit='H',
            cycletime=None,
            cycleunit='H',
            machrun=1,
            teamsize=1,
            scrappct=0,
            pcteff=100,
            laboracct=None,
            setuprate=None,
            cyclerate=None,
            burdenrate=None,
            laborrate=None,
            unattendop='N',
            leadtime=vend_code.leadtime,
            markuppct=vend_code.markup if vend_code.markup is not None else 0,
            certreq='N',
            glacct=vend_code.glacct1,
            cost1=0.,
            unit1='EA',
            setup1=0.,
            cost2=0.,
            unit2='EA',
            setup2=0.,
            cost3=0.,
            unit3='EA',
            setup3=0.,
            cost4=0.,
            unit4='EA',
            setup4=0.,
            cost5=0.,
            unit5='EA',
            setup5=0.,
            cost6=0.,
            unit6='EA',
            setup6=0.,
            cost7=0.,
            unit7='EA',
            setup7=0.,
            cost8=0.,
            unit8='EA',
            setup8=0.,
            setupprice=0.,
            cycleprice=0.,
            total=self._exporter.get_value_relative_to_current_node(operation.cost.dollars),
            estimqty=None,
            actualpiecesgood=None,
            actualpiecesscrapped=None,
            ignorevendmin=None,
            nummachforjob=1,
            lastmoddate=None,
            lastmoduser=None,
        )
        return routing_line

    def get_outside_operation_description(self, is_default_vendor_code, operation):
        # If we are assigning to the default vendor, indicate what the PP Operation was called in the description
        descrip = operation.notes if operation.notes is not None else ''
        if is_default_vendor_code:
            preamble = f'Could not find PP op {operation.name} - please update the mapping.'
            descrip = f'{preamble} \n\n{descrip}'
        return descrip

    def get_vendor_code(self, operation):
        is_default_vendor_code = False
        vendor_code = self.map_pp_op_to_e2_vend_code(operation)
        if vendor_code is None:
            logger.info(f'Did not find {operation.name} or {operation.operation_definition_name} in '
                        f'PAPERLESS_PARTS_OPERATION_TO_E2_VENDOR_CODE_MAPPING - assigning to default vendor code')
            is_default_vendor_code = True
            vendor_code = self._exporter.erp_config.default_vendor_code_name
        return vendor_code, is_default_vendor_code

    def map_pp_op_to_e2_vend_code(self, operation):
        if self._exporter.erp_config.should_get_vend_code_from_operation_variable:
            vendor_code = self.map_pp_op_to_e2_vend_code_from_op_var(operation)
        else:
            vendor_code = self.map_pp_op_to_e2_vend_code_from_dict(operation)
        return vendor_code

    def map_pp_op_to_e2_vend_code_from_dict(self, operation):
        PAPERLESS_PARTS_OPERATION_TO_E2_VENDOR_CODE_MAPPING = \
            self.get_paperless_parts_operation_to_e2_vendor_code_mapping()
        vendor_code = PAPERLESS_PARTS_OPERATION_TO_E2_VENDOR_CODE_MAPPING.get(operation.name, None)
        if vendor_code is None:
            vendor_code = PAPERLESS_PARTS_OPERATION_TO_E2_VENDOR_CODE_MAPPING.get(
                operation.operation_definition_name, None)
        return vendor_code

    def map_pp_op_to_e2_vend_code_from_op_var(self, operation):
        vend_code = operation.get_variable(self._exporter.erp_config.vendor_code_operation_variable_name)
        if vend_code is not None:
            vend_code = vend_code.upper()
        return vend_code

    def map_pp_op_to_e2_op_code_from_op_var(self, operation):
        op_code = operation.get_variable(self._exporter.erp_config.op_code_operation_variable_name)
        if op_code is not None:
            op_code = op_code.upper()
        return op_code

    def get_or_create_default_work_center(self):
        default_work_center_name = self._exporter.erp_config.default_work_center_name
        default_work_center = e2.Workcntr.objects.filter(shortname=default_work_center_name).first()
        if default_work_center is None:
            # The WorkCntr table doesn't appear to use the NextNumber table to determine its next id, for some reason.
            # This suggests that the WorkCntr column is managed using E2 application logic. We'll simulate this by
            # finding the max existing value and incrementing it by 1
            existing_work_centers = [work_center.workcntr for work_center in e2.Workcntr.objects.all()]
            highest_existing_work_center_number = max(existing_work_centers) if existing_work_centers else 0
            new_work_center_number = highest_existing_work_center_number + 1
            logger.info(f'Creating new default work center {default_work_center_name}')
            default_work_center = e2.Workcntr.objects.create(
                workcntr=new_work_center_number,
                descrip='PP Integration Default',
                queueunit='H',  # This was filled out when minimally populating a new WorkCntr in the UI
                shortname=default_work_center_name,  # This was filled out when minimally populating a new WorkCntr in the UI
                capacityfactor=1,  # This was filled out when minimally populating a new WorkCntr in the UI
                active='Y',  # This was filled out when minimally populating a new WorkCntr in the UI
                loadingmethod='FINITE',  # This was filled out when minimally populating a new WorkCntr in the UI
                utilizationpct=100,  # This was filled out when minimally populating a new WorkCntr in the UI
            )
        return default_work_center

    def get_or_create_default_vendor_code(self):
        default_vendor_code_name = self._exporter.erp_config.default_vendor_code_name
        default_vendor_code = e2.Vendcode.objects.filter(vendcode=default_vendor_code_name).first()
        if default_vendor_code is None:
            logger.info(f'Creating new default vendor code {default_vendor_code_name}')
            now = datetime.now()
            default_vendor_code = e2.Vendcode.objects.create(
                vendcode=default_vendor_code_name,
                vendname='PP Integration Default',
                vendtype='',
                printticket='N',
                outserv='N',
                dateopen=now,
                enterby=self._exporter.erp_config.entered_by,
                enterdate=now,
                currencycode='USA',
                salestaxcode=self._exporter.erp_config.tax_exempt_code,
                schedbegin='09:00',
                schedend='17:00',
                worksaturday='N',
                worksunday='N',
                active='Y',
                ten99='N',
                shipcode='',
                qbvendcode='PP Integration Default',
            )
        return default_vendor_code

    def should_skip_operation(self, operation):
        should_skip_operation = False
        skip_list = self.get_operation_skip_list()
        if operation.name in skip_list or operation.operation_definition_name in skip_list:
            should_skip_operation = True
        return should_skip_operation

    def get_operation_skip_list(self):
        if self._exporter.operation_skip_list is None:
            skip_list = []
            try:
                logger.info('Fetching operation skip list from Paperless Parts')
                skip_list_mapping_table_details = CustomTable.get('operation_skip_list')
                rows = skip_list_mapping_table_details['rows']
                for row in rows:
                    skip_list.append(row['paperless_parts_operation_name'])
            except Exception as e:
                logger.error(f'Encountered an error fetching the operation skip list: {e}')
            self._exporter.operation_skip_list = skip_list
        return self._exporter.operation_skip_list

    def get_paperless_parts_operation_to_e2_work_center_mapping(self):
        if self._exporter.pp_op_to_e2_work_center_mapping is None:
            op_to_work_center_mapping = {}
            try:
                logger.info('Fetching operation to work center mapping from Paperless Parts')
                operation_mapping_table_details = CustomTable.get('operation_to_work_center_mapping')
                rows = operation_mapping_table_details['rows']
                for row in rows:
                    op_to_work_center_mapping[row['paperless_parts_operation_name']] = row['e2_work_center_short_name']
            except Exception as e:
                logger.error(f'Encountered an error fetching the operation to work center mapping: {e}')
            self._exporter.pp_op_to_e2_work_center_mapping = op_to_work_center_mapping
        return self._exporter.pp_op_to_e2_work_center_mapping

    def get_paperless_parts_operation_to_e2_vendor_code_mapping(self):
        PAPERLESS_PARTS_OPERATION_TO_E2_VENDOR_CODE_MAPPING = {}
        return PAPERLESS_PARTS_OPERATION_TO_E2_VENDOR_CODE_MAPPING
