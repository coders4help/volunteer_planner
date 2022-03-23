import logging

from django.db import models

logger = logging.getLogger(__name__)


class NewsEntryQuerySet(models.QuerySet):
    """ Custom QuerySet for NewsEntry.
        Defines auxiliary methods for optimizing fetching for and from large lists of affected facilities.
    """
    def for_facilities(self, facilities):
        """ Updates the query set to filter for a given set of facilities.

            :param facilities: array or list of facilities to filter for
            :type facilities: organization.models.Facility

            :return: the query set configured to filter only for given facilities
        """
        logger.debug(u'Filtering for %d facilities', len(facilities))
        return self.filter(facility__in=facilities)

    def filter_by_facility(self, facility):
        """ Filters this NewsEntry query set for a given facility.

            :param facility: Facility to filter for
            :type facility: organization.models.Facility

            :return: Iterator containing only news entries for the given facility
        """
        logger.debug(u'Filtering news entries for facility %s (id: %s)', facility.name, facility.id)
        return filter(lambda entry: entry.facility_id == facility.id, self)


# NewsEntry manager created from query set that enables filtering for facilities
NewsEntryManager = models.Manager.from_queryset(NewsEntryQuerySet)
