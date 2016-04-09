# coding: utf-8
import logging
import os
import tempfile

from django.core.mail.message import EmailMessage
from excel_renderer import ExcelRenderer

log = logging.getLogger(__name__)


class GenerateExcelSheet:
    def __init__(self, shifts, mailer):
        if not shifts:
            raise AssertionError(u'No shifts given. Cannot generate Excel file for {}.'.format(mailer.facility))

        self.shifts = shifts
        self.mailer = mailer
        self.tmpdir = tempfile.mkdtemp()
        self.tmpfiles = []

    def __del__(self):
        for filename in self.tmpfiles:
            if filename and os.path.exists(filename):
                os.remove(filename)
        if self.tmpdir is not None and os.path.exists(self.tmpdir):
            log.debug(u'Removing tmpdir %s', self.tmpdir)
            os.removedirs(self.tmpdir)

    def generate_excel(self):
        if self.shifts is None or self.shifts.count() == 0:
            log.warn(u'No shifts, not shift schedule.')
            return None

        log.debug(u'About to generate XLS for facility "%s"', self.shifts[0].facility)
        log.debug(u'Shifts query: %s', self.shifts.query)
        filename = os.path.join(self.tmpdir, u'Dienstplan_{}_{}.xls'.format(self.mailer.organization,
                                                                            self.shifts[0].starting_time
                                                                            .strftime('%Y%m%d')))
        self.tmpfiles.append(filename)

        renderer = ExcelRenderer()
        renderer.generate_shift_overview(self.mailer.organization, self.mailer.facility, self.shifts, filename)

        return filename

    def send_file(self):
        attachment = self.generate_excel()

        if not self.mailer:
            log.error(u'Cannot create and send email without mailer information')
            return

        mail = EmailMessage()
        mail.body = "Hallo " + self.mailer.first_name + " " + self.mailer.last_name + "\n\n"\
                    "Anbei die Liste zum Dienstplan der Freiwilligen.\nDies ist ein Service von volunteer-planner.org"
        mail.subject = "Dienstplan fuer den " + self.shifts[0].starting_time.strftime("%d.%m.%Y") + \
                       " der Freiwilligen in der Unterkunft " + self.shifts[0].facility.name
        mail.from_email = "noreply@Volunteer-Planner.org <noreply@volunteer-planner.org>"
        mail.to = [str(self.mailer.email)]
        if attachment is not None:
            mail.attach_file(path=attachment, mimetype='application/vnd.ms-excel')
            mail.send()
        else:
            log.warn(u'No attachment, not mail.')
