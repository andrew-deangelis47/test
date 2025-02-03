from paperless.objects.orders import OrderComponent, Order, OrderItem, OrderOperation
from plex_v2.objects.part import Part
from plex_v2.factories.base import BaseFactory
from plex_v2.objects.part_upload_update_datasource import PartUploadUpdateDatasource
from typing import Union


class PlexPartFactory(BaseFactory):

    def to_plex_material_part(self, order: Order, material_operation: OrderOperation) -> Part:
        part_no = self.utils.operation_utils.get_variable_value_from_operation(
            material_operation,
            self.config.var_material_part_number
        )

        revision = self.utils.get_plex_revision_from_material_operation(material_operation)

        return Part(
            id=part_no,
            number=part_no,
            revision=revision[:8],
            description="",
            standard_job_qty=0,
            bom_substitution_allowed=True,
            type=self._get_type(material_operation),
            group=self._get_group(material_operation),
            productType=self._get_product_type(material_operation),
            status=self._get_part_status(material_operation),
            source=self._get_part_source(material_operation),
            note=self._get_note(order),
            is_new_rev_of_old_part=self.utils.is_new_rev_of_old_material_part(material_operation),
            buildingCode=self._get_building_code(material_operation),
            leadTimeDays=self._get_lead_time_days(material_operation),
            name=self._get_name(material_operation)
        )

    def to_plex_part(self, order: Order, order_item: OrderItem, order_component: OrderComponent) -> Part:
        """
        this is to create a part using the normal api, not datasources
        """

        part_number = self.utils.get_plex_part_number_of_pp_component(order_component)
        revision = self.utils.get_plex_part_revision_from_paperless_component(order_component)
        is_new_rev_of_old_part = self.utils.is_new_rev_of_old_part(order_component)

        return Part(
            id=part_number,
            number=part_number,
            revision=revision[:8],
            description=self._get_description(order_component),
            standard_job_qty=self._get_standard_job_qty(order_component),
            bom_substitution_allowed=self._get_bom_substitution_allowed(),
            type=self._get_type(order_component),
            group=self._get_group(order_component),
            productType=self._get_product_type(order_component),
            status=self._get_part_status(order_component),
            source=self._get_part_source(order_component),
            note=self._get_note(order),
            is_new_rev_of_old_part=is_new_rev_of_old_part,
            buildingCode=self._get_building_code(order_component),
            leadTimeDays=self._get_lead_time_days(order_item),
            name=self._get_name(order_component)
        )

    def to_plex_part_update_datasource(self, component: Union[OrderComponent, OrderOperation]):
        """
        for now the only property we will update here is Grade because it is a common ask
        for updating anything else use this function in a custom processor
        """
        part_no: str
        revision: str

        # 1) if material op get part num and rev from op
        if isinstance(component, OrderOperation):
            part_no = self.utils.operation_utils.get_variable_value_from_operation(
                component,
                self.config.var_material_part_number
            )

            revision = self.utils.get_plex_revision_from_material_operation(component)

        # 2) otherwise get it from the component
        else:
            part_no = self.utils.get_plex_part_number_of_pp_component(component)
            revision = self.utils.get_plex_part_revision_from_paperless_component(component)

        # 3) create shell object with minimum properties
        part_upload_datasource = PartUploadUpdateDatasource(
            Part_No=part_no,
            Revision=revision
        )

        # set grade if configured
        if self.config.should_export_part_grade:
            part_upload_datasource.Grade = self._get_part_grade(component)

        # set cycle frequency if configured
        if self.config.should_export_part_cycle_frequency:
            part_upload_datasource.Cycle_Frequency = self._get_cycle_frequency(component)

        # set building code if configured
        if self.config.should_export_part_building_code:
            part_upload_datasource.Building_Code = self._get_part_building_code(component)

        # set internal note if configured
        if self.config.should_export_internal_note:
            part_upload_datasource.Internal_Note = self._get_internal_note(component)

        # set weight if configured
        if self.config.should_export_part_weight:
            part_upload_datasource.Weight = self._get_part_weight(component)

        return part_upload_datasource

    def _get_name(self, order_component: Union[OrderComponent, OrderOperation]) -> str:
        return ''

    def _get_part_weight(self, order_component: Union[OrderComponent, OrderOperation]) -> str:
        # if material op get it right from the op
        if isinstance(order_component, OrderOperation):
            return self.utils.operation_utils.get_variable_value_from_operation(
                order_component,
                self.config.part_weight_var,
                self.config.default_part_weight_raw_material
            )

        # otherwise get it from the informational op
        default_part_weight = self.config.default_part_weight
        if order_component.is_hardware:
            default_part_weight = self.config.default_part_weight_purchased_component

        return self.utils.operation_utils.get_operation_variable_value_from_component(
            order_component,
            self.config.part_information_op_def_name,
            self.config.part_weight_var,
            default_part_weight
        )

    def _get_internal_note(self, order_component: Union[OrderComponent, OrderOperation]) -> str:
        # if material op get it right from the op
        if isinstance(order_component, OrderOperation):
            return self.utils.operation_utils.get_variable_value_from_operation(
                order_component,
                self.config.internal_note_var,
                self.config.default_internal_note_raw_material
            )

        # otherwise get it from the informational op
        default_internal_note = self.config.default_internal_note
        if order_component.is_hardware:
            default_internal_note = self.config.default_internal_note_purchased_component

        return self.utils.operation_utils.get_operation_variable_value_from_component(
            order_component,
            self.config.part_information_op_def_name,
            self.config.internal_note_var,
            default_internal_note
        )

    def _get_cycle_frequency(self, order_component: Union[OrderComponent, OrderOperation]) -> str:
        # if material op get it right from the op
        if isinstance(order_component, OrderOperation):
            return self.utils.operation_utils.get_variable_value_from_operation(
                order_component,
                self.config.part_cycle_frequency_var,
                self.config.default_part_cycle_frequency_raw_material
            )

        # otherwise get it from the informational op
        default_cycle_frequency = self.config.default_part_cycle_frequency
        if order_component.is_hardware:
            default_cycle_frequency = self.config.default_part_cycle_frequency_purchased_component

        return self.utils.operation_utils.get_operation_variable_value_from_component(
            order_component,
            self.config.part_information_op_def_name,
            self.config.part_cycle_frequency_var,
            default_cycle_frequency
        )

    def _get_part_grade(self, order_component: Union[OrderComponent, OrderOperation]) -> str:
        # if material op get it right from the op
        if isinstance(order_component, OrderOperation):
            return self.utils.operation_utils.get_variable_value_from_operation(
                order_component,
                self.config.part_grade_var,
                self.config.default_part_grade_raw_material
            )

        # otherwise get it from part info op
        default_part_grade = self.config.default_part_grade
        if order_component.is_hardware:
            default_part_grade = self.config.default_part_grade_purchased_component

        return self.utils.operation_utils.get_operation_variable_value_from_component(
            order_component,
            self.config.part_information_op_def_name,
            self.config.part_grade_var,
            default_part_grade
        )

    def _get_part_building_code(self, order_component: Union[OrderComponent, OrderOperation]) -> str:
        # if material op get it right from the op
        if isinstance(order_component, OrderOperation):
            return self.utils.operation_utils.get_variable_value_from_operation(
                order_component,
                self.config.part_building_code_var,
                self.config.default_part_building_code_raw_material
            )

        # determine default if it's not material based on if it's hardware
        default_part_building_code = self.config.default_part_building_code
        if order_component.is_hardware:
            default_part_building_code = self.config.default_part_building_code_purchased_component

        return self.utils.operation_utils.get_operation_variable_value_from_component(
            order_component,
            self.config.part_information_op_def_name,
            self.config.part_building_code_var,
            default_part_building_code
        )

    def _get_description(self, order_component: OrderComponent) -> str:
        if order_component.description is not None:
            return order_component.description[:99]

        return ''

    def _get_standard_job_qty(self, order_component: OrderComponent) -> int:
        return order_component.make_quantity

    def _get_bom_substitution_allowed(self) -> bool:
        return True

    def _get_type(self, order_component: Union[OrderComponent, OrderOperation]) -> str:
        # if it's a material op get it right from the op
        if isinstance(order_component, OrderOperation):
            return self.utils.operation_utils.get_variable_value_from_operation(
                order_component,
                self.config.part_type_var,
                self.config.default_raw_material_part_type
            )

        default_part_type = self.config.default_part_type
        # if it's a purchased component there is a different default
        if order_component.is_hardware:
            default_part_type = self.config.default_purchased_component_part_type

        return self.utils.operation_utils.get_operation_variable_value_from_component(
            order_component,
            self.config.part_information_op_def_name,
            self.config.part_type_var,
            default_part_type
        )

    def _get_group(self, order_component: Union[OrderComponent, OrderOperation]) -> str:
        # if material get it right from the op
        if isinstance(order_component, OrderOperation):
            return self.utils.operation_utils.get_variable_value_from_operation(
                order_component,
                self.config.part_group_var,
                self.config.default_part_group_raw_material
            )

        # otherwise get it from the informational op
        default_part_group = self.config.default_part_group
        if order_component.is_hardware:
            default_part_group = self.config.default_part_group_purchased_component

        return self.utils.operation_utils.get_operation_variable_value_from_component(
            order_component,
            self.config.part_information_op_def_name,
            self.config.part_group_var,
            default_part_group
        )

    def _get_product_type(self, order_component: Union[OrderComponent, OrderOperation]) -> str:
        # if it's a material op get it right from the op
        if isinstance(order_component, OrderOperation):
            return self.utils.operation_utils.get_variable_value_from_operation(
                order_component,
                self.config.part_product_type_var,
                self.config.default_product_type_raw_material
            )

        # otherwise get it from informational op
        default_product_type = self.config.default_product_type
        if order_component.is_hardware:
            default_product_type = self.config.default_product_type_purchased_components

        return self.utils.operation_utils.get_operation_variable_value_from_component(
            order_component,
            self.config.part_information_op_def_name,
            self.config.part_product_type_var,
            default_product_type
        )

    def _get_part_status(self, order_component: Union[OrderComponent, OrderOperation]) -> str:
        # if material op then get it right from the op
        if isinstance(order_component, OrderOperation):
            return self.utils.operation_utils.get_variable_value_from_operation(
                order_component,
                self.config.part_status_var,
                self.config.default_raw_material_part_status
            )

        # otherwise get it from Part Information op
        default_part_status = self.config.default_part_status
        # if this is a PC we have a different default part status
        if order_component.is_hardware:
            default_part_status = self.config.default_purchased_component_part_status

        return self.utils.operation_utils.get_operation_variable_value_from_component(
            order_component,
            self.config.part_information_op_def_name,
            self.config.part_status_var,
            default_part_status
        )

    def _get_part_source(self, order_component: Union[OrderComponent, OrderOperation]) -> str:
        # if material operation then get it right from the op
        if isinstance(order_component, OrderOperation):
            return self.utils.operation_utils.get_variable_value_from_operation(
                order_component,
                self.config.part_status_var,
                self.config.default_raw_material_part_source
            )

        # otherwise get it from Part Information op
        default_part_source = self.config.default_part_source
        if order_component.is_hardware:
            default_part_source = self.config.default_purchased_component_part_source

        return self.utils.operation_utils.get_operation_variable_value_from_component(
            order_component,
            self.config.part_information_op_def_name,
            self.config.part_source_var,
            default_part_source
        )

    def _get_note(self, order: Order):
        quote_number_with_revision = f'{order.quote_number}{f"-{order.quote_revision_number}" if order.quote_revision_number is not None else ""}'
        return f'Paperless Parts Quote: https://app.paperlessparts.com/quotes/edit/{quote_number_with_revision}'

    def _get_building_code(self, order_component: Union[OrderComponent, OrderOperation]) -> str:
        # if material get it from the material op
        if isinstance(order_component, OrderOperation):
            return self.utils.operation_utils.get_variable_value_from_operation(
                order_component,
                self.config.part_building_code_var,
                self.config.default_part_building_code
            )

        # otherwise use the Part Information op to get it
        self.utils.operation_utils.get_operation_variable_value_from_component(
            order_component,
            self.config.part_information_op_def_name,
            self.config.part_building_code_var,
            self.config.default_part_building_code
        )

    def _get_lead_time_days(self, order_item: Union[OrderItem, OrderOperation]) -> float:
        # if material then look for it in the operation
        if isinstance(order_item, OrderOperation):
            lead_time = self.utils.operation_utils.get_variable_value_from_operation(
                order_item,
                self.config.part_lead_time_var,
                self.config.default_raw_material_lead_time
            )
            return int(lead_time)

        if order_item.lead_days is not None:
            return order_item.lead_days

        return 0.0
