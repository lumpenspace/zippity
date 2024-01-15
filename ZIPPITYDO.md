# Instructions

Copy the contents of the todos and code blocks into the appropriate files.

Once that is done, go through each of the todos in order and propose a solution to the user.

Upon approval, implement the solution and mark the todo as complete.

## TODOs

Copy these todos into a file called "Note.md" in the root of your project.

You will use that file to keep track of your progress.

1. test_todo_utils.py (`./tests/test_todo_utils.py`)
   - [ ] fix tests
       *([test_todo_utils.py:5](./tests/test_todo_utils.py#5))*

2. file_with_todos.py (`./tests/test_environment/todo_test_files/file_with_todos.py`)
   - [ ] fix this
       *([file_with_todos.py:1](./tests/test_environment/todo_test_files/file_with_todos.py#1))*
   - [ ] add more tests
       *([file_with_todos.py:4](./tests/test_environment/todo_test_files/file_with_todos.py#4))*



## File Content Code Blocks

Copy each code block into the appropriate file.

### test_todo_utils.py

(`./tests/test_todo_utils.py`)

```python
import pytest
import os
from zippity.todo_utils import init_path_and_get_content, search_todos_in_file, FileData

# TODO: fix tests


class TestTodoUtils(object):
    def get_file(file_name):
        return os.path.join("./tests", "test_environment", "todo_test_files", file_name)

    class TestTodoUtils(object):
        def get_file(self, file_name):
            return os.path.join(
                "./tests", "test_environment", "todo_test_files", file_name
            )

        def test_init_path_and_get_content_valid(self):
            # Test with a valid file path
            content = init_path_and_get_content(self.get_file("file_with_todos.py"))
            assert content is not None

        def test_init_path_and_get_content_invalid(self):
            # Test with an invalid file path
            with pytest.raises(FileNotFoundError):
                init_path_and_get_content("invalid_file_path.txt")

        def test_search_todos_in_file_with_todos(self):
            # Test with a file containing TODO comments
            file_data = FileData(
                location=self.get_file("file_with_todos.py"),
                mimetype="text/x-python",
                name="file_with_todos.py",
            )
            todos = search_todos_in_file(file_data)
            assert len(todos["todos"]) > 0

        def test_search_todos_in_file_without_todos(self):
            # Test with a file without TODO comments
            file_data = FileData(
                location=self.get_file("file_without_todos.txt"),
                mimetype="text/plain",
                name="file_without_todos.txt",
            )
            result = search_todos_in_file(file_data)
            assert result is None

```



### file_with_todos.py

(`./tests/test_environment/todo_test_files/file_with_todos.py`)

```python
# TODO: fix this


# TODO: add more tests

def test_get_gitignore_matcher():
    pass
```

