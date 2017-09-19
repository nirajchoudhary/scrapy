from __future__ import unicode_literals

from django.db import models


class Url_List(models.Model):
    pk_id = models.AutoField(primary_key=True, db_column="pk_id")
    page_url = models.CharField(max_length=256)
    link = models.CharField(max_length=256)
    link_type = models.CharField(max_length=25)

    class Meta:
        db_table = 'url_list'
