import argparse
import os
import server.FileService as FileService
import logging
import sys
import traceback

def main():
    """Entry point

    Command line options:
    -d --dir -  Working directory, (default: 'data')

    """

    try:

        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--dir', default=os.path.join(os.getcwd(), 'data'), type=str, help="Working directory, (default: 'data')")
        parser.add_argument('-l', '--loglevel', default="ERROR", choices=["DEBUG","INFO","WARNING","ERROR"], type=str, help="Logging level, (default: 'ERROR')")

        params = parser.parse_args()

        logging.basicConfig(filename=os.path.join(os.getcwd(), "server.log"),
                            level=logging.getLevelName(params.loglevel),
                            format='%(asctime)s %(funcName)s - %(levelname)s %(message)s')

        FileService.change_dir(params.dir)

    except (RuntimeError, ValueError) as err:
        logging.error(err)
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)


if __name__ == "__main__":
    main()
