from .base_extractor import BaseExtractor
from sage.models.sage_models.vendor import Supplier, SupplierFullEntity


class VendorExtractor(BaseExtractor):
    primary_table_key = 'B'

    def get_vendors(self, i_file: str):
        raw_full_suppliers = self.extract_full_entities(i_file)
        full_supplier_objects = []

        for raw_full_customer in raw_full_suppliers:
            supplier = self.extract_entities(raw_full_customer, 'B', Supplier)[0]

            full_supplier_objects.append(
                SupplierFullEntity(supplier=supplier)
            )

        return full_supplier_objects
