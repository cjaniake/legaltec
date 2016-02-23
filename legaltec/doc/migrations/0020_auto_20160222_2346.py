# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0019_documentstatus_glyphicon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentstatus',
            name='minimumTimeUnit',
            field=models.IntegerField(default=1, verbose_name=b'Unidade de Tempo', choices=[(1, b'Dia(s)'), (30, b'M\xc3\xaas(s)'), (365, b'Ano(s)')]),
        ),
    ]
