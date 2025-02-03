import simplejson as json
from typing import Union
import decimal


class GenericJSONEncoder:
    @classmethod
    def encode(cls, resource, schema, json_dumps=True) -> Union[dict, str]:
        """
        Schema data definition:

        a Schema is a list of Union(str, Tuple(str, Schema))
        """
        out_dict = {}
        for field, value in schema.items():
            if field.__class__ is str:
                out_dict[field] = getattr(resource, field, None)
            elif field.__class__ is decimal.Decimal:
                out_dict[field] = round((getattr(resource, field, None)), 2)
            else:
                raise ValueError('Unrecognized field in schema')

        out_dict = {k: out_dict[k] for k in out_dict if out_dict[k] is not None}
        if json_dumps:
            return json.dumps(out_dict)
        else:
            return out_dict

    @classmethod
    def decode(cls, resource_cls, json_dict: dict, schema):
        kwargs = {}

        for field in schema:
            kwargs[field] = json_dict[field] if field in json_dict else None
        return resource_cls(**kwargs)
