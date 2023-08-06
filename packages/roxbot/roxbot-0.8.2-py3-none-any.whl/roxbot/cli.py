#!/usr/bin/env python3
"""
roxbot CLI
"""

# type: ignore

import click

from roxbot.version import get_version


@click.group()
def cli():
    pass  # pragma: no cover


@cli.command()
def info():
    """Print package info"""
    print(get_version())


cli.add_command(info)

if __name__ == "__main__":
    cli()  # pragma: no cover
