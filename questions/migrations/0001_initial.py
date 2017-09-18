# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-18 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Url_List',
            fields=[
                ('pk_id', models.AutoField(db_column='pk_id', primary_key=True, serialize=False)),
                ('page_url', models.CharField(max_length=256)),
                ('relative_link', models.CharField(max_length=256)),
                ('absolute_link', models.CharField(max_length=256)),
                ('external_link', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'url_list',
            },
        ),
    ]
