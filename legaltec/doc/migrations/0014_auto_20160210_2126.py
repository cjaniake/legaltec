# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0013_remove_documentstatus_minimumvalidity'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentstatus',
            name='minimumTime',
            field=models.IntegerField(default=0, verbose_name=b'Validade'),
        ),
        migrations.AddField(
            model_name='documentstatus',
            name='minimumTimeUnit',
            field=models.IntegerField(default=1, verbose_name=b'Unidade de Tempo', choices=[(1, b'Dia'), (2, b'M\xc3\xaas'), (3, b'Ano')]),
        ),
    ]
