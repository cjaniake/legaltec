# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='areastatus',
            name='minimumValidity',
            field=models.IntegerField(null=True, verbose_name=b'Validade m\xc3\xadnima', blank=True),
        ),
    ]
