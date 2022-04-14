# coding: utf-8

import json
import logging
from abc import ABC
from datetime import date

from django.contrib import messages
from django.contrib.admin.models import DELETION, LogEntry
from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, F, Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, FormView, TemplateView

from accounts.models import UserAccount
from organizations.models import Facility, FacilityMembership
from organizations.templatetags.memberships import (
    is_facility_manager,
    is_facility_member,
    is_membership_pending,
)
from organizations.views import get_facility_details
from scheduler.models import Shift, ShiftHelper, ShiftMessageToHelpers
from volunteer_planner.utils import LoginRequiredMixin
from .forms import RegisterForShiftForm, ShiftMessageToHelpersModelForm

logger = logging.getLogger(__name__)


def get_open_shifts():
    shifts = Shift.open_shifts.all()
    shifts = shifts.select_related(
        "facility",
        "facility__place",
        "facility__place__area",
        "facility__place__area__region",
        "facility__place__area__region__country",
    )

    shifts = shifts.order_by(
        "facility__place__area__region__country",
        "facility__place__area__region",
        "facility__place__area",
        "facility__place",
        "facility",
        "starting_time",
    )
    return shifts


class JoinLeaveFormView(ABC, FormView):
    """
    Abstract base class for FormViews, that should be used to sign up for
    or drop out from a shift.
    """

    def form_invalid(self, form):
        messages.warning(self.request, _("The submitted data was invalid."))
        return super().form_invalid(form)

    def form_valid(self, form):
        user = self.request.user
        try:
            user_account = UserAccount.objects.get(user=user)
        except UserAccount.DoesNotExist:
            messages.warning(self.request, _("User account does not exist."))
            return super().form_valid(form)

        shift_to_join = form.cleaned_data.get("join_shift")
        shift_to_leave = form.cleaned_data.get("leave_shift")

        if shift_to_join:

            if shift_to_join.members_only and not is_facility_member(
                self.request.user, shift_to_join.facility
            ):

                if not is_membership_pending(user, shift_to_join.facility):
                    mbs, created = FacilityMembership.objects.get_or_create(
                        user_account=user_account,
                        facility=shift_to_join.facility,
                        defaults=dict(
                            status=FacilityMembership.Status.PENDING,
                            role=FacilityMembership.Roles.MEMBER,
                        ),
                    )
                    if created:
                        messages.success(
                            self.request, _("A membership request has been sent.")
                        )
                return super().form_valid(form)

            hard_conflicts, graced_conflicts = ShiftHelper.objects.conflicting(
                shift_to_join, user_account=user_account
            )
            hard_conflicted_shifts = [
                shift_helper.shift for shift_helper in hard_conflicts
            ]

            soft_conflicted_shifts = [
                shift_helper.shift for shift_helper in graced_conflicts
            ]

            if hard_conflicted_shifts:
                error_message = _(
                    "We can't add you to this shift because you've already "
                    "agreed to other shifts at the same time:"
                )
                message_list = "<ul>{}</ul>".format(
                    "\n".join(
                        [
                            "<li>{}</li>".format(conflict)
                            for conflict in hard_conflicted_shifts
                        ]
                    )
                )
                messages.warning(
                    self.request,
                    mark_safe("{}<br/>{}".format(error_message, message_list)),
                )
            elif shift_to_join.slots - shift_to_join.volunteer_count <= 0:
                error_message = _(
                    "We can't add you to this shift because there are no more "
                    "slots left."
                )
                messages.warning(self.request, error_message)
            else:
                shift_helper, created = ShiftHelper.objects.get_or_create(
                    user_account=user_account, shift=shift_to_join
                )
                if created:
                    messages.success(
                        self.request, _("You were successfully added to this shift.")
                    )

                    if soft_conflicted_shifts:
                        warning_message = _(
                            "The shift you joined overlaps with other shifts "
                            "you already joined. Please check for "
                            "conflicts:"
                        )
                        message_list = "<ul>{}</ul>".format(
                            "\n".join(
                                [
                                    "<li>{}</li>".format(conflict)
                                    for conflict in soft_conflicted_shifts
                                ]
                            )
                        )
                        messages.warning(
                            self.request,
                            mark_safe(
                                "{}<br/>{}".format(warning_message, message_list)
                            ),
                        )
                else:
                    messages.warning(
                        self.request,
                        _(
                            "You already signed up for this shift at {date_time}."
                        ).format(date_time=shift_helper.joined_shift_at),
                    )

        elif shift_to_leave:
            try:
                sh = ShiftHelper.objects.get(
                    user_account=user_account, shift=shift_to_leave
                )
                LogEntry.objects.log_action(
                    user_id=user.id,
                    content_type_id=ContentType.objects.get_for_model(ShiftHelper).id,
                    object_id=sh.id,
                    object_repr='User "{user}" @ shift "{shift}"'.format(
                        user=user, shift=shift_to_leave
                    ),
                    action_flag=DELETION,
                    change_message="Initially joined at {}".format(
                        sh.joined_shift_at.isoformat()
                    ),
                )
                sh.delete()
            except ShiftHelper.DoesNotExist:
                # just catch the exception,
                # user seems not to have signed up for this shift
                pass
            messages.success(self.request, _("You successfully left this shift."))

        return super().form_valid(form)


class HelpDesk(LoginRequiredMixin, TemplateView):
    """
    Facility overview. First view that a volunteer gets redirected to when they log in.
    """

    template_name = "helpdesk.html"

    def get_context_data(self, **kwargs):
        context = super(HelpDesk, self).get_context_data(**kwargs)

        facilities = (
            Facility.objects.with_open_shifts()
            .select_related(
                "organization",
                "place",
                "place__area",
                "place__area__region",
                "place__area__region__country",
            )
            .prefetch_related(
                Prefetch(
                    "shift_set", queryset=Shift.open_shifts.all(), to_attr="open_shifts"
                ),
                "news_entries",
            )
        )

        facility_list = []
        used_places = set()
        used_countries = set()

        for facility in facilities:
            used_places.add(facility.place.area)
            facility_list.append(get_facility_details(facility))
            used_countries.add(facility.place.area.region.country)

        context["areas_json"] = json.dumps(
            [
                {"slug": area.slug, "name": area.name}
                for area in sorted(used_places, key=lambda p: p.name)
            ]
        )
        context["country_json"] = json.dumps(
            [
                {"slug": country.slug, "name": country.name}
                for country in sorted(used_countries, key=lambda p: p.name)
            ]
        )

        context["facility_json"] = json.dumps(facility_list, cls=DjangoJSONEncoder)
        return context


class GeographicHelpdeskView(DetailView):
    template_name = "geographic_helpdesk.html"
    context_object_name = "geographical_unit"

    @staticmethod
    def make_breadcrumps_dict(country, region=None, area=None, place=None):

        result = dict(
            country=country,
            flattened=[
                country,
            ],
        )

        for k, v in zip(("region", "area", "place"), (region, area, place)):
            if v:
                result[k] = v
                result["flattened"].append(v)

        return result

    def get_queryset(self):
        return (
            super(GeographicHelpdeskView, self)
            .get_queryset()
            .select_related(*self.model.get_select_related_list())
        )

    def get_context_data(self, **kwargs):
        context = super(GeographicHelpdeskView, self).get_context_data(**kwargs)
        place = self.object
        context["breadcrumps"] = self.make_breadcrumps_dict(*place.breadcrumps)
        context["shifts"] = get_open_shifts().by_geography(place)
        return context


class ShiftDetailView(LoginRequiredMixin, JoinLeaveFormView):
    template_name = "shift_details.html"
    form_class = RegisterForShiftForm

    def get_context_data(self, **kwargs):
        context = super(ShiftDetailView, self).get_context_data(**kwargs)

        try:
            schedule_date = date(
                int(self.kwargs["year"]),
                int(self.kwargs["month"]),
                int(self.kwargs["day"]),
            )
        except ValueError:
            raise Http404(
                "Invalid date "
                f"{self.kwargs['year']}/{self.kwargs['month']}/{self.kwargs['day']}"
            )

        try:
            shift = (
                Shift.objects.on_shiftdate(schedule_date)
                .annotate(volunteer_count=Count("helpers"))
                .get(
                    facility__slug=self.kwargs["facility_slug"],
                    id=self.kwargs["shift_id"],
                )
            )
        except Shift.DoesNotExist:
            raise Http404()
        context["shift"] = shift
        return context

    def get_success_url(self):
        """
        Redirect to the same page.
        """
        return reverse("shift_details", kwargs=self.kwargs)


class PlannerView(LoginRequiredMixin, JoinLeaveFormView):
    """
    View that gets shown to volunteers when they browse a specific day.
    It'll show all the available shifts, and they can add and remove
    themselves from shifts.
    """

    template_name = "helpdesk_single.html"
    form_class = RegisterForShiftForm

    def get_context_data(self, **kwargs):

        context = super(PlannerView, self).get_context_data(**kwargs)
        try:
            schedule_date = date(
                int(self.kwargs["year"]),
                int(self.kwargs["month"]),
                int(self.kwargs["day"]),
            )
        except ValueError:
            raise Http404(
                "Invalid date "
                f"{self.kwargs['year']}/{self.kwargs['month']}/{self.kwargs['day']}"
            )

        facility = get_object_or_404(Facility, slug=self.kwargs["facility_slug"])

        shifts = (
            Shift.objects.filter(facility=facility)
            .on_shiftdate(schedule_date)
            .annotate(volunteer_count=Count("helpers"))
            .order_by(
                "facility",
                F("task__priority").desc(nulls_last=True),
                F("workplace__priority").desc(nulls_last=True),
                "task__name",
                "workplace__name",
                "ending_time",
            )
            .select_related("task", "workplace", "facility")
            .prefetch_related("helpers", "helpers__user")
        )

        context["shifts"] = shifts
        context["facility"] = facility
        context["schedule_date"] = schedule_date
        context["shift_message_to_helpers_form"] = ShiftMessageToHelpersModelForm
        return context

    def get_success_url(self):
        """
        Redirect to the same page.
        """
        return reverse("planner_by_facility", kwargs=self.kwargs)


class SendMessageToShiftHelpers(LoginRequiredMixin, FormView):
    """
    View processes the sending of an email to all shift helpers.
    """

    template_name = "helpdesk_single.html"
    form_class = ShiftMessageToHelpersModelForm

    def form_invalid(self, form):
        messages.warning(self.request, _("The submitted data was invalid."))
        return super(SendMessageToShiftHelpers, self).form_invalid(form)

    def form_valid(self, form):
        user = self.request.user
        try:
            user_account = UserAccount.objects.get(user=user)
        except UserAccount.DoesNotExist:
            messages.warning(self.request, _("User account does not exist."))
            return super(SendMessageToShiftHelpers, self).form_valid(form)

        shift = form.cleaned_data.get("shift")
        if not is_facility_manager(user_account.user, shift.facility):
            messages.warning(
                self.request, _("You have no permissions to send e-mails!")
            )
            return super(SendMessageToShiftHelpers, self).form_valid(form)

        shift_message = ShiftMessageToHelpers.objects.create(
            message=form.cleaned_data.get("message"),
            shift=shift,
            sender=user_account,
        )

        # also send a copy of the message to shift manager
        shift_message.recipients.add(user_account)
        for helper in shift.helpers.exclude(user__email=""):
            if helper.user.email:
                shift_message.recipients.add(helper)
        shift_message.save()

        messages.info(self.request, _("E-mail has been sent."))
        return super(SendMessageToShiftHelpers, self).form_valid(form)

    def get_success_url(self):
        """redirect to referer site"""
        try:
            return self.request.META["HTTP_REFERER"]
        except KeyError:
            return reverse("helpdesk")
