# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from doc.forms import DocumentStatusForm, DocumentTypeForm, DocumentTypeFieldForm
from doc.models import DocumentStatus, DocumentType, DocumentTypeField


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
