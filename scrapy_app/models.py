from __future__ import unicode_literals

from django.db import models


class Start_Url_List(models.Model):
    pk_id = models.AutoField(primary_key=True, db_column="pk_id")
    start_url = models.CharField(max_length=1024)
    executed_on = models.DateTimeField()

    class Meta:
        db_table = 'start_url_list'


class Url_List(models.Model):
    pk_id = models.AutoField(primary_key=True, db_column="pk_id")
    fk_start_url = models.ForeignKey(Start_Url_List, on_delete=models.CASCADE,
                                     db_column="fk_start_url")
    page_url = models.CharField(max_length=1024)
    link = models.CharField(max_length=1024)
    link_type = models.CharField(max_length=50)
    url_category = models.CharField(max_length=50)

    class Meta:
        db_table = 'url_list'
