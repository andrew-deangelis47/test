from baseintegration.datamigration import logger
from paperless.objects.quotes import Quote
from baseintegration.exporter.quote_exporter import QuoteExporter
from baseintegration.exporter.order_exporter import OrderExporter
import requests
import json
from datetime import datetime
from random import randint
from lillyworks.exporter.configuration import LillyWorksConfig
from paperless.objects.orders import Order

# Every time this module starts up we assign a new random initial value for the id_counter
id_counter = randint(0, 65535)


class LillyWorksOrderExporter(OrderExporter):

    def _process_order(self, order: Order):
        logger.info(str(order.number))
        return order.number


class LillyWorksQuoteExporter(QuoteExporter):
    """An integration specific to LillyWorks"""

    def _setup_erp_config(self):
        global LILLYWORKS_CONFIG
        if not self._integration.test_mode:
            logger.info('Reading config specific configuration file')
            parser = self._integration.config_yaml["Exporters"]["quotes"]
            secrets = self._integration.config
            LILLYWORKS_CONFIG = LillyWorksConfig(
                email_address=parser.get("email_address"),
                password=secrets.get("password"),
                which=secrets.get("which"),
                company_name=parser.get("company_name"),
                default_quote_name=parser.get("default_quote_name", ""),
                lookup_customers_by_id=parser.get("lookup_customers_by_id", True)
            )
        else:
            LILLYWORKS_CONFIG = LillyWorksConfig(
                email_address="boaty@mcboatface.com",
                password="facethemcboat",
                which="boaty-boat-house",
                company_name="British Antarctic Survey",
                default_quote_name="",
                lookup_customers_by_id=True
            )

    def _register_default_processors(self):
        pass

    def _process_quote(self, quote: Quote):
        """Brings over quotes based on a certain quote number"""
        logger.info(f'Processing quote {quote.number}')
        logger.info('Testing quote connection')
        login_response = self.login()
        headers = self.get_headers(login_response)
        application_url = self.get_application_url(login_response)
        post_upsert_url = f"{application_url}api/data/postupsert"
        quote_id = self.generate_id()
        logger.info(f"Generating quote with id {quote_id}")

        # We need to first add to the quote table then quote item table
        quote_description = "PP-" + str(quote.number)
        quote_name = self.get_quote_name(quote)
        quote_upload_data = [
            {
                "$type": "LillyWorks.Models.Quote",
                "Name": quote_name,
                "Description": quote_description,
                "QuoteID": f"{quote_id}"
            }
        ]

        # Get customer. If one does not exist, add one
        customer: list = self.get_customer(application_url, headers, quote.contact.account.erp_code,
                                           quote.contact.account.name)
        if len(customer) == 1:
            logger.info("Found one customer match. Using it for quote")
            logger.info(f"Customer is {customer[0].get('Name', 'Not found')}")
            customer_id = customer[0].get("CustomerID")
            quote_upload_data[0]["CustomerID"] = customer_id
            # Bring over terms definition from terms definition on the customer
            terms_definition_id = customer[0].get("TermsDefinitionID")
            # If terms definition does not exist for that customer, use "NET30"
            if not terms_definition_id:
                terms_definition_id = self.get_net_30_terms_definition_id(application_url, headers)
            else:
                logger.info("Terms definition found on customer. Using it")
        else:
            logger.info("Did not find a customer. Adding it to DB")
            new_cust = self.add_customer(quote.contact)
            # add customer
            r = requests.post(post_upsert_url, headers=headers, json=new_cust)
            logger.info(r.text)
            logger.info("Adding new customer ID to quote")
            quote_upload_data[0]["CustomerID"] = new_cust[0]["CustomerID"]
            terms_definition_id = self.get_net_30_terms_definition_id(application_url, headers)

        # get terms definition
        quote_upload_data[0]["TermsDefinitionID"] = terms_definition_id

        # add quote
        logger.info("Adding quote to DB")
        r = requests.post(post_upsert_url, headers=headers, json=quote_upload_data)
        logger.info(r.text)
        if r.status_code != 200:
            raise ValueError(f"Quote {quote.number} failed")

        # add quote items
        quote_item_upload_data = []
        self.add_quote_items(quote_item_upload_data, quote_id, quote.quote_items, quote.number)
        r = requests.post(post_upsert_url, headers=headers, json=quote_item_upload_data)
        logger.info(r.text)
        if r.status_code != 200:
            raise ValueError(f"Quote {quote.number} failed")
        else:
            logger.info("Completed!")

    def get_quote_name(self, quote: Quote) -> str:
        if quote.request_for_quote:
            quote_name = quote.request_for_quote
            logger.info("Found request for quote, using it for the quote")
        else:
            # PDQ would like quote name to be empty if RFQ doesn't exist
            quote_name = ""
            logger.info("Did not find request for quote, setting quote name to empty")
        return quote_name

    def get_net_30_terms_definition_id(self, application_url: str, headers: dict):
        logger.info("Getting the terms definition for net 30")
        terms_definition_url = f"{application_url}api/data/TermsDefinitions"
        query_data = {
            "$filter": "(substringof('NET30',Name) eq true)"
        }
        terms_definition = json.loads(requests.get(url=terms_definition_url, params=query_data, headers=headers).text)
        if isinstance(terms_definition, list) and len(terms_definition) > 0:
            return terms_definition[0].get("TermsDefinitionID")
        else:
            raise ValueError("Please add a NET30 terms definition into LillyWorks")

    def add_quote_items(self, upload_data: dict, quote_id: int, quote_items: list, number: int):
        i = 1
        for item in quote_items:
            logger.info(f"At LineNo {str(i)}")
            logger.info(f"Adding quote item for {item.root_component.part_number}")
            if not item.root_component.part_number:
                self.send_email("Failed to bring over quote items",
                                f"Did not bring over quote items for Paperless Parts quote {str(number)} due to lack of part number on a part. Please enter manually")
                raise ValueError(
                    f"Did not bring over quote items for quote {str(number)} due to lack of part number on a part")
            new_item = {
                "$type": "LillyWorks.Models.QuoteLine",
                "QuoteLineID": f"{self.generate_id()}",
                "Description": item.public_notes,
                "QuoteID": str(quote_id),
                "LineNo": i,
                "Name": item.root_component.part_number
            }
            logger.info("Adding pricing information")
            j = 0
            # LillyWorks requires JSON called "Pricing" and another called "Unit Pricing" in order to show prices for quote successfully in UI
            pricing = {"PricingType": "Quantity",
                       "$type": "LillyWorks.Models.Pricing"}
            # Quantities are stored in fields UnitPrice0, Qty0, UnitPrice1, Qty1, etc.
            for quantity in item.root_component.quantities:
                unit_pricing_key = f"UnitPrice{str(j)}"
                quantity_key = f"ItemQty{str(j)}"
                pricing[quantity_key] = quantity.quantity
                pricing[unit_pricing_key] = float(quantity.unit_price.raw_amount)
                j = j + 1
            new_item["Pricing"] = pricing
            new_item["UserPricing"] = pricing
            upload_data.append(new_item)
            i = i + 1

    def login(self):
        login_direct_url = "https://app.lillyworks.net/account/logindirect"
        data = {
            'emailAddress': LILLYWORKS_CONFIG.email_address,
            'password': LILLYWORKS_CONFIG.password,
            'which': LILLYWORKS_CONFIG.which,
            'companyName': LILLYWORKS_CONFIG.company_name,
        }
        return requests.post(login_direct_url, data=data, verify=False)  # TODO - remove the verify=False!

    def add_customer(self, contact):
        cust_id = str(self.generate_id())
        cust_name = contact.account.name
        new_cust = [{
            "$type": "LillyWorks.Models.Customer",
            "Name": cust_name,
            "CustomerID": f"{cust_id}",
            "Active": "True"
        }]
        self.send_email("New customer created in LillyWorks",
                        f"A new customer with name {cust_name} and LillyWorks ID {str(cust_id)} has been brought from Paperless Parts into LillyWorks. Please review manually")  # noqa: E501
        return new_cust

    def get_customer(self, application_url: str, headers: dict, erp_code, company_name):
        customer_url = f"{application_url}api/data/customers"
        if erp_code and LILLYWORKS_CONFIG.lookup_customers_by_id:
            res = self.query_customers_by_id(customer_url, erp_code, headers)
            query_result_by_id: list = json.loads(res.text)
            if len(query_result_by_id) == 1:
                return query_result_by_id
        res = self.query_customers_by_name(customer_url, company_name, headers)
        query_result_by_customer: list = json.loads(res.text)
        if len(query_result_by_customer) == 1:
            return query_result_by_customer
        elif len(query_result_by_customer) == 0:
            return []
        else:
            raise ValueError(
                "More than one customer found matching with the customer name. Please add a customer ID as an ERP code instead")

    def query_customers_by_id(self, customer_url: str, erp_code: str, headers: dict):
        query_data = {
            "$filter": f"(substringof('{erp_code}',AccountNumber) eq true)"
        }
        return requests.get(url=customer_url, params=query_data, headers=headers)

    def query_customers_by_name(self, customer_url: str, company_name: str, headers: dict):
        query_data = {
            "$filter": f"(substringof('{company_name}',Name) eq true)"
        }
        return requests.get(url=customer_url, params=query_data, headers=headers)

    def get_headers(self, login_response):
        logger.info(login_response)
        try:
            bearer_token = login_response.headers['x-bearer-token']
            headers = {'x-bearer-token': bearer_token}
            logger.info(headers)
            return headers
        except:
            raise ValueError("Token not found in login response headers")

    def get_application_url(self, login_response):
        try:
            application_url = login_response.headers['x-application-url']
            logger.info(application_url)
            return application_url
        except:
            raise ValueError("Application URL not found in login response")

    def generate_id(self):
        """
        Generate an ID for a LillyWorks entity. This is the way LillyWorks generates IDs internally, according to the API
        documentation.

        We start with a number based on the current date in a very small unit of measure. We borrow a concept from C# called
        "ticks", where 1 tick = 100 nanoseconds. Then, we shift this value up by 16 bits. Next, we add a short integer value
        called id_counter. This id_counter value is seeded randomly, and then incremented by one each time a new ID is
        generated. Finally, we mask the value to keep only the 52 least significant bits (to keep the number smaller than
        2^53, which prevents overflow in Javascript where everything is a floating point number).

        Note: This scheme doesn't guarantee a unique ID. However, given the number of IDs that will be generated and the
        fact that they will be spread across multiple tables, for all practical purposes we can treat these IDs as
        unique. The id_counter is a module-level variable, which means that it gets re-seeded every time a new process
        runs this code. In practice, there should only be a single long-running connector process for this integration,
        so the id_counter will only get re-seeded when the process is restarted. Because we are not relying on this counter
        for uniqueness it is not important to persist its value across sessions.
        """

        def ticks(dt):
            return (dt - datetime(1, 1, 1)).total_seconds() * 10000000

        now = datetime.now()
        global id_counter
        id_counter += 1
        return ((int(ticks(now)) << 16) + id_counter) & 0xFFFFFFFFFFFFF
