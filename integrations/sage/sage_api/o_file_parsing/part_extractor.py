from .base_extractor import BaseExtractor
from sage.models.sage_models.part import PartFullEntity, Product, ProductSiteTotals


class PartExtractor(BaseExtractor):
    primary_table_key = 'I'

    def get_parts(self, i_file: str):
        full_parts = self.extract_full_entities(i_file)
        full_part_objects = []

        for full_part_payload in full_parts:
            product = self.extract_entities(full_part_payload, 'I', Product)[0]
            product_site_totals = self.extract_entities(full_part_payload, 'K', ProductSiteTotals)

            # we don't always get a product site totals entity, make sure we have it or default to 0
            product_site_total = ProductSiteTotals()
            if len(product_site_totals) > 0:
                product_site_total = product_site_totals[0]

            full_part_objects.append(
                PartFullEntity(product=product, prod_site_totals=product_site_total)
            )

        return full_part_objects
