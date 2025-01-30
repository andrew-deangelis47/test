from typing import Optional

from baseintegration.importer.import_processor import BaseImportProcessor
from inforvisual.models import Customer, CustContact, Contact
from baseintegration.datamigration import logger
from paperless.objects.customers import Address, Account
from baseintegration.utils import normalize_country, create_or_update_account, \
    get_or_create_contact, clean_up_phone_number


class AccountImportProcessor(BaseImportProcessor):

    def _process(self, account_id: str):  # noqa: C901
        client = self._importer._integration._client
        logger.info(client)
        logger.info(f"Processing {account_id}")
        account: Customer = Customer.objects.filter(id=account_id).first()
        if not account:
            logger.info("Account not processed")
            return
        logger.info(f'Found customer with account_id {account.id} in the Customer table in Inforvisual')
        pp_account = self._create_or_update_account(account)
        if pp_account:
            self._create_or_update_contacts(account, pp_account)
        else:
            logger.info("Not processing contacts")
        logger.info(f"Account {account_id} was updated or created!")

    def _create_or_update_account(self, infor_customer: Customer) -> Optional[Account]:
        pp_account, account_is_new = create_or_update_account(integration=self._importer._integration,
                                                              erp_code=infor_customer.id,
                                                              account_name=infor_customer.name)
        # Create a Paperless Parts record for this account
        name = infor_customer.name
        erp_code = infor_customer.id

        pp_account.name = name
        pp_account.erp_code = erp_code
        pp_account.phone = clean_up_phone_number(infor_customer.contact_phone)
        pp_account.phone_ext = infor_customer.contact_phone_ext
        pp_account.url = infor_customer.web_url
        if infor_customer.terms_description and infor_customer.terms_net_days is not None:
            pp_account.payment_terms = infor_customer.terms_description
            pp_account.payment_terms_period = infor_customer.terms_net_days

        infor_customer_country = normalize_country(infor_customer.country)
        if infor_customer.addr_1 and infor_customer.city and infor_customer.state and infor_customer_country \
                and infor_customer.zipcode:
            sold_to_address = Address(
                address1=infor_customer.addr_1,
                address2=infor_customer.addr_2,
                city=infor_customer.city,
                country=infor_customer_country,
                postal_code=infor_customer.zipcode,
                state=infor_customer.state
            )

            pp_account.sold_to_address = sold_to_address

        try:
            if account_is_new:
                pp_account.create()
            else:
                pp_account.update()
        except Exception as e:
            logger.warning(e)
            logger.warning(f'Encountered an error importing account: {name} - skipping.')
            if account_is_new:
                return None
        return pp_account

    def _create_or_update_contacts(self, infor_customer: Customer, paperless_account: Account):
        for cust_contact in CustContact.objects.filter(customer=infor_customer):
            infor_contact: Contact = cust_contact.contact

            if not (infor_contact.email and infor_contact.first_name and infor_contact.last_name):
                logger.info(f"Contact {infor_contact.id} not imported: email, first name, "
                            f"and last name are all required.")
                continue
            logger.info(f'Processing contact {infor_contact.email}')

            pp_contact, contact_is_new = get_or_create_contact(infor_contact.email, paperless_account)

            pp_contact.email = infor_contact.email
            pp_contact.first_name = infor_contact.first_name
            pp_contact.last_name = infor_contact.last_name
            pp_contact.phone = clean_up_phone_number(infor_contact.phone)
            pp_contact.phone_ext = infor_contact.phone_ext

            infor_contact_country = normalize_country(infor_contact.country)
            if infor_contact.addr_1 and infor_contact.city and infor_contact.state and infor_contact_country \
                    and infor_contact.zipcode:
                pp_contact.address = Address(
                    address1=infor_contact.addr_1,
                    address2=infor_contact.addr_2,
                    city=infor_contact.city,
                    state=infor_contact.state,
                    country=infor_contact_country,
                    postal_code=infor_contact.zipcode
                )

            try:
                if contact_is_new:
                    pp_contact.create()
                else:
                    pp_contact.update()
            except Exception as e:
                logger.warning(e)
                logger.warning(f'Encountered an error importing contact: {infor_contact.email} - skipping.')
