from .base_extractor import BaseExtractor
from sage.models.sage_models.standard_operations import StandardOperationFullEntity, StandardOperation


class StandardOperationExtractor(BaseExtractor):
    primary_table_key = 'E'

    def get_standard_operations(self, i_file: str):
        # this import is weird, comes in with quotes, remove them
        i_file = i_file.replace('"', '')
        i_file = i_file.replace("'", '')

        raw_full_standard_operations = self.extract_full_entities(i_file)
        full_standard_operation_objects = []

        for raw_full_standard_operation in raw_full_standard_operations:
            standard_operation = self.extract_entities(raw_full_standard_operation, 'E', StandardOperation)[0]

            full_standard_operation_objects.append(
                StandardOperationFullEntity(standard_operation=standard_operation)
            )

        return full_standard_operation_objects
