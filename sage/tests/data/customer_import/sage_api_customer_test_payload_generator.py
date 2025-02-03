"""
This class provides some test data mirroring what we get from the YBPCPPEXP exports template - which gets customer data
All field names in this file come from sage
We can get 4 possible entities from a single customer payload (in this order), each prefixed with an indicator
- B: customer data
- A: address data
- D: ship to customer data
- C: contact data
- R: bank information
"""


class SageApiCustomerTestPayloadGenerator:
    # delimiter for the ifile we are reading from
    DELIMITER = ';'

    # test customer data
    SAGE_CUSTOMER_INDICATOR = 'B'
    SAGE_CUSTOMER_CATEGORY = 'customer_category'
    SAGE_CUSTOMER_CUSTOMER = 'C123456'
    SAGE_CUSTOMER_COMPANY_NAME = 'customer_company_name'
    SAGE_CUSTOMER_SHORT_DESCRIPTION = 'customer_short_description'
    SAGE_CUSTOMER_ACRONYM = 'customer_acronym'
    # just called 'address' in sage
    SAGE_CUSTOMER_ADDRESS_0 = 'BILL'
    # just called 'address' in sage
    SAGE_CUSTOMER_ADDRESS_1 = 'BILL'
    SAGE_CUSTOMER_DEFAULT_ADDRESS = 'BILL'
    SAGE_CUSTOMER_SHIP_TO_CUSTOMER_ADDRESS = ' SHIP'
    SAGE_CUSTOMER_CURRENCY = ' customer_currency'
    SAGE_CUSTOMER_SITE_TAX_ID_NO = 'customer_site_text_id_no'
    SAGE_CUSTOMER_SIC_CODE = 'customer_sic_code'
    SAGE_CUSTOMER_EU_VAT_NO = 'customer_eu_vat_no'
    SAGE_CUSTOMER_BILL_TO_CUSTOMER = 'C123456'
    SAGE_CUSTOMER_TAX_RULE = 'customer_tax_rule'
    SAGE_CUSTOMER_PAYMENT_TERM = 'customer_payment_term'
    SAGE_CUSTOMER_ACCOUNTING_CODE = 'customer_accounting_code'
    SAGE_CUSTOMER_STATISTICAL_GROUP = 'customer_statistical_group'
    SAGE_CUSTOMER_AUTHORIZED_CREDIT = 'customer_authorized_credit'
    SAGE_CUSTOMER_COMMISSION_CATEGORY = 'customer_commission_category'
    SAGE_CUSTOMER_SALES_REP = 'customer_sales_rep'
    # just called 'order text' in sage
    SAGE_CUSTOMER_ORDER_TEXT_0 = 'customer_order_text_0'
    # just called 'order text' in sage
    SAGE_CUSTOMER_ORDER_TEXT_1 = 'customer_order_text_0'
    # just called 'invoice text' in sage
    SAGE_CUSTOMER_INVOICE_TEXT_0 = 'customer_invoice_text_0'
    # just called 'invoice text' in sage
    SAGE_CUSTOMER_INVOICE_TEXT_1 = 'customer_invoice_text_0'

    # test address payload
    SAGE_ADDRESS_INDICATOR = 'A'
    SAGE_ADDRESS_ADDRESS_BILL = 'BILL'
    SAGE_ADDRESS_ADDRESS_SHIP = 'SHIP'
    SAGE_ADDRESS_DESCRIPTION = 'address_description'
    # just called 'address line' in sage
    SAGE_ADDRESS_ADDRESS_LINE_0 = 'address_address_line_0'
    # just called 'address line' in sage
    SAGE_ADDRESS_ADDRESS_LINE_1 = 'address_address_line_1'
    # just called 'address line' in sage
    SAGE_ADDRESS_ADDRESS_LINE_2 = 'address_address_line_2'
    SAGE_ADDRESS_POSTAL_CODE = 'address_postal_code'
    SAGE_ADDRESS_CITY = 'address_city'
    SAGE_ADDRESS_COUNTRY = 'address_country'
    SAGE_ADDRESS_TELEPHONE = 'address_telephone'
    SAGE_ADDRESS_FAX = 'address_fax'
    SAGE_ADDRESS_BY_DEFAULT = 'address_by_default'
    SAGE_ADDRESS_STATE = 'address_state'

    # test customer payload
    SAGE_CONTACT_INDICATOR = 'C'
    SAGE_CONTACT_CODE = 'contact_code'
    SAGE_CONTACT_TITLE = 'contact_title'
    SAGE_CONTACT_FIRST_NAME = 'contact_first_name'
    SAGE_CONTACT_LAST_NAME = 'contact_last_name'
    SAGE_CONTACT_TELEPHONE = 'contact_telephone'
    SAGE_CONTACT_FUNCTION = 'contact_function'
    SAGE_CONTACT_EMAIL = 'contact_email'

    def generate_test_customer_payload(self) -> str:
        """
        returns a test payload of ONLY customer data (B)
        """
        customer_test_payload = self.SAGE_CUSTOMER_INDICATOR + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_CATEGORY + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_CUSTOMER + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_COMPANY_NAME + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_SHORT_DESCRIPTION + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_ACRONYM + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_ADDRESS_0 + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_ADDRESS_1 + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_DEFAULT_ADDRESS + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_SHIP_TO_CUSTOMER_ADDRESS + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_CURRENCY + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_SITE_TAX_ID_NO + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_SIC_CODE + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_EU_VAT_NO + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_BILL_TO_CUSTOMER + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_TAX_RULE + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_PAYMENT_TERM + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_ACCOUNTING_CODE + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_STATISTICAL_GROUP + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_AUTHORIZED_CREDIT + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_COMMISSION_CATEGORY + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_SALES_REP + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_ORDER_TEXT_0 + self.DELIMITER
        customer_test_payload += self.SAGE_CUSTOMER_ORDER_TEXT_1 + self.DELIMITER

        return customer_test_payload

    def generate_test_address_payload(self, address_type: str) -> str:
        """
        returns a test payload of ONLY address data (A)
        - accepts a parameter address_type which is either 'SHIP' or 'BILL'
        - to have a full customer payload we need two addresses at min, 'SHIP' and 'BILL'
        """
        address_test_payload = self.SAGE_ADDRESS_INDICATOR + self.DELIMITER

        # billing or shipping?
        if address_type == 'BILL':
            address_test_payload += self.SAGE_ADDRESS_ADDRESS_BILL + self.DELIMITER
        else:
            address_test_payload += self.SAGE_ADDRESS_ADDRESS_SHIP + self.DELIMITER
        address_test_payload += self.SAGE_ADDRESS_DESCRIPTION + self.DELIMITER
        address_test_payload += self.SAGE_ADDRESS_ADDRESS_LINE_0 + self.DELIMITER
        address_test_payload += self.SAGE_ADDRESS_ADDRESS_LINE_1 + self.DELIMITER
        address_test_payload += self.SAGE_ADDRESS_ADDRESS_LINE_2 + self.DELIMITER
        address_test_payload += self.SAGE_ADDRESS_POSTAL_CODE + self.DELIMITER
        address_test_payload += self.SAGE_ADDRESS_CITY + self.DELIMITER
        address_test_payload += self.SAGE_ADDRESS_COUNTRY + self.DELIMITER
        address_test_payload += self.SAGE_ADDRESS_TELEPHONE + self.DELIMITER
        address_test_payload += self.SAGE_ADDRESS_FAX + self.DELIMITER
        address_test_payload += self.SAGE_ADDRESS_BY_DEFAULT + self.DELIMITER
        address_test_payload += self.SAGE_ADDRESS_STATE + self.DELIMITER

        return address_test_payload

    def generate_test_contact_payload(self, unique_id: str = None) -> str:
        """
        returns a test payload of ONLY contact data (C)
        """
        contact_payload = self.SAGE_CONTACT_INDICATOR + self.DELIMITER
        if unique_id is not None:
            contact_payload += self.SAGE_CONTACT_CODE + '_' + unique_id + self.DELIMITER
            contact_payload += self.SAGE_CONTACT_TITLE + '_' + unique_id + self.DELIMITER
            contact_payload += self.SAGE_CONTACT_FIRST_NAME + '_' + unique_id + self.DELIMITER
            contact_payload += self.SAGE_CONTACT_LAST_NAME + '_' + unique_id + self.DELIMITER
            contact_payload += self.SAGE_CONTACT_TELEPHONE + '_' + unique_id + self.DELIMITER
            contact_payload += self.SAGE_CONTACT_FUNCTION + '_' + unique_id + self.DELIMITER
            contact_payload += self.SAGE_CONTACT_EMAIL + '_' + unique_id + self.DELIMITER
        else:
            contact_payload += self.SAGE_CONTACT_CODE + self.DELIMITER
            contact_payload += self.SAGE_CONTACT_TITLE + self.DELIMITER
            contact_payload += self.SAGE_CONTACT_FIRST_NAME + self.DELIMITER
            contact_payload += self.SAGE_CONTACT_LAST_NAME + self.DELIMITER
            contact_payload += self.SAGE_CONTACT_TELEPHONE + self.DELIMITER
            contact_payload += self.SAGE_CONTACT_FUNCTION + self.DELIMITER
            contact_payload += self.SAGE_CONTACT_EMAIL + self.DELIMITER

        return contact_payload

    def generate_full_customer_export_payload(self, num_contacts: int = 1, total_num: int = 1) -> str:
        """
        returns a test payload of a whole customer payload from the sage YBPCPPEXP exports template
        - includes customer (B), addresses (A), and contacts (C)
        """
        # customer payload
        sage_customer_payload = self.generate_test_customer_payload() + '|'

        # address payload - make a billing and shipping
        sage_address_payload = ''
        sage_address_payload += self.generate_test_address_payload('BILL') + '|'
        sage_address_payload += self.generate_test_address_payload('SHIP') + '|'

        # contact payload
        sage_contact_payload = ''
        for i in range(num_contacts):
            sage_contact_payload += self.generate_test_contact_payload(str(i)) + '|'

        full_payload = sage_customer_payload + sage_address_payload + sage_contact_payload
        final_payload = ''
        for payload in range(total_num):
            final_payload += full_payload

        return final_payload
