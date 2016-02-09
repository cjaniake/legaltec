# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0010_auto_20160209_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='modifiedDate',
            field=models.DateField(auto_now=True, verbose_name=b'Alterado'),
        ),
    ]
