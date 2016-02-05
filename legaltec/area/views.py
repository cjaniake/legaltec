# -*- coding: utf-8 -*-
import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from area.forms import AreaForm, EstablishmentForm, AreaStatusForm
from area.models import Area, Establishment, AreaStatus


class ListAreaStatusView(TemplateView):
    template_name = "list_template.html"
    def get_context_data(self, **kwargs):
        context = super(ListAreaStatusView, self).get_context_data(**kwargs)
        context['object_list'] = list(AreaStatus.objects.all())
        new = AreaStatus()
        new.name = "<novo>"
        context['object_list'].append(new)
        return context

def handle_areastatus(request):
    if request.method == 'POST':

        form = AreaStatusForm(request.POST)

        if form.is_valid():
            a = Area()
            a.name = form.cleaned_data['name']
            a.enabled = form.cleaned_data['enabled']

            a.save()

            return HttpResponseRedirect('/areastatus/')

    else:
        form = AreaStatusForm()
    return render(request, 'detail_template.html', {'form': form, 'action':'/areastatus/', 'http_method':'POST'})

# GET/POST /area/<areacode>
def edit_areastatus(request, areacode=None):
    if(areacode):
        a = AreaStatus.objects.get(id=int(areacode))

        if request.method == 'POST':
            #update record with submitted values

            form = AreaStatusForm(request.POST, instance=a)

            if form.is_valid():
                a.name = form.cleaned_data['name']
                a.enabled = form.cleaned_data['enabled']

                a.save()

                return HttpResponseRedirect('/areastatus/')

            return render(request, 'detail_template.html', {'form': form, 'action':'/area/' + areacode + '/', 'http_method':'POST'})
        else:
            #load record to allow edition

            form = AreaStatusForm(instance=a)
            return render(request, 'detail_template.html', {'form': form, 'action':'/area/' + areacode + '/', 'http_method':'POST'})
    else:
        return HttpResponseRedirect('/areastatus/')

class ListAreaView(TemplateView):
    template_name = "list_template.html"
    def get_context_data(self, **kwargs):
        context = super(ListAreaView, self).get_context_data(**kwargs)
        context['object_list'] = list(Area.objects.all())
        new = Area()
        new.name = "<nova>"
        context['object_list'].append(new)
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

# GET /area/<areacode>/establishments
class ListEstablishmentView(TemplateView):
    template_name = "list_template.html"
    def get_context_data(self, **kwargs):
        areacode = kwargs['areacode']
        context = super(ListEstablishmentView, self).get_context_data(**kwargs)
        area = Area.objects.get(id=int(areacode))
        context['area'] = area
        establishmentArray = area.establishment_set.values
        context['object_list'] = establishmentArray
        new = Establishment()
        new.name = "<novo>"
        context['object_list'].append(new)
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

            form = EstablishmentnForm(instance=l)
            return render(request, 'detail_template.html', {'form': form, 'action':'/area/' + areacode + '/establishment/' + establishmentid + '/', 'http_method':'POST', 'area': area})
        return HttpResponseRedirect('/area/' + areacode + '/establishments') if areacode else HttpResponseRedirect('/areas/')
