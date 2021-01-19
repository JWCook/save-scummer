from pprint import pformat

import click

from save_scummer.backup import get_included_files, make_backup, restore_backup
from save_scummer.config import add_game, list_games, normalize_path


@click.group()
def ssc():
    pass


@ssc.command()
@click.argument('game')
@click.argument('path')
def add(game: str, path: str):
    """Add a game and its save directory.

    \b
    Relative paths, user paths, and glob patterns are supported:
    ssc add mygame ~/Games/mygame       # Add a dir (including subdirs) under user home
    ssc add mygame '~/Games/mygame/**'  # Equivalent glob pattern
    ssc add 'C:/Games/mygame/*.sav'     # Add files ending in .sav
    """
    if not get_included_files(path):
        click.secho('Error: No files are in the specified path')
    else:
        add_game(game, path)
        click.echo(f'Source path for "{game}" added: {normalize_path(path)}')


@ssc.command()
def ls():
    """List all currently configured games"""
    click.echo(pformat(list_games(), indent=4))


@ssc.command()
@click.argument('game')
def backup(game):
    """Make a backup of the specified game"""
    make_backup(game)


@ssc.command()
@click.argument('game')
@click.argument(
    'archive_path'
)  # Temporary until I add a better way to specify an individual backup
def restore(game, archive_path):
    """Restore a backup of the specified game"""
    restore_backup(game, archive_path)
