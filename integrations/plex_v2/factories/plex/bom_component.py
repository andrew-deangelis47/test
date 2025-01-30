from plex_v2.objects.bom import BOMComponent
from paperless.objects.orders import OrderComponent, OrderOperation
from plex_v2.objects.part import Part
from plex_v2.objects.routing import PartOperation
from plex_v2.factories.base import BaseFactory


class BomComponentFactory(BaseFactory):

    def to_bom_component(self, plex_parent_component: Part, plex_child_component: Part, pp_child_component: OrderComponent):
        first_plex_operation: PartOperation = self.utils.get_first_plex_part_op_for_plex_part(plex_parent_component)

        return BOMComponent(
            componentId=plex_child_component.id,
            componentPartId=plex_parent_component.id,
            partOperationId=first_plex_operation.id,
            quantity=pp_child_component.innate_quantity,
            maximumQuantity=pp_child_component.innate_quantity * 2
        )

    def to_material_bom_component(self, plex_parent_component: Part, material_operation: OrderOperation):
        plex_material: Part = self.utils.get_plex_material_from_material_op(material_operation)
        first_plex_operation: PartOperation = self.utils.get_first_plex_part_op_for_plex_part(plex_parent_component)
        quantity = self.utils.operation_utils.get_variable_value_from_operation(
            material_operation,
            self.config.material_quantity_var
        )

        return BOMComponent(
            componentId=plex_material.id,
            componentPartId=plex_parent_component.id,
            partOperationId=first_plex_operation.id,
            quantity=quantity,
            maximumQuantity=quantity * 2
        )
