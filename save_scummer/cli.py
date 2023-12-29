from contextlib import contextmanager
from logging import basicConfig, getLogger

import click
from click_completion import init as init_completion
from click_completion.core import install as install_completion
from click_completion.core import shells
from halo import Halo
from tabulate import tabulate

from save_scummer.backup import get_included_files, make_backup, restore_backup
from save_scummer.config import LOG_PATH, GAMES, add_game, list_game, list_games, normalize_path

basicConfig(filename=LOG_PATH, level='INFO')
init_completion()
logger = getLogger(__name__)

# Param type containing a list of all game titles; used for autocompletion
GameChoice = click.Choice(GAMES)


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


@click.group(context_settings={'help_option_names': ['-h', '--help']}, invoke_without_command=True)
@click.option(
    '--install',
    type=click.Choice(shells),
    help='Install completion script for the specified shell',
)
@click.pass_context
def ssc(ctx, install):
    if ctx.invoked_subcommand:
        pass
    elif install:
        shell, path = install_completion(install)
        click.echo(f'{shell} completion installed in {path}')
    else:
        click.echo(ssc.get_help(ctx))


@ssc.command()
@click.argument('title')
@click.argument('source')
@click.option(
    '-c',
    '--clean-restore',
    default=False,
    help='Delete existing save files before restoring backups',
)
@click.pass_context
def add(ctx, title: str, source: str, clean_restore):
    """Add a game and its save directory.
    Relative paths, user paths, and glob patterns are supported.
    This command can also be used to update a previously added game.

    \b
    Examples:
      ssc add game1 ~/Games/game1           # Add a dir (including any subdirs)
      ssc add game1 '~/Games/game1/**'      # Equivalent glob pattern (quotes required)
      ssc add game2 'C:\\Games\\game2\\*.sav'  # Add files ending in .sav
    """
    included_files = [str(f[1]) for f in get_included_files(source)]
    if not included_files:
        click.secho('Error: No files are in the specified path')
        ctx.exit()

    # If a glob pattern is specified, show the files matched as a sanity check
    if '*' in source:
        click.echo(
            f'This pattern matches the following {len(included_files)} files:\n  '
            + '\n  '.join(included_files)
        )
        click.confirm('Does this look correct?')

    add_game(title, source=source, clean_restore=clean_restore)
    click.echo(f'Source path for "{title}" added: {normalize_path(source)}')


@ssc.command()
@click.argument('title', type=GameChoice, required=False)
def ls(title):
    """List details on all configured games. Or, enter a game title to get more detailed info."""
    if title:
        # TODO: alignment
        game_info = list_game(title, extra_details=True)
        table = '\n'.join(f'{k}: \t{v}' for k, v in game_info.items())
    else:
        table = tabulate(list_games(), headers='keys', tablefmt='fancy_grid')
    click.echo(table)


@ssc.command()
@click.argument('titles', type=GameChoice, nargs=-1)
@click.option('-d', '--description', help='Optional description for this backup')
@click.option(
    '-a',
    '--all',
    help='Make a backup of all configured games',
    default=False,
    is_flag=True,
)
@click.pass_context
def backup(ctx, titles, description, all):
    """Create a backup of one, multiple, or all games

    \b
    Example:
      # Create a single backup
      ssc backup game1
      \b
      # Create a backup with a description
      ssc backup game1 -d 'level 10 with full health'
      \b
      # Backup multiple games
      ssc backup game1 game2
      \b
      # Backup all of the things
      ssc backup --all

    """
    # Exactly one of these args is required (title(s) XOR all)
    if bool(titles) == bool(all):
        click.echo(backup.get_help(ctx))
        ctx.exit(1)

    titles_to_backup = GAMES if all else titles
    for title in titles_to_backup:
        with spin(ctx, 'Creating backup'):
            status = make_backup(title, description)
        click.echo(status)


@ssc.command()
@click.argument('title', type=GameChoice)
@click.option(
    '-i', '--index', help='Backup number (starting at 0, from newest to oldest)', type=click.INT
)
@click.option('-a', '--age', help='Minimum age (relative to current time)')
@click.option('-d', '--date', help='Maximum date/time (absolute)')
@click.option('-f', 'filename', help='Backup filename; either absolute or relative to backup dir')
@click.pass_context
def restore(ctx, title, filename, index, age, date):
    """Restore a backup of the specified game.
    A specific backup can be indicated by backup index, age, date/time, or filename.
    Otherwise, the most recent backup is restored.

    \b
    Notes:
    * Makes a backup of the current save files before overwriting.
    * For time specifiers, the time of the original save is used, not the time
      of the backup.

    \b
    Backup specifiers:
      Index:
        The backup index, sorted from newest to oldest, e.g.
        "Restore the save from x backups ago." 0 is the latest backup, 1 is the
        backup made before that, etc.
        Negative values can also be given; -1 would give you the oldest backup.
        See ls command for full list of available backups.
      Age:
        Minimum age of the save to restore, e.g "I want to go back in time by
        1 hour." Amounts of time can be specified in 'HH:MM' format, or
        with a number followed by a unit.
        Examples:
          * '1:30' (an hour and a half ago)
          * '30m' (or '30 minutes')
          * '6h' (or '6 hours')
          * '9 hours, 15 minutes' (or '9:15')
          * '2d' (or '2 days')
          * See pytimeparse for more formats
      Date/Time:
        Maximum date/time of the save to restore, e.g., "I want to go back in
        time to 1:30 yesterday." Most date/time formats are supported.
        Examples: '16:30' or '4:30 PM' (today), '2021-01-20', 'August 3 2020'
          * '16:30' or '4:30 PM' (today)
          * '2021-01-20'
          * 'August 3 2020'
          * Most date/time formats are supported; see dateutil for more examples
      Filename:
        Either a full path or just the filename (relative to the backup dir)

    \b
    Examples:
      # Just restore the most recent backup
      ssc restore game1
      \b
      # Restore the backup made 2 backups ago (aka the 3rd most recent)
      ssc restore game1 -i 2
      \b
      # Restore a backup from (at least) an hour and a half ago
      ssc restore game1 -a '1:30'
      \b
      # Restore a backup from (at least) 2 days ago
      ssc restore game1 -a 2d
      \b
      # Restore a backup from 4:00 PM today or earlier
      ssc restore game1 -d '4:00 PM'
      \b
      # Restore a backup from March 22 or earlier
      ssc restore game1 -d 'Mar 22 2021'
      \b
      # Restore a backup by filename
      ssc restore game1 -f game1-2021-01-20T00:09:10.zip
    """
    with spin(ctx, 'Restoring backup'):
        status = restore_backup(title, filename, index, age, date)
    click.echo(status)
