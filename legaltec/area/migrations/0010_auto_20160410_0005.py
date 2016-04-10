# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0009_auto_20160228_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='establishment',
            name='cnpj',
            field=models.CharField(max_length=20, null=True, verbose_name=b'CNPJ', blank=True),
        ),
        migrations.AddField(
            model_name='establishment',
            name='iest',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Inscri\xc3\xa7\xc3\xa3o Estadual', blank=True),
        ),
    ]
