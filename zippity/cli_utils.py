"""Utilities for the CLI."""

import click

def p(msg, c=None, b=False, **kwargs):
    """Print a message to stdout."""
    click.echo(click.style(msg, fg=c, bold=b), **kwargs)
               
