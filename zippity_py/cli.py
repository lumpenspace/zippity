import click
import os
import logging
from typing import List
from clipboard_maximizer import copy_to_clipboard
from .fs_utils import collect_files
from .todo_utils import search_todos_in_file
from .template import render
from .cli_utils import p

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("gitignore_parser").setLevel(logging.WARNING)


@click.command()
@click.argument(
    "source_directory",
    type=click.Path(exists=True, file_okay=False, readable=True),
    default=os.getcwd(),
)
@click.option(
    "--extensions", "-e", multiple=True, default=[".py", ".js", ".ts", ".tsx"]
)
@click.option(
    "--result_file",
    "-r",
    type=click.Path(file_okay=True, writable=True),
    default="./ZIPPITYDO.md",
)
@click.option(
    "--template_file", "-t", type=click.Path(exists=True, file_okay=True, readable=True)
)
def main(
    source_directory: str, extensions: List[str], result_file: str, template_file: str
):
    result = []
    files = collect_files(source_directory, extensions)
    for file in files:
        todos = search_todos_in_file(file)
        if todos:
            result.append(todos)

    if len(result) == 0:
        p(msg="No TODOs found.", c="white")
        return

    p(msg=f"{len(result)} todos found.", c="white")
    # Write the document to the result file
    with open(result_file, "w", encoding="utf-8") as outfile:
        outfile.write(render(result, template_file))

    filename = click.format_filename(result_file)
    p(f"📋 TODOs written to: \b{filename}", c="green", b=True)

    copy_to_clipboard([os.path.abspath(source_directory)])
    return


if __name__ == "__main__":
    main()
