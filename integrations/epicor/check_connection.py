# implement check_connection() function in a script called check_connection.py to get this to work
# check_connection should return None if successfully and an exception
from baseintegration.integration import Integration
from epicor.exporter.exporter import EpicorOrderExporter
from epicor.customer import Customer
from baseintegration.utils import CONNECTION_SUCCESS_STRING, CONNECTION_FAILURE_STRING, log_connection_error_for_icc


def check_connection() -> None:
    try:
        EpicorOrderExporter(Integration())
        Customer.get_all()
        print(CONNECTION_SUCCESS_STRING)
    except Exception as e:
        print(e)
        log_connection_error_for_icc(e)
        print(CONNECTION_FAILURE_STRING)
        raise ValueError(CONNECTION_FAILURE_STRING)
