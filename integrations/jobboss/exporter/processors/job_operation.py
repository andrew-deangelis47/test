import jobboss.models as jb
import datetime
import uuid
from paperless.objects.components import BaseOperation
from paperless.objects.orders import OrderComponent, OrderItem, OrderOperation
from jobboss.exporter.routing import generate_routing_lines
from . import JobBossProcessor
from paperless.custom_tables.custom_tables import CustomTable
from jobboss.query.job import get_template_job, get_most_recent_job
from baseintegration.datamigration import logger
from baseintegration.utils import safe_get, safe_round
from baseintegration.utils import trim_django_model
from django.utils.timezone import make_aware


class JobOperationProcessor(JobBossProcessor):

    def get_paperless_operation_to_jobboss_work_center_mapping(self):
        if self.pp_operation_to_jb_work_center_mapping is None:
            self.pp_operation_to_jb_work_center_mapping = {}
            try:
                operation_mapping_table_details = CustomTable.get('operation_to_work_center_mapping')
                rows = operation_mapping_table_details['rows']
                for row in rows:
                    pp_op_name = row['paperless_parts_operation_name']
                    jb_wc_name = row['jobboss_work_center_name']
                    jb_service_name = row['jobboss_service_name']
                    self.pp_operation_to_jb_work_center_mapping[pp_op_name] = [jb_wc_name, jb_service_name]
            except Exception as e:
                logger.error(f'Encountered an error fetching the operation to work center mapping: {e}')

    @staticmethod
    def get_jb_vendor_from_op_variable(vendor_variable, op, select_default_vendor=None):
        vendor_name = op.get_variable(vendor_variable)
        vendor_instance = jb.Vendor.objects.filter(vendor__iexact=vendor_name).last()
        return vendor_name, vendor_instance

    def get_default_vendor_instance(self, pp_operation, vendor_variable):
        vendor_name = pp_operation.get_variable(vendor_variable)
        default_vendor_name = self._exporter.erp_config.select_default_vendor
        vendor_instance = jb.Vendor.objects.filter(vendor__iexact=default_vendor_name).first()
        return vendor_name, vendor_instance

    @staticmethod
    def get_jb_service_name_from_op_variable(service_variable, op):
        service_name = op.get_variable(service_variable)
        if service_name:
            return service_name[:10]
        return None

    def get_jb_lead_days_from_op_variable(self, op: OrderOperation):
        return int(op.get_variable("Jobboss Lead Days") or 0)

    @staticmethod
    def get_notes(op, work_center_instance):
        notes = ""
        if op.notes is not None:
            notes += f"\nPaperless Parts Notes: {op.notes}"
        if work_center_instance is not None and work_center_instance.note_text is not None:
            notes += f"\nWork Center Notes:\n{work_center_instance.note_text}"
        return notes

    def assign_outside_service_paramters(self, comp: OrderComponent, job_op: jb.JobOperation, today, routing_line,
                                         op: OrderOperation):
        job_op.inside_oper = False
        job_op.cost_unit = 'ea'
        job_op.cost_unit_conv = 1
        job_op.trade_currency = 1
        job_op.trade_date = today
        op_cost = self._exporter.get_value_relative_to_current_node(op.cost.dollars)
        job_op.est_total_cost = safe_round(op_cost)
        job_op.note_text = self.get_notes(op, None)
        job_op.lag_hrs = None
        if comp.deliver_quantity:
            job_op.est_unit_cost = safe_round(op.cost.dollars / comp.deliver_quantity)

        vendor_variable_name = self._exporter.erp_config.vendor_variable
        default_vendor_name = self._exporter.erp_config.select_default_vendor
        vendor_name, vendor_instance = self.get_jb_vendor_from_op_variable(vendor_variable_name, op,
                                                                           default_vendor_name)
        if not vendor_instance:
            self.get_default_vendor_instance(op, vendor_variable_name)

        service_variable_name = self._exporter.erp_config.service_variable
        service_name = self.get_jb_service_name_from_op_variable(service_variable_name, op)

        job_op.vendor = vendor_instance
        job_op.wc_vendor = vendor_name[:10] if vendor_name is not None else "N/A"
        job_op.operation_service = service_name
        job_op.lead_days = self.get_jb_lead_days_from_op_variable(op)
        return job_op

    def assign_inside_service_parameters(self, job_op: jb.JobOperation, routing_line, op):
        logger.info(f"Assigning inside operation attributes for operation: {op.name}")
        work_center_instance = self.get_jobboss_work_center_instance(
            self.pp_operation_to_jb_work_center_mapping,
            self._exporter.erp_config.default_work_center_name, op.operation_definition_name
        )
        service_name = self.get_jb_operation_from_op_to_work_center_mapping(op)
        if not work_center_instance:
            work_center_instance = self.get_work_center_from_op_variable(op)
        if not work_center_instance:
            work_center_instance = self.get_work_center_from_op_def(op)
        if not work_center_instance:
            work_center_instance = self.get_default_jobboss_work_center()

        # Optionally set runtime based on standard integration selections
        if self._exporter.erp_config.assign_runtime_and_setup_time_from_standard_op_variables:
            self.get_standard_jb_runtime_and_units(op, job_op)

        job_op.inside_oper = True
        job_op.work_center = work_center_instance
        job_op.operation_service = service_name
        job_op.wc_vendor = work_center_instance.work_center[:10] \
            if work_center_instance is not None else "N/A"
        job_op.workcenter_oid = safe_get(work_center_instance, 'objectid')
        job_op.queue_hrs = safe_get(work_center_instance, 'queue_hrs')
        job_op.lag_hours = safe_get(work_center_instance, 'lag_hrs', default_value=0)
        job_op.note_text = self.get_notes(op, work_center_instance)
        job_op.est_run_labor = float(work_center_instance.run_labor_rate) * job_op.est_run_hrs \
            if work_center_instance is not None else 0
        job_op.est_labor_burden = work_center_instance.labor_burden if work_center_instance is not None else 0
        return job_op

    def get_standard_jb_runtime_and_units(self, pp_operation, job_op: jb.JobOperation):
        runtime = pp_operation.get_variable("Jobboss Runtime")
        runtime_units = pp_operation.get_variable("Runtime Units")
        setup_time = pp_operation.get_variable("Jobboss Setup Time")
        job_op.est_setup_hrs = setup_time
        if runtime_units and runtime:
            job_op.run_method = runtime_units
            job_op.run = runtime
        elif runtime_units == "FixedHrs":
            runtime = setup_time
            job_op.run_method = runtime_units
            job_op.run = 0
            job_op.est_setup_hrs = runtime
            job_op.est_total_hrs = setup_time
        else:
            logger.info("Could not determine runtime units and/or runtime, defaulting to Min/Part units")
            job_op.run_method = "Min/Part"
            job_op.run = (pp_operation.runtime * 60) if pp_operation.runtime is not None else 0

    def get_jb_operation_from_op_to_work_center_mapping(self, pp_operation):
        op_service_row = self.pp_operation_to_jb_work_center_mapping.get(pp_operation.operation_definition_name, None)
        if op_service_row:
            service_name = op_service_row[1]
        else:
            service_name = self.get_service_name(pp_operation)
        return service_name

    def get_service_name(self, pp_operation):
        """
        Override this function if you need to implement customization to assign a service with more
        granularity than provided by the custom table operation to work center/service mapping.
        """
        return None

    @staticmethod
    def get_jobboss_work_center_instance(pp_to_job_op_mapping: dict, default_work_center_name: str, op_name: str):
        """
        - Returns a work center instance from custom table operation to work center mapping if exists.
        - If no valid match is found, returns None and subsequent handling will find a work center
        - This is the primary method of determining a work center name.
        """
        logger.info("Attempting to get jb work center from 'operation_to_work_center_mapping'")
        op_map_row = pp_to_job_op_mapping.get(op_name, None)
        if op_map_row:
            wc_name = op_map_row[0]  # Gets the work center name from the custom table operation to WC map
            work_center_instance = jb.WorkCenter.objects.filter(work_center=wc_name).last()
            return work_center_instance
        return None

    def get_work_center_from_op_variable(self, pp_job_op):
        """
        If no custom table op map exits, check for an operation variable containing the work center name.
        - Return: work center instance
        """
        work_center_name = pp_job_op.get_variable(self._exporter.erp_config.standard_work_center_variable_name)
        logger.info(f"Attempting to get work center instance from operation variable: {work_center_name}")
        if work_center_name is not None:
            work_center_instance = jb.WorkCenter.objects.filter(work_center=work_center_name).first()
            if work_center_instance:
                return work_center_instance
        return None

    def get_work_center_from_op_def(self, pp_job_op):
        """
        If the first two methods fail, try using the operation definition name to query the work center
        - Return: work center instance
        """
        op_def_name = pp_job_op.operation_definition_name
        logger.info(f"Attempting to get work center instance from operation definition name: {op_def_name}")
        work_center_instance = jb.WorkCenter.objects.filter(work_center=op_def_name).first()
        return work_center_instance

    def get_default_jobboss_work_center(self):
        """
        Returns default work center instance, if specified default is valid. Else returns None.
        """
        default_wc_name = self._exporter.erp_config.default_work_center_name
        logger.info(f"Attempting to get default work center instance: {default_wc_name}")
        default_wc_instance = jb.WorkCenter.objects.filter(work_center=default_wc_name).first()
        if default_wc_instance is None:
            logger.info("\n\nDid you assign a valid default work center in config.yaml?\n\n")
        return default_wc_instance

    def create_routing_from_template_job(self, template_job: jb.Job, comp: OrderComponent, job: jb.Job, now):
        job_ops = []
        router_total_hours = 0
        operations_list = jb.JobOperation.objects.filter(job=template_job)
        j = -1
        for op in operations_list:
            operation_total_hours = self.get_template_job_operation_total_hours(comp, op)
            operation_run_hours = self.get_template_job_operation_run_hours(comp, op)
            router_total_hours += operation_total_hours
            j += 1
            job_op = jb.JobOperation(
                job=job,
                work_center=op.work_center,
                wc_vendor=op.wc_vendor,
                vendor=op.vendor,
                inside_oper=op.inside_oper,
                operation_service=op.operation_service,
                workcenter_oid=op.workcenter_oid,
                queue_hrs=op.queue_hrs,
                sequence=op.sequence,
                description=op.description,
                priority=op.priority,
                run_method=op.run_method,
                run=op.run,
                est_run_per_part=op.est_run_per_part,
                efficiency_pct=op.efficiency_pct,
                attended_pct=op.attended_pct,
                est_total_hrs=operation_total_hours,
                est_setup_hrs=op.est_setup_hrs,
                est_run_hrs=operation_run_hours,
                est_setup_labor=op.est_setup_labor,
                est_run_labor=op.est_run_labor,
                est_labor_burden=op.est_labor_burden,
                est_machine_burden=op.est_machine_burden,
                est_ga_burden=op.est_ga_burden,
                est_required_qty=self._exporter.get_make_quantity(comp),
                est_unit_cost=op.est_unit_cost,
                est_addl_cost=op.est_addl_cost,
                est_total_cost=op.est_total_cost,
                deferred_qty=self._exporter.get_make_quantity(comp),
                act_setup_hrs=0,
                act_run_hrs=0,
                act_run_qty=0,
                act_scrap_qty=0,
                act_setup_labor=0,
                act_run_labor=0,
                act_labor_burden=0,
                act_machine_burden=0,
                act_ga_burden=0,
                act_unit_cost=0,
                act_addl_cost=0,
                act_total_cost=0,
                setup_pct_complete=0,
                run_pct_complete=0,
                rem_run_hrs=operation_run_hours,
                rem_setup_hrs=op.rem_setup_hrs,
                rem_total_hrs=op.rem_total_hrs,
                overlap=0,
                overlap_qty=0,
                est_ovl_hrs=0,
                lead_days=op.lead_days,
                schedule_exception_old=False,
                status='O',
                minimum_chg_amt=0,
                cost_unit_conv=0,
                currency_conv_rate=1,
                fixed_rate=True,
                rwk_quantity=0,
                rwk_setup_hrs=0,
                rwk_run_hrs=0,
                rwk_setup_labor=0,
                rwk_run_labor=0,
                rwk_labor_burden=0,
                rwk_machine_burden=0,
                rwk_ga_burden=0,
                rwk_scrap_qty=0,
                note_text=op.note_text,
                last_updated=now,
                act_run_labor_hrs=0,
                setup_qty=0,
                run_qty=0,
                rwk_run_labor_hrs=0,
                rwk_setup_qty=0,
                rwk_run_qty=0,
                act_setup_labor_hrs=0,
                rwk_setup_labor_hrs=0,
                objectid=str(uuid.uuid4()),
                job_oid=job.objectid,
                sched_resources=1,
                manual_start_lock=False,
                manual_stop_lock=False,
                priority_zero_lock=False,
                firm_zone_lock=False,
                sb_runmethod=None
            )
            try:
                job_op = trim_django_model(job_op)
                job_op.save()
                logger.info(f'Saved template JobOperation {j} - {job_op.work_center} {job_op.vendor}')
            except:
                logger.error(f'Could not save JobOperation {job_op.description}')
                logger.error(job_op.__dict__)
                raise
            job_ops.append(job_op)
        self.save_job_total_hours(job, router_total_hours)
        return job_ops

    def create_new_routing_line(self, job: jb.Job, j: int, comp: OrderComponent, op, now, runtime: int = 0,
                                setup_time: int = 0):
        job_op = jb.JobOperation(
            job=job,
            sequence=j,
            description=op.name[0:25] if op.name else None,
            priority=5,
            run_method='Min/Part',
            run=round(runtime * 60, 2),
            est_run_per_part=round(runtime, 2),
            efficiency_pct=100,
            attended_pct=100,
            queue_hrs=0,
            est_total_hrs=round(self._exporter.get_make_quantity(comp) * runtime + setup_time, 2),
            est_setup_hrs=round(setup_time, 2),
            est_run_hrs=round(runtime * self._exporter.get_make_quantity(comp), 2),
            est_setup_labor=0,
            est_run_labor=0,
            est_labor_burden=0,
            est_machine_burden=0,
            est_ga_burden=0,
            est_required_qty=self._exporter.get_make_quantity(comp),
            est_unit_cost=0,
            est_addl_cost=0,
            est_total_cost=0,
            deferred_qty=self._exporter.get_make_quantity(comp),
            act_setup_hrs=0,
            act_run_hrs=0,
            act_run_qty=0,
            act_scrap_qty=0,
            act_setup_labor=0,
            act_run_labor=0,
            act_labor_burden=0,
            act_machine_burden=0,
            act_ga_burden=0,
            act_unit_cost=0,
            act_addl_cost=0,
            act_total_cost=0,
            setup_pct_complete=0,
            run_pct_complete=0,
            rem_run_hrs=round(runtime * self._exporter.get_make_quantity(comp), 2),
            rem_setup_hrs=round(setup_time, 2),
            rem_total_hrs=round(self._exporter.get_make_quantity(comp) * runtime + setup_time, 2),
            overlap=0,
            overlap_qty=0,
            est_ovl_hrs=0,
            lead_days=0,
            schedule_exception_old=False,
            status='O',
            minimum_chg_amt=0,
            cost_unit_conv=0,
            currency_conv_rate=1,
            fixed_rate=True,
            rwk_quantity=0,
            rwk_setup_hrs=0,
            rwk_run_hrs=0,
            rwk_setup_labor=0,
            rwk_run_labor=0,
            rwk_labor_burden=0,
            rwk_machine_burden=0,
            rwk_ga_burden=0,
            rwk_scrap_qty=0,
            last_updated=now,
            act_run_labor_hrs=0,
            setup_qty=0,
            run_qty=0,
            rwk_run_labor_hrs=0,
            rwk_setup_qty=0,
            rwk_run_qty=0,
            act_setup_labor_hrs=0,
            rwk_setup_labor_hrs=0,
            objectid=str(uuid.uuid4()),
            job_oid=job.objectid,
            sched_resources=1,
            manual_start_lock=False,
            manual_stop_lock=False,
            priority_zero_lock=False,
            firm_zone_lock=False,
            sb_runmethod=None,
        )
        return job_op

    @staticmethod
    def get_runtime(comp: OrderComponent, op):
        if isinstance(op, BaseOperation):
            return op.runtime if op.runtime is not None else 0
        return 0

    @staticmethod
    def get_setup_time(comp: OrderComponent, op):
        if isinstance(op, BaseOperation):
            return op.setup_time if op.setup_time is not None else 0
        return 0

    @staticmethod
    def should_ignore_op(pp_to_job_op_mapping: dict, op_def_name):
        op_map_row = pp_to_job_op_mapping.get(op_def_name, None)
        if op_map_row is not None:
            should_ignore = op_map_row[0].strip().upper()
            if should_ignore == "IGNORE":
                return True
        return False

    def get_operation_total_hours(self, comp: OrderComponent, setup_time, runtime):
        operation_total_hours = round(self._exporter.get_make_quantity(comp) * runtime + setup_time, 2)
        logger.info(f"Operation Total Hours: {operation_total_hours}")
        return operation_total_hours

    def get_template_job_operation_total_hours(self, comp: OrderComponent, job_op: jb.JobOperation):
        """
        Calculates job total hours from a template job.
        - JobBOSS calculates total hours = est_run_per_part (hrs) * part_qty + setup_time
        - Besides the "FixedHrs" run_method, the "est_run_per_part" field is always in units of time(hrs)/part
        - If units are "FixedHrs" this means the total hours are calculated independent of quantity
        - Note: JB only stores the "run" to 2 decimal places, so if the "run" is 200 parts/hr, the calculated hrs/part
          should equal 0.005, but JB will round to 0.01.
        """
        est_run_per_part = job_op.est_run_per_part
        make_quantity = self._exporter.get_make_quantity(comp)
        total_setup_time = self._exporter.get_value_relative_to_current_node(job_op.est_setup_hrs)
        if job_op.run_method == "FixedHrs":
            total_runtime = est_run_per_part
        else:
            total_runtime = est_run_per_part * make_quantity
        return total_setup_time + total_runtime

    def get_template_job_operation_run_hours(self, comp: OrderComponent, job_op: jb.JobOperation):
        est_run_per_part = job_op.est_run_per_part
        if job_op.run_method == "FixedHrs":
            total_runtime = est_run_per_part
        else:
            total_runtime = est_run_per_part * self._exporter.get_make_quantity(comp)
        return total_runtime

    @staticmethod
    def save_job_total_hours(job: jb.Job, router_total_hours):
        job.est_total_hrs = router_total_hours
        try:
            job.save()
            logger.info(f"Saved job total hours: {router_total_hours} to job: {job.job}")
        except Exception as e:
            logger.info(f"Could not update Job Total Hours - ERROR {e}")

    def _process(self, order_item: OrderItem, comp: OrderComponent, job: jb.Job, top_level_router):
        self.get_paperless_operation_to_jobboss_work_center_mapping()  # noqa: F841
        now = make_aware(datetime.datetime.utcnow())
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        op_ignore = self._exporter.erp_config.op_ignore.split(",")
        operations_list = comp.shop_operations + top_level_router
        template_job = get_template_job(comp, self._exporter.erp_config)
        matching_part_number_job = get_most_recent_job(comp, self._exporter.erp_config)
        job_ops = []
        router_total_hours = 0

        if self._exporter.erp_config.template_job_matching_enabled and template_job:
            job_ops = self.create_routing_from_template_job(template_job, comp, job, now)
        elif self._exporter.erp_config.part_number_job_matching_enabled and matching_part_number_job:
            logger.info(f"Matched part number: {comp.part_number} with Job: {matching_part_number_job}")
            job_ops = self.create_routing_from_template_job(matching_part_number_job, comp, job, now)
        else:
            j = -1
            for op in operations_list:
                runtime = self.get_runtime(comp, op)
                setup_time = self.get_setup_time(comp, op)
                setup_time = self._exporter.get_value_relative_to_current_node(setup_time)
                op_def_name = op.operation_definition_name
                routing_lines = list(generate_routing_lines(op_def_name))
                should_ignore_op = self.should_ignore_op(self.pp_operation_to_jb_work_center_mapping, op_def_name)
                for k, routing_line in enumerate(routing_lines):
                    if op_def_name in op_ignore or should_ignore_op:
                        logger.info(f"Ignoring operation: {op_def_name}")
                        continue
                    j += 1
                    router_total_hours += self.get_operation_total_hours(comp, setup_time, runtime)
                    job_op = self.create_new_routing_line(job, j, comp, op, now, runtime, setup_time)
                    if op.is_outside_service:
                        job_op = self.assign_outside_service_paramters(comp, job_op, today, routing_line, op)
                    else:
                        job_op = self.assign_inside_service_parameters(job_op, routing_line, op)
                    try:
                        job_op = trim_django_model(job_op)
                        job_op.save()
                        logger.info(f'Saved JobOperation {j} - Work Center: {job_op.work_center}, Service: {job_op.operation_service} Vendor: {job_op.vendor}')
                    except:
                        logger.error(f'Could not save JobOperation {job_op.description}')
                        logger.error(job_op.__dict__)
                        raise
                    job_ops.append(job_op)
            self.save_job_total_hours(job, router_total_hours)
        return job_ops
