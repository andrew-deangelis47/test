from dataclasses import dataclass
from typing import Optional

from mietrak_pro.models import Workcenter, Quoteassembly, Workorderassembly, Item, \
    Unitofmeasureset, Party, Quote, Quotequantity, Router, Routerworkcenter, Itemtype


def get_template_operation_costing_variables(rwc: Routerworkcenter, wc: Workcenter):
    return {
        "leadtime": (rwc.leadtime, float),
        "comment": (rwc.comment, str),
        "runemployees": (rwc.runemployees, float),
        "setupemployees": (rwc.setupemployees, float),
        "overagepercentage": (rwc.overagepercentage, float),
        "stockpiecesscrappercentage": (rwc.stockpiecesscrappercentage, float),
        "partsperblankscrappercentage": (rwc.partsperblankscrappercentage, float),
        "unattendedpercentage": (rwc.unattendedpercentage, float),
        "unattendedoperation": (rwc.unattendedoperation, float),
        **get_workcenter_costing_variables(wc)
    }


def get_estimated_operation_costing_variables(qa: Quoteassembly, wc: Workcenter):
    return {
        "leadtime": (qa.leadtime, float),
        "comment": (qa.comment, str),
        "runemployees": (qa.runemployees, float),
        "setupemployees": (qa.setupemployees, float),
        "overagepercentage": (qa.overagepercentage, float),
        "stockpiecesscrappercentage": (qa.stockpiecesscrappercentage, float),
        "partsperblankscrappercentage": (qa.partsperblankscrappercentage, float),
        "unattendedpercentage": (qa.unattendedpercentage, float),
        "unattendedoperation": (qa.unattendedoperation, float),
        **get_workcenter_costing_variables(wc)
    }


def get_engineered_operation_costing_variables(wo: Workorderassembly, wc: Workcenter):
    return {
        "leadtime": (wo.leadtime, float),
        "comment": (wo.comment, str),
        "runemployees": (wo.runemployees, float),
        "setupemployees": (wo.setupemployees, float),
        "overagepercentage": (wo.overagepercentage, float),
        "stockpiecesscrappercentage": (wo.stockpiecesscrappercentage, float),
        "partsperblankscrappercentage": (wo.partsperblankscrappercentage, float),
        "unattendedpercentage": (wo.unattendedpercentage, float),
        "unattendedoperation": (wo.unattendedoperation, float),
        **get_workcenter_costing_variables(wc)
    }


def get_workcenter_costing_variables(wc: Workcenter):
    return {
        "name": (wc.description, str),
        "lagtime": (wc.lagtime, float),
        "gapdays": (wc.gapdays, float),
        "wc_description": (wc.description, str),
        "averageemployeerate": (wc.averageemployeerate, float),
        "averageemployeeoverheadrate": (wc.averageemployeeoverheadrate, float),
        "hourlyoverhead": (wc.hourlyoverhead, float),
        "hourlyrate": (wc.hourlyrate, float),
        "setuprate": (wc.setuprate, float),
    }


def get_template_material_costing_variables(rwc: Routerworkcenter, item: Item):
    return {
        "material": (item.partnumber, str),
        "vendor": ("", str),
        "quantity": (rwc.quantityrequired, float),
        "quantity_per": (rwc.quantityperinverse, float),
        "unit_of_measure": (rwc.unitofmeasuresetfk and Unitofmeasureset(rwc.unitofmeasuresetfk).name, str),
        "cost": (rwc.price, float),
        "partsrequired": (rwc.partsrequired, float),
        "pieceweight": (rwc.pieceweight, float),
        "part_length": (rwc.partlength, float),
        "part_weight": (rwc.weightfactor, float),
        "blanklength": (rwc.blanklength, float),
        "blankweight": (rwc.blankwidth, float),
        "vendorunit": (rwc.vendorunit, float),
    }


def get_estimated_material_costing_variables(qa: Quoteassembly, item: Item):
    return {
        "material": (item.partnumber, str),
        "vendor": (qa.partyfk and Party(qa.partyfk).name, str),
        "quantity": (qa.quantityrequired, float),
        "quantity_per": (qa.quantityperinverse, float),
        "unit_of_measure": (qa.unitofmeasuresetfk and Unitofmeasureset(qa.unitofmeasuresetfk).name, str),
        "cost": (qa.piececost, float),
        "partsrequired": (qa.partsrequired, float),
        "pieceweight": (qa.pieceweight, float),
        "part_length": (qa.partlength, float),
        "part_weight": (qa.weightfactor, float),
        "blanklength": (qa.blanklength, float),
        "blankweight": (qa.blankwidth, float),
        "vendorunit": (qa.vendorunit, float),
    }


def get_engineered_material_costing_variables(wo: Workorderassembly, item: Item):
    return {
        "material": (item.partnumber, str),
        "vendor": (item.partyfk and Party(item.partyfk).name, str),
        "quantity": (wo.quantityrequired, float),
        "quantity_per": (wo.quantityperinverse, float),
        "unit_of_measure": (wo.unitofmeasuresetfk and Unitofmeasureset(wo.unitofmeasuresetfk).name, str),
        "cost": (item.commoditycost, float),
        "partsrequired": (wo.partsrequired, float),
        "pieceweight": (wo.pieceweight, float),
        "part_length": (wo.partlength, float),
        "part_weight": (wo.weightfactor, float),
        "blanklength": (wo.blanklength, float),
        "blankweight": (wo.blankwidth, float),
        "vendorunit": (wo.vendorunit, float),
    }


@dataclass
class MoMQuantityData:
    """
    Represents data about a quote at a particular quantity.
    """
    root: Quote  # root of quote
    total_quantity: int  # total quantity of quote, including quantities of parents
    quantity_data: Quotequantity  # Quotequantity object tied to the quote at its quantity
    linking_assembly: Optional[Quoteassembly]  # Quoteassembly that ties this quote to its parent


@dataclass
class MoMTemplateQuantityData:
    """
    Represents data about a router (item template) at a particular quantity.
    """
    root: Router  # root of quote
    total_quantity: int  # total quantity, including quantities of parents


@dataclass
class OperationData:
    setup_hours = 0
    run_hours = 0
    cost = 0


@dataclass
class MoMCostData:
    """
    Represents data about the prices of a method of manufacture
    """
    unit_price = 0
    total_price = 0


def is_purchased_component(item: Item) -> bool:
    if item:
        item_type: Itemtype = item.itemtypefk
        if item_type and 'Hardware' in item_type.description:
            return True
    return False
