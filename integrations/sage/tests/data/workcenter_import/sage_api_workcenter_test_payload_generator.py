"""
This class provides some test data mirroring what we get from the MWS exports template - which gets work center data
All field names in this file come from sage
We can get 1 possible entity from a single payload each prefixed with an indicator
- E: work_center data
"""


class SageApiWorkCenterTestPayloadGenerator:
    # delimiter for the ifile we are reading from
    DELIMITER = ';'

    # test work center data
    SAGE_WORK_CENTER_INDICATOR = 'E'
    SAGE_WORK_CENTER_WORK_CENTER = 'work_center_work_center'
    SAGE_WORK_CENTER_GROUP = 'C123456'
    SAGE_WORK_CENTER_MANUFACTURING_SITE = 'work_center_company_name'
    SAGE_WORK_CENTER_TITLE = 'work_center_short_description'
    SAGE_WORK_CENTER_SHORT_DESCRIPTION = 'work_center_acronym'
    SAGE_WORK_CENTER_TYPE = 'MAIN'
    SAGE_WORK_COSTING_DIMENSION = ' work_center_currency'
    SAGE_WORK_CENTER_STORAGE_LOCATION = 'work_center_site_text_id_no'
    SAGE_WORK_CENTER_WEEKLY_STRUCTURE = 'work_center_sic_code'
    SAGE_WORK_CENTER_NO_RESOURCES = 'work_center_eu_vat_no'
    SAGE_WORK_CENTER_PERCENT_EFFICIENCY = 'work_center_tax_rule'
    SAGE_WORK_CENTER_SHRINKAGE_IN_PERCENT = 'work_center_payment_term'
    SAGE_WORK_CENTER_AUTOMATIC_CLOSING_PERCENT = 'work_center_accounting_code'

    def generate_test_work_center_payload(self) -> str:
        """
        returns a test payload of  work_center data, this is the only data in the payload
        """
        work_center_test_payload = self.SAGE_WORK_CENTER_INDICATOR + self.DELIMITER
        work_center_test_payload += self.SAGE_WORK_CENTER_WORK_CENTER + self.DELIMITER
        work_center_test_payload += self.SAGE_WORK_CENTER_GROUP + self.DELIMITER
        work_center_test_payload += self.SAGE_WORK_CENTER_MANUFACTURING_SITE + self.DELIMITER
        work_center_test_payload += self.SAGE_WORK_CENTER_TITLE + self.DELIMITER
        work_center_test_payload += self.SAGE_WORK_CENTER_SHORT_DESCRIPTION + self.DELIMITER
        work_center_test_payload += self.SAGE_WORK_CENTER_TYPE + self.DELIMITER
        work_center_test_payload += self.SAGE_WORK_COSTING_DIMENSION + self.DELIMITER
        work_center_test_payload += self.SAGE_WORK_CENTER_STORAGE_LOCATION + self.DELIMITER
        work_center_test_payload += self.SAGE_WORK_CENTER_WEEKLY_STRUCTURE + self.DELIMITER
        work_center_test_payload += self.SAGE_WORK_CENTER_NO_RESOURCES + self.DELIMITER
        work_center_test_payload += self.SAGE_WORK_CENTER_PERCENT_EFFICIENCY + self.DELIMITER
        work_center_test_payload += self.SAGE_WORK_CENTER_SHRINKAGE_IN_PERCENT + self.DELIMITER
        work_center_test_payload += self.SAGE_WORK_CENTER_AUTOMATIC_CLOSING_PERCENT + self.DELIMITER

        return work_center_test_payload + '|'
