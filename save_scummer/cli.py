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
@click.pass_context
@click.argument('game')
@click.argument('path')
def add(ctx, game: str, path: str):
    """Add a game and its save directory.
    Relative paths, user paths, and glob patterns are supported.

    \b
    Examples:
      ssc add game1 ~/Games/game1           # Add a dir (including any subdirs)
      ssc add game1 '~/Games/game1/**'      # Equivalent glob pattern (quotes required)
      ssc add game2 'C:\\Games\\game2\\*.sav'  # Add files ending in .sav
    """
    included_files = [str(f[1]) for f in get_included_files(path)]
    if not included_files:
        click.secho('Error: No files are in the specified path')
        ctx.exit()

    # If a glob pattern is specified, show the files matched as a sanity check
    if '*' in path:
        click.echo(
            f'This pattern matches the following {len(included_files)} files:\n  '
            + '\n  '.join(included_files)
        )
        click.confirm('Does this look correct?')

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


# See [pytimeparse](https://github.com/wroberts/pytimeparse) for all possible formats
# Most date/time formats are supported; see [dateutil](https://dateutil.readthedocs.io/en/stable/examples.html#parse-examples) for more examples
@ssc.command()
@click.pass_context
@click.argument('game')
@click.option(
    '-i', '--index', help='Backup number (starting at 0, from newest to oldest)', type=click.INT
)
@click.option('-a', '--age', help='Minimum age (relative to current time)')
@click.option('-d', '--date', help='Maximum date/time (absolute)')
@click.option('-f', 'filename', help='Backup filename; either absolute or relative to backup dir')
def restore(ctx, game, filename, index, age, date):
    """Restore a backup of the specified game.
    A specific backup can be indicated by backup number, age, date/time, or filename.

    \n
    Notes:
    * Restores the most recent backup by default
    * Makes a backup of the current save files before overwriting.
    * For time specifiers, the time of the original save is used, not the time
      of the backup.

    \b
    Backup specifiers:
      Index:
        The backup index, sorted from newest to oldest, e.g.
        "restore the save from x backups ago." 0 is the latest backup, 1 is the
        backup made before that, etc.
        Negative values can also be given; -1 would give you the oldest backup.
      Age:
        Minimum age of the save to restore, e.g "I want to go back in time by
        (at least) 1 hour." Amounts of time can be specified in 'HH:MM' format, or
        with a number followed by a unit.
        Examples: '1:30' (an hour and a half ago), '30m' (or '30 minutes'),
        '6h' (or '6 hours'), '9 hours, 15 minutes' (or '9:15'), '2d' (or '2 days')
      Date/Time:
        Maximum date/time of the save to restore, e.g., "I want to go back in
        time to 1:30 yesterday (or before)." Most date/time formats are supported.
        Examples: '16:30' or '4:30 PM' (today), '2021-01-20', 'August 3 2020'
      Filename:
        Either a full path or just the filename

    \b
    Examples:
      # Just restore the most recent backup
      ssc restore game1
      \b
      # Restore the backup made 2 backups ago (aka the 3rd most recent)
      ssc restore game1 -i 2
      \b
      # Restore a backup from (at least) an hour and a half ago
      ssc restore -a '1:30'
      \b
      # Restore a backup from (at least) 2 days ago
      ssc restore -a 2d
      \b
      # Restore a backup from 4:00 PM today or earlier
      ssc restore -d '4:00 PM'
      \b
      # Restore a backup from March 22 or earlier
      ssc restore -d 'Mar 22 2021'
      \b
      # Restore a backup by filename
      ssc restore -f game1-2021-01-20T00:09:10.zip
    """
    with spin(ctx, 'Restoring backup'):
        status = restore_backup(game, filename, index, age, date)
    click.echo(status)
