# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0018_auto_20160210_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentstatus',
            name='glyphicon',
            field=models.CharField(default=b'glyphicon-star', max_length=30, null=True, verbose_name=b'Glyphicon', blank=True),
        ),
    ]
