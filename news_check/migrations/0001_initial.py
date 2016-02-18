# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('full_name', models.CharField(max_length=255)),
                ('symbol', models.CharField(max_length=10)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]
