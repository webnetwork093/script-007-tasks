import argparse
import os
import server.FileService as FileService
import logging
import sys
import traceback
import configparser
from Singleton import singleton
import json

from aiohttp import web

from server.WebHandler import WebHandler

@singleton
class Config:
    def __init__(self):

        self.config = {}
        self.read_config()
        self.process_arguments()

    def read_config(self) -> None:
        self.config = configparser.ConfigParser()

        with open(os.path.join(os.getcwd(), 'config.ini')) as stream:
            self.config.read_string('[default]\n' + stream.read())

        self.config = dict(self.config['default'])
        return None

    def process_arguments(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--dir', default=os.path.join(os.getcwd(), 'data'), type=str,
                            help="Working directory, (default: 'data')")
        parser.add_argument('-l', '--loglevel', default=self.config.get("log_level","error").lower(), choices=["debug", "info", "warning", "error"], type=str,
                            help="Logging level, (default: 'error')")

        self.config["args"] = parser.parse_args()

        return None

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
        web.post('/files/{filename}', handler.create_file),
        web.delete('/files/{filename}', handler.delete_file),
    ])

    web.run_app(app, host=config.get("host"), port=config.get("port"))

if __name__ == "__main__":
    main()






