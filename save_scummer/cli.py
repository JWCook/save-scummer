from contextlib import contextmanager
from logging import basicConfig, getLogger

import click
from halo import Halo
from tabulate import tabulate

from save_scummer.backup import get_included_files, make_backup, restore_backup
from save_scummer.config import add_game, list_games, normalize_path

basicConfig(filename='save-scummer.log', level='INFO')
logger = getLogger(__name__)


@contextmanager
def spin(ctx, text: str = None):
    """Show a spinner within the wrapped context, handling any errors that occur"""
    spinner = Halo(text, color='magenta', text_color='white')
    with spinner:
        try:
            yield
        # Show 'cancel' symbol on Ctrl-C
        except KeyboardInterrupt:
            spinner.stop_and_persist('🚫')
            ctx.exit(1)
        # On any other error, show the short error message and log the full traceback
        except Exception as e:
            spinner.fail()
            click.secho(str(e), fg='red')
            logger.exception(e)
            ctx.exit(1)
    spinner.succeed()


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
@click.pass_context
@click.argument('game')
@click.argument('description', required=False)
def backup(ctx, game, description):
    """Make a backup of the specified game, optionally with a short description.

    \b
    Example:
      ssc backup game1 'level 10 with full health'
    """
    with spin(ctx, 'Creating backup'):
        status = make_backup(game, description)
    click.echo(status)


@ssc.command()
@click.pass_context
@click.argument('game')
@click.argument(
    'archive_path'
)  # Temporary until I add a better way to specify an individual backup
def restore(game, archive_path):
    """Restore a backup of the specified game"""
    restore_backup(game, archive_path)
