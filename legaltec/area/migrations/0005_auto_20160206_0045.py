# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0004_auto_20160205_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establishment',
            name='city',
            field=models.CharField(max_length=100, verbose_name=b'Cidade'),
        ),
    ]
