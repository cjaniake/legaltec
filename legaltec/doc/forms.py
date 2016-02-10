from django.forms import ModelForm, Form, FileField, Field, ImageField
from doc.models import DocumentStatus, DocumentType, DocumentTypeField, Document


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

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['establishment','documentType','documentStatus','expeditionDate','expirationDate']

class DocumentDetailForm(ModelForm):
    class Meta:
        model = Document
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(DocumentDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True


class DocumentFileUploadForm(Form):
    file = FileField(label='Arquivo')

class DocumentImageFileUploadForm(Form):
    file = ImageField(label='Arquivo')
