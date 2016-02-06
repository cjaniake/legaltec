# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from doc.forms import DocumentStatusForm
from doc.models import DocumentStatus


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
