# coding: utf-8
import logging

from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from registration.models import RegistrationProfile

from .models import UserAccount

logger = logging.getLogger(__name__)


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    def get_user_first_name(self, obj):
        return obj.user.first_name

    get_user_first_name.short_description = _("first name")
    get_user_first_name.admin_order_field = "user__first_name"

    def get_user_last_name(self, obj):
        return obj.user.last_name

    get_user_last_name.short_description = _("first name")
    get_user_last_name.admin_order_field = "user__last_name"

    def get_user_email(self, obj):
        return obj.user.email

    get_user_email.short_description = _("email")
    get_user_email.admin_order_field = "user__email"

    def user_is_active(self, obj):
        return obj.user.is_active

    user_is_active.boolean = True
    user_is_active.short_description = _("active")
    user_is_active.admin_order_field = "user__is_active"

    def get_user_join_date(self, obj):
        return obj.user.date_joined

    get_user_join_date.short_description = _("date joined")
    get_user_join_date.admin_order_field = "user__date_joined"

    def get_user_last_login(self, obj):
        return obj.user.last_login

    get_user_last_login.short_description = _("last login")
    get_user_last_login.admin_user_field = "user"

    date_hierarchy = "user__date_joined"
    actions = ["resend_activation_mail"]

    list_display = (
        "user",
        "get_user_email",
        "get_user_first_name",
        "get_user_last_name",
        "user_is_active",
        "get_user_join_date",
        "get_user_last_login",
    )
    raw_id_fields = ("user",)
    search_fields = (
        "user__username",
        "user__email",
        "user__last_name",
        "user__first_name",
    )

    list_filter = (
        "user__is_active",
        "user__is_staff",
        "user__last_login",
    )

    def resend_activation_mail(self, request, queryset):
        site = get_current_site(request)
        for profile in queryset:
            user = profile.user
            logger.info(
                f'Attempt to re-send activation mail for "{user.username}" <{user.email}>'
            )
            RegistrationProfile.objects.resend_activation_mail(
                user.email, site, request
    )


from django.contrib.sessions.models import Session
from django.contrib.auth.models import User


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        _session_data = ""
        decoded = obj.get_decoded()
        for key in sorted(decoded):
            _session_data += "<b>" + key + "</b>: " + decoded.get(key)
            if "_auth_user_id" == key:
                try:
                    user = User.objects.get(id=decoded.get(key))
                    _session_data += " (" + user.username + ")"
                except Exception as e:
                    pass
            _session_data += "<br/>"
        return format_html(_session_data)

    _session_data.allow_tags = True
    list_display = ["session_key", "_session_data", "expire_date"]
    readonly_fields = ["_session_data"]
    exclude = ["session_data"]
    date_hierarchy = "expire_date"
    ordering = ["expire_date"]
