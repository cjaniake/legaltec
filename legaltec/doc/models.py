# -*- coding: utf-8 -*-
from django.db import models

from area.models import Establishment

from django.contrib.auth.models import User

class DocumentType(models.Model):
    name = models.CharField("Tipo de documento", max_length=50, unique=True)
    validityPeriod = models.IntegerField("Validade em meses")
    description = models.CharField("Descrição", max_length=50, null=True, blank=True)
    group = models.CharField("Grupo", max_length=50, null=True, blank=True)
    city = models.CharField("Cidade", max_length=50, null=True, blank=True)
    state = models.CharField("Estado", max_length=50, null=True, blank=True)
    def __unicode__(self):
        return u'%s' % (self.name)

FIELD_TYPE_CHOICES = (
    (1, 'Texto'),
    (2, 'Inteiro'),
    (3, 'Decimal'),
    (4, 'Lista'),
)

class DocumentTypeField(models.Model):
    documentType = models.ForeignKey(DocumentType, verbose_name="Tipo de documento")
    name = models.CharField("Campo", max_length=50, unique=True)
    field_type = models.IntegerField("Tipo do campo",
                                      choices=FIELD_TYPE_CHOICES,
                                      default=1)
    field_choices = models.CharField("Opções", max_length=50)
    class Meta:
        unique_together = ("documentType", "name")

class DocumentStatus(models.Model):
    name = models.CharField("Status", max_length=50, unique=True)
    enabled = models.BooleanField("Ativo")
    minimumValidity = models.IntegerField("Validade mínima", null=True, blank=True)
    colorCode = models.CharField("Color", max_length=7, default="#FFFFFF")
    def __unicode__(self):
        return u'%s' % (self.name)

class Document(models.Model):
    establishment = models.ForeignKey(Establishment, verbose_name="Estabelecimento")
    documentType = models.ForeignKey(DocumentType, verbose_name="Tipo de documento")
    documentStatus = models.ForeignKey(DocumentStatus, verbose_name="Status do documento")
    expeditionDate = models.DateField("Data de Emissão")
    expirationDate = models.DateField("Data de Expiração")
    createdDate = models.Date("Criado", auto_now_add=True)
    modifiedDate = models.Date("Criado", auto_now=True)
    def __unicode__(self):
        return u'%s %s-%s' % (self.documentType.name, self.expeditionDate, self.expirationDate)

class DocumentHistory(models.Model):
    document = models.ForeignKey(Document, verbose_name="Documento")
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    eventDate = models.DateTimeField(auto_now=True)
    operation = models.CharField("Operação", max_length=50)
    snapshot = models.CharField("Resumo dos dados", max_length=1000)

class DocumentImageFile(models.Model):
    document = models.ForeignKey(Document, verbose_name="Documento")
    imageFile = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    enabled = models.BooleanField
    uploadDate = models.DateTimeField(auto_now_add=True)
    checksum = models.CharField(max_length=20)

class DocumentFile(models.Model):
    document = models.ForeignKey(Document, verbose_name="Documento")
    documentFile = models.FileField(upload_to='uploads/%Y/%m/%d/')
    enabled = models.BooleanField
    uploadDate = models.DateTimeField(auto_now_add=True)
    checksum = models.CharField(max_length=20)
