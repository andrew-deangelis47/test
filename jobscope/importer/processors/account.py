from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.datamigration import logger
from paperless.objects.customers import Address, Facility, Contact
from baseintegration.utils import clean_up_phone_number, safe_get, set_blank_to_default_value, normalize_country, create_or_update_account


class AccountImportProcessor(BaseImportProcessor):

    def _process(self, jobscope_account_id: str):  # noqa: C901
        client = self._importer.client
        logger.info(f"Processing {jobscope_account_id}")
        jobscope_acct: dict = client.get_customer(jobscope_account_id)
        if not jobscope_acct:
            logger.info(f"Account with customer number {jobscope_acct} not processed")
            return

        pp_account, account_is_new = create_or_update_account(integration=self._importer._integration,
                                                              erp_code=jobscope_account_id,
                                                              account_name=jobscope_acct["customerName"])
        logger.info(f'Found customer with account_id {jobscope_account_id} in the customer table in jobscope')
        pp_account.erp_code = jobscope_account_id
        pp_account.name = jobscope_acct["customerName"]
        pp_account.notes = "Bill code is: " + jobscope_acct["billCode"]
        pp_sold_to_address = self.populate_pp_sold_to_address_from_e2_account(jobscope_acct)
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
        jobscope_contacts = client.get_contacts_by_customer(int(jobscope_acct["customerId"]))
        for i, jobscope_contact in enumerate(jobscope_contacts):
            logger.info(jobscope_contact)
            pp_contact = self.get_matching_pp_contact(jobscope_contact, pp_contacts)
            pp_contact, is_contact_new = self.populate_paperless_contact_from_jobscope_contact(jobscope_contact, pp_account, pp_contact)
            try:
                if pp_contact is not None:
                    if is_contact_new:
                        logger.info(f'Creating new contact {pp_contact.email} for account {jobscope_contact}')
                        pp_contact.create()
                    else:
                        logger.info(f'Updating contact {pp_contact.email} for account {jobscope_contact}')
                        pp_contact.update()
            except Exception as e:
                logger.warning(e)
                logger.warning(f'Encountered an error importing contact: {pp_contact.email} - skipping.')

        # Optionally, import the E2 shipping address(es) as facilities in Paperless Parts
        sites = client.get_sites_by_customer(int(jobscope_acct["customerId"]))
        for site in sites:
            logger.info(site)
            if not site["isShipToSite"]:
                logger.info(f"Site {site['siteName']} is not a ship to, skipping")
                continue
            pp_facility = self.get_matching_pp_facility(site, pp_facilities)
            pp_facility, is_facility_new = \
                self.populate_pp_facility_from_jobscope_shipping_address(site, pp_facility)

            try:
                if is_facility_new:
                    logger.info(f'Creating new facility {pp_facility.name} for account {jobscope_account_id}')
                    pp_facility.create(pp_account.id)
                else:
                    logger.info(f'Updating facility {pp_facility.name} for account {jobscope_account_id}')
                    pp_facility.update()
            except Exception as e:
                logger.warning(f'Failed to create/update facility {jobscope_account_id} | {str(e)}')

    def get_matching_pp_contact(self, jobscope_contact, pp_contacts):
        # TODO - Once we have ERP codes for facilities, use the ShipTo_ID instead of the location name to check for
        #  matching records
        email = jobscope_contact.get("emailAddress")
        contact = None
        for c in pp_contacts:
            if c.email == email:
                contact = c
        return contact

    def populate_paperless_contact_from_jobscope_contact(self, jobscope_contact, pp_account, pp_contact):
        is_contact_new = False

        email = jobscope_contact["emailAddress"]
        first_name = jobscope_contact["firstName"]
        last_name = jobscope_contact["lastName"] if jobscope_contact["lastName"] else "N/A"
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
        phone = clean_up_phone_number(jobscope_contact["phoneNumber"])
        pp_contact.phone = phone
        return pp_contact, is_contact_new

    def get_matching_pp_facility(self, ship_to: dict, pp_facilities: list):
        # TODO - Once we have ERP codes for facilities, use the ShipTo_ID instead of the location name to check for
        #  matching records
        shipping_name = ship_to["siteName"]
        facility = None
        for f in pp_facilities:
            if f.name == shipping_name:
                facility = f
        return facility

    def populate_pp_facility_from_jobscope_shipping_address(self, ship_to, pp_facility):
        is_facility_new = False
        if pp_facility is None:
            is_facility_new = True

        shipping_address1 = set_blank_to_default_value(ship_to.get("addressLine1"), None)
        shipping_address2 = set_blank_to_default_value(ship_to.get("addressLine2"), None)
        shipping_name = set_blank_to_default_value(ship_to.get("siteName"), None)
        shipping_city = set_blank_to_default_value(ship_to.get("city"), None)
        shipping_country = set_blank_to_default_value(ship_to.get("country"), "USA")

        # TODO - the Paperless Parts Facility model currently does not allow Null for the attention field. Until that
        #  is resolved, write an empty string if the ship contact is Null in E2. If/when the empty string is written
        #  back to E2, the empty string will be rendered the same as a Null, so this is not as bad as using a
        #  placeholder string like 'N/A'
        shipping_contact = ''

        shipping_postal_code = set_blank_to_default_value(ship_to.get("postalCode"), None)
        shipping_state = set_blank_to_default_value(ship_to.get("state"), None)

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

    def populate_pp_sold_to_address_from_e2_account(self, jobscope_account: dict):

        # Assign the billing information for this account
        billing_address1 = set_blank_to_default_value(jobscope_account["addressLine1"], None)
        billing_address2 = set_blank_to_default_value(jobscope_account["addressLine2"], None)
        billing_city = set_blank_to_default_value(jobscope_account["city"], None)
        billing_country = set_blank_to_default_value(normalize_country(jobscope_account["country"]), "USA")
        billing_postal_code = set_blank_to_default_value(jobscope_account["postalCode"], None)
        billing_state = set_blank_to_default_value(jobscope_account["state"], None)

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
