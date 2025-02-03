from plex_v2.factories.base import BaseFactory
from plex_v2.objects.part import Part
from plex_v2.objects.customer import CustomerPart, Customer


class CustomerPartFactory(BaseFactory):

    def to_customer_part(self, plex_part: Part, plex_customer: Customer) -> CustomerPart:
        return CustomerPart(
            number=plex_part.number,
            partId=plex_part.id,
            revision=plex_part.revision,
            customerId=plex_customer.id,
            description=self._get_description(plex_part)
        )

    def _get_description(self, part: Part) -> str:
        description = part.name
        if description and part.description:
            description += f"\n {part.description}"
        elif part.description:
            description = part.description
        return description[:200]
