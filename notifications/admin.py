from django.contrib import admin
from django import forms
# Register your models here.
from ckeditor.widgets import CKEditorWidget
from .models import Notification


class NotificationAdminForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'
    text = forms.CharField(widget=CKEditorWidget())


class NotificationAdmin(admin.ModelAdmin):
    form = NotificationAdminForm
    readonly_fields = ('slug',)

admin.site.register(Notification, NotificationAdmin)
