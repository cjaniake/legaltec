# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0009_auto_20160209_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documenttypefield',
            name='fieldChoices',
            field=models.TextField(null=True, verbose_name=b'Op\xc3\xa7\xc3\xb5es', blank=True),
        ),
    ]
