# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.serializers import json
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from area.models import Establishment, Area
from doc.forms import DocumentStatusForm, DocumentTypeForm, DocumentTypeFieldForm, DocumentForm, DocumentDetailForm
from doc.models import DocumentStatus, DocumentType, DocumentTypeField, Document, DocumentHistory
from legaltec.utils import to_JSON


class DocumentStatusWrapper:
    def __init__(self, documentstatus):
        self.documentstatus = documentstatus
    def name(self, **kwargs):
        return self.documentstatus.name
    def id(self, **kwargs):
        return self.documentstatus.id
    content = 'content about document status'
    link = '/documentstatus/'

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

def handle_documentstatus(request):
    if request.method == 'POST':

        form = DocumentStatusForm(request.POST)

        if form.is_valid():
            a = DocumentStatus()
            a.name = form.cleaned_data['name']
            a.enabled = form.cleaned_data['enabled']
            a.minimumValidity = form.cleaned_data['minimumValidity']
            a.colorCode = form.cleaned_data['colorCode']

            a.save()

            return HttpResponseRedirect('/documentstatuss/')

    else:
        form = DocumentStatusForm()
    return render(request, 'detail_template.html', {'form': form, 'action':'/documentstatus/', 'http_method':'POST'})

# GET/POST /area/<docstatuscode>
def edit_documentstatus(request, docstatuscode=None):
    if(docstatuscode):
        a = DocumentStatus.objects.get(id=int(docstatuscode))

        if request.method == 'POST':
            #update record with submitted values

            form = DocumentStatusForm(request.POST, instance=a)

            if form.is_valid():
                a.name = form.cleaned_data['name']
                a.enabled = form.cleaned_data['enabled']
                a.minimumValidity = form.cleaned_data['minimumValidity']
                a.colorCode = form.cleaned_data['colorCode']

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
    content = 'content about document type'
    link = '/documenttype/'

class ListDocumentTypeView(TemplateView):
    template_name = "doc/doctype_list_template.html"
    def get_context_data(self, **kwargs):
        context = super(ListDocumentTypeView, self).get_context_data(**kwargs)
        context['object_list'] = map(lambda s: DocumentTypeWrapper(s), DocumentType.objects.all())
        new = DocumentType()
        new.name = "<novo>"
        context['object_list'].append(DocumentTypeWrapper(new))
        return context

def handle_documenttype(request):
    if request.method == 'POST':

        form = DocumentTypeForm(request.POST)

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
def edit_documenttype(request, doctypecode=None):
    if(doctypecode):
        a = DocumentType.objects.get(id=int(doctypecode))

        if request.method == 'POST':
            #update record with submitted values

            form = DocumentTypeForm(request.POST, instance=a)

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

def handle_documenttypefield(request, doctypecode=None):
    doctype = DocumentType.objects.get(id=int(doctypecode))
    if request.method == 'POST':

        form = DocumentTypeFieldForm(request.POST)

        if form.is_valid():
            a = DocumentTypeField()
            a.name = form.cleaned_data['name']
            a.fieldType = form.cleaned_data['fieldType']
            a.fieldChoices = form.cleaned_data['fieldChoices']
            doctype.documenttypefield_set.add(a)

            return HttpResponseRedirect('/documenttype/' + str(doctype.id) + '/fields/')

    else:
        form = DocumentTypeFieldForm()
    return render(request, 'detail_template.html', {'form': form, 'action':'/documenttype/' + str(doctype.id) + '/field/', 'http_method':'POST'})

# GET/POST /area/<doctypefieldcode>
def edit_documenttypefield(request, doctypecode=None, doctypefieldcode=None):
    doctype = DocumentType.objects.get(id=int(doctypecode))
    if(doctypecode and doctypefieldcode):
        a = DocumentTypeField.objects.get(id=int(doctypefieldcode))

        if request.method == 'POST':
            #update record with submitted values

            form = DocumentTypeFieldForm(request.POST, instance=a)

            if form.is_valid():
                a.name = form.cleaned_data['name']
                a.fieldType = form.cleaned_data['fieldType']
                a.fieldChoices = form.cleaned_data['fieldChoices']
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
    def documentAsList(self, document):
        return [document.establishment.name, document.documentType.name, document.documentStatus.name, document.expirationDate]
    def get_context_data(self, **kwargs):
        context = super(ListDocumentView, self).get_context_data(**kwargs)
        qset = Document.objects
        selectionList = self.request.session.get('selection_list') # keep serialized version
        selected = {}                                              # keep object version
        if(not selectionList):
           selectionList = {}
        areacode = self.request.session.get('areacode')
        if(areacode):
            area = Area.objects.get(id=int(areacode))

        e = None
        establishmentId = self.request.GET.get('establishmentId')
        if(establishmentId):
            if(establishmentId=='None'):
                if 'establishment' in selectionList:
                    del selectionList['establishment']
            else:
                e = Establishment.objects.get(id=establishmentId)
                selectionList['establishment'] = to_JSON(e)
                qset = qset.filter(establishment=e)
                self.request.session['areacode'] = e.area.id
                area = e.area
        else:
            if 'establishment' in selectionList:
                for obj in serializers.deserialize("json", selectionList['establishment']):
                    e = obj.object
        if(e):
            selected['establishment'] = e
            qset = qset.filter(establishment=e)
        else:
            inner_qs = Establishment.objects.filter(area__id__exact=area.id)
            qset = qset.filter(establishment__in=inner_qs)

        t = None
        documentTypeId = self.request.GET.get('documentTypeId')
        if(documentTypeId):
            if(documentTypeId=='None'):
                if 'documentType' in selectionList:
                    del selectionList['documentType']
            else:
                t = DocumentType.objects.get(id=documentTypeId)
                selectionList['documentType'] = to_JSON(t)
                qset = qset.filter(documentType=t)
        else:
            if 'documentType' in selectionList:
                for obj in serializers.deserialize("json", selectionList['documentType']):
                    t = obj.object
        if(t):
            selected['documentType'] = t

        st = None
        documentStatusId = self.request.GET.get('documentStatusId')
        if(documentStatusId):
            if(documentStatusId=='None'):
                if 'documentStatus' in selectionList:
                    del selectionList['documentStatus']
            else:
                st = DocumentStatus.objects.get(id=documentStatusId)
                selectionList['documentStatus'] = to_JSON(st)
                qset = qset.filter(documentStatus=st)
        else:
            if 'documentStatus' in selectionList:
                for obj in serializers.deserialize("json", selectionList['documentStatus']):
                    st = obj.object
        if(st):
            selected['documentStatus'] = st

        self.request.session['selection_list'] = selectionList
        context['area'] = area
        context['selected'] = selected
        context['tableheader_list'] = ['Estabelecimento', 'Tipo de Documento', 'Status', 'Data de Expiração']
        context['object_list'] = map(lambda s: s, qset.all())
        context['area_choices'] = map(lambda s: s.name, Area.objects.all())
        context['establishment_choices'] = map(lambda s: { 'name' : s.name, 'id' : s.id }, area.establishment_set.all()) if area else []
        context['document_type_choices'] = map(lambda s: { 'name' : s.name, 'id' : s.id }, DocumentType.objects.all())
        context['document_status_choices'] = map(lambda s: { 'name' : s.name, 'id' : s.id }, DocumentStatus.objects.all())
        return context

# GET/POST /document/
@login_required
def handle_document(request):
    area = None
    areacode = request.session.get('areacode')
    if(areacode):
        area = Area.objects.get(id=int(areacode))


    if request.method == 'POST':

        form = DocumentForm(request.POST)

        if form.is_valid():
            a = Document()
            a.establishment = form.cleaned_data['establishment']
            a.documentType = form.cleaned_data['documentType']
            a.documentStatus = form.cleaned_data['documentStatus']
            a.expeditionDate = form.cleaned_data['expeditionDate']
            a.expirationDate = form.cleaned_data['expirationDate']

            a.save()

            h = DocumentHistory()
            h.user = request.user
            h.operation = "CREATION"
            h.snapshot = to_JSON(a)

            a.documenthistory_set.add()

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
        form = DocumentForm(initial={'establishment': e,'documentType': t })

    return render(request, 'detail_template.html', {'form': form, 'action':'/document/', 'http_method':'POST', 'area' : area})

# GET/POST /document/<documentcode>
@login_required
def edit_document(request, documentcode=None):
    if(documentcode):
        a = Document.objects.get(id=int(documentcode))

        if request.method == 'POST':
            #update record with submitted values

            form = DocumentForm(request.POST, instance=a)

            if form.is_valid():
                a.establishment = form.cleaned_data['establishment']
                a.documentType = form.cleaned_data['documentType']
                a.documentStatus = form.cleaned_data['documentStatus']
                a.expeditionDate = form.cleaned_data['expeditionDate']
                a.expirationDate = form.cleaned_data['expirationDate']

                a.save()

                h = DocumentHistory()
                h.user = request.user
                h.operation = "MODIFICATION"
                h.snapshot = to_JSON(a)

                a.documenthistory_set.add()

                return HttpResponseRedirect('/documents/')

            return render(request, 'detail_template.html', {'form': form, 'action':'/document/' + documentcode + '/', 'http_method':'POST'})
        else:
            #load record to allow edition

            form = DocumentForm(instance=a)
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
        context['form'] = DocumentDetailForm(instance=document)
        context['file_list'] = document.documentfile_set.values()
        context['imagefile_list'] = document.documentimagefile_set.values()
        return context

# GET/POST /document/
@login_required
def handle_documentupload(request):
    area = None
    areacode = request.session.get('areacode')
    if(areacode):
        area = Area.objects.get(id=int(areacode))



class ListDocumentHistoryView(TemplateView):
    template_name = "doc/dochistory_template.html"
