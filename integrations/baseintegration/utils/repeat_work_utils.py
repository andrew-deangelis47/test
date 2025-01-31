from dataclasses import dataclass
from typing import List, Dict
from django.db.models import Model
from ...baseintegration.utils.repeat_work_objects import Header, MethodOfManufacture


@dataclass
class MOMWrapper:  # by caching the source of the MOM's erp code, we reduce DB hits when building the headers
    method_of_manufacture: MethodOfManufacture
    header_type: str
    root: Model


def get_headers_from_methods(methods_of_manufacture: List[MOMWrapper],
                             get_template_header, get_estimated_header,
                             get_engineered_header, get_executed_header) -> List[Header]:
    headers_by_key: Dict[tuple, Header] = {}
    for mom_wrapper in methods_of_manufacture:
        method_of_manufacture = mom_wrapper.method_of_manufacture
        header_type = mom_wrapper.header_type
        header_key = (header_type, mom_wrapper.root.pk)
        header = headers_by_key.get(header_key)
        if not header:
            if header_type == "template":
                header = get_template_header(mom_wrapper.root)
            elif header_type == "estimated":
                header = get_estimated_header(mom_wrapper.root)
            elif header_type == "engineered":
                header = get_engineered_header(mom_wrapper.root)
            elif header_type == "executed":
                header = get_executed_header(mom_wrapper.root)
            else:
                raise "Header type does not exist"
            headers_by_key[header_key] = header
        header.methods_of_manufacture.append(method_of_manufacture)
    return list(headers_by_key.values())
