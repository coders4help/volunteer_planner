# -*- coding: utf-8 -*-
from collections import defaultdict
import itertools
from operator import itemgetter

from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.db.models import Q, Count
from django.template.defaultfilters import striptags
from django.utils.encoding import smart_str as smart_text

from django.utils.translation import gettext_lazy as _

from . import models
from scheduler import models as shiftmodels
from organizations.models import Membership

DEFAULT_FILTER_ROLES = (models.Membership.Roles.ADMIN,
                        models.Membership.Roles.MANAGER)


def get_memberships_by_role(membership_queryset):
    memberships_by_role = defaultdict(lambda: [])
    membership_queryset = membership_queryset.filter(
        membership__status__gte=Membership.Status.APPROVED
    )
    qs = membership_queryset.order_by('membership__role') \
        .values_list('membership__role', 'pk')
    for role, group in itertools.groupby(qs, itemgetter(0)):
        memberships_by_role[role] = list(map(itemgetter(1), group))
    return memberships_by_role


def get_cached_memberships(user, roles=DEFAULT_FILTER_ROLES):
    user_memberships = getattr(user, '__memberships', None)
    if not user_memberships:
        user_memberships = {
            'facilities': get_memberships_by_role(user.account.facility_set),
            'organizations': get_memberships_by_role(
                user.account.organization_set),
        }
        setattr(user, '__memberships', user_memberships)

    user_orgs = list(itertools.chain.from_iterable(
        user_memberships['organizations'][role] for role in roles))

    user_facilities = list(itertools.chain.from_iterable(
        user_memberships['facilities'][role] for role in roles))

    return user_orgs, user_facilities


def filter_queryset_by_membership(qs, user,
                                  facility_filter_fk=None,
                                  organization_filter_fk=None,
                                  roles=DEFAULT_FILTER_ROLES,
                                  skip_superuser=True):
    if facility_filter_fk and organization_filter_fk:
        raise Exception(
            'facility_filter_fk and organization_filter_fk are mutually exclusive.')

    if skip_superuser and user.is_superuser:
        return qs

    user_orgs, user_facilities = get_cached_memberships(user, roles)

    if qs.model == models.Organization:
        qs = qs.filter(pk__in=user_orgs)
    elif qs.model == models.Facility:
        qs = qs.filter(
            Q(pk__in=user_facilities) |
            Q(organization_id__in=user_orgs)
        )
    else:
        if facility_filter_fk is None and organization_filter_fk is None:
            facility_filter_fk = 'facility'

        if qs.model == models.OrganizationMembership:
            if organization_filter_fk:
                qs = qs.filter(**{organization_filter_fk + '_id__in': user_orgs})
        elif qs.model == shiftmodels.ShiftHelper:
            qs = qs.filter(
                Q(**{'shift__' + facility_filter_fk + '_id__in': user_facilities}) |
                Q(**{'shift__' + facility_filter_fk + '__organization_id__in': user_orgs})
            )
        else:
            if organization_filter_fk:
                qs = qs.filter(**{organization_filter_fk + '_id__in': user_orgs})
            elif facility_filter_fk:
                qs = qs.filter(
                    Q(**{facility_filter_fk + '_id__in': user_facilities}) |
                    Q(**{facility_filter_fk + '__organization_id__in': user_orgs})
                )
    return qs


class MembershipFilteredAdmin(admin.ModelAdmin):
    facility_filter_fk = 'facility'
    organization_filter_fk = 'organization'
    widgets = None

    def get_readonly_fields(self, request, obj=None):
        readonly = super(MembershipFilteredAdmin, self).get_readonly_fields(
            request=request, obj=obj)
        if request.user.is_superuser:
            return readonly
        else:
            if not ('facility' in readonly and 'organization' in readonly):
                user_orgs, user_facilities = get_cached_memberships(
                    request.user)
                if len(user_facilities) <= 1 and hasattr(obj, 'facility') \
                        and 'facility' not in readonly:
                    readonly += ('facility',)
                if len(user_orgs) <= 1 and hasattr(obj, 'organization') \
                        and 'organization' not in readonly:
                    readonly += ('organization',)
        if obj and hasattr(obj, "user_account"):
            readonly += ('user_account',)
        return readonly

    # def get_list_display(self, request):
    #     list_display = list(
    #         super(MembershipFilteredAdmin, self).get_list_display(request))
    #     if request.user.is_superuser:
    #         return list_display
    #     if 'facility' in list_display or 'organization' in list_display:
    #         user_orgs, user_facilities = get_cached_memberships(request.user)
    #         if len(user_facilities) <= 1 and 'facility' in list_display:
    #             list_display.remove('facility')
    #         if len(user_orgs) <= 1 and 'organization' in list_display:
    #             list_display.remove('organization')
    #     return list_display

    def get_list_display_links(self, request, list_display):
        list_display_links = list(
            super(MembershipFilteredAdmin, self).get_list_display_links(request,
                                                                        list_display))
        return list(filter(lambda i: i in list_display, list_display_links))

    def get_edit_link(self, obj):
        return _(u'edit')

    get_edit_link.short_description = _(u'edit')

    def get_form(self, request, obj=None, **kwargs):
        form = super(MembershipFilteredAdmin, self).get_form(
            request, obj, widgets=self.widgets, **kwargs)

        if 'facility' in form.base_fields:
            facilities = models.Facility.objects.all()
            user_facilities = filter_queryset_by_membership(facilities,
                                                            request.user)
            if len(user_facilities) == 1:
                form.base_fields['facility'].initial = user_facilities.get()

        return form

    def get_queryset(self, request):
        qs = super(MembershipFilteredAdmin, self).get_queryset(request)
        fac_filter = self.facility_filter_fk
        org_filter = None
        if qs.model.__name__.startswith('Organization'):
            fac_filter = None
            org_filter = self.organization_filter_fk
        return filter_queryset_by_membership(
            qs, user=request.user, facility_filter_fk=fac_filter, organization_filter_fk=org_filter)

    def get_field_queryset(self, db, db_field, request):
        qs = super(MembershipFilteredAdmin, self).get_field_queryset(
            db, db_field, request)
        if db_field.remote_field.model in (models.Facility,
                               models.Organization,
                               models.Task,
                               models.Workplace):
            qs = qs or db_field.remote_field.model.objects.all()
            qs = filter_queryset_by_membership(qs, request.user)
        return qs


class MembershipFilteredTabularInline(admin.TabularInline):
    facility_filter_fk = 'facility'
    widgets = None

    def get_formset(self, request, obj=None, **kwargs):
        return super(MembershipFilteredTabularInline, self).get_formset(
            request, obj, widgets=self.widgets, **kwargs)

    def get_queryset(self, request):
        qs = super(MembershipFilteredTabularInline, self).get_queryset(request)
        return filter_queryset_by_membership(
            qs, user=request.user, facility_filter_fk=self.facility_filter_fk)

    def get_field_queryset(self, db, db_field, request):
        qs = super(MembershipFilteredTabularInline, self).get_field_queryset(
            db, db_field, request)
        if db_field.remote_field.model in (models.Facility,
                               models.Organization,
                               models.Task,
                               models.Workplace):
            qs = qs or db_field.remote_field.model.objects.all()
            qs = filter_queryset_by_membership(qs, request.user)
        return qs


class MembershipFieldListFilter(admin.RelatedFieldListFilter):
    def field_choices(self, field, request, model_admin):
        query = field.remote_field.model.objects.all()
        query = query.annotate(usage_count=Count(field.related_query_name()))
        query = query.exclude(usage_count=0)
        qs = filter_queryset_by_membership(query, request.user)
        return [(x._get_pk_val(), smart_text(x)) for x in qs]


@admin.register(models.Organization)
class OrganizationAdmin(MembershipFilteredAdmin):

    def get_description(self, obj):
        return striptags(obj.description)

    get_description.short_description = _(u'description')
    get_description.allow_tags = True

    def get_contact_info(self, obj):
        return striptags(obj.contact_info)

    get_contact_info.short_description = _(u'contact info')
    get_contact_info.allow_tags = True

    list_display = (
        'name',
        'get_description',
        'contact_info',
        'address',
    )
    raw_id_fields = ('members',)
    search_fields = ('name',)
    widgets = {
        'description': CKEditorWidget(),
        'contact_info': CKEditorWidget(),
    }
    prepopulated_fields = {'slug': ['name']}


@admin.register(models.Facility)
class FacilityAdmin(MembershipFilteredAdmin):

    def get_description(self, obj):
        return striptags(obj.description)

    get_description.short_description = _(u'description')
    get_description.allow_tags = True

    def get_contact_info(self, obj):
        return striptags(obj.contact_info)

    get_contact_info.short_description = _(u'contact info')
    get_contact_info.allow_tags = True

    list_display = (
        'name',
        'organization',
        'get_description',
        'get_contact_info',
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
    widgets = {
        'description': CKEditorWidget(),
        'contact_info': CKEditorWidget(),
    }
    prepopulated_fields = {'slug': ['name']}


@admin.register(models.OrganizationMembership)
class OrganizationMembershipAdmin(MembershipFilteredAdmin):
    list_display = (
        'user_account',
        'organization',
        'role',
        'status',
    )
    list_filter = (
        ('organization', MembershipFieldListFilter),
        'status',
    )
    raw_id_fields = ('user_account',)


@admin.register(models.FacilityMembership)
class FacilityMembershipAdmin(MembershipFilteredAdmin):
    list_display = (
        'user_account',
        'facility',
        'role',
        'status',
    )
    list_filter = (
        ('facility', MembershipFieldListFilter),
        'status',
    )
    raw_id_fields = ('user_account',)


@admin.register(models.Workplace)
class WorkplaceAdmin(MembershipFilteredAdmin):
    def get_description(self, obj):
        return striptags(obj.description)

    get_description.short_description = _(u'description')
    get_description.allow_tags = True

    list_display = (
        'name',
        'facility',
        'priority',
        'get_description'
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
    def get_description(self, obj):
        return striptags(obj.description)

    get_description.short_description = _(u'description')
    get_description.allow_tags = True

    list_display = (
        'name',
        'facility',
        'priority',
        'get_description'
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


