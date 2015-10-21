# coding=utf-8
from django.contrib import admin
from django import forms
# Register your models here.
from ckeditor.widgets import CKEditorWidget
from .models import Notification
from organizations.admin import MembershipFilteredAdmin


class NotificationAdminForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'
    text = forms.CharField(widget=CKEditorWidget())


@admin.register(Notification)
class NotificationAdmin(MembershipFilteredAdmin):
    form = NotificationAdminForm
    readonly_fields = ('slug',)


