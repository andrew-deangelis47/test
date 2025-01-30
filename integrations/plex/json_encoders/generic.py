import json
from typing import Union


class FlatMapJSONEncoder:
    @classmethod
    def encode(cls, resource, schema, json_dumps=True) -> Union[dict, str]:
        """
        Schema data definition:

        a Schema is a Dict[str, str | Callable[[str, typeof resource], Any]]
        """
        out_dict = {}
        for field in schema:
            target = schema[field]
            if isinstance(target, str):
                if target == '.':  # shorthand for identity
                    out_dict[field] = getattr(resource, field, None)
                else:
                    out_dict[field] = getattr(resource, target, None)
            elif callable(target):
                out_dict[field] = target(field, resource)
            else:
                raise ValueError('Unrecognized field in schema')

        if json_dumps:
            return json.dumps(out_dict)
        else:
            return out_dict

    @classmethod
    def decode(cls, resource_cls, json_dict: dict, schema):
        kwargs = {}

        for field in schema:
            target = schema[field]
            if isinstance(target, str):
                if target == '.':
                    kwargs[field] = json_dict[field] if field in json_dict else None
                else:
                    kwargs[field] = json_dict[target] if target in json_dict else None
            elif callable(target):
                kwargs[field] = target(field, json_dict)
                pass
            else:
                raise ValueError('Unrecognized field in schema')
        return resource_cls(**kwargs)
