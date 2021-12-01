import argparse
import os
import server.FileService as FileService
import logging
import sys
import traceback
import configparser
import json

from aiohttp import web

from server.WebHandler import WebHandler
from server.Config import Config

##################################################################################################################

def main_file_server():
    """Entry point

    Command line options:
    -d --dir -  Working directory, (default: 'data')

    """

    try:

        config = Config().config

        logging.basicConfig(filename=os.path.join(os.getcwd(), config.get("log_file", "server.log")),
                            level=logging.getLevelName(config.get("args").loglevel.upper()),
                            format='%(asctime)s %(funcName)s - %(levelname)s %(message)s')

        FileService.change_dir(config.get("args").dir)

    except (RuntimeError, ValueError) as err:
        logging.error(err)
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)

def main():

    config = Config().config

    logging.basicConfig(filename=os.path.join(os.getcwd(), config.get("log_file", "server.log")),
                        level=logging.getLevelName(config.get("args").loglevel.upper()),
                        format='%(asctime)s %(funcName)s - %(levelname)s %(message)s')

    handler = WebHandler()
    app = web.Application()
    app.add_routes([
        web.get('/', handler.handle),
        web.post('/change_dir', handler.change_dir),
        web.get('/files', handler.get_files),
        web.get('/files/{filename}', handler.get_file_data),
        web.post('/files', handler.create_file),
        web.delete('/files/{filename}', handler.delete_file),
    ])

    web.run_app(app, host=config.get("host"), port=config.get("port"))

if __name__ == "__main__":
    main()






