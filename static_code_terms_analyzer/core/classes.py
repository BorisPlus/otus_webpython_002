#!/usr/bin/python3
import git
import logging
import os
import shutil


# class Config:
#     class Singleton:
#         __sources_local_path = ''
#
#         def __init__(self):
#             pass
#
#         def get_sources_local_path(self):
#             return self.__sources_local_path
#
#     __instance = Singleton()
#
#     @staticmethod
#     def get_instance():
#         return Config.__instance


class Source(object):
    """
    Истоник исходников. Базовый класс.
    """
    source_path = None

    @staticmethod
    def validate_attrs(**kwargs):
        """
        Валидация параметров взаимодействия с истоником, которые понадобятся для его "copy_to_local"
        :param kwargs: параметры взаимодействия с истоником, которые понадобятся для его "copy_to_local"
        :return: либо подтверждает валидность либо генерирует соответствующее исключение
        """
        if 'source_path' in kwargs and kwargs['source_path'] and kwargs['source_path'].endswith('/'):
            return True
        elif 'source_path' in kwargs and kwargs['source_path'] and not kwargs['source_path'].endswith('/'):
            raise Exception('Атрибут "source_path" должен оканчиваться на "/"')
        elif 'source_path' in kwargs and not kwargs['source_url']:
            raise Exception('Атрибут "source_path" имеет неудовлетворительное знасение')
        else:
            raise Exception('Атрибут "source_path" не задан')

    def __init__(self, **kwargs):
        """
        Инициализация объекта
        :param kwargs: параметры взаимодействия с истоником, которые понадобятся для его "copy_to_local"
        """
        try:
            self.__class__.validate_attrs(**kwargs)
            for k in kwargs:
                self.__setattr__(k, kwargs[k])
        except Exception as e:
            raise

    def __str__(self):
        return '%s' % self.__dict__

    # def is_source_exists(self):
    #     """
    #     Проверка существования истоника
    #     :return:
    #     """
    #     raise Exception('Реализуйте этот метод в наследнике')

    def copy_to_local(self, target_path, delete_if_exists=False):
        """
        Копирование истоника в локальную директорию
        :param target_path: Локальная директория
        :param delete_if_exists: по умолчанию False, а если True, удалит существующую директорию источника, иначе исключение
        :return:
        """
        raise Exception('Реализуйте этот метод в наследнике')


class GitHubSource(Source):
    def copy_to_local(self, target_path, delete_if_exists=False):
        if delete_if_exists:
            target_source_dir = self.source_path.split('/')[-2]
            target_source_full_path = os.path.join(target_path, target_source_dir)
            if os.path.exists(target_source_full_path):
                shutil.rmtree(target_source_full_path)
        git.Git(target_path).clone(self.source_path)


class LocalFilesystemSource(Source):
    def copy_to_local(self, target_path, delete_if_exists=False):
        target_source_dir = self.source_path.split('/')[-2]
        target_source_full_path = os.path.join(target_path, target_source_dir)
        if delete_if_exists:
            if os.path.exists(target_source_full_path):
                shutil.rmtree(target_source_full_path)
        shutil.copytree(self.source_path, target_source_full_path)

    @staticmethod
    def validate_attrs(**kwargs):
        """
        Дополнительная к родительской валидация на предмет физического существования источника
        :param kwargs: параметры взаимодействия с истоником, которые понадобятся для его "copy_to_local"
        :return: либо подтверждает валидность либо генерирует соответствующее исключение
        """
        if Source.validate_attrs(**kwargs):
            if not os.path.exists(kwargs['source_path']):
                raise Exception('"source_path" "%s" не существует' % kwargs['source_path'])
        return True

if __name__ == '__main__':

    rootLogger = logging.getLogger('scta.core.classes')
    rootLogger.setLevel(logging.INFO)
    logFormatter = logging.Formatter("[%(asctime)s] %(filename)-15s %(levelname)-8s %(message)s")

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.INFO)
    rootLogger.addHandler(consoleHandler)

    # Test GitHubSource

    from_source = 'https://github.com/Melevir/python-image-restoration/'

    to_target = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'downloads'
    )
    rootLogger.info('START')
    rootLogger.info('COPY FROM "%s" TO "%s"' % (from_source, to_target))

    src = GitHubSource(
        source_path=from_source
    )
    src.copy_to_local(to_target, delete_if_exists=True)
    rootLogger.info('DONE')

    # Test LocalFilesystemSource

    from_source = '/home/developer/PycharmProjects/otus_webpython_002/static_code_terms_analyzer/'

    to_target = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'downloads')
    rootLogger.info('START')
    rootLogger.info('COPY FROM "%s" TO "%s"' % (from_source, to_target))

    src = LocalFilesystemSource(
        source_path=from_source
    )
    src.copy_to_local(to_target, delete_if_exists=True)
    rootLogger.info('DONE')
