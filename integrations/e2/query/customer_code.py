import re
from typing import Optional
from baseintegration.utils import tokenize
from e2.models import CustomerCode, Terms

MAX_CODE_LENGTH = 12  # max length of cust_code
MAX_CODE_RETRIES = 20
MAX_CUSTOMER_NAME_LENGTH = 30  # max length of customer name


def get_or_create_customer_code(
        name: str,
        code: Optional[str] = None,
) -> CustomerCode:
    """
        Find existing CustomerCode record using supplied customer code or create a new
        CustomerCode.

        :param name: business name
        :param code: optional customer code
        :return: matched or newly created E2 CustomerCode record
        """
    # Try matching based on the unique code first
    if code:
        customer_code = CustomerCode.objects.filter(customer_code=code).first()
        if customer_code is not None:
            return customer_code

    # If no code was supplied, or no match was found, create a new CustomerCode record
    customer_code = create_customer_code(name)
    return customer_code


def create_customer_code(name: str) -> CustomerCode:
    return CustomerCode.objects.create(
        active="Y",
        customer_code=get_available_customer_code(name),
        customer_name=name[0:MAX_CUSTOMER_NAME_LENGTH]
    )


def filter_fuzzy_customer_code(name: str) -> Optional[CustomerCode]:
    qs = CustomerCode.objects
    for token in tokenize(name):
        qs = qs.filter(customer_name__icontains=token)
    if hasattr(CustomerCode, 'last_mod_date'):
        qs.order_by('-last_mod_date')
    for customer_code in qs.all():
        # TODO: NEED TO ACCOUNT FOR MAX CUSTOMER NAME HERE
        if '-'.join(tokenize(customer_code.customer_name)) == '-'.join(tokenize(name)):
            return customer_code
    return None


def get_available_customer_code(name: str):
    """
    Searches for available customer code to satisfy the unique constraint.

    Attempts are made for each normalized word in the name.

    If none are available, we will begin appending numbers to each word in the customers name.

    :param name: str
    :return: str
    """
    tokens = tokenize(name)
    for token in tokens:
        code = token.upper()[0:MAX_CODE_LENGTH]
        if CustomerCode.objects.filter(customer_code=code).count() == 0:
            return code
    for token in tokens:
        code = token.upper()[0:MAX_CODE_LENGTH]
        tries = 0
        while tries < MAX_CODE_RETRIES:
            if CustomerCode.objects.filter(customer_code=code).count() == 0:
                return code
            code = increment_code(code)
            tries += 1
    raise ValueError("Can't find an unused customer code for {}".format(name))


def increment_code(code, max_code_length=MAX_CODE_LENGTH):
    search = re.search('(\d+)$', code)  # noqa: W605
    if search is None:
        if len(code) < max_code_length:
            return code + '1'
        else:
            return code[0:max_code_length - 1] + '1'
    else:
        suffix = search.group(0)
        base_code = code[0:-len(suffix)]
        new_suffix = str(int(search.group(0)) + 1)
        remove = len(base_code) + len(new_suffix) - max_code_length
        if remove > 0:
            base_code = base_code[0:-remove]
        return base_code + new_suffix


def get_or_create_terms(terms_code, net_due_days):
    terms = Terms.objects.filter(termscode=terms_code).first()
    if terms is None:
        terms = Terms.objects.create(
            termscode=terms_code,
            netduedays=net_due_days
        )
    return terms
