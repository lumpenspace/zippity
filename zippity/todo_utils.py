import os
import re
from typing import List, NamedTuple, TypedDict, Dict
from .file_extensions import get_language_from_file_extension


todo_pattern = re.compile(r'^\s*([^[:alpha:]]*)\s*TODO[\:\s](.*)\n', re.IGNORECASE)

TodoTuple = NamedTuple('TodoTuple', [('line_number', int), ('todo_text', str)])
PathItem = TypedDict('PathItem', {
    'todos': List[TodoTuple],
    'content': str,
    'language': str
})

def init_path_and_get_content(file_path) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

# TODO comments in a file
# on two line
def search_todos_in_file(file_path: str) -> List[TodoTuple]:
    todos:List[TodoTuple] = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            item = todo_pattern.findall(line)
            if (len(item) == 0):
                continue
            [(comment_marker, todo_text)] = item
            next_line = next(file, None).strip()
            print(comment_marker, next_line)
            print(next_line.strip().startswith(comment_marker))
            print(next_line)
            while next_line and next_line.strip().startswith(comment_marker):
                todo_text = f'{todo_text}\n    {next_line[1:].strip()}'
                next_line = next(file, None)
            todos.append(TodoTuple(line_number, todo_text))
    return todos

def get_file_data(root: str, file: str) -> PathItem:
    file_path = os.path.join(root, file)
    todos = search_todos_in_file(file_path)
    
    if len(todos) > 0:
        return (file_path, PathItem({
            'todos': todos,
            'content': init_path_and_get_content(file_path),
            'language': get_language_from_file_extension(file_path)
        }))
    return (file_path, None)

def search_todos_in_directory(directory, matches_ignore: callable, file_extensions: List[str]) -> Dict[str, PathItem]:
    items = {}
    for root, dirs, files in os.walk(directory):
        # Filter out ignored files and directories
        dirs[:] = [d for d in dirs if callable(matches_ignore) and not matches_ignore(os.path.join(root, d))]
        files[:] = [f for f in files if callable(matches_ignore) and not matches_ignore(os.path.join(root, f)) and any(f.endswith(ext) for ext in file_extensions)]
        print(files)
        for file in files:
            (path, item) = get_file_data(root, file)
            if item:
                items[path] = item
    return items

