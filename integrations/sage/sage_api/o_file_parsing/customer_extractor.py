from .base_extractor import BaseExtractor
from sage.models.sage_models.customer import Customer, Address, Contact, SageCustomerFullEntity


class CustomerExtractor(BaseExtractor):
    primary_table_key = 'B'

    def get_customers(self, i_file: str):
        raw_full_customers = self.extract_full_entities(i_file)
        full_customers_objects = []

        for raw_full_customer in raw_full_customers:
            customer = self.extract_entities(raw_full_customer, 'B', Customer)[0]
            contacts = self.extract_entities(raw_full_customer, 'C', Contact)
            addresses = self.extract_entities(raw_full_customer, 'A', Address)

            full_customers_objects.append(
                SageCustomerFullEntity(
                    customer=customer,
                    contacts=contacts,
                    addresses=addresses
                )
            )

        return full_customers_objects
