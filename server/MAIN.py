import argparse
import os
import server.FileService as FileService
import logging
import sys
import traceback
import configparser
from Singleton import singleton


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

def main():
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


if __name__ == "__main__":
    main()






