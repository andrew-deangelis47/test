import os
import sys
from time import perf_counter
from baseintegration.datamigration import logger
from baseintegration.integration import Integration
import configparser
from paperless.objects.customers import Contact, Account, AccountList
from paperless.objects.quotes import Quote
from paperless.objects.events import Event
import argparse
import json
from paperless.client import PaperlessClient, PaperlessException
from django.utils.text import slugify
import pycountry
from baseintegration.utils.suffixes import STREET_SUFFIX_ABBREVS
import logging
import debugpy
from datetime import datetime, timedelta, timezone
from functools import reduce
from paperless.objects.integration_actions import IntegrationAction
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
import pendulum
from django.db.models.expressions import RawSQL
from requests import Response
from django.conf import settings
from django.db import connection, reset_queries, OperationalError, Error as DjangoError
from typing import Optional, Union, Callable
import pyodbc

BULK_IMPORT_ENTITY_ID_STRING = "(assorted)"
CONNECTION_SUCCESS_STRING = "Connected to ERP successfully!"
CONNECTION_FAILURE_STRING = "Connection failed"


def set_sql_env_variables():
    """This sets the SQL env variables before the import occurs. Only needs to be called during non-test runs"""
    logger.info('Reading SQL secrets file')
    parser = configparser.ConfigParser()
    parser.read(os.path.join(os.path.dirname(__file__), "../../../secrets.ini"))
    try:
        os.environ.setdefault('DB_HOST', parser['SQL']['host'])
        os.environ.setdefault('DB_NAME', parser['SQL']['name'])
        os.environ.setdefault('DB_USERNAME', parser['SQL']['user'])
        os.environ.setdefault('DB_PASSWORD', parser['SQL']['password'])
        if parser['SQL'].get('instance'):
            os.environ.setdefault('DB_INSTANCE', parser['SQL'].get('instance'))
        if parser['SQL'].get('port'):
            os.environ.setdefault('DB_PORT', parser['SQL'].get('port'))
    except KeyError as e:
        logger.info("Could not find one of the SQL connection values. Do you have a [SQL] section in your secrets.ini?")
        raise e


def get_args(parser):
    parser.add_argument("--debug", const=False, nargs="?", dest="debug_mode", help="whether in debug mode")
    subparsers = parser.add_subparsers(dest="command", help="type of test")
    subparsers.add_parser("integration")

    # exporter arguments
    deploy = subparsers.add_parser("exporter", help="Run integration against real database from Paperless to ERP")
    deploy.add_argument("--order-num", dest='order_num',
                        help="Pass this in if you want to run integration against single order")
    deploy.add_argument("--quote-num", dest='quote_num',
                        help="Pass this in if you want to run integration against single quote")

    # autoquote arguments
    autoquote = subparsers.add_parser("autoquote", help="Run auto quote against single quote.")
    autoquote.add_argument("--quote-num", dest='quote_num',
                           help="Pass this in if you want to run auto quote against single quote")

    # importer arguments
    importer = subparsers.add_parser("importer", help="Run importer from ERP to Paperless")
    importer.add_argument("--account-id", dest='account_id',
                          help="Pass this in if you want to run importer against single ERP account")
    importer.add_argument("--purchased-component-id", dest='purchased_component_id',
                          help="Pass this in if you want to run importer against single ERP purchased component")
    importer.add_argument("--material-id", dest='material_id',
                          help="Pass this in if you want to run importer against single ERP material")
    importer.add_argument("--work-center-id", dest='work_center_id',
                          help="Pass this in if you want to run importer against single ERP work center")
    importer.add_argument("--vendor-id", dest='vendor_id',
                          help="Pass this in if you want to run importer against single ERP vendor")
    importer.add_argument("--service-id", dest='service_id',
                          help="Pass this in if you want to run importer against a single ERP service")
    importer.add_argument("--repeat-part-id", dest='repeat_part_id',
                          help="Pass this in if you want to run the repeat part importer")
    importer.add_argument("--quote-num", dest='quote_num',
                          help="Pass this in if you want to run custom logic for a quote import")
    importer.add_argument("--custom-id", dest='custom_id',
                          help="Pass this in if you want to run the custom table importer")
    subparsers.add_parser("connect", help="Run Python shell with connection setup")
    return parser.parse_args()


def add_v2_module_path(module_name: str, integration: Integration):
    """
    points the path to the customer directory to get the module
    """

    module_path = f'../../customers/{integration.paperless_config.slug}/{module_name}'  # This could be any string representing a module
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), module_path)))


def get_data_migrator(action_type, integration: Integration):
    if action_type == "export_order":
        from custom_order_exporter import CustomOrderExporter
        return CustomOrderExporter(integration)
    elif action_type == "export_quote":
        from custom_quote_exporter import CustomQuoteExporter
        return CustomQuoteExporter(integration)
    elif action_type == "auto_quote":
        if integration.paperless_config.v2_integration:
            add_v2_module_path("custom_auto_quoter", integration)
        from custom_auto_quoter import CustomAutoQuoter
        return CustomAutoQuoter(integration)
    elif action_type == "import_account":
        from custom_account_importer import CustomAccountImporter
        return CustomAccountImporter(integration)
    elif action_type == "import_material":
        from custom_material_importer import CustomMaterialImporter
        return CustomMaterialImporter(integration)
    elif action_type == "import_purchased_component":
        from custom_purchased_component_importer import CustomPurchasedComponentImporter
        return CustomPurchasedComponentImporter(integration)
    elif action_type == "import_work_center":
        from custom_work_center_importer import CustomWorkCenterImporter
        return CustomWorkCenterImporter(integration)
    elif action_type == "import_vendor":
        from custom_vendor_importer import CustomVendorImporter
        return CustomVendorImporter(integration)
    elif action_type == "import_service":
        from custom_outside_service_importer import CustomOutsideServiceImporter
        return CustomOutsideServiceImporter(integration)
    elif action_type == "import_custom_table_record":
        from custom_custom_table_importer import CustomCustomTableRecordImporter
        return CustomCustomTableRecordImporter(integration)
    elif action_type == "import_repeat_part":
        from custom_repeat_part_importer import CustomRepeatPartImporter
        return CustomRepeatPartImporter(integration)
    elif action_type == "import_material_pricing":
        from custom_material_pricing_importer import CustomMaterialPricingImporter
        return CustomMaterialPricingImporter(integration)
    else:
        raise ValueError("Data migrator not found, are you sure your action type is correct?")


def run_integration():  # noqa: C901
    # Runner has three scenarios - test, run single order, run integration
    args = get_args(argparse.ArgumentParser())
    integration = Integration()
    if args.debug_mode == "debug":
        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
    if args.command == "integration":
        integration.run()
    elif args.command == 'autoquote':
        if args.quote_num is None:
            raise Exception('Unrecognized argugument for autoquote command.')

        exporter = get_data_migrator("auto_quote", integration=integration)
        exporter.run(args.quote_num)

    elif args.command == "exporter":
        if args.order_num is not None:
            exporter = get_data_migrator("export_order", integration=integration)
            exporter.run(args.order_num)
        elif args.quote_num is not None:
            exporter = get_data_migrator("export_quote", integration=integration)
            exporter.run(args.quote_num)
        else:
            integration.run()
    elif args.command == "importer":
        # if passed ID to runner is "first" then will run a full one time import
        if args.account_id is not None:
            importer = get_data_migrator("import_account", integration=integration)
            importer.run(args.account_id)
        elif args.material_id is not None:
            importer = get_data_migrator("import_material", integration=integration)
            importer.run(args.material_id)
        elif args.purchased_component_id is not None:
            importer = get_data_migrator("import_purchased_component", integration=integration)
            importer.run(args.purchased_component_id)
        elif args.work_center_id is not None:
            importer = get_data_migrator("import_work_center", integration=integration)
            importer.run(args.work_center_id)
        elif args.vendor_id is not None:
            importer = get_data_migrator("import_vendor", integration=integration)
            importer.run(args.vendor_id)
        elif args.service_id is not None:
            importer = get_data_migrator("import_service", integration=integration)
            importer.run(args.service_id)
        elif args.repeat_part_id is not None:
            importer = get_data_migrator("import_repeat_part", integration=integration)
            importer.run(args.repeat_part_id)
        elif args.quote_num is not None:
            importer = get_data_migrator("import_material_pricing", integration=integration)
            importer.run(args.quote_num)
        elif args.custom_id is not None:
            importer = get_data_migrator("import_custom_table_record", integration=integration)
            importer.run(args.custom_id)
        else:
            integration.run()
    else:
        pass


def safe_round(f):
    try:
        return round(f, 2)
    except TypeError:
        return f


def object_to_query(obj) -> str:
    """This helper function returns the insert query for a given Django object"""
    from django.db.models import sql
    values = obj._meta.local_fields
    q = sql.InsertQuery(obj)
    q.insert_values(values, [obj])
    compiler = q.get_compiler('default')
    # Normally, execute sets this, but we don't want to call execute
    setattr(compiler, 'return_id', False)
    stmts = compiler.as_sql()
    stmt = [stmt % params for stmt, params in stmts]
    logger.info(stmt[0])
    return str(stmt[0])


def trim_django_model(model):
    """
    This helper function takes a single Django model as an argument
    - Iterates through each attribute on the model
    - Gets the max length of each field as prescribed by the Django model (._meta information)
    - Trims every CharField down to the max length
    - Returns the model ready to be saved
    """
    if model is None:
        logger.info("No model was supplied. Cannot truncate model!")
        return None
    for key in model.__dict__:
        max_length = None
        try:
            max_length = model._meta.get_field(f"{key}").max_length
        except Exception:
            pass
        if max_length is not None:
            model_value = getattr(model, key)
            if model_value is not None and isinstance(model_value, str):
                if len(model_value) > max_length:
                    truncated_value = model_value[:max_length]
                    logger.info(f"Truncating the value for key {key} from value {model_value} to {truncated_value}")
                    setattr(model, key, truncated_value)
    return model


def custom_table_put(client: PaperlessClient, url: str, data: dict, identifier: str) -> dict:
    response: Response = client.request(url, data=json.dumps(data), method="put")
    return handle_custom_table_response(client, url, data, identifier, response)


def custom_table_delete_row(client: PaperlessClient, url: str, data: dict, identifier: str) -> dict:
    response: Response = client.request(url, data=json.dumps(data), method="delete")
    return handle_custom_table_response(client, url, data, identifier, response)


def custom_table_patch(client: PaperlessClient, url: str, data: dict, identifier: str):
    response = client.request(url, data=json.dumps(data), method="patch")
    return handle_custom_table_response(client, url, data, identifier, response)


def handle_custom_table_response(client: PaperlessClient, url: str, data: dict, identifier: str, response: Response) -> dict:
    try:
        if response.status_code in [200, 201]:
            logger.info(f"Processed {identifier} successfully")
            return response.json()
        if response.status_code == 204:
            logger.info(f"Processed {identifier} successfully")
            return response.status_code
        if response.status_code == 502:
            response = client.request(url, data=json.dumps(data), method="patch")
            if response.status_code in [200, 201]:
                logger.info(f"Processed {identifier} successfully")
                return response.json()
            raise Exception(f"Did not process {identifier} successfully")
        raise Exception(f"Did not process {identifier} successfully")
    except PaperlessException as e:
        if e.error_code == 502:
            response = client.request(url, data=json.dumps(data), method="patch")
            if response.status_code in [200, 201]:
                logger.info(f"Processed {identifier} successfully")
                return response.json()
            raise Exception(f"Did not process {identifier} successfully")
        raise Exception(f"Did not process {identifier} successfully")


def repeat_part_bulk_post(client: PaperlessClient, url: str, data: dict):
    logger.info(f"Attempting to post a batch of repeat part data.\n"
                f"Posting to user group: {client.group_slug} at url: {client.base_url}/{url}")
    response = client.request(url, data=json.dumps(data), method="post")
    return response


def update_account_erp_code(integration: Integration, account_id, erp_id):
    if not integration.paperless_config.should_write_to_paperless_parts:
        logger.info("Not updating account erp code since should_write_to_paperless_parts is not set to True")
        return
    logger.info(f'Updating Account record in Paperless Parts to have erp_code {erp_id}')
    account = Account.get(account_id)
    account.erp_code = erp_id
    account.update()


def create_new_paperless_parts_account(integration: Integration, erp_id, business_name, contact_id):
    account_id = None
    try:
        if not integration.paperless_config.should_write_to_paperless_parts:
            logger.info("Not creating new Account since should_write_to_paperless_parts is not set to True")
            return
        logger.info(f'Creating new Account record in Paperless Parts with name {business_name} and erp_code {erp_id}')
        account = Account(name=business_name, erp_code=erp_id)
        account.create()
        account_id = account.id

        # Also associate the contact from this Order with the newly-created account
        contact = Contact.get(contact_id)
        logger.info(f'Associating Contact {contact.email} with the newly-created Account in Paperless Parts')
        contact.account_id = account_id
        contact.update()
    except Exception as e:
        logger.info(f'Encountered error creating new Paperless Parts Account: {e}')

    # If we created a new Account, we need to pass its ID along to other functions
    return account_id


def update_quote_erp_code(integration: Integration, quote_number, quote_revision, erp_id):
    logger.info(f'Updating Quote record in Paperless Parts to have erp_code {erp_id}')
    if not integration.paperless_config.should_write_to_paperless_parts:
        logger.info("Not updating quote erp code since should_write_to_paperless_parts is not set to True")
        return
    quote = Quote.get(quote_number, quote_revision)
    quote.erp_code = erp_id
    quote.update()


def address_tokenize(street_address):
    """Tokenize street address lines"""
    tokens = slugify(street_address).split('-')
    if len(tokens) > 1:
        return [
            STREET_SUFFIX_ABBREVS[t] if t in STREET_SUFFIX_ABBREVS else t
            for t in tokens
        ]
    else:
        return tokens


def tokenize(name):
    """Tokenization for business names"""
    tokens = slugify(name).split('-')
    if len(tokens) > 1:
        return [t for t in tokens if t not in STOP_WORDS]
    else:
        return tokens


def normalize_country(country_name):
    country_alpha_3_code = None
    if country_name is not None:
        country_name = country_name.strip()
        country = pycountry.countries.get(name=country_name)
        if country is not None:
            country_alpha_3_code = country.alpha_3
        return country_alpha_3_code
    else:
        return None


def clean_up_phone_number(phone_number):
    import re
    try:
        return re.sub(r'\D', '', phone_number)[:10]  # noqa: W605
    except:
        return None


def set_blank_to_default_value(val, default_value=None):
    if val is None:
        return default_value
    elif isinstance(val, str) and val.strip() == '':
        return default_value
    else:
        return val


def is_blank(val):
    if val is None:
        return True
    elif isinstance(val, str) and val.strip() == '':
        return True
    else:
        return False


def set_custom_formatter(integration: Integration, resource_type: str, resource_id: str):
    f = logging.Formatter(
        f'%(asctime)s - %(name)s - %(levelname)s - running {resource_type} {resource_id} - %(message)s')
    integration.ph.setFormatter(f)
    integration.fh.setFormatter(f)


def create_or_update_account(integration: Integration, erp_code: str, account_name: str) -> (Account, bool):
    pp_accounts_abridged = Account.filter(
        erp_code=erp_code)  # TODO - make it so the Account.filter returns Account objects, not AccountList objects to save a request?
    pp_account_abridged = pp_accounts_abridged[0] if pp_accounts_abridged else None
    if pp_account_abridged is not None:
        account_is_new = False
        pp_account = Account.get(pp_account_abridged.id)
        logger.info("Account found in Paperless! Going to edit rather than create")
    else:
        # next check by name if there is a matching acc
        pp_accounts_abridged = AccountList.filter(name=account_name, null_erp_code=None)
        pp_account_abridged = pp_accounts_abridged[0] if pp_accounts_abridged else None
        if pp_account_abridged is not None:
            # if no erp_code, give the existing account the erp_code and update. Otherwise, create new acc called "account - erp code"
            pp_account = Account.get(pp_account_abridged.id)
            if pp_account.erp_code is None or pp_account.erp_code == "":
                logger.info("Matching account found with no erp code, going to update w erp code")
                update_account_erp_code(integration, pp_account_abridged.id, erp_code)
                account_is_new = False
            else:
                account_is_new = True
                pp_account = Account(name=f"{account_name} - {erp_code}", erp_code=erp_code)
                logger.info("Creating new Paperless account")
        else:
            account_is_new = True
            pp_account = Account(name=account_name, erp_code=erp_code)
            logger.info("Creating new Paperless account")
    return pp_account, account_is_new


def get_or_create_contact(email: str, account: Account) -> (Contact, bool):
    contacts = Contact.filter(account_id=account.id)
    matching_contacts = [contact for contact in contacts if contact.email == email]
    if matching_contacts:
        # contact found
        contact_is_new = False
        contact = Contact.get(matching_contacts[0].id)
    else:
        # create new contact
        contact_is_new = True
        contact = Contact(account_id=account.id, first_name='', last_name='', email=email)
    return contact, contact_is_new


def reset_custom_formatter(integration: Integration):
    integration.ph.setFormatter(integration.default_formatter)
    integration.fh.setFormatter(integration.default_formatter)


STOP_WORDS = ['and', 'assn', 'assoc', 'co', 'comp', 'corp', 'company',
              'corporation', 'dba', 'gmbh', 'group', 'inc', 'incorporated',
              'intl', 'llc', 'llp', 'lp', 'ltd', 'manufacturing', 'mfg']


class Workcenter:

    def __init__(self):
        self.name = "n/a"


class OutsideService:

    def __init__(self):
        self.name = "n/a"


class Vendor:

    def __init__(self):
        self.name = "n/a"


def should_time_out_integration_action_from_event(event: Event):
    if (datetime.utcnow() - event.created_dt.replace(tzinfo=None)).days > 3:
        return True
    return False


def safe_get(obj, keys, default_value=None):
    """
    This function can be used to safely get information out of objects
    Helps avoid the case where you call on a django object .attribute and the object is none
    So for example, instead of writing: addr = contact.address if contact is not None else None
    You can write: addr = safe_get(contact, 'address')
    This also allows you to write in one line: attention = safe_get(order, 'shipping_info.attention')
    For pulling from nested dicts
    inspired by stackoverflow: https://stackoverflow.com/questions/64285182/optional-chaining-in-python
    """
    if obj is None:
        return default_value

    def _getattr(obj, attr):
        try:
            return getattr(obj, attr)
        except AttributeError:
            return default_value

    return reduce(_getattr, keys.split('.'), obj)


def safe_get_non_null(obj, keys, default_value=None):
    """
    This function can be used to safely get information out of objects
    Returns the object attribute only if it is not None, otherwise returns the default value
    """
    if obj is None:
        return default_value

    def _getattr(obj, attr):
        try:
            attr_val = getattr(obj, attr)
            return attr_val if attr_val is not None else default_value
        except AttributeError:
            return default_value

    return reduce(_getattr, keys.split('.'), obj)


def mark_action_as_completed(action: IntegrationAction, success_message: str) -> None:
    action.status = "completed"
    action.status_message = success_message[:250] if success_message is not None else ""
    action.update()


def mark_action_as_failed(action: IntegrationAction, e: Exception, entity_id) -> None:
    error_message = str(e)
    action.status_message = error_message[:250] if error_message is not None else ""
    if isinstance(e, CancelledIntegrationActionException):
        logger.info(f"Cancelled the {action.type}: {entity_id}. Moving on")
        action.status = "cancelled"
    else:
        logger.info(f"Failed the {action.type}: {entity_id}. Moving on")
        action.status = "failed"
    action.update()


def mark_action_as_cancelled(action: IntegrationAction, message: str) -> None:
    action.status = "cancelled"
    action.status_message = message[:250] if message is not None else ""
    action.update()


def get_last_action_datetime(managed_integration_uuid: str, action_type: str, bulk: bool = False, database_minutes_offset=0):
    ia_record = IntegrationAction.get_first_record(managed_integration_uuid=managed_integration_uuid, type=action_type)
    # if we're doing a bulk import, get everything from history
    if bulk:
        return pendulum.naive(year=1970, month=1, day=2)
    if ia_record and ia_record.entity_id != BULK_IMPORT_ENTITY_ID_STRING:
        logger.info("Last action is likely a manual action, getting last bulk action")
        ia_record = get_last_bulk_action(managed_integration_uuid, action_type)
    # if we're doing a new type of import or we have not found a reasonable high water mark, just get the last 3 days worth of stuff
    if ia_record is None:
        return datetime.now() - timedelta(days=3)
    delta_minutes = database_minutes_offset + 10
    dt_delta = timedelta(minutes=delta_minutes)
    return ia_record.created_dt - dt_delta


def get_last_bulk_action(
    managed_integration_uuid: str,
    type: Optional[str] = None,
) -> Optional[IntegrationAction]:

    params = {'status': None, "type": type}

    client = PaperlessClient.get_instance()
    response = client.get_resource_list(
        IntegrationAction.construct_list_url(managed_integration_uuid=managed_integration_uuid),
        params=params,
    )
    resource_list = IntegrationAction.parse_list_response(response)
    for resource in resource_list:
        ia = IntegrationAction.from_json(resource)
        if ia.entity_id == BULK_IMPORT_ENTITY_ID_STRING:
            return ia
    return None


def get_sql_query_for_last_action_datetime(managed_integration_uuid: str, action_type: str, bulk: bool = False) -> str:
    last_date_obj = get_last_action_datetime(managed_integration_uuid=managed_integration_uuid,
                                             action_type=action_type, bulk=bulk)
    last_date_str = last_date_obj.strftime("%Y-%m-%d %H:%M:%S")
    date_to_search = datetime.strptime(last_date_str, '%Y-%m-%d %H:%M:%S')
    return f"SELECT DATEADD(second, -DATEDIFF(second, getdate(), getutcdate()), '{date_to_search}')"


def get_last_action_datetime_sql(managed_integration_uuid: str, action_type: str, bulk: bool = False) -> RawSQL:
    to_search_adjusted_time_query = get_sql_query_for_last_action_datetime(managed_integration_uuid, action_type, bulk)
    return RawSQL(to_search_adjusted_time_query, [])


def get_last_action_datetime_value(managed_integration_uuid: str, action_type: str, bulk: bool = False) -> str:
    to_search_adjusted_time_query = get_sql_query_for_last_action_datetime(managed_integration_uuid, action_type, bulk)
    cursor = connection.cursor()
    cursor.execute(to_search_adjusted_time_query)
    return cursor.fetchone()[0]


def convert_datetime_to_utc(datetime_object):
    if not isinstance(datetime_object, datetime):
        return None
    utc_timestamp = datetime_object.replace(tzinfo=timezone.utc).timestamp()
    return int(utc_timestamp)


def current_datetime_utc():
    return convert_datetime_to_utc(datetime.now())


class DjangoPerformanceLogger:
    """
    A utility for tracking performance of SQL-based integrations. Initialize it when you want to start keeping
    track of time/queries, then use log() to see the number of seconds/queries since the last log.

    This is for performance testing only. Do not commit any usages of this.
    """
    def __init__(self):
        settings.DEBUG = True
        self.last_time = perf_counter()
        self.counter = 1
        reset_queries()

    def log(self):
        new_time = perf_counter()
        print(f"Stats at log number {self.counter}:")
        print(f"Time: {new_time-self.last_time} seconds")
        print(f"Queries: {len(connection.queries)}")
        self.last_time = new_time
        self.counter += 1
        reset_queries()


def get_string_size(string: str):
    """Returns size of given string in MB, using UTF-8 encoding."""
    byte = bytes(string, "utf-8")
    size = round(len(byte) / 1000000, 3)  # MB
    return size


def get_dict_size(dictionary: dict):
    """Returns size of given dict as JSON in MB, using UTF-8 encoding."""
    json_string = json.dumps(dictionary)
    return get_string_size(json_string)


def log_connection_error_for_icc(exception: Exception):
    """
    Standard for logging errors during connection checks.
    This output is used by the ICC to display errors to the user. Be careful when editing this function or
    its usages.
    """
    if isinstance(exception, OperationalError) and hasattr(exception, 'args'):
        error_number = exception.args[0]
        detailed_error_message = exception.args[1]
        clean_error_message = detailed_error_message.replace(
            f"[{error_number}] [Microsoft][ODBC Driver 17 for SQL Server]", "")
    else:
        detailed_error_message = clean_error_message = str(exception)
    one_line_detailed_message = "  ".join(detailed_error_message.splitlines())
    one_line_clean_message = "  ".join(clean_error_message.splitlines())
    logger.error(f"[ICC_CLEAN_ERROR]{one_line_clean_message}")
    logger.error(f"[ICC_DETAILED_ERROR]{one_line_detailed_message}")


def is_deadlock_error(error: Union[pyodbc.Error, DjangoError]):
    sqlstate = error.args[0] if hasattr(error, 'args') and len(error.args) > 0 else None
    return sqlstate == '40001'


def retry_if_deadlocked(fn: Callable[[], any]):
    """
    Run the given function; if a database deadlock occurs, retry it several more times.
    """
    max_attempts = 3
    current_attempt = 0
    while True:
        try:
            return fn()
        except (pyodbc.Error, DjangoError) as error:
            if is_deadlock_error(error) and current_attempt < max_attempts:
                logger.error("Deadlock error occurred, retrying", exc_info=error)
                current_attempt += 1
            else:
                raise error
