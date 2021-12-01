import configparser
import os
import argparse

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
        #self.process_arguments()
        self.config["loglevel"] = "error"

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
        parser.add_argument('-l', '--loglevel', default=self.config.get("log_level", "error").lower(), choices=["debug", "info", "warning", "error"], type=str,
                            help="Logging level, (default: 'error')")

        self.config["args"] = parser.parse_args()

        return None
