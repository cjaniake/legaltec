# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0003_areastatus_colorcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areastatus',
            name='colorCode',
            field=models.CharField(default=b'#FFFFFF', max_length=7, verbose_name=b'Color'),
        ),
    ]
