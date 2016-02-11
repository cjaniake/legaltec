# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0006_auto_20160210_2118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='areaStatus',
        ),
        migrations.AddField(
            model_name='area',
            name='applyPermissions',
            field=models.BooleanField(default=False, verbose_name=b'Exigir permiss\xc3\xb5es espec\xc3\xadficas'),
        ),
        migrations.AddField(
            model_name='area',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name=b'Ativo'),
        ),
        migrations.AddField(
            model_name='area',
            name='validUntil',
            field=models.IntegerField(null=True, verbose_name=b'Validade licen\xc3\xa7a', blank=True),
        ),
        migrations.DeleteModel(
            name='AreaStatus',
        ),
    ]
