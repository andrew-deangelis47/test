import attr
from attr.validators import instance_of, optional
from plex_v2.objects.base import BaseObject, CreateMixin, RetrieveMixin, SearchMixin, RetrieveDataSourceMixin


@attr.s(init=True, kw_only=True)
class Supplier(BaseObject, RetrieveMixin, CreateMixin, SearchMixin):
    _resource_name = 'mdm/v1/suppliers'
    ORIGINAL_RESOURCE_NAME = 'mdm/v1/suppliers'

    id = attr.ib(validator=instance_of(str))
    code = attr.ib(validator=instance_of(str))
    type = attr.ib(validator=instance_of(str))
    name = attr.ib(validator=instance_of(str))
    modifiedDate = attr.ib(validator=optional(instance_of((str, None))), default=None)
    createdDate = attr.ib(validator=optional(instance_of((str, None))), default=None)
    category = attr.ib(validator=optional(instance_of((str, None))), default="")
    status = attr.ib(validator=instance_of(str))

    breakpointQuantity = attr.ib(validator=optional(instance_of((int, float))), default=None)

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


@attr.s(kw_only=True)
class SupplierGetDatasource(BaseObject, CreateMixin, RetrieveDataSourceMixin, SearchMixin):
    _resource_name = '5137/execute'

    Supplier_No = attr.ib(validator=optional(instance_of(int)))
    Supplier_Code = attr.ib(validator=optional(instance_of(str)))

    @classmethod
    def get(cls, supplier_code: str):
        body = {
            "Supplier_Code": supplier_code,
        }

        return cls.datasource_get(body)
