# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-03 07:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page_Url_List',
            fields=[
                ('pk_id', models.AutoField(db_column='pk_id', primary_key=True, serialize=False)),
                ('page_url', models.CharField(max_length=1024)),
                ('link_count', models.IntegerField()),
            ],
            options={
                'db_table': 'page_url_list',
            },
        ),
        migrations.CreateModel(
            name='Start_Url_List',
            fields=[
                ('pk_id', models.AutoField(db_column='pk_id', primary_key=True, serialize=False)),
                ('start_url', models.CharField(max_length=1024)),
                ('depth', models.IntegerField()),
                ('page_count', models.IntegerField()),
                ('executed_on', models.DateTimeField()),
            ],
            options={
                'db_table': 'start_url_list',
            },
        ),
        migrations.CreateModel(
            name='Url_List',
            fields=[
                ('pk_id', models.AutoField(db_column='pk_id', primary_key=True, serialize=False)),
                ('link', models.CharField(max_length=1024)),
                ('link_type', models.CharField(max_length=50)),
                ('url_category', models.CharField(max_length=50)),
                ('fk_page_url', models.ForeignKey(db_column='fk_page_url', on_delete=django.db.models.deletion.CASCADE, to='scrapy_app.Page_Url_List')),
            ],
            options={
                'db_table': 'url_list',
            },
        ),
        migrations.AddField(
            model_name='page_url_list',
            name='fk_start_url',
            field=models.ForeignKey(db_column='fk_start_url', on_delete=django.db.models.deletion.CASCADE, to='scrapy_app.Start_Url_List'),
        ),
    ]
