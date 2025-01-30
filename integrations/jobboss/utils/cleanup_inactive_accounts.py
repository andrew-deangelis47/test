from baseintegration.integration import Integration
from paperless.objects.customers import Account
from baseintegration.utils import logger
import jobboss.models as jb


i = Integration()
client = i._client


def cleanup_inactive_accounts():
    jb_customers = jb.Customer.objects.filter(status="Inactive").all()
    inactive_customer_id_list = set()
    inactive_customer_id_list.update(str(jb_cust.customer) for jb_cust in jb_customers)
    logger.info(f"Found {len(inactive_customer_id_list)} accounts to delete.")
    paperless_accounts = Account.list()
    logger.info(f"There are {len(paperless_accounts)} Paperless Parts accounts in total.")
    for account in paperless_accounts:
        account_erp_code = account.erp_code
        if account_erp_code in inactive_customer_id_list:
            try:
                account = Account.get(account.id)
                logger.info(f"Deleting inactive JB customer ({account_erp_code}) from Paperless Part.")
                account.delete()
            except Exception as e:
                logger.info(f"Could not find or delete:\nAccount.erp_code={account_erp_code}\nAccount.id={account.id}"
                            f"\nERROR: {e}")
