# coding=utf-8
from django.core.mail import send_mail
from django.db.models.signals import pre_delete
from django.dispatch import receiver


from . import models

@receiver(pre_delete, sender=models.Need)
def send_email_notifications(sender, instance, **kwargs):
    """
    HACK ALERT

    This needed to be done quickly. Please use a proper email template,
    add some error handling, some sane max recipient handling, tests, etc.
    """
    subject = u'Schicht gelöscht'
    message = u'''
    Hallo ihr,

    leider mussten wir die folgende Schicht löschen:

    {need}

    Dies hier ist eine automatisch generierte Email. Im Helpdesk steht mit ein
    bisschen Glück eine Erklärung, warum die Schicht entfernt wurde.

    Liebe Grüße vom Volunteer Planner.
    '''.format(need=instance)

    from_email = "Volunteer-Planner.org <no-reply@volunteer-planner.org>"

    addresses = instance.get_volunteers().values_list('user__email', flat=True)

    send_mail(subject, message, from_email, addresses, fail_silently=True)
