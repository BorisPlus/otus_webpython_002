import os
import collections
import sys
import logging

module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if module_path not in sys.path:
    sys.path.append(module_path)
from static_code_terms_analyzer.scta import (
    get_nouns_of_variables_names_in_path
)

if __name__ == '__main__':

    rootLogger = logging.getLogger('scta.example_usage.000')
    rootLogger.setLevel(logging.INFO)
    while rootLogger.handlers:
        rootLogger.handlers.pop()
    logFormatter = logging.Formatter("[%(asctime)s] LOGGER: \"%(name)s\" "
                                     "RUN: %(filename)-15s %(levelname)-8s %(message)s")

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.INFO)
    rootLogger.addHandler(consoleHandler)

    base_path = sys.argv[1] if len(sys.argv) >= 2 else os.path.dirname(os.path.abspath(__file__))
    limit_top_size = int(sys.argv[2]) if len(sys.argv) >= 3 and sys.argv[2].isdigit() else 10

    limit_top_size_partitions_of_nouns_of_variables_names = []
    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
        '',
    ]
    for project in projects:
        path_to_analyze = os.path.join(base_path, project)
        if os.path.exists(path_to_analyze):
            rootLogger.info('"%s" CHECKING' % path_to_analyze)
            limit_top_size_partitions_of_nouns_of_variables_names.extend(
                get_nouns_of_variables_names_in_path(path_to_analyze)
            )
        else:
            rootLogger.warning('"%s" NOT EXISTS' % path_to_analyze)

    rootLogger.info(
        'TOTAL NOUNS IN VARIABLES MANES: %s nouns, %s unique' % (
            len(limit_top_size_partitions_of_nouns_of_variables_names),
            len(set(limit_top_size_partitions_of_nouns_of_variables_names))
        )
    )

    for word_item, occurence in collections.Counter(
            limit_top_size_partitions_of_nouns_of_variables_names).most_common(limit_top_size):
        rootLogger.info(
            '%s: %s' % (
                word_item,
                occurence
            )
        )
