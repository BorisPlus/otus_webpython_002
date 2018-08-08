import csv
import json


# Задача: выводить результат в консоль, json-файл или csv-файл (в зависимости от параметра отчёта);
# Буду использовать ReportFormatMixin


class ExportFormatMixin:
    # report_data = None

    def _export_report(self, report_name=''):
        pass


class ConsoleExportFormatMixin(ExportFormatMixin):
    def _export_report(self, report_name=''):
        print(report_name)
        for row in self.report_data:
            print(row)


class CsvFileExportFormatMixin(ExportFormatMixin):
    def _export_report(self, report_name=''):
        with open('%s.csv' % report_name, 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(self.report_data)


class JsonFileExportFormatFileMixin(ExportFormatMixin):
    def _export_report(self, report_name=''):
        with open('%s.json' % report_name, 'w') as out_file:
            for row in self.report_data:
                out_file.write(json.dumps(row))
                out_file.write('\n')
