import os
import re
import logging
from datetime import datetime

#print(os.path.join(os.getcwd(),"server.log"))
#logging.info('{} + {} = {}'.format(1,3,4))


def check_file_name(filename: str) -> int:
    """Checks filename is valid (for Windows)

    Args:
        filename: base Filename

    Returns: count of invalid symbols in filename

    """
    return len(re.findall("[\\\/\*:\?|<>]", filename)) > 0


def change_dir(path: str, autocreate: bool = True) -> None:
    """Change current directory of app.

    Args:
        path (str): Path to working directory with files.
        autocreate (bool): Create folder if it doesn't exist.

    Raises:
        RuntimeError: if directory does not exist and autocreate is False.
        ValueError: if path is invalid.
    """

    if not os.path.exists(path):
        if autocreate:
            os.makedirs(path, mode=0o777, exist_ok=False)
        else:
            raise RuntimeError("Directory does not exist")
    elif check_file_name(os.path.basename(path)):
        raise ValueError("Directory name is invalid")
    elif not os.path.isdir(path):
        raise ValueError("Path is not directory")

    os.chdir(path)
    logging.debug("Directory changed to " + path)

def get_files() -> list:
    """Get info about all files in working directory.

    Returns:
        List of dicts, which contains info about each file. Keys:
        - name (str): filename
        - create_date (datetime): date of file creation.
        - edit_date (datetime): date of last file modification.
        - size (int): size of file in bytes.
    """

    curr_dir = os.getcwd()
    files = []

    for file in os.listdir(curr_dir):
        if os.path.isfile(file):
            logging.debug("File found: " + file)
            files.append(get_file_data(file))

    return files


def get_file_data(filename: str, get_content: bool = True) -> dict:
    """Get full info about file.

    Args:
        filename (str): Filename.

    Returns:
        Dict, which contains full info about file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - edit_date (datetime): date of last file modification
        - size (int): size of file in bytes

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """
    if check_file_name(os.path.basename(filename)):
        raise ValueError("Filename is invalid")

    if not os.path.exists(filename):
        raise RuntimeError("File does not exist")

    if get_content:
        with open(filename, "r") as file:
            content = file.read()
    else:
        content = ""

    return {"name": os.path.basename(filename),
            "content": content,
            "create_date": datetime.fromtimestamp(os.path.getctime(filename)).strftime('%d.%m.%Y %H:%M:%S'),
            "edit_date": datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%d.%m.%Y %H:%M:%S'),
            "size": os.path.getsize(filename)}


def create_file(filename: str, content: str = "") -> dict:
    """Create a new file.

    Args:
        filename (str): Filename.
        content (str): String with file content.

    Returns:
        Dict, which contains name of created file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - size (int): size of file in bytes

    Raises:
        ValueError: if filename is invalid.
    """
    if check_file_name(os.path.basename(filename)):
        raise ValueError("Filename is invalid")

    with open(filename, "wb") as file:
        file.write(bytearray(content, 'utf-8'))

    return get_file_data(filename)


def delete_file(filename: str) -> None:
    """Delete file.

    Args:
        filename (str): filename

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """

    if check_file_name(os.path.basename(filename)):
        raise ValueError("Filename is invalid")

    if not os.path.exists(filename):
        raise RuntimeError("File does not exist")

    try:
        if os.path.isfile(filename):
            os.remove(filename)
        else:
            os.removedirs(filename)
    except:
        raise RuntimeError("Can't delete file/path")
