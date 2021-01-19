from pprint import pformat

import click

from save_scummer.config import add_game, list_games


@click.group()
def ssc():
    pass


@ssc.command()
@click.argument('name')
@click.argument('path', type=click.Path(exists=True, resolve_path=True))
def add(name: str, path: str):
    """Add a game and its save directory"""
    add_game(name, path)
    click.echo(f'Source path for "{name}" added: {path}')


@ssc.command()
def ls():
    """List all currently configured games"""
    click.echo(pformat(list_games(), indent=4))


@ssc.command()
def backup():
    pass


@ssc.command()
def restore():
    pass
