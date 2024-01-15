import os
from zippity_py.fs_utils import (
    get_gitignore_matcher,
    collect_files,
    find_gitignore,
    collect_non_ignored_files,
)
import pytest


@pytest.fixture
def test_files_directory():
    return "./tests/test_environment"  # Update with actual path


@pytest.fixture
def with_gitignore(test_files_directory):
    return os.path.join(
        test_files_directory, "fs_test_files", "directory_with_gitignore"
    )


@pytest.fixture
def without_gitignore(test_files_directory):
    return os.path.join(test_files_directory, "todo_test_files")


def test_get_gitignore_matcher_with_gitignore(with_gitignore):
    # Test with a valid directory containing a `.gitignore` file
    matcher = get_gitignore_matcher(with_gitignore)
    assert matcher is not None


def test_get_gitignore_matcher_without_gitignore(without_gitignore):
    # Test with a directory without a `.gitignore` file
    matcher = get_gitignore_matcher(without_gitignore)
    assert not matcher("")


def test_collect_files_valid(without_gitignore):
    # Test with a valid directory and file extensions
    files = list(collect_files(without_gitignore, [".py", ".txt"]))
    files = [file["name"] for file in files]
    assert len(files) > 0


def test_collect_files_invalid():
    # Test with an empty or invalid directory
    with pytest.raises(Exception):
        list(collect_files("invalid_dir", ["py", "txt"]))


def test_collect_non_ignored_files_valid(without_gitignore):
    # Test with a valid directory and mime matcher
    files = list(
        collect_non_ignored_files(without_gitignore, lambda x: "text/x-python")
    )
    assert len(files) > 0


# Additional test cases for other functions and scenarios can be added here

if __name__ == "__main__" or __name__ == "pytest":
    pytest.main()
