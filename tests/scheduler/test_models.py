from django.test import TestCase
import datetime

from tests.factories import NeedFactory


def create_need(start_hour, end_hour):
    """
    Tiny helper because setting time periods is awkward till we remove the FK relationship.
    """
    start = datetime.datetime(2015, 1, 1, start_hour)
    end = datetime.datetime(2015, 1, 1, end_hour)
    return NeedFactory.create(time_period_from__date_time=start, time_period_to__date_time=end)


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
