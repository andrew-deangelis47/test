import attr
from attr.validators import optional, instance_of
from plex_v2.objects.base import BaseObject, CreateMixin, RetrieveMixin, SearchMixin, RetrieveDataSourceMixin

from plex_v2.objects.bom import BOMComponent, ComponentBOM
from plex_v2.exceptions import PlexException


@attr.s(init=True, kw_only=True)
class Part(BaseObject, RetrieveMixin, CreateMixin, SearchMixin):
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

    id = attr.ib(validator=instance_of(str))
    number = attr.ib(validator=instance_of(str))
    name = attr.ib(validator=optional(instance_of(str)), default=None)
    revision = attr.ib(validator=instance_of(str))
    type = attr.ib(validator=instance_of(str), default=None)
    group = attr.ib(validator=optional(instance_of(str)), default=None)
    productType = attr.ib(validator=optional(instance_of(str)), default=None)
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

    def to_raw_material_custom_table_row(self) -> dict:
        return {
            "Number": self.number,
            "Description": self.description,
            "Part_Name": self.name,
            "Part_Type": self.type,
            "Part_Group": self.group,
            "Part_Source": self.source
        }

    @classmethod
    def get_resource_name(cls, type: str, **resource_name_kwargs):
        if type != 'search':
            return cls._resource_name

        resource_name = cls._resource_name
        filter = '?'
        for key, value in resource_name_kwargs.items():
            filter += f'{key}={value}&'
        resource_name += filter[:-1]

        return resource_name

    def is_new_rev(self):
        return self.is_new_rev_of_old_part

    def create(self, in_place=True, resource_name_kwargs=None):
        bom = self.bill_of_materials
        super().create(in_place, resource_name_kwargs)
        self.bill_of_materials = bom
        return self

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
    def find_part(cls, number: str, rev: str = None):
        """
        Search for an existing part that matches a given part_no or revision. Returns a list of all revisions of the
        part with index 0 being the exact match or None
        https://developers.plex.com/parts-api/apis/get/parts
        """
        if rev is None:
            return cls.search(number=number)
        return cls.search(number=number, revision=rev)


@attr.s(kw_only=True)
class PartInventorySummaryGetDataSource(BaseObject, CreateMixin, RetrieveDataSourceMixin, SearchMixin):
    _resource_name = '15664/execute'

    Part_Key = attr.ib(validator=optional(instance_of(int)))
    Part_No = attr.ib(validator=optional(instance_of(str)))
    Color = attr.ib(validator=optional(instance_of(str)))
    Order_Line_Quantity = attr.ib(validator=optional(instance_of(float)))
    Order_Line_Weight = attr.ib(validator=optional(instance_of(float)))
    FG_Quantity = attr.ib(validator=optional(instance_of(float)))
    FG_Weight = attr.ib(validator=optional(instance_of(float)))
    WIP_Quantity = attr.ib(validator=optional(instance_of(float)))
    WIP_Weight = attr.ib(validator=optional(instance_of(float)))
    Job_Count = attr.ib(validator=optional(instance_of(int)))
    Job_Quantity = attr.ib(validator=optional(instance_of(float)))
    Job_Weight = attr.ib(validator=optional(instance_of(float)))
    Job_Demand_Quantity = attr.ib(validator=optional(instance_of(float)))
    Job_Demand_Weight = attr.ib(validator=optional(instance_of(float)))
    Avail_FG_Weight = attr.ib(validator=optional(instance_of(float)))
    Avail_WIP = attr.ib(validator=optional(instance_of(float)))
    Avail_Job = attr.ib(validator=optional(instance_of(float)))

    def to_dict(self) -> dict:
        return {
            "Part_Key": self.Part_Key,
            "Part_No": self.Part_No,
            "Color": self.Color,
            "Order_Line_Quantity": self.Order_Line_Quantity,
            "Order_Line_Weight": self.Order_Line_Weight,
            "FG_Quantity": self.FG_Quantity,
            "FG_Weight": self.FG_Weight,
            "WIP_Quantity": self.WIP_Quantity,
            "WIP_Weight": self.WIP_Weight,
            "Job_Count": self.Job_Count,
            "Job_Quantity": self.Job_Quantity,
            "Job_Weight": self.Job_Weight,
            "Job_Demand_Quantity": self.Job_Demand_Quantity,
            "Job_Demand_Weight": self.Job_Demand_Weight,
            "Avail_FG_Weight": self.Avail_FG_Weight,
            "Avail_WIP": self.Avail_WIP,
            "Avail_Job": self.Avail_Job
        }

    @classmethod
    def get(cls, part_no: str):
        body = {
            "Part_No": part_no
        }

        return super().datasource_get(body)
