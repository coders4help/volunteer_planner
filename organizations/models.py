# coding: utf-8
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from accounts.models import UserAccount
from scheduler.models import Shift
from .managers import FacilityManager


class Membership(models.Model):
    """ Abstract base class for memberships of users.

    Defines three choices lists: JoinMode, Status and Roles.

    JoinMode contains Invitation only, Approval by admin and Anyone.
    Status contains Rejected, Peding and Approved.
    Roles contains Admin, Manager and Member.

    Has fields: role, status and user_account.
    Role makes use of choices list Role, status of status.
    user_account is a foreign-key to User-account.
    """

    related_name = None

    class JoinMode:
        INVITATION_ONLY, APPROVAL_BY_ADMIN, ANYONE = 0, 1, 2
        CHOICES = (
            (INVITATION_ONLY, _(u'by invitation')),
            (APPROVAL_BY_ADMIN, _(u'anyone (approved by manager)')),
            (ANYONE, _(u'anyone')),
        )

    class Status:
        REJECTED, PENDING, APPROVED = 0, 1, 2
        CHOICES = (
            (REJECTED, _(u'rejected')),
            (PENDING, _(u'pending')),
            (APPROVED, _(u'approved')),
        )

    class Roles:
        ADMIN, MANAGER, MEMBER = 0, 1, 2
        CHOICES = (
            (ADMIN, _(u'admin')),
            (MANAGER, _(u'manager')),
            (MEMBER, _(u'member')),
        )

    role = models.PositiveSmallIntegerField(choices=Roles.CHOICES,
                                            default=Roles.MEMBER,
                                            verbose_name=_(u'role'))

    status = models.PositiveSmallIntegerField(choices=Status.CHOICES,
                                              default=Status.APPROVED,
                                              verbose_name=_(u'status'))

    user_account = models.ForeignKey(UserAccount,
                                     models.CASCADE,
                                     verbose_name=_(u'user account'),
                                     related_name=related_name)

    class Meta:
        abstract = True


class Organization(models.Model):
    """ Organizations organize the work at the facilities.

    Has fields: name, short description, description, contact info, address,
        members (many2many relationship through OrganizationMembership),
        slug and join mode (choices list join_mode of abstract class Membership).
    """
    # the name of the organization, ie. "Wilmersdorf hilft"
    name = models.CharField(max_length=256, verbose_name=_(u'name'))

    # a description of the organization
    description = models.TextField(verbose_name=_(u'description'))

    # anything one needs to know on how to contact the facility
    contact_info = models.TextField(verbose_name=_(u'contact info'))

    # the orgs address
    address = models.TextField(verbose_name=_('address'))

    # users associated with this organization
    # ie. members, admins, admins
    members = models.ManyToManyField(
        UserAccount,
        through='organizations.OrganizationMembership'
    )

    slug = models.SlugField(max_length=80, verbose_name=_(u'slug'))

    join_mode = models.PositiveSmallIntegerField(
        choices=Membership.JoinMode.CHOICES,
        default=Membership.JoinMode.INVITATION_ONLY,
        verbose_name=_(u'join mode'),
        help_text=_(u'Who can join this organization?'))

    class Meta:
        verbose_name = _(u'organization')
        verbose_name_plural = _(u'organizations')
        ordering = ('name',)

    def __unicode__(self):
        return f"{self.name}"

    def __str__(self):
        return self.__unicode__()

    def get_absolute_url(self):
        return reverse('organization',
                       args=[self.slug])


class Facility(models.Model):
    """ Facilities are the places where the voluntary work is done,
    mainly where refugees live or administrative places.

    Has fields: organization (org. that is running the fac.,foreign-key to organization),
        name, short description, description, contact info,
        members (User account many2many Facility),
        place, adress, zip-code, show_on_map, latitude, longitude, slug,
        timeline enabled and join mode.
    """

    class TimelineViewMode:
        DISABLED, COLLAPSED, ENABLED = 0, 1, 2
        CHOICES = (
            (DISABLED, _(u'disabled')),
            (COLLAPSED, _(u'enabled (collapsed)')),
            (ENABLED, _(u'enabled')),
        )

    # the organization running this facility
    organization = models.ForeignKey('organizations.Organization',
                                     models.CASCADE,
                                     verbose_name=_('organization'),
                                     related_name='facilities')

    # the name of the facility, ie. "Fehrbelliner Platz 4"
    name = models.CharField(max_length=256, verbose_name=_(u'name'))

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
                              models.CASCADE,
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

    slug = models.SlugField(max_length=80, verbose_name=_(u'slug'))

    timeline_enabled = models.PositiveSmallIntegerField(
        choices=TimelineViewMode.CHOICES,
        default=TimelineViewMode.COLLAPSED,
        verbose_name=_(u'timeline'))

    join_mode = models.PositiveSmallIntegerField(
        choices=Membership.JoinMode.CHOICES,
        default=Membership.JoinMode.INVITATION_ONLY,
        verbose_name=_(u'join mode'),
        help_text=_(u'Who can join this facility?'))

    objects = FacilityManager()

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
        return f"{self.name}"

    def __str__(self):
        return self.__unicode__()

    def get_absolute_url(self):
        return reverse('facility',
                       args=[self.organization.slug, self.slug])


class OrganizationMembership(Membership):
    """ Users membership of organizations.

    Inherits from Membership which has a foreign key to user account.
    Has a foreign key field to Organization,
        so this is the many2many model of the m2m relationship user accounts/organization.
    """

    related_name = 'organizations'

    organization = models.ForeignKey(Organization,
                                     models.CASCADE,
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

    def __str__(self):
        return self.__unicode__()


class FacilityMembership(Membership):
    """ Users membership of facilities.

    Inherits from Membership which has a foreign key to user account.
    Has a foreign key field to Facility,
        so this is the many2many model of the m2m relationship user accounts/facility.
    """
    related_name = 'facilities'

    facility = models.ForeignKey(Facility,
                                 models.CASCADE,
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

    def __str__(self):
        return self.__unicode__()


class Workplace(models.Model):
    """ Workplaces are places at the facilities, where work is done,
        eg. kitchen or clothing store.

    Has foreign key to facility, name and description.
    """
    # the facility the workplace belongs to
    facility = models.ForeignKey('Facility',
                                 models.CASCADE,
                                 verbose_name=_(u"facility"),
                                 related_name='workplaces'
                                 )

    # the name of the workplace, ie. "Küche"
    name = models.CharField(max_length=256, verbose_name=_(u'name'))

    # a description of the workplace
    description = models.TextField(blank=True, verbose_name=_(u'description'))

    priority = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("priority"))

    class Meta:
        verbose_name = _(u'workplace')
        verbose_name_plural = _(u'workplaces')
        ordering = ('facility', '-priority', 'name',)

    def __unicode__(self):
        return f"{self.name}"

    def __str__(self):
        return self.__unicode__()


class Task(models.Model):
    """ Tasks that are to be done at the facilities.

    Has foreign key to facility, name and description.
    """
    # the facility the task belongs to
    facility = models.ForeignKey('Facility',
                                 models.CASCADE,
                                 verbose_name=_(u"facility"),
                                 related_name='tasks')

    # the name of the task, ie. "Dolmetscher Farsi"
    name = models.CharField(max_length=256, verbose_name=_(u'name'))

    # a description of the task
    description = models.TextField(blank=True, verbose_name=_(u'description'))

    priority = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("priority"))

    class Meta:
        verbose_name = _(u'task')
        verbose_name_plural = _(u'tasks')
        ordering = ('facility', '-priority', 'name',)

    def __unicode__(self):
        return f"{self.name}"

    def __str__(self):
        return self.__unicode__()
