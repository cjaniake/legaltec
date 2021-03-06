from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from area.models import Establishment
from customauth.forms import ChatUserMessageForm, ChatAdminMessageForm, EventForm
from customauth.models import Message
from django.core.cache import cache
from django.contrib.auth import logout as djangologout
from django.contrib.auth.models import User
from customauth.models import SystemEvent
from django.db.models import Count, Max

def countUserMsg(user):
    qset = Message.objects.filter(establishment_id = None).filter(readDate = None)
    if user is None or user.is_superuser:
        qset = qset.filter(origin = 1)
    else:
        qset = qset.filter(origin__gt=1).filter(user = user)
    return qset.count()

def cacheKeyUser(user):
    cache_key = 'usermsg_'
    if user is None or user.is_superuser: cache_key = cache_key + 'SU'
    else: cache_key = cache_key + str(user.id)

def cacheUserMsg(request, user):
    cache_time = 1800 # time to live in seconds
    result = cache.get(cacheKeyUser(user))
    if not result:
        result = countUserMsg(user)
        cache.set(cacheKeyUser(user), result, cache_time)
    return result

class UserMsgMiddleware(object):
    def process_request(self, request):
        if not request.user.is_anonymous():
            request.session['user_messages'] = cacheUserMsg(request, request.user)

class ListUserMessagesView(TemplateView):
    template_name = "customauth/user_messages.html"
    def get_context_data(self, **kwargs):
        context = super(ListUserMessagesView, self).get_context_data(**kwargs)

        u = self.request.user
        estabParam = None
        if 'estab' in self.request.GET and self.request.GET['estab'] != 'None':
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
        cache.delete(cacheKeyUser(u))

        context['action'] = '/chat/user/post/'
        return context

class ListAdminMessagesView(TemplateView):
    template_name = "customauth/admin_messages.html"
    def get_context_data(self, **kwargs):
        context = super(ListAdminMessagesView, self).get_context_data(**kwargs)

        ordered_users = User.objects.annotate(maxdt=Max('message__eventDate')).order_by('-maxdt')
        admin_chat_context = []

        for user in ordered_users:
            admin_chat_user = {}
            admin_chat_user['user'] = user
            admin_chat_user['unread'] = Message.objects.filter(establishment_id = None).filter(user_id = user.id).filter(origin=1).filter(readDate = None).count()
            admin_chat_user['msg_list'] = Message.objects.filter(establishment_id = None).filter(user_id = user.id).order_by('-eventDate')[:6]
            admin_chat_user['form'] = ChatAdminMessageForm(initial = {"user": user})

            admin_chat_context.append(admin_chat_user)

        userParam = self.request.GET['user'] if 'user' in self.request.GET and self.request.GET['user'] != '' else None

        context['admin_chat'] = admin_chat_context
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
            cache.delete(cacheKeyUser(None))

    return HttpResponseRedirect(redirectTo)

def handle_admin_message(request):
    redirectTo = '/chat/admin/'
    if request.method == 'POST':

        form = ChatAdminMessageForm(request.POST)

        if form.is_valid():
            m = Message()
            user = form.cleaned_data['user']
            m.user = user
            m.text = form.cleaned_data['text']
            m.origin = 2
            m.save()
            cache.delete(cacheKeyUser(user))


    return HttpResponseRedirect(redirectTo)

def mark_as_read_admin_message(self, userid=None):
    qset = Message.objects.filter(establishment_id = None).filter(user_id = userid).filter(origin=1).filter(readDate = None)
    updateResult = qset.update(readDate=timezone.now())
    cache.delete(cacheKeyUser(None))

class ListEventsView(TemplateView):
    template_name = "customauth/event_list.html"
    def get_context_data(self, **kwargs):
        context = super(ListEventsView, self).get_context_data(**kwargs)

        u = self.request.user
        estabParam = None
        pageParam = 1
        if 'page' in self.request.GET and self.request.GET['page'] != 'None':
            pageParam = int(self.request.GET['page'])

        pagesize=20
        start=(pageParam-1)*pagesize
        if start < 0: start = 0
        end=start + pagesize + 1
        events = SystemEvent.objects.all()[start:end]
        context['page'] = pageParam
        context['page1'] = pageParam + 1
        context['page2'] = pageParam + 2
        context['page3'] = pageParam + 3
        context['page4'] = pageParam + 4
        context['pagePrev'] = pageParam - 1 if pageParam > 1 else 1
        context['pageNext'] = pageParam + 1
        context['event_list'] = events

        return context

def view_event(request, eventid=None):
    evt = SystemEvent.objects.get(id=int(eventid))
    form = EventForm(instance=evt)
    return render(request, 'customauth/event_detail.html', {'form': form, 'event':evt, 'action':'/events/'})

def logout(request):
    djangologout(request)
    return HttpResponseRedirect('/accounts/login/')