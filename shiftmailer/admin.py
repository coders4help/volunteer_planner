# coding=utf-8
from django.contrib import admin
from .models import Mailer
from organizations.admin import MembershipFilteredAdmin


@admin.register(Mailer)
class MailerAdmin(MembershipFilteredAdmin):
    pass
