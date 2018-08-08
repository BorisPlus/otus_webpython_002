import os
import sys
import logging
import getopt

from static_code_terms_analyzer.core.reports import (
    Report,
    CsvFileExportFormatMixin,
    ConsoleExportFormatMixin,
    JsonFileExportFormatFileMixin,
    get_variable_nodes_names_at_lowercase_of_trees,
    get_function_def_nodes_names_at_lowercase,
    get_all_nodes_names_at_lowercase_of_trees,
    get_nouns_from_statements,
    get_verbs_from_statements,
    get_words_from_statements,
)

if __name__ == '__main__':

    if __name__ == '__main__':

        rootLogger = logging.getLogger('scta.core.reports')
        rootLogger.setLevel(logging.INFO)
        while rootLogger.handlers:
            rootLogger.handlers.pop()
        logFormatter = logging.Formatter("[%(asctime)s] LOGGER: \"%(name)s\" "
                                         "RUN: %(filename)-15s %(levelname)-8s %(message)s")

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        consoleHandler.setLevel(logging.INFO)
        rootLogger.addHandler(consoleHandler)

        def get_cmd_options_and_arguments(argv):
            """
            список аргументов и опций командной строки
            :param argv:
            :return:
            """
            parsed_options = dict()
            default_message = 'FORMAT: %s.py ' \
                              '--paths_to_analyze=<comma_separated_paths> ' \
                              '--files_top_limit_to_analyze=<int_value>' \
                              '--extensions_to_analyze=<comma_separated_extensions_with_lead_dot>' \
                              '--term_type=<term_type, one of [noun, verb, all, default]>' \
                              '--entity_type=<entity_type, one of [variables, functions, all, default]>' \
                              '--export_type=<export format, one of [console, csv_file, json_file, all, default]>' \
                              '--top_report_data=<int_value>' \
                              '' % (
                                  os.path.basename(__file__)
                              )
            try:
                options, args = getopt.getopt(argv, "", [
                    "paths_to_analyze=",
                    "files_top_limit_to_analyze=",
                    "extensions_to_analyze=",
                    "term_type=",
                    "entity_type=",
                    "export_type=",
                    "top_report_data=",
                ])
                rootLogger.info('argv')
                rootLogger.info(argv)
                rootLogger.info('options')
                rootLogger.info(options)
                rootLogger.info('args')
                rootLogger.info(args)
            except getopt.GetoptError:
                rootLogger.info(argv)
                rootLogger.info(default_message)
                sys.exit(2)
            for opt, arg in options:
                if opt == '-h':
                    rootLogger.info(default_message)
                    sys.exit()
                else:
                    parsed_options[opt.lstrip('--')] = arg
                    # elif opt in ("--paths_to_analyze",):
                    #     paths_to_analyze = arg
                    # elif opt in ("--files_top_limit_to_analyze",):
                    #     files_top_limit_to_analyze = arg
                    # elif opt in ("--extensions_to_analyze",):
                    #     extensions_to_analyze = arg
                    # elif opt in ("--term_type",):
                    #     term_type = arg
                    # elif opt in ("--entity_type",):
                    #     entity_type = arg
                    # elif opt in ("--export_type",):
                    #     export_type = arg
                    # elif opt in ("--top_report_data",):
                    #     top_report_data = arg
            return dict(
                options=parsed_options,
                args=args,
            )


        options_and_args = get_cmd_options_and_arguments(sys.argv[1:])

        paths_to_analyze = set(options_and_args.get('paths_to_analyze').strip(';')) \
            if options_and_args.get('paths_to_analyze', False) \
            else [os.path.dirname(os.path.abspath(__file__))]
        files_top_limit_to_analyze = int(options_and_args.get('files_top_limit_to_analyze')) \
            if options_and_args.get('files_top_limit_to_analyze', False) \
               and options_and_args.get('files_top_limit_to_analyze', '').isnumeric() \
            else 200
        extensions_to_analyze = set(options_and_args.get('paths_to_analyze').strip(',')) \
            if options_and_args.get('paths_to_analyze', False) \
            else ('.py',)

        term_type = options_and_args.get('term_type', 'default')
        entity_type = options_and_args.get('entity_type', 'default')
        export_type = options_and_args.get('export_type', 'json')

        use_top_report_data = int(options_and_args.get('top_report_data')) \
            if options_and_args.get('top_report_data', False) and options_and_args.get('top_report_data',
                                                                                       '').isnumeric() \
            else 10

        # Доступные форматы экспорта отчетов
        export_classes_mixin = dict(
            csv=CsvFileExportFormatMixin,
            json=JsonFileExportFormatFileMixin,
            console=ConsoleExportFormatMixin,
            default=ConsoleExportFormatMixin,
        )
        # Указанный формат экспорта отчета
        export_class_mixin = export_classes_mixin.get(
            export_type,
            export_classes_mixin.get('default'),
        )

        # Доступные функции извлечения сущностей кода (функции, переменные, без разницы) из AST-дерева
        entities_extractor_functions = dict(
            variables=get_variable_nodes_names_at_lowercase_of_trees,
            functions=get_function_def_nodes_names_at_lowercase,
            all=get_all_nodes_names_at_lowercase_of_trees,
            default=get_all_nodes_names_at_lowercase_of_trees,
        )
        # Выбранная функция извлечения сущностей кода
        use_entities_extractor_function = entities_extractor_functions.get(
            entity_type,
            entities_extractor_functions.get('default'),
        )

        # Доступные функции извлечения частей речи (существительные, глаголы, без разницы) из предложений
        terms_extractor_functions = dict(
            noun=get_nouns_from_statements,
            verb=get_verbs_from_statements,
            all=get_words_from_statements,
            default=get_words_from_statements,
        )
        # Выбранная функция извлечения частей речи
        use_terms_extractor_function = terms_extractor_functions.get(
            term_type,
            terms_extractor_functions.get('default'),
        )


        # Динамически создам класс отчета с примесью формата экспорта,
        # заодно для простоты вызова реализуем в нем метод, инкапсулирующий в себе
        # загрузку, подсчет и экспорт данных
        # Формально: условия использования примесей соблюдены, при это не надо плодить миксы для подсчета частей речи
        # в сущностях статического кода
        # class CsvReportClass(CsvFileExportFormatMixin, Report):
        #   pass
        # class JsonReportClass(JsonExportFormatFileMixin, Report):
        #   pass
        # class ConsoleReportClass(ConsoleExportFormatMixin, Report):
        #   pass
        class MixedReportClass(export_class_mixin, Report):
            def quick(self, top_report_data=5, report_name='Dynamic MixedReportClass'):
                self.load_source_data()
                self.build_report_data(top_report_data=top_report_data)
                self._export_report(report_name=report_name)


        mixed_report = MixedReportClass(
            source_code_paths=set(paths_to_analyze),
            entities_extractor_function=use_entities_extractor_function,
            terms_extractor_function=use_terms_extractor_function,
            files_top_limit=files_top_limit_to_analyze,
            files_extensions=extensions_to_analyze
        )

        mixed_report.quick(top_report_data=use_top_report_data, report_name='Dynamic ReportClass')
