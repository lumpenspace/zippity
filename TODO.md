# Instructions

## TODOs

Copy these todos into a file called "Note.md" in the root of your project.

You will use that file to keep track of your progress.

1. [ ] comments in a file
    on two line
    *([todo_utils.py:21](zippity/todo_utils.py:21))*
2. [ ]  fix tests
    *([cli.py:8](zippity/cli.py:8))*


## File Content Code Blocks

Copy each code block into the appropriate file.

### todo_utils.py

```python file:zippity/todo_utils.py

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


```

### cli.py

```python file:zippity/cli.py

import os
import click
from gitignore_parser import parse_gitignore
from .todo_utils import search_todos_in_directory
from .git_utils import find_gitignore
from .template import render

# TODO: fix tests

@click.command()
@click.argument('source_directory', type=click.Path(exists=True, file_okay=False, readable=True))
@click.option('--file_types', '-t', multiple=True, default=['.py', '.js', '.ts', '.tsx'])
@click.option('--result_file', '-r', type=click.Path(file_okay=True, writable=True), default='./TODO.md')
@click.option('--template_file', '-f', type=click.Path(exists=True, file_okay=True, readable=True))

def main(source_directory:str='./', file_types=['.py', '.js', '.ts', '.tsx'], result_file='./TODO.md', template_file=None):
    # Read the .gitignore file to get a list of patterns to ignore
    gitignore_file = find_gitignore(os.getcwd(), source_directory)
    matches_ignore = parse_gitignore(gitignore_file) if gitignore_file else lambda x: False

    # Search for TODO comments and build the document
    todos = search_todos_in_directory(source_directory, matches_ignore, file_types)

    if (len(todos) == 0):
        print("No TODOs found.")
        exit(0)

    print(f"Found {len(todos)} TODOs.")


    # Write the document to the result file
    with open(result_file, 'w', encoding='utf-8') as result:
        output = render(todos, template_file)
        result.write(output)
    
    exit(0)

if __name__ == '__main__':
    main()

```

