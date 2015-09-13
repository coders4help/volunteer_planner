# coding: utf-8

import time

from django.core.mail.message import EmailMessage
from xlwt import *


class GenerateExcelSheet:
    def __init__(self, needs, mailer):
        self.needs = needs
        self.mailer = mailer
        self.send_file()

    def generate_excel(self):

        wb = Workbook()
        ws = wb.add_sheet('Registrierungen')
        style_bold = easyxf('font: bold 1')

        colnames = ["Zeit von",
                    "Zeit bis",
                    "Bereich",
                    "Anz",
                    "Freiwillige",
                    ]
        ws.write(0, 2, "Listenuebersicht der Freiwilligen in der Unterkunft " + self.needs[0].location.name, style_bold)
        ws.write(1, 2, "Erstellt fuer " + self.mailer.organization)
        ws.write(2, 2, "Jedwede Weitergabe der Daten an Dritte ist verboten!")

        for colindex, columname in enumerate(colnames):
            ws.write(3, colindex, columname, style_bold)

        for row_idx, row_data in enumerate(self.needs, start=4):

            ws.write(row_idx, 0, row_data.time_period_from.date_time.strftime("%d.%m.%Y %H:%M:00"))
            ws.write(row_idx, 1, row_data.time_period_to.date_time.strftime("%d.%m.%Y %H:%M:00"))
            ws.write(row_idx, 2, row_data.topic.title)
            ws.write(row_idx, 3, row_data.get_volunteer_total())
            volunteers_string = ""
            for volunteers in row_data.get_volunteers():
                volunteers_string += volunteers.user.email + ", "
            ws.write(row_idx, 4, volunteers_string)
        filename = "Dienstplan" + str(time.time()) + ".xls"
        wb.save(filename)
        return filename

    def send_file(self):
        mail = EmailMessage()
        mail.body = "Hallo " + self.mailer.first_name + " " + self.mailer.last_name + \
                    " Anbei die Liste zum Dienstplan der Freiwilligen. Dies ist ein Service von volunteer-planner.org"
        mail.subject = "Dienstplan fuer den " + self.needs[0].time_period_from.date_time.strftime("%d.%m.%Y") + \
                       " der Freiwilligen in der Unterkunft " + self.needs[0].location.name
        mail.from_email = "Volunteer-Planner.org <no-reply@volunteer-planner.org>"
        mail.to = [str(self.mailer.email)]
        attachment = self.generate_excel()
        mail.attach_file(path=attachment, mimetype='application/octet-stream')
        mail.send()
