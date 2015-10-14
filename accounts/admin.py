# coding: utf-8

from django.contrib import admin

from .models import UserAccount


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = (u'id', 'user')
    raw_id_fields = ('user',)
