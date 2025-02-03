from baseintegration.utils.repeat_work_objects import Part as RepeatPart, MethodOfManufacture, Child, AddOn
from epicor.engineering_workbench import EWBRev, EWBOperation, EWBMaterial
from typing import List, Dict, Union, Tuple
from epicor.quote import QuoteDetail, QuoteQuantity, QuoteAssembly, QuoteDetailSearch
from epicor.job import JobEntry, JobAssembly
from baseintegration.utils import safe_get, logger


class RepeatPartUtilObject:

    def __init__(self, repeat_part: RepeatPart, epicor_job_entries: List[JobEntry],
                 epicor_job_assemblies: List[JobAssembly], epicor_child_job_assemblies: Dict[str, List[JobAssembly]],
                 epicor_quote_details: List[QuoteDetail], epicor_quote_assemblies: List[QuoteAssembly],
                 epicor_child_quote_assemblies: Dict[str, List[QuoteAssembly]], epicor_ewb_revs: List[EWBRev],
                 epicor_ewb_assemblies: List[EWBMaterial], epicor_child_ewb_assemblies: Dict[str, List[EWBMaterial]]):
        self.repeat_part: RepeatPart = repeat_part
        self.epicor_client_cache = None

        self.epicor_job_entries: List[JobEntry] = epicor_job_entries
        self.epicor_job_assemblies: List[JobAssembly] = epicor_job_assemblies
        self.epicor_child_job_assemblies: Dict[str, List[JobAssembly]] = epicor_child_job_assemblies

        self.epicor_quote_details: List[QuoteDetail] = epicor_quote_details
        self.epicor_quote_assemblies: List[QuoteAssembly] = epicor_quote_assemblies
        self.epicor_child_quote_assemblies: Dict[str, List[QuoteAssembly]] = epicor_child_quote_assemblies

        self.epicor_ewb_revs: List[EWBRev] = epicor_ewb_revs
        self.epicor_ewb_assemblies: List[EWBMaterial] = epicor_ewb_assemblies
        self.epicor_child_ewb_assemblies: Dict[str, List[EWBMaterial]] = epicor_child_ewb_assemblies

        self.quote_mom_utils: List[QuoteMOMUtil] = []
        self.job_mom_utils: List[JobMOMUtil] = []
        self.ewb_mom_utils: List[EWBMOMUtil] = []


class QuoteMOMUtil:
    def __init__(self, mom: MethodOfManufacture, epicor_quote_detail: QuoteDetail, epicor_quote_qty: QuoteQuantity, quote_assembly: QuoteAssembly, type: str, erp_code: str):
        self.mom: MethodOfManufacture = mom
        self.quote_assembly: QuoteAssembly = quote_assembly
        self.epicor_quote_detail: QuoteDetail = epicor_quote_detail
        self.epicor_quote_qty: QuoteQuantity = epicor_quote_qty
        self.add_ons: List[AddOn] = []
        self.type: str = type
        self.erp_code: str = erp_code


class JobMOMUtil:
    def __init__(self, mom: MethodOfManufacture, epicor_job: JobEntry, job_assembly: JobAssembly, type: str, erp_code: str):
        self.mom: MethodOfManufacture = mom
        self.epicor_job: JobEntry = epicor_job
        self.job_assembly: JobAssembly = job_assembly
        self.type: str = type
        self.erp_code: str = erp_code


class EWBMOMUtil:
    def __init__(self, mom, epicor_ewb_rev: EWBRev, type: str, erp_code: str):
        self.mom: MethodOfManufacture = mom
        self.epicor_ewb_rev: EWBRev = epicor_ewb_rev
        self.operations: List[EWBOperation] = []
        self.required_materials: List[EWBMaterial] = []
        self.children: List[Child] = []
        self.type: str = type
        self.erp_code: str = erp_code


def get_quote_detail_erp_code(epicor_quote_detail: QuoteDetail) -> str:
    erp_code = f"{epicor_quote_detail.QuoteNum}-{epicor_quote_detail.QuoteLine}"
    return erp_code


def construct_ewb_erp_code(ewb_rev: EWBRev):
    part_num = safe_get(ewb_rev, "PartNum", None)
    rev = safe_get(ewb_rev, "RevisionNum", None)
    group_id = safe_get(ewb_rev, "GroupID", None)
    if part_num and rev:
        return f"{part_num}-{rev}-{group_id}"
    return str(part_num)


def get_ewb_unique_identifier(part_number: str, revision: str) -> str:
    return f"{part_number}:_:{revision}"


MATERIAL_COSTING_VARS = {
    "MtlSeq": 0,
    "PartNum": "",
    "RevisionNum": "",
    "QtyPer": 0,
    "IUM": "string",
    "Direct": False,
    "LeadTime": 0,
    "VendorNum": 0,
    "BuyIt": False,
    "MinimumCost": 0,
    "EstUnitCost": 0,
    "MtlBurRate": 0,
    "EstMtlBurUnitCost": 0,
    "RequiredQty": 0,
    "FixedQty": False,
    "Class": "string",
    "EstMtlUnitCost": 0,
    "EnableFixedQty": False,
    "PartExists": False,
    "QtyBearing": False,
    "ClassDescription": "",
    "ClassInactive": False,
}

JOB_MATERIAL_COSTING_VARS = {
    "MtlSeq": 0,
    "PartNum": "",
    "RevisionNum": "",
    "QtyPer": 0,
    "RequiredQty": 0,
    "IUM": "string",
    "LeadTime": 0,
    "MtlBurRate": 0,
    "EstMtlBurUnitCost": 0,
    "EstUnitCost": 0,
    "IssuedQty": 0,
    "TotalCost": 0,
    "MtlBurCost": 0,
    "VendorNum": 0,
    "FixedQty": False,
    "Direct": False,
    "MaterialMtlCost": 0,
    "MaterialLabCost": 0,
    "MaterialSubCost": 0,
    "MaterialBurCost": 0,
    "ProdCode": "",
    "UnitPrice": 0,
    "DocUnitPrice": 0,
    "Weight": 0,
    "WeightUOM": "",
    "EstMtlUnitCost": 0,
    "EstLbrUnitCost": 0,
    "EstBurUnitCost": 0,
    "EstSubUnitCost": 0,
    "EstCost": 0,
    "PartExists": False,
    "SubContract": False,
}

JOB_OPERATION_COSTING_VARS = {
    "OpCode": "",
    "OpStdID": "",
    "EstSetHours": 0,
    "EstProdHours": 0,
    "ProdStandard": 0,
    "StdFormat": "",
    "StdBasis": "",
    "OpsPerPart": 0,
    "QtyPer": 0,
    "ProdLabRate": 0,
    "SetupLabRate": 0,
    "ProdBurRate": 0,
    "SetupBurRate": 0,
    "AddedOper": False,
    "Machines": 0,
    "SetUpCrewSize": 0,
    "ProdCrewSize": 0,
    "EstScrap": 0,
    "EstScrapType": "",
    "SubContract": False,
    "IUM": "string",
    "EstUnitCost": 0,
    "PartNum": "",
    "Description": "",
    "VendorNum": 0,
    "CommentText": "",
    "RunQty": 0,
    "ReworkBurCost": 0,
    "ReworkLabCost": 0,
    "HoursPerMachine": 0,
    "LaborRate": 0,
    "BillableLaborRate": 0,
    "DocLaborRate": 0,
    "DocBillableLaborRate": 0,
    "Billable": False,
    "UnitPrice": 0,
    "BillableUnitPrice": 0,
    "DocBillableUnitPrice": 0,
    "DocUnitPrice": 0,
    "EstBurdenCost": 0,
    "EstLabHours": 0,
    "EstLaborCost": 0,
    "EstSubCost": 0,
    "FinalOpr": False,
    "ProductionQty": 0,
    "ScrapQty": 0,
    "OpCodeOpDesc": "",
    "ActProdHours": 0,
    "ActProdRwkHours": 0,
    "ActSetupHours": 0,
    "ActSetupRwkHours": 0,
    "ActBurCost": 0,
    "ActLabCost": 0,
}

QUOTE_OPERATION_COSTING_VARS = {
    "OpCode": "",
    "OpStdID": "",
    "EstSetHours": 0,
    "ProdStandard": 0,
    "StdFormat": "",
    "StdBasis": "",
    "OpsPerPart": 0,
    "QtyPer": 0,
    "ProdLabRate": 0,
    "SetupLabRate": 0,
    "ProdBurRate": 0,
    "SetupBurRate": 0,
    "Machines": 0,
    "SetUpCrewSize": 0,
    "ProdCrewSize": 0,
    "EstScrap": 0,
    "EstScrapType": "",
    "SubContract": False,
    "IUM": "",
    "DaysOut": 0,
    "PartNum": "",
    "Description": "",
    "VendorNum": 0,
    "CommentText": "",
    "MinimumCost": 0,
    "EstUnitCost": 0,
    "AddlSetupHours": 0,
    "AddlSetUpQty": 0,
    "RunQty": 0,
    "MiscAmt": 0,
    "OpDesc": "",
    "FinalOpr": False,
    "HoursPerMachine": 0,
    "OpCodeOpDesc": "",
}


def split_entity_id(repeat_part_number: str) -> Union[Tuple[str, str], Tuple[str, None]]:
    ids_list: List[str] = repeat_part_number.split(":_:")
    if len(ids_list) == 2:
        return ids_list[0], ids_list[1]
    elif len(ids_list) == 1:
        return ids_list[0], None
    if len(ids_list) != 2:
        logger.info(
            f"Unable to import part with entity ID {repeat_part_number}. Entity ID {repeat_part_number}"
            f" is not well-formed: there must be a part number and revision number specified, separated by :_:"
        )
        raise ValueError(f"Unable to import part with entity ID {repeat_part_number}. Entity ID "
                         f"{repeat_part_number} is not well-formed: there must be a part number and revision number"
                         f" specified, separated by :_:")


def create_id_separated_part_number_and_revision_string(epicor_object: Union[JobEntry, JobAssembly, QuoteDetail, QuoteDetailSearch, QuoteAssembly, EWBRev, EWBMaterial]) -> str:
    part_number = epicor_object.PartNum
    revision = epicor_object.RevisionNum
    id_separator = ":_:"
    return f"{part_number}{id_separator}{revision}"
