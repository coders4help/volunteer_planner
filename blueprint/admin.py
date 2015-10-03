# coding=utf-8
from django.contrib import admin
from django import forms

from .models import BluePrintCreator, NeedBluePrint


class BluePrintCreatorAdminForm(forms.ModelForm):
    class Meta:
        model = BluePrintCreator
        fields = '__all__'

    def clean(self):
        try:
            if BluePrintCreator.objects.get(facility=self.data['facility']):
                raise forms.ValidationError("Ort hat bereits eine Vorlage!")
        except Exception:
            return self.cleaned_data


class BluePrintCreatorAdmin(admin.ModelAdmin):
    form = BluePrintCreatorAdminForm
    filter_horizontal = ('needs',)

    fieldsets = (
        (None, {
            'fields': ('title', 'facility')
        }),
        (None, {
            'classes': ('needs_in_blueprint',),
            'fields': ('needs',)
        }),
    )


class NeedBluePrintAdmin(admin.ModelAdmin):
    list_display = ['topic', 'get_facility', 'from_time', 'to_time']


admin.site.register(BluePrintCreator, BluePrintCreatorAdmin)
admin.site.register(NeedBluePrint, NeedBluePrintAdmin)
