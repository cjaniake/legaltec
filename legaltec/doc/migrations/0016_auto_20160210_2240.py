# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0015_auto_20160210_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentstatus',
            name='minimumTimeUnit',
            field=models.IntegerField(default=1, verbose_name=b'Unidade de Tempo', choices=[(1, b'Dia(s)'), (2, b'M\xc3\xaas(s)'), (3, b'Ano(s)')]),
        ),
    ]
