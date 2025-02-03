from paperless.objects.orders import OrderOperation
from baseintegration.utils.custom_table import ImportCustomTable
from datetime import timedelta


class PlexUtils:
    @staticmethod
    def get_op_code(order_op: OrderOperation, erp_config, operation_mapping: list):
        code = None
        plex_operation_code_column_header = erp_config.plex_operation_code_column_header
        paperless_op_header = erp_config.paperless_operation_name_column_header
        definition = order_op.operation_definition_name
        name = order_op.name

        for row in operation_mapping:
            if row[paperless_op_header] != '' and ((definition and row[paperless_op_header] == definition) or (name and row[paperless_op_header] == name)):
                paperless_only = row.get('Paperless_Only', False)
                if paperless_only:
                    return None
                return row[plex_operation_code_column_header]

        if code is None:
            lookup = order_op.get_variable_obj('Operation Lookup')
            code = lookup.row.get('Plex_Operation_Code', '') if lookup else None
        return code if code else order_op.operation_definition_name

    @staticmethod
    def get_timestamp_with_offset(identifier: str):
        date_record = ImportCustomTable.get_last_processed_date(identifier)
        adjusted_date_time = date_record - timedelta(hours=9)
        date_to_search = adjusted_date_time.isoformat().replace('T', ' ')
        return date_to_search
