# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('area', '0005_auto_20160206_0045'),
        ('doc', '0005_auto_20160208_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('expeditionDate', models.DateField(verbose_name=b'Data de Emiss\xc3\xa3o')),
                ('expirationDate', models.DateField(verbose_name=b'Data de Expira\xc3\xa7\xc3\xa3o')),
                ('documentStatus', models.ForeignKey(verbose_name=b'Status do documento', to='doc.DocumentStatus')),
                ('documentType', models.ForeignKey(verbose_name=b'Tipo de documento', to='doc.DocumentType')),
                ('establishment', models.ForeignKey(verbose_name=b'Estabelecimento', to='area.Establishment')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operation', models.CharField(max_length=50, verbose_name=b'Opera\xc3\xa7\xc3\xa3o')),
                ('snapshot', models.CharField(max_length=1000, verbose_name=b'Resumo dos dados')),
                ('document', models.ForeignKey(verbose_name=b'Documento', to='doc.Document')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imageFile', models.FileField(upload_to=b'uploads/%Y/%m/%d/')),
                ('documentFile', models.FileField(upload_to=b'uploads/%Y/%m/%d/')),
                ('checksum', models.CharField(max_length=20)),
                ('document', models.ForeignKey(verbose_name=b'Documento', to='doc.Document')),
            ],
        ),
    ]
