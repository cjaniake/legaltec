# -*- coding: utf-8 -*-
import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from area.forms import AreaForm, EstablishmentForm, AreaStatusForm
from area.models import Area, Establishment, AreaStatus


class AreaStatusWrapper:
    def __init__(self, areastatus):
        self.areastatus = areastatus
    def name(self, **kwargs):
        return self.areastatus.name
    def id(self, **kwargs):
        return self.areastatus.id
    content = 'content about area status'
    link = '/areastatus/'

class ListAreaStatusView(TemplateView):
    template_name = "list_template.html"
    def get_context_data(self, **kwargs):
        context = super(ListAreaStatusView, self).get_context_data(**kwargs)
        #context['object_list'] = list(AreaStatus.objects.all())
        context['object_list'] = map(lambda s: AreaStatusWrapper(s), AreaStatus.objects.all())
        new = AreaStatus()
        new.name = "<novo>"
        context['object_list'].append(AreaStatusWrapper(new))
        return context

def handle_areastatus(request):
    if request.method == 'POST':

        form = AreaStatusForm(request.POST)

        if form.is_valid():
            a = AreaStatus()
            a.name = form.cleaned_data['name']
            a.enabled = form.cleaned_data['enabled']
            a.minimumValidity = form.cleaned_data['minimumValidity']
            a.colorCode = form.cleaned_data['colorCode']

            a.save()

            return HttpResponseRedirect('/areastatus/')

    else:
        form = AreaStatusForm()
    return render(request, 'detail_template.html', {'form': form, 'action':'/areastatus/', 'http_method':'POST'})

# GET/POST /area/<areastatuscode>
def edit_areastatus(request, areastatuscode=None):
    if(areastatuscode):
        a = AreaStatus.objects.get(id=int(areastatuscode))

        if request.method == 'POST':
            #update record with submitted values

            form = AreaStatusForm(request.POST, instance=a)

            if form.is_valid():
                a.name = form.cleaned_data['name']
                a.enabled = form.cleaned_data['enabled']
                a.minimumValidity = form.cleaned_data['minimumValidity']
                a.colorCode = form.cleaned_data['colorCode']

                a.save()

                return HttpResponseRedirect('/areastatuss/')

            return render(request, 'detail_template.html', {'form': form, 'action':'/areastatus/' + areastatuscode + '/', 'http_method':'POST'})
        else:
            #load record to allow edition

            form = AreaStatusForm(instance=a)
            return render(request, 'detail_template.html', {'form': form, 'action':'/areastatus/' + areastatuscode + '/', 'http_method':'POST'})
    else:
        return HttpResponseRedirect('/areastatus/')

class AreaWrapper:
    def __init__(self, area):
        self.area = area
    def name(self, **kwargs):
        return self.area.name
    def id(self, **kwargs):
        return self.area.id
    content = 'content about area'
    def link(self, **kwargs):
        return '/area/' + str(self.area.id)
    def linkentrar(self, **kwargs):
        return '/area/' + str(self.area.id) + '/establishments'

class ListAreaView(TemplateView):
    template_name = "area/area_list_template.html"
    def get_context_data(self, **kwargs):
        context = super(ListAreaView, self).get_context_data(**kwargs)
        #context['object_list'] = list(Area.objects.all())
        context['object_list'] = map(lambda s: AreaWrapper(s), Area.objects.all())
        new = Area()
        new.name = "<nova>"
        context['object_list'].append(AreaWrapper(new))
        return context

def handle_area(request):
    if request.method == 'POST':

        form = AreaForm(request.POST)

        if form.is_valid():
            a = Area()
            a.name = form.cleaned_data['name']
            a.areaStatus = form.cleaned_data['areaStatus']
            a.adminEmail = form.cleaned_data['adminEmail']

            a.save()

            return HttpResponseRedirect('/areas/')

    else:
        form = AreaForm()
    return render(request, 'detail_template.html', {'form': form, 'action':'/area/', 'http_method':'POST'})

# GET/POST /area/<areacode>
def edit_area(request, areacode=None):
    if(areacode):
        a = Area.objects.get(id=int(areacode))

        if request.method == 'POST':
            #update record with submitted values

            form = AreaForm(request.POST, instance=a)

            if form.is_valid():
                a.name = form.cleaned_data['name']
                a.areaStatus = form.cleaned_data['areaStatus']
                a.adminEmail = form.cleaned_data['adminEmail']

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
    def __init__(self, estab):
        self.estab = estab
    def name(self, **kwargs):
        return self.estab.name
    def id(self, **kwargs):
        return self.estab.id
    content = 'content about estab'
    def link(self, **kwargs):
        return '/area/' + str(self.estab.area.id) + '/establishment/' + str(self.estab.id)
    def linkentrar(self, **kwargs):
        return '/documents?establishment=' + str(self.estab.id)

# GET /area/<areacode>/establishments
class ListEstablishmentView(TemplateView):
    template_name = "area/area_list_template.html"
    def get_context_data(self, **kwargs):
        areacode = kwargs['areacode']
        context = super(ListEstablishmentView, self).get_context_data(**kwargs)
        area = Area.objects.get(id=int(areacode))
        context['area'] = area
        #establishmentArray = area.establishment_set.values
        #context['object_list'] = establishmentArray
        establishmentArray = area.establishment_set.all()
        context['object_list'] = map(lambda s: EstablishmentWrapper(s), establishmentArray)
        new = Establishment()
        new.name = "<novo>"
        new.area = area
        context['object_list'].append(EstablishmentWrapper(new))
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

            area = Area.objects.get(id=int(areacode))
            area.establishment_set.add(l)

            return HttpResponseRedirect('/area/' + areacode + '/establishments')

    else:
        form = EstablishmentForm()
    return render(request, 'detail_template.html', {'form': form, 'action':'/area/' + areacode + '/establishment/', 'http_method':'POST', 'area': area})

# GET/POST /area/<areacode>/establishment/<establishmentid>
def edit_establishment(request, areacode=None, establishmentid=None):
    if(areacode and establishmentid):
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

                l.save()

                return HttpResponseRedirect('/area/' + areacode + '/establishments')

            return render(request, 'detail_template.html', {'form': form, 'action':'/area/' + areacode + '/establishment/' + establishmentid + '/', 'http_method':'POST', 'area': area})
        else:
            #load record to allow edition

            form = EstablishmentForm(instance=l)
            return render(request, 'detail_template.html', {'form': form, 'action':'/area/' + areacode + '/establishment/' + establishmentid + '/', 'http_method':'POST', 'area': area})
        return HttpResponseRedirect('/area/' + areacode + '/establishments') if areacode else HttpResponseRedirect('/areas/')
