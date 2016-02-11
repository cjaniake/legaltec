# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0007_auto_20160210_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='validUntil',
            field=models.DateField(null=True, verbose_name=b'Validade licen\xc3\xa7a', blank=True),
        ),
    ]
