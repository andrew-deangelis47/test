import attr
from typing import List
import json
from baseintegration.datamigration import logger
from acumatica.client import AcumaticaClient
from acumatica.json_encoders.generic import GenericJSONEncoder
DEFAULT_VERSION = '22.200.001'
MANUFACTURING_VERSION = '21.200.001'


def optional_convert(convert):
    """Invoke the subconverter only if the value is present."""

    def optional_converter(val):
        if val is None:
            return None
        else:
            return convert(val)

    return optional_converter


class BaseObject:
    resource_name: str
    base_url: str

    def to_dict(self) -> dict:
        """
        Convert the current object into a dictionary format
        :returns: dict
        """
        return attr.asdict(self, recurse=True)

    _serialization_schema = None

    # TODO: The attrs library could be used here to generate a default serialization schema
    #  if cls is an attrs class. The attrs library has a function to check for that
    @classmethod
    def get_serialization_schema(cls, mode='out'):
        if attr.has(cls) and cls._serialization_schema is None:
            fields_dict = attr.fields_dict(cls)
            return fields_dict
        else:
            return cls._serialization_schema

    """
    Transforms self into a json object as expected to be serialized by the
    Acumatica API.

    :returns: json
    """

    def optional_convert(convert):
        """Invoke the subconverter only if the value is present."""

    def to_json(self):
        schema = self.get_serialization_schema(mode='out')
        if schema is None:
            raise NotImplementedError('_serialization_schema must be defined in derived class')
        return GenericJSONEncoder.encode(self, schema)

    @classmethod
    def from_json(cls, json_dict, encoder_class=GenericJSONEncoder):
        schema = cls.get_serialization_schema(mode='in')
        if schema is None:
            raise NotImplementedError('_serialization_schema must be defined in derived class')
        return encoder_class.decode(cls, json_dict, schema)

    @staticmethod
    def format_query_key(key) -> str:
        """
        Formats a query key to be used in OData filters.
        """
        if isinstance(key, str):
            key_quotes_escaped = "''".join(key.split("'"))  # double each single quote
            return f"'{key_quotes_escaped}'"
        else:
            return key

    @classmethod
    def get_with_params(cls, params: dict = {}):
        client: AcumaticaClient = AcumaticaClient.get_instance()
        resp_json = client.get_resource(f'{cls.base_url}{cls.resource_name}', params=params, identifier=None)
        results = resp_json
        result: List[cls] = [cls.from_json(result, encoder_class=cls.encoder_class if hasattr(cls, "encoder_class") else GenericJSONEncoder) for result in results]
        return result

    @classmethod
    def get_by_id(cls, id, params=None, skip_serializer=False):
        client: AcumaticaClient = AcumaticaClient.get_instance()
        result = None
        try:
            resp_json = client.get_resource(f'{cls.base_url}{cls.resource_name}', identifier=id, params=params)
            results = resp_json
            if skip_serializer:  # pragma: no cover
                return resp_json
            result = cls.from_json(results, encoder_class=cls.encoder_class if hasattr(cls, "encoder_class") else GenericJSONEncoder)
        except Exception as e:
            logger.info(f'Exception occurred for id {id} : {e}')
        return result

    @classmethod
    def get_all(cls, filters: dict = {}, params: dict = {}):
        """
        Returns all entities that match the given filter strings.
        """
        # create equality filters using given dictionary
        filter_strings = []
        for filter_name, value in filters.items():
            if value is None:
                return []
            else:
                filter_strings.append(f'{filter_name} eq {BaseObject.format_query_key(value)}')

        # combine filters into query parameter
        full_filter = ' and '.join(filter_strings)
        if full_filter:
            params['$filter'] = full_filter

        return cls.get_with_params(params)

    @classmethod
    def get_first(cls, filters: dict):
        """
        Returns the first entity that matches the given filters.
        """
        logger.info(f'Searching for resource {cls.resource_name} with {filters}')
        results = cls.get_all(filters)
        if len(results) == 0:
            logger.info(f'Acumatica resource {cls.resource_name} with {filters} not found')
            logger.error(f"Unable to locate {cls.resource_name} object with {filters}")
            raise Exception
        else:
            logger.info(f'Acumatica resource {cls.resource_name} with {filters} was found!')
            return results[0]

    @classmethod
    def get_changed(cls, params: dict) -> List:
        return cls.get_all(params=params)

    @classmethod
    def get_by(cls, field_name: str, value: str):
        return cls.get_first({field_name: value})

    @staticmethod
    def add_value_keys(data: dict):
        filtered_data = {}
        for k, v in data.items():
            if k == 'id' or k == 'custom':
                filtered_data[k] = v
            elif v is not None:
                filtered_data[k] = {'value': v}
        return filtered_data

    @classmethod
    def create(cls, data: dict, skip_keys=False, skip_serializer=False):
        client: AcumaticaClient = AcumaticaClient.get_instance()
        if skip_keys:
            formatted_data = data
        else:
            formatted_data = cls.add_value_keys(data=data)
        json_data = json.dumps(formatted_data)
        resp_json = client.update_resource(resource_url=f'{cls.base_url}{cls.resource_name}',
                                           id=None, data=json_data)
        #  TODO ProductionOrderDetail serializer not working. This is temp workaround.
        if not skip_serializer:
            result: cls = cls.from_json(resp_json)
            return result
        return resp_json

    def create_instance(self):
        return self.create(self.to_dict())

    @classmethod
    def update_resource(cls, data: dict, parameters=None):
        client: AcumaticaClient = AcumaticaClient.get_instance()
        formatted_data = cls.add_value_keys(data)

        if parameters:
            str_parameters = [str(p) for p in parameters]
            formatted_params = f'({",".join(str_parameters)})'
            resp_json = client.update_resource(resource_url=f'{cls.base_url}{cls.resource_name}{formatted_params}', data=json.dumps(formatted_data), id=None)
        else:
            resp_json = client.update_resource(resource_url=f'{cls.base_url}{cls.resource_name}', data=json.dumps(formatted_data), id=None)

        result: cls = cls.from_json(resp_json)
        return result


@attr.s
class Address(BaseObject):
    base_url = f'entity/Default/{DEFAULT_VERSION}/'
    resource_name = 'Address'

    id = attr.ib(validator=attr.validators.instance_of(str))
    AddressLine1 = attr.ib(validator=attr.validators.instance_of(str))
    City = attr.ib(validator=attr.validators.instance_of(str))
    State = attr.ib(validator=attr.validators.instance_of(str))
    Country = attr.ib(validator=attr.validators.instance_of(str))
    PostalCode = attr.ib(validator=attr.validators.instance_of(str))


@attr.s
class Contact(BaseObject):
    base_url = f'entity/Default/{DEFAULT_VERSION}/'
    resource_name = 'Contact'

    ContactID = attr.ib(validator=attr.validators.instance_of(int))
    BusinessAccount = attr.ib(validator=attr.validators.instance_of(str))
    Phone1 = attr.ib(
        converter=optional_convert(str),
        validator=attr.validators.instance_of(str)
    )
    FirstName = attr.ib(validator=attr.validators.instance_of(str), default=None)
    LastName = attr.ib(validator=attr.validators.instance_of(str), default=None)
    Email = attr.ib(validator=attr.validators.instance_of(str), default=None)


@attr.s
class BillingContact(BaseObject):
    base_url = f'entity/Default/{DEFAULT_VERSION}/Customer/'
    resource_name = 'BillingContact'

    id = attr.ib(validator=attr.validators.instance_of(str))
    Address = attr.ib(validator=attr.validators.instance_of(dict))

    def get_address(self) -> [Address, None]:
        #  TODO validate Address has required fields.
        return Address.from_json(json_dict=self.Address)


@attr.s
class ShippingContact(BaseObject):
    base_url = f'entity/Default/{DEFAULT_VERSION}/Customer/'
    resource_name = 'ShippingContact'

    id = attr.ib(validator=attr.validators.instance_of(str))
    Address = attr.ib(validator=attr.validators.instance_of(dict))
    DisplayName = attr.ib(validator=attr.validators.instance_of(str))
    Attention = None  # attr.ib(validator=attr.validators.instance_of(str), default='', converter='')
    FirstName = None  # attr.validators.optional(validator=attr.validators.instance_of(str))
    LastName = None  # attr.validators.optional(validator=attr.validators.instance_of(str))

    def get_address(self) -> [Address, None]:
        #  TODO validate Address has required fields.
        return Address.from_json(json_dict=self.Address)


@attr.s
class LocationContact(BaseObject):
    id = attr.ib(validator=attr.validators.instance_of(str))
    Address = attr.ib(validator=attr.validators.instance_of(dict))
    DisplayName = attr.ib(validator=attr.validators.instance_of(str))


@attr.s
class CustomerLocation(BaseObject):
    base_url = f'entity/Default/{DEFAULT_VERSION}/'
    resource_name = 'CustomerLocation'

    id = attr.ib(validator=attr.validators.instance_of(str))
    LocationContact = attr.ib(validator=attr.validators.instance_of(dict))
    LocationName = attr.ib(validator=attr.validators.instance_of(str))
    LocationID = attr.ib(validator=attr.validators.instance_of(str))

    # Attention = None #attr.ib(validator=attr.validators.instance_of(str), default='', converter='')
    # FirstName = None  #attr.validators.optional(validator=attr.validators.instance_of(str))
    # LastName = None #attr.validators.optional(validator=attr.validators.instance_of(str))

    def get_address(self) -> [Address, None]:
        return Address.from_json(json_dict=self.LocationContact['Address'])
        # shipping_address: Address = customer_location.get_address()


@attr.s
class Customer(BaseObject):
    base_url = f'entity/Default/{DEFAULT_VERSION}/'
    resource_name = 'Customer'

    Contacts = attr.ib(validator=attr.validators.instance_of(list))
    BillingContact = attr.ib(validator=attr.validators.instance_of(dict))
    ShippingContact = attr.ib(validator=attr.validators.instance_of(dict))

    CustomerID = attr.ib(validator=attr.validators.instance_of(str), default=None)
    CustomerName = attr.ib(validator=attr.validators.instance_of(str), default=None)
    CreditLimit = attr.ib(validator=attr.validators.instance_of(float), default=None)
    Terms = attr.ib(validator=attr.validators.instance_of(str), default=None)

    def get_shipping_contact(self) -> ShippingContact:
        return ShippingContact.from_json(json_dict=self.ShippingContact)

    def get_billing_contact(self) -> BillingContact:
        return BillingContact.from_json(json_dict=self.BillingContact)

    def get_contacts(self) -> List[Contact]:
        contact_list = list()
        for contact_json in self.Contacts:
            contact: Contact = Contact.get_by_id(id=contact_json.get('id'))
            contact_list.append(contact)
        return contact_list

    @classmethod
    def get_customer_locations(cls, customer_id) -> [CustomerLocation, None]:
        locations = CustomerLocation.get_all(
            params={'$expand': 'LocationContact/Address'}, filters={'Customer': customer_id}
        )
        return locations

    @classmethod
    def get(cls, cust_id):
        # We need to expand Contacts/Address info here so that we can use the IDs downstream.
        return cls.get_by_id(id=cust_id, params={'$expand': 'Contacts,BillingContact/Address,ShippingContact/Address'})


@attr.s
class CustomerContact(BaseObject):
    base_url = f'entity/Default/{DEFAULT_VERSION}/Customer/Contacts/Contact'
    resource_name = 'Contact'

    CustomerID = attr.ib(validator=attr.validators.instance_of(str))
    CustomerName = attr.ib(validator=attr.validators.instance_of(str))
    CreditLimit = attr.ib(validator=attr.validators.instance_of(float))
    Terms = attr.ib(validator=attr.validators.instance_of(str))


@attr.s
class WorkCenter(BaseObject):
    base_url = f'entity/Manufacturing/{MANUFACTURING_VERSION}/'
    resource_name = 'WorkCenter'

    id = attr.ib(validator=attr.validators.instance_of(str))
    WorkCenterID = attr.ib(validator=attr.validators.instance_of(str))
    Description = attr.ib(validator=attr.validators.instance_of(str), default='', converter=str)
    Location = attr.ib(validator=attr.validators.instance_of(str), default='', converter=str)
    OutsideProcessing = attr.ib(validator=attr.validators.instance_of(str), default='', converter=str)
    StandardCost = attr.ib(validator=attr.validators.instance_of(int), default=0, converter=int)


@attr.s
class Overhead(BaseObject):
    base_url = f'entity/Manufacturing/{MANUFACTURING_VERSION}/'
    resource_name = 'Overhead'

    id = attr.ib(validator=attr.validators.instance_of(str))
    OverheadID = attr.ib(validator=attr.validators.instance_of(str))
    CostRate = attr.ib(validator=attr.validators.instance_of(int))


@attr.s
class ProductionOrder(BaseObject):
    base_url = f'entity/Manufacturing/{MANUFACTURING_VERSION}/'
    resource_name = 'ProductionOrder'

    id = attr.ib(validator=attr.validators.instance_of(str))
    InventoryID = attr.ib(validator=attr.validators.instance_of(str))
    note = attr.ib(validator=attr.validators.instance_of(str))
    Constraint = attr.ib(validator=attr.validators.instance_of(str))
    CostingMethod = attr.ib(validator=attr.validators.instance_of(str))
    Customer = attr.ib(validator=attr.validators.instance_of(str))
    CustomerName = attr.ib(validator=attr.validators.instance_of(str))
    DispatchPriority = attr.ib(validator=attr.validators.instance_of(int))
    EndDate = attr.ib(validator=attr.validators.instance_of(str))
    ExcludefromMRP = attr.ib(validator=attr.validators.instance_of(bool))
    Hold = attr.ib(validator=attr.validators.instance_of(bool))
    Location = attr.ib(validator=attr.validators.instance_of(str))
    OrderDate = attr.ib(validator=attr.validators.instance_of(str))
    OrderType = attr.ib(validator=attr.validators.instance_of(str))
    QtyComplete = attr.ib(validator=attr.validators.instance_of(float))
    QtyRemaining = attr.ib(validator=attr.validators.instance_of(float))
    QtyScrapped = attr.ib(validator=attr.validators.instance_of(float))
    QtytoProduce = attr.ib(validator=attr.validators.instance_of(float))
    RequireParentLotSerialNumber = attr.ib(validator=attr.validators.instance_of(str))
    SchedulingMethod = attr.ib(validator=attr.validators.instance_of(str))
    ScrapOverride = attr.ib(validator=attr.validators.instance_of(bool))
    Source = attr.ib(validator=attr.validators.instance_of(str))
    SourceDate = attr.ib(validator=attr.validators.instance_of(str))
    StartDate = attr.ib(validator=attr.validators.instance_of(str))

    Status = attr.ib(validator=attr.validators.instance_of(str))
    UOM = attr.ib(validator=attr.validators.instance_of(str))
    UpdateProject = attr.ib(validator=attr.validators.instance_of(bool))
    UseFixedMfgLeadTimesforOrderDates = attr.ib(validator=attr.validators.instance_of(bool))
    UseOrderStartDateforMRP = attr.ib(validator=attr.validators.instance_of(bool))  # false
    Warehouse = attr.ib(validator=attr.validators.instance_of(str))  # CMDNY01 or CMDFL

    WIPAccount = attr.ib(validator=attr.validators.instance_of(str))  # 1221
    WIPSubaccount = attr.ib(validator=attr.validators.instance_of(str))  # 000000
    WIPVarianceAccount = attr.ib(validator=attr.validators.instance_of(str))  # 5130
    WIPVarianceSubaccount = attr.ib(validator=attr.validators.instance_of(str))  # 000000

    ParentOrder = attr.ib(
        converter=optional_convert(str),
        validator=attr.validators.instance_of(str)
    )
    ParentOrderType = attr.ib(
        converter=optional_convert(str),
        validator=attr.validators.instance_of(str)
    )
    ProductionNbr = attr.ib(
        converter=optional_convert(str),
        validator=attr.validators.instance_of(str)
    )
    SOLineNbr = attr.ib(
        converter=optional_convert(str),
        validator=attr.validators.instance_of(str)
    )
    SOOrderNbr = attr.ib(
        converter=optional_convert(str),
        validator=attr.validators.instance_of(str)
    )
    SOOrderType = attr.ib(
        converter=optional_convert(str),
        validator=attr.validators.instance_of(str)
    )
    #  ProductionNbr is not optional. Its is auto created by Acumatica. This is defined for downstream processors to
    #  reference autonumbered value


@attr.s
class ProductionOrderDetail(BaseObject):
    base_url = f'entity/Manufacturing/{MANUFACTURING_VERSION}/'
    resource_name = 'ProductionOrderDetail'

    id = attr.ib(validator=attr.validators.instance_of(str))
    note = attr.ib(validator=attr.validators.instance_of(str))  # 12`21
    Hold = attr.ib(validator=attr.validators.instance_of(bool))  # 1221
    InventoryID = attr.ib(validator=attr.validators.instance_of(str))  # 1221
    OrderDate = attr.ib(validator=attr.validators.instance_of(str))  # 1221
    OrderType = attr.ib(validator=attr.validators.instance_of(str))  # 1221
    ProductionNbr = attr.ib(validator=attr.validators.instance_of(str))  # 1221
    Status = attr.ib(validator=attr.validators.instance_of(str))  # 1221
    Warehouse = attr.ib(validator=attr.validators.instance_of(str))  # 1221


@attr.s
class Operation(BaseObject):
    base_url = f'entity/Manufacturing/{MANUFACTURING_VERSION}/'
    resource_name = 'Operation'

    id = attr.ib(validator=attr.validators.instance_of(str))
    note = attr.ib(validator=attr.validators.instance_of(str))
    AtVendorQuantity = attr.ib(validator=attr.validators.instance_of(float))  # 12`2
    BackflushLabor = attr.ib(validator=attr.validators.instance_of(bool))  # 12`21
    DropShippedtoVendor = attr.ib(validator=attr.validators.instance_of(bool))  # 12`21
    FinishTime = attr.ib(validator=attr.validators.instance_of(str))  # 12`21
    MachineTime = attr.ib(validator=attr.validators.instance_of(str))  # 12`21
    MachineUnits = attr.ib(validator=attr.validators.instance_of(str))  # 12`21
    MoveTime = attr.ib(validator=attr.validators.instance_of(str))  # 12`21
    OperationDescription = attr.ib(validator=attr.validators.instance_of(str))  # 12`21
    OperationNbr = attr.ib(validator=attr.validators.instance_of(str))  # 12`21
    OperationStatus = attr.ib(validator=attr.validators.instance_of(str))  # 12`21
    OutsideProcess = attr.ib(validator=attr.validators.instance_of(bool))   # 12`21

    # Ignoring phantom bom for now

    QtyComplete = attr.ib(validator=attr.validators.instance_of(float))  # 12`21
    QtyRemaining = attr.ib(validator=attr.validators.instance_of(float))  # 12`21
    QtyScrapped = attr.ib(validator=attr.validators.instance_of(float))  # 12`21
    QtytoProduce = attr.ib(validator=attr.validators.instance_of(float))  # 12`21
    QueueTime = attr.ib(validator=attr.validators.instance_of(str))  # 12`21
    RunTime = attr.ib(validator=attr.validators.instance_of(str))  # 12`21
    RunUnits = attr.ib(validator=attr.validators.instance_of(float))  # 12`21
    ScrapAction = attr.ib(validator=attr.validators.instance_of(str))  # 12`21
    SetupTime = attr.ib(validator=attr.validators.instance_of(str))  # 12`21
    ShippedQuantity = attr.ib(validator=attr.validators.instance_of(float))  # 12`21
    ShipRemainingQty = attr.ib(validator=attr.validators.instance_of(float))  # 12`21
    TotalQty = attr.ib(validator=attr.validators.instance_of(float))  # 12`21
    WorkCenter = attr.ib(validator=attr.validators.instance_of(str))  # 12`21


@attr.s
class Material(BaseObject):
    base_url = f'entity/Manufacturing/{MANUFACTURING_VERSION}/'
    resource_name = 'Material'

    id = attr.ib(validator=attr.validators.instance_of(str))
    BatchSize = attr.ib(validator=attr.validators.instance_of(float))
    Byproduct = attr.ib(validator=attr.validators.instance_of(bool))
    Description = attr.ib(validator=attr.validators.instance_of(str))
    InventoryID = attr.ib(validator=attr.validators.instance_of(str))
    LineNbr = attr.ib(validator=attr.validators.instance_of(int))
    LineOrder = attr.ib(validator=attr.validators.instance_of(int))
    MarkforPO = attr.ib(validator=attr.validators.instance_of(bool))
    MarkforProduction = attr.ib(validator=attr.validators.instance_of(bool))
    MaterialType = attr.ib(validator=attr.validators.instance_of(str))
    OperationNbr = attr.ib(validator=attr.validators.instance_of(str))
    PlannedCost = attr.ib(validator=attr.validators.instance_of(float))
    QtyActual = attr.ib(validator=attr.validators.instance_of(float))
    QtyRemaining = attr.ib(validator=attr.validators.instance_of(float))
    QtyRequired = attr.ib(validator=attr.validators.instance_of(float))
    QtyRoundUp = attr.ib(validator=attr.validators.instance_of(bool))
    ScrapFactor = attr.ib(validator=attr.validators.instance_of(float))
    SubcontractSource = attr.ib(validator=attr.validators.instance_of(str))
    TotalActualCost = attr.ib(validator=attr.validators.instance_of(float))
    TotalRequired = attr.ib(validator=attr.validators.instance_of(float))
    UnitCost = attr.ib(validator=attr.validators.instance_of(float))
    UOM = attr.ib(validator=attr.validators.instance_of(str))
    Warehouse = attr.ib(validator=attr.validators.instance_of(str))
    WarehouseOverride = attr.ib(validator=attr.validators.instance_of(bool))

    '''
        {
                    "note": {
                        "value": ""
                    },
                    "BatchSize": {
                        "value": 1.000000
                    },
                    "Byproduct": {
                        "value": false
                    },
                    "CompBOMEffDate": {},
                    "CompBOMID": {},
                    "CompBOMRevision": {},
                    "Description": {
                        "value": "PULLEY, S3, SIDEGRIP (M002488)"
                    },
                    "InventoryID": {
                        "value": "24208820"
                    },
                    "LineNbr": {
                        "value": 1
                    },
                    "LineOrder": {
                        "value": 1
                    },
                    "Location": {},
                    "MarkforPO": {
                        "value": false
                    },
                    "MarkforProduction": {
                        "value": false
                    },
                    "MaterialType": {
                        "value": "Regular"
                    },
                    "OperationNbr": {
                        "value": "0010"
                    },
                    "PlannedCost": {
                        "value": 0.00
                    },
                    "QtyActual": {
                        "value": 0.000000
                    },
                    "QtyRemaining": {
                        "value": 100.0000
                    },
                    "QtyRequired": {
                        "value": 1.000000
                    },
                    "QtyRoundUp": {
                        "value": false
                    },
                    "ScrapFactor": {
                        "value": 0.000000
                    },
                    "SubcontractSource": {
                        "value": "None"
                    },
                    "TotalActualCost": {
                        "value": 0.000000
                    },
                    "TotalRequired": {
                        "value": 100.000000
                    },
                    "UnitCost": {
                        "value": 0.000000
                    },
                    "UOM": {
                        "value": "EA"
                    },
                    "Warehouse": {
                        "value": "CMDNY01"
                    },
                    "WarehouseOverride": {
                        "value": false
                    }
                }
   '''


@attr.s
class Vendor(BaseObject):
    base_url = f'entity/Default/{DEFAULT_VERSION}/'
    resource_name = 'Vendor'

    VendorID = attr.ib(validator=attr.validators.instance_of(str))
    VendorName = attr.ib(validator=attr.validators.instance_of(str))
    VendorClass = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(str)))


@attr.s
class StockItem(BaseObject):
    base_url = f'entity/Default/{DEFAULT_VERSION}/'
    resource_name = 'StockItem'

    id = attr.ib(validator=attr.validators.instance_of(str))
    InventoryID = attr.ib(validator=attr.validators.instance_of(str))
    DefaultPrice = attr.ib(
        converter=optional_convert(float),
        validator=attr.validators.instance_of(float)
    )
    CurySpecificPrice = attr.ib(
        converter=optional_convert(float),
        validator=attr.validators.instance_of(float)
    )
    Description = attr.ib(
        converter=optional_convert(str),
        validator=attr.validators.instance_of(str)
    )
    LastCost = attr.ib(
        converter=optional_convert(float),
        validator=attr.validators.instance_of(float)
    )
    AverageCost = attr.ib(
        converter=optional_convert(float),
        validator=attr.validators.instance_of(float)
    )
    LastModified = attr.ib(
        converter=optional_convert(str),
        validator=attr.validators.instance_of(str)
    )
    ItemClass = attr.ib(validator=attr.validators.instance_of(str))
    ItemType = attr.ib(validator=attr.validators.instance_of(str))
    ItemStatus = attr.ib(validator=attr.validators.instance_of(str))
    DefaultWarehouseID = attr.ib(
        converter=optional_convert(str),
        validator=attr.validators.instance_of(str)
    )
    LotSerialClass = attr.ib(validator=attr.validators.instance_of(str))
    PostingClass = attr.ib(validator=attr.validators.instance_of(str))
    PurchaseUOM = attr.ib(validator=attr.validators.instance_of(str))
    SalesUOM = attr.ib(validator=attr.validators.instance_of(str))
    VendorDetails: List[Vendor] = attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(
        member_validator=attr.validators.instance_of(Vendor),
        iterable_validator=attr.validators.instance_of(list),
    )), factory=Vendor)


@attr.s
class SalesOrderHeader(BaseObject):
    base_url = f'entity/Default/{DEFAULT_VERSION}/'
    resource_name = 'SalesOrder'

    id = attr.ib(validator=attr.validators.instance_of(str))
    CustomerID = attr.ib(validator=attr.validators.instance_of(str))
    OrderType = attr.ib(validator=attr.validators.instance_of(str))
    CustomerOrder = attr.ib(validator=attr.validators.instance_of(str))
    ContactID = attr.ib(validator=attr.validators.instance_of(str))
    ShipToAddressID = attr.ib(
        converter=optional_convert(str),
        validator=attr.validators.instance_of(str)
    )
    BillToAddressID = attr.ib(
        converter=optional_convert(str),
        validator=attr.validators.instance_of(str)
    )
    RequestedOn = attr.ib(validator=attr.validators.instance_of(str))

    Details = attr.ib(
        converter=optional_convert(list),
        validator=attr.validators.instance_of(list)
    )

    custom = attr.ib(
        converter=optional_convert(dict),
        validator=attr.validators.instance_of(dict)
    )
    #  Owner = attr.ib(validator=attr.validators.instance_of(str)) # Figure this out with cmfg
    #  CustomAttr = attr.ib(validator=attr.validators.instance_of(str)) # custom by copius, maps to estimator


@attr.s
class SalesOrderDetail(BaseObject):
    base_url = f'entity/Default/{DEFAULT_VERSION}/'
    resource_name = 'SalesOrder'

    LineNbr = attr.ib(validator=attr.validators.instance_of(int))
    InventoryID = attr.ib(validator=attr.validators.instance_of(str))
    LineType = attr.ib(validator=attr.validators.instance_of(str))
    UnitPrice = attr.ib(validator=attr.validators.instance_of(float))
    OrderQty = attr.ib(validator=attr.validators.instance_of(float))


@attr.s
class NonStockItem(BaseObject):
    base_url = f'entity/Default/{DEFAULT_VERSION}/'
    resource_name = 'NonStockItem'

    id = attr.ib(validator=attr.validators.instance_of(str))
    InventoryID = attr.ib(validator=attr.validators.instance_of(str))
    Description = attr.ib(
        converter=optional_convert(str),
        validator=attr.validators.instance_of(str)
    )
    LastCost = attr.ib(
        converter=optional_convert(float),
        validator=attr.validators.instance_of(float)
    )
    LastModifiedDateTime = attr.ib(
        converter=optional_convert(str),
        validator=attr.validators.instance_of(str)
    )
    ItemClass = attr.ib(validator=attr.validators.instance_of(str))
    ItemType = attr.ib(validator=attr.validators.instance_of(str))
    ItemStatus = attr.ib(validator=attr.validators.instance_of(str))
    VendorDetails = None

    @classmethod
    def get(cls, id):
        #  We need to expand Contacts/Address info here so that we can use the IDs downstream.
        return cls.get_by_id(id=id, params={'$expand': 'VendorDetails'})
