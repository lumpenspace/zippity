"""Filesystem utilities for zippity"""

import os
from typing import List, TypedDict, Generator
from gitignore_parser import parse_gitignore
from .file_extensions import get_mime_matcher


FileData = TypedDict(
    "FileData",
    {
        "language": str,
        "mimetype": str,
        "name": str,
    },
)


def get_gitignore_matcher(directory: str) -> callable:
    gitignore = find_gitignore(os.path.abspath(directory))
    return parse_gitignore(gitignore) if gitignore else lambda x: False


def collect_files(
    directory: str, extensions: List[str]
) -> Generator[FileData, None, None]:
    """
    Collects files from a directory based on the specified extensions.

    Args:
        directory (str): The directory to collect files from.
        extensions (List[str]): A list of file extensions to filter the collected files.

    Yields:
        FileData: A generator that yields FileData objects representing the collected files.

    Raises:
        Exception: If the specified directory is invalid.

    """
    # get ignored files
    if not os.path.isdir(directory):
        raise Exception(f"Invalid directory: {directory}")
    gitignore_matcher = get_gitignore_matcher(directory)
    get_mime = get_mime_matcher(extensions)
    return collect_non_ignored_files(
        directory, lambda x: None if (gitignore_matcher(x)) else get_mime(x)
    )


def check_if_gitignore_exists(directory: str) -> str or None:
    """
    Check if a .gitignore file exists in the specified directory.

    Args:
        directory (str): The directory to check.

    Returns:
        str or None: The path to the .gitignore file if it exists, otherwise None.
    """
    gitignore_file = os.path.join(directory, ".gitignore")

    return gitignore_file if os.path.isfile(gitignore_file) else None


def find_gitignore(source_directory: str) -> str or None:
    """
    Finds the .gitignore file in the given source directory or its parent directories.

    Args:
        source_directory (str): The path to the source directory.

    Returns:
        str or None: The path to the .gitignore file if found, otherwise None.
    """

    launch_directory = os.path.abspath(os.getcwd())
    current_dir = os.path.abspath(source_directory)

    while True:
        if not os.path.commonpath([current_dir, launch_directory]) == launch_directory:
            return check_if_gitignore_exists(current_dir)

        gitignore_file = check_if_gitignore_exists(current_dir)
        if gitignore_file:
            return gitignore_file
        elif current_dir == launch_directory:
            break
        else:
            current_dir = os.path.dirname(current_dir)
            break
    return None


def collect_non_ignored_files(
    directory: str, mime_matcher: callable
) -> Generator[FileData, None, None]:
    """
    Collects non-ignored files in the specified directory and its subdirectories.

    Args:
        directory (str): The directory to search for files.
        mime_matcher (callable): A function that determines the MIME type of a file.

    Yields:
        dict: A dictionary containing information about each non-ignored file, including its location, MIME type, name, and language.
    """
    for root, dirs, files in os.walk(directory):
        # Filter out ignored files and directories

        for filename in files:
            mime = mime_matcher(filename)
            if not (
                mime == None or mime == False or mime == "text/plain" or mime == True
            ):
                language = mime.split("/")[1].replace("x-", "")
                yield {
                    "location": os.path.join(root, filename),
                    "mimetype": mime,
                    "name": filename,
                    "language": language,
                }
