import click
from tabulate import tabulate

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
    Relative paths, user paths, and glob patterns are supported.

    \b
    Examples:
      ssc add game1 ~/Games/game1           # Add a dir (including any subdirs)
      ssc add game1 '~/Games/game1/**'      # Equivalent glob pattern (quotes required)
      ssc add game2 'C:\\Games\\game2\\*.sav'  # Add files ending in .sav
    """
    if not get_included_files(path):
        click.secho('Error: No files are in the specified path')
    else:
        add_game(game, path)
        click.echo(f'Source path for "{game}" added: {normalize_path(path)}')


@ssc.command()
def ls():
    """List all currently configured games"""
    table = tabulate(list_games(), headers='keys', tablefmt='fancy_grid')
    click.echo(table)


@ssc.command()
@click.argument('game')
@click.argument('description')
def backup(game, description):
    """Make a backup of the specified game, optionally with a short description.

    \b
    Example:
      ssc backup game1 'level 10 with full health'
    """
    make_backup(game, description)


@ssc.command()
@click.argument('game')
@click.argument(
    'archive_path'
)  # Temporary until I add a better way to specify an individual backup
def restore(game, archive_path):
    """Restore a backup of the specified game"""
    restore_backup(game, archive_path)
