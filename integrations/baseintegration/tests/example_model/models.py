from django.db import models
from ...baseintegration.tests.example_model.settings import IS_TEST
from ...baseintegration.utils.truncated_model import TruncatedModel


class InstaModel(models.Model):
    pk_field = models.IntegerField(db_column="PK_Field", max_length=6, primary_key=True, blank=False, null=False)
    job_title = models.CharField(db_column="Job_Title", max_length=20, blank=True, null=True)
    is_real_job = models.BooleanField(db_column="Is_Real_Job")
    catch_phrase = models.CharField(db_column="Catch_Phrase", max_length=30, blank=True, null=True)
    last_updated = models.DateTimeField(db_column='Last_Updated')

    class Meta:
        managed = IS_TEST


class InstaTruncatedModel(TruncatedModel):
    pk_field = models.IntegerField(db_column="PK_Field", max_length=6, primary_key=True, blank=False, null=False)
    job_title = models.CharField(db_column="Job_Title", max_length=20, blank=True, null=True)
    is_real_job = models.BooleanField(db_column="Is_Real_Job")
    catch_phrase = models.CharField(db_column="Catch_Phrase", max_length=30, blank=True, null=True)
    last_updated = models.DateTimeField(db_column='Last_Updated')

    class Meta:
        managed = IS_TEST
