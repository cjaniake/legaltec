from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from area.models import Establishment
from customauth.forms import ChatUserMessageForm, ChatAdminMessageForm
from customauth.models import Message

class ListUserMessagesView(TemplateView):
    template_name = "customauth/user_messages.html"
    def get_context_data(self, **kwargs):
        context = super(ListUserMessagesView, self).get_context_data(**kwargs)

        u = self.request.user
        estabParam = None
        if 'estab' in self.request.GET:
            estabParam = self.request.GET['estab']
            context['estab'] = Establishment.get(id=estabParam)

        context['form'] = ChatUserMessageForm()
        qset = Message.objects.filter(user_id = u.id)
        qset = qset.filter(establishment_id = estabParam)
        context['msg_list'] = qset.order_by('-eventDate')[:20]
        context['action'] = '/chat/user/post/'
        return context

class ListAdminMessagesView(TemplateView):
    template_name = "customauth/admin_messages.html"
    def get_context_data(self, **kwargs):
        context = super(ListAdminMessagesView, self).get_context_data(**kwargs)

        estabParam = self.request.GET['estab'] if 'estab' in self.request.GET and self.request.GET['estab'] != '' else None
        userParam = self.request.GET['user'] if 'user' in self.request.GET and self.request.GET['user'] != '' else None

        context['form'] = ChatAdminMessageForm(initial = {"user": userParam, "establishment": estabParam})
        qset = Message.objects
        qset = qset.filter(establishment_id = estabParam)
        if(userParam):
            qset = qset.filter(user_id = userParam)
        context['msg_list'] = qset.order_by('-eventDate')[:20]
        context['action'] = '/chat/admin/post/'
        return context

def handle_user_message(request):
    if request.method == 'POST':

        form = ChatUserMessageForm(request.POST)

        if form.is_valid():
            m = Message()
            m.user = request.user
            m.text = form.cleaned_data['text']
            m.origin = 1

            m.save()

    return HttpResponseRedirect('/chat/user/')

def handle_admin_message(request):
    if request.method == 'POST':

        form = ChatAdminMessageForm(request.POST)

        if form.is_valid():
            m = Message()
            m.user = form.cleaned_data['user']
            m.text = form.cleaned_data['text']
            m.origin = 2

            m.save()

    return HttpResponseRedirect('/chat/admin/')
