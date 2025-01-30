import json

import attr
from attr.validators import instance_of, optional
from plex.objects.base import BaseObject, CreateMixin, RetrieveMixin, SearchMixin
from baseintegration.datamigration import logger
from client import PlexClient


@attr.s(kw_only=True)
class WorkCenterDataSource(BaseObject, CreateMixin):
    Operation_Code = attr.ib(validator=optional(instance_of(str)), default='')
    Operation_No = attr.ib(validator=optional(instance_of(int)), default=10)
    Part_No = attr.ib(validator=optional(instance_of(str)), default='')
    Revision = attr.ib(validator=optional(instance_of(str)), default='')
    Workcenter_Code = attr.ib(validator=optional(instance_of(str)), default='')
    Sort_Order = attr.ib(validator=optional(instance_of(int)), default=1)
    Lead_Time = attr.ib(validator=instance_of((int, float)), default=1)
    Setup_Time = attr.ib(validator=instance_of((int, float)), default=1)
    Standard_Production_Rate = attr.ib(validator=optional(instance_of((int, float))), default=0.0)
    Crew_Size = attr.ib(validator=instance_of((int, float)), default=0.0)
    Note = attr.ib(validator=optional(instance_of(str)), default='')
    c_url = attr.ib(validator=optional(instance_of(str)), default='')

    @classmethod
    def get_serialization_schema(cls, mode):
        raise NotImplementedError

    @classmethod
    def get_resource_name(cls, action, instance=None, **kwargs):
        raise NotImplementedError

    def create(self):
        body = {
            "inputs": {
                "Active": True,
                "Operation_Code": self.Operation_Code,
                "Operation_No": self.Operation_No,
                "Part_No": self.Part_No,
                "Revision": self.Revision,
                "Workcenter_Code": self.Workcenter_Code,
                "Sort_Order": self.Sort_Order,
                "Lead_Time": self.Lead_Time,
                "Setup_Time": self.Setup_Time,
                "Standard_Production_Rate": self.Standard_Production_Rate,
                "Crew_Size": self.Crew_Size,
                "Note": self.Note,
            }
        }
        client = self._get_client()
        resp = client.request(url=self.c_url, method=PlexClient.METHODS.POST, data=json.dumps(body), datasource=True)
        logger.debug(resp)
        return True


@attr.s(kw_only=True, repr=False)
class ApprovedWorkcenter(BaseObject, CreateMixin, SearchMixin):
    _resource_name = 'production/v1-beta1/production-definitions/approved-workcenters'
    workcenterId = attr.ib(validator=instance_of(str), default="00000000-0000-0000-0000-000000000000")
    partId = attr.ib(validator=instance_of(str), default="00000000-0000-0000-0000-000000000000")
    partOperationId = attr.ib(validator=instance_of(str), default="00000000-0000-0000-0000-000000000000")
    workcenterCode = attr.ib(validator=optional(instance_of(str)), default=None)
    workcenterName = attr.ib(validator=optional(instance_of(str)), default=None)
    partNo = attr.ib(validator=optional(instance_of(str)), default=None)
    partRevision = attr.ib(validator=optional(instance_of(str)), default=None)
    partNoRevision = attr.ib(validator=optional(instance_of(str)), default=None)
    partOperationId = attr.ib(validator=optional(instance_of(str)), default=None)
    operationNo = attr.ib(validator=optional(instance_of(int)), default=None)
    operationCode = attr.ib(validator=optional(instance_of(str)), default=None)
    crewSize = attr.ib(validator=optional(instance_of(float)), default=None)
    standardProductionRate = attr.ib(validator=optional(instance_of(float)), default=None)
    note = attr.ib(validator=optional(instance_of(str)), default=None)
    setupTime = attr.ib(validator=optional(instance_of(float)), default=None)
    idealRate = attr.ib(validator=optional(instance_of(float)), default=None)
    targetRate = attr.ib(validator=optional(instance_of(float)), default=None)
    setupCrewSize = attr.ib(validator=optional(instance_of(float)), default=None)

    @classmethod
    def get_serialization_schema(cls, mode):
        if mode == 'out':
            schema = super().get_serialization_schema('out')
            del schema['id']
            return schema
        elif mode == 'in':
            return super().get_serialization_schema('in')

    @classmethod
    def find_approved_workcenters(
            cls,
            workcenterId=None,
            partId=None,
            partOperationId=None,
            resource_name_kwargs=None,
    ):
        return cls.search(
            workcenterId=workcenterId,
            partId=partId,
            partOperationId=partOperationId,
            exclude_if_null=['workcenterId', 'partId', 'partOperationId'],
            resource_name_kwargs=resource_name_kwargs,
        )


@attr.s(kw_only=True, repr=False)
class Workcenter(BaseObject, RetrieveMixin, SearchMixin):
    _resource_name = 'production/v1/production-definitions/workcenters'
    workcenterId = attr.ib(validator=optional(instance_of(str)), default="00000000-0000-0000-0000-000000000000")
    workcenterCode = attr.ib(validator=optional(instance_of(str)), default=None)
    name = attr.ib(validator=optional(instance_of(str)), default=None)
    workcenterType = attr.ib(validator=optional(instance_of(str)), default=None)
    workcenterGroup = attr.ib(validator=optional(instance_of(str)), default=None)
    buildingId = attr.ib(validator=optional(instance_of(str)), default="00000000-0000-0000-0000-000000000000")
    buildingCode = attr.ib(validator=optional(instance_of(str)), default=None)

    @classmethod
    def get_serialization_schema(cls, mode):
        if mode == 'out':
            schema = super().get_serialization_schema('out')
            del schema['id']
            return schema
        elif mode == 'in':
            schema = super().get_serialization_schema('in')
            del schema['id']
            return super().get_serialization_schema('in')

    @classmethod
    def find_workcenters(
            cls,
            workcenterCode=None,
            name=None,
            workcenterType=None,
            workcenterGroup=None,
            buildingId=None,
            resource_name_kwargs=None,
    ):
        return cls.search(
            workcenterCode=workcenterCode,
            name=name,
            workcenterType=workcenterType,
            workcenterGroup=workcenterGroup,
            buildingId=buildingId,
            exclude_if_null=['workcenterCode', 'name', 'workcenterType', 'workcenterGroup', 'buildingId'],
            resource_name_kwargs=resource_name_kwargs,
        )
