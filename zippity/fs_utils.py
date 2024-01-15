"""Filesystem utilities for zippity"""

import os
from typing import List, TypedDict, Generator
from gitignore_parser import parse_gitignore
from .file_extensions import get_mime_matcher


FileData = TypedDict('FileData', {
    'language': str,
    'mimetype': str,
    'name': str,
})

def get_gitignore_matcher(directory:str) -> callable:
    gitignore = find_gitignore(os.path.abspath(directory))
    return parse_gitignore(gitignore) if gitignore else lambda x: False

def collect_files(directory:str, extensions:List[str]) -> Generator[FileData, None, None]:
    # get ignored files
    if not os.path.isdir(directory):
        raise Exception(f"Invalid directory: {directory}")
    gitignore_matcher = get_gitignore_matcher(directory)
    get_mime = get_mime_matcher(extensions)
    return collect_non_ignored_files(directory, lambda x: None if (gitignore_matcher(x)) else get_mime(x) )

def check_if_gitignore_exists(directory:str) -> str or None:
    gitignore_file = os.path.join(directory, '.gitignore')
        
    return gitignore_file if os.path.isfile(gitignore_file) else None

def find_gitignore(source_directory:str) -> str or None:

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

def collect_non_ignored_files(directory:str, mime_matcher:callable) -> Generator[FileData, None, None]:
    for root, dirs, files in os.walk(directory):
        # Filter out ignored files and directories

        for filename in files:
    
            mime = mime_matcher(filename)
            if not(mime == None or mime == False or mime == 'text/plain' or mime == True):
                language = mime.split('/')[1].replace('x-', '')
                yield { "location": os.path.join(root, filename), "mimetype": mime, "name": filename, "language": language }
