# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0021_auto_20160228_1823'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stringvalue', models.CharField(max_length=100)),
                ('document', models.ForeignKey(verbose_name=b'Documento', to='doc.Document')),
                ('documentTypeField', models.ForeignKey(verbose_name=b'Campo de tipo de documento', to='doc.DocumentTypeField')),
            ],
        ),
    ]
