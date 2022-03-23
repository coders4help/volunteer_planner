# coding: utf-8

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class BreadcrumpablePlaceManager(models.Manager):

    def get_queryset(self):
        return super(BreadcrumpablePlaceManager,
                     self).get_queryset().select_related(
            *self.model.get_select_related_list())


class BreadcrumpablePlaceModel(models.Model):
    PARENT_MODEL = None
    PARENT_FIELD = None

    name = models.CharField(max_length=50, unique=True, verbose_name=_('name'))
    slug = models.SlugField(verbose_name=_(u'slug'))

    objects = BreadcrumpablePlaceManager()

    class Meta:
        abstract = True

    @property
    def parent(self):
        return None

    @property
    def breadcrumps(self):
        return self.parent and self.parent.breadcrumps + [self, ] or [self, ]

    @classmethod
    def get_select_related_list(cls, chain=None):
        select_related = []
        if cls.PARENT_FIELD:
            if chain:
                related = '{}__{}'.format(chain, cls.PARENT_FIELD)
            else:
                related = cls.PARENT_FIELD
            select_related.append(related)
            select_related += cls.PARENT_MODEL.get_select_related_list(related)
        return select_related

    def get_detail_view_name(self):
        detail_view_name = getattr(self, 'DETAIL_VIEW_NAME', None)
        return detail_view_name or u'{}-details'.format(
            self._meta.model_name.lower())

    def get_absolute_url(self):
        return reverse(self.get_detail_view_name(),
                       args=[o.slug for o in self.breadcrumps])

    def __unicode__(self):
        return u'{}'.format(self.name)

    def __str__(self):
        return self.__unicode__()


class Country(BreadcrumpablePlaceModel):
    """
    A country
    """

    DETAIL_VIEW_NAME = 'country-details'

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')
        ordering = ('name',)


class Region(BreadcrumpablePlaceModel):
    """
    A region is a geographical region for grouping areas (and facilities within areas).
    """

    PARENT_FIELD = 'country'
    PARENT_MODEL = Country

    country = models.ForeignKey(Country,
                                models.PROTECT,
                                related_name='regions',
                                verbose_name=_('country'))

    class Meta:
        verbose_name = _('region')
        verbose_name_plural = _('regions')
        ordering = ('country', 'name',)

    @property
    def parent(self):
        return self.country


class Area(BreadcrumpablePlaceModel):
    """
    An area is a subdivision of a region, such as cities, neighbourhoods, etc.
    Each area belongs to a region.
    """

    PARENT_FIELD = 'region'
    PARENT_MODEL = Region

    region = models.ForeignKey(Region,
                               models.PROTECT,
                               related_name='areas',
                               verbose_name=_('region'))

    class Meta:
        verbose_name = _('area')
        verbose_name_plural = _('areas')
        ordering = ('region', 'name',)

    @property
    def parent(self):
        return self.region


class Place(BreadcrumpablePlaceModel):
    """
    A place (german: Ort) can be a city like Jena in Thüringen - Jena
    or a 'district' like  Wilmersdorf in Berlin - Berlin.
    """

    PARENT_FIELD = 'area'
    PARENT_MODEL = Area

    area = models.ForeignKey(Area,
                             models.PROTECT,
                             related_name='places',
                             verbose_name=_('area'))

    class Meta:
        verbose_name = _('place')
        verbose_name_plural = _('places')
        ordering = ('area', 'name',)

    @property
    def parent(self):
        return self.area
