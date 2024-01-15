from typing import List, TypedDict
from comment_parser import comment_parser
from .fs_utils import FileData

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


def init_path_and_get_content(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content


def search_todos_in_file(file: FileData) -> List[Todo]:
    """
    Searches for TODO comments in a file and returns a list of todos.

    Args:
        file (FileData): The file to search for todos.

    Returns:
        List[Todo]: A list of todos found in the file, or None if no todos are found.
    """
    file_content = init_path_and_get_content(file["location"])
    mime = file["mimetype"]
    if mime in [None, False, "text/plain"]:
        return None
    todos = []
    try:
        comments = comment_parser.extract_comments_from_str(
            file_content, mime=mime
        )
    except UnsupportedError as e:
        print(f"Unsupported file type: {mime}")
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
            **file,
        }
    else:
        return None
