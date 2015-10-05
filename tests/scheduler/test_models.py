# coding: utf-8

from datetime import timedelta, datetime

from django.test import TestCase

from scheduler.models import Need, Location, ShiftHelper
from tests.factories import NeedFactory, LocationFactory, UserAccountFactory


def create_need(start_hour, end_hour, location=None):
    """
    Tiny helper because setting time periods is awkward till we remove the FK relationship.
    """
    create_args = dict(
        starting_time=datetime(2015, 1, 1, start_hour),
        ending_time=datetime(2015, 1, 1, end_hour)
    )
    if location:
        create_args['location'] = location
    return NeedFactory.create(**create_args)


class NeedTestCase(TestCase):
    """
    We have some logic to detect conflicting needs. This test case tests a few basic
    cases.
    """

    def setUp(self):
        self.user_account = UserAccountFactory.create()
        self.morning_shift = create_need(9, 12)
        ShiftHelper.objects.create(user_account=self.user_account,
                                   need=self.morning_shift)

        self.evening_shift = create_need(18, 21)
        ShiftHelper.objects.create(user_account=self.user_account,
                                   need=self.evening_shift)

    def tearDown(self):
        Need.objects.all().delete()
        ShiftHelper.objects.all().delete()

    def test_non_conflict_tight_fitting(self):
        need = create_need(12, 18)
        assert ShiftHelper.objects.conflicting(need=need).count() == 0

    def test_non_conflict_gap_after(self):
        need = create_need(12, 17)
        assert ShiftHelper.objects.conflicting(need=need).count() == 0

    def test_non_conflict_gap_before(self):
        need = create_need(13, 18)
        assert ShiftHelper.objects.conflicting(need=need).count() == 0

    def test_non_conflict_tight_fitting_no_grace(self):
        need = create_need(12, 18)
        assert ShiftHelper.objects.conflicting(need=need,
                                               grace=None).count() == 0

    def test_non_conflict_gap_after_no_grace(self):
        need = create_need(12, 17)
        assert ShiftHelper.objects.conflicting(need=need,
                                               grace=None).count() == 0

    def test_non_conflict_gap_before_no_grace(self):
        need = create_need(13, 18)
        assert ShiftHelper.objects.conflicting(need=need,
                                               grace=None).count() == 0

    def test_non_conflict_gaps(self):
        need = create_need(13, 17)
        assert ShiftHelper.objects.conflicting(need=need).count() == 0

    def test_non_conflict_gaps_no_grace(self):
        need = create_need(13, 17)
        assert ShiftHelper.objects.conflicting(need=need,
                                               grace=None).count() == 0

    def test_conflict_at_beginning(self):
        need = create_need(8, 11)
        assert ShiftHelper.objects.conflicting(need=need).count() == 1

    def test_conflict_at_beginning_no_grace(self):
        need = create_need(9, 11)
        assert ShiftHelper.objects.conflicting(need=need,
                                               grace=None).count() == 1

    def test_conflict_at_end(self):
        need = create_need(10, 15)
        assert ShiftHelper.objects.conflicting(need=need).count() == 1

    def test_conflict_at_end_no_grace(self):
        need = create_need(11, 15)
        assert ShiftHelper.objects.conflicting(need=need,
                                               grace=None).count() == 1

    def test_conflict_within(self):
        need = create_need(10, 11)
        assert ShiftHelper.objects.conflicting(need=need).count() == 1

    def test_conflict_within_no_grace(self):
        need = create_need(9, 12)
        assert ShiftHelper.objects.conflicting(need=need,
                                               grace=None).count() == 1

    def test_conflict_around(self):
        need = create_need(8, 13)
        assert ShiftHelper.objects.conflicting(need=need).count() == 1

    def test_conflict_around_no_grace(self):
        need = create_need(8, 13)
        assert ShiftHelper.objects.conflicting(need=need).count() == 1


class LocationTestCase(TestCase):
    def test_need_manager_for_location(self):
        """
            checks that get_days_with_needs() returns only dates later than datetime.now()
        """
        now = datetime.now()
        yesterday_start = now - timedelta(1)
        yesterday_end = yesterday_start + timedelta(hours=1)
        tomorrow_start = now + timedelta(1)
        tomorrow_end = tomorrow_start + timedelta(hours=1)

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
