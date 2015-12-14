# coding: utf-8

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

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
