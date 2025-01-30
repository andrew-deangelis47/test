from datetime import datetime
from typing import List

import attr

from dynamics.client import DynamicsClient
from dynamics.exceptions import DynamicsNotFoundException, DynamicsException
from dynamics.json_encoders.generic import GenericJSONEncoder

from baseintegration.exporter.order_exporter import logger

str_type = {'validator': attr.validators.instance_of(str)}
num_type = {'validator': attr.validators.instance_of(tuple([int, float]))}
bool_type = {'validator': attr.validators.instance_of(bool)}


class BaseObject(object):

    resource_name = None  # name of resource in URL

    @classmethod
    def get_serialization_schema(cls):
        return attr.fields_dict(cls)

    """
    Transforms self into a json object as expected to be serialized by the Plex API.

    :returns: json
    """
    def to_json(self):
        schema = self.get_serialization_schema()
        return GenericJSONEncoder.encode(self, schema)

    @classmethod
    def from_json(cls, json_dict):
        schema = cls.get_serialization_schema()
        return GenericJSONEncoder.decode(cls, json_dict, schema)

    @classmethod
    def finalize(cls, data: dict):
        finalized: cls = cls.from_json(data)
        return finalized

    @classmethod
    def create(cls, data: dict):
        """
        Create an entity based on the data loaded on the object.
        @return: returns self
        """
        client: DynamicsClient = DynamicsClient.get_instance()

        logger.info(f'Creating Dynamics resource {cls.resource_name} with {data}')

        # try each creation a few times; the API is a bit flaky
        num_attempts = 5
        for i in range(num_attempts):
            try:
                resp_json = client.post_resource(cls.resource_name, data)
                return cls.finalize(resp_json)
            except DynamicsException as e:
                if i >= num_attempts - 1:
                    raise e

    @classmethod
    def get_with_filter_strings(cls, filter_strings: List[str]):
        """
        Returns all entities that match the given filter strings.
        """
        client: DynamicsClient = DynamicsClient.get_instance()

        params = {}

        # combine filters into query parameter
        full_filter = ' and '.join(filter_strings)
        if full_filter:
            params['$filter'] = full_filter

        resp_json = client.get_resource(cls.resource_name, params=params)
        results = resp_json["value"]
        result_objects: List[cls] = [cls.finalize(result) for result in results]
        return result_objects

    @classmethod
    def get_all(cls, filters: dict = {}):
        """
        Returns all entities that match the given filters.
        """
        filter_strings = []
        for filter_name, value in filters.items():
            if value is None:
                empty_list: List[cls] = []
                return empty_list
            else:
                filter_strings.append(f'{filter_name} eq {DynamicsClient.format_query_key(value)}')
        return cls.get_with_filter_strings(filter_strings)

    @classmethod
    def get_first(cls, filters: dict):
        """
        Returns the first entity that matches the given filters.
        """
        logger.info(f'Searching for Dynamics resource {cls.resource_name} with {filters}')
        results = cls.get_all(filters)
        if len(results) == 0:
            logger.info(f'Dynamics resource {cls.resource_name} with {filters} not found')
            raise DynamicsNotFoundException(f'Entity of type {cls.resource_name} with {filters} not found.')
        else:
            logger.info(f'Dynamics resource {cls.resource_name} with {filters} was found!')
            return results[0]

    @classmethod
    def get_or_create(cls, filters, data: dict = {}):
        """
        Returns the first entity that matches the given filters; if not found, creates a new entity.
        """
        try:
            return cls.get_first(filters)
        except DynamicsNotFoundException:
            return cls.create({
                **filters,
                **data
            })

    @classmethod
    def get_all_modified_after(cls, date: datetime):
        date_string = date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return cls.get_with_filter_strings([
            f'Last_DateTime_Modified gt {date_string}'
        ])

    @classmethod
    def update(cls, identifier, data={}):
        """
        Updates an entity based on the data loaded on the object.
        @return: returns self
        """
        client: DynamicsClient = DynamicsClient.get_instance()

        identifier_list = identifier if isinstance(identifier, list) else [identifier]
        formatted_id_list = [DynamicsClient.format_query_key(identifier) for identifier in identifier_list]
        joined_id_list = ', '.join(formatted_id_list)

        logger.info(f'Updating Dynamics resource {cls.resource_name} with id {identifier} with {data}')

        url = f'{cls.resource_name}({joined_id_list})'

        # first we must send a GET to get the E-Tag used for the PATCH
        get_resp = client.get_resource(url)
        e_tag = get_resp['@odata.etag']

        headers = {
            'If-Match': e_tag
        }
        resp_json = client.patch_resource(url, data, headers=headers)
        return cls.finalize(resp_json)
