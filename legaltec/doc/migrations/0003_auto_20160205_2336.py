# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0002_documentstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentstatus',
            name='colorCode',
            field=models.CharField(default=b'#FFFFFF', max_length=7, verbose_name=b'Color'),
        ),
    ]
