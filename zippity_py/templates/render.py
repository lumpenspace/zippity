"""
Utilities to render templates.
"""

import os
from jinja2 import Environment, FileSystemLoader

from zippity_py.todos.todo_utils import FileTodos


def default_template() -> str:
    """
    Get the default template.
    """
    with open(
        os.path.join(os.path.dirname(__file__), "todo_template.md.jinja"),
        "r",
        encoding="utf-8",
    ) as file:
        return file.read()


def render(result: FileTodos, template_file: str | None = None) -> str:
    """
    Render the template.
    """
    if template_file:
        template_loader = FileSystemLoader(searchpath=os.path.dirname(template_file))
        template_env = Environment(loader=template_loader)
        template = template_env.get_template(os.path.basename(template_file))
    else:
        template_env = Environment()
        template = template_env.from_string(default_template())

    return template.render(result=result)
