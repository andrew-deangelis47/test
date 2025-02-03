from decimal import Decimal
from epicor.base import BaseObject
import attr


@attr.s
class Operation(BaseObject):
    base_url = 'Erp.BO.OpMasterSvc/'
    resource_name = 'OpMasters'

    Company = attr.ib(validator=attr.validators.instance_of(str))
    OpCode = attr.ib(validator=attr.validators.instance_of(str))
    OpDesc = attr.ib(validator=attr.validators.instance_of(str))
    OPType = attr.ib(validator=attr.validators.instance_of(str))
    Subcontract = attr.ib(validator=attr.validators.instance_of(bool))
    VendorNum = attr.ib(validator=attr.validators.instance_of(int))
    CommentText = attr.ib(validator=attr.validators.instance_of(str))

    def get_details(self, erp_config):
        params = {
            "$top": int(erp_config.returned_record_limit)
        }
        return OperationDetails.get_by('OpCode', self.OpCode, params)


@attr.s
class OperationDetails(BaseObject):
    base_url = 'Erp.BO.OpMasterSvc/'
    resource_name = 'OpMasDtls'

    Company = attr.ib(validator=attr.validators.instance_of(str))
    OpCode = attr.ib(validator=attr.validators.instance_of(str))
    OpDtlSeq = attr.ib(validator=attr.validators.instance_of(int))
    ResourceGrpID = attr.ib(validator=attr.validators.instance_of(str))  # may be blank
    ResourceID = attr.ib(validator=attr.validators.instance_of(str))  # may be blank
    Plant = attr.ib(validator=attr.validators.instance_of(str))  # may be blank


@attr.s
class ResourceGroup(BaseObject):
    base_url = 'Erp.BO.ResourceGroupSvc/'
    resource_name = 'ResourceGroups'

    Company = attr.ib(validator=attr.validators.instance_of(str))
    ResourceGrpID = attr.ib(validator=attr.validators.instance_of(str))
    OpCode = attr.ib(validator=attr.validators.instance_of(str))  # may be blank
    Plant = attr.ib(validator=attr.validators.instance_of(str))
    Description = attr.ib(validator=attr.validators.instance_of(str))
    ProdBurRate = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    ProdLabRate = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    SetupBurRate = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    SetupLabRate = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    QProdBurRate = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    QProdLabRate = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    QSetupBurRate = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    QSetupLabRate = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))


@attr.s
class Resource(BaseObject):
    base_url = 'Erp.BO.ResourceSvc/'
    resource_name = 'Resources'

    Company = attr.ib(validator=attr.validators.instance_of(str))
    ResourceID = attr.ib(validator=attr.validators.instance_of(str))
    ResourceGrpID = attr.ib(validator=attr.validators.instance_of(str))  # may be blank
    OpCode = attr.ib(validator=attr.validators.instance_of(str))  # may be blank
    Description = attr.ib(validator=attr.validators.instance_of(str))
    ProdBurRate = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    ProdLabRate = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    SetupBurRate = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    SetupLabRate = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    QProdBurRate = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    QProdLabRate = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    QSetupBurRate = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    QSetupLabRate = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
