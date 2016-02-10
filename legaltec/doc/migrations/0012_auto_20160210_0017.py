# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0011_auto_20160209_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentfile',
            name='size',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documentimagefile',
            name='size',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
