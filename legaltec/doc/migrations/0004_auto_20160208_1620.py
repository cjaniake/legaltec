# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0003_auto_20160205_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='documenttype',
            name='City',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Cidade', blank=True),
        ),
        migrations.AddField(
            model_name='documenttype',
            name='Description',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Descri\xc3\xa7\xc3\xa3o', blank=True),
        ),
        migrations.AddField(
            model_name='documenttype',
            name='Group',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Grupo', blank=True),
        ),
        migrations.AddField(
            model_name='documenttype',
            name='State',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Estado', blank=True),
        ),
    ]
