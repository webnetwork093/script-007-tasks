import argparse
import os
import server.FileService as FileService
import logging

format = '%(asctime)s %(funcName)s - %(levelname)s %(message)s'

def main():
    """Entry point

    Command line options:
    -d --dir -  Working directory, (default: 'data')

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', default=os.path.join(os.getcwd(), 'data'), type=str, help="Working directory, (default: 'data')")
    parser.add_argument('-l', '--loglevel', default=logging.getLevelName("ERROR"), type=str, help="Logging level, (default: 'ERROR')")

    params = parser.parse_args()

    logging.basicConfig(filename=os.path.join(os.getcwd(), "server.log"), level=logging.getLevelName(params.loglevel), format=format)

    logging.debug("debug")
    logging.error("error")
    logging.info("info")

    FileService.change_dir(params.dir)

if __name__ == "__main__":
    main()
