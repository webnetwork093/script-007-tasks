#!/usr/bin/env python3
import logging
import logging.config
import sys

from aiohttp import web

from server.WebHandler import WebHandler
from utils.Config import config


def setup_logger(level='NOTSET', filename=None):
    logger_conf = {
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
        logger_conf['handlers']['file'] = {
            'class': 'logging.FileHandler',
            'encoding': 'UTF-8',
            'formatter': 'default',
            'filename': filename,
        }
        logger_conf['root']['handlers'].append('file')
    logging.config.dictConfig(logger_conf)


def main():
    setup_logger(level=logging.getLevelName(config.log.level.upper()), filename=config.log.file)
    logging.debug('started')
    logging.debug('config %s', config.to_dict())

    handler = WebHandler()
    app = web.Application()
    app.add_routes([
        web.get('/', handler.handle),
        web.post('/change_dir', handler.change_dir),
        web.get('/files', handler.get_files),
        web.get('/files/{filename}', handler.get_file_data),
        web.post('/files/{filename}', handler.create_file),
        web.delete('/files/{filename}', handler.delete_file),
        # TODO: add more routes - done
    ])
    web.run_app(app, port=config.port)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')
    except BaseException as err:
        print(f'ERROR: Something goes wrong:\n{err}')
        sys.exit(1)
