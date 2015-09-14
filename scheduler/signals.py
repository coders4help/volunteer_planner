# coding=utf-8
from django.core.mail import EmailMessage

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from scheduler.models import Need


@receiver(pre_delete, sender=Need)
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

    from_email = "Volunteer-Planner.org <noreply@volunteer-planner.org>"

    addresses = instance.registrationprofile_set.values_list('user__email', flat=True)

    mail = EmailMessage(subject=subject, body=message,
                        to='support@volunteer-planner.org',
                        from_email=from_email,
                        bcc=addresses)
    mail.send()
