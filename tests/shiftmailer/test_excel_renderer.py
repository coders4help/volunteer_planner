# coding: utf-8

import os
import pytest
import factory

from datetime import datetime

from tests.factories import OrganizationFactory, UserAccountFactory, ShiftFactory, FacilityFactory, ShiftHelperFactory

from organizations.models import Facility, Task
from scheduler.models import Shift, ShiftHelper
from shiftmailer.models import Mailer
from shiftmailer.excelexport import ExcelRenderer


@pytest.fixture
def facility():
    return FacilityFactory.build()


@pytest.fixture
def shifts(monkeypatch):

    shift_helpers = ShiftHelperFactory.create_batch(2)
    for shift_helper in shift_helpers:
        monkeypatch.setattr(shift_helper.shift, "volunteer_count", 2, False)

    return [shift_helper.shift for shift_helper in shift_helpers]


@pytest.mark.django_db
class TestExcelRenderer:
    def test_excel_rendering(self, facility, shifts, tmpdir):
        # Convert to plain string as tmpdir has its own write method which we don't want to use here
        filename = str(tmpdir.join("test.xls"))
        sut = ExcelRenderer()
        file = sut.generate_shift_overview(facility.organization, facility, shifts, filename)
        # assert 'h' in x
