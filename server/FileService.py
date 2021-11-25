import os
import re

def check_file_name(filename: str) -> int:
    """Checks filename is valid (for Windows)

    Args:
        filename: base Filename

    Returns: count of invalid symbols in filename

    """
    return len(re.findall("[\\\/\*:\?|<>]", filename))


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
    elif check_file_name(os.path.basename(path)) > 0:
        raise ValueError("Directory name is invalid")
    elif not os.path.isdir(path):
        raise ValueError("Path is not directory")

    os.chdir(path)


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
        #file = os.path.join(curr_dir, file)
        if os.path.isfile(file):
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
    if check_file_name(os.path.basename(filename)) > 0:
        raise ValueError("Filename is invalid")

    if not os.path.exists(filename):
        raise RuntimeError("File does not exist")

    if get_content:
        with open(filename, "r") as file:
            content = file.read()

    return {"name": os.path.basename(filename),
            "content": content,
            "create_date": os.path.getctime(filename),
            "edit_date": os.path.getmtime(filename),
            "size": os.path.getsize}


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
    if check_file_name(os.path.basename(filename)) > 0:
        raise ValueError("Filename is invalid")

    with open(filename, "wb") as file:
        file.write(bytearray(content, 'utf-8'))

    return get_file_data(filename)


def delete_file(filename: str) -> bool:
    """Delete file.

    Args:
        filename (str): filename

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """

    if check_file_name(os.path.basename(filename)) > 0:
        raise ValueError("Filename is invalid")

    if not os.path.exists(filename):
        raise RuntimeError("File does not exist")

    try:
        if os.path.isfile(filename):
            os.remove(filename)
        else:
            os.removedirs(filename)
        return True
    except RuntimeError:
        print("Can't delete file/path")
