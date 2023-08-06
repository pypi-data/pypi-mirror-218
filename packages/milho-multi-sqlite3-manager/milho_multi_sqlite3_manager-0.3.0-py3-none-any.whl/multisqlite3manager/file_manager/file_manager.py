import os
import typing
import glob

MULTISQLITE3MANAGER_FILE_MANAGER_ROOT_PATH_KEY = "MULTISQLITE3MANAGER_FILE_MANAGER_ROOT_PATH"
MULTISQLITE3MANAGER_FILE_MANAGER_ROOT_PATH_DEFAULT = os.getenv(MULTISQLITE3MANAGER_FILE_MANAGER_ROOT_PATH_KEY)
  
def open_file(filename: str, mode: str = 'r', root_path: str = MULTISQLITE3MANAGER_FILE_MANAGER_ROOT_PATH_DEFAULT) -> typing.IO:
    """
        Open a file.
        :param filename: The file name.
        :param mode: The file mode.
        :param root_path: The root path.
        :return: A file object.
    """
    return open(os.path.join(root_path, filename), mode)

def read_file(filename: str, root_path: str = MULTISQLITE3MANAGER_FILE_MANAGER_ROOT_PATH_DEFAULT) -> str:
    """
        Read a file.
        :param filename: The file name.
        :param root_path: The root path.
        :return: A string.
    """
    with open_file(filename, 'r', root_path) as file:
        return file.read()

def read_many_files(filename_pattern: str, root_path: str = MULTISQLITE3MANAGER_FILE_MANAGER_ROOT_PATH_DEFAULT) -> typing.List[str]:
    """
        Read many files using glob pattern.
        :param filename_pattern: The file name pattern.
        :param root_path: The root path.
        :return: A list of strings.
    """
    return [read_file(filename, root_path) for filename in glob.glob(os.path.join(root_path, filename_pattern))]

def print_file_head(filename: str, n: int = 5, root_path: str = MULTISQLITE3MANAGER_FILE_MANAGER_ROOT_PATH_DEFAULT) -> None:
    """
        Print the first n lines of a file.
        :param filename: The file name.
        :param n: The number of lines to print.
        :param root_path: The root path.
    """
    with open_file(filename, 'r', root_path) as file:
        for _ in range(n):
            print(file.readline(), end='')

def print_file_tail(filename: str, n: int = 5, root_path: str = MULTISQLITE3MANAGER_FILE_MANAGER_ROOT_PATH_DEFAULT) -> None:
    """
        Print the last n lines of a file.
        :param filename: The file name.
        :param n: The number of lines to print.
        :param root_path: The root path.
    """
    with open_file(filename, 'r', root_path) as file:
        lines = file.readlines()
        for line in lines[-n:]:
            print(line, end='')