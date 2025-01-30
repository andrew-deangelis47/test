"""Model mixin for automatic atomic numbering of various JobBOSS entities.

In addition to autonumber primary keys, JobBOSS has two other styles of
autonumbered columns:

1. "AutoNumber" entities where the last used number is stored in the JobBOSS
Auto_Number table, with a row for each type of entity. We call this
"AutoNumberColumn".

2. Secondary autonumber columns where a column other than the primary key has
an auto incremented unique integer. We call this "AutoIncrementColumn".
"""
from django.db import models, transaction
from django.db.models import Max


class AutoNumberMixin(models.Model):
    class Meta:
        abstract = True

    def save_with_autonumber(self, *args, **kwargs):
        assert hasattr(self, 'auto_number_attrs'), \
            'Model class must have `auto_number_attrs` attribute to use ' \
            'AutoNumberMixin'
        with transaction.atomic():
            auto_type: AutoColumnType
            for auto_type in self.auto_number_attrs:
                if not getattr(self, auto_type.attr_name):
                    auto_type.set_column(self)
            self.save(*args, **kwargs)


class AutoColumnType:
    def __init__(self, attr_name):
        self.attr_name = attr_name

    def set_column(self, record):
        raise NotImplementedError


class AutoNumberColumn(AutoColumnType):
    def __init__(self, attr_name, e2_name):
        super().__init__(attr_name)
        self.e2_name = e2_name

    def set_column(self, record):
        from e2.models import Nextnumber
        qs = Nextnumber.objects.select_for_update().filter(object=self.e2_name)
        an_row: Nextnumber = qs.first()

        # E2 has unfortunate logic that updates the NextNumber table when both entering and exiting the "New" screen for
        # Orders. Consider the situation where a user manually creates an order (Order N) by clicking "New". Immediately
        # upon navigating to the Order editing screen, the NextNumber for ORDER is updated to N+1. Now suppose an order
        # is imported automatically by the integration while that screen remains open. This will create Order N+1 and
        # update the NextNumber for ORDER to N+2. When the screen is closed, E2 will set the NextNumber for ORDER back
        # to N+1, which means that the next order that is processed automatically by the integration will try to assign
        # Order number N+2 and will fail due to an integrity error. As a result, we cannot rely solely on the NextNumber
        # table. We need logic that searches for the next available order number, starting with the value in the
        # NextNumber table
        next_available_number = an_row.nextnumber
        model = type(record)
        existing_record_for_number = model.objects.filter(**{self.attr_name: str(next_available_number)}).first()
        while existing_record_for_number is not None:
            next_available_number += 1
            existing_record_for_number = model.objects.filter(**{self.attr_name: str(next_available_number)}).first()

        setattr(record, self.attr_name, str(next_available_number))
        an_row.nextnumber = next_available_number + 1
        an_row.save()


class AutoIncrementColumn(AutoColumnType):
    def set_column(self, record):
        manager = record.__class__.objects
        max_value = manager.select_for_update().all().aggregate(
            Max(self.attr_name))['{}__max'.format(self.attr_name)] or 0
        setattr(record, self.attr_name, max_value + 1)
