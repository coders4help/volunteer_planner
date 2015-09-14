from django.contrib import admin
from django import forms
from .models import BluePrintCreator, NeedBluePrint


class BluePrintCreatorAdminForm(forms.ModelForm):
    class Meta:
        model = BluePrintCreator
        fields = '__all__'

    def clean(self):
        try:
            if BluePrintCreator.objects.get(location=self.data['location']):
                raise forms.ValidationError("Ort hat bereits eine Vorlage!")
        except Exception:
            return self.cleaned_data


class BluePrintCreatorAdmin(admin.ModelAdmin):
    form = BluePrintCreatorAdminForm
    filter_horizontal = ('needs',)


class NeedBluePrintAdmin(admin.ModelAdmin):
    list_display = ['topic', 'get_location']


admin.site.register(BluePrintCreator, BluePrintCreatorAdmin)
admin.site.register(NeedBluePrint, NeedBluePrintAdmin)
