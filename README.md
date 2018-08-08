# Static Code Terms Analyzer

Проект модуля статическго анализа кода, с возможностью подготовки отчетов.
Реализован на базе проекта соотетствующей ранее реализованной библиотеки [SCTA](https://github.com/BorisPlus/otus_webpython_001).

## Как пользоваться

### Требования

[SCTA](https://github.com/BorisPlus/otus_webpython_001) использует:
* nltk==3.3 (http://www.nltk.org/)
Данный проект допольнительно использует:
* GitPython-2.1.11

```
pip3 install nltk==3.3
pip3 install GitPython==2.1.11
```

или

```
pip3 install -r requirements.txt
```

не забудте проверить

```bash
Please use the NLTK Downloader to obtain the resource:
python3
>>> import nltk
>>> nltk.download('averaged_perceptron_tagger')

  Searched in:
    - '/home/developer/nltk_data'
    - '/usr/share/nltk_data'
    - '/usr/local/share/nltk_data'
    - '/usr/lib/nltk_data'
    - '/usr/local/lib/nltk_data'
    - '/usr/nltk_data'
    - '/usr/share/nltk_data'
    - '/usr/lib/nltk_data'
```

если не сработает, то попробуйте

```bash
>>> import nltk
>>> nltk.download('all')
```
или с ручным выбором через GUI

```bash
>>> import nltk
>>> nltk.download()
```

### Установка

Скопируйте к себе в проект папку static_code_terms_analyzer или установите иным известным Вам и возможным образом.
### Примеры

См. директорию [example_usage](https://github.com/BorisPlus/otus_webpython_001/tree/master/example_usage)


#### Пример №1

```python

import sys
import logging


from static_code_terms_analyzer.scta import (
    get_top_verbs_of_functions_names_in_path,
)

if __name__ == '__main__':

    rootLogger = logging.getLogger('scta.example_usage.001')
    rootLogger.setLevel(logging.INFO)
    while rootLogger.handlers:
        rootLogger.handlers.pop()
    logFormatter = logging.Formatter("[%(asctime)s] LOGGER: \"%(name)s\" "
                                     "RUN: %(filename)-15s %(levelname)-8s %(message)s")

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.INFO)
    rootLogger.addHandler(consoleHandler)

    path_to_analyze = sys.argv[1] if len(sys.argv) >= 2 else '../static_code_terms_analyzer'
    limit_top_size = int(sys.argv[2]) if len(sys.argv) >= 3 and sys.argv[2].isdigit() else 10

    #

    limited_partition_of_words = get_top_verbs_of_functions_names_in_path(path_to_analyze)

    rootLogger.info(
        'TOTAL TOP FUNCTION VERBS: %s words' % len(limited_partition_of_words)
    )

    for word_item, occurence in limited_partition_of_words:
        rootLogger.info(
            '%s: %s' % (
                word_item,
                occurence
            )
        )
```

РЕЗУЛЬТАТ

```
[2018-08-07 22:48:31,029] LOGGER: "scta.example_usage.001" RUN: example_001.py  INFO     TOTAL TOP FUNCTION VERBS: 5 words
[2018-08-07 22:48:31,030] LOGGER: "scta.example_usage.001" RUN: example_001.py  INFO     get: 35
[2018-08-07 22:48:31,030] LOGGER: "scta.example_usage.001" RUN: example_001.py  INFO     is: 8
[2018-08-07 22:48:31,030] LOGGER: "scta.example_usage.001" RUN: example_001.py  INFO     filtered: 2
[2018-08-07 22:48:31,030] LOGGER: "scta.example_usage.001" RUN: example_001.py  INFO     apply: 2
[2018-08-07 22:48:31,030] LOGGER: "scta.example_usage.001" RUN: example_001.py  INFO     applied: 1
```

#### Пример №2 (если в статическом коде есть ошибка)

```python
import os
import collections
import sys
import logging

from static_code_terms_analyzer.scta import (
    get_words_in_path,
)


if __name__ == '__main__':

    rootLogger = logging.getLogger('scta.example_usage.002')
    rootLogger.setLevel(logging.INFO)
    while rootLogger.handlers:
        rootLogger.handlers.pop()
    logFormatter = logging.Formatter("[%(asctime)s] LOGGER: \"%(name)s\" "
                                     "RUN: %(filename)-15s %(levelname)-8s %(message)s")

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.INFO)
    rootLogger.addHandler(consoleHandler)

    base_path = sys.argv[1] if len(sys.argv) >= 2 \
        else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'downloads')
    limit_top_size = sys.argv[2] if len(sys.argv) >= 3 else 100

    limit_top_size_partitions_of_verbs = []
    projects = [
        'python-image-restoration',
    ]
    for project in projects:
        path_to_analyze = os.path.join(base_path, project)
        if os.path.exists(path_to_analyze):
            rootLogger.info('"%s" CHECKING' % path_to_analyze)
            limit_top_size_partitions_of_verbs.extend(
                get_words_in_path(path_to_analyze)
            )
        else:
            rootLogger.warning('"%s" NOT EXISTS' % path_to_analyze)

    rootLogger.info(
        'TOTAL: %s words, %s unique' % (
            len(limit_top_size_partitions_of_verbs),
            len(set(limit_top_size_partitions_of_verbs))
        )
    )
    for word_item, occurence in collections.Counter(limit_top_size_partitions_of_verbs).most_common(
            int(limit_top_size)
    ):
        rootLogger.info(
            '%s: %s' % (
                word_item,
                occurence
            )
        )
```

РЕЗУЛЬТАТ

```
[2018-08-07 22:54:59,442] LOGGER: "scta.example_usage.002" RUN: example_002.py  INFO     "/home/developer/PycharmProjects/otus_webpython_002/downloads/python-image-restoration" CHECKING
[2018-08-07 22:54:59,444] scta.py ERROR    Missing parentheses in call to 'print' (<unknown>, line 75)
[2018-08-07 22:54:59,445] LOGGER: "scta.example_usage.002" RUN: example_002.py  INFO     TOTAL: 0 words, 0 unique
```

#### Пример №3 (используя "супердиспетчер")

Комбинируя параметры диспетчера отчетов, такие как части речи (term_type:=['verb','noun','all']) или сущности кода (entity_type:=['variables','functions','all']), возможно получение стьатистического среза по любым сущностям и используемым в них частям речи. Результат этого примера идентичен Примеру №1.

```python
from static_code_terms_analyzer.scta import (
    get_top_terms_of_entities_in_path
)
...
    limited_partition_of_words = get_top_terms_of_entities_in_path(
        path_to_analyze,
        term_type='verbs',
        entity_type='functions'
    )
```

#### Пример №4 (загрузка с GitHub, файловой системы и пр.)

Реализованы классы загрузки репозиториев с Гитхаба и локальных файловых директорий.

Так, для GitHubSource

```python
# Test GitHubSource
try:
    from_source = 'https://github.com/Melevir/python-image-restoration/'
    to_target = os.path.join('<full_path>','downloads')
    src = GitHubSource(source_path=from_source)
    src.copy_to_local(to_target, delete_if_exists=True)
except:
    print(sys.exc_info()[1])
```

и для LocalFilesystemSource

```python
# Test LocalFilesystemSource
from_source = '<full_path>/static_code_terms_analyzer/'
to_target = os.path.join('<full_path>', 'downloads')
src = LocalFilesystemSource(source_path=from_source)
src.copy_to_local(to_target, delete_if_exists=True)
```

#### Пример №5 (использование "примесей" (mixin) для отчетов)

Подготовка отчетов статического анализа кода.
Отчеты могут быть выведены в CSV-файлы, JSON-файлы или консоль.
Для этого используовать "примеси":

* ConsoleExportFormatMixin(ExportFormatMixin):
* CsvFileExportFormatMixin(ExportFormatMixin):
* JsonFileExportFormatFileMixin(ExportFormatMixin):

Например, возможно динамически создать класс отчета с примесью формата экспорта,
заодно для простоты вызова реализуем в нем метод, инкапсулирующий в себе
загрузку, подсчет и экспорт данных.
Формально: условия использования примесей соблюдены, при это не надо плодить миксы для подсчета частей речи
в сущностях статического кода

```python
class CsvReportClass(CsvFileExportFormatMixin, Report):
    pass
class JsonReportClass(JsonExportFormatFileMixin, Report):
    pass
class ConsoleReportClass(ConsoleExportFormatMixin, Report):
    pass
```

подробнее смтори пример [example_202_report_work.py](https://github.com/BorisPlus/otus_webpython_001/tree/master/example_usage/example_202_report_work.py)

```python
export_type = 'json'
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

```
РЕЗУЛЬТАТ ДЛЯ JSON-ФАЙЛА
```json
["rootlogger", 62]
["top", 35]
["sys", 33]
["path", 32]
["os", 28]
["consolehandler", 24]
["limit", 24]
["words", 23]
["options", 22]
["len", 22]
```
## Авторы

* **Melevir** - *Initial work* - [Melevir](https://gist.github.com/Melevir/5754a1b553eb11839238e43734d0eb79)
* **BorisPlus** - *Доработка по домашнему заданию №1* - [BorisPlus](https://github.com/BorisPlus/otus_webpython_001)
* **BorisPlus** - *Доработка по домашнему заданию №2* - [BorisPlus](https://github.com/BorisPlus/otus_webpython_002)


## Лицензия

Огриничивается лицензиями используемых библиотек

## Дополнительные сведения

Проект в рамках курса "Web-разработчик на Python" на https://otus.ru/learning

