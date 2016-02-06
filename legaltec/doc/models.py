# -*- coding: utf-8 -*-
from django.db import models

class DocumentType(models.Model):
    name = models.CharField("Tipo de documento", max_length=50, unique=True)
    validityPeriod = models.IntegerField("Validade em meses")
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
