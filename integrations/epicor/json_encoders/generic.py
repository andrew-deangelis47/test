from decimal import Decimal


class GenericJSONEncoder:

    @classmethod
    def decode(cls, resource_cls, json_dict: dict, schema):
        kwargs = {}

        for field in schema:
            # if isinstance(field, str):
            kwargs[field] = json_dict[field] if field in json_dict else None
            # elif isinstance(field, tuple): if len(field) != 2: raise
            # ValueError('Invalid schema: tuple length must be 2') kwargs[
            # field[0]] = cls.decode(getattr(resource, field[0], None),
            # field[1]) TODO: Implement me if needed it looks like all of
            #  the Plex API schemas are flat, so adding this extra
            #  functionality may not be necessary. pass else: raise
            #  ValueError('Unrecognized field in schema')
        return resource_cls(**kwargs)


class NewGenericJsonEncoder:

    @classmethod
    def decode(cls, resource_cls, json_dict: dict, schema):
        kwargs = {}

        for field in schema:
            value = json_dict.get(field)
            if isinstance(value, Decimal):
                value = float(value)

            kwargs[field] = value

        return resource_cls(**kwargs)
