from django.db import models
from ...baseintegration.utils import trim_django_model
from django.db.models import QuerySet

from ...baseintegration.utils.test_utils import fill_and_save


class TruncatedModelQuerySet(QuerySet):
    def filter(self, *args, **kwargs):
        for key, value in kwargs.items():
            try:
                max_length = self.model._meta.get_field(f"{key}").max_length
                if max_length and isinstance(value, str) and len(value) > max_length:
                    kwargs[key] = value[:max_length]
            except Exception:
                pass
        trim_django_model(self.model)
        self._not_support_combined_queries('filter')
        return self._filter_or_exclude(False, args, kwargs)

    def no_truncate_filter(self, *args, **kwargs):
        """
        For use when the search parameters should not be truncated.
        """
        self._not_support_combined_queries("filter")
        return self._filter_or_exclude(False, args, kwargs)


class TruncatedModel(models.Model):
    objects = TruncatedModelQuerySet.as_manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self = trim_django_model(self)
        return super(TruncatedModel, self).save(*args, **kwargs)

    def fill_and_save(self):
        return fill_and_save(self)
