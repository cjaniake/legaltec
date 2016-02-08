# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import User

from area.models import Area

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, verbose_name="Área", null=True, blank=True)
    class Meta:
        verbose_name = "Custom information"
