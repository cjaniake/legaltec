from django import forms
from django.forms import ModelForm, TextInput

from customauth.models import Message, SystemEvent


class ChatUserMessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'establishment']
        widgets = {
            'text': forms.Textarea(attrs={'rows':4}),
            'establishment': forms.HiddenInput()
        }
class ChatAdminMessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['user','establishment','text']
        widgets = {
            'text': forms.Textarea(attrs={'rows':4})
        }

class EventForm(ModelForm):
    class Meta:
        model = SystemEvent
        fields = ['user','entity','operation','error','snapshot']
        widgets = {
            'snapshot': forms.Textarea(attrs={'rows':4})
        }
