# -*- coding: utf-8 -*-
from collections import defaultdict
import itertools
from operator import itemgetter

from ckeditor.widgets import CKEditorWidget

from django.contrib import admin

from django.db.models import Q

from django.utils.encoding import smart_text

from . import models
from organizations.models import Facility

DEFAULT_FILTER_ROLES = (models.Membership.Roles.ADMIN,
                        models.Membership.Roles.MANAGER)


def get_memberships_by_role(membership_queryset):
    memberships_by_role = defaultdict(lambda: [])
    qs = membership_queryset.order_by('membership__role') \
        .values_list('membership__role', 'pk')
    for role, group in itertools.groupby(qs, itemgetter(0)):
        memberships_by_role[role] = map(itemgetter(1), group)
    return memberships_by_role


def get_cached_memberships(user):
    user_memberships = getattr(user, '__memberships', None)
    if not user_memberships:
        print 'cache miss. caching now...'
        user_memberships = {
            'facilities': get_memberships_by_role(user.account.facility_set),
            'organizations': get_memberships_by_role(
                user.account.organization_set),
        }
        setattr(user, '__memberships', user_memberships)
    return user_memberships


def filter_queryset_by_membership(qs, user,
                                  facility_filter_fk=None,
                                  organization_filter_fk=None,
                                  roles=DEFAULT_FILTER_ROLES):
    if facility_filter_fk and organization_filter_fk:
        raise Exception(
            'facility_filter_fk and organization_filter_fk are mutually exclusive.')

    if user.is_superuser:
        return qs

    user_memberships = get_cached_memberships(user)
    user_orgs = itertools.chain.from_iterable(
        user_memberships['organizations'][role] for role in roles)

    user_facilities = itertools.chain.from_iterable(
        user_memberships['facilities'][role] for role in roles)

    if qs.model == models.Organization:
        return qs.filter(pk__in=user_facilities)
    elif qs.model == models.Facility:
        return qs.filter(
            Q(pk__in=user_facilities) |
            Q(organization_id__in=user_orgs)
        )
    else:
        if facility_filter_fk is None and organization_filter_fk is None:
            facility_filter_fk = 'facility'

        if organization_filter_fk:
            return qs.filter(**{organization_filter_fk + '_id__in': user_orgs})
        else:
            return qs.filter(
                Q(**{facility_filter_fk + '_id__in': user_facilities}) |
                Q(**{facility_filter_fk + '__organization_id__in': user_orgs})
            )


class MembershipFilteredAdmin(admin.ModelAdmin):
    facility_filter_fk = 'facility'
    widgets = None

    def get_form(self, request, obj=None, **kwargs):
        form = super(MembershipFilteredAdmin, self).get_form(
            request, obj, widgets=self.widgets, **kwargs)

        if 'facility' in form.base_fields:
            facilities = Facility.objects.all()
            user_facilities = filter_queryset_by_membership(facilities,
                                                            request.user)
            if len(user_facilities) == 1:
                form.base_fields['facility'].initial = user_facilities.get()

        return form

    def get_queryset(self, request):
        qs = super(MembershipFilteredAdmin, self).get_queryset(request)
        return filter_queryset_by_membership(
            qs, user=request.user, facility_filter_fk=self.facility_filter_fk)

    def get_field_queryset(self, db, db_field, request):
        qs = super(MembershipFilteredAdmin, self).get_field_queryset(
            db, db_field, request)
        if db_field.rel.to in (models.Facility,
                               models.Organization,
                               models.Task,
                               models.Workplace):
            qs = qs or db_field.rel.to.objects.all()
            qs = filter_queryset_by_membership(qs, request.user)
        return qs


class MembershipFilteredTabularInline(admin.TabularInline):
    facility_filter_fk = 'facility'

    def get_queryset(self, request):
        qs = super(MembershipFilteredTabularInline, self).get_queryset(request)
        return filter_queryset_by_membership(
            qs, user=request.user, facility_filter_fk=self.facility_filter_fk)

    def get_field_queryset(self, db, db_field, request):
        qs = super(MembershipFilteredTabularInline, self).get_field_queryset(
            db, db_field, request)
        if db_field.rel.to in (models.Facility,
                               models.Organization,
                               models.Task,
                               models.Workplace):
            qs = qs or db_field.rel.to.objects.all()
            qs = filter_queryset_by_membership(qs, request.user)
        return qs


class MembershipFieldListFilter(admin.RelatedFieldListFilter):
    def field_choices(self, field, request, model_admin):
        qs = filter_queryset_by_membership(field.rel.to.objects.all(),
                                           request.user)
        return [(x._get_pk_val(), smart_text(x)) for x in qs]


@admin.register(models.Organization)
class OrganizationAdmin(MembershipFilteredAdmin):
    list_display = (
        'name',
        'short_description',
        'description',
        'contact_info',
        'address',
    )
    raw_id_fields = ('members',)
    search_fields = ('name',)
    widgets = {
        'short_description': CKEditorWidget(),
        'description': CKEditorWidget(),
        'contact_info': CKEditorWidget(),
    }


@admin.register(models.Facility)
class FacilityAdmin(MembershipFilteredAdmin):
    list_display = (
        'organization',
        'name',
        'short_description',
        'description',
        'contact_info',
        'place',
        'address',
        'zip_code',
        'show_on_map',
        'latitude',
        'longitude',
    )
    list_filter = (
        ('organization', MembershipFieldListFilter),
    )
    raw_id_fields = ('members',)
    search_fields = ('name',)
    radio_fields = {"organization": admin.VERTICAL}
    widgets = {
        'short_description': CKEditorWidget(),
        'description': CKEditorWidget(),
        'contact_info': CKEditorWidget(),
    }


@admin.register(models.OrganizationMembership)
class OrganizationMembershipAdmin(MembershipFilteredAdmin):
    list_display = (
        'user_account',
        'organization',
        'role',
    )
    list_filter = (
        ('organization', MembershipFieldListFilter),
    )
    raw_id_fields = ('user_account',)


@admin.register(models.FacilityMembership)
class FacilityMembershipAdmin(MembershipFilteredAdmin):
    list_display = (
        'role',
        'user_account',
        'facility'
    )
    list_filter = (
        ('facility', MembershipFieldListFilter),
    )
    raw_id_fields = ('user_account',)


@admin.register(models.Workplace)
class WorkplaceAdmin(MembershipFilteredAdmin):
    list_display = (
        'facility',
        'name',
        'description'
    )
    list_filter = (
        ('facility', MembershipFieldListFilter),
    )
    search_fields = ('name',)
    list_select_related = True
    radio_fields = {"facility": admin.VERTICAL}
    widgets = {
        'description': CKEditorWidget(),
    }


@admin.register(models.Task)
class TaskAdmin(MembershipFilteredAdmin):
    list_display = (
        'facility',
        'name',
        'description'
    )
    list_filter = (
        ('facility', MembershipFieldListFilter),
    )
    search_fields = ('name',)
    list_select_related = True
    radio_fields = {"facility": admin.VERTICAL}
    widgets = {
        'description': CKEditorWidget(),
    }
