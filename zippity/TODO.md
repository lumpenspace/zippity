# Instructions

Here are some TODOs, followed bys some code blocks.

Your task is to copy the TODOs into a file called "Notes.md" in the root of your project, and then copy the code blocks into the appropriate files.

At that point, you will go through the TODOs and complete them, creating other files as necessary.

## TODOs

Copy these todos into a file called "Notes.md" in the root of your project.

You will use that file to keep track of your progress.

1. [ ] add tests
    *([:18](./todo_utils.py:18))*
2. [ ] add tests
    *([:8](./fs_utils.py:8))*

## File Content Code Blocks

Copy each code block into the appropriate file.

### todo_utils.py

(`./todo_utils.py`)

```python
from typing import List, TypedDict
from comment_parser import comment_parser
from .fs_utils import FileData

Todo = TypedDict('Todo', {
    'line_number': int,
    'text': str,
})

FileTodos = ('FileTodos', {
    'todos': List[Todo],
    'content': str,
    'language': str,
    'mimetype': str,
    'name': str,
    })

# TODO: add tests

def init_path_and_get_content(file_path) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def search_todos_in_file(file: FileData) -> List[Todo]:
    file_content = init_path_and_get_content(file['location'])

    todos = []
    comments = comment_parser.extract_comments_from_str(file_content, mime=file['mimetype'])
    
    for comment in comments:
        if (comment.text().strip().startswith('TODO')):
            todos.append({
                'line_number': comment.line_number(),
                'text': comment.text().replace('TODO:', '').strip(),
            })
    if (len(todos) > 0):
        return {
            'todos': todos,
            'content': file_content,
            **file,
        }
    else:
        return None
```



### fs_utils.py

(`./fs_utils.py`)

```python
"""Filesystem utilities for zippity"""

import os
from typing import List, TypedDict, Generator
from gitignore_parser import parse_gitignore
from .file_extensions import get_mime_matcher

# TODO: add tests

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

```

