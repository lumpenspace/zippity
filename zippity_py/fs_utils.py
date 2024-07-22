"""Filesystem utilities for zippity"""

import os
from typing import Callable, List, TypedDict, Generator
from gitignore_parser import parse_gitignore

from .mime_utils import get_mime_matcher


FileData = TypedDict(
    "FileData",
    {
        "location": str,
        "language": str,
        "mimetype": str,
        "name": str,
    },
)


def get_gitignore_matcher(directory: str) -> Callable[[str], bool]:
    """
    Get a function that matches files against a .gitignore file.
    """
    gitignore = find_gitignore(os.path.abspath(directory))
    return parse_gitignore(gitignore) if gitignore else lambda x: False


def collect_files(
    directory: str, extensions: List[str]
) -> Generator[FileData, None, None]:
    """
    Collects files from a directory based on the specified extensions.

    Args:
        directory (str): The directory to collect files from.
        extensions (List[str]): A list of file extensions to filter the
        collected files.

    Yields:
        FileData: A generator that yields FileData objects representing the
        collected files.

    Raises:
        Exception: If the specified directory is invalid.

    """
    # get ignored files
    if not os.path.isdir(directory):
        raise ValueError(f"Invalid directory: {directory}")
    gitignore_matcher: Callable[[str], bool] = get_gitignore_matcher(directory)
    get_mime: Callable[[str], str | None] = get_mime_matcher(extensions)
    return collect_non_ignored_files(
        directory, lambda x: None if (gitignore_matcher(x)) else get_mime(x)
    )


def check_if_gitignore_exists(directory: str) -> str | None:
    """
    Check if a .gitignore file exists in the specified directory.

    Args:
        directory (str): The directory to check.

    Returns:
        str or None: The path to the .gitignore file if it exists,
        otherwise None.
    """
    gitignore_file: str = os.path.join(directory, ".gitignore")

    return gitignore_file if os.path.isfile(gitignore_file) else None


def find_gitignore(source_directory: str) -> str | None:
    """
    Finds the .gitignore file in the given source directory or its parent
    directories.

    Args:
        source_directory (str): The path to the source directory.

    Returns:
        str or None: The path to the .gitignore file if found, otherwise None.
    """

    launch_dir: str = os.path.abspath(os.getcwd())
    current_dir: str = os.path.abspath(source_directory)

    while True:
        candidate_path: str = os.path.commonpath([current_dir, launch_dir])
        if not candidate_path == launch_dir:
            return candidate_path if os.path.isfile(candidate_path) else None

        gitignore_file: str | None = check_if_gitignore_exists(current_dir)
        if gitignore_file:
            return gitignore_file
        elif current_dir == launch_dir:
            break
        else:
            current_dir = os.path.dirname(current_dir)
            break
    return None


def collect_non_ignored_files(
    directory: str, mime_matcher: Callable[[str], str | None]
) -> Generator[FileData, None, None]:
    """
    Collects non-ignored files in the specified directory
    and its subdirectories.

    Args:
        directory (str): The directory to search for files.
        mime_matcher (callable): A function that determines the MIME type
        of a file.

    Yields:
        dict: A dictionary containing information about each non-ignored file,
        including its location, MIME type, name, and language.
    """
    for root, _, files in os.walk(directory):
        # Filter out ignored files and directories

        for filename in files:
            mime: str | None = mime_matcher(filename)
            if not (mime is None or mime == "text/plain"):
                language: str = mime.split("/")[1].replace("x-", "")
                yield {
                    "location": os.path.join(root, filename),
                    "mimetype": mime,
                    "name": filename,
                    "language": language,
                }


__all__: list[str] = ["collect_files", "FileData"]


def init_path_and_get_content(file_path: str) -> str:
    """Initialize a file path and get its content."""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content
