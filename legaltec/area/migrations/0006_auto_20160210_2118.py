# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0005_auto_20160206_0045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='areastatus',
            name='minimumValidity',
        ),
        migrations.AddField(
            model_name='areastatus',
            name='validUntil',
            field=models.IntegerField(null=True, verbose_name=b'Validade licen\xc3\xa7a', blank=True),
        ),
    ]
