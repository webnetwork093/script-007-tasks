import logging
import os
import re
import shutil

import utils.TimeUtils as TimeUtils


def _is_unsafe_folder_name(path: str) -> bool:
    # security check
    return bool(re.search(r'(^|[\\/])\.\.($|[\\/])', path))


def change_dir(path: str, autocreate: bool = True) -> None:
    """Change current directory of app.

    Args:
        path (str): Path to working directory with files.
        autocreate (bool): Create folder if it doesn't exist.

    Raises:
        RuntimeError: if directory does not exist and autocreate is False.
        ValueError: if path is invalid.
    """

    if _is_unsafe_folder_name(path):
        raise ValueError('Incorrect value of folder: {}'.format(path))

    if not os.path.exists(path):
        if autocreate:
            os.makedirs(path)
        else:
            raise RuntimeError('Directory {} is not found'.format(path))
    os.chdir(path)
    logging.debug('change working directory to %s', path)


def get_files() -> list:
    """Get info about all files in working directory.

    Returns:
        List of dicts, which contains info about each file. Keys:
        - name (str): filename
        - create_date (datetime): date of file creation.
        - edit_date (datetime): date of last file modification.
        - size (int): size of file in bytes.
    """

    path = os.getcwd()

    # get list of files in `path`
    files = []
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    # collect information about each file
    data = []
    prefix_size = len(path) + 1
    for full_filename in files:
        filename = full_filename[prefix_size:]
        data.append({
            'name': filename,
            'create_date': TimeUtils.floattime_to_datatime(os.path.getctime(full_filename)),
            'edit_date': TimeUtils.floattime_to_datatime(os.path.getmtime(full_filename)),
            'size': os.path.getsize(full_filename),
        })

    return data


def _filename_to_local_path(filename: str, folder_autocreate: bool = False) -> str:
    """Get local path for filename.

    Args:
        filename (str): Filename
        folder_autocreate (bool): Create a subfolder if True

    Returns:
        (str) Local path.

    Raises:
        ValueError: if filename is invalid.
    """

    if _is_unsafe_folder_name(filename):
        raise ValueError('Incorrect value of filename: {}'.format(filename))

    path = os.getcwd()
    full_filename = os.path.join(path, filename)

    folder = os.path.dirname(full_filename)
    if folder_autocreate:
        os.makedirs(folder)

    return full_filename


def get_file_data(filename: str) -> dict:
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

    local_file = _filename_to_local_path(filename)
    if not os.path.exists(local_file):
        raise RuntimeError('File {} does not exist'.format(filename))

    with open(local_file, 'rb') as file_handler:
        return {
            'name': filename,
            'create_date': TimeUtils.floattime_to_datatime(os.path.getctime(local_file)),
            'edit_date': TimeUtils.floattime_to_datatime(os.path.getmtime(local_file)),
            'size': os.path.getsize(local_file),
            'context': file_handler.read(),
        }


def create_file(filename: str, content: str = None) -> dict:
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

    local_file = _filename_to_local_path(filename)

    if os.path.exists(local_file):
        logging.warning('file %s exists', local_file)

    with open(local_file, 'wb') as file_handler:
        if content:
            data = bytes(content)
            file_handler.write(data)

    return {
        'name': filename,
        'create_date': TimeUtils.floattime_to_datatime(os.path.getctime(local_file)),
        'size': os.path.getsize(local_file),
        'content': content,
    }


def delete_file(filename: str) -> None:
    """Delete file.

    Args:
        filename (str): filename

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """

    local_file = _filename_to_local_path(filename)
    if not os.path.exists(local_file):
        raise RuntimeError('File {} does not exist'.format(filename))

    if os.path.isdir(local_file):
        shutil.rmtree(local_file)
    else:
        os.remove(local_file)
