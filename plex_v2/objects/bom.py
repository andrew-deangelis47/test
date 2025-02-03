import attr
from attr.validators import optional, instance_of, deep_iterable
from plex_v2.objects.base import BaseObject, CreateMixin, RetrieveMixin, SearchMixin
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from plex_v2.exceptions import PlexException
from plex_v2.client import PlexClient
from baseintegration.integration.erp_error_message_converter import ConvertedErrorException


@attr.s(kw_only=True)
class BOMComponent(BaseObject, CreateMixin, RetrieveMixin, SearchMixin):
    _resource_name = 'engineering/v1-beta1/boms'

    @classmethod
    def get_serialization_schema(cls, mode):
        if mode == 'out':
            # TODO: To prevent all this boilerplate, FlatJSONMixin could be extended to provide
            #  an interface for adding "rules" or "overrides" to the default identity schema
            schema = {
                'partOperationId': lambda _, obj: obj.partOperationId,
                'componentId': lambda _, obj: obj.componentId
                if obj.componentId is not None else obj.componentPartId
                if obj.componentPartId is not None else obj.componentSupplyItemId,
                'componentPartId': lambda _, obj: obj.componentPartId,
                'quantity': '.',
                'scaling': '.',
                'validate': '.',
                'autoDeplete': '.',
                'transferHeat': '.',
                'note': '.',
                'depletionUnitOfMeasure': '.',
                'depletionConversionFactor': '.',
                'maximumQuantity': lambda _, obj: obj.maximumQuantity,
                'minimumQuantity': lambda _, obj: obj.minimumQuantity
            }

            return schema
        elif mode == 'in':
            base_schema = super().get_serialization_schema('in')
            base_schema['componentId'] = lambda _, json_dict: (json_dict['componentPartId']
                                                               if json_dict['componentPartId'] is not None
                                                               else json_dict['componentSupplyItemId'])
            return base_schema

    def create(self, in_place=True, resource_name_kwargs=None):
        try:
            super().create(in_place, resource_name_kwargs)
        except ConvertedErrorException as e:
            if "When creating a bom component the component part does not exist or is not valid." in str(e):
                component_id = self.componentId if self.componentId is not None else self.componentPartId if self.componentPartId is not None else self.componentSupplyItemId
                message = str(e) + f' Component id is "{component_id}". '
                raise ConvertedErrorException(message)

            raise e

    partOperationId = attr.ib(validator=instance_of(str))
    quantity = attr.ib(validator=instance_of((int, float)))
    componentId = attr.ib(validator=optional(instance_of(str)))

    partId = attr.ib(validator=optional(instance_of(str)), default=None)
    partNumber = attr.ib(validator=optional(instance_of(str)), default=None)
    partRevision = attr.ib(validator=optional(instance_of(str)), default=None)
    partNumberRevision = attr.ib(validator=optional(instance_of(str)), default=None)
    partOperationCode = attr.ib(validator=optional(instance_of(str)), default=None)
    partOperationNumber = attr.ib(validator=optional(instance_of(int)), default=None)
    partOperationType = attr.ib(validator=optional(instance_of(str)), default=None)
    componentPartId = attr.ib(validator=optional(instance_of(str)), default=None)
    componentPartNumber = attr.ib(validator=optional(instance_of(str)), default=None)
    componentPartRevision = attr.ib(validator=optional(instance_of(str)), default=None)
    componentPartNumberRevision = attr.ib(validator=optional(instance_of(str)), default=None)
    componentSupplyItemId = attr.ib(validator=optional(instance_of(str)), default=None)
    componentSupplyItemNumber = attr.ib(validator=optional(instance_of(str)), default=None)
    componentUnitOfMeasure = attr.ib(validator=optional(instance_of(str)), default=None)
    minimumQuantity = attr.ib(validator=optional(instance_of((int, float))), default=0)
    maximumQuantity = attr.ib(validator=optional(instance_of((int, float))), default=None)
    quantityFixed = attr.ib(validator=optional(instance_of(bool)), default=None)
    depletionUnitOfMeasure = attr.ib(validator=optional(instance_of(str)), default=None)
    depletionConversionFactor = attr.ib(validator=optional(instance_of((int, float))), default=None)
    sortOrder = attr.ib(validator=instance_of((int, float)), default=0)
    active = attr.ib(validator=instance_of(bool), default=True)
    position = attr.ib(validator=optional(instance_of(str)), default=None)
    side = attr.ib(validator=optional(instance_of(str)), default=None)
    scaling = attr.ib(validator=instance_of(bool), default=True)
    validate = attr.ib(validator=instance_of(bool), default=True)
    autoDeplete = attr.ib(validator=instance_of(bool), default=True)
    transferHeat = attr.ib(validator=instance_of(bool), default=True)
    note = attr.ib(validator=optional(instance_of(str)), default=None)

    @classmethod
    def get_with_filters(cls, **kwargs):
        url = 'engineering/v1-beta1/boms'
        filter = '?'
        for key, value in kwargs.items():
            filter += f'{key}={value}&'
        url = url + filter[:-1]

        try:
            client = PlexClient.get_instance()
            objs = client.request(url=url, method=PlexClient.METHODS.GET)
            objs = objs.json()
            formatted_objs = []
            for ob in objs:
                formatted_objs.append(cls.deserialize(ob))
        except PlexException as e:
            raise CancelledIntegrationActionException(e.message)

        return formatted_objs


@attr.s(kw_only=True)
class ComponentBOM(object):
    bom_components = attr.ib(
        validator=optional(deep_iterable(
            member_validator=instance_of(BOMComponent),
            iterable_validator=instance_of(list)
        )),
        default=None,
    )
    part_quantities = attr.ib(
        validator=optional(deep_iterable(
            member_validator=instance_of(tuple),
            iterable_validator=instance_of(list),
        )),
        default=None,
    )

    _is_created = False

    def add_part(self, part, quantity: int, op_id: int = None, depletion_units: str = None,
                 depletion_conversion_factor: float = None, ):
        if self.part_quantities is None:
            self.part_quantities = []

        self.part_quantities.append((part, quantity, op_id, depletion_units, depletion_conversion_factor))

    def create(self, part_operation_id):
        if self.bom_components is None:
            self.bom_components = []

        for part, quantity, op_id, depletion_units, depletion_conversion_factor in self.part_quantities:
            if op_id is None:
                op_id = part_operation_id
            if part.is_created():
                self.bom_components.append(part.as_bom_component(
                    operation_id=op_id,
                    quantity=quantity,
                    depletion_units=depletion_units,
                    depletion_conversion_factor=depletion_conversion_factor,
                    create=False,
                ))
            else:
                created_part = part.create()
                self.bom_components.append(created_part.as_bom_component(
                    operation_id=op_id,
                    quantity=quantity,
                    depletion_units=depletion_units,
                    depletion_conversion_factor=depletion_conversion_factor,
                    create=False,
                ))

        for bom_component in self.bom_components:
            bom_component.create()

        self._is_created = True

    def is_created(self):
        return self._is_created
