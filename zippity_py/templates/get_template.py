"""
Get the template.
"""

import os

from enum import Enum
from typing import Any, Dict, Type

from zippity_py.todos.todo_utils import FileTodos


class TemplateType(Enum):
    """
    The type of template to get.
    """

    TODO = "todo"
    REPORT = "report"


template_input_types: dict[TemplateType, Type[Any]] = {
    TemplateType.TODO: FileTodos,
}


class TemplateHandler:
    """
    The dictionary of template input types.
    """

    def __init__(self, template_type: TemplateType):
        super().__init__()
        self.template_type: TemplateType = template_type
        self.input_type: Type[Any] = template_input_types[template_type]

    def get_template(self) -> str:
        """
        Get the template.
        """
        with open(
            os.path.join(
                os.path.dirname(__file__),
                f"{self.template_type.value}_template.md.jinja",
            ),
            "r",
            encoding="utf-8",
        ) as file:
            return file.read()
