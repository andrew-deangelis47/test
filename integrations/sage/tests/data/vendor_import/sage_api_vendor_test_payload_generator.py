"""
This class provides some test data mirroring what we get from the BPS exports template - which gets customer data
All field names in this file come from sage
We can get 4 possible entities from a single customer payload (in this order), each prefixed with an indicator
- B: supplier data
- A: address data
- R: bank information
- C: contact data
"""


class SageApiSupplierTestPayloadGenerator:
    # delimiter for the ifile we are reading from
    DELIMITER = ';'

    # test SUPPLIER data
    SAGE_SUPPLIER_INDICATOR = 'B'
    SAGE_SUPPLIER_CATEGORY = 'supplier_category'
    SAGE_SUPPLIER_SUPPLIER = 'C123456'
    SAGE_SUPPLIER_COMPANY_NAME = 'supplier_company_name'
    SAGE_SUPPLIER_SHORT_DESCRIPTION = 'supplier_short_description'
    SAGE_SUPPLIER_ACRONYM = 'supplier_acronym'
    SAGE_SUPPLIER_DEFAULT_ADDRESS = 'MAIN'
    SAGE_SUPPLIER_CURRENCY = ' supplier_currency'
    SAGE_SUPPLIER_SITE_TAX_ID_NO = 'supplier_site_text_id_no'
    SAGE_SUPPLIER_SIC_CODE = 'supplier_sic_code'
    SAGE_SUPPLIER_EU_VAT_NO = 'supplier_eu_vat_no'
    SAGE_SUPPLIER_TAX_RULE = 'supplier_tax_rule'
    SAGE_SUPPLIER_PAYMENT_TERM = 'supplier_payment_term'
    SAGE_SUPPLIER_ACCOUNTING_CODE = 'supplier_accounting_code'
    SAGE_SUPPLIER_STATISTICAL_GROUP_0 = 'supplier_statistical_group_0'
    SAGE_SUPPLIER_STATISTICAL_GROUP_1 = 'supplier_statistical_group_1'
    SAGE_SUPPLIER_PRICE_LIST_STRUCTURE = 'sage_supplier_price_list_structure'
    SAGE_SUPPLIER_DELIVERY_MODE = 'sage_supplier_delivery_mode'
    SAGE_SUPPLIER_INCO_TERM = 'sage_supplier_inco_term'
    SAGE_SUPPLIER_CREDIT_CONTROL = 'sage_supplier_credit_control'
    SAGE_SUPPLIER_AUTHORIZED_CREDIT = 'supplier_authorized_credit'
    SAGE_SUPPLIER_NOTES = 'supplier_authorized_notes'
    SAGE_SUPPLIER_ORDER_TEXT_0 = 'supplier_order_text_0'
    SAGE_SUPPLIER_ORDER_TEXT_1 = 'supplier_order_text_1'
    SAGE_SUPPLIER_RETURN_TEXT_0 = 'supplier_return_text_0'
    SAGE_SUPPLIER_RETURN_TEXT_1 = 'supplier_return_text_1'

    # test supplier address data
    SAGE_SUPPLIER_ADDRESS_INDICATOR = 'A'
    SAGE_SUPPLIER_ADDRESS_ADDRESS = 'MAIN'
    SAGE_SUPPLIER_ADDRESS_DESCRIPTION = 'address_description'
    SAGE_SUPPLIER_ADDRESS_ADDRESS_LINE_0 = 'address_address_0'
    SAGE_SUPPLIER_ADDRESS_ADDRESS_LINE_1 = 'address_address_1'
    SAGE_SUPPLIER_ADDRESS_ADDRESS_LINE_2 = 'address_address_2'
    SAGE_SUPPLIER_ADDRESS_POSTAL_CODE = 'address_postal_code'
    SAGE_SUPPLIER_ADDRESS_CITY = 'address_city'
    SAGE_SUPPLIER_ADDRESS_COUNTRY = 'address_country'
    SAGE_SUPPLIER_ADDRESS_TELEPHONE = 'address_telephone'
    SAGE_SUPPLIER_ADDRESS_FAX = 'address_fax'

    # test supplier bank info
    SAGE_SUPPLIER_BANK_INFO_INDICATOR = 'R'
    SAGE_SUPPLIER_BANK_INFO_COUNTRY = 'bank_info_country'
    SAGE_SUPPLIER_BANK_INFO_BANK_ACCOUNT_NUMBER = 'bank_info_bank_account_number'
    SAGE_SUPPLIER_BANK_INFO_PAYING_BANK = 'bank_info_paying_bank'

    # test contact info
    SAGE_SUPPLIER_CONTACT_INDICATOR = 'C'
    SAGE_SUPPLIER_CONTACT_CODE = 'contact_code'
    SAGE_SUPPLIER_CONTACT_TITLE = 'contact_title'
    SAGE_SUPPLIER_CONTACT_FIRST_NAME = 'contact_first_name'
    SAGE_SUPPLIER_CONTACT_LAST_NAME = 'contact_last_name'
    SAGE_SUPPLIER_CONTACT_TELEPHONE = 'contact_telephone'
    SAGE_SUPPLIER_CONTACT_FUNCTION = 'contact_function'

    def generate_test_supplier_payload(self) -> str:
        """
        returns a test payload of ONLY supplier data
        """
        supplier_test_payload = self.SAGE_SUPPLIER_INDICATOR + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_CATEGORY + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_SUPPLIER + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_COMPANY_NAME + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_SHORT_DESCRIPTION + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_ACRONYM + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_DEFAULT_ADDRESS + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_CURRENCY + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_SITE_TAX_ID_NO + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_SIC_CODE + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_EU_VAT_NO + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_TAX_RULE + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_PAYMENT_TERM + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_ACCOUNTING_CODE + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_STATISTICAL_GROUP_0 + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_STATISTICAL_GROUP_1 + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_PRICE_LIST_STRUCTURE + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_DELIVERY_MODE + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_INCO_TERM + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_CREDIT_CONTROL + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_AUTHORIZED_CREDIT + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_NOTES + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_ORDER_TEXT_0 + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_ORDER_TEXT_1 + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_RETURN_TEXT_0 + self.DELIMITER
        supplier_test_payload += self.SAGE_SUPPLIER_RETURN_TEXT_1 + self.DELIMITER

        return supplier_test_payload

    def generate_test_address_payload(self) -> str:
        address_test_payload = self.SAGE_SUPPLIER_ADDRESS_INDICATOR + self.DELIMITER
        address_test_payload += self.SAGE_SUPPLIER_ADDRESS_ADDRESS + self.DELIMITER
        address_test_payload += self.SAGE_SUPPLIER_ADDRESS_DESCRIPTION + self.DELIMITER
        address_test_payload += self.SAGE_SUPPLIER_ADDRESS_ADDRESS_LINE_0 + self.DELIMITER
        address_test_payload += self.SAGE_SUPPLIER_ADDRESS_ADDRESS_LINE_1 + self.DELIMITER
        address_test_payload += self.SAGE_SUPPLIER_ADDRESS_ADDRESS_LINE_2 + self.DELIMITER
        address_test_payload += self.SAGE_SUPPLIER_ADDRESS_POSTAL_CODE + self.DELIMITER
        address_test_payload += self.SAGE_SUPPLIER_ADDRESS_CITY + self.DELIMITER
        address_test_payload += self.SAGE_SUPPLIER_ADDRESS_COUNTRY + self.DELIMITER
        address_test_payload += self.SAGE_SUPPLIER_ADDRESS_TELEPHONE + self.DELIMITER
        address_test_payload += self.SAGE_SUPPLIER_ADDRESS_FAX + self.DELIMITER
        return address_test_payload

    def generate_test_bank_info_payload(self) -> str:
        bank_info_test_payload = self.SAGE_SUPPLIER_BANK_INFO_INDICATOR + self.DELIMITER
        bank_info_test_payload += self.SAGE_SUPPLIER_BANK_INFO_COUNTRY + self.DELIMITER
        bank_info_test_payload += self.SAGE_SUPPLIER_BANK_INFO_BANK_ACCOUNT_NUMBER + self.DELIMITER
        bank_info_test_payload += self.SAGE_SUPPLIER_BANK_INFO_PAYING_BANK + self.DELIMITER
        return bank_info_test_payload

    def generate_contact_info_payload(self) -> str:
        contact_info_test_payload = self.SAGE_SUPPLIER_CONTACT_INDICATOR + self.DELIMITER
        contact_info_test_payload += self.SAGE_SUPPLIER_CONTACT_CODE + self.DELIMITER
        contact_info_test_payload += self.SAGE_SUPPLIER_CONTACT_TITLE + self.DELIMITER
        contact_info_test_payload += self.SAGE_SUPPLIER_CONTACT_FIRST_NAME + self.DELIMITER
        contact_info_test_payload += self.SAGE_SUPPLIER_CONTACT_LAST_NAME + self.DELIMITER
        contact_info_test_payload += self.SAGE_SUPPLIER_CONTACT_TELEPHONE + self.DELIMITER
        contact_info_test_payload += self.SAGE_SUPPLIER_CONTACT_FUNCTION + self.DELIMITER
        return contact_info_test_payload

    def generate_full_supplier_export_payload(self) -> str:
        """
        returns a test payload of a whole supplier payload from the sage BPS exports template
        - includes customer (B), addresses (A), bank info (D), and contacts (C)
        """

        supplier_payload = self.generate_test_supplier_payload() + '|'
        address_payload = self.generate_test_address_payload() + '|'
        bank_info_payload = self.generate_test_bank_info_payload() + '|'
        # let's make two contacts here, why not
        contact_info = self.generate_contact_info_payload() + '|'
        contact_info += self.generate_contact_info_payload() + '|'

        payload = supplier_payload + address_payload + bank_info_payload + contact_info

        return payload
