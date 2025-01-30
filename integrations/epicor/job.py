from datetime import datetime
from typing import List, Optional
import attr
from decimal import Decimal
from epicor.base import BaseObject
from epicor.json_encoders.generic import GenericJSONEncoder


@attr.s
class JobAssembly(BaseObject):
    base_url = 'ERP.BO.JobEntrySvc/'
    resource_name = 'JobAsmbls'

    Company = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    JobComplete = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=True)
    JobNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    AssemblySeq = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=0)
    PartNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    Description = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    RevisionNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    QtyPer = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                     default=0)
    IUM = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    RequiredQty = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                          default=0)
    EstUnitCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                          default=0)
    TotalCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                        default=0)
    TLETotalCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]
                                                                                                ))), default=0)
    BomSequence = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=0)
    BomLevel = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=0)
    PlanAsAsm = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    AddAsmAs = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    ChildAssemblySeq = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=0)
    Parent = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=0)
    ParentAssemblySeq = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=0)
    ParentPartNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    ParentRev = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    PartExists = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    JobMtls = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(List)), default=[])
    JobOpers = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(List)), default=[])

    @classmethod
    def get_multiple_job_assemblies(cls, part_number: str, revision: str) -> List['JobAssembly']:
        job_assembly_query = dict(PartNum=part_number, RevisionNum=revision)
        filter_query = cls.construct_query_filter(job_assembly_query, False)
        final_query = {
            '$filter': filter_query,
        }  # $top param allows API to return more than 100 results

        return cls.get_paginated_results_with_params(params=final_query)

    @classmethod
    def get_child_job_assemblies_by_parent_assembly(cls, job_number: str, parent_assembly_sequence_num: int):
        job_assembly_query = dict(JobNum=job_number, Parent=parent_assembly_sequence_num)
        filter_query = cls.construct_query_filter(job_assembly_query, False)
        final_query = {
            '$filter': filter_query,
        }

        return cls.get_paginated_results_with_params(params=final_query, page_size=50)


@attr.s
class JobOperation(BaseObject):
    base_url = 'ERP.BO.JobEntrySvc/'
    resource_name = 'JobOpers'

    Company = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    JobNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    AssemblySeq = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=0)
    OprSeq = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=0)
    OpCode = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    OpCodeOpDesc = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    OpStdID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    EstSetHours = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                          default=0)
    EstProdHours = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    EstStdDescription = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    EstBurdenCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                            default=0)
    EstLabHours = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                          default=0)
    EstLaborCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    EstSubCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                         default=0)
    ProdStandard = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    StdFormat = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    StdBasis = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    OpsPerPart = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                         default=0)
    QtyPer = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                     default=0)
    ProdLabRate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                          default=0)
    SetupLabRate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    ProdBurRate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                          default=0)
    SetupBurRate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    Machines = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                       default=0)
    SetUpCrewSize = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    ProdCrewSize = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    ActProdHours = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    ActProdRwkHours = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    ActSetupHours = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    ActSetupRwkHours = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    ActBurCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                         default=0)
    ActLabCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                         default=0)
    IUM = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    EstUnitCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                          default=0)
    PartNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    RevisionNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    Description = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    CommentText = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    RunQty = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                     default=0)
    LaborRate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                        default=0)
    BillableLaborRate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    DocLaborRate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    UnitPrice = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                        default=0)
    DocUnitPrice = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    PricePerCode = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    OpDesc = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    SchedComment = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    SubContract = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    VendorNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=0)
    VendorNumName = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    VendorNumVendorID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    @classmethod
    def get_job_operations(cls, job_number: int, assembly_seq: int) -> List['JobOperation']:
        job_operation_filter = dict(JobNum=job_number, AssemblySeq=assembly_seq)
        filter_query = cls.construct_query_filter(job_operation_filter, False)
        final_query = {
            '$filter': filter_query,
        }
        return cls.get_paginated_results_with_params(params=final_query, page_size=50)


@attr.s
class JobMaterial(BaseObject):
    base_url = 'ERP.BO.JobEntrySvc/'
    resource_name = 'JobMtls'

    Company = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    JobComplete = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    JobNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    AssemblySeq = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    MtlSeq = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=10)
    PartNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    RevisionNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    Description = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    QtyPer = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                     default=0)
    RequiredQty = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                          default=0)
    IUM = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    LeadTime = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                       default=0)
    RelatedOperation = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(
        tuple([Decimal, float, int]))), default=0)
    EstUnitCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                          default=0)
    IssuedQty = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                        default=0)
    TotalCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                        default=0)
    MfgComment = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    PurComment = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    VendorNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                        default=0)
    BuyIt = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    FixedQty = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    ProdCode = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    UnitPrice = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                        default=0)
    BaseUOM = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    Weight = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                     default=0)
    WeightUOM = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    @classmethod
    def get_child_materials(cls, job_number: str, assembly_seq_num: int) -> List['JobMaterial']:
        job_material_query = dict(JobNum=job_number, AssemblySeq=assembly_seq_num)
        filter_query = cls.construct_query_filter(job_material_query, False)
        final_query = {'$filter': filter_query}

        return cls.get_paginated_results_with_params(params=final_query, page_size=50)


@attr.s
class JobEntry(BaseObject):
    base_url = 'ERP.BO.JobEntrySvc/'
    resource_name = 'JobEntries'

    Company = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    JobNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    PartNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    RevisionNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    PartDescription = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    ProdQty = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([int, Decimal]))), default=None)
    OrderQty = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([int, Decimal]))), default=None)
    QuoteNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    QuoteLine = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    CustID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    CustName = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    CreateDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([datetime, str]))), default=None)
    StartDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([datetime, str]))), default=None)
    ClosedDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([datetime, str]))), default=None)
    LastChangedOn = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([datetime, str]))), default=None)
    JobCompletionDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([datetime, str]))), default=None)
    JobClosed = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    JobComplete = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    JobEngineered = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    Plant = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    JobType = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    BasePartNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    BaseRevisionNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    PartNumPartDescription = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    ProdCodeDescription = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    CommentText = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    JobAsmbls = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(List)), default=[])

    @classmethod
    def get_changed(cls, last_modified: datetime, bulk: bool = False) -> List['JobEntry']:
        last_mod_str = last_modified.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        filter_string = f'CreateDate ge {last_mod_str} or JobCompletionDate ge {last_mod_str} or ClosedDate ge {last_mod_str}'
        if bulk is True:
            filter_string += ' or LastChangedOn eq null'
        return cls.get_paginated_results_with_params(params={
            '$filter': filter_string,
            '$select': 'JobNum, PartNum, RevisionNum'
        }, page_size=1000)
        # TEST METHOD TO RETURN LESS RESULTS
        # return cls.get_all(params={
        #     '$filter': filter_string,
        #     '$top': 1000
        # })

    @classmethod
    def get_job_entries(cls, part_num: str, revision_num: str, newer_than_date_str: Optional[str] = None) -> List['JobEntry']:
        filter_string = f"PartNum eq '{part_num}' and RevisionNum eq '{revision_num}'"
        if newer_than_date_str is not None:
            filter_string += f" and CreateDate ge {newer_than_date_str}"
        job_entries: List[JobEntry] = JobEntry.get_paginated_results_with_params(params={
            '$filter': filter_string,
        })
        return job_entries

    @classmethod
    def get_all_nested_job_data_by_job_number(cls, filter_string: str, page_size: int = 10) -> List['JobEntry']:
        job_data: List = JobEntry.get_paginated_results_with_params(params={
            '$filter': filter_string,
            '$expand': 'JobAsmbls($expand=JobMtls,JobOpers)',
        }, page_size=page_size)
        job_entries: List[JobEntry] = []
        for job_entry in job_data:
            job_assemblies: List[JobAssembly] = []

            for job_assembly in job_entry.JobAsmbls:
                job_assembly: JobAssembly = JobAssembly.from_json(job_assembly, encoder_class=JobAssembly.encoder_class if hasattr(JobAssembly, "encoder_class") else GenericJSONEncoder)

                job_materials: List[JobMaterial] = []
                for job_material in job_assembly.JobMtls:
                    job_materials.append(JobMaterial.from_json(job_material, encoder_class=JobMaterial.encoder_class if hasattr(JobMaterial, "encoder_class") else GenericJSONEncoder))

                job_operations: List[JobOperation] = []
                for job_operation in job_assembly.JobOpers:
                    job_operations.append(JobOperation.from_json(job_operation, encoder_class=JobOperation.encoder_class if hasattr(JobOperation, "encoder_class") else GenericJSONEncoder))

                job_assembly.JobMtls = job_materials
                job_assembly.JobOpers = job_operations
                job_assemblies.append(job_assembly)

            job_entry.JobAsmbls = job_assemblies
            job_entries.append(job_entry)

        return job_entries
