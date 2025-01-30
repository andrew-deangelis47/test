from decimal import Decimal
import attr


class BaseObject:

    def to_dict(self):
        # Remove any null values - MongoDB validation rejects nulls
        return attr.asdict(self, recurse=True, filter=lambda k, v: v is not None)

    def to_json(self):
        json_body = GenericJSONEncoder.encode(self, self.to_dict())

        return json_body


class GenericJSONEncoder:
    @classmethod
    def encode(cls, resource, schema: dict):
        data = {}
        for key in schema.keys():
            value = getattr(resource, key, None)

            # Remove any null values - MongoDB validation rejects nulls
            if value is None:
                continue

            if key == "erp_code":  # Capitalize all erp_code fields for search purposes in documentDB
                value = str(value).upper()

            if isinstance(value, Decimal):
                value = float(value)
            if isinstance(value, BaseObject):
                value = value.to_dict()
            elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], BaseObject):
                value = [v.to_dict() for v in value if isinstance(v, BaseObject)]
            data[key] = value
        return data
