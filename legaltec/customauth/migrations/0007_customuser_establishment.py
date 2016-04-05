# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0009_auto_20160228_1823'),
        ('customauth', '0006_auto_20160319_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='establishment',
            field=models.ForeignKey(verbose_name=b'Estabelecimento', blank=True, to='area.Establishment', null=True),
        ),
    ]
