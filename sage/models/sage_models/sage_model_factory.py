from sage.models.sage_models.base_object import BaseObject as SageBaseObject
from baseintegration.datamigration import logger
from sage.models.sage_models.customer.contact import Contact

"""
This class is responsible for taking raw data from a Sage x3
API request and converting it to the desired model based on
it's SEQUENCE property where the class property is mapped to a portion
of the raw payload
"""


def _massage_data_for_contact(contact: Contact):
    if len(contact.first_name) == 0:
        contact.first_name = "default_first_name"
    if len(contact.last_name) == 0:
        contact.first_name = "default_last_name"
    return contact


class SageModelFactory:

    @staticmethod
    def create_sage_model(resource_cls: SageBaseObject, data_payload):
        parsed_payload = data_payload.split(resource_cls.FIELD_DELIMITER)
        sage_model = resource_cls()
        for object_property in sage_model.SEQUENCE:
            try:
                field, position = object_property
                value = parsed_payload[position]

                # special case if the value we are setting is the last in the entity payload we also get the '|' character
                # need to strip it
                if position == sage_model.TOTAL_ELEMENTS - 1:
                    value = value[:-1]
                # set the attribute
                setattr(sage_model, field, value)
            except IndexError:
                logger.error(f'\nMissing data point in import payload for {resource_cls} object, skipping...')
                logger.error(f'attribute = {field}')
                logger.error(f'payload position = {position}')

        # massage data for contact
        if isinstance(sage_model, Contact):
            sage_model = _massage_data_for_contact(sage_model)

        return sage_model
