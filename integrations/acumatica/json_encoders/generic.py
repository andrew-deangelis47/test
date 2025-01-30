from attr import Factory


class GenericJSONEncoder:

    @classmethod
    def decode(cls, resource_cls, json_dict: dict, schema):
        """
        This decoding method allows one level deep of nested decoding when the factory is specified on deep iterables
        If deeper decoding is needed, rewrite this recursively to decode values using their factory class
        """
        kwargs = {}
        for field in schema:
            if type(schema[field].default) is Factory:
                factory = schema[field].default.factory
                new_schema = factory.get_serialization_schema(mode='in')
                kwargs[field] = []
                if field in json_dict:
                    for item in json_dict[field]:
                        args = {}
                        for sub_field in new_schema:
                            if isinstance(item.get(sub_field), dict):
                                args[sub_field] = item[sub_field].get('value')
                        kwargs[field].append(factory(**args))
            elif field in json_dict:
                data = json_dict[field]
                if isinstance(data, dict):
                    if 'value' in data.keys():
                        data = data.get('value')
                    elif field == 'LocationName':  # Breaks for facilities without a name, at the model level
                        data = ""
                    elif not data:
                        data = ""
                kwargs[field] = data
        return resource_cls(**kwargs)
