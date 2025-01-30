from datetime import datetime, timedelta
from typing import List, Dict, Any
import attr
from baseintegration.datamigration import logger
from epicor.client import EpicorClient
from epicor.exceptions import EpicorNotFoundException
from epicor.json_encoders.generic import GenericJSONEncoder
from epicor.exceptions import EpicorException
from baseintegration.integration.erp_error_message_converter import ERPErrorMessageConverter
from baseintegration.integration.erp_error_message_converter import ConvertedErrorException


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
        # print(f'get_serialzation_schema: {cls._serialization_schema}')
        if attr.has(cls) and cls._serialization_schema is None:
            fields_dict = attr.fields_dict(cls)
            return fields_dict
        else:
            return cls._serialization_schema

    """
    Transforms self into a json object as expected to be serialized by the
    Epicor API.

    :returns: json
    """
    def to_json(self):
        schema = self.get_serialization_schema(mode='out')
        if schema is None:
            raise NotImplementedError('_serialization_schema must be defined in derived class')
        return GenericJSONEncoder.encode(self, schema)

    @classmethod
    def from_json(cls, json_dict, encoder_class=GenericJSONEncoder):
        schema = cls.get_serialization_schema(mode='in')
        # print(f'schema: {schema}')
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
        client: EpicorClient = EpicorClient.get_instance()
        resp_json = client.get_resource(f'{cls.base_url}{cls.resource_name}', params=params)
        results = resp_json["value"]
        result: List[cls] = [cls.from_json(result, encoder_class=cls.encoder_class if hasattr(cls, "encoder_class") else GenericJSONEncoder) for result in results]
        return result

    @classmethod
    def get_all(cls, filters: dict = {}, params: dict = None):
        """
        Returns all entities that match the given filter strings.
        """
        # create equality filters using given dictionary
        if params is None:
            params = {}
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
    def get_first(cls, filters: dict, params: dict = None):
        """
        Returns the first entity that matches the given filters.
        """
        logger.info(f'Searching for resource {cls.resource_name} with {filters}')
        results = cls.get_all(filters, params)
        if len(results) == 0:
            logger.info(f'Epicor resource {cls.resource_name} with {filters} not found')
            raise EpicorNotFoundException(
                message=f"Unable to locate {cls.resource_name} object with {filters}"
            )
        else:
            logger.info(f'Epicor resource {cls.resource_name} with {filters} was found!')
            return results[0]

    @classmethod
    def get_changed(cls, last_modified: datetime) -> List:
        last_mod_str = last_modified.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return cls.get_all(params={
            '$filter': f'ChangeDate ge {last_mod_str}',
            '$top': '99999'
        })

    @classmethod
    def get_by(cls, field_name: str, value: str, params: dict = None):
        return cls.get_first({field_name: value}, params)

    @staticmethod
    def remove_none_values(data: dict):
        filtered_data = {}
        for k, v in data.items():
            if v is not None:
                filtered_data[k] = v
        return filtered_data

    @classmethod
    def create(cls, data: dict):
        client: EpicorClient = EpicorClient.get_instance()

        filtered_data = cls.remove_none_values(data)

        try:
            resp_json = client.post_resource(f'{cls.base_url}{cls.resource_name}', filtered_data)
        except EpicorException as e:
            paperless_error_message = cls.get_paperless_error_message(str(e))
            if paperless_error_message is None:
                raise e

            # we could add some more contextual information for some specific errors
            raise ConvertedErrorException(cls.get_contextual_error_message_for_model_if_possible(paperless_error_message, data))

        result: cls = cls.from_json(resp_json)
        return result

    def create_instance(self):
        return self.create(self.to_dict())

    @classmethod
    def update_resource(cls, parameters: list, data: dict):
        client: EpicorClient = EpicorClient.get_instance()

        filtered_data = cls.remove_none_values(data)

        str_parameters = [str(p) for p in parameters]
        formatted_params = f'({",".join(str_parameters)})'

        client.patch_resource(f'{cls.base_url}{cls.resource_name}{formatted_params}', filtered_data)

    @classmethod
    def construct_query_filter(cls, filter_criteria: Dict[str, Any], should_include_null_dates=True,
                               result_count=100) -> str:  # Dict["odata_field", "value"]
        """Example ODATA filter.
        '(ClassID eq 'MFG' or ClassID eq 'HDW') and (TypeCode eq 'P') and (NonStock eq true')
        """
        filter = []
        values = ''
        individual_eq_str_query = "{id} eq '{value}'"
        individual_eq_bool_query = "{id} eq {value}"
        individual_ge_date_query = "{id} ge {value}"
        for odata_field, field_values in filter_criteria.items():
            if isinstance(field_values, list):
                values = " or ".join(
                    individual_eq_str_query.format(id=odata_field, value=value) for value in field_values)
            elif isinstance(field_values, datetime):
                hours_ago = field_values - timedelta(hours=12)
                to_string = hours_ago.strftime("%Y-%m-%d")
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
    def get_paginated_results_with_params(cls, params: dict = {}, page_size: int = 10):
        client: EpicorClient = EpicorClient.get_instance()
        results_list: List[cls] = []
        params["$top"] = page_size
        params["$skip"] = 0
        terminate_loop = False

        if "$filter" in params.keys() and params["$filter"] in (None, '', ' '):
            terminate_loop = True

        while terminate_loop is False:
            results = []
            try:
                resp_json = client.get_resource(f'{cls.base_url}{cls.resource_name}', params=params)
                results = resp_json["value"]
                for result in results:
                    results_list.append(cls.from_json(result, encoder_class=cls.encoder_class if hasattr(cls, "encoder_class") else GenericJSONEncoder))
            except EpicorException as e:
                logger.info(f"Could not execute API call. Returning empty list. Error below:\n{e}")

            params["$skip"] += page_size
            if len(results) < page_size:
                terminate_loop = True
        return results_list

    @classmethod
    def get_response_json_value(cls, params: dict = {}):
        client: EpicorClient = EpicorClient.get_instance()
        if params["$filter"] in (None, '', ' '):
            return []
        else:
            try:
                resp_json = client.get_resource(f'{cls.base_url}{cls.resource_name}', params=params)
                results = resp_json["value"]
                return results
            except EpicorException as e:
                logger.info(f"Could not execute API call. Returning empty list. Error below:\n{e}")
        return []

    @classmethod
    def _get_error_message_converter(cls):
        return ERPErrorMessageConverter.get_instance()

    @classmethod
    def get_paperless_error_message(cls, erp_error_message: str):
        converter: ERPErrorMessageConverter = cls._get_error_message_converter()
        if converter is None:
            return None
        return converter.get_clean_message(erp_error_message)

    @classmethod
    def get_contextual_error_message_for_model_if_possible(cls, converted_error_message: str, object_data: dict) -> str:
        """
        - for some models there are specific errors that we can provide more information about, in addition to the
          error mapping yaml message,
        - this is optional to setup for any model
        - see part model for example (on create function)
        - if not implemented for a model it will just return the supplied error message
        """
        return converted_error_message
