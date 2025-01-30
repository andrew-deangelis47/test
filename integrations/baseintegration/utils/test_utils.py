# This file contains utility methods that are shared between ERP tests
from typing import Optional, List

from paperless.objects.orders import Order
from paperless.objects.quotes import Quote
import random
import string

from django.db.models.fields import Field, CharField, TextField, BooleanField, DecimalField, FloatField, \
    IntegerField, AutoField, DateTimeField, SmallIntegerField
from django.db.models.query_utils import DeferredAttribute
from django.db.models import Model, ForeignKey, OneToOneField

from paperless.client import PaperlessClient

orders = {}
quotes = {}


def get_order(order_num: int):
    # cache orders to avoid hitting rate limit
    if order_num not in orders:
        orders[order_num] = Order.get(order_num)
    return orders[order_num]


def get_quote(quote_num: int, quote_revision_num: Optional[int] = None) -> Quote:
    # cache orders to avoid hitting rate limit
    if (quote_num, quote_revision_num) not in quotes:
        quotes[(quote_num, quote_revision_num)] = Quote.get(quote_num, quote_revision_num)
    return quotes[(quote_num, quote_revision_num)]


def generate_random_string(length: int):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def fill_model(model: Model):
    """
    Sets all required attributes in the given model instance to dummy values, if they have not already been set.
    """
    model_dict = vars(type(model))
    for field_name, field_value in vars(model).items():
        if field_value is None and field_name in model_dict:
            deferred_field: DeferredAttribute = model_dict[field_name]
            field: Field = deferred_field.field
            field_type = type(field)
            if not field.null and field_type != AutoField:
                if field_type in [CharField, TextField]:
                    val = ""
                elif field_type in [BooleanField]:
                    val = False
                elif field_type in [DecimalField, FloatField, IntegerField, SmallIntegerField]:
                    val = 0
                elif field_type in [DateTimeField]:
                    val = "1900-01-01"
                elif field_type in [ForeignKey, OneToOneField]:
                    val = fill_and_save(field.related_model()).pk
                else:
                    val = ""
                setattr(model, field_name, val)


def fill_and_save(model: Model):
    """
    Fills unset values with dummy values, then saves the model instance.
    """
    fill_model(model)
    model.save()
    return model


def get_repeat_parts_from_backend(part_number, root_only=True) -> List[dict]:
    part_search_json = {"part_number": part_number, "root_only": root_only}
    url = "/v2/erp_stores/public/historical_work_search_view"
    client: PaperlessClient = PaperlessClient.get_instance()
    response = client.request(url, method="get", params=part_search_json)
    assert response.status_code == 200
    return response.json()
