from .sage_api_filter_generator import SageApiFilterGenerator


def _get_formatted_date(last_update_time: str):
    last_action_datetime = str(last_update_time).split('T')[0]
    data = last_action_datetime.split('-')
    return data[1] + '/' + data[2] + '/' + data[0]


class VendorFilterGenerator(SageApiFilterGenerator):

    def get_filter_by_id(id: str) -> str:
        return f'"BPSNUM=\'{id}\'"'

    def get_filter_by_last_update_time(last_update_time: str) -> str:
        formatted_date = _get_formatted_date(last_update_time)
        return f'"[F:BPS]UPDDAT>[{formatted_date}]"'
