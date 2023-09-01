#!/usr/bin/env python3
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


@click.command()
def clean():
    j = jumper.Jumper()
    j.clean()


cli.add_command(jump)
cli.add_command(hint)
cli.add_command(clean)


if __name__ == "__main__":
    cli()
