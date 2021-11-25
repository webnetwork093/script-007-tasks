import argparse
import os
import FileService

def main():
    """Entry point

    Command line options:
    -d --dir -  Working directory, (default: 'data')

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', default=os.path.join(os.getcwd(), 'data'), type=str, help="Working directory, (default: 'data')")

    params = parser.parse_args()
    print(params.dir)
    FileService.change_dir(params.dir)

if __name__ == "__main__":
    main()
