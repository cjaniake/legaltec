from django.forms import ModelForm, Form, FileField, Field, ImageField, TextInput, BooleanField
from doc.models import DocumentStatus, DocumentType, DocumentTypeField, Document


class DocumentStatusForm(ModelForm):
    class Meta:
        model = DocumentStatus
        fields = ['name','minimumTime','minimumTimeUnit','enabled','colorCode','glyphicon']

class DocumentTypeForm(ModelForm):
    class Meta:
        model = DocumentType
        fields = ['name','validityPeriod','description','group','city','state']
        widgets = {
            'name': TextInput(attrs={'size': 50}),
            'description': TextInput(attrs={'size': 50}),
        }

class DocumentTypeFieldForm(ModelForm):
    class Meta:
        model = DocumentTypeField
        fields = ['name','fieldType','help','fieldChoices']

class DocumentForm(ModelForm):
    enabled = BooleanField(required=False, label="Ativo")
    class Meta:
        model = Document
        fields = ['establishment','documentType','expeditionDate','expirationDate']

class DocumentFileUploadForm(Form):
    file = FileField(label='Arquivo')

class DocumentImageFileUploadForm(Form):
    file = ImageField(label='Arquivo')
