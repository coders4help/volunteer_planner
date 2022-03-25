# coding: utf-8
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.flatpages.forms import FlatpageForm

from content.models import FlatPageTranslation


class FlatPageTranslationFormWithHTMLEditor(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        fields = "__all__"
        model = FlatPageTranslation


class FlatPageFormWithHTMLEditor(FlatpageForm):
    content = forms.CharField(widget=CKEditorWidget())
