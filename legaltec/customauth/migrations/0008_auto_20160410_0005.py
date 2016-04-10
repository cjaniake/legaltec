# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customauth', '0007_customuser_establishment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='establishment',
            field=models.ForeignKey(verbose_name=b'Estabelecimen', blank=True, to='area.Establishment', null=True),
        ),
    ]
