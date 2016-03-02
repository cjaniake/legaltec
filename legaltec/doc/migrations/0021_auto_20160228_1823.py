# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0020_auto_20160222_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='documentStatus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Status do documento', to='doc.DocumentStatus'),
        ),
        migrations.AlterField(
            model_name='document',
            name='documentType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Tipo de documento', to='doc.DocumentType'),
        ),
        migrations.AlterField(
            model_name='document',
            name='establishment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Estabelecimento', to='area.Establishment'),
        ),
    ]
