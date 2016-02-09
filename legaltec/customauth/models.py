# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import User

from area.models import Area

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, verbose_name="Área", null=True, blank=True)
    class Meta:
        verbose_name = "Custom information"

class SystemEvent(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    eventDate = models.DateTimeField(auto_now_add=True)
    entity = models.CharField("Entidade", max_length=50)
    operation = models.CharField("Operação", max_length=50)
    snapshot = models.CharField("Resumo dos dados", max_length=1000)
    error = models.BooleanField("Erro", default=False)



