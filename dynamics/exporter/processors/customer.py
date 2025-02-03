from baseintegration.datamigration import logger
from dynamics.exporter.utils import get_failed_quote_instructions
from paperless.exceptions import PaperlessNotFoundException
from paperless.objects.quotes import Contact as QuoteContact
from paperless.objects.customers import Account

from dynamics.exceptions import DynamicsNotFoundException, RecognizedException
from dynamics.utils import DynamicsExportProcessor
from dynamics.objects.customer import Customer, Contact, PaymentTerm, CountryCode


class CustomerProcessor(DynamicsExportProcessor):

    def _process(self, quote_contact: QuoteContact) -> (Customer, Contact):

        should_create_customer = self.get_config_value('should_create_customer')

        if not (quote_contact.account and quote_contact.account.id):
            email_text = f'The quote contact {quote_contact.first_name} {quote_contact.last_name} ' \
                         f'({quote_contact.email}) is not tied to an account. Please ensure that all contacts are ' \
                         f'associated with an account, and {get_failed_quote_instructions()}'
            exception_text = f'No account found on Paperless contact {quote_contact.email}'
            raise RecognizedException(exception_text, email_text)

        paperless_account: Account

        try:
            paperless_account = Account.get(quote_contact.account.id)
        except PaperlessNotFoundException:
            email_text = f'The quote account {quote_contact.account.name} could not be found. Please ' \
                         f'{get_failed_quote_instructions()}'
            exception_text = f'Could not find Paperless account with ID {quote_contact.account.id}'
            raise RecognizedException(exception_text, email_text)

        dynamics_company: Customer

        try:
            # try finding customer by number
            dynamics_company = Customer.get_first({
                "No": paperless_account.erp_code
            })
        except DynamicsNotFoundException:
            try:
                # next try finding customer by name
                dynamics_company = Customer.get_first({
                    "Name": paperless_account.name
                })
            except DynamicsNotFoundException:
                if should_create_customer:
                    erp_code = paperless_account.erp_code
                    name = paperless_account.name
                    payment_terms = paperless_account.payment_terms
                    payment_terms_period = paperless_account.payment_terms_period
                    sold_to = paperless_account.sold_to_address
                    phone = paperless_account.phone

                    PaymentTerm.get_or_create({
                        "Code": payment_terms
                    }, {
                        "Due_Date_Calculation": f'{payment_terms_period}D'
                    })

                    country_str = ""
                    if sold_to and sold_to.country:
                        country_code = CountryCode.get_or_create({
                            "Name": sold_to.country
                        }, {
                            "Code": sold_to.country
                        })
                        country_str = country_code.Code

                    data = {
                        "Name": name,
                        "No": erp_code or None,
                        "E_Mail": quote_contact.email,
                        "Phone_No": phone or "",
                        "Address": sold_to.address1 if sold_to else "",
                        "Address_2": sold_to.address2 if sold_to else "",
                        "City": sold_to.city if sold_to else "",
                        "County": sold_to.state if sold_to else "",
                        "Post_Code": sold_to.postal_code if sold_to else "",
                        "Country_Region_Code": country_str,
                        "Payment_Terms_Code": payment_terms,
                        "Gen_Bus_Posting_Group": self.get_config_value('gen_bus_posting_group'),
                        "Customer_Posting_Group": self.get_config_value('customer_posting_group'),
                        "Tax_Area_Code": self.get_config_value('tax_area_code')
                    }

                    dynamics_company = Customer.create(data)
                    if not erp_code and paperless_account:
                        paperless_account.erp_code = dynamics_company.No
                        paperless_account.update()
                else:
                    email_text = f'The quote account {paperless_account.name} (number: {paperless_account.erp_code}) ' \
                                 f'could not be found as a customer in Dynamics. Please create a matching account in ' \
                                 f'Dynamics, and {get_failed_quote_instructions()}'
                    exception_text = f'Dynamics customer {paperless_account.name} ({paperless_account.erp_code}) ' \
                                     f'not found'
                    raise RecognizedException(exception_text, email_text)

        dynamics_contact = self._process_contact(quote_contact, dynamics_company)

        return dynamics_company, dynamics_contact

    def _process_contact(self, quote_contact: QuoteContact, dynamics_company: Customer):
        should_create_contact = self.get_config_value('should_create_contact')

        dynamics_contact: Contact

        try:
            dynamics_contact = Contact.get_first({
                "Company_Name": dynamics_company.Name,
                "E_Mail": quote_contact.email
            })
        except DynamicsNotFoundException:
            if should_create_contact:
                # First we need to ensure the company itself is registered as a contact
                company_contact = Contact.get_or_create({
                    "Company_Name": dynamics_company.Name,
                    "Type": "Company"
                })

                # Create the contact person if necessary
                dynamics_contact = Contact.create({
                    "Company_No": company_contact.No,
                    "E_Mail": quote_contact.email,
                    "First_Name": quote_contact.first_name,
                    "Surname": quote_contact.last_name,
                    "Type": "Person"
                })
            else:
                logger.warning(f'Dynamics contact {quote_contact.email} not found')
                return None

        return dynamics_contact
