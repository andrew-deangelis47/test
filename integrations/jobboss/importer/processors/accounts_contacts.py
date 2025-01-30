from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.datamigration import logger
import jobboss.models as jb
from paperless.objects.customers import Contact, Address, BillingAddress, Facility, Money, Account
from baseintegration.utils import clean_up_phone_number, safe_get, set_blank_to_default_value, create_or_update_account
from typing import List, Union, Optional
from django.db import connection
from django.db.utils import ProgrammingError


class AccountImportProcessor(BaseImportProcessor):

    def _process(self, account_id: str = None):
        jb_customer = jb.Customer.objects.filter(customer=account_id).first()

        valid_billing_addresses, valid_shipping_addresses = self.get_lists_of_valid_addresses(jb_customer.customer)
        pp_account: Optional[Account] = self.update_or_create_pp_accounts(jb_customer, valid_billing_addresses)

        if pp_account:
            if self._importer.erp_config.should_import_billing_addresses:
                self.update_or_create_pp_billing_addresses(pp_account, valid_billing_addresses)

            if self._importer.erp_config.should_import_shipping_addresses:
                self.update_or_create_pp_facilities(pp_account, valid_shipping_addresses)

            if self._importer.erp_config.should_import_contacts:
                self.update_or_create_pp_contacts(pp_account)

        return pp_account

    def update_or_create_pp_accounts(self, jb_customer: jb.Customer, valid_billing_addresses: List[jb.Address]
                                     ) -> Union[Account, None]:  # noqa: C901
        # Check if inactive customers should be imported
        if jb_customer.status == "Inactive" and self._importer.erp_config.should_import_inactive_customers is False:
            logger.info(f"Customer ID: {jb_customer.customer} is inactive. Skipping.")
            return None

        # Make sure that a name and erp code are present to create a complete Paperless Parts Account
        if not jb_customer.name or not jb_customer.customer:
            logger.info(f"Cannot import ACCOUNT_ID='{jb_customer.customer}'this account due to missing JB Customer name"
                        f" or JB Customer ERP Code. Skipping import...")
            return None

        # Create basic account, assign additional parameters later...
        pp_account, account_is_new = create_or_update_account(integration=self._importer._integration,
                                                              erp_code=jb_customer.customer,
                                                              account_name=jb_customer.name)
        pp_account = self.assign_account_attributes(pp_account, jb_customer)

        # Set sold to address as the first billing address if a valid address exists
        if len(valid_billing_addresses) > 0:
            pp_account = self.set_pp_sold_to_address(pp_account, valid_billing_addresses[0])

        # Update or create PP Account
        try:
            if account_is_new:
                pp_account.create()
                logger.info(f"Created new Paperless Parts Account record for {pp_account.name}")
                return pp_account
            else:
                pp_account.update()
                logger.info(f"Updated existing Paperless Parts Account: {pp_account.name}")
                return pp_account
        except Exception as e:
            logger.warning(f'Encountered an error importing account: {pp_account.name} - skipping.  Error: {e}')
            return pp_account

    def set_pp_sold_to_address(self, pp_account: Account, address: jb.Address) -> Account:
        # Normalize the data in case anything is missing or completely mangled - assigns default values
        erp_code, billing_address1, billing_address2, billing_city, billing_state, billing_postal_code, \
            billing_country = self.normalized_address(address)

        # Set normalized attributes to the sold to address
        sold_to_address = Address(
            erp_code=erp_code,
            address1=billing_address1,
            address2=billing_address2,
            city=billing_city,
            country=billing_country,
            postal_code=billing_postal_code,
            state=billing_state
        )
        pp_account.sold_to_address = sold_to_address
        return pp_account

    def update_or_create_pp_billing_addresses(self, pp_account: Account, valid_billing_addresses: List[jb.Address]):
        logger.info("Creating valid billing addresses.")
        pp_billing_addresses: List[BillingAddress] = pp_account.billing_addresses

        for address in valid_billing_addresses:

            erp_code, address1, address2, city, state, postal_code, country = self.normalized_address(address)
            existing_billing_address, billing_address_is_new = self.check_if_address_already_exists(
                pp_billing_addresses, erp_code, address1, city, state, postal_code, country)

            billing_address = BillingAddress(
                erp_code=erp_code,
                address1=address1,
                address2=address2,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country
            )

            try:
                if billing_address_is_new:
                    logger.info("Creating new billing address.")
                    billing_address.create(pp_account.id)
                else:
                    logger.info("Updating existing billing address.")
                    existing_billing_address.erp_code = erp_code
                    existing_billing_address.address2 = address2
                    existing_billing_address.update()
            except Exception as e:
                logger.warning(f"Encountered error importing billing address for account {pp_account.name}. "
                               f"Error: {e}")

    def update_or_create_pp_facilities(self, pp_account: Account, valid_shipping_addresses: List[jb.Address]):
        logger.info("Creating valid shipping addresses.")
        pp_facilities: List[Facility] = Facility.list(account_id=pp_account.id)

        for address in valid_shipping_addresses:

            erp_code, address1, address2, city, state, postal_code, country = self.normalized_address(address)
            existing_facility, facility_is_new = self.check_if_facility_is_new(
                pp_facilities, erp_code, address1, city, state, postal_code, country)

            shipping_address = Address(
                erp_code=erp_code,
                address1=address1,
                address2=address2,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country
            )
            facility = Facility(
                address=shipping_address,
                name=address.name,
                attention=address.name,
            )
            try:
                if facility_is_new:
                    logger.info("Creating new Facility")
                    facility.create(pp_account.id)
                else:
                    logger.info("Updating existing Facility")
                    existing_facility.address = shipping_address
                    existing_facility.attention = str(address.name)
                    existing_facility.name = str(address.name)
                    existing_facility.update()
            except Exception as e:
                logger.info(f"Encountered error importing shipping address for account {pp_account.name}.  Error: {e}")

    def get_contact_status_field_if_exists(self, contact_key: str) -> [None, bool]:
        """
        Not all Jobboss instances will have a "Status" field for contacts
        This function gets the status field of a contact if it exists
        If this Status field does not exist we return None
        """
        with connection.cursor() as cursor:
            try:
                cursor.execute("SELECT Status FROM Contact WHERE ContactKey = %s", [contact_key])
                row = cursor.fetchone()
            except ProgrammingError:
                return None

        if len(row) == 0:
            return None
        return row[0]

    def should_skip_contact_import(self, jb_contact: jb.Contact):
        """
        We will skip importing the contact under 3 conditions
        1) customer config "should_import_inactive_contacts" exists and is set to False
        2) The customer's JB instance has a "Status" column for contacts
        3) The contact in JB is marked inactive
        """

        if self._importer.erp_config.should_import_inactive_contacts:
            return False

        contact_status = self.get_contact_status_field_if_exists(jb_contact.contactkey)
        if contact_status is None:
            return False

        if contact_status:
            return False

        return True

    def update_or_create_pp_contacts(self, pp_account: Account):
        # Get JobBOSS contacts associated with the Account ERP code
        jb_contacts = jb.Contact.objects.filter(customer=pp_account.erp_code)
        logger.info(f'Found {len(jb_contacts)} contacts associated with {pp_account.name}')

        # Get list of existing contacts associated with the account
        pp_contacts_by_account_id = Contact.filter(account_id=pp_account.id)
        pp_contacts = [Contact.get(id=c.id) for c in pp_contacts_by_account_id]

        for jb_contact in jb_contacts:

            # if configured, do not import inactive contacts
            if self.should_skip_contact_import(jb_contact):
                logger.info(f'Contact {jb_contact.contact_name} is inactive, skipping import')
                continue

            # Check for a match between existing Paperless contact email and JobBOSS contact email
            pp_contact = self.get_matching_pp_contact(jb_contact, pp_contacts)

            first_name, last_name = self.get_names(jb_contact.contact_name)
            phone = clean_up_phone_number(jb_contact.phone)
            notes = self.get_notes(jb_contact)
            phone_ext = jb_contact.phone_ext

            # If Paperless contact exists, move on, else, create the new contact
            if pp_contact is not None:
                contact_is_new = False
                pp_contact = self.update_contact_attributes(pp_contact, first_name, last_name, notes, phone, phone_ext)
            else:
                contact_is_new = True
                email = self.get_email(jb_contact)
                if not email:
                    logger.warning(f"No email for contact {first_name} {last_name} - skipping importing this contact")
                    continue
                pp_contact = Contact(
                    account_id=safe_get(pp_account, 'id'),
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    notes=notes,
                    phone=phone,
                    phone_ext=phone_ext,
                )

            # Create a contact if the contact does not already exist, else, update the contact
            try:
                if contact_is_new:
                    pp_contact.create()
                    logger.info("Created new Paperless Parts contact.")
                else:
                    pp_contact.update()
                    logger.info("Updated attributes on existing Paperless Parts contact")
            except Exception as e:
                logger.warning(f'Encountered an error importing contact: {pp_contact.email} - skipping. Error: {e}')

    def get_payment_terms_period(self, terms):  # noqa: C901
        period = 30
        if terms:
            terms = terms.strip().lower()
            if 'net 30' in terms:
                period = 30
            elif 'net 15' in terms:
                period = 15
            elif 'net 10' in terms:
                period = 10
            elif 'net 21' in terms:
                period = 21
            elif 'net 45' in terms:
                period = 45
            elif 'net 60' in terms:
                period = 60
            elif 'net 90' in terms:
                period = 90
            elif 'net 40' in terms:
                period = 40
            elif 'net 75' in terms:
                period = 75
        return period

    def get_names(self, full_name):
        first_name = "FIRST_NAME"
        last_name = "LAST_NAME"
        if full_name:
            fragments = full_name.split(' ')
            if len(fragments) > 0:
                first_name = fragments[0]
            if len(fragments) > 1:
                last_name = ' '.join(fragments[1:])
        return first_name, last_name

    def get_email(self, jb_contact):
        if jb_contact.email_address is not None:
            return jb_contact.email_address
        else:
            return None

    def get_notes(self, jb_contact):
        notes = str(jb_contact.contact) + " "
        if jb_contact.title:
            notes += f'\nTitle: {jb_contact.title}'
        if jb_contact.fax:
            notes += f'\nFax: {jb_contact.fax}'
        if jb_contact.cell_phone:
            notes += f'\nCell: {jb_contact.cell_phone}'
        return notes

    def normalize_country(self, country):
        if country is not None and country.strip() == 'US':
            return 'USA'
        elif country is not None and country.strip() == 'CN' or country is not None and country.strip() == 'CA':
            return 'CAN'
        else:
            return country

    def normalized_address(self, address: jb.Address):
        erp_code = str(address.addresskey)
        billing_address1 = set_blank_to_default_value(address.line1, 00000)
        billing_address2 = set_blank_to_default_value(address.line2, None)
        billing_city = set_blank_to_default_value(address.city, 'CITY')
        billing_state = set_blank_to_default_value(address.state, "AL")
        billing_postal_code = set_blank_to_default_value(address.zip, 00000)
        billing_country = set_blank_to_default_value(self.normalize_country(address.country), "USA")
        return erp_code, billing_address1, billing_address2, billing_city, billing_state, billing_postal_code, billing_country

    def assign_account_attributes(self, pp_account: Account, jb_customer: jb.Customer) -> Account:
        pp_account.name = str(jb_customer.name)
        pp_account.erp_code = str(jb_customer.customer)
        pp_account.credit_line = Money(jb_customer.credit_limit) if jb_customer.credit_limit is not None else None
        pp_account.notes = jb_customer.note_text
        pp_account.payment_terms = jb_customer.terms if jb_customer.terms is not None else "Net 30"
        pp_account.payment_terms_period = self.get_payment_terms_period(jb_customer.terms)
        pp_account.phone = None  # JB doesn't have phone numbers on Customer records
        pp_account.phone_ext = None
        pp_account.purchase_orders_enabled = jb_customer.accept_bo if jb_customer is not None else False
        pp_account.tax_exempt = True if jb_customer.tax_code is None else False
        pp_account.tax_rate = None
        pp_account.url = jb_customer.url
        return pp_account

    def get_matching_pp_contact(self, jb_contact, pp_contacts):
        email = jb_contact.email_address
        contact = None
        for pp_contact in pp_contacts:
            if pp_contact.email == email:
                contact = pp_contact
        return contact

    def update_contact_attributes(self, pp_contact, first_name, last_name, notes, phone, phone_ext):
        pp_contact.first_name = first_name
        pp_contact.last_name = last_name
        pp_contact.notes = notes
        pp_contact.phone = phone
        pp_contact.phone_ext = phone_ext
        return pp_contact

    def check_if_address_already_exists(self, pp_billing_addresses: List[BillingAddress], erp_code, address1, city,
                                        state, postal_code, country) -> (Optional[BillingAddress], bool):
        for existing_address in pp_billing_addresses:
            if existing_address.erp_code == erp_code:
                return existing_address, False

            elif (existing_address.address1 == address1) and (existing_address.city == city) and (
                    existing_address.state == state) and (existing_address.postal_code == postal_code) and (
                    existing_address.country == country):
                return existing_address, False

        return None, True

    def check_if_facility_is_new(self, pp_facilities: List[Facility], erp_code, address1, city, state, postal_code,
                                 country) -> (Optional[Facility], bool):
        for existing_facility in pp_facilities:
            existing_address = existing_facility.address

            if existing_address.erp_code == erp_code:
                return existing_facility, False

            elif (existing_address.address1 == address1) and (existing_address.city == city) and (
                    existing_address.state == state) and (existing_address.postal_code == postal_code) and (
                    existing_address.country == country):
                return existing_facility, False

        return None, True

    def validate_address(self, jb_address: jb.Address) -> bool:
        # Check if address has enough criteria for Paperless Parts address validation
        address_fields = (jb_address.addresskey, jb_address.line1, jb_address.city, jb_address.state, jb_address.zip)
        address_is_valid = all([field is not None for field in address_fields])
        return address_is_valid

    def get_lists_of_valid_addresses(self, jb_customer_id) -> (list, list):
        valid_billing_addresses = []
        valid_shipping_addresses = []

        # Query a list of JobBOSS addresses associated with the account. Create arrays to capture types of addresses.
        jb_customer_addresses = jb.Address.objects.filter(customer=jb_customer_id)

        # Iterate all addresses, validate them, sort them into lists of billing and shipping addresses
        for jb_address in jb_customer_addresses:
            address_is_valid = self.validate_address(jb_address)

            if address_is_valid and jb_address.billable:
                valid_billing_addresses.append(jb_address)
            if address_is_valid and jb_address.shippable:
                valid_shipping_addresses.append(jb_address)

        return valid_billing_addresses, valid_shipping_addresses
