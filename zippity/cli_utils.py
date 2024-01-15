"""Utilities for the CLI."""

import click

def p(msg, c=None, **kwargs):
    """Print a message to stdout."""
    click.echo(msg, color=c, **kwargs)
