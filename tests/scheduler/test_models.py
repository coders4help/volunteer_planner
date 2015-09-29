import datetime

from django.test import TestCase

from scheduler.models import Need, Location
from tests.factories import NeedFactory, LocationFactory


def create_need(start_hour, end_hour):
    """
    Tiny helper because setting time periods is awkward till we remove the FK relationship.
    """
    start = datetime.datetime(2015, 1, 1, start_hour)
    end = datetime.datetime(2015, 1, 1, end_hour)
    return NeedFactory.create(starting_time=start, ending_time=end)


class NeedTestCase(TestCase):
    """
    We have some logic to detect conflicting needs. This test case tests a few basic
    cases.
    """

    def setUp(self):
        self.needs = [create_need(9, 12), create_need(18, 21)]

    def test_non_conflict(self):
        need = create_need(14, 16)
        assert not need.get_conflicting_needs(self.needs)

    def test_clear_conflict(self):
        need = create_need(9, 12)
        assert need.get_conflicting_needs(self.needs)

    def test_not_conflict_1h_grace(self):
        need = create_need(11, 14)
        assert not need.get_conflicting_needs(self.needs)

    def test_conflict_0h_grace(self):
        need = create_need(11, 14)
        assert need.get_conflicting_needs(self.needs,
                                          grace=datetime.timedelta(hours=0))


class LocationTestCase(TestCase):
    def test_need_manager_for_location(self):
        """
            checks that get_days_with_needs() returns only dates later than datetime.now()
        """
        now = datetime.datetime.now()
        yesterday_start = now - datetime.timedelta(1)
        yesterday_end = yesterday_start + datetime.timedelta(hours=1)
        tomorrow_start = now + datetime.timedelta(1)
        tomorrow_end = tomorrow_start + datetime.timedelta(hours=1)

        location = LocationFactory.create()

        yesterday_need = NeedFactory.create(location=location,
                                            starting_time=yesterday_start,
                                            ending_time=yesterday_end)
        tomorrow_need = NeedFactory.create(location=location,
                                           starting_time=tomorrow_start,
                                           ending_time=tomorrow_end)

        assert Location.objects.count() == 1, "test case assumes that needs have been created for the same location, as the NeedFactory indeed does at the time of writing of this test case"
        assert Location.objects.all()[0] == location

        needs = Need.open_needs.at_location(location=location)

        assert needs.count() == 1, "only 1 need should be found with Need.open_needs"
        assert needs[0] == tomorrow_need, "wrong shift was found"
        assert needs[0].ending_time > now, "the time has to be in the future"
