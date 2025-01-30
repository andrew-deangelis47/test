from plex_v2.objects.part import Part
from plex_v2.utils.import_utils import ImportUtils
from plex_v2.objects.approved_supplier import ApprovedSupplierGetDatasource
from plex_v2.configuration import PlexConfig
from baseintegration.datamigration import logger


class MaterialPricingHelper:

    """
    Gets the price for a material via a chain of calls to certain data sources
    """

    utils: ImportUtils

    def __init__(self, utils: ImportUtils, config: PlexConfig):
        self.utils = utils
        self.config = config

    def get_price_and_pricing_unit(self, material: Part) -> tuple:
        """
        getting pricing requires a chain of API calls
        if we get a bad value from any one of these we just return the default
        """

        # get the part key
        part_key: int = self.utils.get_plex_part_key_from_part(material)

        # get the op code
        op_code: str = self.utils.get_first_op_code_for_part(material)
        if op_code is None:
            print('Material pricing getter: could not find op code')
            return self._return_defaults(material)

        # get the part operation key
        part_operation_key: int = self.utils.get_part_op_key_from_op_code_and_part_key(op_code, part_key)
        if part_operation_key is None:
            print('Material pricing getter: could not find part op key')
            return self._return_defaults(material)

        # get the supplier id
        supplier_id: str = self.utils.get_supplier_id_from_part_and_op_code(material, op_code)
        if supplier_id is None:
            print('Material pricing getter: could not find supplier id')
            return self._return_defaults(material)

        # get the supplier code
        supplier_code: str = self.utils.get_supplier_code_from_supplier_id(supplier_id)
        if supplier_code is None:
            print('Material pricing getter: could not find supplier code')
            return self._return_defaults(material)

        # get the supplier number
        supplier_no: int = self.utils.get_supplier_no_from_supplier_code(supplier_code)
        if supplier_no is None:
            print('Material pricing getter: could not find supplier number')
            return self._return_defaults(material)

        # get the price
        approved_supplier_get_datasource: ApprovedSupplierGetDatasource = self.utils.get_supplier_material_price_and_price_unit(material, part_key, part_operation_key, supplier_no)
        if approved_supplier_get_datasource is None:
            print('Material pricing getter: could not approved supplier')
            return self._return_defaults(material)

        if approved_supplier_get_datasource.Price is None:
            print('Material pricing getter: no price from approved supplier')
            return self._return_defaults(material)

        print(f'Material price: {approved_supplier_get_datasource.Price}')
        print(f'Material price unit: {approved_supplier_get_datasource.Price_Unit}')

        return round(approved_supplier_get_datasource.Price, 4), approved_supplier_get_datasource.Price_Unit

    def _return_defaults(self, material: Part):
        logger.info(f'Skipping price import of material "{material.number}"')
        # determine defaults based on which import config we have
        if self.config.default_pc_piece_price is not None:
            price = self.config.default_pc_piece_price
            unit = self.config.default_pc_price_unit
        else:
            price = self.config.default_material_price
            unit = self.config.default_material_price_unit

        logger.info(f'Configured default price: {price}')
        logger.info(f'Configured default price unit: {unit}')
        return price, unit
