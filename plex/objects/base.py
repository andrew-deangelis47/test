import attr
from attr.validators import optional, instance_of
from plex.json_encoders.generic import FlatMapJSONEncoder
from plex.client import PlexClient


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


class InstanceActionMixin(BaseActionMixin):
    def get_id(self):
        raise NotImplementedError('get_id must be implemented in derived class')


class CreateMixin(BaseActionMixin):
    def create(self, in_place=True, resource_name_kwargs=None):
        if resource_name_kwargs is None:
            resource_name_kwargs = {}
        created_object = self.deserialize(
            self._get_client().create_resource(
                self.get_resource_name('create', instance=self, **resource_name_kwargs),
                self.serialize()
            )
        )
        schema_keyset = set(self.get_serialization_schema('in').keys())
        fields_keyset = set(attr.fields_dict(self.__class__).keys())
        if in_place:
            for field_name in schema_keyset:
                setattr(self, field_name, getattr(created_object, field_name, None))
        for field_name in fields_keyset - schema_keyset:
            setattr(created_object, field_name, getattr(self, field_name, None))
        return created_object


class RetrieveMixin(BaseActionMixin):
    @classmethod
    def get(cls, id_, resource_name_kwargs=None):
        if resource_name_kwargs is None:
            resource_name_kwargs = {}
        return cls.deserialize(
            cls._get_client().get_resource(cls.get_resource_name('get', **resource_name_kwargs), id_)
        )


class UpdateMixin(InstanceActionMixin):
    def update(self, resource_name_kwargs=None):
        if resource_name_kwargs is None:
            resource_name_kwargs = {}
        return self.deserialize(
            self._get_client().update_resource(
                self.get_resource_name('update', instance=self, **resource_name_kwargs),
                self.get_id(),
                self.serialize(),
            )
        )


class SearchMixin(BaseActionMixin):
    @classmethod
    def search(cls, resource_name_kwargs=None, exclude_if_null=None, **kwargs):
        if resource_name_kwargs is None:
            resource_name_kwargs = {}
        if exclude_if_null is None:
            exclude_if_null = []
        client = cls._get_client()
        resource_data_list = client.get_resource_list(
            cls.get_resource_name('search', **resource_name_kwargs),
            params={k: kwargs[k] for k in kwargs if k not in exclude_if_null or kwargs[k] is not None}
        )
        out = []
        for obj in resource_data_list:
            out.append(cls.deserialize(obj))

        return out
