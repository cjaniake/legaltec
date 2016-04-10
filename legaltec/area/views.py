# -*- coding: utf-8 -*-
import logging

from django.core.serializers import json
from django.core.signals import request_finished
from django.db.models import Count
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from area.forms import AreaForm, EstablishmentForm
from area.models import Area, Establishment
from doc.models import Document, DocumentStatus
from customauth.models import CustomUser, Message

class AreaWrapper:
    def __init__(self, area, presentation):
        self.area = area
        self.presentation = presentation
        inner_qs = Establishment.objects.filter(area__id__exact=self.area.id)
        qset = Document.objects.filter(establishment__in=inner_qs, documentStatus__enabled=True)
        self.priorityDocs = qset.order_by('expirationDate')[:2]
    def name(self, **kwargs):
        return self.area.name
    def id(self, **kwargs):
        return self.area.id
    def content(self, **kargs):
        return self.priorityDocs
    def link(self, **kwargs):
        return '/area/' if self.area.id is None else '/area/' + str(self.area.id)
    def linkentrar(self, **kwargs):
        return '/area/' + str(self.area.id) + '/establishments/?p=' + self.presentation
    def icon(self, **kwargs):
        if self.priorityDocs and len(self.priorityDocs) > 0:
            return self.priorityDocs[0].documentStatus.glyphicon
        else :
            return 'glyphicon-ban-circle'
    def iconcolor(self, **kwargs):
        if self.priorityDocs and len(self.priorityDocs) > 0:
            return self.priorityDocs[0].documentStatus.colorCode
        else :
            return '#E6E6E6'
    def dataseries(self, **kwargs):
        inner_qs = Establishment.objects.filter(area__id__exact=self.area.id)
        qset = DocumentStatus.objects\
            .filter(document__establishment__in=inner_qs)\
            .filter(document__documentStatus__enabled=True)\
            .annotate(num_docs=Count('document'))
        return map(lambda d: {'value':d.num_docs, 'label':d.name, 'color':d.colorCode}, qset)


class ListAreaView(TemplateView):
    template_name = "area/area_objlist_small.html"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        c = CustomUser.objects.filter(user__id=request.user.id)
        if c and c[0].establishment:
            return HttpResponseRedirect('/documents/')
        if c and c[0].area:
            return HttpResponseRedirect('/area/' + str(c[0].area.id) + '/establishments/')
        return super(ListAreaView, self).dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        presentation = self.request.GET['p'] if 'p' in self.request.GET else 'small'
        context = super(ListAreaView, self).get_context_data(**kwargs)
        #context['object_list'] = list(Area.objects.all())
        context['object_list'] = map(lambda area: AreaWrapper(area, presentation), Area.objects.all())

        # clean session information
        if 'areacode' in self.request.session:
            del self.request.session['areacode']
        if 'selection_list' in self.request.session:
            del self.request.session['selection_list']

        # select template to be presented
        if presentation == 'large':
            self.template_name = "area/area_objlist_large.html"
        elif presentation == 'list':
            self.template_name = "area/area_objlist_list.html"
        else:
            self.template_name = "area/area_objlist_small.html"

        return context

def handle_area(request):
    if request.method == 'POST':

        form = AreaForm(request.POST)

        if form.is_valid():
            a = Area()
            a.name = form.cleaned_data['name']
            a.enabled = form.cleaned_data['enabled']
            a.adminEmail = form.cleaned_data['adminEmail']
            a.validUntil = form.cleaned_data['validUntil']
            a.applyPermissions = form.cleaned_data['applyPermissions']
            a.save()

            return HttpResponseRedirect('/areas/')

    else:
        form = AreaForm()
    return render(request, 'detail_template.html', {'form': form, 'action':'/area/', 'http_method':'POST'})

# GET/POST /area/<areacode>
def edit_area(request, areacode=None):
    if areacode:
        a = Area.objects.get(id=int(areacode))

        if request.method == 'POST':
            #update record with submitted values

            form = AreaForm(request.POST, instance=a)

            if form.is_valid():
                a.name = form.cleaned_data['name']
                a.enabled = form.cleaned_data['enabled']
                a.adminEmail = form.cleaned_data['adminEmail']
                a.validUntil = form.cleaned_data['validUntil']
                a.applyPermissions = form.cleaned_data['applyPermissions']
                a.save()

                return HttpResponseRedirect('/areas/')

            return render(request, 'detail_template.html', {'form': form, 'action':'/area/' + areacode + '/', 'http_method':'POST'})
        else:
            #load record to allow edition

            form = AreaForm(instance=a)
            return render(request, 'detail_template.html', {'form': form, 'action':'/area/' + areacode + '/', 'http_method':'POST'})
    else:
        return HttpResponseRedirect('/areas/')

class EstablishmentWrapper:
    def __init__(self, estab, request):
        self.estab = estab
        qset = Document.objects.filter(establishment__id=self.estab.id, documentStatus__enabled=True)
        self.priorityDocs = qset.order_by('expirationDate')[:2]
        self.request = request
    def name(self, **kwargs):
        return self.estab.name
    def id(self, **kwargs):
        return self.estab.id
    def content(self, **kargs):
        return self.priorityDocs
    def link(self, **kwargs):
        return '/area/' + str(self.estab.area.id) + '/establishment/'
    def linkentrar(self, **kwargs):
        return '/documents/?establishmentId=' + str(self.estab.id)
    def icon(self, **kwargs):
        if self.priorityDocs:
            return self.priorityDocs[0].documentStatus.glyphicon
        else :
            return 'glyphicon-ban-circle'
    def iconcolor(self, **kwargs):
        if self.priorityDocs:
            return self.priorityDocs[0].documentStatus.colorCode
        else :
            return '#E6E6E6'
    def dataseries(self, **kwargs):
        qset = DocumentStatus.objects\
            .filter(document__establishment__exact=self.estab.id)\
            .filter(document__documentStatus__enabled=True)\
            .annotate(num_docs=Count('document'))
        return map(lambda d: {'value':d.num_docs, 'label':d.name, 'color':d.colorCode}, qset)
    def messagecount(self, **kwargs):
        qset = Message.objects.filter(establishment_id = self.estab.id).filter(readDate = None)
        if self.request.user.is_superuser:
            qset = qset.filter(origin = 1)
        else:
            qset = qset.filter(origin__gt=1).filter(user = self.request.user)
        return qset.count()



# GET /area/<areacode>/establishments
class ListEstablishmentView(TemplateView):
    template_name = "area/establishment_objlist_small.html"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        c = CustomUser.objects.filter(user__id=request.user.id)
        if c and c[0].establishment:
            return HttpResponseRedirect('/documents/')
        return super(ListEstablishmentView, self).dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        areacode = kwargs['areacode']
        context = super(ListEstablishmentView, self).get_context_data(**kwargs)
        area = Area.objects.get(id=int(areacode))
        context['area'] = area
        self.request.session['areacode'] = areacode
        establishmentArray = area.establishment_set.all()
        context['object_list'] = map(lambda s: EstablishmentWrapper(s, self.request), establishmentArray)

        # clean session information
        if 'selection_list' in self.request.session:
            del self.request.session['selection_list']

        # select template to be presented
        presentation = self.request.GET['p'] if 'p' in self.request.GET else 'small'
        if presentation == 'large':
            self.template_name = "area/establishment_objlist_large.html"
        elif presentation == 'list':
            self.template_name = "area/establishment_objlist_list.html"
        else:
            self.template_name = "area/establishment_objlist_small.html"

        return context

# GET/POST /area/<areacode>/establishment
def handle_establishment(request, areacode=None):
    area = Area.objects.get(id=int(areacode))
    if request.method == 'POST':

        form = EstablishmentForm(request.POST)

        if form.is_valid():
            l = Establishment()
            l.name = form.cleaned_data['name']
            l.city = form.cleaned_data['city']
            l.state = form.cleaned_data['state']
            l.adminEmail = form.cleaned_data['adminEmail']
            l.cpnj = form.cleaned_data['cnpj']
            l.iest = form.cleaned_data['iest']
            l.area = area

            l.save()
            area.establishment_set.add(l)

            return HttpResponseRedirect('/area/' + areacode + '/establishments')

    else:
        form = EstablishmentForm()
    return render(request, 'detail_template.html', {'form': form, 'action':'/area/' + areacode + '/establishment/', 'http_method':'POST', 'area': area})

# GET/POST /area/<areacode>/establishment/<establishmentid>
def edit_establishment(request, areacode=None, establishmentid=None):
    if areacode and establishmentid:
        area = Area.objects.get(id=int(areacode))
        l = Establishment.objects.get(id=int(establishmentid))

        if request.method == 'POST':
            #update record with submitted values

            form = EstablishmentForm(request.POST, instance=l)

            if form.is_valid():
                l.name = form.cleaned_data['name']
                l.city = form.cleaned_data['city']
                l.state = form.cleaned_data['state']
                l.adminEmail = form.cleaned_data['adminEmail']
                l.cpnj = form.cleaned_data['cnpj']
                l.iest = form.cleaned_data['iest']
                l.save()

                return HttpResponseRedirect('/area/' + areacode + '/establishments')

            return render(request, 'detail_template.html', {'form': form, 'action':'/area/' + areacode + '/establishment/' + establishmentid + '/', 'http_method':'POST', 'area': area})
        else:
            #load record to allow edition

            form = EstablishmentForm(instance=l)
            return render(request, 'detail_template.html', {'form': form, 'action':'/area/' + areacode + '/establishment/' + establishmentid + '/', 'http_method':'POST', 'area': area})
        return HttpResponseRedirect('/area/' + areacode + '/establishments') if areacode else HttpResponseRedirect('/areas/')
