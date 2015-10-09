# coding: utf-8

from datetime import timedelta, datetime

from django.test import TestCase

from organizations.models import Facility
from scheduler.models import Shift, ShiftHelper
from tests.factories import ShiftFactory, UserAccountFactory, TaskFactory, \
    FacilityFactory


def create_shift(start_hour, end_hour, facility=None):
    """
    Tiny helper because setting time periods is awkward till we remove the FK relationship.
    """
    create_args = dict(
        starting_time=datetime(2015, 1, 1, start_hour),
        ending_time=datetime(2015, 1, 1, end_hour)
    )
    if facility:
        create_args['facility'] = facility
    return ShiftFactory.create(**create_args)


class ShiftTestCase(TestCase):
    """
    We have some logic to detect conflicting shifts. This test case tests a few basic
    cases.
    """

    def setUp(self):
        self.user_account = UserAccountFactory.create()
        self.morning_shift = create_shift(9, 12)
        ShiftHelper.objects.create(user_account=self.user_account,
                                   shift=self.morning_shift)

        self.evening_shift = create_shift(18, 21)
        ShiftHelper.objects.create(user_account=self.user_account,
                                   shift=self.evening_shift)

    def test_non_conflict_tight_fitting(self):
        shift = create_shift(12, 18)
        assert ShiftHelper.objects.conflicting(shift=shift).count() == 0

    def test_non_conflict_gap_after(self):
        shift = create_shift(12, 17)
        assert ShiftHelper.objects.conflicting(shift=shift).count() == 0

    def test_non_conflict_gap_before(self):
        shift = create_shift(13, 18)
        assert ShiftHelper.objects.conflicting(shift=shift).count() == 0

    def test_non_conflict_tight_fitting_no_grace(self):
        shift = create_shift(12, 18)
        assert ShiftHelper.objects.conflicting(shift=shift,
                                               grace=None).count() == 0

    def test_non_conflict_gap_after_no_grace(self):
        shift = create_shift(12, 17)
        assert ShiftHelper.objects.conflicting(shift=shift,
                                               grace=None).count() == 0

    def test_non_conflict_gap_before_no_grace(self):
        shift = create_shift(13, 18)
        assert ShiftHelper.objects.conflicting(shift=shift,
                                               grace=None).count() == 0

    def test_non_conflict_gaps(self):
        shift = create_shift(13, 17)
        assert ShiftHelper.objects.conflicting(shift=shift).count() == 0

    def test_non_conflict_gaps_no_grace(self):
        shift = create_shift(13, 17)
        assert ShiftHelper.objects.conflicting(shift=shift,
                                               grace=None).count() == 0

    def test_conflict_at_beginning(self):
        shift = create_shift(8, 11)
        assert ShiftHelper.objects.conflicting(shift=shift).count() == 1

    def test_conflict_at_beginning_no_grace(self):
        shift = create_shift(9, 11)
        assert ShiftHelper.objects.conflicting(shift=shift,
                                               grace=None).count() == 1

    def test_conflict_at_end(self):
        shift = create_shift(10, 15)
        assert ShiftHelper.objects.conflicting(shift=shift).count() == 1

    def test_conflict_at_end_no_grace(self):
        shift = create_shift(11, 15)
        assert ShiftHelper.objects.conflicting(shift=shift,
                                               grace=None).count() == 1

    def test_conflict_within(self):
        shift = create_shift(10, 11)
        assert ShiftHelper.objects.conflicting(shift=shift).count() == 1

    def test_conflict_within_no_grace(self):
        shift = create_shift(9, 12)
        assert ShiftHelper.objects.conflicting(shift=shift,
                                               grace=None).count() == 1

    def test_conflict_around(self):
        shift = create_shift(8, 13)
        assert ShiftHelper.objects.conflicting(shift=shift).count() == 1

    def test_conflict_around_no_grace(self):
        shift = create_shift(8, 13)
        assert ShiftHelper.objects.conflicting(shift=shift).count() == 1


class FacilityTestCase(TestCase):
    def test_shift_manager_for_facility(self):
        """
            checks that get_days_with_shifts() returns only dates later than datetime.now()
        """
        now = datetime.now()
        yesterday_start = now - timedelta(1)
        yesterday_end = yesterday_start + timedelta(hours=1)
        tomorrow_start = now + timedelta(1)
        tomorrow_end = tomorrow_start + timedelta(hours=1)

        facility = FacilityFactory.create()
        task = TaskFactory.create(facility=facility)

        yesterday_shift = ShiftFactory.create(facility=facility,
                                              task=task,
                                              starting_time=yesterday_start,
                                              ending_time=yesterday_end)

        tomorrow_shift = ShiftFactory.create(facility=facility,
                                             task=task,
                                             starting_time=tomorrow_start,
                                             ending_time=tomorrow_end)

        assert Facility.objects.count() == 1, "test case assumes that shifts have been created for the same facility, as the ShiftFactory indeed does at the time of writing of this test case"
        assert Facility.objects.get() == task.facility

        shifts = Shift.open_shifts.filter(facility=facility)

        assert shifts.count() == 1, "only 1 shift should be found with Shifts.open_shifts"
        shift = shifts.get()
        assert shift == tomorrow_shift, "wrong shift was found"
        assert shift.ending_time > now, "the time has to be in the future"
