from django.forms import ModelForm

from doc.models import DocumentStatus


class DocumentStatusForm(ModelForm):
    class Meta:
        model = DocumentStatus
        fields = ['name','minimumValidity','enabled','colorCode']
