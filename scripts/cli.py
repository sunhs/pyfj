from typing import *

import click

from pyfj import jumper, search


@click.group()
def cli():
    ...


@click.command()
@click.argument("patterns", nargs=-1)
def jump(patterns: List[str]):
    j = jumper.Jumper()
    matched = j.jump(patterns)
    print(matched)


@click.command()
@click.argument("patterns", nargs=-1)
def hint(patterns: List[str]):
    j = jumper.Jumper()
    hints = j.hint(patterns)
    print(hints)


cli.add_command(jump)
cli.add_command(hint)


if __name__ == "__main__":
    cli()
