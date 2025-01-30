from inforsyteline.exporter.processors.job_route import JobRouteProcessor
from baseintegration.exporter import logger
from inforsyteline.utils import ItemData, add_notes
from inforsyteline.models import JobrouteMst, ItemMst, WcMst
from django.db import connection
from paperless.objects.orders import OrderOperation
from paperless.custom_tables.custom_tables import CustomTable


class Syteline10JobRouteProcessor(JobRouteProcessor):

    def get_paperless_operation_to_syteline_work_center_mapping(self):
        if self._exporter.workcenter_mapping is None:
            self._exporter.workcenter_mapping = {}
            try:
                operation_mapping_table_details = CustomTable.get('workcenter_mapping')
                rows = operation_mapping_table_details['rows']
                for row in rows:
                    pp_op_name = row['pp_op_def_name']
                    sl_wc = row['sl_workcenter']
                    sl_resource_group = row['sl_resource_group']
                    self._exporter.workcenter_mapping[pp_op_name] = [sl_wc, sl_resource_group]
            except Exception as e:
                logger.error(f'Encountered an error fetching the operation to work center mapping: {e}')
        return self._exporter.workcenter_mapping

    def get_work_center_id(self, operation: OrderOperation) -> str:
        wc_mapping = self.get_paperless_operation_to_syteline_work_center_mapping()
        if operation.operation_definition_name in wc_mapping:
            return wc_mapping[operation.operation_definition_name][0]
        else:
            return None

    def get_setup_resource_group(self, operation: OrderOperation) -> str:
        wc_mapping = self.get_paperless_operation_to_syteline_work_center_mapping()
        if operation.operation_definition_name in wc_mapping:
            return f"{wc_mapping[operation.operation_definition_name][1]}".replace("'", "")
        else:
            return "NULL"

    def create_operations(self, item: ItemData) -> None:
        sequence_no = 10
        component = item.component
        operations = component.shop_operations
        logger.info(f"Processing operations for {str(component.part_number)}")
        for operation in operations:
            logger.info(f"Operations being processed for operation {operation.name}")
            work_center_id: str = self.get_work_center_id(operation)
            pieces_per_hour: float = self.get_pieces_per_hour(operation)
            setup_labor_rate: float = self.get_setup_labor_rate(operation)
            machine_overhead_rate: float = self.get_machine_overhead_rate(operation)
            variable_overhead_rate: float = self.get_variable_overhead_rate(operation)
            setup_resource_group_id: str = self.get_setup_resource_group(operation)
            move_hrs = 0
            if not work_center_id:
                logger.info("Work center ID not found on operation. Must be an informational operation. Skipping and going to the next one")
                continue
            else:
                use_fixed_schedule = "NULL"
                logger.info(f"Work center ID is {work_center_id}")
            setup_hrs: float = round(operation.setup_time, 2) if operation.setup_time else 0
            run_hrs: float = round(operation.runtime, 2) if operation.runtime else 0
            logger.info(f"run is {run_hrs}")
            logger.info(f"setup is {setup_hrs}")
            logger.info(f"machine is {machine_overhead_rate}")
            logger.info(f"variable is {variable_overhead_rate}")
            logger.info(f"setup is {setup_labor_rate}")
            item_job = ItemMst.objects.filter(item=item.item_number).first().job
            if not self._exporter._integration.test_mode:
                logger.info("Making SQL execution")
                with connection.cursor() as cursor:
                    sql = f"""
                            USE [pMMP_App];
                            SET NOCOUNT ON;
                            DECLARE	@Infobar InfobarType;
                            DECLARE @return_value int;
                            DECLARE @myid uniqueidentifier;
                            SET @myid = NEWID();
                            Exec [dbo].[SetSiteSp] '{self._exporter.erp_config.site_ref}', Infobar
                            BEGIN TRAN;
                            EXEC @return_value = [dbo].[CreateCurrentOperationSp]
                            @Item='{item.item_number}',
                            @CopyOption='R',
                            @JobrouteOperNum='{sequence_no}',
                            @Jobroutewc='{work_center_id}',
                            @JobrouteRunBasisLbr='H',
                            @JobrouteRunBasisMch='H',
                            @JobrouteBflushType='N',
                            @JobrouteCntrlPoint='1',
                            @JobrouteSetupRate='{setup_labor_rate}',
                            @JobrouteEfficiency='70.0',
                            @JobrouteFovhdRateMch='{machine_overhead_rate}',
                            @JobrouteVovhdRateMch='0',
                            @JobrouteRunRateLbr='{setup_labor_rate}'
                            ,@JobrouteVarovhdRate='{variable_overhead_rate}'
                            ,@JobrouteFixovhdRate='0'
                            ,@JobrouteEffectDate=NULL
                            ,@JobrouteObsDate=NULL
                            ,@JobrouteYield='100'
                            ,@JrtSchSetupTicks='0'
                            ,@JrtSchSetupHrs='{setup_hrs}'
                            ,@JrtSchRunTicksLbr='{run_hrs}'
                            ,@JrtSchRunLbrHrs='{run_hrs}'
                            ,@JrtSchRunTicksMch='{run_hrs}'
                            ,@JrtSchRunMchHrs='{run_hrs}'
                            ,@JrtSchPcsPerLbrHr='{pieces_per_hour}'
                            ,@JrtSchPcsPerMchHr='{pieces_per_hour}'
                            ,@JrtSchSchedTicks={use_fixed_schedule}
                            ,@JrtSchSchedOff={use_fixed_schedule}
                            ,@JrtSchOffsetHrs='0'
                            ,@JrtSchMoveTicks='0'
                            ,@JrtSchMoveHrs='{move_hrs}'
                            ,@JrtSchQueueTicks='0'
                            ,@JrtSchQueueHrs='0'
                            ,@JrtSchFinishHrs='0'
                            ,@JrtSchMatrixType='F'
                            ,@JrtSchTabid=NULL
                            ,@JrtSchWhenrule='0'
                            ,@JrtSchSchedDrv='{self._exporter.erp_config.job_route_schedule_driver}'
                            ,@JrtSchPlannerStep='0'
                            ,@JrtSchSetuprgid='{setup_resource_group_id}'
                            ,@JrtSchSetuprule='5'
                            ,@JrtSchSchedsteprule='0'
                            ,@JrtSchCrsbrkrule='0'
                            ,@JrtSchAllowReallocation='0'
                            ,@JrtSchSplitsize='0'
                            ,@JrtSchBatchDefinitionId=NULL
                            ,@JobRouteRowPointer=@myid
                            ,@Infobar=@Infobar OUTPUT;
                            COMMIT TRAN;
                            SELECT @Infobar as N'@Infobar';
                            """
                    cursor.execute(sql)
                    try:
                        # log error message if appropriate
                        logger.info(cursor.fetchone()[0])
                    except:
                        pass
                    try:
                        logger.info("Attempting to add the job resource group")
                        job_resource_group_sql = f"INSERT INTO [dbo].[jrtresourcegroup_mst] (site_ref, job, suffix, oper_num, rgid, noteexistsflag, qty_resources) VALUES ('{self._exporter.erp_config.site_ref}', '{item_job}', '0', '{sequence_no}', '{setup_resource_group_id}', '0', '0');"
                        print(job_resource_group_sql)
                        cursor.execute(job_resource_group_sql)
                    except Exception as e:
                        logger.info(e)
                        logger.info("Was not able to add the job resource group, moving on")
            else:
                wc = WcMst.objects.filter(wc=int(work_center_id)).first()
                JobrouteMst.objects.create(site_ref="SYTE",
                                           job=item_job,
                                           oper_num=sequence_no,
                                           wc=wc,
                                           setup_hrs_t=setup_hrs,
                                           run_hrs_t_lbr=run_hrs
                                           )
            job_route: JobrouteMst = JobrouteMst.objects.filter(job=item_job, oper_num=sequence_no).first()
            if not job_route:
                raise ValueError(f"Job route {job_route} was not created in database. Actual SQL execution failed")
            else:
                logger.info("Adding notes")
                notes = operation.notes.replace("'", "") if operation.notes is not None else ""
                add_notes(object_name="jobroute", row_pointer=job_route.rowpointer, note_desc="Quote Notes", note_text=notes, database_name=self._exporter.erp_config.name)
            sequence_no = sequence_no + 10
            logger.info(f"Op {operation.name} with item number {item.item_number} has been created")
