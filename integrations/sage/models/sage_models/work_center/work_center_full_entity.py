import attr
from sage.models.sage_models.work_center import WorkCenter, WorkCenterExtraInfo
from attr.validators import instance_of, optional
from sage.models.sage_models.base_object import BaseObject


class WorkCenterFullEntity(BaseObject):

    def __init__(self, work_center: WorkCenter, extra_info: WorkCenterExtraInfo):
        self.work_center = work_center
        self.extra_info = extra_info

    work_center = attr.ib(validator=optional(instance_of(WorkCenter)), default=None)
    extra_info = attr.ib(validator=optional(instance_of(WorkCenterExtraInfo)), default=None)
