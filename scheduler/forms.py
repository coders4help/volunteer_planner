from django import forms
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from scheduler.models import Shift, ShiftMessageToHelpers


class RegisterForShiftForm(forms.Form):
    leave_shift = forms.ModelChoiceField(queryset=Shift.objects, required=False)
    join_shift = forms.ModelChoiceField(
        queryset=Shift.objects.annotate(volunteer_count=Count("helpers")),
        required=False,
    )


class ShiftMessageToHelpersModelForm(forms.ModelForm):
    message = forms.TextInput(attrs={"class": "form-control"})

    def __init__(self, *args, **kwargs):
        super(ShiftMessageToHelpersModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = ShiftMessageToHelpers
        fields = ["message", "shift"]
        widgets = {
            "shift": forms.HiddenInput(),
        }
        labels = {"message": _("Write a message")}
