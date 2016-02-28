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
from customauth import views as userviews
from django.conf.urls.static import static

from legaltec import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/profile/', areaviews.ListAreaView.as_view()),
    url(r'^areas/', areaviews.ListAreaView.as_view()),
    url(r'^area/$', areaviews.handle_area),
    url(r'^area/(?P<areacode>[0-9]+)/$', areaviews.edit_area),
    url(r'^area/(?P<areacode>[0-9]+)/establishments/$', areaviews.ListEstablishmentView.as_view()),
    url(r'^area/(?P<areacode>[0-9]+)/establishment/$', areaviews.handle_establishment),
    url(r'^area/(?P<areacode>[0-9]+)/establishment/(?P<establishmentid>[0-9]+)/$', areaviews.edit_establishment),
    url(r'^documentstatuss/', docviews.ListDocumentStatusView.as_view()),
    url(r'^documentstatus/$', docviews.handle_documentstatus),
    url(r'^documentstatus/(?P<docstatuscode>[0-9]+)/$', docviews.edit_documentstatus),
    url(r'^documenttypes/', docviews.ListDocumentTypeView.as_view()),
    url(r'^documenttype/$', docviews.handle_documenttype),
    url(r'^documenttype/(?P<doctypecode>[0-9]+)/$', docviews.edit_documenttype),
    url(r'^documenttype/(?P<doctypecode>[0-9]+)/fields/', docviews.ListDocumentTypeFieldView.as_view()),
    url(r'^documenttype/(?P<doctypecode>[0-9]+)/field/$', docviews.handle_documenttypefield),
    url(r'^documenttype/(?P<doctypecode>[0-9]+)/field/(?P<doctypefieldcode>[0-9]+)/$', docviews.edit_documenttypefield),
    url(r'^documents/$', docviews.ListDocumentView.as_view()),
    url(r'^document/$', docviews.handle_document),
    url(r'^document/(?P<documentcode>[0-9]+)/$', docviews.edit_document),
    url(r'^document/(?P<documentcode>[0-9]+)/files/$', docviews.ListDocumentFileView.as_view()),
    url(r'^document/(?P<documentcode>[0-9]+)/file/$', docviews.handle_documentupload),
    url(r'^document/(?P<documentcode>[0-9]+)/imagefile/$', docviews.handle_imageupload),
    url(r'^document/(?P<documentcode>[0-9]+)/history/$', docviews.ListDocumentHistoryView.as_view()),
    url(r'^updateDocumentStatus/$', docviews.update_document_status),
    url(r'^chat/user/$', userviews.ListUserMessagesView.as_view()),
    url(r'^chat/admin/$', userviews.ListAdminMessagesView.as_view()),
    url(r'^chat/user/post/$', userviews.handle_user_message),
    url(r'^chat/admin/post/$', userviews.handle_admin_message),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)