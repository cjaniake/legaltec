# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0007_auto_20160209_0027'),
    ]

    operations = [
        migrations.AddField(
            model_name='documenttypefield',
            name='help',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Ajuda', blank=True),
        ),
        migrations.AlterField(
            model_name='documenttypefield',
            name='fieldChoices',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Op\xc3\xa7\xc3\xb5es', blank=True),
        ),
    ]
