import csv
import json
# Задача: выводить результат в консоль, json-файл или csv-файл (в зависимости от параметра отчёта);
# Буду использовать ReportFormatMixin


class ReportFormatMixin:
    data = None


class ReportFormatConsoleMixin(ReportFormatMixin):
    def do_report(self, report_name=''):
        print(report_name)
        for row in self.data:
            print(row)


class ReportFormatCsvFileMixin(ReportFormatMixin):
    def do_report(self, report_name=''):
        with open(report_name, 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(self.data)


class ReportFormatJsonFileMixin(ReportFormatMixin):
    def do_report(self, report_name=''):
        with open(report_name, 'w') as out_file:
            for row in self.data:
                out_file.write(json.loads(row))

