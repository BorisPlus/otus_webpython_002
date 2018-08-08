#!/usr/bin/python3
import collections

from static_code_terms_analyzer.scta import (
    get_files_of_paths,
    get_trees_of_files_list,
    get_real_trees,
    get_real_statements,
    get_not_special_statements,
)


class Report:
    source_code_paths = []
    files_top_limit = 5
    files_extensions = ()
    entities_extractor_function = None
    terms_extractor_function = None
    __files_paths = None
    __real_trees = None
    __not_special_statements = None
    __is_source_data_was_loaded = False
    __source_data = None
    __is_report_data_was_build = False
    report_data = None

    def __init__(self,
                 source_code_paths,
                 entities_extractor_function,
                 terms_extractor_function,
                 files_top_limit=10,
                 files_extensions=('.py',)):
        """

        :param source_code_paths: Список (любая коллекция) директорий для статического анализа
        :param entities_extractor_function: функция извлечения сущностей кода, одно из:
            get_variable_nodes_names_at_lowercase_of_trees,
            get_function_def_nodes_names_at_lowercase,
            get_all_nodes_names_at_lowercase_of_trees
        :param terms_extractor_function: функция извлечения частей речи, одно из:
            get_nouns_from_statements,
            get_verbs_from_statements,
            get_words_from_statements
        :param files_top_limit: Число файлов, содержимое которых необходимо проанализировать
        :param files_extensions: Кортеж расширений файлов, содержимое которых необходимо проанализировать
        """
        if not isinstance(source_code_paths, set):
            raise Exception('source_code_paths must be set')
        if not isinstance(files_top_limit, int):
            raise Exception('files_top_limit must be int')
        if not isinstance(files_extensions, tuple):
            raise Exception('files_extensions must be tuple')
        # if not callable(entities_extractor_function) and not (entities_extractor_function is None):
        #     raise Exception('entities_extractor_function must be function or None')
        if not callable(entities_extractor_function):
            raise Exception('entities_extractor_function must be function or None')
        if not callable(terms_extractor_function):
            raise Exception('terms_extractor_function must be function or None')
        self.source_code_paths = source_code_paths
        self.files_top_limit = files_top_limit
        self.files_extensions = files_extensions
        self.entities_extractor_function = entities_extractor_function
        self.terms_extractor_function = terms_extractor_function

    def load_source_data(self):
        self.__files_paths = get_files_of_paths(self.source_code_paths)
        self.__real_trees = get_real_trees(get_trees_of_files_list(self.__files_paths))
        statements = self.entities_extractor_function(self.__real_trees)
        real_statements = get_real_statements(statements)
        self.__not_special_statements = get_not_special_statements(real_statements)
        self.__source_data = self.terms_extractor_function(self.__not_special_statements)
        self.__is_source_data_was_loaded = True

    def set_source_data(self, data):
        self.__real_trees = []
        self.__not_special_statements = []
        self.__source_data = data
        self.__is_source_data_was_loaded = True
        self.__is_report_data_was_build = False

    def build_report_data(self, top_report_data=10, **kwargs):
        if kwargs:
            pass
        self.report_data = collections.Counter(self.__source_data).most_common(top_report_data)
        self.__is_report_data_was_build = True

    def set_report_data(self, data):
        self.report_data = data
        self.__is_report_data_was_build = True


if __name__ == '__main__':
    pass
