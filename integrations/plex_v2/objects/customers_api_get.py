import attr
from attr.validators import instance_of, optional
from plex_v2.objects.base import RetrieveDataSourceMixin, BaseObject


@attr.s(kw_only=True)
class CustomersApiGet(BaseObject, RetrieveDataSourceMixin):
    _resource_name = '230853/execute'

    # required for input
    Customer_Code = attr.ib(validator=optional(instance_of(str)))

    # output
    Resource_ID = attr.ib(validator=optional(instance_of(str)), default=None)
    Customer_Status = attr.ib(validator=optional(instance_of(str)), default=None)
    Active = attr.ib(validator=optional(instance_of(int)), default=None)
    Terms = attr.ib(validator=optional(instance_of(str)), default=None)
    Name = attr.ib(validator=optional(instance_of(str)), default=None)

    @classmethod
    def get(cls, customer_code: str):
        payload_dict: dict = {
            "Customer_Code": customer_code
        }

        return super().datasource_get(payload_dict)
