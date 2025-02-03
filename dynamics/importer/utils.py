from typing import Optional

from paperless.objects.address import Address as PaperlessAddress
from paperless.objects.customers import Account as PaperlessAccount, Contact as PaperlessContact
from paperless.objects.purchased_components import PurchasedComponent as PaperlessPurchasedComponent

from dynamics.objects.customer import AddressMixin as DynamicsAddress, Customer as DynamicsCustomer, \
    Contact as DynamicsContact, ContactInfoMixin
from dynamics.objects.item import PurchasedComponent as DynamicsPurchasedComponent, RawMaterial, Material, CoatingItem, \
    MachineCenter


class PaperlessObjectCreator:
    """
    Contains utility methods to generate empty Paperless objects, to be updated later with real data.
    """

    @staticmethod
    def empty_address():
        return PaperlessAddress(
            address1='',
            city='',
            country='',
            postal_code='',
            state=''
        )

    @staticmethod
    def empty_account():
        return PaperlessAccount(
            name=''
        )

    @staticmethod
    def empty_contact():
        return PaperlessContact(
            account_id=None,
            email='',
            first_name='',
            last_name=''
        )

    @staticmethod
    def empty_purchased_component():
        return PaperlessPurchasedComponent(
            oem_part_number='',
            piece_price=''
        )


class DynamicsToPaperlessTranslator:
    """
    Contains utility methods that update a Paperless object with data from a Dynamics object.
    """

    @staticmethod
    def update_address(pp_address: PaperlessAddress, dynamics_address: DynamicsAddress):
        pp_address.address1 = dynamics_address.Address
        pp_address.address2 = dynamics_address.Address_2
        pp_address.city = dynamics_address.City
        pp_address.state = dynamics_address.County
        pp_address.postal_code = dynamics_address.Post_Code
        pp_address.country = dynamics_address.get_country()

    @staticmethod
    def update_account(pp_account: PaperlessAccount, dynamics_customer: DynamicsCustomer):
        pp_account.erp_code = dynamics_customer.No
        pp_account.name = dynamics_customer.Name
        pp_account.phone = DynamicsToPaperlessTranslator.translate_phone_num(dynamics_customer)
        pp_account.url = dynamics_customer.Home_Page
        dynamics_payment_terms_period = dynamics_customer.get_payment_terms_period()
        if dynamics_customer.Payment_Terms_Code and isinstance(dynamics_payment_terms_period, int):
            pp_account.payment_terms = dynamics_customer.Payment_Terms_Code
            pp_account.payment_terms_period = dynamics_payment_terms_period
        if dynamics_customer.address_exists():
            if not isinstance(pp_account.sold_to_address, PaperlessAddress):
                pp_account.sold_to_address = PaperlessObjectCreator.empty_address()
            DynamicsToPaperlessTranslator.update_address(pp_account.sold_to_address, dynamics_customer)

    @staticmethod
    def update_contact(pp_contact: PaperlessContact, dynamics_contact: DynamicsContact, paperless_account_id: int):
        pp_contact.account_id = paperless_account_id
        pp_contact.email = dynamics_contact.E_Mail
        pp_contact.phone = DynamicsToPaperlessTranslator.translate_phone_num(dynamics_contact)
        pp_contact.first_name = dynamics_contact.First_Name
        pp_contact.last_name = dynamics_contact.Surname
        if dynamics_contact.address_exists():
            if not isinstance(pp_contact.address, PaperlessAddress):
                pp_contact.address = PaperlessObjectCreator.empty_address()
            DynamicsToPaperlessTranslator.update_address(pp_contact.address, dynamics_contact)

    @staticmethod
    def update_purchased_component(pp_purchased_component: PaperlessPurchasedComponent,
                                   dynamics_purchased_component: DynamicsPurchasedComponent):
        pp_purchased_component.oem_part_number = dynamics_purchased_component.No
        pp_purchased_component.internal_part_number = dynamics_purchased_component.No
        pp_purchased_component.piece_price = dynamics_purchased_component.Unit_Cost
        pp_purchased_component.description = dynamics_purchased_component.Description

    @staticmethod
    def update_machine_center(pp_machine_center: dict, dynamics_machine_center: MachineCenter):
        pp_machine_center['No'] = dynamics_machine_center.No
        pp_machine_center['Name'] = dynamics_machine_center.Name
        pp_machine_center['Work_Center_No'] = dynamics_machine_center.Work_Center_No
        pp_machine_center['Capacity'] = dynamics_machine_center.Capacity
        pp_machine_center['Efficiency'] = dynamics_machine_center.Efficiency
        pp_machine_center['Search_Name'] = dynamics_machine_center.Search_Name
        pp_machine_center['Overhead_Rate'] = dynamics_machine_center.Overhead_Rate

    @staticmethod
    def update_raw_material(pp_material: dict, dynamics_material: RawMaterial):
        pp_material['No'] = dynamics_material.No
        pp_material['Description'] = dynamics_material.Description
        pp_material['Type'] = dynamics_material.Type
        pp_material['Unit_Cost'] = dynamics_material.Unit_Cost
        pp_material['Unit_Price'] = dynamics_material.Unit_Price
        pp_material['Vendor_No'] = dynamics_material.Vendor_No
        pp_material['Base_Unit_of_Measure'] = dynamics_material.Base_Unit_of_Measure

        for pp_column_name, value in dynamics_material.get_attribute_values().items():
            pp_material[pp_column_name] = value

    @staticmethod
    def update_material(pp_material: dict, dynamics_material: Material):
        DynamicsToPaperlessTranslator.update_raw_material(pp_material, dynamics_material)
        pp_material['Quantity_on_Hand'] = dynamics_material.Inventory
        pp_material['Substitutes_Exist'] = 'TRUE' if dynamics_material.Substitutes_Exist else 'False'

    @staticmethod
    def update_coating_item(pp_material: dict, dynamics_item: CoatingItem):
        DynamicsToPaperlessTranslator.update_raw_material(pp_material, dynamics_item)
        pp_material['Search_Description'] = dynamics_item.Search_Description
        pp_material['Inventory_Posting_Group'] = dynamics_item.Inventory_Posting_Group
        pp_material['Profit'] = dynamics_item.Profit_Percent
        pp_material['Last_Direct_Cost'] = dynamics_item.Last_Direct_Cost
        pp_material['Indirect_Cost'] = dynamics_item.Indirect_Cost_Percent
        pp_material['Vendor_Item_No'] = dynamics_item.Vendor_Item_No
        pp_material['Lead_Time_Calculation'] = dynamics_item.Lead_Time_Calculation
        pp_material['Global_Dimension_1_Code'] = dynamics_item.Global_Dimension_1_Code
        pp_material['Global_Dimension_2_Code'] = dynamics_item.Global_Dimension_2_Code
        pp_material['Sales_Unit_of_Measure'] = dynamics_item.Sales_Unit_of_Measure
        pp_material['Purch_Unit_of_Measure'] = dynamics_item.Purch_Unit_of_Measure
        pp_material['Item_Category_Code'] = dynamics_item.Item_Category_Code

    @staticmethod
    def translate_phone_num(entity: ContactInfoMixin):
        return entity.Phone_No.replace('-', '')


class ObjectMatchChecker:
    """
    Contains utility methods that check whether a certain Dynamics object matches a certain Dynamics object.
    """

    @staticmethod
    def address_matches(dynamics_address: DynamicsAddress, pp_address: Optional[PaperlessAddress]):
        if not pp_address:
            return not dynamics_address.address_exists()
        return all([
            dynamics_address.Address == pp_address.address1,
            dynamics_address.Address_2 == pp_address.address2,
            dynamics_address.City == pp_address.city,
            dynamics_address.County == pp_address.state,
            dynamics_address.Post_Code == pp_address.postal_code,
            dynamics_address.get_country() == pp_address.country
        ])

    @staticmethod
    def account_matches(dynamics_customer: DynamicsCustomer, pp_account: PaperlessAccount):
        return all([
            dynamics_customer.No == pp_account.erp_code,
            dynamics_customer.Name == pp_account.name,
            DynamicsToPaperlessTranslator.translate_phone_num(dynamics_customer) == pp_account.phone,
            dynamics_customer.Home_Page == pp_account.url,
            dynamics_customer.Payment_Terms_Code == pp_account.payment_terms,
            dynamics_customer.get_payment_terms_period() == pp_account.payment_terms_period,
            ObjectMatchChecker.address_matches(dynamics_customer, pp_account.sold_to_address)
        ])

    @staticmethod
    def contact_matches(dynamics_contact: DynamicsContact, pp_contact: PaperlessContact, paperless_account_id: int):
        return all([
            paperless_account_id == pp_contact.account_id,
            dynamics_contact.E_Mail == pp_contact.email,
            DynamicsToPaperlessTranslator.translate_phone_num(dynamics_contact) == pp_contact.phone,
            dynamics_contact.First_Name == pp_contact.first_name,
            dynamics_contact.Surname == pp_contact.last_name,
            ObjectMatchChecker.address_matches(dynamics_contact, pp_contact.address)
        ])

    @staticmethod
    def purchased_component_matches(pp_purchased_component: PaperlessPurchasedComponent,
                                    dynamics_purchased_component: DynamicsPurchasedComponent):
        return all([
            dynamics_purchased_component.No == pp_purchased_component.oem_part_number,
            dynamics_purchased_component.No == pp_purchased_component.internal_part_number,
            float(dynamics_purchased_component.Unit_Cost) == float(pp_purchased_component.piece_price),
            dynamics_purchased_component.Description == pp_purchased_component.description
        ])
