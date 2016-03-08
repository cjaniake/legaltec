from django import forms
from django.forms import ModelForm, Form, FileField, Field, TextInput, BooleanField, Select
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

class DocumentAddForm(ModelForm):
    enabled = BooleanField(required=False, label="Ativo")
    class Meta:
        model = Document
        fields = ['establishment','documentType','expeditionDate','expirationDate']

class DocumentModifForm(ModelForm):
    enabled = BooleanField(required=False, label="Ativo")
    class Meta:
        model = Document
        fields = ['establishment','documentType','expeditionDate','expirationDate']
        widgets = {
            'establishment': Select(attrs={'disabled': True}),
            'documentType': Select(attrs={'disabled': True}),
        }
    def __init__(self, *args, **kwargs):
            extraFields = kwargs.pop('extraFields', None)
            super(DocumentModifForm, self).__init__(*args, **kwargs)

            #(1, 'Texto'),
            #(2, 'Inteiro'),
            #(3, 'Decimal'),
            #(4, 'Lista'),

            if(extraFields):
                for documentTypeField in extraFields:
                    if(documentTypeField.fieldType == 1):
                        self.fields['extra_%s' % documentTypeField.id] = forms.CharField(label=documentTypeField.name)
                    if(documentTypeField.fieldType == 2):
                        self.fields['extra_%s' % documentTypeField.id] = forms.IntegerField(label=documentTypeField.name)
                    if(documentTypeField.fieldType == 3):
                        self.fields['extra_%s' % documentTypeField.id] = forms.DecimalField(label=documentTypeField.name, localize=True)
                    if(documentTypeField.fieldType == 4):
                        self.fields['extra_%s' % documentTypeField.id] = forms.ChoiceField(label=documentTypeField.name,
                            choices=[x for x in enumerate(documentTypeField.fieldChoices.split(','), 1)])

class DocumentFileUploadForm(Form):
    file = FileField(label='Arquivo')

class DocumentImageFileUploadForm(Form):
    file = FileField(label='Arquivo')
