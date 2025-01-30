from plex_v2.configuration import PlexConfig
from unittest.mock import create_autospec
from plex_v2.utils.export import ExportUtils
from baseintegration.utils.operations import OperationUtils
from paperless.objects.orders import OrderComponent, OrderItem, OrderOperation
from unittest.mock import patch
from plex_v2.objects.part import Part
import os
import json
from paperless.objects.components import AssemblyComponent, ChildComponent
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from plex_v2.objects.customer import Customer, CustomerPart
from plex_v2.objects.base import SearchMixin
from paperless.objects.components import PurchasedComponent
from plex_v2.objects.routing import PartOperation
from plex_v2.objects.bom import BOMComponent


class TestExportUtils:

    VALID_PART_NO_0 = 'VALID_PART_NO_0'
    VALID_PART_NO_1 = 'VALID_PART_NO_1'
    VALID_REVISION_0 = 'VAL_REV0'
    VALID_REVISION_1 = 'VAL_REV1'
    VALID_PART_NAME = 'VALID_PART_NAME'
    VALID_PLEX_PART_ID_0 = 'VALID_PLEX_PART_ID_0'
    VALID_PLEX_PART_ID_1 = 'VALID_PLEX_PART_ID_1'
    VALID_PLEX_CUSTOMER_ID_0 = 'VALID_PLEX_CUSTOMER_ID_0'
    VALID_PLEX_CUSTOMER_ID_1 = 'VALID_PLEX_CUSTOMER_ID_1'
    VALID_CHILD_COMPONENT_ID_0 = 'VALID_CHILD_COMPONENT_ID_0'
    VALID_CHILD_COMPONENT_ID_1 = 'VALID_CHILD_COMPONENT_ID_1'
    VALID_ORDER_COMPONENT_ID_0 = 'VALID_ORDER_COMPONENT_ID_0'
    VALID_ORDER_COMPONENT_ID_1 = 'VALID_ORDER_COMPONENT_ID_1'
    VALID_MATERIAL_PART_NUM_VAR = 'VALID_MATERIAL_PART_NUM_VAR'
    VALID_MATERIAL_PART_REV_VAR = 'VALID_MATERIAL_PART_REV_VAR'

    def setup_method(self):
        self.config = create_autospec(PlexConfig)
        self.config.var_material_part_number = self.VALID_MATERIAL_PART_NUM_VAR
        self.config.var_material_part_revision = self.VALID_MATERIAL_PART_REV_VAR
        self.operation_utils = create_autospec(OperationUtils)
        self.utils = ExportUtils(self.config, self.operation_utils)

        with open(os.path.join(os.path.dirname(__file__), "../data/part.json"), 'r') as f:
            self.mock_part_in = json.load(f)

    def test_get_plex_material_from_material_op_returns_first_plex_part_returned_by_api(self):
        material_op = create_autospec(OrderOperation)

        plex_part_0 = create_autospec(Part)
        plex_part_1 = create_autospec(Part)

        with patch.object(Part, 'search', return_value=[plex_part_0, plex_part_1]):
            assert self.utils.get_plex_material_from_material_op(material_op) == plex_part_0

    def test_get_plex_material_from_material_op_raises_exception_if_no_material_found(self):
        material_op = create_autospec(OrderOperation)

        with patch.object(Part, 'search', return_value=[]):
            try:
                self.utils.get_plex_material_from_material_op(material_op)
                assert False
            except CancelledIntegrationActionException:
                assert True

    def test_does_bom_component_already_exist_returns_false_if_bom_component_id_does_not_match_child_part_id_when_material_op(self):
        plex_parent_comp = create_autospec(Part)
        plex_parent_comp.id = self.VALID_PLEX_PART_ID_0
        plex_parent_comp.number = self.VALID_PART_NO_0

        plex_child_component = create_autospec(Part)
        plex_child_component.id = self.VALID_CHILD_COMPONENT_ID_1
        plex_child_component.number = self.VALID_PART_NO_1

        existing_bom_component = create_autospec(BOMComponent)
        existing_bom_component.componentId = self.VALID_CHILD_COMPONENT_ID_0

        plex_material = create_autospec(Part)

        with patch.object(Part, 'search', return_value=plex_material):
            with patch.object(BOMComponent, 'get_with_filters', return_value=[existing_bom_component]):
                assert not self.utils.does_bom_component_already_exist(plex_parent_comp, plex_child_component)

    def test_does_bom_component_already_exist_returns_true_if_bom_component_id_matches_child_part_id_when_material_op(
            self):
        plex_parent_comp = create_autospec(Part)
        plex_parent_comp.id = self.VALID_PLEX_PART_ID_0
        plex_parent_comp.number = self.VALID_PART_NO_0

        plex_child_component = create_autospec(Part)
        plex_child_component.id = self.VALID_CHILD_COMPONENT_ID_0
        plex_child_component.number = self.VALID_PART_NO_1

        existing_bom_component = create_autospec(BOMComponent)
        existing_bom_component.componentId = self.VALID_CHILD_COMPONENT_ID_0

        plex_material = create_autospec(Part)

        with patch.object(Part, 'search', return_value=plex_material):
            with patch.object(BOMComponent, 'get_with_filters', return_value=[existing_bom_component]):
                assert self.utils.does_bom_component_already_exist(plex_parent_comp, plex_child_component)

    def test_does_bom_component_already_exist_returns_true_if_bom_component_id_matches_child_part_exists_when_not_material_op(self):
        plex_parent_comp = create_autospec(Part)
        plex_parent_comp.id = self.VALID_PLEX_PART_ID_0
        plex_parent_comp.number = self.VALID_PART_NO_0

        plex_child_component = create_autospec(Part)
        plex_child_component.id = self.VALID_CHILD_COMPONENT_ID_0
        plex_child_component.number = self.VALID_PART_NO_1

        existing_bom_component = create_autospec(BOMComponent)
        existing_bom_component.componentId = self.VALID_CHILD_COMPONENT_ID_0

        with patch.object(BOMComponent, 'get_with_filters', return_value=[existing_bom_component]):
            assert self.utils.does_bom_component_already_exist(plex_parent_comp, plex_child_component)

    def test_does_bom_component_already_exist_returns_false_if_bom_component_id_does_not_match_child_part_id_when_not_material_op(self):
        plex_parent_comp = create_autospec(Part)
        plex_parent_comp.id = self.VALID_PLEX_PART_ID_0
        plex_parent_comp.number = self.VALID_PART_NO_0

        plex_child_component = create_autospec(Part)
        plex_child_component.id = self.VALID_CHILD_COMPONENT_ID_1
        plex_child_component.number = self.VALID_PART_NO_1

        existing_bom_component = create_autospec(BOMComponent)
        existing_bom_component.componentId = self.VALID_CHILD_COMPONENT_ID_0

        with patch.object(BOMComponent, 'get_with_filters', return_value=[existing_bom_component]):
            assert not self.utils.does_bom_component_already_exist(plex_parent_comp, plex_child_component)

    def test_get_assembly_components_for_level_returns_all_components_for_specified_level(self):
        component_0 = create_autospec(AssemblyComponent)
        component_0.level = 0
        component_1 = create_autospec(AssemblyComponent)
        component_1.level = 0
        component_2 = create_autospec(AssemblyComponent)
        component_2.level = 0

        component_3 = create_autospec(AssemblyComponent)
        component_3.level = 1
        component_4 = create_autospec(AssemblyComponent)
        component_4.level = 1
        component_5 = create_autospec(AssemblyComponent)
        component_5.level = 1

        order_item = create_autospec(OrderItem)
        order_item.iterate_assembly.return_value = [component_0, component_1, component_2, component_3, component_4, component_5]

        components = self.utils.get_assembly_components_for_level(order_item, 1)
        assert components == [component_3, component_4, component_5]

    def test_get_bottom_level_of_order_item_bom_returns_max_level_of_assembly(self):
        component_0 = create_autospec(AssemblyComponent)
        component_0.level = 0
        component_1 = create_autospec(AssemblyComponent)
        component_1.level = 1
        component_2 = create_autospec(AssemblyComponent)
        component_2.level = 2

        order_item = create_autospec(OrderItem)
        order_item.iterate_assembly.return_value = [component_0, component_1, component_2]

        max_level = self.utils.get_bottom_level_of_order_item_bom(order_item)
        assert max_level == 2

    def test_get_first_plex_part_op_for_plex_part_returns_first_op_in_list_of_ops(self):
        part = create_autospec(Part)
        part.id = self.VALID_PLEX_PART_ID_0
        op_returned_0 = create_autospec(PartOperation)
        op_returned_1 = create_autospec(PartOperation)

        with patch.object(SearchMixin, 'search', return_value=[op_returned_0, op_returned_1]):
            assert self.utils.get_first_plex_part_op_for_plex_part(part) == op_returned_0

    def test_get_first_plex_part_op_for_plex_part_raises_exception_if_no_ops_found(self):
        part = create_autospec(Part)
        part.id = self.VALID_PLEX_PART_ID_0
        part.number = self.VALID_PART_NO_0

        with patch.object(SearchMixin, 'search', return_value=[]):
            try:
                self.utils.get_first_plex_part_op_for_plex_part(part)
                assert False
            except CancelledIntegrationActionException:
                assert True

    def test_does_material_exist_if_part_num_and_rev_match(self):
        def side_effect(mat_op, var_name, default=None):
            if var_name == self.VALID_MATERIAL_PART_REV_VAR:
                return self.VALID_REVISION_0
            elif var_name == self.VALID_MATERIAL_PART_NUM_VAR:
                return self.VALID_PART_NO_0

        material_op = create_autospec(OrderOperation)

        plex_part = create_autospec(spec=Part, name='plex_part')
        plex_part.number = self.VALID_PART_NO_0
        plex_part.revision = self.VALID_REVISION_0
        config = create_autospec(PlexConfig)
        config.var_material_part_number = self.VALID_MATERIAL_PART_NUM_VAR
        config.var_material_part_revision = self.VALID_MATERIAL_PART_REV_VAR
        op_utils = create_autospec(OperationUtils)  # need to force it to return a p3L value
        op_utils.get_variable_value_from_operation.side_effect = side_effect
        utils = ExportUtils(config, op_utils)

        # mock the return of the part search to return one mock part
        with patch.object(Part, 'search', return_value=[plex_part]):
            assert utils.does_material_exist(material_op)

    def test_get_plex_part_revision_from_paperless_component_returns_hardware_component_rev(self):
        component = create_autospec(OrderComponent)
        component.revision = self.VALID_REVISION_0
        component.is_hardware = True

        rev = self.utils.get_plex_part_revision_from_paperless_component(component)
        assert rev == self.VALID_REVISION_0

    def test_get_plex_part_revision_from_paperless_component_returns_hardware_rev_in_pc_lib_if_component_does_not_have_rev(self):
        pc = create_autospec(PurchasedComponent)
        pc.get_property.return_value = self.VALID_REVISION_0

        component = create_autospec(OrderComponent)
        component.revision = None
        component.is_hardware = True
        component.purchased_component = pc

        rev = self.utils.get_plex_part_revision_from_paperless_component(component)
        assert rev == self.VALID_REVISION_0

    def test_get_plex_part_revision_from_paperless_component_returns_blank_str_if_no_rev_with_hardware_component(self):
        pc = create_autospec(PurchasedComponent)
        pc.get_property.return_value = None

        component = create_autospec(OrderComponent)
        component.revision = None
        component.is_hardware = True
        component.purchased_component = pc

        rev = self.utils.get_plex_part_revision_from_paperless_component(component)
        assert rev == ""

    def test_get_plex_part_revision_from_paperless_component_returns_blank_str_if_rev_is_none(self):
        component = create_autospec(OrderComponent)
        component.revision = None
        component.is_hardware = False

        rev = self.utils.get_plex_part_revision_from_paperless_component(component)
        assert rev == ""

    def test_get_plex_part_revision_from_paperless_component_returns_rev_if_exists(self):
        component = create_autospec(OrderComponent)
        component.revision = self.VALID_REVISION_0
        component.is_hardware = False

        rev = self.utils.get_plex_part_revision_from_paperless_component(component)
        assert rev == self.VALID_REVISION_0

    def test_get_plex_part_number_of_pp_component_returns_part_num_if_not_none(self):
        component = create_autospec(OrderComponent)
        component.part_number = self.VALID_PART_NO_0

        part_num = self.utils.get_plex_part_number_of_pp_component(component)
        assert part_num == self.VALID_PART_NO_0

    def test_get_plex_part_number_of_pp_component_returns_trimmed_part_name_if_part_num_is_none(self):
        component = create_autospec(OrderComponent)
        component.part_number = None
        component.part_name = self.VALID_PART_NAME

        part_num = self.utils.get_plex_part_number_of_pp_component(component)
        assert part_num == self.VALID_PART_NAME

    def test_is_new_rev_of_old_part_returns_false_if_part_num_and_rev_match(self):
        component = create_autospec(spec=OrderComponent, name='component')
        component.part_number = self.VALID_PART_NO_0
        component.revision = self.VALID_REVISION_0
        component.is_hardware = False

        plex_part = create_autospec(spec=Part, name='plex_part')
        plex_part.number = self.VALID_PART_NO_0
        plex_part.revision = self.VALID_REVISION_0

        # mock the return of the part search to return one mock part
        with patch.object(Part, 'search', return_value=[plex_part]):
            assert not self.utils.is_new_rev_of_old_part(component)

    def test_is_new_rev_of_old_part_raises_exception_if_no_part_num_on_component(self):
        component = create_autospec(spec=OrderComponent, name='component')
        component.part_number = None
        component.part_name = self.VALID_PART_NAME
        component.revision = self.VALID_REVISION_0
        component.is_hardware = False

        plex_part = create_autospec(spec=Part, name='plex_part')
        plex_part.number = self.VALID_PART_NO_0
        plex_part.revision = self.VALID_REVISION_0

        # mock the return of the part search to return one mock part
        with patch.object(Part, 'search', return_value=[plex_part]):
            try:
                self.utils.is_new_rev_of_old_part(component)
                assert False
            except CancelledIntegrationActionException:
                assert True

    def test_is_new_rev_of_old_part_returns_false_if_part_num_does_not_match(self):
        component = create_autospec(spec=OrderComponent, name='component')
        component.part_number = self.VALID_PART_NO_0
        component.revision = self.VALID_REVISION_0
        component.is_hardware = False

        plex_part = create_autospec(spec=Part, name='plex_part')
        plex_part.number = self.VALID_PART_NO_1
        plex_part.revision = self.VALID_REVISION_0

        # mock the return of the part search to return one mock part
        with patch.object(Part, 'search', return_value=[plex_part]):
            assert not self.utils.is_new_rev_of_old_part(component)

    def test_is_new_rev_of_old_part_returns_false_if_rev_matches(self):
        component = create_autospec(OrderComponent)
        component.part_number = self.VALID_PART_NO_0
        component.revision = self.VALID_REVISION_0
        component.is_hardware = False

        plex_part = create_autospec(Part)
        plex_part.number = self.VALID_PART_NO_0
        plex_part.revision = self.VALID_REVISION_0

        # mock the return of the part search to return one mock part
        with patch.object(Part, 'search', return_value=[plex_part]):
            assert not self.utils.is_new_rev_of_old_part(component)

    def test_is_new_rev_of_old_part_returns_true_if_part_num_matches_and_rev_does_not(self):
        component = create_autospec(OrderComponent)
        component.part_number = self.VALID_PART_NO_0
        component.revision = self.VALID_REVISION_0
        component.is_hardware = False

        plex_part = create_autospec(Part)
        plex_part.number = self.VALID_PART_NO_0
        plex_part.revision = self.VALID_REVISION_1

        # mock the return of the part search to return one mock part
        with patch.object(Part, 'search', return_value=[plex_part]):
            assert self.utils.is_new_rev_of_old_part(component)

    def test_is_new_rev_of_old_material_part_returns_false_if_part_num_matches_and_rev_matches(self):
        def side_effect(mat_op, var, default=None):
            if var == self.VALID_MATERIAL_PART_NUM_VAR:
                return self.VALID_PART_NO_0
            elif var == self.VALID_MATERIAL_PART_REV_VAR:
                return self.VALID_REVISION_0

        material_operation = create_autospec(OrderOperation)
        plex_part = create_autospec(Part)
        plex_part.number = self.VALID_PART_NO_0
        plex_part.revision = self.VALID_REVISION_0
        config = create_autospec(PlexConfig)
        config.var_material_part_number = self.VALID_MATERIAL_PART_NUM_VAR
        config.var_material_part_revision = self.VALID_MATERIAL_PART_REV_VAR
        op_utils = create_autospec(OperationUtils)  # need to force it to return a p3L value
        op_utils.get_variable_value_from_operation.side_effect = side_effect
        utils = ExportUtils(config, op_utils)

        # mock the return of the part search to return one mock part
        with patch.object(SearchMixin, 'search', return_value=[plex_part]):
            assert not utils.is_new_rev_of_old_material_part(material_operation)

    def test_is_new_rev_of_old_material_part_returns_true_if_part_num_matches_and_rev_does_not(self):
        def side_effect(mat_op, var, default=None):
            if var == self.VALID_MATERIAL_PART_NUM_VAR:
                return self.VALID_PART_NO_0
            elif var == self.VALID_MATERIAL_PART_REV_VAR:
                return self.VALID_REVISION_0

        material_operation = create_autospec(OrderOperation)
        plex_part = create_autospec(Part)
        plex_part.number = self.VALID_PART_NO_0
        plex_part.revision = self.VALID_REVISION_1
        config = create_autospec(PlexConfig)
        config.var_material_part_number = self.VALID_MATERIAL_PART_NUM_VAR
        config.var_material_part_revision = self.VALID_MATERIAL_PART_REV_VAR
        op_utils = create_autospec(OperationUtils)  # need to force it to return a p3L value
        op_utils.get_variable_value_from_operation.side_effect = side_effect
        utils = ExportUtils(config, op_utils)

        # mock the return of the part search to return one mock part
        with patch.object(SearchMixin, 'search', return_value=[plex_part]):
            assert utils.is_new_rev_of_old_material_part(material_operation)

    def test_does_material_exist_returns_true_if_part_no_and_rev_match(self):
        def side_effect(mat_op, var, default=None):
            if var == self.VALID_MATERIAL_PART_NUM_VAR:
                return self.VALID_PART_NO_0
            elif var == self.VALID_MATERIAL_PART_REV_VAR:
                return self.VALID_REVISION_0

        material_operation = create_autospec(OrderOperation)
        plex_part = create_autospec(Part)
        plex_part.number = self.VALID_PART_NO_0
        plex_part.revision = self.VALID_REVISION_0
        config = create_autospec(PlexConfig)
        config.var_material_part_number = self.VALID_MATERIAL_PART_NUM_VAR
        config.var_material_part_revision = self.VALID_MATERIAL_PART_REV_VAR
        op_utils = create_autospec(OperationUtils)  # need to force it to return a p3L value
        op_utils.get_variable_value_from_operation.side_effect = side_effect
        utils = ExportUtils(config, op_utils)

        # mock the return of the part search to return one mock part
        with patch.object(Part, 'search', return_value=[plex_part]):
            exists, existing_part = utils.does_material_exist(material_operation)
            assert exists
            assert existing_part is not None

    def test_does_material_exist_returns_false_if_part_no_does_not_match(self):
        def side_effect(mat_op, var, default=None):
            if var == self.VALID_MATERIAL_PART_NUM_VAR:
                return self.VALID_PART_NO_0
            elif var == self.VALID_MATERIAL_PART_REV_VAR:
                return self.VALID_REVISION_0

        material_operation = create_autospec(OrderOperation)
        config = create_autospec(PlexConfig)
        config.var_material_part_number = self.VALID_MATERIAL_PART_NUM_VAR
        config.var_material_part_revision = self.VALID_MATERIAL_PART_REV_VAR
        op_utils = create_autospec(OperationUtils)  # need to force it to return a p3L value
        op_utils.get_variable_value_from_operation.side_effect = side_effect
        utils = ExportUtils(config, op_utils)

        # mock the return of the part search to return one mock part
        with patch.object(Part, 'search', return_value=[]):
            exists, existing_part = utils.does_material_exist(material_operation)
            assert not exists
            assert existing_part is None

    def test_does_material_exist_returns_false_if_rev_does_not_match(self):
        def side_effect(mat_op, var, default=None):
            if var == self.VALID_MATERIAL_PART_NUM_VAR:
                return self.VALID_PART_NO_0
            elif var == self.VALID_MATERIAL_PART_REV_VAR:
                return self.VALID_REVISION_0

        material_operation = create_autospec(OrderOperation)
        plex_part = create_autospec(Part)
        plex_part.number = self.VALID_PART_NO_0
        plex_part.revision = self.VALID_REVISION_1
        config = create_autospec(PlexConfig)
        config.var_material_part_number = self.VALID_MATERIAL_PART_NUM_VAR
        config.var_material_part_revision = self.VALID_MATERIAL_PART_REV_VAR
        op_utils = create_autospec(OperationUtils)  # need to force it to return a p3L value
        op_utils.get_variable_value_from_operation.side_effect = side_effect
        utils = ExportUtils(config, op_utils)

        # mock the return of the part search to return one mock part
        with patch.object(Part, 'search', return_value=[plex_part]):
            exists, existing_part = utils.does_material_exist(material_operation)
            assert not exists
            assert existing_part is None

    def test_get_top_level_part_from_order_item_returns_root_component(self):
        order_item = create_autospec(OrderItem)

        top_level_assembly_component = create_autospec(AssemblyComponent)
        top_level_component = create_autospec(OrderComponent)
        top_level_component.is_root_component = True
        top_level_assembly_component.component = top_level_component

        non_top_level_assembly_component = create_autospec(AssemblyComponent)
        non_top_level_component = create_autospec(OrderComponent)
        non_top_level_component.is_root_component = False
        non_top_level_component.component = non_top_level_component

        order_item.iterate_assembly.return_value = [
            non_top_level_assembly_component,
            top_level_assembly_component
        ]

        result_component = self.utils.get_top_level_part_from_order_item(order_item)
        assert result_component.is_root_component

    def test_get_top_level_part_from_order_item_raises_exception_if_not_found(self):
        order_item = create_autospec(OrderItem)

        assem_component_0 = create_autospec(AssemblyComponent)
        order_component_0 = create_autospec(OrderComponent)
        order_component_0.is_root_component = False
        assem_component_0.component = order_component_0

        assem_component_1 = create_autospec(AssemblyComponent)
        order_component_1 = create_autospec(OrderComponent)
        order_component_1.is_root_component = False
        assem_component_1.component = order_component_1

        order_item.iterate_assembly.return_value = [
            assem_component_1,
            assem_component_0
        ]

        try:
            self.utils.get_top_level_part_from_order_item(order_item)
            assert False
        except CancelledIntegrationActionException as e:
            assert str(e) == 'Could not find top level part for order item'

    def test_does_part_exist_returns_false_if_no_plex_part_exists_with_components_part_no(self):
        component = create_autospec(OrderItem)
        component.part_number = self.VALID_PART_NO_0
        component.revision = self.VALID_REVISION_0
        component.is_hardware = False

        # mock the return of the part search to return one mock part
        with patch.object(Part, 'search', return_value=[]):
            does_exist, existing_part = self.utils.does_part_exist(component)
            assert not does_exist

    def test_does_part_exist_returns_false_if_no_plex_part_exists_with_components_part_no_and_revision(self):
        component = create_autospec(OrderItem)
        component.part_number = self.VALID_PART_NO_0
        component.revision = self.VALID_REVISION_0
        component.is_hardware = False

        returned_part = create_autospec(Part)
        returned_part.revision = self.VALID_REVISION_1

        # mock the return of the part search to return one mock part
        with patch.object(Part, 'search', return_value=[returned_part]):
            does_exist, existing_part = self.utils.does_part_exist(component)
            assert not does_exist

    def test_get_plex_part_revision_from_paperless_component_returns_blank_if_revision_is_none(self):
        component = create_autospec(OrderItem)
        component.revision = None
        component.is_hardware = False

        revision = self.utils.get_plex_part_revision_from_paperless_component(component)
        assert revision == ""

    def test_get_plex_part_revision_from_paperless_component_returns_revision_if_revision_is_not_none(self):
        component = create_autospec(OrderItem)
        component.revision = self.VALID_REVISION_0
        component.is_hardware = False

        revision = self.utils.get_plex_part_revision_from_paperless_component(component)
        assert revision == self.VALID_REVISION_0

    def test_get_plex_part_from_paperless_component_returns_part_with_matching_number_and_rev(self):
        component = create_autospec(OrderItem)
        component.part_number = self.VALID_PART_NO_0
        component.revision = self.VALID_REVISION_0
        component.is_hardware = False

        returned_part = create_autospec(Part)
        returned_part.number = self.VALID_PART_NO_0
        returned_part.revision = self.VALID_REVISION_0

        # mock the return of the part search to return one mock part
        with patch.object(Part, 'search', return_value=[returned_part]):
            part = self.utils.get_plex_part_from_paperless_component(component)
            assert part.number == component.part_number
            assert part.revision == component.revision

    def test_get_plex_part_from_paperless_component_raises_exception_if_part_not_found(self):
        component = create_autospec(OrderItem)
        component.part_number = self.VALID_PART_NO_0
        component.revision = self.VALID_REVISION_0
        component.is_hardware = False

        # mock the return of the part search to return one mock part
        with patch.object(Part, 'search', return_value=[]):
            try:
                self.utils.get_plex_part_from_paperless_component(component)
                assert False
            except CancelledIntegrationActionException as e:
                assert str(e) == f'Part not found in Plex: number="{component.part_number}", revision={component.revision}'

    def test_get_customer_part_if_exists_returns_customer_part_if_matches_on_part_and_customer(self):
        plex_part = create_autospec(Part)
        plex_part.number = self.VALID_PART_NO_0
        plex_part.id = self.VALID_PLEX_PART_ID_0

        customer = create_autospec(Customer)
        customer.id = self.VALID_PLEX_CUSTOMER_ID_0

        customer_part = create_autospec(CustomerPart)
        customer_part.number = self.VALID_PART_NO_0
        customer_part.partId = self.VALID_PLEX_PART_ID_0
        customer_part.customerId = self.VALID_PLEX_CUSTOMER_ID_0

        # mock the return on the customer part search
        with patch.object(CustomerPart, 'find_customer_parts', return_value=[customer_part]):
            customer_part = self.utils.get_customer_part_if_exists(plex_part, customer)
            assert customer_part is not None

    def test_get_customer_part_if_exists_returns_none_if_no_results_from_api(self):
        plex_part = create_autospec(Part)
        plex_part.number = self.VALID_PART_NO_0
        plex_part.id = self.VALID_PLEX_PART_ID_0

        customer = create_autospec(Customer)
        customer.id = self.VALID_PLEX_CUSTOMER_ID_0

        # mock the return on the customer part search
        with patch.object(CustomerPart, 'find_customer_parts', return_value=[]):
            customer_part = self.utils.get_customer_part_if_exists(plex_part, customer)
            assert customer_part is None

    def test_get_customer_part_if_exists_returns_none_if_part_num_does_not_match(self):
        plex_part = create_autospec(Part)
        plex_part.number = self.VALID_PART_NO_0
        plex_part.id = self.VALID_PLEX_PART_ID_0

        customer = create_autospec(Customer)
        customer.id = self.VALID_PLEX_CUSTOMER_ID_0

        customer_part = create_autospec(CustomerPart)
        customer_part.number = self.VALID_PART_NO_1
        customer_part.partId = self.VALID_PLEX_PART_ID_0
        customer_part.customerId = self.VALID_PLEX_CUSTOMER_ID_0

        # mock the return on the customer part search
        with patch.object(CustomerPart, 'find_customer_parts', return_value=[customer_part]):
            customer_part = self.utils.get_customer_part_if_exists(plex_part, customer)
            assert customer_part is None

    def test_get_customer_part_if_exists_returns_none_if_part_id_does_not_match(self):
        plex_part = create_autospec(Part)
        plex_part.number = self.VALID_PART_NO_0
        plex_part.id = self.VALID_PLEX_PART_ID_0

        customer = create_autospec(Customer)
        customer.id = self.VALID_PLEX_CUSTOMER_ID_0

        customer_part = create_autospec(CustomerPart)
        customer_part.number = self.VALID_PART_NO_0
        customer_part.partId = self.VALID_PLEX_PART_ID_1
        customer_part.customerId = self.VALID_PLEX_CUSTOMER_ID_0

        # mock the return on the customer part search
        with patch.object(CustomerPart, 'find_customer_parts', return_value=[customer_part]):
            customer_part = self.utils.get_customer_part_if_exists(plex_part, customer)
            assert customer_part is None

    def test_get_customer_part_if_exists_returns_none_if_customer_id_does_not_match(self):
        plex_part = create_autospec(Part)
        plex_part.number = self.VALID_PART_NO_0
        plex_part.id = self.VALID_PLEX_PART_ID_0

        customer = create_autospec(Customer)
        customer.id = self.VALID_PLEX_CUSTOMER_ID_0

        customer_part = create_autospec(CustomerPart)
        customer_part.number = self.VALID_PART_NO_0
        customer_part.partId = self.VALID_PLEX_PART_ID_0
        customer_part.customerId = self.VALID_PLEX_CUSTOMER_ID_1

        # mock the return on the customer part search
        with patch.object(CustomerPart, 'find_customer_parts', return_value=[customer_part]):
            customer_part = self.utils.get_customer_part_if_exists(plex_part, customer)
            assert customer_part is None

    def test_get_sub_components_of_order_component_returns_all_sub_components(self):
        order_component_0 = create_autospec(spec=OrderComponent, name='order_component_0')
        order_component_0.id = self.VALID_ORDER_COMPONENT_ID_0
        order_component_0.child_id = self.VALID_ORDER_COMPONENT_ID_0
        order_component_1 = create_autospec(spec=OrderComponent, name='order_component_1')
        order_component_1.id = self.VALID_ORDER_COMPONENT_ID_1
        order_component_1.child_id = self.VALID_ORDER_COMPONENT_ID_1

        assembly_component_0 = create_autospec(spec=AssemblyComponent, name='assembly_component_0')
        assembly_component_0.component = order_component_0
        assembly_component_1 = create_autospec(spec=AssemblyComponent, name='assembly_component_1')
        assembly_component_1.component = order_component_0

        order_item = create_autospec(spec=OrderItem, name='order_item')
        order_item.iterate_assembly.return_value = [assembly_component_0, assembly_component_1]

        order_component_2 = create_autospec(spec=OrderComponent, name='order_component_2')
        order_component_2.components = [order_component_0, order_component_1]
        order_component_2.children = [order_component_0, order_component_1]

        child_comp_0 = create_autospec(spec=ChildComponent, name='child_comp_0')
        child_comp_0.child_id = self.VALID_CHILD_COMPONENT_ID_0
        child_comp_1 = create_autospec(spec=ChildComponent, name='child_comp_1')
        child_comp_1.child_id = self.VALID_CHILD_COMPONENT_ID_1

        order_item.children = [child_comp_0, child_comp_1]

        sub_comps = self.utils.get_sub_components_of_order_component(order_component_2, order_item)
        assert len(sub_comps) == 2
