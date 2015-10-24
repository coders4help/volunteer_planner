# coding: utf-8

from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget

from . import models


class NewsAdminForm(forms.ModelForm):
    class Meta:
        model = models.NewsEntry
        fields = '__all__'

    text = forms.CharField(widget=CKEditorWidget())


@admin.register(models.NewsEntry)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm

    list_display = (
        'title',
        'subtitle',
        'slug',
        'creation_date',
        'facility',
        'organization'
    )
    list_filter = (
        'facility',
        'organization'
    )
    readonly_fields = ('slug',)
