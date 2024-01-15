"""Filesystem utilities for zippity"""

import os
from typing import List, TypedDict, Generator
from gitignore_parser import parse_gitignore
from .file_extensions import get_mime_matcher

# TODO: Add a test for this

FileData = TypedDict('FileData', {
    'language': str,
    'mimetype': str,
    'name': str,
})

def get_gitignore_matcher(directory:str) -> callable:
    gitignore = find_gitignore(os.getcwd(), directory)
    return parse_gitignore(gitignore) if gitignore else lambda x: False

def collect_files(directory:str, extensions:List[str]) -> Generator[FileData, None, None]:
    # get ignored files
    gitignore_matcher = get_gitignore_matcher(directory)
    get_mime = get_mime_matcher(extensions)

    return collect_non_ignored_files(directory, lambda x: not gitignore_matcher(x) and get_mime(x) )

def find_gitignore(launch_directory:str, source_directory:str) -> str or None:

    current_dir = source_directory
    while True:
        gitignore_file = os.path.join(current_dir, '.gitignore')
        
        if os.path.isfile(gitignore_file):
            return gitignore_file
        elif current_dir == launch_directory:
            break
        else:
            current_dir = os.path.dirname(current_dir)
            break
    return None

def collect_non_ignored_files(directory:str, mime_matcher:callable) -> Generator[FileData, None, None]:
    for root, dirs, files in os.walk(directory):
        # Filter out ignored files and directories
        for filename in files:
            mime = mime_matcher(filename)
            if not mime == None and not mime == False:
                langauge = mime.split('/')[1].replace('x-', '')
                yield { "location": os.path.join(root, filename), "mimetype": mime, "name": filename, "language": langauge }
