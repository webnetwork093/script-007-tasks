import argparse
import os
import server.FileService as FileService
import logging
import sys
import traceback
import configparser

def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance

@singleton
class Config:
    def __init__(self):

        self.config = {}
        self.read_config()
        self.process_arguments()

    def read_config(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(os.getcwd(), 'config.ini'))
        self.config = dict(self.config['DEFAULT'])
        return None

    def process_arguments(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--dir', default=os.path.join(os.getcwd(), 'data'), type=str,
                            help="Working directory, (default: 'data')")
        parser.add_argument('-l', '--loglevel', default="ERROR", choices=["DEBUG", "INFO", "WARNING", "ERROR"], type=str,
                            help="Logging level, (default: 'ERROR')")

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

        logging.debug(config)
        print(config.get("args").loglevel)

        logging.basicConfig(filename=os.path.join(os.getcwd(), config.get("log_file", "server.log")),
                            level=logging.getLevelName(config.get("args").loglevel),
                            format='%(asctime)s %(funcName)s - %(levelname)s %(message)s')

        FileService.change_dir(config.get("args").dir)

    except (RuntimeError, ValueError) as err:
        logging.error(err)
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)


if __name__ == "__main__":
    main()






