# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0002_areastatus_minimumvalidity'),
    ]

    operations = [
        migrations.AddField(
            model_name='areastatus',
            name='colorCode',
            field=models.CharField(default=b'#FFFFFF', max_length=8, verbose_name=b'Color'),
        ),
    ]
