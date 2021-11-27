#!/usr/bin/env python3
import argparse
import logging
import logging.config
import os
import sys

import server.FileService as FileService
import server.Config as Config


def setup_logger(level='NOTSET', filename=None):
    config = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': level,
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
    if filename:
        config['handlers']['file'] = {
            'class': 'logging.FileHandler',
            'encoding': 'UTF-8',
            'formatter': 'default',
            'filename': filename,
        }
        config['root']['handlers'].append('file')
    logging.config.dictConfig(config)


def main():
    config = Config
    x = config.log.level.upper()
    setup_logger(level=logging.getLevelName(Config.log.level.upper()), filename=Config.log.file)
    logging.debug('started')

    FileService.change_dir(Config.dir)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')
    except BaseException as err:
        print(f'ERROR: Something goes wrong:\n{err}')
        sys.exit(1)
