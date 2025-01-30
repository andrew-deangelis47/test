import attr
from attr.validators import optional, instance_of
from plex_v2.json_encoders.generic import FlatMapJSONEncoder
from plex_v2.client import PlexClient
from baseintegration.integration.erp_error_message_converter import ERPErrorMessageConverter, ConvertedErrorException
from plex_v2.exceptions import PlexRequestProcessingErrorException
from baseintegration.datamigration import logger
import json


class JSONSerializable(object):
    def serialize(self):
        raise NotImplementedError("serialize needs to be implemented")

    @classmethod
    def deserialize(cls, obj):
        raise NotImplementedError("deserialize needs to be implemented")


@attr.s(kw_only=True)
class BaseObject(object):
    id = attr.ib(validator=optional(instance_of(str)), default=None)

    def is_created(self):
        return self.id is not None

    def get_id(self):
        return self.id


class FlatJSONMixin(JSONSerializable):
    @classmethod
    def get_serialization_schema(cls, mode):
        if attr.has(cls):
            fields_dict = attr.fields_dict(cls)
            return {x: x for x in fields_dict}

    """
    Transforms self into a json object as expected to be serialized by the Plex API.

    :returns: json
    """

    def to_json(self):
        schema = self.get_serialization_schema(mode='out')
        if schema is None:
            raise ValueError('get_serialization_schema must not return None')
        return FlatMapJSONEncoder.encode(self, schema)

    @classmethod
    def from_json(cls, json_dict):
        schema = cls.get_serialization_schema(mode='in')
        if schema is None:
            raise ValueError('get_serialization_schema must not return None')
        return FlatMapJSONEncoder.decode(cls, json_dict, schema)

    def serialize(self):
        return self.to_json()

    @classmethod
    def deserialize(cls, obj):
        return cls.from_json(obj)


class BaseActionMixin(FlatJSONMixin):
    _resource_name = None

    @classmethod
    def get_resource_name(cls, action, instance=None, **kwargs):
        return cls._resource_name

    @classmethod
    def _get_client(cls):
        return PlexClient.get_instance()

    @classmethod
    def _get_error_message_converter(cls):
        return ERPErrorMessageConverter.get_instance()

    @classmethod
    def get_paperless_error_message(cls, erp_error_message: str):
        converter: ERPErrorMessageConverter = cls._get_error_message_converter()
        if converter is None:
            return None
        return converter.get_clean_message(erp_error_message)


class InstanceActionMixin(BaseActionMixin):
    def get_id(self):
        raise NotImplementedError('get_id must be implemented in derived class')


class CreateMixin(BaseActionMixin):
    def create(self, in_place=True, resource_name_kwargs=None):
        logger.info('-------------------------------')
        logger.info(f'Creating {str(type(self).__name__)} object in Plex')
        schema = self.get_serialization_schema(mode='out')
        for key, value in vars(self).items():
            if key == 'id' or value is None or key not in schema:
                continue
            logger.info(f'{key}: {value}')
        logger.info('-------------------------------\n')

        if resource_name_kwargs is None:
            resource_name_kwargs = {}

        resource_name = self.get_resource_name('create', instance=self, **resource_name_kwargs)
        # handling an API error message
        try:
            created_object = self.deserialize(
                self._get_client().create_resource(
                    resource_name,
                    self.serialize()
                )
            )
        # catch the 500 errors - error message is created in the client
        except PlexRequestProcessingErrorException as e:
            raise ConvertedErrorException(str(e))

        except Exception as e:
            paperless_error_message = self.get_paperless_error_message(str(e))
            if paperless_error_message is None:
                raise e
            raise ConvertedErrorException(paperless_error_message)

        schema_keyset = set(self.get_serialization_schema('in').keys())
        fields_keyset = set(attr.fields_dict(self.__class__).keys())
        if in_place:
            for field_name in schema_keyset:
                setattr(self, field_name, getattr(created_object, field_name, None))
        for field_name in fields_keyset - schema_keyset:
            setattr(created_object, field_name, getattr(self, field_name, None))

        logger.info('\n')
        return created_object


class RetrieveDataSourceMixin(BaseActionMixin):

    @classmethod
    def get_resource_name(cls):
        return cls._resource_name

    @classmethod
    def get_serialization_schema(cls, mode):
        if mode == 'in':
            base_schema = super().get_serialization_schema(mode)
            del base_schema['id']
            return base_schema
        else:
            raise NotImplementedError(f'get_serialization_schema not implemented for "out" in {cls.__name__}')

    @classmethod
    def deserialize(cls, json_dict: dict):
        columns = json_dict['tables'][0]['columns']
        rows = json_dict['tables'][0]['rows']

        schema = cls.get_serialization_schema(mode='in')

        objects = []
        for row in rows:
            kwargs = {}
            for column in columns:
                if column in schema:
                    kwargs[column] = row[columns.index(column)]

            objects.append(cls(**kwargs))

        return objects

    @classmethod
    def serialize(cls, dictionary: dict) -> str:
        body = {"inputs": {}}
        body["inputs"] = dictionary

        return json.dumps(body)

    @classmethod
    def datasource_get(cls, body: dict):
        logger.info(f'Fetching data using {str(cls.__name__)} datasource in Plex')
        for key, value in body.items():
            logger.info(f'{key}: {value}')

        # handling an API error message]
        try:
            response_objects = cls.deserialize(
                cls._get_client().create_resource(
                    cls.get_resource_name(),
                    cls.serialize(body),
                    True
                )
            )
        # catch the 500 errors - error message is created in the client
        except PlexRequestProcessingErrorException as e:
            raise ConvertedErrorException(str(e))

        except Exception as e:
            paperless_error_message = cls.get_paperless_error_message(str(e))
            if paperless_error_message is None:
                raise e
            raise ConvertedErrorException(paperless_error_message)

        logger.info('\n')

        return response_objects


class CreateDatasourceMixin(BaseActionMixin):

    def get_resource_name(cls):
        return cls._resource_name

    def serialize(self):
        # create the body, only including attributes that are not None
        inputs = {}
        for attribute_name, value in vars(self).items():
            if value is not None and value != "":
                inputs[f'{attribute_name}'] = value

        body = {"inputs": inputs}
        return json.dumps(body)

    def create(self, in_place=True, resource_name_kwargs=None):
        logger.info('-------------------------------')
        logger.info(f'Creating {str(type(self).__name__)} object in Plex')
        for key, value in vars(self).items():
            if key == 'id' or value is None:
                continue
            logger.info(f'{key}: {value}')
        logger.info('-------------------------------\n')

        if resource_name_kwargs is None:
            resource_name_kwargs = {}

        resource_name = self.get_resource_name()
        # handling an API error message
        try:
            self.deserialize(
                self._get_client().create_resource(
                    resource_name,
                    self.serialize(),
                    True
                )
            )
        # catch the 500 errors - error message is created in the client
        except PlexRequestProcessingErrorException as e:
            raise ConvertedErrorException(str(e))

        except Exception as e:
            paperless_error_message = self.get_paperless_error_message(str(e))
            if paperless_error_message is None:
                raise e
            raise ConvertedErrorException(paperless_error_message)

        logger.info('\n')


class RetrieveMixin(BaseActionMixin):
    @classmethod
    def get(cls, id_, resource_name_kwargs=None):
        logger.info(f'Getting resource {cls.__name__}')
        if resource_name_kwargs is None:
            resource_name_kwargs = {}
        resource_name = cls.get_resource_name('get', **resource_name_kwargs)
        try:
            return cls.deserialize(
                cls._get_client().get_resource(resource_name, id_)
            )

        # catch the 500 errors - error message is created in the client
        except PlexRequestProcessingErrorException as e:
            raise ConvertedErrorException(str(e))

        except Exception as e:
            logger.error('In the normal exception block')
            paperless_error_message = cls.get_paperless_error_message(str(e))
            if paperless_error_message is None:
                raise e
            raise ConvertedErrorException(paperless_error_message)

        logger.info('\n')


class SearchMixin(BaseActionMixin):
    @classmethod
    def search(cls, resource_name_kwargs=None, exclude_if_null=None, **kwargs):
        logger.info(f'Getting resource {cls.__name__}')
        if resource_name_kwargs is None:
            resource_name_kwargs = {}
        if exclude_if_null is None:
            exclude_if_null = []
        client = cls._get_client()

        resource_name = cls.get_resource_name('search', **resource_name_kwargs)
        try:
            resource_data_list = client.get_resource_list(
                resource_name,
                params={k: kwargs[k] for k in kwargs if k not in exclude_if_null or kwargs[k] is not None}
            )
            out = []
            for obj in resource_data_list:
                out.append(cls.deserialize(obj))

        # catch the 500 errors - error message is created in the client
        except PlexRequestProcessingErrorException as e:
            raise ConvertedErrorException(str(e))

        except Exception as e:
            logger.error('In the normal exception block')
            paperless_error_message = cls.get_paperless_error_message(str(e))
            if paperless_error_message is None:
                raise e
            raise ConvertedErrorException(paperless_error_message)

        logger.info('\n')
        return out
