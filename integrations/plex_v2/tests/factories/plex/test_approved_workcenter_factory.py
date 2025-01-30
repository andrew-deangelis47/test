from plex_v2.factories.plex.approved_workcenter import ApprovedWorkCenterFactory
from plex_v2.configuration import PlexConfig
from unittest.mock import create_autospec
from plex_v2.utils.export import ExportUtils
from paperless.objects.orders import OrderOperation
from plex_v2.objects.part import Part
from plex_v2.objects.operations_mapping import OperationsMapping
from baseintegration.utils.operations import OperationUtils


class TestApprovedWorkcenterFactory:

    VALID_PP_OP_DEF_NAME = 'VALID_PP_OP_DEF_NAME'
    VALID_PART_NUMBER = 'VALID_PART_NUMBER'
    VALID_PART_REVISION = 'VALID_PART_REVISION'
    VALID_PLEX_OP_CODE = 'VALID_PLEX_OP_CODE'
    VALID_APPROVED_WORKCENTER_CODES = [
        'VALID_APPROVED_WORKCENTER_CODE_0',
        'VALID_APPROVED_WORKCENTER_CODE_1'
    ]

    VALID_PART_OP_INCREMENT_STEP = 10
    VALID_PP_OP_SETUP_TIME = 1.2
    VALID_PP_OP_RUN_TIME = 3.7
    VALID_CREW_SIZE = 2

    def setup_method(self):
        self.config = create_autospec(PlexConfig)
        self.config.part_operation_increment_step = self.VALID_PART_OP_INCREMENT_STEP
        self.config.crew_size_var = 'crew_size_var'
        self.config.default_approved_workcenter_crew_size = 1

        self.utils = create_autospec(spec=ExportUtils, name='utils')
        self.operation_utils = create_autospec(spec=OperationUtils, name='operation_utils')
        # only needed for crew size
        self.operation_utils.get_variable_value_from_operation.return_value = self.VALID_CREW_SIZE
        self.utils.operation_utils = self.operation_utils

        self.factory = ApprovedWorkCenterFactory(
            config=self.config,
            utils=self.utils
        )

        self.pp_operation = create_autospec(OrderOperation)
        self.pp_operation.operation_definition_name = self.VALID_PP_OP_DEF_NAME
        self.pp_operation.setup_time = self.VALID_PP_OP_SETUP_TIME
        self.pp_operation.runtime = self.VALID_PP_OP_RUN_TIME

        self.plex_part = create_autospec(Part)
        self.plex_part.number = self.VALID_PART_NUMBER
        self.plex_part.revision = self.VALID_PART_REVISION

        self.operations_mapping = create_autospec(OperationsMapping)
        self.operations_mapping.get_plex_op_code_from_pp_op_using_mapping_table.return_value = self.VALID_PLEX_OP_CODE
        self.operations_mapping.get_approved_workcenter_codes_by_pp_op.return_value = self.VALID_APPROVED_WORKCENTER_CODES

        self.op_no = 10

    def test_to_approved_workcenter_sets_active_to_true(self):
        self.utils.operation_utils = self.operation_utils

        approved_workcenter = self.factory.to_approved_workcenters(
            self.pp_operation,
            self.plex_part,
            self.operations_mapping,
            self.op_no
        )[0]

        assert approved_workcenter.Active

    def test_to_approved_workcenter_sets_op_code_based_on_op_mappings_object(self):
        approved_workcenter = self.factory.to_approved_workcenters(
            self.pp_operation,
            self.plex_part,
            self.operations_mapping,
            self.op_no
        )[0]

        assert approved_workcenter.Operation_Code == self.VALID_PLEX_OP_CODE

    def test_to_approved_workcenter_sets_op_no_to_what_is_passed_in(self):
        approved_workcenter = self.factory.to_approved_workcenters(
            self.pp_operation,
            self.plex_part,
            self.operations_mapping,
            self.op_no
        )[0]

        assert approved_workcenter.Operation_No == self.op_no

    def test_to_approved_workcenter_sets_part_no_to_plex_part_no(self):
        approved_workcenter = self.factory.to_approved_workcenters(
            self.pp_operation,
            self.plex_part,
            self.operations_mapping,
            self.op_no
        )[0]

        assert approved_workcenter.Part_No == self.plex_part.number

    def test_to_approved_workcenter_sets_rev_to_plex_part_rev(self):
        approved_workcenter = self.factory.to_approved_workcenters(
            self.pp_operation,
            self.plex_part,
            self.operations_mapping,
            self.op_no
        )[0]

        assert approved_workcenter.Revision == self.plex_part.revision

    def test_to_approved_workcenter_sets_first_sort_order_to_config_value(self):
        approved_workcenter = self.factory.to_approved_workcenters(
            self.pp_operation,
            self.plex_part,
            self.operations_mapping,
            self.op_no
        )[0]

        assert approved_workcenter.Sort_Order == self.config.part_operation_increment_step

    def test_to_approved_workcenter_sets_subsequent_sort_order_to_previous_sort_order_plus_config_value(self):
        approved_workcenters = self.factory.to_approved_workcenters(
            self.pp_operation,
            self.plex_part,
            self.operations_mapping,
            self.op_no
        )

        previous_sort_order = approved_workcenters[0].Sort_Order

        assert approved_workcenters[1].Sort_Order == previous_sort_order + self.config.part_operation_increment_step

    def test_to_approved_workcenter_sets_workcenter_code_based_on_op_mappings_object(self):
        approved_workcenters = self.factory.to_approved_workcenters(
            self.pp_operation,
            self.plex_part,
            self.operations_mapping,
            self.op_no
        )

        assert approved_workcenters[0].Workcenter_Code == self.VALID_APPROVED_WORKCENTER_CODES[0]
        assert approved_workcenters[1].Workcenter_Code == self.VALID_APPROVED_WORKCENTER_CODES[1]
