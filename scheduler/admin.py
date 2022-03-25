import logging

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.utils import timezone
from django.utils.html import format_html, mark_safe
from django.utils.translation import gettext_lazy as _

from organizations.admin import MembershipFieldListFilter, MembershipFilteredAdmin
from . import models
from .fields import FormattedModelChoiceIteratorFactory

logger = logging.getLogger(__name__)


class FormattedModelChoiceFieldAdminMixin:

    fk_label_formats = None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if self.fk_label_formats and db_field.name in self.fk_label_formats.keys():
            field.iterator = FormattedModelChoiceIteratorFactory(
                label_format=self.fk_label_formats[db_field.name]
            )
        return field


class ShiftAdminForm(forms.ModelForm):
    class Meta:
        model = models.Shift
        fields = [
            "facility",
            "slots",
            "task",
            "workplace",
            "starting_time",
            "ending_time",
            "members_only",
        ]

    def __init__(self, *args, **kwargs):
        super(ShiftAdminForm, self).__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, "facility"):
            facility = self.instance.facility
            self.fields["task"].queryset = self.fields["task"].queryset.filter(
                facility=facility
            )
            self.fields["workplace"].queryset = self.fields[
                "workplace"
            ].queryset.filter(facility=facility)

    def clean(self):
        """Validation of shift data, to prevent non-sense values to be entered"""
        # Check start and end times to be reasonable
        start = self.cleaned_data.get("starting_time")
        end = self.cleaned_data.get("ending_time")

        facility = self.cleaned_data.get("facility") or self.instance.facility
        if facility:

            task = self.cleaned_data.get("task")
            if task and not task.facility == facility:
                msg = (
                    str(_(f"Facilities do not match."))
                    + " "
                    + str(
                        _(
                            f'"{task.name}" belongs to facility '
                            f'"{task.facility.name}", but shift takes place at '
                            f'"{facility.name}".'
                        )
                    )
                )
                self.add_error("task", ValidationError(msg))

            workplace = self.cleaned_data.get("workplace")
            if workplace and not workplace.facility == facility:
                msg = (
                    str(_(f"Facilities do not match."))
                    + " "
                    + str(
                        _(
                            f'"{workplace.name}" is at '
                            f'"{workplace.facility.name}" but shift takes place '
                            f'at "{facility.name}".'
                        )
                    )
                )
                self.add_error("workplace", ValidationError(msg))

        # No times, no joy
        if not start:
            self.add_error("starting_time", ValidationError(_("No start time given.")))
        if not end:
            self.add_error("ending_time", ValidationError(_("No end time given.")))

        # There is no known reason to modify shifts in the past
        if start:
            now = timezone.now()
            if start < now:
                self.add_error(
                    "starting_time", ValidationError(_("Start time in the past."))
                )
            if end and not end > start:
                self.add_error(
                    "ending_time", ValidationError(_("Shift ends before it starts."))
                )

        return self.cleaned_data


@admin.register(models.Shift)
class ShiftAdmin(FormattedModelChoiceFieldAdminMixin, MembershipFilteredAdmin):
    form = ShiftAdminForm

    fk_label_formats = {
        "task": "{obj.name} ({obj.facility.name})",
        "workplace": "{obj.name} ({obj.facility.name})",
    }

    def get_queryset(self, request):
        qs = super(ShiftAdmin, self).get_queryset(request)
        qs = qs.annotate(volunteer_count=Count("helpers"))
        qs = qs.select_related("facility", "task", "workplace")
        qs = qs.prefetch_related("helpers", "helpers__user")
        return qs

    def get_volunteer_count(self, obj):
        return obj.volunteer_count

    get_volunteer_count.short_description = _("number of volunteers")
    get_volunteer_count.admin_order_field = "volunteer_count"

    def get_volunteer_names(self, obj):
        def _format_username(user):
            full_name = user.get_full_name()
            username = format_html("<strong>{}</strong>", user.username)

            if full_name:
                username = format_html("{} ({})", full_name, username)
            return format_html("<li>{}</li>", username)

        return format_html(
            "<ul>{}</ul>",
            mark_safe(
                "\n".join(
                    _format_username(volunteer.user) for volunteer in obj.helpers.all()
                )
            ),
        )

    get_volunteer_names.short_description = _("volunteers")
    get_volunteer_names.allow_tags = True

    list_display = (
        "task",
        "workplace",
        "facility",
        "starting_time",
        "ending_time",
        "members_only",
        "slots",
        "get_volunteer_count",
        "get_volunteer_names",
    )

    search_fields = (
        "id",
        "task__name",
    )
    list_filter = (
        ("facility", MembershipFieldListFilter),
        "members_only",
        "starting_time",
        "ending_time",
    )


@admin.register(models.ShiftHelper)
class ShiftHelperAdmin(MembershipFilteredAdmin):
    list_display = ("id", "user_account", "shift", "joined_shift_at")
    list_filter = ("joined_shift_at",)
    raw_id_fields = ("user_account", "shift")
