from datetime import datetime
from typing import List, Optional
import attr
from decimal import Decimal
from epicor.base import BaseObject
from epicor.json_encoders.generic import GenericJSONEncoder


@attr.s
class EngineeringWorkbench(BaseObject):
    base_url = 'ERP.BO.EngWorkBenchSvc/'
    resource_name = 'EngWorkBenches'

    Company = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    GroupID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    Description = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    GroupClosed = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    CommentText = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    EffectiveDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    CompletionDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    DueDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    CreatedDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    CreatedBy = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    CreatedTime = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    ClosedDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    ClosedBy = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    ClosedTime = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    ECO = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    TaskSetID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    CurrentWFStageID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    ActiveTaskID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    LastTaskID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    CheckInAllowed = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    PrimeSalesRepCode = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    WFGroupID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    CheckOutAllowed = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    WFComplete = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    SingleUser = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    GrpLocked = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    GrpLockedBy = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    SysRevID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    SysRowID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    MassAssignDesc = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    MassAssignECO = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    MassAssignEffectiveDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    CanApproveAll = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    MultiBOMAllowed = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    CanCheckInAll = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    WFGroupIDDesc = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    UseMethodForPartsInTree = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    CurrentWFStageDesc = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    EnableCheckInAll = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    BitFlag = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    TaskSetIDWorkflowType = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    TaskSetIDTaskSetDescription = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)


@attr.s
class EWBOperation(BaseObject):
    base_url = 'ERP.BO.EngWorkBenchSvc/'
    resource_name = 'ECOOprs'

    Company = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    PartNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    RevisionNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    OprSeq = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                     default=0)
    OpCode = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    OpDesc = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    OpStdID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    EstSetHours = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                          default=0)
    EstProdHours = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    ProdStandard = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    StdFormat = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    StdBasis = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    OpsPerPart = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                         default=0)
    QtyPer = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                     default=1)
    SetUpCrewSize = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([float, Decimal, int]))), default=None)
    ProdCrewSize = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    SubContract = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    IUM = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    EstUnitCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([float, Decimal, int]))), default=None)
    VendorNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([float, Decimal, int]))), default=None)
    CommentText = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    OpStdDescription = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    @classmethod
    def get_ewb_operations(cls, part_num: str, revision_num: str) -> List['EWBOperation']:
        filter_string = f"PartNum eq '{part_num}' and RevisionNum eq '{revision_num}'"
        ewb_operations: List[EWBOperation] = EWBOperation.get_all(params={
            '$filter': filter_string,
            '$top': 50
        })
        return ewb_operations


@attr.s
class EWBMaterial(BaseObject):
    base_url = 'ERP.BO.EngWorkBenchSvc/'
    resource_name = 'ECOMtls'

    Company = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    PartNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    RevisionNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    MtlSeq = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=0)
    ParentMtlSeq = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=0)
    MtlPartNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    MtlRevisionNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    QtyPer = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([float, Decimal, int]))),
                     default=None)
    FixedQty = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([float, Decimal, int]))),
                       default=None)
    MfgComment = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    PurComment = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    PullAsAsm = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=None)
    ViewAsAsm = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=None)
    PlanAsAsm = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=None)
    MtlBurRate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([float, Decimal, int]))),
                         default=None)
    EstMtlBurUnitCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple(
        [float, Decimal, int]))), default=None)
    UOMCode = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    Weight = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([float, Decimal, int]))),
                     default=None)
    WeightUOM = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    IsPartMtl = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=None)
    EnableFixedQty = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=None)
    SysRowID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    @classmethod
    def get_ewb_assemblies(cls, part_number: str, revision: str) -> List['EWBMaterial']:
        ewb_assembly_query = dict(PartNum=part_number, RevisionNum=revision, PullAsAsm=True)
        # PullAsAsm=True means the record will be pulled into a Job/Quote as an actual component
        filter_query = cls.construct_query_filter(ewb_assembly_query, False)
        final_query = {
            '$filter': filter_query,
            '$top': 100
        }  # $top param allows API to return more than 100 results

        return cls.get_with_params(params=final_query)

    @classmethod
    def get_ewb_repeat_part_materials(cls, part_number: str, revision: str) -> List['EWBMaterial']:
        ewb_material_query = dict(PartNum=part_number, RevisionNum=revision, ViewAsAsm=True, PullAsAsm=False)
        # PullAsAsm=False means the record will be pulled into a Job/Quote as a material
        filter_query = cls.construct_query_filter(ewb_material_query, False)
        final_query = {
            '$filter': filter_query,
            '$top': 100
        }  # $top param allows API to return more than 100 results

        return cls.get_with_params(params=final_query)

    @classmethod
    def get_all_ewb_repeat_part_materials(cls) -> List['EWBMaterial']:
        ewb_material_query = dict(ViewAsAsm=True, PullAsAsm=False)
        # PullAsAsm=False means the record will be pulled into a Job/Quote as a material
        filter_query = cls.construct_query_filter(ewb_material_query, False)
        final_query = {
            '$filter': filter_query,
            '$top': 100
        }  # $top param allows API to return more than 100 results

        return cls.get_with_params(params=final_query)

    @classmethod
    def get_child_ewb_assemblies_by_parent_assembly(cls, ewb_part_number: str, ewb_revision: str,
                                                    parent_assembly_sequence_num: int):
        ewb_assembly_query = dict(PartNum=ewb_part_number, RevisionNum=ewb_revision,
                                  ParentMtlSeq=parent_assembly_sequence_num)
        filter_query = cls.construct_query_filter(ewb_assembly_query, False)
        final_query = {
            '$filter': filter_query,
            '$top': 100
        }

        return cls.get_with_params(params=final_query)


@attr.s
class EWBRev(BaseObject):
    base_url = 'ERP.BO.EngWorkBenchSvc/'
    resource_name = 'ECORevs'

    Company = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    GroupID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    PartNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    RevisionNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    RevShortDesc = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    RevDescription = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    EffectiveDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    TLRLaborCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)),
                           default=Decimal(0.0))
    TLRBurdenCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)),
                            default=Decimal(0.0))
    TLRMaterialCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)),
                              default=Decimal(0.0))
    TLRSubcontractCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)),
                                 default=Decimal(0.0))
    TLRMtlBurCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)),
                            default=Decimal(0.0))
    TLRSetupLaborCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)),
                                default=Decimal(0.0))
    TLRSetupBurdenCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)),
                                 default=Decimal(0.0))
    LLRLaborCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)),
                           default=Decimal(0.0))
    LLRBurdenCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)),
                            default=Decimal(0.0))
    LLRMaterialCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)),
                              default=Decimal(0.0))
    LLRSubcontractCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)),
                                 default=Decimal(0.0))
    LLRMtlBurCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)),
                            default=Decimal(0.0))
    LLRSetupLaborCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)),
                                default=Decimal(0.0))
    LLRSetupBurdenCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)),
                                 default=Decimal(0.0))
    SysRowID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    ECOMtls = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(List)), default=[])
    ECOOprs = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(List)), default=[])

    @classmethod
    def get_ewb_revs(cls, part_num: str, revision_num: str, newer_than_date_str: Optional[str] = None) -> List['EWBRev']:
        filter_string = f"PartNum eq '{part_num}' and RevisionNum eq '{revision_num}'"
        if newer_than_date_str is not None:
            filter_string += f" and ApprovedDate ge {newer_than_date_str}"
        ewb_revs: List[EWBRev] = EWBRev.get_all(params={
            '$filter': filter_string,
            '$top': 1000
        })
        return ewb_revs

    @classmethod
    def get_changed(cls, last_modified: datetime, bulk: bool = False) -> List['EWBRev']:
        last_mod_str = last_modified.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        filter_string = f'EffectiveDate ge {last_mod_str}'
        if bulk is True:
            filter_string += ' or ApprovedDate eq null'
        # return cls.get_paginated_results_with_params(params={
        #     '$filter': filter_string,
        #     '$select': 'SysRowID, PartNum, RevisionNum',
        # }, page_size=1000)
        # TEST METHOD TO RETURN LESS RESULTS
        return cls.get_all(params={
            '$filter': filter_string,
            '$select': 'SysRowID, PartNum, RevisionNum',
            '$top': 1000
        })

    @classmethod
    def get_all_nested_ewb_rev_data_by_sys_row_id(cls, filter_string: str, page_size: int = 10) -> List['EWBRev']:
        ewb_rev_data: List = EWBRev.get_paginated_results_with_params(params={
            '$filter': filter_string,
            '$expand': 'ECOMtls,ECOOprs',
        }, page_size=page_size)
        ewb_revs: List[EWBRev] = []
        for ewb_rev in ewb_rev_data:
            ewb_materials: List[EWBMaterial] = []
            ewb_operations: List[EWBOperation] = []

            for ewb_material in ewb_rev.ECOMtls:
                ewb_material: EWBMaterial = EWBMaterial.from_json(ewb_material, encoder_class=EWBMaterial.encoder_class if hasattr(EWBMaterial, "encoder_class") else GenericJSONEncoder)
                ewb_materials.append(ewb_material)
            for ewb_operation in ewb_rev.ECOOprs:
                ewb_operation: EWBOperation = EWBOperation.from_json(ewb_operation, encoder_class=EWBOperation.encoder_class if hasattr(EWBOperation, "encoder_class") else GenericJSONEncoder)
                ewb_operations.append(ewb_operation)

            ewb_rev.ECOMtls = ewb_materials
            ewb_rev.ECOOprs = ewb_operations
            ewb_revs.append(ewb_rev)

        return ewb_revs
