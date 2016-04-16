# coding: utf-8
import logging
import xlwt

log = logging.getLogger(__name__)

style_bold = xlwt.easyxf(u'font: bold 1;')
style_1cm = xlwt.easyxf(u'font: height 450;')
style_right = xlwt.easyxf(u'align: horiz right')
style_left = xlwt.easyxf(u'align: horiz left')
style_center = xlwt.easyxf(u'align: horiz center;')
shift_time_full_format = '%d.%m.%Y %H:%M'
shift_time_short_format = '%H:%M'


class ExcelRenderer:
    def __init__(self):
        pass

    @staticmethod
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

    @staticmethod
    def write_user_line(ws, cur, i, volunteer, style):
        first_name = volunteer.user.first_name if volunteer.user.first_name else volunteer.user.username + ': '
        last_name = volunteer.user.last_name
        # '-' are supposed to be replaced by indication of user property status, once they're implemented:
        # "id_verified", "health_card" & "penal clearance certificate"
        # '' are intentionally empty, it's entering and leaving time fields, filled manually
        for cidx, val in enumerate([i, first_name, last_name, '', '', ]):
            ws.write(cur, cidx, val, style[cidx])
        ws.row(cur).set_style(style_1cm)

    def generate_shift_overview(self, organization, facility, shifts, filename):
        wb = xlwt.Workbook()
        ws = ExcelRenderer.get_sheet(wb, u'Anmeldungen',
                                     header=u'Schichtplan für {}\n{}\n'u'Jedwede Weitergabe der Daten an Dritte ist verboten!'
                       .format(facility, organization),
                                     footer=u'Jedwede Weitergabe der Daten an Dritte ist verboten!\n&F (&P/&N)')

        colnames = [u'#', u'Vorname', u'Nachname', u'Von', u'Bis',
                    u'Teilnehmer', u'Plätze']
        colwidths = [5, 25, 25, 5, 5,
                     12, 12]
        colstyle = [style_right, style_left, style_left, style_center, style_center,
                    style_center, style_center, style_center, style_right, style_right]

        cur_line = 0

        for idx, name in enumerate(colnames):
            ws.write(cur_line, idx, name, style_bold)
            ws.col(idx).width = 256 * colwidths[idx]
            ws.row(cur_line).set_style(style_1cm)
        cur_line += 1

        prev_shift = None
        i = 1
        for shift in shifts:
            if 0 == shift.volunteer_count:
                continue

            if prev_shift is None or shift.task_id != prev_shift.task_id:
                log.debug(u'New shift task %s->%s', prev_shift, shift)
                prev_shift = shift
                ws.write(cur_line, 0, shift.task.name, style_bold)
                cur_line += 1
            if shift.starting_time.day == shift.ending_time.day:
                end_fmt = shift_time_short_format
            else:
                log.debug(u'Shift days differ: %s<->%s', shift.starting_time.day, shift.ending_time.day)
                end_fmt = shift_time_full_format
            ws.write(cur_line, 0, u'{} - {} ({}/{})'.format(shift.starting_time.strftime(shift_time_full_format),
                                                            shift.ending_time.strftime(end_fmt),
                                                            shift.volunteer_count, shift.slots))
            ws.write(cur_line, 5, shift.volunteer_count)
            ws.write(cur_line, 6, shift.slots)
            cur_line += 1

            for volunteer in shift.helpers.all():
                log.debug(u'Writing user line: %s', volunteer.user.username)
                ExcelRenderer.write_user_line(ws, cur_line, i, volunteer, colstyle)
                cur_line += 1
                i += 1

        wb.save(filename)
