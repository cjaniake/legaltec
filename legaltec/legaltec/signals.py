from django.db.models.signals import pre_save
from django.dispatch import receiver
from customauth.models import SystemEvent

#@receiver(pre_save, sender=MyModel)
@receiver(pre_save)
def general_pre_save_handler(sender, **kwargs):
    event = SystemEvent()
    event.save()

