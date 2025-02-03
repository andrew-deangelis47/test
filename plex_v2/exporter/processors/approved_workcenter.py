from plex_v2.exporter.processors.base import PlexProcessor
from paperless.objects.orders import Order, OrderComponent, OrderItem, OrderOperation
from paperless.objects.components import AssemblyComponent
from typing import List
from plex_v2.utils.export import ExportUtils
from plex_v2.factories.plex.approved_workcenter import ApprovedWorkCenterFactory
from plex_v2.objects.work_center_export import ApprovedWorkcenterAddUpdate
from plex_v2.objects.part import Part
from plex_v2.objects.operations_mapping import OperationsMapping
from baseintegration.datamigration import logger


class ApprovedWorkcenterProcessor(PlexProcessor):
    """
    you can add the integration report here if you want
    it is kept out of the PlexV2 base integration because it is not clean
    """
    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'approved_workcenters'

    def _process(self, order: Order, utils: ExportUtils, factory: ApprovedWorkCenterFactory, operations_mapping: OperationsMapping):

        # iterate order items
        order_item: OrderItem
        for order_item in order.order_items:

            # iterate components
            paperless_component: AssemblyComponent
            components: List[AssemblyComponent] = order_item.iterate_assembly()
            for paperless_component in components:
                paperless_component: OrderComponent = paperless_component.component

                # get the corresponding plex part
                plex_part: Part = utils.get_plex_part_from_paperless_component(paperless_component)

                # get the existing PP operations for this component
                pp_part_ops: List[OrderOperation] = utils.get_non_ignored_operations_for_component(paperless_component)

                # iterate pp ops and create approved workcenters
                op_num = self.config.part_operation_increment_step
                pp_op: OrderOperation
                for pp_op in pp_part_ops:

                    # create approved workcenters for this op
                    approved_workcenters: List[ApprovedWorkcenterAddUpdate] = factory.to_approved_workcenters(
                        pp_operation=pp_op,
                        plex_part=plex_part,
                        operations_mapping=operations_mapping,
                        op_no=op_num
                    )

                    approved_workcenter: ApprovedWorkcenterAddUpdate
                    created_approved_workcenters: [ApprovedWorkcenterAddUpdate] = []
                    for approved_workcenter in approved_workcenters:
                        did_create = self._create_approved_workcenter_if_op_exists(approved_workcenter)
                        if did_create:
                            created_approved_workcenters.append(approved_workcenter)

                    op_num += self.config.part_operation_increment_step

                    self._log_created_approved_workcenters(created_approved_workcenters)

    def _log_created_approved_workcenters(self, created_approved_workcenters: List[ApprovedWorkcenterAddUpdate]) -> None:
        if len(created_approved_workcenters) > 0:
            operation_code: str = created_approved_workcenters[0].Operation_Code
            part_no: str = created_approved_workcenters[0].Part_No
            work_center_list = [x.Workcenter_Code for x in created_approved_workcenters]
            self._add_report_message(f'The following approved workcenters were created or already existed for part {part_no} on operation {operation_code}: {", ".join(work_center_list)}')

    def _create_approved_workcenter_if_op_exists(self, approved_workcenter: ApprovedWorkcenterAddUpdate):
        """
        handles the case where we try to create a duplicate routing step
        for instance, if the first export fails and we try again
        returns whether the op exsisted or not
        """
        try:
            approved_workcenter.create()
            return True
        except Exception as e:
            if 'Error when posting to data source "233466": Invalid Part Operation' in str(e):
                response_message = f'Attempted to add approved workcenter {approved_workcenter.Workcenter_Code} on op {approved_workcenter.Operation_Code} for part number {approved_workcenter.Part_No} which did not exist, skipping'
                logger.info(response_message)
                self._add_report_message(response_message)
                return False
