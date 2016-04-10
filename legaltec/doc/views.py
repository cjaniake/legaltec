# -*- coding: utf-8 -*-
from datetime import datetime, date
from time import timezone

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ValidationError
from django.core.serializers import json
from django.core.signals import request_finished
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from area.models import Establishment, Area
from customauth.models import CustomUser
from doc.models import DocumentStatus, DocumentType, DocumentTypeField, Document, DocumentHistory, DocumentFile, DocumentImageFile, TIME_UNIT_CHOICES, \
    DocumentField
from doc.forms import DocumentStatusForm, DocumentTypeForm, DocumentTypeFieldForm, DocumentImageFileUploadForm, DocumentFileUploadForm, \
    DocumentAddForm, DocumentModifForm, EmailForm
from legaltec.utils import to_JSON
import json
from django.core.mail import EmailMessage

class DocumentStatusWrapper:
    def __init__(self, documentstatus):
        self.documentstatus = documentstatus
        self.timeunitdict = dict(TIME_UNIT_CHOICES)
    def name(self, **kwargs):
        return self.documentstatus.name
    def id(self, **kwargs):
        return self.documentstatus.id
    def content(self):
        return '{} {}'.format(self.documentstatus.minimumTime, self.timeunitdict[self.documentstatus.minimumTimeUnit])
    link = '/documentstatus/'
    glyphicon = 'glyphicon-list-alt'

class ListDocumentStatusView(TemplateView):
    template_name = "list_template.html"
    def get_context_data(self, **kwargs):
        context = super(ListDocumentStatusView, self).get_context_data(**kwargs)
        #context['object_list'] = list(DocumentStatus.objects.all())
        context['object_list'] = map(lambda s: DocumentStatusWrapper(s), DocumentStatus.objects.all())
        new = DocumentStatus()
        new.name = "<novo>"
        context['object_list'].append(DocumentStatusWrapper(new))
        return context

@login_required
def handle_documentstatus(request):
    if request.method == 'POST':

        form = DocumentStatusForm(request.POST)

        if not request.user.is_superuser and not request.user.has_perm('doc.add_documentstatus'):
            form.add_error(None, ValidationError('User has no permission'))

        if form.is_valid():
            a = DocumentStatus()
            a.name = form.cleaned_data['name']
            a.enabled = form.cleaned_data['enabled']
            a.minimumTime = form.cleaned_data['minimumTime']
            a.minimumTimeUnit = form.cleaned_data['minimumTimeUnit']
            a.colorCode = form.cleaned_data['colorCode']
            a.glyphicon = form.cleaned_data['glyphicon']
            a.save()

            return HttpResponseRedirect('/documentstatuss/')

    else:
        form = DocumentStatusForm()
    return render(request, 'detail_template.html', {'form': form, 'action':'/documentstatus/', 'http_method':'POST'})

# GET/POST /area/<docstatuscode>
@login_required
def edit_documentstatus(request, docstatuscode=None):
    if docstatuscode:
        a = DocumentStatus.objects.get(id=int(docstatuscode))

        if request.method == 'POST':
            #update record with submitted values

            form = DocumentStatusForm(request.POST, instance=a)

            if not request.user.is_superuser and not request.user.has_perm('doc.change_documentstatus'):
                 form.add_error(None, ValidationError('User has no permission'))

            if form.is_valid():
                a.name = form.cleaned_data['name']
                a.enabled = form.cleaned_data['enabled']
                a.minimumTime = form.cleaned_data['minimumTime']
                a.minimumTimeUnit = form.cleaned_data['minimumTimeUnit']
                a.colorCode = form.cleaned_data['colorCode']
                a.glyphicon = form.cleaned_data['glyphicon']
                a.save()

                return HttpResponseRedirect('/documentstatuss/')

            return render(request, 'detail_template.html', {'form': form, 'action':'/documentstatus/' + docstatuscode + '/', 'http_method':'POST'})
        else:
            #load record to allow edition

            form = DocumentStatusForm(instance=a)
            return render(request, 'detail_template.html', {'form': form, 'action':'/documentstatus/' + docstatuscode + '/', 'http_method':'POST'})
    else:
        return HttpResponseRedirect('/documentstatus/')

class DocumentTypeWrapper:
    def __init__(self, documenttype):
        self.documenttype = documenttype
    def name(self, **kwargs):
        return self.documenttype.name
    def id(self, **kwargs):
        return self.documenttype.id
    def content(self):
        return self.documenttype.description
    link = '/documenttype/'
    glyphicon = 'glyphicon-book'

class ListDocumentTypeView(TemplateView):
    template_name = "doc/doctype_list_template.html"
    def get_context_data(self, **kwargs):
        context = super(ListDocumentTypeView, self).get_context_data(**kwargs)
        context['object_list'] = map(lambda s: DocumentTypeWrapper(s), DocumentType.objects.all())
        new = DocumentType()
        new.name = "<novo>"
        context['object_list'].append(DocumentTypeWrapper(new))
        return context

@login_required
def handle_documenttype(request):
    if request.method == 'POST':

        form = DocumentTypeForm(request.POST)

        if not request.user.is_superuser and not request.user.has_perm('doc.add_documenttype'):
            form.add_error(None, ValidationError('User has no permission'))

        if form.is_valid():
            a = DocumentType()
            a.name = form.cleaned_data['name']
            a.validityPeriod = form.cleaned_data['validityPeriod']
            a.description = form.cleaned_data['description']
            a.group = form.cleaned_data['group']
            a.city = form.cleaned_data['city']
            a.state = form.cleaned_data['state']

            a.save()

            return HttpResponseRedirect('/documenttypes/')

    else:
        form = DocumentTypeForm()
    return render(request, 'detail_template.html', {'form': form, 'action':'/documenttype/', 'http_method':'POST'})

# GET/POST /area/<doctypecode>
@login_required
def edit_documenttype(request, doctypecode=None):
    if doctypecode:
        a = DocumentType.objects.get(id=int(doctypecode))

        if request.method == 'POST':
            #update record with submitted values

            form = DocumentTypeForm(request.POST, instance=a)

            if not request.user.is_superuser and not request.user.has_perm('doc.change_documenttype'):
                form.add_error(None, ValidationError('User has no permission'))

            if form.is_valid():
                a.name = form.cleaned_data['name']
                a.validityPeriod = form.cleaned_data['validityPeriod']
                a.description = form.cleaned_data['description']
                a.group = form.cleaned_data['group']
                a.city = form.cleaned_data['city']
                a.state = form.cleaned_data['state']

                a.save()

                return HttpResponseRedirect('/documenttypes/')

            return render(request, 'detail_template.html', {'form': form, 'action':'/documenttype/' + doctypecode + '/', 'http_method':'POST'})
        else:
            #load record to allow edition

            form = DocumentTypeForm(instance=a)
            return render(request, 'detail_template.html', {'form': form, 'action':'/documenttype/' + doctypecode + '/', 'http_method':'POST'})
    else:
        return HttpResponseRedirect('/documenttype/')

class DocumentTypeFieldWrapper:
    def __init__(self, documenttypefield, doctype):
        self.documenttypefield = documenttypefield
        self.doctype = doctype
    def name(self, **kwargs):
        return self.documenttypefield.name
    def id(self, **kwargs):
        return self.documenttypefield.id
    content = 'content about document type field'
    def link(self, **kwargs):
        return '/documenttype/' + str(self.doctype.id) + '/field/'

class ListDocumentTypeFieldView(TemplateView):
    template_name = "list_template.html"
    def get_context_data(self, **kwargs):
        context = super(ListDocumentTypeFieldView, self).get_context_data(**kwargs)
        doctypecode = kwargs['doctypecode']
        doctype = DocumentType.objects.get(id=int(doctypecode))
        context['doctype'] = doctype
        fieldArray = doctype.documenttypefield_set.all()
        context['object_list'] = map(lambda s: DocumentTypeFieldWrapper(s, doctype), fieldArray)
        new = DocumentTypeField()
        new.name = "<novo>"
        context['object_list'].append(DocumentTypeFieldWrapper(new, doctype))
        return context

@login_required
def handle_documenttypefield(request, doctypecode=None):
    doctype = DocumentType.objects.get(id=int(doctypecode))
    if request.method == 'POST':

        form = DocumentTypeFieldForm(request.POST)

        if form.is_valid():
            a = DocumentTypeField()
            a.name = form.cleaned_data['name']
            a.fieldType = form.cleaned_data['fieldType']
            a.fieldChoices = form.cleaned_data['fieldChoices']
            a.documentType_id = int(doctypecode)

            a.save()
            doctype.documenttypefield_set.add(a)

            return HttpResponseRedirect('/documenttype/' + str(doctype.id) + '/fields/')

    else:
        form = DocumentTypeFieldForm()
    return render(request, 'detail_template.html', {'form': form, 'action':'/documenttype/' + str(doctype.id) + '/field/', 'http_method':'POST'})

# GET/POST /area/<doctypefieldcode>
@login_required
def edit_documenttypefield(request, doctypecode=None, doctypefieldcode=None):
    doctype = DocumentType.objects.get(id=int(doctypecode))
    if doctypecode and doctypefieldcode:
        a = DocumentTypeField.objects.get(id=int(doctypefieldcode))

        if request.method == 'POST':
            #update record with submitted values

            form = DocumentTypeFieldForm(request.POST, instance=a)

            if form.is_valid():
                a.name = form.cleaned_data['name']
                a.fieldType = form.cleaned_data['fieldType']
                a.fieldChoices = form.cleaned_data['fieldChoices']
                a.documenttype = doctype

                a.save()
                doctype.documenttypefield_set.add(a)

                return HttpResponseRedirect('/documenttype/' + str(doctype.id) + '/fields/')

            return render(request, 'detail_template.html', {'form': form, 'action':'/documenttype/' + str(doctype.id) + '/field/' + doctypefieldcode + '/', 'http_method':'POST'})
        else:
            #load record to allow edition

            form = DocumentTypeFieldForm(instance=a)
            return render(request, 'detail_template.html', {'form': form, 'action':'/documenttypefield/' + doctypefieldcode + '/', 'http_method':'POST'})
    else:
        return HttpResponseRedirect('/documenttypefield/')

class DocumentWrapper:
    def __init__(self, document):
        self.document = document
    def name(self, **kwargs):
        return self.document.name
    def id(self, **kwargs):
        return self.document.id
    content = 'content about document'
    link = '/document/'

class ListDocumentView(TemplateView):
    template_name = "doc/doctable_template.html"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/admin/login/')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        c = CustomUser.objects.filter(user__id=request.user.id)
        if not c or not c[0].area:
            areacode = request.session.get('areacode')
            if not areacode:
                return HttpResponseRedirect('/areas')
        return super(ListDocumentView, self).dispatch(request, *args, **kwargs)
    def documentAsList(self, document):
        return [document.establishment.name, document.documentType.name, document.documentStatus.name, document.expirationDate]
    def get_context_data(self, **kwargs):
        context = super(ListDocumentView, self).get_context_data(**kwargs)
        qset = Document.objects

        selectionList = self.request.session.get('selection_list') # keep serialized version
        selected = {}                                              # keep object version
        if not selectionList:
            selectionList = {}

        c = CustomUser.objects.filter(user__id=self.request.user.id)
        if c and c[0].area:
            area = c[0].area
        else:
            areacode = self.request.session.get('areacode')
            if areacode:
                area = Area.objects.get(id=int(areacode))

        e = None
        if c and c[0].establishment:
            e = c[0].establishment
            self.request.session['establishment'] = e.name
        else:
            establishmentId = self.request.GET.get('establishmentId')
            if establishmentId:
                if establishmentId=='None':
                    if 'establishment' in selectionList:
                        del selectionList['establishment']
                else:
                    e = Establishment.objects.get(id=establishmentId)
                    selectionList['establishment'] = to_JSON(e)
                    qset = qset.filter(establishment=e)
                    self.request.session['areacode'] = e.area.id
                    area = e.area
                    selected['establishment'] = e
            else:
                if 'establishment' in selectionList:
                    for obj in serializers.deserialize("json", selectionList['establishment']):
                        e = obj.object
                        selected['establishment'] = e

        if e:
            qset = qset.filter(establishment=e)
        else:
            inner_qs = Establishment.objects.filter(area__id__exact=area.id)
            qset = qset.filter(establishment__in=inner_qs)

        t = None
        documentTypeId = self.request.GET.get('documentTypeId')
        if documentTypeId:
            if documentTypeId=='None':
                if 'documentType' in selectionList:
                    del selectionList['documentType']
            else:
                t = DocumentType.objects.get(id=documentTypeId)
                selectionList['documentType'] = to_JSON(t)
        else:
            if 'documentType' in selectionList:
                for obj in serializers.deserialize("json", selectionList['documentType']):
                    t = obj.object
        if t:
            selected['documentType'] = t
            qset = qset.filter(documentType=t)

        activeStatusList = selectionList['activeStatusList'] \
            if 'activeStatusList' in selectionList \
            else list(DocumentStatus.objects.filter(enabled=True).values_list('id', flat=True))
        toggleStatusId = self.request.GET.get('toggleDocumentStatusId')
        if toggleStatusId:
            if int(toggleStatusId) in activeStatusList:
                activeStatusList.remove(int(toggleStatusId))
            else:
                activeStatusList.append(int(toggleStatusId))
            selectionList['activeStatusList'] = activeStatusList

        qset = qset.filter(documentStatus_id__in=activeStatusList)

        self.request.session['selection_list'] = selectionList
        context['area'] = area
        context['selected'] = selected
        context['tableheader_list'] = ['Estabelecimento','Tipo de Documento','Data de Expiração']
        context['object_list'] = map(lambda s: s, qset.all())
        context['area_choices'] = map(lambda s: s.name, Area.objects.all())
        context['establishment_choices'] = map(lambda s: { 'name' : s.name, 'id' : s.id }, area.establishment_set.all()) if area else []
        context['document_type_choices'] = map(lambda s: { 'name' : s.name, 'id' : s.id }, DocumentType.objects.all())
        context['document_status_choices'] = map(lambda s: { 'name' : s.name, 'id' : s.id }, DocumentStatus.objects.all())
        context['activeStatusList'] = activeStatusList
        return context

# GET/POST /document/
@login_required
def handle_document(request):
    area = None
    areacode = request.session.get('areacode')
    if areacode:
        area = Area.objects.get(id=int(areacode))


    if request.method == 'POST':

        form = DocumentAddForm(request.POST)

        if form.is_valid():
            a = Document()
            a.establishment = form.cleaned_data['establishment']
            a.documentType = form.cleaned_data['documentType']
            a.expeditionDate = form.cleaned_data['expeditionDate']
            a.expirationDate = form.cleaned_data['expirationDate']
            if form.cleaned_data['enabled']:
                a.documentStatus = statusForExpirationDate(form.cleaned_data['expirationDate'])
            else:
                a.documentStatus = DocumentStatus.objects.filter(enabled=False)[0]
            a.save()

            h = DocumentHistory()
            h.user = request.user
            h.operation = "CREATION"
            h.snapshot = to_JSON(a)
            h.document = a

            h.save()
            a.documenthistory_set.add(h)

            extraFieldsCount = DocumentTypeField.objects.filter(documentType=a.documentType).count()
            if extraFieldsCount > 0:
                return HttpResponseRedirect('/document/' + str(a.id) + '/')
            else:
                return HttpResponseRedirect('/documents/')

    else:
        selectionList = request.session.get('selection_list')
        e = None
        if 'establishment' in selectionList:
            for obj in serializers.deserialize("json", selectionList['establishment']):
                e = obj.object
        t = None
        if 'documentType' in selectionList:
            for obj in serializers.deserialize("json", selectionList['documentType']):
                t = obj.object
        st = None
        form = DocumentAddForm(initial={'establishment': e,'documentType': t })
        form.fields['enabled'].initial = True

    return render(request, 'detail_template.html', {'form': form, 'action':'/document/', 'http_method':'POST', 'area' : area})

# GET/POST /document/<documentcode>
@login_required
def edit_document(request, documentcode=None):
    if documentcode:
        a = Document.objects.get(id=int(documentcode))

        if request.method == 'POST':
            #update record with submitted values

            form = DocumentModifForm(request.POST, instance=a)
            form.data['establishment'] = str(a.establishment.id)
            form.data['documentType'] = str(a.documentType.id)
            form.full_clean()

            if form.is_valid():
                #a.establishment = form.cleaned_data['establishment']
                #a.documentType = form.cleaned_data['documentType']
                a.expeditionDate = form.cleaned_data['expeditionDate']
                a.expirationDate = form.cleaned_data['expirationDate']
                if form.cleaned_data['enabled']:
                    a.documentStatus = statusForExpirationDate(form.cleaned_data['expirationDate'])
                else:
                    a.documentStatus = DocumentStatus.objects.filter(enabled=False)[0]

                a.save()

                extraKeys = [x for x in form.data if x.startswith('extra_')]
                for extraKey in extraKeys:
                    docTpFieldId = int(extraKey[6:])
                    docTpField = DocumentTypeField.objects.get(id=docTpFieldId)

                    docField = DocumentField()
                    docField.document = a
                    docField.documentTypeField = docTpField
                    docField.stringvalue = form.data[extraKey]

                    docField.save()
                    a.documentfield_set.add(docField)
                    docTpField.documentfield_set.add(docField)

                h = DocumentHistory()
                h.user = request.user
                h.operation = "MODIFICATION"
                h.snapshot = serializers.serialize("json", [a, ])
                h.document = a

                h.save()
                a.documenthistory_set.add(h)

                return HttpResponseRedirect('/documents/')

            return render(request, 'detail_template.html', {'form': form, 'action':'/document/' + documentcode + '/', 'http_method':'POST'})
        else:
            #load record to allow edition

            extraFields = DocumentTypeField.objects.filter(documentType=a.documentType).all()

            form = DocumentModifForm(instance=a, extraFields=extraFields)
            form.fields['enabled'].initial = a.documentStatus.enabled

            for curValue in a.documentfield_set.all():
                form.fields['extra_' + str(curValue.documentTypeField_id)].initial = curValue.stringvalue

            return render(request, 'detail_template.html', {'form': form, 'action':'/document/' + documentcode + '/', 'http_method':'POST'})
    else:
        return HttpResponseRedirect('/document/')


class ListDocumentFileView(TemplateView):
    template_name = "doc/docfiles_template.html"
    def get_context_data(self, **kwargs):
        context = super(ListDocumentFileView, self).get_context_data(**kwargs)
        documentcode = kwargs['documentcode']
        document = Document.objects.get(id=int(documentcode))
        context['document'] = document
        context['file_list'] = DocumentFile.objects.filter(document__id=document.id).all()
        context['imagefile_list'] = DocumentImageFile.objects.filter(document__id=document.id).all()
        context['file_upload_form'] = DocumentFileUploadForm()
        context['imagefile_upload_form'] = DocumentImageFileUploadForm()
        context['area'] = document.establishment.area
        return context

# GET/POST /document/<documentcode>/file/
@login_required
def handle_documentupload(request, documentcode):
    doc = Document.objects.get(id=int(documentcode));
    form = DocumentFileUploadForm(request.POST, request.FILES)
    if form.is_valid():
        df = DocumentFile()
        df.documentFile = form.cleaned_data['file']
        df.enabled = True
        df.checksum = 'TODO'
        df.size = str(form.cleaned_data['file'].size)
        df.document = doc

        df.save()
        doc.documentfile_set.add(df)

        h = DocumentHistory()
        h.user = request.user
        h.operation = "FILE UPLOAD " + df.documentFile.name
        h.snapshot = to_JSON(doc)
        h.document = doc

        h.save()
        doc.documenthistory_set.add(h)

    return HttpResponseRedirect('/document/' + documentcode + '/files/')


# GET/POST /document/<documentcode>/imagefile/
@login_required
def handle_imageupload(request, documentcode):
    doc = Document.objects.get(id=int(documentcode))
    form = DocumentImageFileUploadForm(request.POST, request.FILES)
    if form.is_valid():
        df = DocumentImageFile()
        df.imageFile = form.cleaned_data['file']
        df.enabled = True
        df.checksum = 'TODO'
        df.size = str(form.cleaned_data['file'].size)
        df.document = doc

        df.save()
        doc.documentimagefile_set.add(df)

        h = DocumentHistory()
        h.user = request.user
        h.operation = "IMAGE UPLOAD " + df.imageFile.name
        h.snapshot = to_JSON(doc)
        h.document = doc

        h.save()
        doc.documenthistory_set.add(h)

    return HttpResponseRedirect('/document/' + documentcode + '/files/')

class ListDocumentHistoryView(TemplateView):
    template_name = "doc/dochistory_template.html"
    def get_context_data(self, **kwargs):
        context = super(ListDocumentHistoryView, self).get_context_data(**kwargs)
        documentcode = kwargs['documentcode']
        document = Document.objects.get(id=int(documentcode))
        context['document'] = document
        context['event_list'] = DocumentHistory.objects.filter(document__id=document.id).all()
        context['area'] = document.establishment.area
        return context

def view_history(request, dochistorycode):
    docHistory = DocumentHistory.objects.get(id=int(dochistorycode))
    snapshot = json.dumps(json.loads(docHistory.snapshot), indent=4)
    return render(request, 'doc/dochistory_detail.html', {'document': docHistory.document, 'docHistory': docHistory, 'snapshot': snapshot})


def update_document_status(request):
    inner_qs = DocumentStatus.objects.filter(enabled=True)
    qset = Document.objects.filter(documentStatus__in=inner_qs)
    map(verifyStatusChange, qset.all())
    return HttpResponseRedirect('/documents/')

def verifyStatusChange(doc):
    status = statusForExpirationDate(doc.expirationDate)
    if status == doc.documentStatus:
        print("document {} ok".format(doc.id))
    else:
        print("document {} changed".format(doc.id))
        doc.documentStatus = status
        doc.save()

        h = DocumentHistory()
        h.operation = "STATUS CHANGED"
        h.snapshot = to_JSON(doc)
        h.document = doc

        h.save()
        doc.documenthistory_set.add(h)

def statusForExpirationDate(expirationDate):
    qs = DocumentStatus.objects.filter(enabled=True)
    d = {s.minimumTime * s.minimumTimeUnit: s for s in qs.all()}
    delta = expirationDate - date.today()
    s = None
    for days in sorted(d):
        if days < delta.days or not s:
            s = d[days]
    return s

def emaildocument(request, documentcode):
    doc = Document.objects.get(id=int(documentcode))
    file_list = DocumentFile.objects.filter(document__id=doc.id).all()

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            m = EmailMessage()
            m.subject = form.cleaned_data['subject']
            m.body = form.cleaned_data['body']
            m.to = [form.cleaned_data['to']]
            m.cc = [form.cleaned_data['cc']]
            for file in file_list:
                m.attach_file(file.documentFile.name)
            m.send()
            return HttpResponseRedirect('/documents/')

    else:
        form = EmailForm(initial={'subject': doc.documentType.name, 'body': 'Segue anexo ' + doc.documentType.name + '\n' + doc.establishment.area.name + '\n' + doc.establishment.name})
    return render(request, 'doc/email_template.html', {'document': doc, 'form': form, 'attachments': file_list, 'action': '/document/' + documentcode + '/email/'})

def emaildocumentfile(request, documentcode, filecode):
    doc = Document.objects.get(id=int(documentcode))
    file = DocumentFile.objects.get(id=int(filecode))

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            m = EmailMessage()
            m.subject = form.cleaned_data['subject']
            m.body = form.cleaned_data['body']
            m.to = [form.cleaned_data['to']]
            m.cc = [form.cleaned_data['cc']]
            m.attach_file(file.documentFile.name)
            m.send()
            return HttpResponseRedirect('/document/' + documentcode + '/files/')

    else:
        form = EmailForm(initial={'subject': doc.documentType.name, 'body': 'Segue anexo ' + doc.documentType.name + '\n' + doc.establishment.area.name + '\n' + doc.establishment.name})
    return render(request, 'doc/email_template.html', {'document': doc, 'form': form, 'attachments': [file], 'action': '/document/' + documentcode + '/file/' + filecode + '/email/'})

def printdocumentfile(request, documentcode, filecode):
    file = DocumentFile.objects.get(id=int(filecode))
    return render(request, 'print_image_template.html', {'imagefiles': [file.documentFile.url]})

def printdocumentfiles(request, documentcode):
    doc = Document.objects.get(id=int(documentcode))
    ducument_file_list = DocumentFile.objects.filter(document__id=doc.id).all()
    image_files = map(lambda f: f.documentFile.url, ducument_file_list)
    return render(request, 'print_image_template.html', {'imagefiles': image_files})
