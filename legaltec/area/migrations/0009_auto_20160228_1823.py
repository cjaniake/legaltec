# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0008_auto_20160210_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establishment',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'\xc3\x81rea', to='area.Area'),
        ),
    ]
