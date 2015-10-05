from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import BluePrintCreator, NeedBluePrint


class BluePrintCreatorAdminForm(forms.ModelForm):
    class Meta:
        model = BluePrintCreator
        fields = '__all__'

    def clean(self):
        try:
            if BluePrintCreator.objects.get(location=self.data['location']):
                raise forms.ValidationError(_("There is already a blueprint for this location!"))
        except Exception:
            return self.cleaned_data


class BluePrintCreatorAdmin(admin.ModelAdmin):
    form = BluePrintCreatorAdminForm
    filter_horizontal = ('needs',)

    fieldsets = (
        (None, {
            'fields': ('title', 'location')
        }),
        (None, {
            'classes': ('needs_in_blueprint',),
            'fields': ('needs',)
        }),
    )


class NeedBluePrintAdmin(admin.ModelAdmin):
    list_display = ['topic', 'get_location', 'from_time', 'to_time']


admin.site.register(BluePrintCreator, BluePrintCreatorAdmin)
admin.site.register(NeedBluePrint, NeedBluePrintAdmin)
