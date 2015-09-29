from django.test import TestCase
import datetime

from tests.factories import NeedFactory


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
        assert need.get_conflicting_needs(self.needs, grace=datetime.timedelta(hours=0))


class LocationTestCase(TestCase):      

    def test_get_days_with_needs_at_location_end_later_than_now(self):
        """
            checks that get_days_with_needs() returns only dates later than datetime.now()
        """
        now = datetime.datetime.now()
        yesterday_start = now - datetime.timedelta(1)
        yesterday_end = yesterday_start+datetime.timedelta(hours=1)
        tomorrow_start = now + datetime.timedelta(1)
        tomorrow_end = tomorrow_start+datetime.timedelta(hours=1)

        needs = [NeedFactory.create(starting_time=yesterday_start, ending_time=yesterday_end),
                    NeedFactory.create(starting_time=tomorrow_start, ending_time=tomorrow_end)]

        locations = set()
        for n in needs:
            locations.add(n.location)

        assert len(locations) == 1, "test case assumes that needs have been created for the same location, as the NeedFactory indeed does at the time of writing of this test case"
        #TODO change this assumption by explicitly creating needs for the same location

        for l in locations:
            for day in l.get_days_with_needs():
                assert isinstance(day[0], datetime.datetime)
                assert day[0] > datetime.datetime.now()

    def test_get_days_with_needs_at_location_no_duplicates(self):
        """
        checks that get_days_with_needs() does not return any duplicate dates
        """
        start = datetime.datetime.now()
        end = start + datetime.timedelta(hours=1)
        needs = [NeedFactory.create(starting_time=start, ending_time=end),
                    NeedFactory.create(starting_time=start, ending_time=end)]

        locations = set()
        for n in needs:
            locations.add(n.location)

        assert len(locations) == 1, "test case assumes that needs have been created for the same location, as the NeedFactory indeed does at the time of writing of this test case"
        #TODO change this assumption by explicitly creating needs for the same location

        for l in locations:
            dates = set()
            for d in l.get_days_with_needs():
                assert d[0] not in dates
                dates.add(d[0])

    def test_get_days_with_needs_have_german_formatting(self):
        need = create_need(15,16)
        for d in need.location.get_days_with_needs():
            assert d[0].strftime("%A, %d.%m.%Y") == d[1]
