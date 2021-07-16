#!/usr/bin/env python
from typing import *

import click

from pyfj import jumper


@click.group()
def cli():
    ...


@click.command()
@click.argument("patterns", nargs=-1)
def jump(patterns: List[str]):
    j = jumper.Jumper()
    matched = j.jump(patterns)
    if matched is None:
        exit(1)
    print(matched)


@click.command()
@click.argument("patterns", nargs=-1)
def hint(patterns: List[str]):
    j = jumper.Jumper()
    hints = j.hint(patterns)
    print("\n".join(hints))


cli.add_command(jump)
cli.add_command(hint)


if __name__ == "__main__":
    cli()
