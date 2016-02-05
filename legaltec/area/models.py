# -*- coding: utf-8 -*-
from django.db import models

class AreaStatus(models.Model):
    name = models.CharField("Status", max_length=50, unique=True)
    enabled = models.BooleanField("Ativo")
    def __unicode__(self):
        return u'%s' % (self.name)

class Area(models.Model):
    name = models.CharField("Área", max_length=50, unique=True)
    areaStatus = models.ForeignKey(AreaStatus, verbose_name="Status")
    adminEmail = models.EmailField("Email administrador")

class Establishment(models.Model):
    area = models.ForeignKey(Area, verbose_name="Área")
    name = models.CharField("Estabelecimento", max_length=100, unique=True)
    city = models.CharField("Cidade", max_length=100, unique=True)
    state = models.CharField("Estado", max_length=2)
    adminEmail = models.EmailField("Email administrador")
    class Meta:
        unique_together = ("area", "name")
