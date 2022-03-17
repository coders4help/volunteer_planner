# coding: utf-8
import logging

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from registration.admin import RegistrationAdmin
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

    list_display = (
        "user",
        "get_user_email",
        "get_user_first_name",
        "get_user_last_name",
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
    )


class RegistrationProfileAdmin(RegistrationAdmin):
    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = _("email")
    user_email.admin_order_field = "user__email"

    def user_date_joined(self, obj):
        return obj.user.date_joined

    user_date_joined.short_description = _("date joined")
    user_date_joined.admin_order_field = "user__date_joined"

    def user_last_login(self, obj):
        return obj.user.last_login

    user_last_login.short_description = _("last login")
    user_last_login.admin_order_field = "user__last_login"

    date_hierarchy = "user__date_joined"

    list_display = (
        "user",
        "user_email",
        "activated",
        "activation_key_expired",
        "user_date_joined",
        "user_last_login",
    )

    list_filter = (
        "user__is_active",
        "user__is_staff",
        "user__last_login",
    )


admin.site.unregister(RegistrationProfile)
admin.site.register(RegistrationProfile, RegistrationProfileAdmin)


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
