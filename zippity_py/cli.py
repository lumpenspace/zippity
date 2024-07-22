"""CLI for `zpt`, the Zippity Python CLI."""

# pylint: disable=missing-function-docstring

import logging
import os
import functools
from typing import Any, Callable, Generator, List

import click
from clipboard_maximizer import copy_to_clipboard

from .cli_utils import p
from .fs_utils import collect_files, FileData
from .templates import render_todo
from .todos.todo_utils import Todo, collect_todos_from_file

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("gitignore_parser").setLevel(logging.WARNING)

default_suffixes: list[str] = [".py", ".js", ".ts", ".tsx"]


@click.group()
def cli() -> None:
    pass


def common_params(func: Callable[..., Any]) -> Callable[..., Any]:
    """Common parameters for the CLI."""

    @click.argument(
        "source_directory",
        type=click.Path(exists=True, file_okay=False, readable=True),
        default=os.getcwd(),
        help="The directory to search.",
    )
    @click.option("--extensions", "-e", multiple=True, default=default_suffixes)
    @click.option(
        "--result_file",
        "-r",
        type=click.Path(file_okay=True, writable=True),
        default="./ZIPPITYDO.md",
        help="The path to the file to write the result.",
    )
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper


def main() -> None:
    """Main entry point for the CLI."""

    @click.command()
    @common_params
    @click.option(
        "--template_path",
        "-t",
        type=click.Path(exists=True, file_okay=True, readable=True, dir_okay=False),
        default="./templates/default.md",
        help="The path to the template to use.",
    )
    def main_inner(
        source_directory: str,
        extensions: List[str],
        result_path: str,
        template_path: str,
    ) -> list[Todo] | None:
        """Main entry point for the CLI."""
        files: Generator[FileData, None, None] = collect_files(
            source_directory, extensions=extensions
        )

        todos: List[Todo] = []
        for file in files:
            todos.extend(collect_todos_from_file(file))

        with open(result_path, "w", encoding="utf-8") as outfile:
            filename = click.format_filename(result_path)
            p(f"📋 TODOs written to: \b{filename}", c="green", b=True)
            outfile.write(render_todo(todos, template_path))

            copy_to_clipboard(outfile.read())
            return

    main_inner(
        source_directory=os.getcwd(),
        extensions=[".py", ".js", ".ts", ".tsx"],
        result_path="./ZIPPITYDO.md",
        template_path="./templates/default.md",
    )
