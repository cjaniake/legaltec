from django.forms import ModelForm

from doc.models import DocumentStatus, DocumentType, DocumentTypeField


class DocumentStatusForm(ModelForm):
    class Meta:
        model = DocumentStatus
        fields = ['name','minimumValidity','enabled','colorCode']

class DocumentTypeForm(ModelForm):
    class Meta:
        model = DocumentType
        fields = ['name','validityPeriod','description','group','city','state']

class DocumentTypeFieldForm(ModelForm):
    class Meta:
        model = DocumentTypeField
        fields = ['name','fieldType','help','fieldChoices']
