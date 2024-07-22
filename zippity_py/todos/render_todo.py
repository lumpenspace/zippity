"""
Utilities to render templates.
"""

import os
from jinja2 import Environment, FileSystemLoader, Template

from zippity_py.templates.get_template import TemplateHandler, TemplateType
from zippity_py.todos.todo_utils import FileTodos


def render_todo(result: FileTodos, template_file: str | None = None) -> str:
    """
    Render the template.
    """
    if template_file:
        template_loader = FileSystemLoader(searchpath=os.path.dirname(template_file))
        template_env = Environment(loader=template_loader)
        template: Template = template_env.get_template(os.path.basename(template_file))
    else:
        template_env = Environment()
        template: Template = template_env.from_string(
            TemplateHandler(TemplateType.TODO).get_template()
        )

    return template.render(result=result)
