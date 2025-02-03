from baseintegration.importer.import_processor import BaseImportProcessor
from e2.models import CustomerCode as E2Account, Contacts as E2Contacts, Terms as E2Terms, Taxcode as E2TaxCode, \
    Shipto as E2ShipTo
from baseintegration.datamigration import logger
from paperless.objects.customers import Address, BillingAddress, Facility, Contact
from baseintegration.utils import clean_up_phone_number, safe_get, set_blank_to_default_value, is_blank, normalize_country, create_or_update_account


class AccountImportProcessor(BaseImportProcessor):

    def _process(self, e2_account_id: str):  # noqa: C901
        client = self._importer._integration._client
        logger.info(client)
        logger.info(f"Processing {e2_account_id}")
        e2_account = E2Account.objects.filter(customer_code=e2_account_id).filter(active='Y').first()
        if not e2_account:
            logger.info(f"Account with customer code {e2_account_id} not processed")
            return

        pp_account, account_is_new = create_or_update_account(integration=self._importer._integration,
                                                              erp_code=e2_account_id,
                                                              account_name=e2_account.customer_name)
        logger.info(f'Found customer with account_id {e2_account_id} in the CustomerCode table in E2')

        e2_terms = E2Terms.objects.filter(termscode=e2_account.termscode).first()
        e2_taxcode = E2TaxCode.objects.filter(taxcode=e2_account.taxcode).first()

        pp_account = self.set_pp_account_fields(e2_account, e2_taxcode, e2_terms, pp_account)

        should_import_sold_to_address = self.should_import_sold_to_address(e2_account)
        if should_import_sold_to_address:
            pp_sold_to_address = self.populate_pp_sold_to_address_from_e2_account(e2_account)
            pp_account.sold_to_address = pp_sold_to_address

        try:
            if account_is_new:
                pp_account.create()
            else:
                pp_account.update()
        except Exception as e:
            logger.warning(e)
            logger.warning(f'Encountered an error importing account: {pp_account.name} - skipping.')
            return  # TODO - verify with the team that it makes sense to bail out here

        # Pull down the related facilities and contacts for later use
        pp_facilities = Facility.list(account_id=pp_account.id)
        pp_contacts_list = Contact.filter(account_id=pp_account.id)
        pp_contacts = [Contact.get(id=c.id) for c in pp_contacts_list]

        # Optionally, import the E2 billing address as a billing address in Paperless Parts
        should_import_billing_address = self.should_import_billing_address(e2_account)
        if should_import_billing_address:
            pp_billing_address = self.get_pp_billing_address(pp_account)
            pp_billing_address, is_billing_address_new = \
                self.populate_pp_billing_address_from_e2_account(e2_account, pp_billing_address)

            try:
                if is_billing_address_new:
                    logger.info(f'Creating new billing address for account {e2_account_id}')
                    pp_billing_address.create(pp_account.id)
                else:
                    logger.info(f'Updating billing address for account {e2_account_id}')
                    pp_billing_address.update()
            except Exception as e:
                logger.warning(f'Failed to create/update billing address for account {e2_account_id} | {str(e)}')

        # Optionally, import the E2 shipping address(es) as facilities in Paperless Parts
        e2_ship_to_records = E2ShipTo.objects.filter(custcode=e2_account.customer_code)
        for e2_ship_to in e2_ship_to_records:
            if e2_ship_to is not None:

                should_import_shipping_address = self.should_import_shipping_address(e2_ship_to)
                if should_import_shipping_address:

                    try:
                        pp_facility = self.get_matching_pp_facility(e2_ship_to, pp_facilities)
                        pp_facility, is_facility_new = self.populate_pp_facility_from_e2_shipping_address(e2_ship_to, pp_facility)
                        if is_facility_new:
                            logger.info(f'Creating new facility {pp_facility.name} for account {e2_account_id}')
                            pp_facility.create(pp_account.id)
                        else:
                            logger.info(f'Updating facility {pp_facility.name} for account {e2_account_id}')
                            pp_facility.update()
                    except Exception as e:
                        logger.warning(f'Failed to create/update facility {e2_account_id} | {str(e)}')

        # Create Paperless Parts records for the associated contacts
        should_import_contacts = self.should_import_contacts()
        if should_import_contacts:
            e2_contacts = E2Contacts.objects.filter(code=e2_account_id).filter(active='Y')
            for i, e2_contact in enumerate(e2_contacts):

                pp_contact = self.get_matching_pp_contact(e2_contact, pp_contacts)
                pp_contact, is_contact_new = self.populate_pp_contact_from_e2_contact(e2_contact, pp_account, pp_contact)
                try:
                    if pp_contact is not None:
                        if is_contact_new:
                            logger.info(f'Creating new contact {pp_contact.email} for account {e2_account_id}')
                            pp_contact.create()
                        else:
                            logger.info(f'Updating contact {pp_contact.email} for account {e2_account_id}')
                            pp_contact.update()
                except Exception as e:
                    logger.warning(e)
                    logger.warning(f'Encountered an error importing contact: {pp_contact.email} - skipping.')

    def should_import_contacts(self):
        should_import_contacts = self._importer.erp_config.should_import_contacts
        return should_import_contacts

    def should_import_shipping_address(self, e2_ship_to):
        if not self._importer.erp_config.should_import_shipping_addresses:
            return False

        is_shipping_address_blank = self.determine_if_shipping_address_is_blank(e2_ship_to)
        is_shipping_address_incomplete = self.determine_if_shipping_address_is_incomplete(e2_ship_to)
        should_import_shipping_address = True
        if self._importer.erp_config.should_skip_incomplete_addresses and is_shipping_address_incomplete:
            should_import_shipping_address = False
        if is_shipping_address_blank:
            should_import_shipping_address = False
        return should_import_shipping_address

    def should_import_billing_address(self, e2_account):
        if not self._importer.erp_config.should_import_billing_address:
            return False

        is_billing_address_blank = self.determine_if_billing_address_is_blank(e2_account)
        is_billing_address_incomplete = self.determine_if_billing_address_is_incomplete(e2_account)
        should_import_billing_address = True
        if self._importer.erp_config.should_skip_incomplete_addresses and is_billing_address_incomplete:
            should_import_billing_address = False
        if is_billing_address_blank:
            should_import_billing_address = False
        return should_import_billing_address

    def should_import_sold_to_address(self, e2_account):
        if not self._importer.erp_config.should_import_sold_to_address:
            return False

        is_billing_address_blank = self.determine_if_billing_address_is_blank(e2_account)
        is_billing_address_incomplete = self.determine_if_billing_address_is_incomplete(e2_account)
        should_import_sold_to_address = True
        if self._importer.erp_config.should_skip_incomplete_addresses and is_billing_address_incomplete:
            should_import_sold_to_address = False
        if is_billing_address_blank:
            should_import_sold_to_address = False
        return should_import_sold_to_address

    def get_pp_billing_address(self, pp_account):
        # E2 only allows one billing address per customer so we must assume that the first billing address for
        # an account in Paperless Parts is the billing address in E2 (and any additional billing addresses in
        # Paperless Parts will be ignored)
        pp_billing_address = pp_account.billing_addresses[0] if pp_account.billing_addresses else None
        return pp_billing_address

    def get_matching_pp_contact(self, e2_contact, pp_contacts):
        # TODO - Once we have ERP codes for facilities, use the ShipTo_ID instead of the location name to check for
        #  matching records
        email = e2_contact.email
        if email:
            for c in pp_contacts:
                if c.email.lower() == email.lower():
                    return c
        return None

    def populate_pp_contact_from_e2_contact(self, e2_contact, pp_account, pp_contact):
        is_contact_new = False

        company_erp_code = e2_contact.code
        email = e2_contact.email
        try:
            split_contact = e2_contact.contact.split(' ', 1)
            first_name = split_contact[0]
            last_name = split_contact[1]
        except:
            first_name = e2_contact.contact if e2_contact is not None else 'Contact'
            last_name = company_erp_code
        if email is None or not email:
            return None, False  # Email address is required for PP contacts
        account_id = safe_get(pp_account, 'id')

        if pp_contact is None:
            is_contact_new = True
            pp_contact = Contact(
                account_id=account_id,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
        else:
            pp_contact.email = email
            pp_contact.first_name = first_name
            pp_contact.last_name = last_name

        notes = e2_contact.comments
        phone = clean_up_phone_number(e2_contact.phone)
        phone_ext = e2_contact.extension

        pp_contact.notes = notes
        pp_contact.phone = phone
        pp_contact.phone_ext = phone_ext
        return pp_contact, is_contact_new

    def get_matching_pp_facility(self, e2_ship_to, pp_facilities):
        # TODO - Once we have ERP codes for facilities, use the ShipTo_ID instead of the location name to check for
        #  matching records
        shipping_name = e2_ship_to.location
        facility = None
        for f in pp_facilities:
            if f.name == shipping_name:
                facility = f
        return facility

    def populate_pp_facility_from_e2_shipping_address(self, e2_ship_to, pp_facility):
        is_facility_new = False
        if pp_facility is None:
            is_facility_new = True

        shipping_address1 = set_blank_to_default_value(e2_ship_to.saddr1, None)
        shipping_address2 = set_blank_to_default_value(e2_ship_to.saddr2, None)
        shipping_name = set_blank_to_default_value(e2_ship_to.location, None)
        shipping_city = set_blank_to_default_value(e2_ship_to.scity, None)
        shipping_country = set_blank_to_default_value(normalize_country(e2_ship_to.scountry), None)

        # TODO - the Paperless Parts Facility model currently does not allow Null for the attention field. Until that
        #  is resolved, write an empty string if the ship contact is Null in E2. If/when the empty string is written
        #  back to E2, the empty string will be rendered the same as a Null, so this is not as bad as using a
        #  placeholder string like 'N/A'
        shipping_contact = set_blank_to_default_value(e2_ship_to.shipcontact, '')

        shipping_postal_code = set_blank_to_default_value(e2_ship_to.szipcode, None)
        shipping_state = set_blank_to_default_value(e2_ship_to.sstate, None)

        shipping_address = Address(
            address1=shipping_address1,
            address2=shipping_address2,
            city=shipping_city,
            country=shipping_country,
            postal_code=shipping_postal_code,
            state=shipping_state,
        )

        if is_facility_new:
            pp_facility = Facility(
                address=shipping_address,
                name=shipping_name,
                attention=shipping_contact,
            )
        else:
            pp_facility.address = shipping_address
            pp_facility.name = shipping_name
            pp_facility.attention = shipping_contact

        return pp_facility, is_facility_new

    def determine_if_shipping_address_is_incomplete(self, e2_ship_to):
        required_shipping_address_fields = (
            e2_ship_to.saddr1, e2_ship_to.scity, e2_ship_to.scountry,
            e2_ship_to.szipcode, e2_ship_to.sstate)
        is_shipping_address_incomplete = any(
            [is_blank(field) for field in required_shipping_address_fields])
        return is_shipping_address_incomplete

    def determine_if_shipping_address_is_blank(self, e2_ship_to):
        shipping_address_fields = (e2_ship_to.saddr1, e2_ship_to.saddr2, e2_ship_to.scity,
                                   e2_ship_to.scountry, e2_ship_to.szipcode, e2_ship_to.sstate)
        is_shipping_address_blank = all([is_blank(field) for field in shipping_address_fields])
        return is_shipping_address_blank

    def populate_pp_billing_address_from_e2_account(self, e2_account, pp_billing_address):
        is_billing_address_new = False
        if pp_billing_address is None:
            is_billing_address_new = True

        # Assign the billing information for this account
        billing_address1 = set_blank_to_default_value(e2_account.b_addr1, None)
        billing_address2 = set_blank_to_default_value(e2_account.b_addr2, None)
        billing_city = set_blank_to_default_value(e2_account.b_city, None)
        billing_country = set_blank_to_default_value(normalize_country(e2_account.b_country), None)
        billing_postal_code = set_blank_to_default_value(e2_account.b_zip_code, None)
        billing_state = set_blank_to_default_value(e2_account.b_state, None)

        # Set the billing address to be the billing address from E2
        if is_billing_address_new:
            pp_billing_address = BillingAddress(
                address1=billing_address1,
                address2=billing_address2,
                city=billing_city,
                country=billing_country,
                postal_code=billing_postal_code,
                state=billing_state,
            )
        else:
            pp_billing_address.address1 = billing_address1
            pp_billing_address.address2 = billing_address2
            pp_billing_address.city = billing_city
            pp_billing_address.country = billing_country
            pp_billing_address.postal_code = billing_postal_code
            pp_billing_address.state = billing_state

        return pp_billing_address, is_billing_address_new

    def populate_pp_sold_to_address_from_e2_account(self, e2_account):

        # Assign the billing information for this account
        billing_address1 = set_blank_to_default_value(e2_account.b_addr1, None)
        billing_address2 = set_blank_to_default_value(e2_account.b_addr2, None)
        billing_city = set_blank_to_default_value(e2_account.b_city, None)
        billing_country = set_blank_to_default_value(normalize_country(e2_account.b_country), None)
        billing_postal_code = set_blank_to_default_value(e2_account.b_zip_code, None)
        billing_state = set_blank_to_default_value(e2_account.b_state, None)

        # Set the sold to address to be the billing address from E2
        pp_sold_to_address = Address(
            address1=billing_address1,
            address2=billing_address2,
            city=billing_city,
            country=billing_country,
            postal_code=billing_postal_code,
            state=billing_state
        )
        return pp_sold_to_address

    def determine_if_billing_address_is_incomplete(self, e2_account):
        required_billing_address_fields = (e2_account.b_addr1, e2_account.b_city, e2_account.b_country,
                                           e2_account.b_zip_code, e2_account.b_state)
        is_billing_address_incomplete = any([is_blank(field) for field in required_billing_address_fields])
        return is_billing_address_incomplete

    def determine_if_billing_address_is_blank(self, e2_account):
        billing_address_fields = (e2_account.b_addr1, e2_account.b_addr2, e2_account.b_city, e2_account.b_country,
                                  e2_account.b_zip_code, e2_account.b_state)
        is_billing_address_blank = all([is_blank(field) for field in billing_address_fields])
        return is_billing_address_blank

    def set_pp_account_fields(self, e2_account, e2_taxcode, e2_terms, pp_account):
        # Create a Paperless Parts record for this account
        name = e2_account.customer_name
        erp_code = e2_account.customer_code
        notes = e2_account.comments2  # comments2 is the "About Customer" field in E2. comments1 is "To Customer", which we don't want
        payment_terms = safe_get(e2_terms, 'termscode')
        payment_terms_period = safe_get(e2_terms, 'netduedays')
        phone = clean_up_phone_number(e2_account.phone)
        phone_ext = None  # There isn't a separate phone extension field in E2
        purchase_orders_enabled = True
        tax_exempt = self.get_tax_exempt_status(e2_taxcode)
        url = e2_account.website
        pp_account.name = name
        pp_account.erp_code = erp_code
        pp_account.notes = notes
        pp_account.payment_terms = payment_terms
        pp_account.payment_terms_period = payment_terms_period
        pp_account.phone = phone
        pp_account.phone_ext = phone_ext
        pp_account.purchase_orders_enabled = purchase_orders_enabled
        pp_account.tax_exempt = tax_exempt
        pp_account.url = url

        return pp_account

    def get_tax_exempt_status(self, e2_taxcode):
        tax_exempt = (e2_taxcode.taxcode == self._importer.erp_config.tax_exempt_code or e2_taxcode.taxfactor == 0) \
            if e2_taxcode is not None else False
        return tax_exempt
