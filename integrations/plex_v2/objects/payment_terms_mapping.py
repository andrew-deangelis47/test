import attr
from attr.validators import instance_of, optional
from typing import List, Union


@attr.s(kw_only=True)
class PaymentTermsMapping:

    payment_terms = attr.ib(validator=optional(instance_of(str)))
    payment_terms_period = attr.ib(validator=optional(instance_of((float, int))))


class PaymentTermsMappingList:
    payment_terms_mapping_list: List[PaymentTermsMapping]

    def __init__(self, payment_terms_mapping_list: List[PaymentTermsMapping]):
        self.payment_terms_mapping_list = payment_terms_mapping_list

    def _get_period_by_terms(self, target_terms: str) -> Union[PaymentTermsMapping, None]:
        mapping: PaymentTermsMapping
        for mapping in self.payment_terms_mapping_list:
            if mapping.payment_terms == target_terms:
                return mapping.payment_terms_period

        return None
