# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from area.models import Area, Establishment

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, verbose_name="Área", null=True, blank=True)
    class Meta:
        verbose_name = "Custom information"

class SystemEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    eventDate = models.DateTimeField(auto_now_add=True)
    entity = models.CharField("Entidade", max_length=50)
    operation = models.CharField("Operação", max_length=50)
    snapshot = models.CharField("Resumo dos dados", max_length=1000)
    error = models.BooleanField("Erro", default=False)

MESSAGE_ORIGINS = (
    (1, 'User'),
    (2, 'Company'),
    (3, 'System'),
)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    eventDate = models.DateTimeField(auto_now=True)
    readDate = models.DateTimeField(null=True, blank=True)
    subject = models.CharField("Assunto", max_length=100)
    text = models.TextField("Texto da mensagem", max_length=1000)
    establishment = models.ForeignKey(Establishment, verbose_name="Estabelecimento", null=True, blank=True)
    origin = models.IntegerField("Origem", choices=MESSAGE_ORIGINS, default=3)

import customauth.receiver



