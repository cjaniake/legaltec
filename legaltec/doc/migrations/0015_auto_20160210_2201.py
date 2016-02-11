# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0014_auto_20160210_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documenttype',
            name='description',
            field=models.CharField(max_length=300, null=True, verbose_name=b'Descri\xc3\xa7\xc3\xa3o', blank=True),
        ),
    ]
