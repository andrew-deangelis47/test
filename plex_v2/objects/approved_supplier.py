import attr
from attr.validators import optional, instance_of
from plex_v2.objects.base import BaseObject, CreateMixin, RetrieveMixin, SearchMixin, RetrieveDataSourceMixin


@attr.s(kw_only=True)
class ApprovedSupplierGetDatasource(BaseObject, CreateMixin, RetrieveDataSourceMixin, SearchMixin):
    _resource_name = '8589/execute'

    Container_Reservation_Required = attr.ib(validator=optional(instance_of(bool)), default=None)
    Lead_Time = attr.ib(validator=optional(instance_of(float)), default=None)
    Note = attr.ib(validator=optional(instance_of(str)), default=None)
    Operation_Code = attr.ib(validator=optional(instance_of(str)), default=None)
    Operation_Key = attr.ib(validator=optional(instance_of(int)), default=None)
    Part_No = attr.ib(validator=optional(instance_of(str)), default=None)
    Price = attr.ib(validator=optional(instance_of(float)))
    Price_Conversion = attr.ib(validator=optional(instance_of(float)), default=None)
    Price_Unit = attr.ib(validator=optional(instance_of(str)))
    Revision = attr.ib(validator=optional(instance_of(str)), default=None)
    Sort_Order = attr.ib(validator=optional(instance_of(int)), default=None)
    Supplier_Code = attr.ib(validator=optional(instance_of(str)), default=None)
    Supplier_Code_Name = attr.ib(validator=optional(instance_of(str)), default=None)
    Supplier_No = attr.ib(validator=optional(instance_of(int)), default=None)
    Supplier_Part_No = attr.ib(validator=optional(instance_of(str)), default=None)
    UPC_Code = attr.ib(validator=optional(instance_of(str)), default=None)

    @classmethod
    def get(cls, part_key: int, part_op_key: int, supplier_no: int):
        body = {
            "Part_Key": part_key,
            "Part_Operation_Key": part_op_key,
            "Supplier_No": supplier_no
        }
        return super().datasource_get(body)


@attr.s(kw_only=True, repr=False)
class ApprovedSupplierPurchasing(BaseObject, CreateMixin, SearchMixin):
    _resource_name = 'purchasing/v1/approved-suppliers'
    id = attr.ib(validator=optional(instance_of(str)), default=None)
    partId = attr.ib(validator=optional(instance_of(str)), default=None)
    operationCode = attr.ib(validator=optional(instance_of(str)), default=None)
    supplierId = attr.ib(validator=optional(instance_of(str)), default=None)
    leadTime = attr.ib(validator=optional(instance_of(float)), default=None)
    supplierPartNumber = attr.ib(validator=optional(instance_of(str)), default=None)
    businessPercentage = attr.ib(validator=optional(instance_of(float)), default=None)
    transitTime = attr.ib(validator=optional(instance_of(float)), default=None)
    note = attr.ib(validator=optional(instance_of(str)), default=None)
    partOperationId = attr.ib(validator=optional(instance_of(str)), default=None)

    @classmethod
    def find_approved_suppliers(
            cls,
            partId=None,
            operationCode=None
    ):
        return cls.search(
            partId=partId,
            operationCode=operationCode,
            exclude_if_null=['supplierId', 'partId', 'partOperationId']
        )


@attr.s(kw_only=True, repr=False)
class ApprovedSupplier(BaseObject, CreateMixin, SearchMixin):
    _resource_name = 'production/v1-beta1/production-definitions/approved-suppliers'
    partId = attr.ib(validator=instance_of(str), default="00000000-0000-0000-0000-000000000000")
    supplierId = attr.ib(validator=instance_of(str), default="00000000-0000-0000-0000-000000000000")
    partOperationId = attr.ib(validator=instance_of(str), default="00000000-0000-0000-0000-000000000000")
    partNo = attr.ib(validator=optional(instance_of(str)), default=None)
    partRevision = attr.ib(validator=optional(instance_of(str)), default=None)
    partNoRevision = attr.ib(validator=optional(instance_of(str)), default=None)
    operationNo = attr.ib(validator=optional(instance_of(int)), default=None)
    operationCode = attr.ib(validator=optional(instance_of(str)), default=None)
    supplierCode = attr.ib(validator=optional(instance_of(str)), default=None)
    note = attr.ib(validator=optional(instance_of(str)), default=None)
    approvedSupplierId = attr.ib(validator=optional(instance_of(str)), default=None)

    @classmethod
    def get_serialization_schema(cls, mode):
        if mode == 'out':
            schema = super().get_serialization_schema('out')
            del schema['id']
            return schema
        elif mode == 'in':
            return super().get_serialization_schema('in')

    @classmethod
    def find_approved_suppliers(
            cls,
            supplierId=None,
            partId=None,
            partOperationId=None,
            operationCode=None,
            resource_name_kwargs=None,
    ):
        return cls.search(
            supplierId=supplierId,
            partId=partId,
            partOperationId=partOperationId,
            operationCode=operationCode,
            exclude_if_null=['supplierId', 'partId', 'partOperationId'],
            resource_name_kwargs=resource_name_kwargs,
        )


@attr.s(kw_only=True, repr=False)
class Supplier(BaseObject, RetrieveMixin, SearchMixin):
    _resource_name = 'mdm/v1/suppliers'
    id = attr.ib(validator=optional(instance_of(str)), default="00000000-0000-0000-0000-000000000000")
    code = attr.ib(validator=optional(instance_of(str)), default="")
    oldCode = attr.ib(validator=optional(instance_of(str)), default="")
    name = attr.ib(validator=optional(instance_of(str)), default="")
    language = attr.ib(validator=optional(instance_of(str)), default="")
    category = attr.ib(validator=optional(instance_of(str)), default="")
    status = attr.ib(validator=optional(instance_of(str)), default="")
    type = attr.ib(validator=optional(instance_of(str)), default="")
    parentSupplierId = attr.ib(validator=optional(instance_of(str)), default="00000000-0000-0000-0000-000000000000")
    webAddress = attr.ib(validator=optional(instance_of(str)), default="")
    contactNote = attr.ib(validator=optional(instance_of(str)), default="")
    note = attr.ib(validator=optional(instance_of(str)), default="")
    createdById = attr.ib(validator=optional(instance_of(str)), default="00000000-0000-0000-0000-000000000000")
    createdDate = attr.ib(validator=optional(instance_of(str)), default="")
    modifiedById = attr.ib(validator=optional(instance_of(str)), default="00000000-0000-0000-0000-000000000000")
    modifiedDate = attr.ib(validator=optional(instance_of(str)), default="")

    @classmethod
    def find_suppliers(
            cls,
            id=None,
            code=None,
            oldCode=None,
            name=None,
            language=None,
            category=None,
            status=None,
            type=None,
            parentSupplierId=None,
            createdById=None,
            createdDateBegin=None,
            createdDateEnd=None,
            modifiedById=None,
            modifiedDateBegin=None,
            modifiedDateEnd=None,
            resource_name_kwargs=None,
    ):
        return cls.search(
            id=id,
            code=code,
            oldCode=oldCode,
            name=name,
            language=language,
            category=category,
            status=status,
            type=type,
            parentSupplierId=parentSupplierId,
            createdById=createdById,
            createdDateBegin=createdDateBegin,
            createdDateEnd=createdDateEnd,
            modifiedById=modifiedById,
            modifiedDateBegin=modifiedDateBegin,
            modifiedDateEnd=modifiedDateEnd,
            exclude_if_null=['id',
                             'code',
                             'oldCode',
                             'name',
                             'language',
                             'category',
                             'status',
                             'type',
                             'parentSupplierId',
                             'createdById',
                             'createdDateBegin',
                             'createdDateEnd',
                             'modifiedById',
                             'modifiedDateBegin',
                             'modifiedDateEnd', ],
            resource_name_kwargs=resource_name_kwargs,
        )
