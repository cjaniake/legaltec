# -*- coding: utf-8 -*-
from django.db import models

class Area(models.Model):
    name = models.CharField("Área", max_length=50, unique=True)
    enabled = models.BooleanField("Ativo", default=True)
    adminEmail = models.EmailField("Email administrador")
    validUntil = models.DateField("Validade licença", null=True, blank=True)
    applyPermissions = models.BooleanField("Exigir permissões específicas", default=False)
    def __unicode__(self):
        return u'%s' % (self.name)

class Establishment(models.Model):
    area = models.ForeignKey(Area, verbose_name="Área", on_delete=models.PROTECT)
    name = models.CharField("Estabelecimento", max_length=100, unique=True)
    city = models.CharField("Cidade", max_length=100)
    state = models.CharField("Estado", max_length=2)
    adminEmail = models.EmailField("Email administrador")
    class Meta:
        unique_together = ("area", "name")
    def __unicode__(self):
        return u'%s' % (self.name)
