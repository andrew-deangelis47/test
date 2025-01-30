import re
from typing import Tuple

from baseintegration.datamigration import logger
from baseintegration.exporter.processor import BaseProcessor
from paperless.objects.orders import OrderItem, OrderComponent, OrderOperation, OrderCostingVariable, OrderedAddOn
from paperless.objects.components import PurchasedComponent

from visualestitrack.exporter.processors.utilities import Utilities
from visualestitrack.models import Requestforquote, Quoteheader, Quotequantities, Quoteoperations, \
    Quotematerials, Quoteonetimecharges

DEFAULT_WORK_CENTER = 'PP'


class CreateQuoteHeader(BaseProcessor):
    """
    This class extends BaseProcessor from baseintegration and is used to create Quote records into VisualEstiTrack.
    """

    def _process(self, rfq: Requestforquote, order_item: OrderItem, component: OrderComponent, root_id: str, qid: str,
                 sub_count: int, fg_add: bool = True) -> Quoteheader:

        quote_header: Quoteheader
        part_number = CreateQuoteHeader.generate_part_number(component)
        if component.is_root_component:
            quote_header = CreateQuoteHeader.create_quote_objects(rfq=rfq, description=order_item.description,
                                                                  revision=component.revision,
                                                                  private_notes=order_item.private_notes,
                                                                  public_notes=order_item.public_notes,
                                                                  part_number=part_number, pid=qid, qid=qid,
                                                                  sub_count=sub_count, fg_add=fg_add)
        else:
            quote_header = CreateQuoteHeader.create_quote_objects(rfq=rfq, description=component.description,
                                                                  revision=component.revision,
                                                                  part_number=part_number, pid=root_id,
                                                                  qid=qid, sub_count=sub_count, fg_add=fg_add)
        return quote_header

    @staticmethod
    def create_quote_objects(rfq: Requestforquote, description, revision: str, part_number: str, qid: str, pid: str,
                             sub_count: int, private_notes: str = '', public_notes: str = '', fg_add: bool = True):
        des, des_ext = Utilities.split_part_description(description)
        qid = qid
        pid = pid

        part_number = Utilities.shorten_part_number(part_number)
        revision_shorten = Utilities.shorten_revision_number(revision)
        quote = Quoteheader(
            id=qid,
            requestforquoteid=rfq,
            parentquoteid=pid,
            subquotenum=sub_count,
            quotedate=rfq.rfqdate,
            partdescription=des,
            extendedpartdescription=des_ext,
            revisionnumber=revision_shorten,
            partnumber=part_number,
            internalnotes=private_notes,
            customernotes=public_notes,
        )
        if fg_add:
            quote.fginventoryno = part_number

        quote.save()
        return quote

    @staticmethod
    def generate_part_number(component: OrderComponent) -> str:

        number = component.part_number
        if number is None:
            split = component.part_name.split('.')
            number = split[0]
            logger.info(f'VisualEstiTrackExporter: part number was empty for component {component.id}. Falling back to'
                        f'part name {component.part_name}')
        return number


class CreateQuotePeripherals(BaseProcessor):

    def _process(self, quote: Quoteheader, order_item: OrderItem, component: OrderComponent, purchased: list,
                 excluded_operations: list):

        o_item = None
        if component.is_root_component:
            o_item = order_item
            CreateQuotePeripherals.create_peripheral_add_ons(quote, order_item)

        CreateQuotePeripherals.create_peripheral_quote_quantities(quote, component, o_item)
        CreateQuotePeripherals.create_peripheral_quote_operations(quote, component, excluded_operations)
        if component.material is not None and len(component.material_operations) > 0:
            CreateQuotePeripherals.create_peripheral_quote_materials(quote.id, component, excluded_operations)
        purchased_component: OrderComponent
        for purchased_component in purchased:
            CreateQuotePeripherals.create_peripheral_quote_purchase_component(quote.id,
                                                                              purchased_component.deliver_quantity,
                                                                              purchased_component.purchased_component,
                                                                              purchased_component.shop_operations)

    @staticmethod
    def create_peripheral_quote_quantities(quote: Quoteheader, component: OrderComponent, order_item: OrderItem = None):
        quantities: Quotequantities
        quantities = Quotequantities(
            quoteheaderid=quote.id,
            quantity=component.make_quantity,
            priceperpiece=0.0,
            numberofsetups=1
        )
        for shop_operation in component.shop_operations:
            if shop_operation.name == 'Number of Lots':
                value = shop_operation.get_variable('Number of Lots')
                if value is not None:
                    quantities.numberofsetups = int(value)
        if order_item is not None:
            quantities.priceperpiece = order_item.unit_price.raw_amount
        quantities.save()

    @staticmethod
    def create_peripheral_quote_operations(quote: Quoteheader, component: OrderComponent, excluded_operations: list):
        operation: Quoteoperations
        shop_operation: OrderOperation
        idx = 1
        for shop_operation in component.shop_operations:
            if CreateQuotePeripherals.is_excluded_operation(shop_operation.name, excluded_operations):
                continue
            op_type = CreateQuotePeripherals.get_op_type(shop_operation.is_outside_service)
            laborrate, burdenrate, setuphourlyrate, workcentercode = \
                CreateQuotePeripherals.get_operations_costing_variables(shop_operation.costing_variables)
            runtime, runtime_type = CreateQuotePeripherals.get_runtime_values(shop_operation.runtime)
            description = ''
            if shop_operation.notes:
                description = f'{shop_operation.notes}'
            operation = Quoteoperations(
                quoteheaderid=quote.id,
                operationnumber=idx,
                workcentercode=workcentercode,
                description=description,
                operationtype=op_type,
                setuphours=shop_operation.setup_time,
                runtimetype=runtime_type,
                runtime=runtime,
                setuphourlyrate=setuphourlyrate,
                laborrate=laborrate,
                burdenrate=burdenrate
            )
            operation.save()
            idx += 1

    @staticmethod
    def is_excluded_operation(operation_name: str, excluded_operations: list) -> bool:
        for string in excluded_operations:
            found = re.search(string, operation_name, re.IGNORECASE)
            if found is not None:
                return True
        return False

    @staticmethod
    def get_operations_costing_variables(costing_variables: [OrderCostingVariable]):
        labor_rate = 0.0
        burden_rate = 0.0
        setup_hourly_rate = 0.0
        work_center_code = DEFAULT_WORK_CENTER
        variable: OrderCostingVariable
        for variable in costing_variables:
            if variable.label == 'Rate Lookup':
                labor_rate = variable.row.get("labor_rate")
                burden_rate = variable.row.get("burden_rate")
                if work_center_code == DEFAULT_WORK_CENTER:
                    inv_op = variable.row.get("inv_op")
                    work_center_code = CreateQuotePeripherals.shorten_work_center_value(inv_op)
            if variable.label == 'Total Rate ($)':
                setup_hourly_rate = variable.value
            if variable.label == 'Workcenter' and work_center_code == DEFAULT_WORK_CENTER:
                work_center_code = CreateQuotePeripherals.shorten_work_center_value(variable.value)
        return labor_rate, burden_rate, setup_hourly_rate, work_center_code

    @staticmethod
    def shorten_work_center_value(value: str):
        work_center_code = value
        if work_center_code is None:
            work_center_code = DEFAULT_WORK_CENTER
        if len(work_center_code) > 5:
            work_center_code = work_center_code[0:5]
            logger.warning(
                f'VisualEstiTrackExporter: Workcenter "{value}" too long (limit 5) for'
                f' VisualEstiTrack for VisualEstiTrack, truncating to the first 5')
        return work_center_code

    @staticmethod
    def create_peripheral_quote_materials(qid: int, component: OrderComponent, excluded_operations: list):
        material: Quotematerials

        details = 'Raw Material Record; '
        description = ''
        if component.material:
            description, des_ext = Utilities.split_part_description(component.material.name)
            details += f'Name: {component.material.name}, '

        material_operation: OrderOperation
        for material_operation in component.material_operations:
            if CreateQuotePeripherals.is_excluded_operation(material_operation.name, excluded_operations):
                continue
            name = material_operation.name
            details_op = details
            raw_material_inventory_no = ''
            quantity = 1.0
            total_cost = 0.0
            total_cost = total_cost + float(material_operation.cost.raw_amount)
            variable: OrderCostingVariable
            for variable in material_operation.costing_variables:
                details_op += f'{variable.label}: {variable.value}, '
                if variable.label == "Parts Per Sheet" and variable.value > 0:
                    quantity = 1 / variable.value
                if variable.label == "Material Inventory":
                    raw_material_inventory_no = variable.value
                    name = description
            unit_cost = total_cost / (quantity * component.deliver_quantity)

            material = Quotematerials(
                quoteheaderid=qid,
                partnumber='',
                description=name,
                stockuom='each',
                rawmaterialinventoryno=raw_material_inventory_no,
                quantityperpiece=quantity,
                extendedpartdescription=details_op,
                unitcost=unit_cost
            )
            material.save()

    @staticmethod
    def create_peripheral_quote_purchase_component(qid: int, deliver_quantity: int,
                                                   purchased_component: PurchasedComponent,
                                                   shop_operations: [OrderOperation]):
        material: Quotematerials

        description = purchased_component.description
        des, des_ext = Utilities.split_part_description(description)
        operation: OrderOperation
        part_number = purchased_component.oem_part_number
        unit_cost = purchased_component.piece_price.raw_amount
        details = f'Purchase Component; OEM Part Number: {part_number}, Description: {description}, '

        for operation in shop_operations:
            variable: OrderCostingVariable
            for variable in operation.costing_variables:
                details += f'{variable.label}: {variable.value}, '

        part_number = Utilities.shorten_part_number(part_number)

        material = Quotematerials(
            quoteheaderid=qid,
            partnumber=part_number,
            description=des,
            stockuom='each',
            rawmaterialinventoryno='',
            quantityperpiece=deliver_quantity,
            extendedpartdescription=details,
            unitcost=unit_cost
        )
        material.save()

    @staticmethod
    def create_peripheral_add_ons(quote: Quoteheader, order_item: OrderItem):
        add_on: OrderedAddOn
        for add_on in order_item.ordered_add_ons:
            quantity_check = add_on.quantity if add_on.quantity is not None and add_on.quantity != 0 else 1
            unit_price = round((float(add_on.price.raw_amount) / quantity_check), 2)
            one_time_charges = Quoteonetimecharges(
                quoteheaderid=quote.id,
                description=add_on.name,
                quantity=add_on.quantity,
                unitprice=unit_price,
                extendedprice=0.00
            )
            one_time_charges.save()

    @staticmethod
    def get_op_type(outside_op: bool = None):
        """
        A transformation method the converts the OrderOperation.is_outside_service variable to something VisualEstitrack
        can consume.

        @param outside_op:  is the operation out sourced
        @type outside_op: bool
        @return:
        I = "In-house" and maps to 'is_outside_service = False'
        S = "Subcontractv" and maps to  'is_outside_service = True'
        C = "Comment" and maps to None
        @rtype: str
        """
        if outside_op is True:
            return "S"
        elif outside_op is False:
            return "I"
        return "C"

    @staticmethod
    def get_runtime_values(runtime: float) -> Tuple[int, str]:
        """
        This method takes runtime in hours and converts it into seconds if the value is less then 1.

        @param runtime: The runtime values in hours
        @type runtime: float
        @return: The transformed value and the units for that value will be returned as a tuple.  The value type can be:
        S = SecondsPerPiece
        H = HoursPerPiece
        @rtype: tuple
        """
        value_type = 'H'
        value = runtime
        if value is not None and value < 1.00:
            value_type = 'S'
            value = runtime * 3600
        return value, value_type
