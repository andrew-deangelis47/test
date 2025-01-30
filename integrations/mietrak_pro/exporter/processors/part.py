import os
from typing import Optional, Union
from baseintegration.utils import safe_get

from mietrak_pro.models import Party, Itemtype, Item, Generalledgeraccount
from mietrak_pro.exporter.processors import MietrakProProcessor
from baseintegration.datamigration import logger

from mietrak_pro.exporter.utils import PartData, RawMaterialPartData
from mietrak_pro.query.part import create_item, get_item, get_item_type, get_calculation_type, get_unit_of_measure_set, \
    get_general_ledger_account_from_num
from paperless.objects.orders import OrderComponent, OrderItem, Order
from paperless.objects.quotes import QuoteComponent, QuoteItem, Quote
from paperless.objects.purchased_components import PurchasedComponent
from typing import List
from baseintegration.utils.operations import OperationUtils
import re


class PartProcessor(MietrakProProcessor):
    do_rollback = False
    stock_length = None
    stock_width = None
    thickness = None

    def _process(self, component: Union[OrderComponent, QuoteComponent],
                 quote_or_order_item: Union[OrderItem, QuoteItem],
                 quote_or_order: Union[Order, Quote],
                 customer: Party):

        part_number = self.get_part_number(component)
        revision = self.get_revision(component)
        description = self.get_description(component, quote_or_order_item)
        assigned_party = self.get_party(customer, component, quote_or_order_item, quote_or_order)

        item_type = self.get_type(component)
        calc_type = self.get_calc_type(item_type)
        general_ledger_account = self.get_general_ledger_account(component, quote_or_order_item, quote_or_order)
        purchase_general_ledger_account = self.get_purchase_general_ledger_account(component)
        item_class = self.get_item_class(component, quote_or_order_item, quote_or_order)
        unit_of_measure_set = self.get_unit_of_measure_set(component)
        is_itar = self.get_is_itar(component)

        division_pk = self._exporter.division_pk

        # Get or create part
        part, is_part_new = self.get_or_create_part(part_number, revision, description, assigned_party, item_type,
                                                    calc_type, general_ledger_account, item_class, unit_of_measure_set,
                                                    is_itar, division_pk,
                                                    purchase_general_ledger_account, self._exporter.estimator)

        # Optionally, update the part description to reflect what was entered in Paperless Parts
        if self._exporter.erp_config.should_update_mietrak_pro_part_description:
            part = self.update_part_description(part, description)

        # If this is a purchased component, bring the additional purchased component information over from Paperless
        if component.type == 'purchased':
            part = self.update_purchased_component_data(part, component, is_part_new)

        # TODO - move this to _post_process
        # TODO - will raw materials be set as explicit components in the tree in Paperless Parts?
        part_data = PartData(part=part, is_part_new=is_part_new, raw_material_part_data=[])
        if component.type in {'manufactured', "assembled"} and self._exporter.erp_config.should_create_mietrak_pro_raw_material_record:
            customer = None
            raw_materials: List[tuple] = self.get_or_create_raw_material(component, customer,
                                                                         quote_or_order_item, quote_or_order)
            for material in raw_materials:
                raw_material, is_raw_material_new = material
                raw_material_quantity = self.get_raw_material_quantity(component)
                raw_material_part = RawMaterialPartData(raw_material_part=raw_material,
                                                        is_raw_material_new=is_raw_material_new,
                                                        raw_material_bom_quantity=raw_material_quantity
                                                        )
                part_data.raw_material_part_data.append(raw_material_part)
                logger.info(f"Created MieTrak raw material Item data for {raw_material.partnumber}")

        return part_data

    def get_part_number(self, component: Union[OrderComponent, QuoteComponent]):
        # The Item PartNumber field has a max length of 150
        part_number = component.part_number.upper()[:150] if component.part_number is not None else None
        if part_number is None:
            part_name = component.part_name[:150]
            part_number, ext = os.path.splitext(part_name)
        return part_number

    def get_revision(self, component: Union[OrderComponent, QuoteComponent]):
        # The Item Revision field has a max length of 20
        return component.revision.upper()[:20] if component.revision is not None else None

    def get_description(self, component: Union[OrderComponent, QuoteComponent],
                        quote_or_order_item: Union[OrderItem, QuoteItem]):
        return component.description

    def get_party(self, customer: Party, component: Union[OrderComponent, QuoteComponent],
                  quote_or_order_item: Union[OrderItem, QuoteItem],
                  quote_or_order: Union[Order, Quote]):
        """ All Item records in MIE Trak Pro need to be associated with a Party. Attempt to assign the Party for this
            Item based on the Party name supplied in the config, but fall back to the customer if no match is found. """
        party_name = self._exporter.erp_config.default_purchased_item_vendor_name
        assigned_party = customer
        if component.type == 'purchased':
            purchased_item_vendor_party = Party.objects.filter(name=party_name).first()
            if purchased_item_vendor_party is not None:
                assigned_party = purchased_item_vendor_party
        return assigned_party

    def get_type(self, component: Optional[Union[OrderComponent, QuoteComponent]], is_raw_material=False):
        component_type = safe_get(component, 'type')
        is_outside_process = False
        item_type = get_item_type(component_type, is_raw_material, is_outside_process)
        return item_type

    def get_calc_type(self, item_type: Itemtype):
        return get_calculation_type(item_type)

    def search_for_op_variable(self, var_name: str, component: Union[OrderComponent, QuoteComponent]):
        for operation in component.shop_operations:
            val = operation.get_variable(var_name)
            if val is not None:
                return val

    def get_general_ledger_account(self, component: Union[OrderComponent, QuoteComponent],
                                   quote_or_order_item: Union[OrderItem, QuoteItem],
                                   quote_or_order: Union[Order, Quote]):
        """ Take component, order_item, and order as arguments because it's not clear what information
            in Paperless we'll need to map to MIE Trak Pro's General Ledger Account. """
        if self._exporter.erp_config.pp_revenue_account_num_var:
            pp_revenue_account_num = self.search_for_op_variable(self._exporter.erp_config.pp_revenue_account_num_var,
                                                                 component)
            if pp_revenue_account_num is not None:
                return get_general_ledger_account_from_num(pp_revenue_account_num)

    def get_purchase_general_ledger_account(self, component: Union[OrderComponent, QuoteComponent]) \
            -> Optional[Generalledgeraccount]:
        if self._exporter.erp_config.pp_purchase_account_num_var:
            pp_purchase_account_num = self.search_for_op_variable(self._exporter.erp_config.pp_purchase_account_num_var,
                                                                  component)
            if pp_purchase_account_num is not None:
                return get_general_ledger_account_from_num(pp_purchase_account_num)

    def get_item_class(self, component: Union[OrderComponent, QuoteComponent],
                       quote_or_order_item: Union[OrderItem, QuoteItem],
                       quote_or_order: Union[Order, Quote]):
        return None

    def get_unit_of_measure_set(self, component: Union[OrderComponent, QuoteComponent]):
        unit_of_measure_set_code = 'EACH'
        return get_unit_of_measure_set(unit_of_measure_set_code)

    def get_is_itar(self, component):
        return component.export_controlled

    def get_raw_material_part_number(self, component: Union[OrderComponent, QuoteComponent]) -> List[str]:
        part_numbers: list = []
        var_name = self._exporter.erp_config.raw_material_part_number_variable_name
        if component.material_operations:
            for material_op in component.material_operations:  # Check for table vars with valid Item PKs
                raw_material = OperationUtils.get_variable_obj(material_op, var_name)
                if raw_material and hasattr(raw_material, 'row') and raw_material.row and 'ItemPK' in raw_material.row:
                    part_number = str(raw_material.row["ItemPK"])
                    part_numbers.append(part_number)
                else:  # Fallback to a P3L variable value if not table var
                    part_number = material_op.get_variable(var_name)
                    if part_number:
                        part_numbers.append(part_number[:150] if len(part_number) > 150 else part_number)
                if not part_number and self._exporter.erp_config.should_use_default_raw_material:
                    part_numbers.append('RAW MATERIAL')
                elif not part_number:
                    raise ValueError(f'Raw material not found on material op for {component.part_name}, '
                                     f'and raw material defaults are disabled in config')
        return part_numbers

    def get_raw_material_revision(self, component: Union[OrderComponent, QuoteComponent]):
        return None

    def get_raw_material_quantity(self, component: Union[OrderComponent, QuoteComponent]):
        return 1.

    def get_raw_material_description(self, component: Union[OrderComponent, QuoteComponent]):
        return None

    def get_raw_material_general_ledger_account(self, component: Union[OrderComponent, QuoteComponent],
                                                quote_or_order_item: Union[OrderItem, QuoteItem],
                                                quote_or_order: Union[Order, Quote]):
        """ Take component, order_item, and order as arguments because it's not clear what information
            in Paperless we'll need to map to MIE Trak Pro's General Ledger Account. """
        return None

    def get_raw_material_unit_of_measure_set(self, component: Union[OrderComponent, QuoteComponent]):
        unit_of_measure_set_code = 'EACH'
        return get_unit_of_measure_set(unit_of_measure_set_code)

    def get_raw_material_is_itar(self, component: Union[OrderComponent, QuoteComponent]):
        return False

    def get_raw_material_party(self, customer: Party, component: Union[OrderComponent, QuoteComponent],
                               quote_or_order_item: Union[OrderItem, QuoteItem],
                               quote_or_order: Union[Order, Quote]):
        """ All Item records in MIE Trak Pro need to be associated with a Party. Attempt to assign the Party for this
            Item based on the Party name supplied in the config, but fall back to the customer if no match is found. """
        party_name = self._exporter.erp_config.default_purchased_item_vendor_name
        raw_material_party = Party.objects.filter(name=party_name).first()
        if raw_material_party is None:
            raw_material_party = customer
        return raw_material_party

    def update_part_description(self, part: Item, description: str):
        logger.info(f'Updating description for part {part.partnumber}')
        part.description = description
        part.save()
        return part

    def update_purchased_component_data(self, part: Item, component: Union[OrderComponent, QuoteComponent], is_part_new: bool):
        purchased_component = component.purchased_component
        should_update_purchased_component_data = \
            self._exporter.erp_config.should_update_mietrak_pro_purchased_components_data or \
            (purchased_component is not None and is_part_new)
        if should_update_purchased_component_data:
            part.description = purchased_component.description
            part.save()

        part = self.update_purchased_component_from_user_defined_fields(part, purchased_component)
        return part

    def update_purchased_component_from_user_defined_fields(self, part: Item, purchased_component: PurchasedComponent):
        # TODO - this should be overridden for each implementation based on their custom purchased component fields
        return part

    def get_or_create_part(self, part_number, revision, description, customer, item_type, calc_type,
                           general_ledger_account, item_class, unit_of_measure_set, is_itar, division_pk: int = 1,
                           purchase_general_ledger_account=None, estimator=None):
        is_part_new = False
        part = get_item(part_number, revision)
        if part is not None:
            logger.info(f'Found existing Item record for part number {part_number} and revision {revision}')
        else:
            logger.info(
                f'Did not find existing Item record for part number {part_number} and revision {revision}. Creating new record.')
            part: Item = create_item(part_number, revision, description, customer, is_itar, item_type,
                                     calc_type, general_ledger_account, item_class, unit_of_measure_set, division_pk,
                                     purchase_general_ledger_account, estimator, self.stock_length, self.stock_width,
                                     self.thickness)
            is_part_new = True
        return part, is_part_new

    def get_or_create_raw_material(self, component: Union[OrderComponent, QuoteComponent], customer: Party,
                                   quote_or_order_item: Union[OrderItem, QuoteItem],
                                   quote_or_order) -> List[tuple]:

        raw_material_party = self.get_raw_material_party(customer, component, quote_or_order_item, quote_or_order)
        item_type = self.get_type(component=None, is_raw_material=True)
        calc_type = self.get_calc_type(item_type)
        general_ledger_account = self.get_raw_material_general_ledger_account(component, quote_or_order_item, quote_or_order)
        purchase_general_ledger_account = self.get_purchase_general_ledger_account(component)
        item_class = None
        unit_of_measure_set = self.get_unit_of_measure_set(component)
        is_itar = self.get_raw_material_is_itar(component)

        part_numbers = self.get_raw_material_part_number(component)
        raw_materials: List[tuple] = []

        for part_number in part_numbers:
            raw_material = ()
            if part_number and re.match('^[0-9.]*$', part_number):  # Get part if valid Item PK (numeric)
                item_pk: int = int(float(part_number))
                raw_material = Item.objects.filter(itempk=item_pk).first()
                if raw_material:
                    raw_materials.append((raw_material, False))
                    continue
            if not raw_material:  # Get/Create new parts if no match on ItemPk
                part_number: str = part_number
                self.stock_length, self.stock_width, self.thickness = self.get_stock_dimensions(part_number, component)
                revision = self.get_raw_material_revision(component)  # Returns None by default
                description = self.get_raw_material_description(component)  # Returns None by default
                raw_material: tuple = self.get_or_create_part(part_number, revision, description, raw_material_party,
                                                              item_type, calc_type, general_ledger_account, item_class,
                                                              unit_of_measure_set, is_itar,
                                                              self._exporter.erp_config.company_division_pk,
                                                              purchase_general_ledger_account,
                                                              self._exporter.estimator)
                raw_materials.append(raw_material)
        return raw_materials

    def get_stock_dimensions(self, part_number, component: Union[OrderComponent, QuoteComponent]):
        stocklength = stockwidth = thickness = 0
        for mat_op in component.material_operations:
            if mat_op.get_variable(self._exporter.erp_config.raw_material_part_number_variable_name) == part_number:
                stocklength = mat_op.get_variable(self._exporter.erp_config.stock_length_variable_name)
                stockwidth = mat_op.get_variable(self._exporter.erp_config.stock_width_variable_name)
                thickness = mat_op.get_variable(self._exporter.erp_config.stock_thickness_variable_name)
        return stocklength, stockwidth, thickness
