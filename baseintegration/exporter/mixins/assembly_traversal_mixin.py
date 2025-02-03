from decimal import Decimal

from paperless.objects.components import AssemblyMixin, BaseComponent


class AssemblyTraversalMixin:
    """
    This mixin provides functionality for using iterate_assembly_with_duplicates.
    It tracks data (like quantities) specific to the current component node, rather than the component as a whole which
    could have different quantities at different places in the assembly tree.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_assm_comp = None
        self.should_export_assemblies_with_duplicate_components = False

    def iterate_assembly(self, assembly: AssemblyMixin, should_export_assemblies_with_duplicate_components: bool):
        self.should_export_assemblies_with_duplicate_components = should_export_assemblies_with_duplicate_components
        iterate_assembly = assembly.iterate_assembly_with_duplicates if should_export_assemblies_with_duplicate_components else assembly.iterate_assembly
        for assm_comp in iterate_assembly():
            self.current_assm_comp = assm_comp
            yield assm_comp

    def get_innate_quantity(self, component: BaseComponent):
        return self.get_value_relative_to_current_node(component.innate_quantity)

    def get_value_relative_to_current_node(self, value):
        """
        Takes a value proportional to the current component's quantity.
        If should_export_assemblies_with_duplicate_components is disabled, it returns the given value as-is.
        If it is enabled, it decreases the value to be specific to the particular component instance (i.e. node).
        """
        if self.should_export_assemblies_with_duplicate_components and value is not None:
            node_quantity_per_root = self.current_assm_comp.quantity_per_root
            component_quantity_per_root = self.current_assm_comp.component.innate_quantity
            node_quantity_per_component_quantity = node_quantity_per_root / component_quantity_per_root
            if isinstance(value, Decimal):
                node_quantity_per_component_quantity = Decimal(node_quantity_per_component_quantity)
            return value * node_quantity_per_component_quantity
        else:
            return value

    def get_current_quantity_per_parent(self):
        return self.current_assm_comp.quantity_per_parent if self.current_assm_comp.parent else 1
