from django.contrib import admin
from django import forms
# Register your models here.
from ckeditor.widgets import CKEditorWidget
from .models import News


class NewsAdminForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
    text = forms.CharField(widget=CKEditorWidget())


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    readonly_fields = ('slug',)

admin.site.register(News, NewsAdmin)
