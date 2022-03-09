# coding: utf-8

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import UserAccount


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):

    def get_user_first_name(self, obj):
        return obj.user.first_name

    get_user_first_name.short_description = _(u'first name')
    get_user_first_name.admin_order_field = 'user__first_name'

    def get_user_last_name(self, obj):
        return obj.user.last_name

    get_user_last_name.short_description = _(u'first name')
    get_user_last_name.admin_order_field = 'user__last_name'

    def get_user_email(self, obj):
        return obj.user.email

    get_user_email.short_description = _(u'email')
    get_user_email.admin_order_field = 'user__email'

    list_display = (
        'user',
        'get_user_email',
        'get_user_first_name',
        'get_user_last_name'
    )
    raw_id_fields = ('user',)
    search_fields = (
        'user__username',
        'user__email',
        'user__last_name',
        'user__first_name'
    )

    list_filter = (
        'user__is_active',
        'user__is_staff',
    )


from django.contrib.sessions.models import Session
from django.contrib.auth.models import User


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        _session_data = u''
        decoded = obj.get_decoded()
        for key in sorted(decoded):
            _session_data += u'<b>' + key + u'</b>: ' + decoded.get(key)
            if '_auth_user_id' == key:
                try:
                    user = User.objects.get(id=decoded.get(key))
                    _session_data += u' (' + user.username + ')'
                except Exception as e:
                    pass
            _session_data += u'<br/>'
        return format_html(_session_data)

    _session_data.allow_tags = True
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    exclude = ['session_data']
    date_hierarchy = 'expire_date'
    ordering = ['expire_date']
