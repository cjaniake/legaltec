from django.core import serializers
from django.core.serializers import json


def to_JSON(modelObject):
    return serializers.serialize("json", [modelObject, ])
