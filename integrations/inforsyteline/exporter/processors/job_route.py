from baseintegration.exporter import BaseProcessor, logger
from paperless.objects.orders import OrderOperation
from inforsyteline.utils import ItemData
from inforsyteline.models import JobrouteMst, ItemMst, WcMst
from django.db import connection


class JobRouteProcessor(BaseProcessor):

    def _process(self, manufactured_components: list) -> None:
        logger.info("Processing job routing steps")
        for item in manufactured_components:
            item: ItemData = item
            if item.item_is_new and not item.component.is_hardware:
                logger.info(f"Creating routing for item {item.item_number}")
                self.create_operations(item)
            else:
                logger.info(f"Not creating routing for item {item.item_number} as it is either old or hardware")

    def get_work_center_id(self, operation: OrderOperation) -> str:
        return operation.get_variable(self._exporter.erp_config.pp_work_center_variable)

    def get_pieces_per_hour(self, operation: OrderOperation) -> float:
        pieces_per_hour = operation.get_variable("Pieces Per Hour")
        if not pieces_per_hour:
            pieces_per_hour = 0
        return pieces_per_hour

    def get_setup_labor_rate(self, operation: OrderOperation) -> float:
        setup_labor_rate = operation.get_variable("Setup Labor Rate")
        if not setup_labor_rate:
            setup_labor_rate = 0
        return setup_labor_rate

    def get_machine_overhead_rate(self, operation: OrderOperation) -> float:
        machine_overhead_rate = operation.get_variable("Machine Overhead Rate")
        if not machine_overhead_rate:
            machine_overhead_rate = 0
        return machine_overhead_rate

    def get_variable_overhead_rate(self, operation: OrderOperation) -> float:
        variable_overhead_rate = operation.get_variable("Variable Overhead Rate")
        if not variable_overhead_rate:
            variable_overhead_rate = 0
        return variable_overhead_rate

    def create_operations(self, item: ItemData) -> None:
        sequence_no = 10
        operations = item.routing_operations
        logger.info(f"Processing operations for {str(item.component.part_number)}")
        logger.info(f"Len of operations is {len(item.routing_operations)}")
        for operation in operations:
            logger.info(f"Operations being processed for operation {operation.name}")
            work_center_id: str = self.get_work_center_id(operation)
            pieces_per_hour: float = self.get_pieces_per_hour(operation)
            setup_labor_rate: float = self.get_setup_labor_rate(operation)
            machine_overhead_rate: float = self.get_machine_overhead_rate(operation)
            variable_overhead_rate: float = self.get_variable_overhead_rate(operation)
            if not work_center_id:
                logger.info("Work center ID not found on operation. Must be an informational operation. Skipping and going to the next one")
                continue
            else:
                logger.info(f"Work center ID is {work_center_id}")
            setup_time = operation.setup_time if operation.setup_time else 0
            runtime = operation.runtime if operation.runtime else 0
            setup_hrs: float = round(setup_time, 2)
            run_hrs: float = round(runtime, 2)
            if not self._exporter._integration.test_mode:
                with connection.cursor() as cursor:
                    sql = f"""
                            SET NOCOUNT ON;
                            DECLARE @RC int;
                            DECLARE @myid uniqueidentifier;
                            DECLARE	@Infobar InfobarType;
                            SET @myid = NEWID();
                            Exec [{self._exporter.erp_config.name}].[dbo].[SetSiteSp] '{self._exporter.erp_config.site_ref}', Infobar
                            EXEC [{self._exporter.erp_config.name}].[dbo].[CreateCurrentOperationSp]
                            @Item='{item.item_number}',
                            @DeleteExistingBOM='0',
                            @JobrouteOperNum='{sequence_no}',
                            @Jobroutewc='{work_center_id}',
                            @JobrouteRunBasisLbr='P',
                            @JobrouteRunBasisMch='P',
                            @JobrouteBflushType='C',
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
                            ,@JrtSchRunTicksLbr='0'
                            ,@JrtSchRunLbrHrs='{run_hrs}'
                            ,@JrtSchRunTicksMch='0'
                            ,@JrtSchRunMchHrs='0'
                            ,@JrtSchPcsPerLbrHr='{pieces_per_hour}'
                            ,@JrtSchPcsPerMchHr='{pieces_per_hour}'
                            ,@JrtSchSchedTicks='0'
                            ,@JrtSchSchedOff='0'
                            ,@JrtSchOffsetHrs='0'
                            ,@JrtSchMoveTicks='0'
                            ,@JrtSchMoveHrs='0'
                            ,@JrtSchQueueTicks='0'
                            ,@JrtSchQueueHrs='0'
                            ,@JrtSchFinishHrs='0'
                            ,@JrtSchMatrixType='F'
                            ,@JrtSchTabid=NULL
                            ,@JrtSchWhenrule='0'
                            ,@JrtSchSchedDrv='{self._exporter.erp_config.job_route_schedule_driver}'
                            ,@JrtSchPlannerStep='0'
                            ,@JrtSchSetuprgid=NULL
                            ,@JrtSchSetuprule='5'
                            ,@JrtSchSchedsteprule='0'
                            ,@JrtSchCrsbrkrule='0'
                            ,@JrtSchAllowReallocation='0'
                            ,@JrtSchSplitsize='0'
                            ,@JrtSchBatchDefinitionId=NULL
                            ,@JobRouteRowPointer=@myid
                            , @Infobar=@Infobar OUTPUT;
                            SELECT @Infobar as N'@Infobar';
                            """
                    cursor.execute(sql)
                    try:
                        # log error message if appropriate
                        logger.info(cursor.fetchone()[0])
                    except:
                        pass
            else:
                item_job = ItemMst.objects.filter(item=item.item_number).first().job
                wc = WcMst.objects.filter(wc=int(work_center_id)).first()
                JobrouteMst.objects.create(site_ref="SYTE",
                                           job=item_job,
                                           oper_num=sequence_no,
                                           wc=wc,
                                           setup_hrs_t=setup_hrs,
                                           run_hrs_t_lbr=run_hrs
                                           )
            sequence_no = sequence_no + 10
            logger.info(f"Op {operation.name} with item number {item.item_number} has been created")
