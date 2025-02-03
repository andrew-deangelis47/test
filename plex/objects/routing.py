import attr
from plex.objects.base import BaseObject, CreateMixin, RetrieveMixin, SearchMixin
from attr.validators import instance_of, optional


@attr.s(kw_only=True)
class Operation(BaseObject, RetrieveMixin, SearchMixin):
    _resource_name = 'mdm/v1-beta1/operations'

    code = attr.ib(validator=instance_of(str))
    type = attr.ib(validator=instance_of(str))
    inventoryType = attr.ib(validator=instance_of(str))

    @classmethod
    def find_operations(
            cls,
            id: str = None,
            code: str = None,
            type: str = None,
            inventory_type: str = None,
    ):
        return cls.search(
            id=id,
            code=code,
            type=type,
            inventoryType=inventory_type,
        )


@attr.s(kw_only=True)
class PartOperation(BaseObject, CreateMixin, RetrieveMixin, SearchMixin):
    _resource_name = 'mdm/v1-beta1/part-operations'
    """
    Represents a step in the Process Routing of a part on Plex.
    """

    type = attr.ib(validator=optional(instance_of(str)))
    partId = attr.ib(validator=instance_of(str))
    operationId = attr.ib(validator=instance_of(str))

    operationNumber = attr.ib(validator=optional(instance_of(int)), default=None)
    active = attr.ib(validator=optional(instance_of(bool)), default=None)
    subOperation = attr.ib(validator=optional(instance_of(bool)), default=None)
    shippable = attr.ib(validator=optional(instance_of(bool)), default=None)
    multiple = attr.ib(validator=optional(instance_of(int)), default=None)
    netWeight = attr.ib(validator=instance_of(float), default=0.0)

    _operation = None

    @property
    def operation(self):
        if self._operation is not None:
            return self._operation
        else:
            op = Operation.get(self.operationId)
            self._operation = op
            return op

    @operation.setter
    def operation(self, value):
        self._operation = value

    @classmethod
    def find_part_operations(
            cls,
            part_id: str = None,
            operation_id: str = None,
            active: bool = True,
            sub_operation: bool = False,
            operation_number: str = None,
    ):
        return cls.search(
            partId=part_id,
            operationId=operation_id,
            active=active,
            subOperation=sub_operation,
            operationNumber=operation_number
        )
