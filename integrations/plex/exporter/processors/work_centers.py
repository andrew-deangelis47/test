from typing import Union

from paperless.objects.orders import OrderOperation

from baseintegration.datamigration import logger
from plex.exporter.processors.base import PlexProcessor
from plex.exporter.processors.utils import PlexUtils
from plex.objects.part import Part
from plex.objects.routing import PartOperation
from plex.objects.work_center import WorkCenterDataSource, ApprovedWorkcenter, Workcenter


class WorkCenterProcessor(PlexProcessor):

    def _process(self, op: OrderOperation, part_op: PartOperation, part: Part, operation_mapping: list) -> bool:
        url = self._exporter.erp_config.datasources_work_center
        if url == '' or url is None:
            return False

        op_code = PlexUtils.get_op_code(op, self._exporter.erp_config, operation_mapping)
        codes = op.get_variable_obj("Workcenter_Codes")
        crew = op.get_variable("Number Crew")

        if codes and codes.options:
            idx = 1
            if crew is None:
                crew = 1
            for code in codes.options:
                setup = op.setup_time if op.setup_time != 0. else 0.
                run = 1 / op.runtime if op.runtime != 0. else 0.
                WorkCenterDataSource(
                    Operation_Code=op_code,
                    Operation_No=part_op.operationNumber,
                    Part_No=part.number,
                    Revision=part.revision,
                    Workcenter_Code=code,
                    Sort_Order=idx,
                    Lead_Time=2,  # TODO: Remove this hard coding.
                    Setup_Time=setup,
                    Standard_Production_Rate=run,
                    Crew_Size=crew,
                    Note=op.notes if op.notes else '',
                    c_url=url
                ).create()
                idx += 1
        return True


class WorkCenterProcessorV2(PlexProcessor):

    def get_crew_size(self, op: OrderOperation) -> int:
        """
        Get crew size from the operation costing variables
        """
        # TODO: Do we want to support the other types here? Make a config param
        crew = op.get_variable(self._exporter.erp_config.costing_variable_work_center_crew_size)
        if crew is None:
            crew = 1
        return int(crew)

    def _process(self, op: OrderOperation, part_op: PartOperation, part: Part) -> Union[ApprovedWorkcenter, bool]:

        code = op.get_variable(self._exporter.erp_config.costing_variable_work_center_code)
        if code is None:
            logger.debug('No work center code found skipping')
            return False
        crew = self.get_crew_size(op)

        work_centers: Workcenter = Workcenter.find_workcenters(workcenterCode=code)
        if len(work_centers) == 0:
            logger.debug('Work center code could not be matched up')
            return False
        setup = op.setup_time if op.setup_time != 0. else 0.
        try:
            standard_production_rate = 1
            if op.runtime and float(op.runtime) > 0.:
                standard_production_rate = 1 / float(op.runtime)
            ap_work_center: ApprovedWorkcenter = ApprovedWorkcenter(
                workcenterId=work_centers[0].workcenterId,
                partOperationId=part_op.id,
                partId=part.id,
                crewSize=float(crew),
                setupCrewSize=float(crew),
                setupTime=float(setup),
                standardProductionRate=float(standard_production_rate),
                note=op.notes if op.notes else '',
                idealRate=0.0,
                targetRate=0.0
            ).create()
        except TypeError:
            logger.exception("A Parameter type mismatch may have occurred")
            return False
        return ap_work_center
