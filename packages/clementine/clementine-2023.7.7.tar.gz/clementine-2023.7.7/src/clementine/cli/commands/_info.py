"""The clementine CLI info commands."""

import click
import pyperclip

from clementine import about
from clementine.env import info as _info


@click.command()
@click.option(
    "--clipboard/--no-clipboard",
    default=False,
    help="Whether to copy the information to the clipboard. Defaults to False.",
)
def info(clipboard):
    """Show information about your environment and clementine installation."""
    env = "\n".join([f"{k}: {v}" for k, v in _info([about.__title__]).items()])
    if clipboard:
        pyperclip.copy(env)
    click.echo(env)
