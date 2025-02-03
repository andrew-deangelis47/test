import requests
from baseintegration.datamigration import logger
import json
from configparser import RawConfigParser
import os
from typing import Union
from datetime import datetime


class JobscopeClient:

    def __init__(self, api_url):
        self.api_url = api_url
        self.token = None
        self.headers = None

    def get_secrets_access_token(self, parser_dict: dict):
        if parser_dict.get("Paperless") and parser_dict["Paperless"].get("jobscope_access_token"):
            return parser_dict["Paperless"]["jobscope_access_token"]
        else:
            return None

    def login(self, username: str, password: str):
        parser = RawConfigParser()
        parser.read(os.path.join(os.path.dirname(__file__), "../../secrets.ini"))
        parser_dict = parser._sections
        logger.info("Logging in")
        if self.get_secrets_access_token(parser_dict):
            self.token = self.get_secrets_access_token(parser_dict)
            self.headers = {
                "Authorization": f"Bearer {self.token}"
            }
            try:
                self.get_customers()
                return
            except ValueError:
                logger.info("Old access key failed, trying to login again")
        url = self.api_url + "/token/user"
        data = {
            "grant_type": "password",
            "username": username,
            "password": password
        }
        res = requests.post(
            url=url,
            data=data
        )
        if res.status_code == 200:
            logger.info("Logged into Jobscope successfully!")
            self.token = json.loads(res.text)["access_token"]
            self.headers = {
                "Authorization": f"Bearer {self.token}"
            }
            parser.set("Paperless", "jobscope_access_token", self.token)
            config = open(os.path.join(os.path.dirname(__file__), "../../secrets.ini"), "w")
            parser.write(config, space_around_delimiters=False)
            config.close()
        else:
            logger.info("Login failed!")
            raise ValueError(f"Login failed with error {res.text}")

    def get(self, url, text) -> Union[list, dict]:
        res = requests.get(
            url=url,
            headers=self.headers
        )
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            logger.info(f"Getting {text} failed! -- trying second time")
            res = requests.get(
                url=url,
                headers=self.headers
            )
            if res.status_code == 200:
                return json.loads(res.text)
            raise ValueError(f"Getting {text} failed with error {res.text}")

    def post(self, url, text, data=None) -> Union[list, dict]:
        res = requests.post(
            url=url,
            data=data,
            headers=self.headers
        )
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            logger.info(f"Creating {text} failed! -- trying second time")
            res = requests.post(
                url=url,
                data=data,
                headers=self.headers
            )
            if res.status_code == 200:
                return json.loads(res.text)
            raise ValueError(f"Creating {text} failed with error {res.text}")

    def put(self, url, text, data=None) -> Union[list, dict]:
        res = requests.put(
            url=url,
            data=data,
            headers=self.headers
        )
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            logger.info(f"Putting {text} failed!")
            raise ValueError(f"Putting {text} failed with error {res.text}")

    def get_customers(self) -> list:
        url = self.api_url + "/api/Customers?IncludeinActive=false"
        return self.get(url, "customers")

    def get_customer(self, customer_id: str) -> dict:
        url = self.api_url + f"/api/customers?CustomerNumber={customer_id}"
        try:
            return self.get(url, "customer")
        except ValueError as e:
            if "Customer doesn't" in str(e):
                return {}

    def create_part(self, part_number: str, material_cost_category_code: str, psm: str,
                    division_id: str, unit_of_issue: str, description: str = None, revision: str = None) -> dict:
        url = self.api_url + f"/api/Parts?PartNumber={part_number}"
        # right now we denote revision - because the jobscope client requires us to pass a revision. It's not an
        # issue because we are only searching by part number, not by part revision, when checking if a part is new if
        # a future jobscope customer wants us to create new parts when the part number already exists in the system
        # and only the revision differs, then this should be revised and we should look at potentially changing the
        # default rev
        if revision is None:
            revision = "-"
        return self.post(url, "parts", data={"MaterialCostCategoryCode": material_cost_category_code,
                                             "PSM": psm,
                                             "IsActive": True,
                                             "Description1": description[0:39] if description is not None else "",
                                             "DivisionId": division_id,
                                             "UnitOfIssue": unit_of_issue,
                                             "CurrentRevision": revision,
                                             "DrawingNumber": "N/A",
                                             "EngineeringUOM": "EA",
                                             "Gauge": "NA",
                                             "NationalStockNumber": "N/A",
                                             "LastVendor": "N/A",
                                             "ManufacturerName": "N/A",
                                             "ManufacturerPartNumber": "N/A",
                                             "RoutingCode": "N/A",
                                             "Tolerance": "N/A",
                                             "EmployeeNumber": "N/A",
                                             "UserText": "",
                                             "VendorCode1": "N/A",
                                             "VendorCode2": "N/A",
                                             "ExportControlClassificationNumber": "N/A",
                                             "ExportScheduleBNumber": "N/A"
                                             })

    def create_routing_header(self, item_number: str, revision: str, description: str, division_id: str):
        url = self.api_url + f"/api/RoutingHeaders?RoutingId={item_number}"
        if revision is None:
            revision = "-"
        if description is None:
            description = "N/A"
        self.post(url, "routing header", data={"Revision": revision,
                                               "Description": description[0:39] if description is not None else '',
                                               "DivisionId": division_id,
                                               "IsReleasedForProduction": True,
                                               "IsAssembly": True,
                                               "IsActive": True})

    def create_part_routing(self, item_number: str, revision: str):
        url = self.api_url + f"/api/PartRoutings?PartNumber={item_number}&Routing={item_number}"
        if revision is None:
            revision = "-"
        self.post(url, "part routing", data={"RoutingId": item_number,
                                             "RoutingRevision": revision,
                                             "IsAssembly": True,
                                             "IsCurrentForType": True,
                                             "IsActive": True
                                             })

    def create_bom_record(self, parent_item_number: str, child_item_number: str, bom_sequence: str, division_id: str,
                          component_revision: str, unit_of_issue: str, quantity_per: str, psm: str):
        bom_sequence = str(bom_sequence).zfill(3)
        url = self.api_url + f"/api/BillOfMaterialComponents?AssemblyNumber={parent_item_number}"
        if component_revision is None:
            component_revision = "-"
        self.post(url, "bom record", data={"ComponentPartNumber": child_item_number,
                                           "BOMSequence": bom_sequence,
                                           "DivisionId": division_id,
                                           "ComponentRevision": component_revision,
                                           "UnitOfIssue": unit_of_issue,
                                           "QuantityPer": quantity_per,
                                           "PSM": psm,
                                           "UserText": "",
                                           "Designation": "N/A",
                                           "ExternalBOMItem": "N/A"})

    def create_routing(self, item_number: str, revision: str, sequence_no: int, work_center_id: str, work_center_description: str,
                       setup_hrs: float, run_hrs: float):
        try:
            sequence_operation = str(sequence_no).zfill(4)
        except:
            pass
        url = self.api_url + f"/api/RoutingOperations?RoutingCode={item_number}&SequenceNumber={sequence_no}"
        if revision is None:
            revision = "-"
        return self.post(url, "routing operation", data={"AtWorkCenter": work_center_id,
                                                         "Description": work_center_description,
                                                         "Operation": sequence_operation,
                                                         "StandardSetupTime": setup_hrs,
                                                         "StandardRunTime": run_hrs,
                                                         "StandardCrewSize": 1,
                                                         "FromRevision": revision,
                                                         "Conversion": 1,
                                                         "IsActive": True,
                                                         "Label": "",
                                                         "RoutingOperationProcessCodeID": 1})

    def get_contacts_by_customer(self, customer_id) -> list:
        url = self.api_url + f"/api/CustomerContacts?IncludeinActive=false&CustomerId={customer_id}"
        return self.get(url, "contacts")

    def get_sites_by_customer(self, customer_id) -> list:
        url = self.api_url + f"/api/CustomerSites?IncludeinActive=false&CustomerId={customer_id}"
        return self.get(url, "customer sites")

    def get_part(self, part_number) -> dict:
        url = self.api_url + f"/api/Parts?PartNumber={part_number}"
        try:
            return self.get(url, "part")
        except ValueError as e:
            if "Part doesn't" in str(e):
                return {}

    def get_parts(self) -> dict:
        url = self.api_url + "/api/Parts"
        try:
            return self.get(url, "parts")
        except ValueError as e:
            if "Part doesn't" in str(e):
                return {}

    def create_job(self, customer_number: str, description: str, shipping_address_line_1: str, shipping_address_line_2: str,
                   shipping_attention: str, shipping_city: str,
                   shipping_state: str, shipping_country: str, shipping_postal_code: str,
                   billing_address_line_1: str, billing_address_line_2: str,
                   billing_attention: str, billing_city: str,
                   billing_state: str, billing_country: str,
                   billing_postal_code: str, order_date: datetime, due_date: datetime, customer_po: str, bill_code: str,
                   wip_code: str, percent_1: float,
                   cost_type: str, project_manager: str, currency_code: str, payment_terms_code: str,
                   canadian_tax_exempt_fed: str,
                   canadian_tax_exempt_prov: str, customer_name: str, company_code: str):
        url = self.api_url + "/api/Jobs"
        data = {"CustomerNumber": customer_number,
                "Description": description[0:39] if description is not None else "",
                "AddressLine1": billing_address_line_1,
                "AddressLine2": billing_address_line_2,
                "AddressLine3": "",
                "Attention": billing_attention,
                "City": billing_city,
                "State": billing_state,
                "Country": billing_country,
                "PostalCode": billing_postal_code,
                "DatePo": order_date,
                "DateDue": due_date,
                "CustomerPoNumber": customer_po,
                "BillCode": bill_code,
                "WipCode": wip_code,
                "SalesAgent1Percentage": percent_1,
                "LaborCostType": cost_type,
                "ProjectManager": project_manager,
                "CurrencyCode": currency_code,
                "PrepaidCollect": "C",
                "PaymentTermsCode": payment_terms_code,
                "CanadianTaxExemptFed": canadian_tax_exempt_fed,
                "CanadianTaxExemptProv": canadian_tax_exempt_prov,
                "CustomerName": customer_name,
                "UserText": "",
                "JobReference": "",
                "JobTitle": "",
                "Reference": "",
                "RecordType": "",
                "TaxExemptNumber1": "",
                "TaxExemptNumber2": "",
                "FobPoint": "-",
                "GovernmentContract": "-",
                "PendingCloseRestrictStatus": "P",
                "Routing": "",
                "Memo": "",
                "CompanyCode": company_code,
                "CustomerPOItem": ""
                }
        job = self.post(url, "jobs", data=data)
        job_number = job["jobNumber"]
        logger.info(f"Job number is {job_number}")
        put_url = self.api_url + f"/api/Releases?ReleaseNumber={job_number}"
        self.put(put_url, "releases", data={
            "JobNumber": job_number,
            "ShipToName": shipping_attention,
            "ShipToAddressLine1": shipping_address_line_1,
            "ShipToAddressLine2": shipping_address_line_2,
            "ShipToAddressLine3": "",
            "ShipToCity": shipping_city,
            "ShipToState": shipping_state,
            "ShipToPostalCode": shipping_postal_code,
            "ShipToCountry": shipping_country,
            "CustomerNumber": customer_number,
            "CanadianTaxExemptFed": canadian_tax_exempt_fed,
            "CanadianTaxExemptProv": canadian_tax_exempt_prov,
            "CustomerName": customer_name,
            "WipCode": wip_code,
            "UserText": "",
            "CarrierAccount": "",
            "CompanyCode": company_code,
            "Priority": "00",
            "Description": description[0:39] if description is not None else "",
        })
        return job

    def create_job_line_item(self, job_number: str, line_item_no: int, accept_warnings: bool, part_number: str,
                             revision: str, psm: str, quantity: int,
                             unit_price: float, uom: str, mrp_status: str, canadian_fed_tax_code: str,
                             canadian_prov_tax_code: str, cost_account: str,
                             description: str,
                             location_code: str, material_cost: str, finish_code: str, position_number: str,
                             receiving_part_number: str,
                             revision_level: str, suggested_order_action: str, work_order: str):
        line_item_no = str(line_item_no).zfill(3)
        url = self.api_url + f"/api/ReleaseLineItems?JobNumber={job_number}&LineNumber={line_item_no}&AcceptWarnings={str(accept_warnings)}"
        if revision is None:
            revision = "-"
        return self.post(url, "job line item", data={"PartNumber": part_number,
                                                     "Revision": revision,
                                                     "PartRevision": revision,
                                                     "PSM": psm,
                                                     "Quantity": quantity,
                                                     "UnitPrice": unit_price,
                                                     "UOM": uom,
                                                     "MRPStatus": mrp_status,
                                                     "CanadianFedTaxCode": canadian_fed_tax_code,
                                                     "CanadianProvTaxCode": canadian_prov_tax_code,
                                                     "CostAccount": cost_account,
                                                     "Description1": description[0:39] if description is not None else "",
                                                     "LocationCode": location_code,
                                                     "MaterialCostAccount": material_cost,
                                                     "FinishCode": finish_code,
                                                     "PositionNumber": position_number,
                                                     "RevisionLevel": revision_level,
                                                     "ReceivingPartNumber": receiving_part_number,
                                                     "SuggestedOrderAction": suggested_order_action,
                                                     "WorkOrder": work_order,
                                                     "DateRequested": datetime.now(),
                                                     "DatePromised": datetime.now()
                                                     })
