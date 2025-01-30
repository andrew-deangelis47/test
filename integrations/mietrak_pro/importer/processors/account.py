from typing import List, Optional

from baseintegration.importer.import_processor import BaseImportProcessor
from mietrak_pro.models import Party, Partybuyer, Address as MietrakProAddress, Term
from baseintegration.datamigration import logger
from paperless.objects.customers import Account, Address, BillingAddress, Facility, Contact
from baseintegration.utils import safe_get, set_blank_to_default_value, is_blank, create_or_update_account


class AccountImportProcessor(BaseImportProcessor):

    def _process(self, mietrak_pro_account_id: int):  # noqa: C901
        client = self._importer._integration._client
        logger.info(client)
        logger.info(f"Processing {mietrak_pro_account_id}")
        mietrak_pro_account = Party.objects.filter(partypk=mietrak_pro_account_id, customer=1).first()
        if not mietrak_pro_account:
            logger.info(f"Account with ID {mietrak_pro_account_id} not processed")
            return

        pp_account, account_is_new = create_or_update_account(integration=self._importer._integration,
                                                              erp_code=mietrak_pro_account.partypk,
                                                              account_name=mietrak_pro_account.name)
        logger.info(f'Found customer with account_id {mietrak_pro_account_id} in the Party table in MIE Trak Pro')

        if self._importer.erp_config.should_use_customer_terms:
            mietrak_pro_terms = mietrak_pro_account.customertermsfk
        else:
            mietrak_pro_terms = mietrak_pro_account.termfk

        pp_account = self.set_pp_account_fields(mietrak_pro_account, mietrak_pro_terms, pp_account)

        primary_mietrak_pro_billing_address = self.get_primary_mietrak_pro_billing_address(mietrak_pro_account)
        should_import_sold_to_address = self.should_import_sold_to_address(primary_mietrak_pro_billing_address)
        if should_import_sold_to_address:
            pp_sold_to_address = self.populate_pp_address_from_mietrak_pro_address(
                primary_mietrak_pro_billing_address)
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

        # Pull down the related billing addresses, facilities, and contacts for later use
        pp_billing_addresses = pp_account.billing_addresses
        pp_facilities = Facility.list(account_id=pp_account.id)
        pp_contacts_list = Contact.filter(account_id=pp_account.id)
        pp_contacts = [Contact.get(id=c.id) for c in pp_contacts_list]

        # Optionally, import the MIE Trak Pro billing addresses as billing addresses in Paperless Parts
        mietrak_pro_billing_addresses = self.get_mietrak_pro_billing_addresses(mietrak_pro_account)
        for mietrak_pro_billing_address in mietrak_pro_billing_addresses:
            if mietrak_pro_billing_address is not None:

                should_import_billing_address = self.should_import_billing_address(mietrak_pro_billing_address)
                if should_import_billing_address:
                    pp_billing_address = self.get_matching_pp_billing_address(mietrak_pro_billing_address,
                                                                              pp_billing_addresses)
                    pp_billing_address, is_billing_address_new = \
                        self.populate_pp_billing_address_from_mietrak_pro_billing_address(mietrak_pro_billing_address,
                                                                                          pp_billing_address)

                    try:
                        if is_billing_address_new:
                            logger.info(
                                f'Creating new billing address for account {mietrak_pro_account_id}')
                            pp_billing_address.create(pp_account.id)
                        else:
                            logger.info(f'Updating billing address for account {mietrak_pro_account_id}')
                            pp_billing_address.update()
                    except Exception as e:
                        logger.info(f'Failed to create/update billing address for account | {str(e)}')

        # Optionally, import the MIE Trak Pro shipping address(es) as facilities in Paperless Parts
        mietrak_pro_shipping_addresses = self.get_mietrak_pro_shipping_addresses(mietrak_pro_account)
        for mietrak_pro_shipping_address in mietrak_pro_shipping_addresses:
            if mietrak_pro_shipping_address is not None:

                should_import_shipping_address = self.should_import_shipping_address(mietrak_pro_shipping_address)
                if should_import_shipping_address:
                    pp_facility = self.get_matching_pp_facility(mietrak_pro_shipping_address, pp_facilities)
                    pp_facility, is_facility_new = \
                        self.populate_pp_facility_from_mietrak_pro_shipping_address(mietrak_pro_shipping_address, pp_facility)

                    # TODO - the Open API currently throws a cryptic error message if the "attention" field is Null.
                    #  However, it cannot be ommitted from the request either. This means that if the "Contact" field
                    #  in MIE Trak Pro is left blank the shipping address import will fail. The correct solution here
                    #  is to fix the validation in the Open API endpoint
                    try:
                        if is_facility_new:
                            logger.info(f'Creating new facility {pp_facility.name} for account {mietrak_pro_account_id}')
                            pp_facility.create(pp_account.id)
                        else:
                            logger.info(f'Updating facility {pp_facility.name} for account {mietrak_pro_account_id}')
                            pp_facility.update()
                    except Exception as e:
                        logger.info(f'Failed to create/update facility {pp_facility.name} | {str(e)}')

        # Create Paperless Parts records for the associated contacts
        should_import_contacts = self.should_import_contacts()
        if should_import_contacts:
            mietrak_pro_party_buyer_linkages = Partybuyer.objects.filter(partyfk=mietrak_pro_account)
            for i, mietrak_pro_party_buyer in enumerate(mietrak_pro_party_buyer_linkages):
                mietrak_pro_contact = mietrak_pro_party_buyer.buyerfk

                pp_contact = self.get_matching_pp_contact(mietrak_pro_contact, pp_contacts)
                pp_contact, is_contact_new = self.populate_pp_contact_from_mietrak_pro_contact(mietrak_pro_contact,
                                                                                               mietrak_pro_party_buyer,
                                                                                               pp_account, pp_contact)
                try:
                    if pp_contact is not None:
                        if is_contact_new:
                            logger.info(f'Creating new contact {pp_contact.email} for account {mietrak_pro_account_id}')
                            pp_contact.create()
                        else:
                            logger.info(f'Updating contact {pp_contact.email} for account {mietrak_pro_account_id}')
                            pp_contact.update()
                except Exception as e:
                    logger.warning(e)
                    logger.warning(f'Encountered an error importing contact: {pp_contact.email} - skipping.')

    def get_mietrak_pro_billing_addresses(self, mietrak_pro_account: Party):
        mietrak_pro_billing_addresses = \
            MietrakProAddress.objects.filter(
                partyfk=mietrak_pro_account,
                addresstypefk__description__in=['Billing', 'Billing & Shipping']
            ).exclude(
                archived=1
            )
        return mietrak_pro_billing_addresses

    def get_primary_mietrak_pro_billing_address(self, mietrak_pro_account: Party):
        mietrak_pro_billing_addresses = self.get_mietrak_pro_billing_addresses(mietrak_pro_account)
        return mietrak_pro_billing_addresses[0] if mietrak_pro_billing_addresses else None

    def get_mietrak_pro_shipping_addresses(self, mietrak_pro_account: Party):
        mietrak_pro_shipping_addresses = \
            MietrakProAddress.objects.filter(
                partyfk=mietrak_pro_account,
                addresstypefk__description__in=['Shipping', 'Billing & Shipping']
            ).exclude(
                archived=1
            )
        return mietrak_pro_shipping_addresses

    def should_import_contacts(self):
        should_import_contacts = self._importer.erp_config.should_import_contacts
        return should_import_contacts

    def should_import_shipping_address(self, mietrak_pro_shipping_address: MietrakProAddress):
        if not self._importer.erp_config.should_import_shipping_addresses or mietrak_pro_shipping_address is None:
            return False

        is_shipping_address_blank = self.determine_if_address_is_blank(mietrak_pro_shipping_address)
        is_shipping_address_incomplete = self.determine_if_address_is_incomplete(mietrak_pro_shipping_address)
        should_import_shipping_address = True
        if self._importer.erp_config.should_skip_incomplete_addresses and is_shipping_address_incomplete:
            should_import_shipping_address = False
        if is_shipping_address_blank:
            should_import_shipping_address = False
        return should_import_shipping_address

    def should_import_billing_address(self, mietrak_pro_billing_address: MietrakProAddress):
        if not self._importer.erp_config.should_import_billing_address or mietrak_pro_billing_address is None:
            return False

        is_billing_address_blank = self.determine_if_address_is_blank(mietrak_pro_billing_address)
        is_billing_address_incomplete = self.determine_if_address_is_incomplete(mietrak_pro_billing_address)
        should_import_billing_address = True
        if self._importer.erp_config.should_skip_incomplete_addresses and is_billing_address_incomplete:
            should_import_billing_address = False
        if is_billing_address_blank:
            should_import_billing_address = False
        return should_import_billing_address

    def should_import_sold_to_address(self, primary_mietrak_pro_billing_address: MietrakProAddress):
        if not self._importer.erp_config.should_import_sold_to_address or primary_mietrak_pro_billing_address is None:
            return False

        is_billing_address_blank = self.determine_if_address_is_blank(primary_mietrak_pro_billing_address)
        is_billing_address_incomplete = \
            self.determine_if_address_is_incomplete(primary_mietrak_pro_billing_address)
        should_import_sold_to_address = True
        if self._importer.erp_config.should_skip_incomplete_addresses and is_billing_address_incomplete:
            should_import_sold_to_address = False
        if is_billing_address_blank:
            should_import_sold_to_address = False
        return should_import_sold_to_address

    def get_matching_pp_contact(self, mietrak_pro_contact: Party, pp_contacts: List[Contact]):
        email = mietrak_pro_contact.email
        contact = None
        for c in pp_contacts:
            if c.email == email:
                contact = c
        return contact

    @classmethod
    def get_contact_first_and_last_name(cls, mietrak_pro_contact: Party):
        try:
            split_contact_name = mietrak_pro_contact.name.split(' ', 1)
            first_name = split_contact_name[0]
            last_name = split_contact_name[1]
            return first_name, last_name
        except:
            return None, None

    def populate_pp_contact_from_mietrak_pro_contact(self, mietrak_pro_contact: Party,
                                                     mietrak_pro_party_buyer: Partybuyer,
                                                     pp_account: Account,
                                                     pp_contact: Optional[Contact]):
        is_contact_new = False

        company_erp_code = mietrak_pro_contact.partypk
        email = mietrak_pro_contact.email

        first_name, last_name = self.get_contact_first_and_last_name(mietrak_pro_contact)
        if not first_name or not last_name:
            first_name = mietrak_pro_contact.name if mietrak_pro_contact is not None else 'Contact'
            last_name = f'Party_ID_{company_erp_code}'
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

        phone, phone_ext = self.clean_up_phone_number(mietrak_pro_contact.phone)

        pp_contact.notes = mietrak_pro_party_buyer.description
        pp_contact.phone = phone
        pp_contact.phone_ext = phone_ext
        return pp_contact, is_contact_new

    def get_matching_pp_facility(self, mietrak_pro_shipping_address: MietrakProAddress, pp_facilities: List[Facility]):
        shipping_address_id = str(mietrak_pro_shipping_address.addresspk)
        facility = None
        for f in pp_facilities:
            if f.address.erp_code == shipping_address_id:
                facility = f
        return facility

    def get_matching_pp_billing_address(self, mietrak_pro_billing_address: MietrakProAddress,
                                        pp_billing_addresses: List[BillingAddress]):
        billing_address_id = str(mietrak_pro_billing_address.addresspk)
        matching_billing_address = None
        for b in pp_billing_addresses:
            if b.erp_code == billing_address_id:
                matching_billing_address = b
        return matching_billing_address

    def populate_pp_facility_from_mietrak_pro_shipping_address(self, mietrak_pro_shipping_address: MietrakProAddress,
                                                               pp_facility: Optional[Facility]):
        is_facility_new = False
        if pp_facility is None:
            is_facility_new = True

        shipping_address = self.populate_pp_address_from_mietrak_pro_address(mietrak_pro_shipping_address)

        shipping_name = set_blank_to_default_value(mietrak_pro_shipping_address.name, '')
        shipping_contact = set_blank_to_default_value(mietrak_pro_shipping_address.contact, '')

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

    def populate_pp_address_from_mietrak_pro_address(self, mietrak_pro_address: MietrakProAddress):

        billing_address1 = set_blank_to_default_value(mietrak_pro_address.address1, None)
        billing_address2 = set_blank_to_default_value(mietrak_pro_address.address2, None)
        billing_city = set_blank_to_default_value(mietrak_pro_address.city, None)
        billing_country = mietrak_pro_address.countryfk.alpha3code if \
            mietrak_pro_address.countryfk is not None else None
        billing_country = set_blank_to_default_value(billing_country, "USA")
        billing_postal_code = set_blank_to_default_value(mietrak_pro_address.zipcode, None)
        billing_state = mietrak_pro_address.statefk.code if \
            mietrak_pro_address.statefk is not None else None
        billing_state = set_blank_to_default_value(billing_state, "MA")
        erp_code = mietrak_pro_address.addresspk

        # Set the sold to address to be the billing address from MIE Trak Pro
        pp_address = Address(
            address1=billing_address1,
            address2=billing_address2,
            city=billing_city,
            country=billing_country,
            postal_code=billing_postal_code,
            state=billing_state,
            erp_code=erp_code,  # TODO - add this to the SDK
        )
        return pp_address

    def populate_pp_billing_address_from_mietrak_pro_billing_address(
            self, mietrak_pro_billing_address: MietrakProAddress, pp_billing_address: BillingAddress):
        is_billing_address_new = False
        if pp_billing_address is None:
            is_billing_address_new = True

        pp_address = self.populate_pp_address_from_mietrak_pro_address(mietrak_pro_billing_address)

        # Set the billing address to be the billing address from MIE Trak Pro
        if is_billing_address_new:
            pp_billing_address = BillingAddress(
                address1=pp_address.address1,
                address2=pp_address.address2,
                city=pp_address.city,
                country=pp_address.country,
                postal_code=pp_address.postal_code,
                state=pp_address.state,
                erp_code=pp_address.erp_code,
            )
        else:
            pp_billing_address.address1 = pp_address.address1
            pp_billing_address.address2 = pp_address.address2
            pp_billing_address.city = pp_address.city
            pp_billing_address.country = pp_address.country
            pp_billing_address.postal_code = pp_address.postal_code
            pp_billing_address.state = pp_address.state

        return pp_billing_address, is_billing_address_new

    def determine_if_address_is_incomplete(self, mietrak_pro_address: MietrakProAddress):
        required_address_fields = (
            mietrak_pro_address.address1,
            mietrak_pro_address.city,
            mietrak_pro_address.countryfk.description if mietrak_pro_address.countryfk is not None else None,
            mietrak_pro_address.zipcode,
            mietrak_pro_address.statefk.description if mietrak_pro_address.statefk is not None else None
        )
        is_address_incomplete = any([is_blank(field) for field in required_address_fields])
        return is_address_incomplete

    def determine_if_address_is_blank(self, mietrak_pro_address: MietrakProAddress):
        address_fields = (
            mietrak_pro_address.address1,
            mietrak_pro_address.city,
            mietrak_pro_address.countryfk.description if mietrak_pro_address.countryfk is not None else None,
            mietrak_pro_address.zipcode,
            mietrak_pro_address.statefk.description if mietrak_pro_address.statefk is not None else None
        )
        is_address_blank = all([is_blank(field) for field in address_fields])
        return is_address_blank

    def set_pp_account_fields(self, mietrak_pro_account: Party, mietrak_pro_terms: Term, pp_account: Account):
        # Create a Paperless Parts record for this account
        name = mietrak_pro_account.name
        erp_code = mietrak_pro_account.partypk
        notes = mietrak_pro_account.notes
        payment_terms = mietrak_pro_terms.description if mietrak_pro_terms is not None else None
        payment_terms_period = mietrak_pro_terms.duedays if mietrak_pro_terms is not None else None
        phone, phone_ext = self.clean_up_phone_number(mietrak_pro_account.phone)
        purchase_orders_enabled = True
        tax_exempt = False
        url = mietrak_pro_account.website
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

    def clean_up_phone_number(self, phone_number: Optional[str]):
        """ Format the phone number as 10 digits without spaces or non-numeric characters.
            Try to parse out the extension as well, if applicable. """
        if phone_number is None:
            return None, None
        import re
        phone_number_components = phone_number.split('x')  # Try to split the extension from the phone number
        phone_number = phone_number_components[0]
        extension = None
        if len(phone_number_components) > 1:
            extension = phone_number_components[1]
        try:
            phone_number = re.sub('\D', '', phone_number)[:10]  # noqa: W605
            if extension is not None:
                extension = re.sub('\D', '', extension)[:10]  # noqa: W605
        except:
            pass
        return phone_number, extension
