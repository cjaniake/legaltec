# -*- coding: utf-8 -*-
from django.db import models

from area.models import Establishment

from django.contrib.auth.models import User

FIELD_TYPE_CHOICES = (
    (1, 'Texto'),
    (2, 'Inteiro'),
    (3, 'Decimal'),
    (4, 'Lista'),
)

TIME_UNIT_CHOICES = (
    (1, 'Dia(s)'),
    (30, 'Mês(s)'),
    (365, 'Ano(s)'),
)

class DocumentType(models.Model):
    name = models.CharField("Tipo de documento", max_length=50, unique=True)
    validityPeriod = models.IntegerField("Validade em meses")
    description = models.CharField("Descrição", max_length=300, null=True, blank=True)
    group = models.CharField("Grupo", max_length=50, null=True, blank=True)
    city = models.CharField("Cidade", max_length=50, null=True, blank=True)
    state = models.CharField("Estado", max_length=50, null=True, blank=True)
    def __unicode__(self):
        return u'%s' % (self.name)

class DocumentTypeField(models.Model):
    documentType = models.ForeignKey(DocumentType, verbose_name="Tipo de documento")
    name = models.CharField("Campo", max_length=50)
    fieldType = models.IntegerField("Tipo do campo",
                                      choices=FIELD_TYPE_CHOICES,
                                      default=1)
    help = models.TextField("Ajuda", null=True, blank=True)
    fieldChoices = models.TextField("Opções", null=True, blank=True)
    class Meta:
        unique_together = ("documentType", "name")

class DocumentStatus(models.Model):
    name = models.CharField("Status", max_length=50, unique=True)
    enabled = models.BooleanField("Ativo")
    colorCode = models.CharField("Color", max_length=7, default="#FFFFFF")
    minimumTime = models.IntegerField("Validade", default=0)
    minimumTimeUnit = models.IntegerField("Unidade de Tempo",
                                      choices=TIME_UNIT_CHOICES,
                                      default=1)
    glyphicon = models.CharField("Glyphicon", max_length=30, null=True, blank=True, default="glyphicon-star")
    def __unicode__(self):
        return u'%s' % (self.name)

class Document(models.Model):
    establishment = models.ForeignKey(Establishment, verbose_name="Estabelecimento", on_delete=models.PROTECT)
    documentType = models.ForeignKey(DocumentType, verbose_name="Tipo de documento", on_delete=models.PROTECT)
    documentStatus = models.ForeignKey(DocumentStatus, verbose_name="Status do documento", on_delete=models.PROTECT)
    expeditionDate = models.DateField("Data de Emissão")
    expirationDate = models.DateField("Data de Expiração")
    createdDate = models.DateField("Criado", auto_now_add=True)
    modifiedDate = models.DateField("Alterado", auto_now=True)
    def __unicode__(self):
        return u'%s %s-%s' % (self.documentType.name, self.expeditionDate, self.expirationDate)

class DocumentHistory(models.Model):
    document = models.ForeignKey(Document, verbose_name="Documento", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    eventDate = models.DateTimeField(auto_now=True)
    operation = models.CharField("Operação", max_length=50)
    snapshot = models.CharField("Resumo dos dados", max_length=1000)

class DocumentImageFile(models.Model):
    document = models.ForeignKey(Document, verbose_name="Documento", on_delete=models.CASCADE)
    imageFile = models.FileField(upload_to='uploads/%Y/%m/%d/')
    enabled = models.BooleanField
    uploadDate = models.DateTimeField(auto_now_add=True)
    checksum = models.CharField(max_length=20)
    size = models.CharField(max_length=20)

class DocumentFile(models.Model):
    document = models.ForeignKey(Document, verbose_name="Documento", on_delete=models.CASCADE)
    documentFile = models.FileField(upload_to='uploads/%Y/%m/%d/')
    enabled = models.BooleanField
    uploadDate = models.DateTimeField(auto_now_add=True)
    checksum = models.CharField(max_length=20)
    size = models.CharField(max_length=20)

class DocumentField(models.Model):
    documentTypeField = models.ForeignKey(DocumentTypeField, verbose_name="Campo de tipo de documento", on_delete=models.CASCADE)
    document = models.ForeignKey(Document, verbose_name="Documento", on_delete=models.CASCADE)
    stringvalue = models.CharField(max_length=100)
