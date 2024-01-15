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
    mime = file['mimetype']
    if mime in [None, False, 'text/plain']:
        return None
    todos = []
    comments = comment_parser.extract_comments_from_str(file_content, mime=file['mimetype'])
    print(comments)
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