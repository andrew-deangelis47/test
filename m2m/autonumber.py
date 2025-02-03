"""
Made2Manage autonumber mixin for setting unique keys using the sysequ table.
"""
from django.db import models, transaction
from baseintegration.datamigration import logger


class AutoNumberMixin(models.Model):
    class Meta:
        abstract = True

    def save_with_autonumber(self, *args, **kwargs):
        assert hasattr(self, 'auto_number_attrs'), \
            'Model class must have `auto_number_attrs` attribute to use ' \
            'AutoNumberMixin'
        from m2m.models import Sysequ
        with transaction.atomic():
            column: AutoColumn
            for column in self.auto_number_attrs:
                qs = Sysequ.objects.select_for_update().filter(
                    fcclass=column.m2m_name)
                an_row: Sysequ = qs.first()
                setattr(self, column.attr_name, '{:06d}'.format(int(an_row.fcnumber)))
                an_row.fcnumber = str(int(an_row.fcnumber) + 1)
                an_row.save()
            self.save(*args, **kwargs)


class AutoColumn:
    def __init__(self, attr_name, m2m_name):
        self.attr_name = attr_name
        self.m2m_name = m2m_name


class AddressNumberMixin(models.Model):
    class Meta:
        abstract = True

    def save_with_number(self, *args, **kwargs):
        assert self.fcalias == 'SLCDPM', 'Can only number SLCDPM addresses'
        assert self.fcaliaskey, 'Must specify fcaliaskey to number address'
        from m2m.models import Syaddr
        with transaction.atomic():
            qs = Syaddr.objects.select_for_update().filter(
                fcalias='SLCDPM',
                fcaliaskey=self.fcaliaskey,
                fcaddrtype=self.fcaddrtype,
            ).values('fcaddrkey')
            max_int = 0
            for row in qs:
                try:
                    val = int(row['fcaddrkey'])
                    if val > max_int:
                        max_int = val
                except (TypeError, ValueError):
                    pass
            self.fcaddrkey = '{:06d}'.format(max_int + 1)
            self.save(*args, **kwargs)


class PartNumberMixin(models.Model):
    class Meta:
        abstract = True

    def save_with_number(self, *args, **kwargs):
        if self.fpartno is None:
            from m2m.models import Soitem
            with transaction.atomic():
                last_item = Soitem.objects.select_for_update().filter(
                    fpartno__startswith='FG').order_by('-fpartno').values(
                    'fpartno').first()
                try:
                    last_part_number = last_item['fpartno']
                    next_number = int(last_part_number[2:]) + 1
                    self.fpartno = 'FG{:06d}'.format(next_number)
                except (ValueError, TypeError) as e:
                    logger.exception(e)
                self.save(*args, **kwargs)
            return
        self.save(*args, **kwargs)
