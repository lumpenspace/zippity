"""
Todo utils.
"""

from typing import List, TypedDict
from comment_parser import comment_parser
from comment_parser.comment_parser import UnsupportedError
from comment_parser.parsers.common import Comment
from zippity_py.cli_utils import p
from zippity_py.fs_utils import init_path_and_get_content
from ..fs_utils import FileData

Todo = TypedDict(
    "Todo",
    {
        "line_number": int,
        "text": str,
    },
)

FileTodos = TypedDict(
    "FileTodos",
    {
        "todos": List[Todo],
        "content": str,
        "language": str,
        "mimetype": str,
        "name": str,
    },
)


def collect_todos_from_file(file: FileData) -> FileTodos | None:
    """Collect todos and context from files."""
    file_todos: FileTodos | None = search_todos_in_file(file)
    if file_todos is None:
        p(msg=f"No TODOs found in {file.get('name')}", c="white")
        return None

    p(msg=f"{len(file_todos['todos'])} todos found.", c="white")
    return file_todos


def search_todos_in_file(file: FileData) -> FileTodos | None:
    """
    Searches for TODO comments in a file and returns a list of todos.

    Args:
        file (FileData): The file to search for todos.

    Returns:
        List[Todo]: A list of todos found in the file, or None if no todos are found.
    """
    file_content: str = init_path_and_get_content(file["location"])
    mime: str = file["mimetype"]
    if mime in [None, False, "text/plain"]:
        return None
    todos: List[Todo] = []
    try:
        comments: List[Comment] = comment_parser.extract_comments_from_str(
            file_content, mime=mime
        )
    except UnsupportedError as e:
        print(f"Unsupported file type: {mime}, {e}")
        return None

    for comment in comments:
        if comment.text().strip().startswith("TODO"):
            todos.append(
                {
                    "line_number": comment.line_number(),
                    "text": comment.text().replace("TODO:", "").strip(),
                }
            )
    if len(todos) > 0:
        return {
            "todos": todos,
            "content": file_content,
            "language": file["language"],
            "mimetype": file["mimetype"],
            "name": file["name"],
        }
    else:
        return None
