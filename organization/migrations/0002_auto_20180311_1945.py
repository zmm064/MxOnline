# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-11 11:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courseorg',
            options={'verbose_name': '课程机构', 'verbose_name_plural': '课程机构'},
        ),
    ]
