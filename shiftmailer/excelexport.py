# coding: utf-8
import logging
import os
import tempfile

from django.core.mail.message import EmailMessage
import xlwt

log = logging.getLogger(__name__)

style_bold = xlwt.easyxf(u'font: bold 1;')
style_1cm = xlwt.easyxf(u'font: height 450;')
style_right = xlwt.easyxf(u'align: horiz right')
style_left = xlwt.easyxf(u'align: horiz left')
style_center = xlwt.easyxf(u'align: horiz center;')
shift_time_full_format = '%d.%m.%Y %H:%M'
shift_time_short_format = '%H:%M'


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

        wb = xlwt.Workbook()
        ws = get_sheet(wb, u'Anmeldungen',
                       header=u'Schichtplan für {}\n{}\n'u'Jedwede Weitergabe der Daten an Dritte ist verboten!'
                       .format(self.mailer.facility, self.mailer.organization),
                       footer=u'Jedwede Weitergabe der Daten an Dritte ist verboten!\n&F (&P/&N)')

        colnames = [u'#', u'Vorname', u'Nachname',
                    u'Von', u'Bis', u'ID', u'RK', u'FZ']
        colwidths = [5, 25, 25,
                     10, 10, 3, 3, 3]
        colstyle = [style_right, style_left, style_left,
                    style_center, style_center, style_center, style_center, style_center]

        cur_line = 0

        for idx, name in enumerate(colnames):
            ws.write(cur_line, idx, name, style_bold)
            ws.col(idx).width = 256 * colwidths[idx]
            ws.row(cur_line).set_style(style_1cm)
        cur_line += 1

        prev_shift = None
        i = 1
        for shift in self.shifts:
            if 0 == shift.volunteer_count:
                continue

            if prev_shift is None or shift.topic_id != prev_shift.topic_id:
                log.debug(u'New shift topic %s->%s', prev_shift, shift)
                prev_shift = shift
                ws.write(cur_line, 0, shift.topic.title, style_bold)
                cur_line += 1
            if shift.starting_time.day == shift.ending_time.day:
                end_fmt = shift_time_short_format
            else:
                log.debug(u'Shift days differ: %s<->%s', shift.starting_time.day, shift.ending_time.day)
                end_fmt = shift_time_full_format
            ws.write(cur_line, 0, u'{} - {} ({}/{})'.format(shift.starting_time.strftime(shift_time_full_format),
                                                            shift.ending_time.strftime(end_fmt),
                                                            shift.volunteer_count, shift.slots))
            cur_line += 1

            for volunteer in shift.helpers.all():
                log.debug(u'Writing user line: %s', volunteer.user.username)
                write_user_line(ws, cur_line, i, volunteer, colstyle)
                cur_line += 1
                i += 1

        wb.save(filename)
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
        mail.from_email = "Volunteer-Planner.org <noreply@volunteer-planner.org>"
        mail.to = [str(self.mailer.email)]
        if attachment is not None:
            mail.attach_file(path=attachment, mimetype='application/vnd.ms-excel')
            mail.send()
        else:
            log.warn(u'No attachment, not mail.')


def get_sheet(wb, name, header=None, footer=None):
    ws = wb.add_sheet(name)
    ws.set_panes_frozen(True)
    ws.set_horz_split_pos(1)
    ws.set_remove_splits(True)
    ws.set_show_grid(True)
    ws.set_print_grid(True)
    ws.set_portrait(True)

    ws.set_top_margin(1.15)
    ws.set_bottom_margin(0.6)
    if header is not None:
        ws.header_str = header
    if footer is not None:
        ws.footer_str = footer
    return ws


def write_user_line(ws, cur, i, volunteer, style):
    first_name = volunteer.user.first_name if volunteer.user.first_name else volunteer.user.username + ': '
    last_name = volunteer.user.last_name
    # '-' are supposed to be replaced by indication of user property status, once they're implemented:
    # "id_verified", "health_card" & "penal clearance certificate"
    # '' are intentionally empty, it's entering and leaving time fields, filled manually
    for cidx, val in enumerate([i, first_name, last_name, '', '', '-', '-', '-']):
        ws.write(cur, cidx, val, style[cidx])
    ws.row(cur).set_style(style_1cm)
