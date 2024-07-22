"""Utilities for the CLI."""

import os

from typing import Any
import click


def p(msg: str, c: str | None = None, b: bool = False, **kwargs: Any) -> None:
    """Print a message to stdout."""
    click.echo(click.style(msg, fg=c, bold=b), **kwargs)
