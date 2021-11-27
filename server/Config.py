import argparse
import logging
import os
import configparser

from utils.SingletonMeta import singleton
import dotted_dict


@singleton
class Config:
    _logger = None
    _env_prefix = 'SERVER'
    _data = None
    _arg_parser = None
    _args = None

    def __new__(cls):
        cls._logger = logging.getLogger('config')
        cls._data = dotted_dict.DottedDict()
        cls._create_parser()

    @classmethod
    def _set_defaults(cls):
        cls._data.update({
            'config': 'config.ini',
            'dir': 'data',
            'log': {
                'level': 'warning',
                'file': None,  # 'server.log'
            }
        })

    @classmethod
    def _create_parser(cls):
        """Get and parse command line parameters and configure web app.

        Command line options:
        -d --dir       - working directory (absolute or relative path).
           --log-level - set verbosity level
        -l --log-file  - set log filename
        """
        cls._arg_parser = argparse.ArgumentParser()
        cls._arg_parser.add_argument('-c', '--config', type=str,
                                     help=f'config filename (default: {cls._data.config})')
        cls._arg_parser.add_argument('-d', '--dir', type=str,
                                     help=f'working directory (default: {cls._data.dir})')
        cls._arg_parser.add_argument('--log-level', choices=['debug', 'info', 'warning', 'error'],
                                     help=f'Log level to console (default: {cls._data.log.level})')
        cls._arg_parser.add_argument('-l', '--log-file', type=str, help='Log file.')

    @classmethod
    def _read_envvars(cls):
        prefix = cls._env_prefix.upper()
        cls._data.config = os.getenv(f'{prefix}_CONFIG', cls._data.config)
        cls._data.dir = os.getenv(f'{prefix}_DIR', cls._data.dir)
        cls._data.log.level = os.getenv(f'{prefix}_LOG_LEVEL', cls._data.log.level)
        cls._data.log.file = os.getenv(f'{prefix}_LOG_FILE', cls._data.log.file)

    @classmethod
    def _parse_arguments(cls):
        cls._args = cls._arg_parser.parse_args()

    @classmethod
    def _read_config(cls):
        if not os.path.exists(cls._data.config):
            cls._logger.warning(f"config file '{cls._data.config}' not found")
            return
        with open(cls._data.config) as stream:
            ini_parser = configparser.ConfigParser()
            ini_parser.read_string('[default]\n' + stream.read())
            ini_params = ini_parser['default']
            cls._data.dir = ini_params.get('dir', cls._data.dir)
            cls._data.log.level = ini_params.get('log.level', cls._data.log.level)
            cls._data.log.file = ini_params.get('log.file', cls._data.log.file)

    @classmethod
    def _read_arguments(cls):
        if cls._args.dir:
            cls._data.dir = cls._args.dir
        if cls._args.log_level:
            cls._data.log.level = cls._args.log_level
        if cls._args.log_file:
            cls._data.log.file = cls._args.log_file

    @classmethod
    def _validate(cls):
        pass

    @classmethod
    def update(cls):
        cls._set_defaults()
        cls._read_envvars()
        cls._parse_arguments()
        if cls._args.config:
            cls._data['config'] = cls._args.config
        cls._read_config()
        cls._read_arguments()
        cls._validate()

    @classmethod
    def dump_config(cls):
        # print to sys.file.stdout or specified file
        pass

    @classmethod
    def __setitem__(cls, key, value):
        cls._data.__setitem__(key, value)

    @classmethod
    def __getitem__(cls, key):
        return cls._data.__getitem__(key)
