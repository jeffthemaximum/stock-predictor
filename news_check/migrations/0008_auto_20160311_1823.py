# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-11 18:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_check', '0007_auto_20160311_1631'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vibe',
            old_name='stock',
            new_name='company',
        ),
    ]
