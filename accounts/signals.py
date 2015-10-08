# coding: utf-8

from django.dispatch import receiver
from registration.signals import user_activated

from .models import UserAccount


@receiver(user_activated)
def registration_completed(sender, user, request, **kwargs):
    account, created = UserAccount.objects.get_or_create(user=user)
    print account, created
