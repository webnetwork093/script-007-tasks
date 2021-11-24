#!/usr/bin/env python3
import argparse
import os

import server.FileService as FileService


def main():
    """Entry point of app.

    Get and parse command line parameters and configure web app.

    Command line options:
    -f --folder - working directory (absolute or relative path, default: current app folder).
    -h --help - help.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', default=os.path.join(os.getcwd(), 'data'), type=str,
                        help="working directory (default: 'data' folder)")

    params = parser.parse_args()
    FileService.change_dir(params.folder)


if __name__ == '__main__':
    main()
