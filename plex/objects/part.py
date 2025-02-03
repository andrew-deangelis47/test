import attr
from attr.validators import optional, instance_of
from plex.objects.base import BaseObject, CreateMixin, RetrieveMixin, SearchMixin, UpdateMixin

from plex.objects.bom import BOMComponent, ComponentBOM
from plex.exceptions import PlexException


@attr.s(init=True, kw_only=True)
class Part(BaseObject, RetrieveMixin, CreateMixin, SearchMixin, UpdateMixin):
    _resource_name = 'mdm/v1/parts'

    @classmethod
    def get_serialization_schema(cls, mode):
        if mode == 'out':
            base_schema = super().get_serialization_schema('out')
            del base_schema['id']
            del base_schema['weight']
            del base_schema['standard_job_qty']
            del base_schema['bom_substitution_allowed']
            del base_schema['bill_of_materials']
            del base_schema['is_new_rev_of_old_part']
            return base_schema
        else:
            base_schema = super().get_serialization_schema(mode)
            del base_schema['is_new_rev_of_old_part']
            return base_schema

    number = attr.ib(validator=instance_of(str))
    name = attr.ib(validator=optional(instance_of(str)), default=None)
    revision = attr.ib(validator=instance_of(str))
    type = attr.ib(validator=instance_of(str))
    group = attr.ib(validator=optional(instance_of(str)))
    productType = attr.ib(validator=optional(instance_of(str)))
    status = attr.ib(validator=instance_of(str))

    note = attr.ib(validator=optional(instance_of(str)), default=None)
    description = attr.ib(validator=optional(instance_of(str)), default=None)

    # Fixme: these are in the UI but not in the schema....
    weight = attr.ib(validator=optional(instance_of(int)), default=None)
    standard_job_qty = attr.ib(validator=optional(instance_of(int)), default=None)
    bom_substitution_allowed = attr.ib(validator=optional(instance_of(bool)), default=None)

    source = attr.ib(validator=optional(instance_of(str)), default=None)
    leadTimeDays = attr.ib(validator=instance_of((int, float)), default=0)
    buildingCode = attr.ib(validator=optional(instance_of(str)), default=None)
    createdById = attr.ib(validator=optional(instance_of(str)), default=None)
    createdDate = attr.ib(validator=optional(instance_of(str)), default=None)
    modifiedById = attr.ib(validator=optional(instance_of(str)), default=None)
    modifiedDate = attr.ib(validator=optional(instance_of(str)), default=None)

    bill_of_materials: ComponentBOM = attr.ib(
        validator=optional(instance_of(ComponentBOM)), default=None
    )

    is_new_rev_of_old_part: bool = attr.ib(
        validator=instance_of(bool), default=False
    )

    def is_new_rev(self):
        return self.is_new_rev_of_old_part

    def create(self, in_place=True, resource_name_kwargs=None):
        bom = self.bill_of_materials
        created_part = super().create(in_place=in_place, resource_name_kwargs=resource_name_kwargs)
        self.bill_of_materials = bom
        created_part.bill_of_materials = bom
        return created_part

    def create_component_bom(self, part_operation_id):
        if self.bill_of_materials is not None:
            self.bill_of_materials.create(part_operation_id)

    def add_child_component(self, part, quantity: int, op_id: int = None, depletion_units: str = None,
                            depletion_conversion_factor: float = None):
        if self.bill_of_materials is None:
            self.bill_of_materials = ComponentBOM()

        self.bill_of_materials.add_part(part=part,
                                        quantity=quantity,
                                        op_id=op_id,
                                        depletion_units=depletion_units,
                                        depletion_conversion_factor=depletion_conversion_factor)

    def as_bom_component(self, operation_id, quantity, depletion_units: str = None,
                         depletion_conversion_factor: float = None, create=True) -> BOMComponent:
        if create:
            component_id = self.id if self.is_created() else self.create().id
        elif self.is_created():
            component_id = self.id
        else:
            raise PlexException('This part is not created yet. It cannot be made into a BOM component')

        return BOMComponent(
            partOperationId=operation_id,
            quantity=quantity,
            componentId=component_id,
            depletionUnitOfMeasure=depletion_units,
            depletionConversionFactor=depletion_conversion_factor
        )

    @classmethod
    def find_part(cls, number: str = None, rev: str = None):
        """
        Search for an existing part that matches a given part_no or revision. Returns a list of all revisions of the
        part with index 0 being the exact match or None
        https://developers.plex.com/parts-api/apis/get/parts
        """
        return cls.search(number=number, rev=rev)
