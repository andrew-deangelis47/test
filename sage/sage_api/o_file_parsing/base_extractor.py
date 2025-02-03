from sage.models.sage_models.sage_model_factory import SageModelFactory


class BaseExtractor:
    primary_table_key: str = None
    _entity_seperator: str = '|'

    def extract_full_entities(self, i_file: str):
        # split i file anytime we see the primary table key
        i_file_full_payload = '|' + i_file
        full_account_entities = i_file_full_payload.split(f'|{self.primary_table_key}')

        # get rid of first entity, just junk produced by the split function
        full_account_entities = full_account_entities[1:]

        # add the primary table  key to the beginning of each entity for consistency, stripped out after split function
        # also add a seperator to the end of the entity
        for x in range(len(full_account_entities)):
            full_account_entities[x] = self.primary_table_key + full_account_entities[x] + self._entity_seperator

        # we dont need the last seperator, duplicate
        if len(full_account_entities) > 0:
            full_account_entities[len(full_account_entities) - 1] = full_account_entities[len(full_account_entities) - 1][:-1]

        return full_account_entities

    def extract_entities(self, entity_full_string: str, key: str, class_name: str):
        # split by the entity delimiter
        entities = entity_full_string.split('|')

        # get rid of first entity, just junk produced by the split function
        entities = entities[:-1]

        models = []
        for entity in entities:
            if entity[0] == key:
                # add a seperator to the end, stripped out due to split function
                entity = entity + self._entity_seperator
                models.append(SageModelFactory.create_sage_model(class_name, entity))

        return models
