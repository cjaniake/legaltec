from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
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
            estab = Establishment.objects.get(id=estabParam)
            context['establishment'] = estab
            context['area'] = estab.area

        context['form'] = ChatUserMessageForm(initial = {"establishment": estabParam})
        qset = Message.objects.filter(user_id = u.id)
        qset = qset.filter(establishment_id = int(estabParam) if estabParam else None)
        context['msg_list'] = qset.order_by('-eventDate')[:20]

        qset = qset.filter(origin__gt=1)
        qset.update(readDate=timezone.now())

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
        qset = qset.filter(establishment_id = int(estabParam) if estabParam else None)
        if userParam:
            qset = qset.filter(user_id = userParam)
        context['msg_list'] = qset.order_by('-eventDate')[:20]

        qset = qset.filter(origin=1)
        qset.update(readDate=timezone.now())

        context['action'] = '/chat/admin/post/'
        return context

def handle_user_message(request):
    redirectTo = '/chat/user/'
    if request.method == 'POST':

        form = ChatUserMessageForm(request.POST)

        if form.is_valid():
            m = Message()
            m.user = request.user
            m.text = form.cleaned_data['text']
            establishment = form.cleaned_data['establishment']
            if establishment:
                m.establishment = establishment
                redirectTo = redirectTo + '?estab=' + str(establishment.id)
            m.origin = 1

            m.save()

    return HttpResponseRedirect(redirectTo)

def handle_admin_message(request):
    redirectTo = '/chat/admin/?'
    if request.method == 'POST':

        form = ChatAdminMessageForm(request.POST)

        if form.is_valid():
            m = Message()
            user = form.cleaned_data['user']
            if user:
                m.user = user
                redirectTo = redirectTo + '&user=' + str(user.id)
            m.text = form.cleaned_data['text']
            m.origin = 2
            establishment = form.cleaned_data['establishment']
            if establishment:
                m.establishment = establishment
                redirectTo = redirectTo + '&estab=' + str(establishment.id)

            m.save()

    return HttpResponseRedirect(redirectTo)
