import argparse
import logging
import os
import configparser

from utils.SingletonMeta import singleton
import dotted_dict


class LayeredConfig:
    _logger = None
    _env_prefix = 'SERVER'
    data = None
    _arg_parser = None
    _args = None

    def __init__(self):
        self._logger = logging.getLogger('config')
        self.data = dotted_dict.DottedDict()
        self._set_defaults()
        self._create_parser()

    def _set_defaults(self):
        self.data.update({
            'config': 'config.ini',
            'dir': 'data',
            'log': {
                'level': 'warning',
                'file': None,  # 'server.log'
            }
        })

    def _create_parser(self):
        """Get and parse command line parameters and configure web app.

        Command line options:
        -d --dir       - working directory (absolute or relative path).
           --log-level - set verbosity level
        -l --log-file  - set log filename
        """
        self._arg_parser = argparse.ArgumentParser()
        self._arg_parser.add_argument('-c', '--config', type=str,
                                      help=f'config filename (default: {self.data.config})')
        self._arg_parser.add_argument('-d', '--dir', type=str,
                                      help=f'working directory (default: {self.data.dir})')
        self._arg_parser.add_argument('--log-level', choices=['debug', 'info', 'warning', 'error'],
                                      help=f'Log level to console (default: {self.data.log.level})')
        self._arg_parser.add_argument('-l', '--log-file', type=str, help='Log file.')

    def _read_envvars(self):
        prefix = self._env_prefix.upper()
        self.data.config = os.getenv(f'{prefix}_CONFIG', self.data.config)
        self.data.dir = os.getenv(f'{prefix}_DIR', self.data.dir)
        self.data.log.level = os.getenv(f'{prefix}_LOG_LEVEL', self.data.log.level)
        self.data.log.file = os.getenv(f'{prefix}_LOG_FILE', self.data.log.file)

    def _parse_arguments(self):
        self._args = self._arg_parser.parse_args()

    def _read_config(self):
        if not os.path.exists(self.data.config):
            self._logger.info(f"config file '{self.data.config}' not found")
            return
        with open(self.data.config) as stream:
            ini_parser = configparser.ConfigParser()
            ini_parser.read_string('[default]\n' + stream.read())
            ini_params = ini_parser['default']
            self.data.dir = ini_params.get('dir', self.data.dir)
            self.data.log.level = ini_params.get('log.level', self.data.log.level)
            self.data.log.file = ini_params.get('log.file', self.data.log.file)

    def _read_arguments(self):
        if self._args.dir:
            self.data.dir = self._args.dir
        if self._args.log_level:
            self.data.log.level = self._args.log_level
        if self._args.log_file:
            self.data.log.file = self._args.log_file

    def _validate(self):
        pass

    def update(self):
        self._set_defaults()
        self._read_envvars()
        self._parse_arguments()
        if self._args.config:
            self.data['config'] = self._args.config
        self._read_config()
        self._read_arguments()
        self._validate()

    def dump_config(self):
        # print to sys.file.stdout or specified file
        pass


@singleton
class SingletonConfig:

    def __init__(self):
        self.layered_config = LayeredConfig()
        self.layered_config.update()


config = SingletonConfig().layered_config.data
