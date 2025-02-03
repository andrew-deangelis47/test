from datetime import datetime
from typing import List, Optional
from epicor.base import BaseObject
import attr
from decimal import Decimal
from typing import Union
from epicor.client import EpicorClient
from epicor.json_encoders.generic import GenericJSONEncoder


@attr.s
class QuoteQuantity(BaseObject):
    base_url = 'Erp.BO.QuoteSvc/'
    resource_name = 'QuoteQties'

    Company = attr.ib(validator=attr.validators.instance_of(str))
    QuoteNum = attr.ib(validator=attr.validators.instance_of(int))
    QuoteLine = attr.ib(validator=attr.validators.instance_of(int))
    QtyNum = attr.ib(validator=attr.validators.instance_of(int))
    OurQuantity = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    UnitPrice = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))

    @classmethod
    def get_quote_quantity(cls, quote_num: int, quote_detail_num: int) -> List['QuoteQuantity']:
        quote_qty_filter = dict(QuoteNum=quote_num, QuoteLine=quote_detail_num)
        return cls.get_all(filters=quote_qty_filter)


@attr.s
class QuoteOperation(BaseObject):
    base_url = 'Erp.BO.QuoteAsmSvc/'
    resource_name = 'QuoteOprs'

    Company = attr.ib(validator=attr.validators.instance_of(str))
    QuoteNum = attr.ib(validator=attr.validators.instance_of(int))
    QuoteLine = attr.ib(validator=attr.validators.instance_of(int))
    OpCode = attr.ib(validator=attr.validators.instance_of(str))
    AssemblySeq = attr.ib(validator=attr.validators.instance_of(int))
    OprSeq = attr.ib(validator=attr.validators.instance_of(int))
    CommentText = attr.ib(validator=attr.validators.instance_of(str))
    StdFormat = attr.ib(validator=attr.validators.instance_of(str))
    StdBasis = attr.ib(validator=attr.validators.instance_of(str))
    SubContract = attr.ib(validator=attr.validators.instance_of(bool))
    HoursPerMachine = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([int, Decimal]))),
                              default=None)
    VendorNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    VendorNumVendorID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    PartNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    Description = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    AutoReceive = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    FinalOpr = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    DaysOut = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([int, Decimal]))),
                      default=None)
    ProdStandard = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([int, Decimal]))),
                           default=None)
    EstUnitCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([int, Decimal]))),
                          default=None)
    MinimumCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([int, Decimal]))),
                          default=None)
    EstSetHours = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([int, Decimal]))),
                          default=None)
    SetupLabRate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([int, Decimal]))),
                           default=None)
    SetupBurRate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([int, Decimal]))),
                           default=None)
    ProdLabRate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([int, Decimal]))),
                          default=None)
    ProdBurRate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([int, Decimal]))),
                          default=None)
    ProdCrewSize = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([int, Decimal]))),
                           default=None)
    SetUpCrewSize = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([int, Decimal]))),
                            default=None)

    def update_detail(self, company_name: str, data: dict):
        QuoteOperationDetail.update_resource([f"'{company_name}'", self.QuoteNum, self.QuoteLine, self.AssemblySeq,
                                              self.OprSeq, 10], data)

    @classmethod
    def get_quote_operations(cls, quote_num: int, quote_line: int, assembly_seq) -> List['QuoteOperation']:
        job_operation_query = dict(QuoteNum=quote_num, QuoteLine=quote_line, AssemblySeq=assembly_seq)
        return cls.get_all(filters=job_operation_query)


@attr.s
class QuoteOperationDetail(BaseObject):
    base_url = 'Erp.BO.QuoteAsmSvc/'
    resource_name = 'QuoteOpDtls'

    ResourceGrpID = attr.ib(validator=attr.validators.instance_of(str))
    ResourceID = attr.ib(validator=attr.validators.instance_of(str))
    SetUpCrewSize = \
        attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Union[str, int])), default=None)
    ProdCrewSize = \
        attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Union[str, int])), default=None)


@attr.s
class QuoteContact(BaseObject):
    base_url = 'Erp.BO.QuoteSvc/'
    resource_name = 'QuoteCnts'

    Company = attr.ib(validator=attr.validators.instance_of(str))
    QuoteNum = attr.ib(validator=attr.validators.instance_of(int))
    CustNum = attr.ib(validator=attr.validators.instance_of(int))  # PK ID of customer
    ConNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)))
    PerConID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)))
    Name = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    CustNumCustID = attr.ib(validator=attr.validators.instance_of(str))  # PK ID of customer
    ShipToNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)


@attr.s
class QuoteMaterial(BaseObject):
    base_url = 'Erp.BO.QuoteAsmSvc/'
    resource_name = 'QuoteMtls'

    Company = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    QuoteNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    QuoteLine = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    AssemblySeq = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    MtlSeq = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    PartNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    Description = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    IUM = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    RevisionNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    QtyPer = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([float, int, Decimal]))),
                     default=None)
    EstScrap = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([float, Decimal, int]))),
                       default=None)
    Direct = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    LeadTime = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    BuyIt = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=None)
    RelatedOperation = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    MfgComment = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    PurComment = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    VendorNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    VendorNumVendorID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    PurPoint = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    MinimumCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([float, Decimal, int]))),
                          default=None)
    EstUnitCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([float, Decimal, int]))),
                          default=None)
    MtlBurRate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([float, Decimal, int]))),
                         default=None)
    EstMtlBurUnitCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple(
        [float, Decimal, int]))), default=None)
    RequiredQty = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([float, Decimal, int]))),
                          default=None)
    FixedQty = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    Class = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    EstMtlUnitCost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple(
        [float, Decimal, int]))), default=None)
    MiscCode = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    MiscCharge = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    EnableFixedQty = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    PartExists = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    QtyBearing = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)

    @classmethod
    def get_child_materials(cls, quote_num: str, quote_line_num: int, assembly_seq_num: int) -> List['QuoteMaterial']:
        quote_material_query = dict(QuoteNum=quote_num, QuoteLine=quote_line_num, AssemblySeq=assembly_seq_num)
        return cls.get_all(filters=quote_material_query)


@attr.s
class QuoteAssembly(BaseObject):
    base_url = 'Erp.BO.QuoteAsmSvc/'
    resource_name = 'QuoteAsms'

    Company = attr.ib(validator=attr.validators.instance_of(str))
    QuoteNum = attr.ib(validator=attr.validators.instance_of(int))
    QuoteLine = attr.ib(validator=attr.validators.instance_of(int))
    PartNum = attr.ib(validator=attr.validators.instance_of(str))
    Description = attr.ib(validator=attr.validators.instance_of(str))
    QtyPer = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal, float])))
    Parent = attr.ib(validator=attr.validators.instance_of(int))
    IUM = attr.ib(validator=attr.validators.instance_of(str))
    AssemblySeq = attr.ib(validator=attr.validators.instance_of(int))
    BomLevel = attr.ib(validator=attr.validators.instance_of(int))
    ParentAssemblySeq = attr.ib(validator=attr.validators.instance_of(int))
    ParentDescription = attr.ib(validator=attr.validators.instance_of(str))
    ParentPartNum = attr.ib(validator=attr.validators.instance_of(str))
    ParentRevisionNum = attr.ib(validator=attr.validators.instance_of(str))
    PriorPeer = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=-1)
    NextPeer = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=-1)
    Child = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=-1)
    ChildAssemblySeq = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=-1)
    RevisionNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    CommentText = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    Template = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    QuoteMtls = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(List)), default=[])
    QuoteOprs = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(List)), default=[])

    @classmethod
    def get_multiple_quote_assemblies(cls, part_number: str, revision: str) -> List['QuoteAssembly']:
        quote_assembly_query = dict(PartNum=part_number, RevisionNum=revision)
        filter_query = cls.construct_query_filter(quote_assembly_query, False)
        final_query = {'$filter': filter_query}

        return cls.get_paginated_results_with_params(params=final_query)

    @classmethod
    def get_child_quote_assemblies_by_parent_assembly(cls, quote_number: str, quote_line: int,
                                                      parent_assembly_sequence_num: str):
        quote_assembly_query = dict(QuoteNum=quote_number, QuoteLine=quote_line, Parent=parent_assembly_sequence_num)
        return cls.get_all(filters=quote_assembly_query)

    @classmethod
    def get_quote_assemblies_nested_data_by_quote_num_line_num(
            cls, filter_string: str, quote_request_object_limit: int = 10) -> List['QuoteAssembly']:
        quote_assm_data: List = QuoteAssembly.get_paginated_results_with_params(params={
            '$filter': filter_string,
            '$expand': 'QuoteMtls,QuoteOprs',
        }, page_size=quote_request_object_limit + 1)
        quote_assemblies: List[QuoteAssembly] = []
        quote_materials: List[QuoteMaterial] = []
        quote_operations: List[QuoteOperation] = []
        for quote_assembly in quote_assm_data:
            for material in quote_assembly.QuoteMtls:
                quote_material: QuoteMaterial = QuoteMaterial.from_json(
                    material, encoder_class=QuoteMaterial.encoder_class if hasattr(
                        QuoteMaterial, "encoder_class") else GenericJSONEncoder)
                quote_materials.append(quote_material)
            for operation in quote_assembly.QuoteOprs:
                quote_operation: QuoteOperation = QuoteOperation.from_json(
                    operation, encoder_class=QuoteOperation.encoder_class if hasattr(
                        QuoteOperation, "encoder_class") else GenericJSONEncoder)
                quote_operations.append(quote_operation)

            quote_assembly.QuoteMtls = quote_materials
            quote_assembly.QuoteOprs = quote_operations
            quote_assemblies.append(quote_assembly)

        return quote_assemblies


@attr.s
class QuoteDetail(BaseObject):
    base_url = 'Erp.BO.QuoteSvc/'
    resource_name = 'QuoteDtls'

    Company = attr.ib(validator=attr.validators.instance_of(str))
    CustNum = attr.ib(validator=attr.validators.instance_of(int))  # PK ID of customer
    CustomerCustID = attr.ib(validator=attr.validators.instance_of(str))  # User-defined Epicor ID number
    QuoteNum = attr.ib(validator=attr.validators.instance_of(int))
    QuoteLine = attr.ib(validator=attr.validators.instance_of(int))
    PartNum = attr.ib(validator=attr.validators.instance_of(str))
    LineDesc = attr.ib(validator=attr.validators.instance_of(str))
    OrderQty = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    SellingExpectedQty = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    Engineer = attr.ib(validator=attr.validators.instance_of(bool))
    ReadyToQuote = attr.ib(validator=attr.validators.instance_of(bool))
    DateQuoted = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([datetime, str]))),
                         default=None)
    EntryDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([datetime, str]))),
                        default=None)
    ExpirationDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([datetime, str]))),
                             default=None)
    ChangeDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([datetime, str]))),
                         default=None)
    RevisionNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    ProdCode = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    SalesCatID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    QuoteComment = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    LineType = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    Template = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=None)
    LeadTime = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    QuoteQties = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(List)), default=[])
    QuoteMscs = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(List)), default=[])
    SellingExpectedUM = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default='EA')

    @classmethod
    def get_changed(cls, last_modified: datetime, bulk: bool = False) -> List['QuoteDetail']:
        last_mod_str = last_modified.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        filter_string = f'ChangeDate ge {last_mod_str}'
        if bulk is True:
            filter_string += ' or ChangeDate eq null'
        return cls.get_all(params={
            '$filter': filter_string,
            '$top': 1000
        })

    @classmethod
    def get_quote_details(cls, part_num: str, revision_num: str, newer_than_date_str: Optional[str] = None
                          ) -> List['QuoteDetail']:
        filter_string = f"PartNum eq '{part_num}' and RevisionNum eq '{revision_num}'"
        if newer_than_date_str is not None:
            filter_string += f" and DateQuoted ge {newer_than_date_str}"
        quote_details: List[QuoteDetail] = QuoteDetail.get_paginated_results_with_params(params={
            '$filter': filter_string})

        return quote_details

    @classmethod
    def get_by_quote_num_and_line(cls, company_code: str, quote_num: str, quote_line: str):
        client: EpicorClient = EpicorClient.get_instance()
        results = client.get_resource(f"{cls.base_url}{cls.resource_name}('{company_code}',{quote_num},{quote_line})")
        result: List[cls] = [cls.from_json(results, encoder_class=cls.encoder_class if hasattr(
            cls, "encoder_class") else GenericJSONEncoder)]
        return result

    @classmethod
    def get_quote_detail_nested_data_by_quote_num_line_num(cls, quote_num: int, quote_line: int
                                                           ) -> Optional['QuoteDetail']:
        filter_string = f"QuoteNum eq {quote_num} and QuoteLine eq {quote_line}"
        quote_data: List = QuoteDetail.get_response_json_value(params={
            '$filter': filter_string,
            '$expand': 'QuoteQties',
            '$top': 10
        })
        quote_detail: Optional[QuoteDetail] = None
        quote_qtys: List[QuoteQuantity] = []
        for quote_item in quote_data:
            for quantity in quote_item["QuoteQties"]:
                quote_qty: QuoteQuantity = QuoteQuantity.from_json(
                    quantity, encoder_class=QuoteQuantity.encoder_class if hasattr(
                        QuoteQuantity, "encoder_class") else GenericJSONEncoder)
                quote_qtys.append(quote_qty)

            quote_detail = cls.from_json(quote_item, encoder_class=GenericJSONEncoder)
            quote_detail.QuoteQties = quote_qtys

        return quote_detail


@attr.s
class QuoteDetailSearch(BaseObject):
    base_url = 'Erp.BO.QuoteDtlSearchSvc/'
    resource_name = 'QuoteDtlSearches'

    Company = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    CustNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    CustomerCustID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    QuoteNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    QuoteLine = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    PartNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    LineDesc = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    OrderQty = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([int, Decimal]))),
                       default=None)
    SellingExpectedQty = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([int, Decimal]))),
                                 default=None)
    Engineer = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=None)
    ReadyToQuote = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=None)
    DateQuoted = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([datetime, str]))),
                         default=None)
    EntryDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([datetime, str]))),
                        default=None)
    ExpirationDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([datetime, str]))),
                             default=None)
    ChangeDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([datetime, str]))),
                         default=None)
    RevisionNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    ProdCode = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    QuoteComment = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    LineType = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    Template = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=None)
    LeadTime = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    @classmethod
    def get_changed(cls, last_modified: datetime, bulk: bool = False) -> List['QuoteDetailSearch']:
        last_mod_str = last_modified.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        filter_string = f'ChangeDate ge {last_mod_str}'
        if bulk is True:
            filter_string += ' or ChangeDate eq null'
        return cls.get_paginated_results_with_params(params={
            '$filter': filter_string,
            '$select': 'QuoteNum, PartNum, RevisionNum'
        }, page_size=1000)
        # TEST METHOD TO RETURN LESS RESULTS
        # return cls.get_all(params={
        #     '$filter': filter_string,
        #     '$select': 'QuoteNum, PartNum, RevisionNum',
        #     "$top": 1000
        # })

    @classmethod
    def get_quote_details(cls, part_num: str, revision_num: str, newer_than_date_str: Optional[str] = None
                          ) -> List['QuoteDetailSearch']:
        filter_string = f"PartNum eq '{part_num}' and RevisionNum eq '{revision_num}'"
        if newer_than_date_str is not None:
            filter_string += f" and DateQuoted ge {newer_than_date_str}"
        quote_details: List[QuoteDetailSearch] = QuoteDetailSearch.get_paginated_results_with_params(params={
            '$filter': filter_string})

        return quote_details


@attr.s
class QuoteMiscellaneousCharge(BaseObject):
    base_url = 'Erp.BO.QuoteSvc/'
    resource_name = 'QuoteMscs'

    Company = attr.ib(validator=attr.validators.instance_of(str))
    QuoteNum = attr.ib(validator=attr.validators.instance_of(int))
    MiscCode = attr.ib(validator=attr.validators.instance_of(str))
    Description = attr.ib(validator=attr.validators.instance_of(str))
    MiscAmt = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    DocMiscAmt = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    DspMiscAmt = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    DocDspMiscAmt = attr.ib(validator=attr.validators.instance_of(tuple([int, Decimal])))
    QuoteLine = attr.ib(validator=attr.validators.instance_of(int))
    FreqCode = attr.ib(validator=attr.validators.instance_of(str))


@attr.s
class QuoteHeader(BaseObject):
    base_url = 'Erp.BO.QuoteSvc/'
    resource_name = 'Quotes'

    CustNum = attr.ib(validator=attr.validators.instance_of(int))  # PK ID of customer
    CustomerCustID = attr.ib(validator=attr.validators.instance_of(str))  # User-defined Epicor ID number
    TermsCode = attr.ib(validator=(attr.validators.instance_of(str)), default=None)  # Quote terms code ID
    QuoteNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    Quoted = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=None)
    ShipToNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    ShipToCustNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    ShpConNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    QuoteComment = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    PONum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    DueDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    SalesRepName = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    EntryDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    NeedByDate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    SalesRepCode = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    Reference = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    QuoteDtls = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(List)), default=[])

    @classmethod
    def get_quote_header_nested_data_by_quote_num(cls, filter_string: str, page_size: int = 10) -> List['QuoteHeader']:
        quote_header_data: List = QuoteHeader.get_paginated_results_with_params(params={
            '$filter': filter_string,
            '$expand': 'QuoteDtls($expand=QuoteQties,QuoteMscs)',
        }, page_size=page_size)
        quote_headers: List[QuoteHeader] = []
        for quote_header in quote_header_data:
            quote_details: List[QuoteDetail] = []
            for detail in quote_header.QuoteDtls:
                quote_detail: QuoteDetail = QuoteDetail.from_json(
                    detail, encoder_class=QuoteDetail.encoder_class if hasattr(
                        QuoteDetail, "encoder_class") else GenericJSONEncoder)

                quote_qtys: List[QuoteQuantity] = []
                for quantity in detail["QuoteQties"]:
                    quote_qty: QuoteQuantity = QuoteQuantity.from_json(
                        quantity, encoder_class=QuoteQuantity.encoder_class if hasattr(
                            QuoteQuantity, "encoder_class") else GenericJSONEncoder)
                    quote_qtys.append(quote_qty)
                quote_misc_charges: List[QuoteMiscellaneousCharge] = []
                for misc_charge in detail["QuoteMscs"]:
                    misc_charge: QuoteMiscellaneousCharge = QuoteMiscellaneousCharge.from_json(
                        misc_charge, encoder_class=QuoteMiscellaneousCharge.encoder_class if hasattr(
                            QuoteMiscellaneousCharge, "encoder_class") else GenericJSONEncoder)
                    quote_misc_charges.append(misc_charge)

                quote_detail.QuoteQties = quote_qtys
                quote_detail.QuoteMscs = quote_misc_charges
                quote_details.append(quote_detail)
            quote_header.QuoteDtls = quote_details
            quote_headers.append(quote_header)

        return quote_headers
