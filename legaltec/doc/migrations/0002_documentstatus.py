# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name=b'Status')),
                ('enabled', models.BooleanField(verbose_name=b'Ativo')),
                ('minimumValidity', models.IntegerField(null=True, verbose_name=b'Validade m\xc3\xadnima', blank=True)),
                ('colorCode', models.CharField(default=b'#FFFFFF', max_length=8, verbose_name=b'Color')),
            ],
        ),
    ]
