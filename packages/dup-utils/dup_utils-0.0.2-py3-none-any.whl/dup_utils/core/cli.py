from __future__ import annotations

import sys
from pathlib import Path

import click

from .scripts.git import cli_git
from .scripts.version import cli_vs


@click.group()
def cli():
    """A simple command line tool."""
    pass  # pragma: no cover.


@cli.command()
@click.option(
    "-p",
    "--path",
    type=click.Path(exists=True, resolve_path=True),
    default=".",
)
def ls(path: str):
    """List files in Current Path"""
    for file in Path(path).glob("*"):
        print(f"> {file.resolve()}")
    sys.exit(0)


@cli.command()
def say():
    """Say Hello World"""
    sys.exit("Hello World")


def main() -> None:
    cli.add_command(cli_git)
    cli.add_command(cli_vs)
    cli.main()


if __name__ == "__main__":
    main()
