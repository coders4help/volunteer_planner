# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.models import UserAccount
from scheduler.models import Shift


class Organization(models.Model):
    # the name of the organization, ie. "Wilmersdorf hilft"
    name = models.CharField(max_length=256, verbose_name=_(u'name'))

    # a short description of the organization.
    # will be derived from description, if empty
    short_description = models.TextField(blank=True,
                                         verbose_name=_(u'short description'))

    # a description of the organization
    description = models.TextField(verbose_name=_(u'description'))

    # anything one needs to know on how to contact the facility
    contact_info = models.TextField(verbose_name=_(u'contact info'))

    # the orgs address
    address = models.TextField(verbose_name=_('address'))

    # users associated with this organization
    # ie. members, admins, admins
    members = models.ManyToManyField(UserAccount,
                                     through='organizations.OrganizationMembership')

    class Meta:
        verbose_name = _(u'organization')
        verbose_name_plural = _(u'organizations')
        ordering = ('name',)

    def __unicode__(self):
        return _(u"{name}").format(name=self.name)


class Facility(models.Model):
    # the organization running this facility
    organization = models.ForeignKey('organizations.Organization',
                                     verbose_name=_('organization'),
                                     related_name='facilities')

    # the name of the facility, ie. "Fehrbelliner Platz 4"
    name = models.CharField(max_length=256, verbose_name=_(u'name'))

    # a short description of the facility.
    # will be derived from description, if empty
    short_description = models.TextField(blank=True,
                                         verbose_name=_(u'short description'))

    # a description of the facility
    description = models.TextField(verbose_name=_(u'description'))

    # anything one needs to know on how to contact the facility
    contact_info = models.TextField(verbose_name=_(u'contact info'))

    # users associated with this facility
    # ie. members, admins, admins
    members = models.ManyToManyField(UserAccount,
                                     through='organizations.FacilityMembership')

    # the geographical location of the faciltiy
    place = models.ForeignKey("places.Place",
                              null=False,
                              related_name='facilities',
                              verbose_name=_('place'))

    # not all addresses need to have the western pattern of
    # street, postal code, city
    address = models.TextField(verbose_name=_('address'))

    # might be useful later, once we want to search by zip code
    zip_code = models.CharField(max_length=25,
                                blank=True,
                                verbose_name=_('postal code'))

    # coordinates for showing it on a map and a flag to switch it on
    show_on_map = models.BooleanField(default=True,
                                      verbose_name=_(
                                          'Show on map of all facilities'))
    latitude = models.CharField(max_length=30, blank=True,
                                verbose_name=_('latitude'))
    longitude = models.CharField(max_length=30, blank=True,
                                 verbose_name=_('longitude'))

    class Meta:
        verbose_name = _(u'facility')
        verbose_name_plural = _(u'facilities')
        ordering = ('organization', 'place', 'name',)

    @property
    def address_line(self):
        return ', '.join(
            filter(None, map(lambda s: s.strip(), self.address.splitlines())))

    # TODO: Could this be implemented in a more optimized way?
    @property
    def open_shifts(self):
        return Shift.open_shifts.filter(facility=self)

    def __unicode__(self):
        return _(u"{name}").format(name=self.name)


class Membership(models.Model):
    related_name = None

    class Roles:
        ADMIN, MANAGER, MEMBER = 0, 1, 2
        CHOICES = (
            (ADMIN, _(u'admin')),
            (MANAGER, _(u'manager')),
            (MEMBER, _(u'member')),
        )

    role = models.PositiveIntegerField(choices=Roles.CHOICES,
                                       default=Roles.MEMBER,
                                       verbose_name=_(u'role'))

    user_account = models.ForeignKey(UserAccount,
                                     verbose_name=_(u'user account'),
                                     related_name=related_name)

    class Meta:
        abstract = True


class OrganizationMembership(Membership):
    related_name = 'organizations'

    organization = models.ForeignKey(Organization,
                                     verbose_name=_(u'organization'),
                                     related_name='memberships',
                                     related_query_name='membership')

    class Meta:
        verbose_name = _(u'organization member')
        verbose_name_plural = _(u'organization members')
        ordering = ('organization', 'role', 'user_account')

    def __unicode__(self):
        return _(u"{username} at {organization_name} ({user_role})").format(
            username=self.user_account.user.username,
            organization_name=self.organization.name,
            user_role=self.role)


class FacilityMembership(Membership):
    related_name = 'facilities'

    facility = models.ForeignKey(Facility,
                                 verbose_name=_(u'facility'),
                                 related_name='memberships',
                                 related_query_name='membership'
                                 )

    class Meta:
        verbose_name = _(u'facility member')
        verbose_name_plural = _(u'facility members')
        ordering = ('facility', 'role', 'user_account')

    def __unicode__(self):
        return _(u"{username} at {facility_name} ({user_role})").format(
            username=self.user_account.user.username,
            facility_name=self.facility.name,
            user_role=self.role)


class Workplace(models.Model):
    # the facility the workplace belongs to
    facility = models.ForeignKey('Facility',
                                 verbose_name=_(u"facility"),
                                 related_name='workplaces'
                                 )

    # the name of the workplace, ie. "Küche"
    name = models.CharField(max_length=256, verbose_name=_(u'name'))

    # a description of the workplace
    description = models.TextField(blank=True, verbose_name=_(u'description'))

    class Meta:
        verbose_name = _(u'workplace')
        verbose_name_plural = _(u'workplaces')
        ordering = ('facility', 'name',)

    def __unicode__(self):
        return _(u"{name}").format(name=self.name)


class Task(models.Model):
    # the facility the task belongs to
    facility = models.ForeignKey('Facility',
                                 verbose_name=_(u"facility"),
                                 related_name='tasks')

    # the name of the task, ie. "Dolmetscher Farsi"
    name = models.CharField(max_length=256, verbose_name=_(u'name'))

    # a description of the task
    description = models.TextField(blank=True, verbose_name=_(u'description'))

    class Meta:
        verbose_name = _(u'task')
        verbose_name_plural = _(u'tasks')
        ordering = ('facility', 'name',)

    def __unicode__(self):
        return _(u"{name}").format(name=self.name)
