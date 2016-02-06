from django.forms import ModelForm

from area.models import Area, Establishment, AreaStatus


class AreaStatusForm(ModelForm):
    class Meta:
        model = AreaStatus
        fields = ['name','minimumValidity','enabled','colorCode']

class AreaForm(ModelForm):
    class Meta:
        model = Area
        fields = ['name','areaStatus','adminEmail']

class EstablishmentForm(ModelForm):
    class Meta:
        model = Establishment
        fields = ['name','city','state','adminEmail']
