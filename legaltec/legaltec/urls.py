"""legaltec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from area import views as areaviews
from doc import views as docviews

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^areas/', areaviews.ListAreaView.as_view()),
    url(r'^area/$', areaviews.handle_area),
    url(r'^area/(?P<areacode>[0-9]+)/$', areaviews.edit_area),
    url(r'^area/(?P<areacode>[0-9]+)/establishments/$', areaviews.ListEstablishmentView.as_view()),
    url(r'^area/(?P<areacode>[0-9]+)/establishment/$', areaviews.handle_establishment),
    url(r'^area/(?P<areacode>[0-9]+)/establishment/(?P<establishmentid>[0-9]+)/$', areaviews.edit_establishment),
    url(r'^areastatuss/', areaviews.ListAreaStatusView.as_view()),
    url(r'^areastatus/$', areaviews.handle_areastatus),
    url(r'^areastatus/(?P<areastatuscode>[0-9]+)/$', areaviews.edit_areastatus),
    url(r'^documentstatuss/', docviews.ListDocumentStatusView.as_view()),
    url(r'^documentstatus/$', docviews.handle_documentstatus),
    url(r'^documentstatus/(?P<docstatuscode>[0-9]+)/$', docviews.edit_documentstatus),
]
