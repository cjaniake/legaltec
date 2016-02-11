from django.forms import ModelForm

from area.models import Area, Establishment

class AreaForm(ModelForm):
    class Meta:
        model = Area
        fields = ['name','enabled','adminEmail','validUntil','applyPermissions']

class EstablishmentForm(ModelForm):
    class Meta:
        model = Establishment
        fields = ['name','city','state','adminEmail']
