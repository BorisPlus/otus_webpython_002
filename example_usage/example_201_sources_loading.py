import os
import sys
import logging

from static_code_terms_analyzer.core.sources import (
    LocalFilesystemSource,
    GitHubSource,
)


if __name__ == '__main__':

    rootLogger = logging.getLogger('scta.core.sources')
    rootLogger.setLevel(logging.INFO)
    while rootLogger.handlers:
        rootLogger.handlers.pop()
    logFormatter = logging.Formatter("[%(asctime)s] LOGGER: \"%(name)s\" "
                                     "RUN: %(filename)-15s %(levelname)-8s %(message)s")

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.INFO)
    rootLogger.addHandler(consoleHandler)

    # Test GitHubSource
    try:
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
    except:
        rootLogger.error(sys.exc_info()[1])

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
