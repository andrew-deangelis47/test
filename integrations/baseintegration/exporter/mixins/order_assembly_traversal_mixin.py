from paperless.objects.orders import OrderComponent

from ....baseintegration.exporter.mixins.assembly_traversal_mixin import AssemblyTraversalMixin


class OrderAssemblyTraversalMixin(AssemblyTraversalMixin):
    """
    This mixin provides functionality for using iterate_assembly_with_duplicates.
    It tracks data (like quantities) specific to the current component node, rather than the component as a whole which
    could have different quantities at different places in the assembly tree.
    """

    def get_deliver_quantity(self, component: OrderComponent):
        return self.get_value_relative_to_current_node(component.deliver_quantity)

    def get_make_quantity(self, component: OrderComponent):
        return self.get_value_relative_to_current_node(component.make_quantity)
