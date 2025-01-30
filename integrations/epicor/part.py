from datetime import datetime, timedelta

import attr
from epicor.client import EpicorClient
from epicor.base import BaseObject

from typing import Optional, List, Dict, Any

from paperless.objects.utils import positive_number_validator
from decimal import Decimal

from epicor.exceptions import EpicorNotFoundException
from baseintegration.datamigration import logger


@attr.s
class PartRev(BaseObject):
    base_url = 'Erp.BO.PartSvc/'
    resource_name = 'PartRevs'

    PartNum = attr.ib(validator=attr.validators.instance_of(str))
    Company = attr.ib(validator=attr.validators.instance_of(str))
    RevisionNum = attr.ib(validator=attr.validators.instance_of(tuple([int, str])))
    RevDescription = attr.ib(validator=attr.validators.instance_of(str))
    DrawNum: Optional[str] = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(str)))

    @classmethod
    def get(cls, company_id, part_num, rev_num):
        try:
            # we have to use this alternate GET endpoint, as the standard one times out
            # TODO: this call fails when there are special characters (such as '/') in the part number, investigate
            url = f"{cls.base_url}{cls.resource_name}('{company_id}','{part_num}','{rev_num}','','')"
            client: EpicorClient = EpicorClient.get_instance()
            return cls.from_json(client.get_resource(url))
        except Exception:
            return None


@attr.s
class Part(BaseObject):
    base_url = 'Erp.BO.PartSvc/'
    resource_name = 'Parts'
    # _json_encoder = PartEncoder

    PartNum: str = attr.ib(validator=attr.validators.instance_of(str))
    Company: str = attr.ib(validator=attr.validators.instance_of(str))
    PartDescription: str = attr.ib(validator=attr.validators.instance_of(str))
    ClassID: str = attr.ib(validator=attr.validators.instance_of(str))
    UnitPrice: Decimal = attr.ib(
        converter=Decimal, validator=positive_number_validator,
        default=Decimal(0)
    )
    TypeCode: str = attr.ib(validator=attr.validators.instance_of(str), default="M")
    LowLevelCode: int = attr.ib(validator=attr.validators.instance_of(int), default=0)
    CostMethod: str = attr.ib(validator=attr.validators.instance_of(str), default="L")
    IUM: str = attr.ib(validator=attr.validators.instance_of(str), default=None)
    UOMClassID: str = attr.ib(validator=attr.validators.instance_of(str), default=None)
    PUM: str = attr.ib(validator=attr.validators.instance_of(str), default=None)
    SalesUM: str = attr.ib(validator=attr.validators.instance_of(str), default=None)
    CreatedOn = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([datetime, str]))),
                        default=None)
    ChangedOn = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([datetime, str]))),
                        default=None)
    InActive = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=False)
    PartLength = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                         default=0.0)
    PartWidth = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                        default=0.0)
    PartHeight = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                         default=0.0)
    Thickness = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(tuple([Decimal, float, int]))),
                        default=0.0)
    # GroupCode = attr.ib(validator=attr.validators.instance_of(str))

    # Optional, not needed for creation

    # Sales category
    ShortChar02: str = attr.ib(
        default=None, validator=attr.validators.optional(
            attr.validators.instance_of(str)))

    @property
    def SalesCategory(self) -> str:
        return self.ShortChar02

    # Company = attr.ib(validator=attr.validators.instance_of(str))
    # Optional, not needed for creation CustNum: Optional[int] = attr.ib(
    # default=None, validator=attr.validators.optional(
    # attr.validators.instance_of(int)))
    AnalysisCode: Optional[str] = attr.ib(default=None,
                                          validator=attr.validators.optional(
                                              attr.validators.instance_of(
                                                  str)))
    ProdCode: Optional[str] = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(str)))

    @classmethod
    def get_contextual_error_message_for_model_if_possible(cls, converted_error_message: str, part_data: dict) -> str:
        """
        for some models there are specific errors that we can provide more information about, in addition to the
        error mapping yaml message
        """
        if "Tried to create part with an invalid Class property" in converted_error_message:
            return converted_error_message + f' Class was "{part_data["ClassID"] if "ClassID" in part_data else "None"}". ' \
                                             f'PN was "{part_data["PartNum"] if "PartNum" in part_data else "None"}".'

        return converted_error_message

    @classmethod
    def get(cls, CompanyID: str, PartNum: str):
        try:
            part = cls.get_by('PartNum', PartNum)
            logger.debug('part found')
            return part
        except EpicorNotFoundException:
            return None

    @classmethod
    def get_changed(cls, last_modified: datetime, bulk: bool = False) -> List['Part']:
        last_mod_str = last_modified.strftime('%Y-%m-%d')
        filter_string = f'ChangedOn ge {last_mod_str}'
        # if bulk is True:
        #     filter_string += f' or ChangedOn eq null'
        return cls.get_all(params={
            '$filter': filter_string,
            '$top': '99999'
        })

    def create_new_part_rev(self, revision_num: str, comment: str = '',
                            description: str = ''
                            ) -> PartRev:
        """
        Create a new part revision with defaults set
        """
        url = f'{self.base_url}PartRevs'

        if not description:
            description = revision_num
        if isinstance(revision_num, str):
            revision_num = revision_num[0:12]
        data = {
            'PartNum': self.PartNum,
            'RevisionNum': str(revision_num),
            'Company': self.Company,
            "RevShortDesc": str(description),
            'DrawNum': self.PartNum[0:25]
        }
        if comment:
            data['RevDescription'] = comment
        else:
            data['RevDescription'] = str(description)

        create_json = data

        client = EpicorClient.get_instance()
        response_json = client.post_resource(url, create_json)
        # TODO: Parse the result, construct the PartRev from response_json
        rev_json = response_json
        partrev: PartRev = None
        if rev_json:
            partrev = PartRev.from_json(rev_json)
        logger.info(f'Rev Created: {partrev}')
        return partrev

    def get_rev(self, rev_num: str) -> PartRev:
        return PartRev.get(self.Company, self.PartNum, rev_num)


@attr.s
class XRefPart(BaseObject):
    base_url = 'Erp.BO.CustomerPartXRefSvc/'
    resource_name = 'CustomerPartXRefs'

    Company: str = attr.ib(validator=attr.validators.instance_of(str))
    PartNum: str = attr.ib(validator=attr.validators.instance_of(str))  # Actual part master part number
    XPartNum: str = attr.ib(validator=attr.validators.instance_of(str))  # Customer PN/Paperless Parts PN
    CustNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)))  # Actual customer ID (not the user-defined customer number)
    CustNumCustID = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)  # User-defined customer number
    XRevisionNum = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)  # Customer rev/Paperless rev
    # NOTE: The CustNumCustID might be an issue with RCO!
    # They change their customer ids sometimes so this might cause a cluster with the mapping...

    @classmethod
    def get_first_x_ref_part(cls, part_num: str, revision_num: str = None) -> Optional['XRefPart']:
        filter_string = f"XPartNum eq '{part_num}'"
        if revision_num:
            filter_string += f" and XRevisionNum eq '{revision_num}'"
        results: List[XRefPart] = XRefPart.get_with_params(params={'$filter': filter_string})

        if len(results) == 0:
            logger.info(f'{cls.resource_name} with {filter_string} not found')
            return None
        else:
            logger.info(f'Epicor resource {cls.resource_name} with {filter_string} was found!')
            return results[0]


@attr.s
class BasePart(BaseObject):
    base_url = 'Erp.BO.PartSvc/'
    resource_name = 'Parts'
    all_resource_endpoint_suffix = 'List'

    @classmethod
    def construct_get_part_url(cls):
        return f"{cls.base_url}{cls.resource_name}"

    @classmethod
    def construct_get_part_list_url(cls):
        return f"{cls.base_url}{cls.all_resource_endpoint_suffix}"

    @classmethod
    def get_part_by_part_num(cls, PartNum: str, client: EpicorClient = None) -> dict:
        client = client if client else EpicorClient.get_instance()

        get_url: str = cls.construct_get_part_url()
        filter_query: dict = {"$filter": f"PartNum eq {BaseObject.format_query_key(PartNum)}"}

        part_response: list = client.get_resource(get_url, params=filter_query)["value"]
        part = None
        if not part_response:
            logger.info(f"Epicor Part '{PartNum}'does not exist. Skipping.")
            raise EpicorNotFoundException(f"Epicor Part '{PartNum}' does not exist.")
        else:
            part = part_response[0]
        return part

    @classmethod
    def get_new_or_updated_parts_list(cls, query, client: EpicorClient = None):
        client = client if client else EpicorClient.get_instance()
        get_url: str = cls.construct_get_part_url()
        part_ids_list = []
        get_parts_list: list = client.get_resource(get_url, params=query)["value"]
        if not get_parts_list:
            logger.info("No new or updated parts exist for import.")
        else:
            parts_list = get_parts_list
            for part in parts_list:
                part_ids_list.append(part.get("PartNum", None))
        return part_ids_list

    @classmethod
    def construct_query_filter(cls, filter_criteria: Dict[str, Any], should_include_null_dates=True,
                               result_count=100) -> str:  # Dict["odata_field", "value"]
        """Example ODATA filter.
        '(ClassID eq 'MFG' or ClassID eq 'HDW') and (TypeCode eq 'P') and (NonStock eq true')
        """
        filter = []
        individual_eq_str_query = "{id} eq '{value}'"
        individual_eq_bool_query = "{id} eq {value}"
        individual_ge_date_query = "{id} ge {value}"
        for odata_field, field_values in filter_criteria.items():
            if isinstance(field_values, list):
                values = " or ".join(
                    individual_eq_str_query.format(id=odata_field, value=value) for value in field_values)
            elif isinstance(field_values, datetime):
                hours_ago = field_values - timedelta(hours=12)
                to_string = hours_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
                if should_include_null_dates:
                    to_string = to_string + f" or {odata_field} eq null"
                values = individual_ge_date_query.format(id=odata_field, value=to_string)
            elif isinstance(field_values, bool):
                to_string = str(field_values).lower()
                values = individual_eq_bool_query.format(id=odata_field, value=to_string)
            elif isinstance(field_values, str):
                values = individual_eq_str_query.format(id=odata_field, value=field_values)

            enclosing_parenth = f"({values})"
            filter.append(enclosing_parenth)
        full_query = " and ".join(filter)
        return full_query

    @classmethod
    def get_all_part_ids(cls, filter_query: str, client: EpicorClient = None, parts_limit: int = 100_000) -> List[str]:
        """The main Svc endpoint in Epicor API systems is very slow at getting all parts. It is much faster to use
               the List functionality of the Svc endpoint to get all parts. Unfortunately, it doesn't have UnitPrice so will still need
               to be cross referenced with main Svc endpoint, so this will only get partial information."""
        url: str = cls.construct_get_part_list_url()
        client: EpicorClient = client if client else EpicorClient.get_instance()
        api_query: dict = {"$top": parts_limit, "$filter": filter_query}
        parts_response: List[dict] = client.get_resource(url, api_query)
        parts_ids: List[str] = [part["PartNum"] for part in parts_response["value"]]
        return parts_ids


@attr.s
class PurchasedComponentPart(BasePart):
    """
    Purchased Components is a Paperless specific subcategory of Parts. Genearally, ERP systems don't specifically
    state a Part as Purchased Components, it'll generally be based on ClassID, TypeCode, NonStock etc.
    Its up to Paperless to find out from each client how they classify a Part as Purchased Component, and modify
    is_purchased_component if needed.
    """

    @classmethod
    def default_purchased_component_filter(cls):
        criteria = dict(TypeCode=["P"], ClassID=["HDW", "MFG"])
        return cls.construct_query_filter(criteria)

    @classmethod
    def get_all_purchased_component_ids(cls, filter_query: str = None, client: EpicorClient = None) -> List[str]:
        """The main Svc endpoint in Epicor API systems is very slow at getting all parts. It is much faster to use
        the List functionality of the Svc endpoint to get all parts. Unfortunately, it doesn't have UnitPrice so will still need
        to be cross referenced with main Svc endpoint, so this will only get partial information."""
        filter_query = filter_query if filter_query else cls.default_purchased_component_filter()
        return cls.get_all_part_ids(filter_query=filter_query, client=client)


@attr.s
class MaterialPart(BasePart):
    """
    Material is a Paperless specific subcategory of Parts. Genearally, ERP systems don't specifically
    state a Part as Material, it'll generally be based on ClassID, TypeCode, NonStock etc.
    Its up to Paperless to find out from each client how they classify a Part as Material, and modify
    is_material if needed.
    """

    @classmethod
    def default_material_filter(cls):
        criteria = dict(NonStock=True, TypeCode="M")
        return cls.construct_query_filter(criteria)

    @classmethod
    def get_all_material_ids(cls, filter_query: str = None, client: EpicorClient = None) -> List[str]:
        """The main Svc endpoint in Epicor API systems is very slow at getting all parts. It is much faster to use
        the List functionality of the Svc endpoint to get all parts. Unfortunately, it doesn't have UnitPrice so will still need
        to be cross referenced with main Svc endpoint, so this will only get partial information."""
        filter_query = filter_query if filter_query else cls.default_material_filter()
        return cls.get_all_part_ids(filter_query=filter_query, client=client)
