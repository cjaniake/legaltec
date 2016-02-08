# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0004_auto_20160208_1620'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documenttype',
            old_name='City',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='documenttype',
            old_name='Description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='documenttype',
            old_name='Group',
            new_name='group',
        ),
        migrations.RenameField(
            model_name='documenttype',
            old_name='State',
            new_name='state',
        ),
    ]
