from datetime import datetime
from dateutil.parser import parse as parse_date
from glob import glob
from pathlib import Path
from shutil import rmtree
from typing import Dict, List, Tuple, Union
from zipfile import ZIP_DEFLATED, ZipFile

from save_scummer.config import CONFIG, get_game_dirs, update_metadata
from save_scummer.utils import (
    StrOrPath,
    format_file_size,
    get_datetime_by_age,
    get_dir_files_by_date,
    get_latest_modified,
    normalize_path,
)


def get_included_files(source_pattern: StrOrPath) -> List[Tuple[Path, Path]]:
    """Get a list of files to backup, resolving user paths and glob patterns.

    Returns:
        List of ``(absolute_path, relative_path)``
    """
    # Default to recursive include w/ subdirs if a glob pattern is not specified
    source_pattern = str(normalize_path(source_pattern))
    if not source_pattern.endswith('*'):
        source_pattern += '/**'
    base_dir = source_pattern.rsplit('/', 1)[0]

    abs_paths = [normalize_path(path) for path in glob(source_pattern, recursive=True)]
    return [(path, path.relative_to(base_dir)) for path in abs_paths if str(path) != base_dir]


def make_backup(game: str, short_desc: str = None) -> str:
    """Make a backup for the specified game. Backup will be named using the time the last save
    was created, optionally with a short description.

    Returns:
        Status message
    """
    source_pattern, backup_dir = get_game_dirs(game)
    paths = get_included_files(source_pattern)
    if not paths:
        raise ValueError('No files are in the specified path')

    # Determine backup path & filename
    last_save_time = get_latest_modified([path[0] for path in paths])
    if short_desc:
        short_desc = '-' + short_desc.lower().replace(' ', '_')
    archive_path = backup_dir.joinpath(f'{game}-{last_save_time.isoformat()}{short_desc or ""}.zip')

    # Write 'paths' inside archive relative to base (source) path
    with ZipFile(archive_path, 'w', compression=ZIP_DEFLATED) as f:
        for abs_path, rel_path in paths:
            # print(f'Writing {abs_path} -> {rel_path}')
            f.write(abs_path, rel_path)

    update_metadata(game, last_save_time)
    archive_size = format_file_size(archive_path.stat().st_size)
    return f'Backed up {len(paths)} files to {archive_path} ({archive_size})'


def restore_backup(
    game: str, filename: str = None, index: int = None, age: str = None, date: str = None
) -> str:
    """Restore a backup matching the given specification(s).
    Makes a backup of current state before overwriting.

    Args:
        game: Title of game
        filename: Absolute or relative path to backup archive
        index: Index of backup to restore
        age: Min age of backup to restore (as a time expression string)
        date: Max date of backup to restore (as a timestamp string)

    Returns:
        Status message
    """
    source_dir, backup_dir = get_game_dirs(game)
    backups = get_dir_files_by_date(backup_dir)
    backup_paths = list(backups.keys())
    n_backups = len(backup_paths)

    # Choose backup to restore based on specifier(s)
    if filename:
        archive = Path(filename)
    elif index:
        if abs(index) > n_backups:
            raise ValueError(f'Index {index} does not exist; {n_backups} backups are available')
        archive = backup_paths[index]
    elif age:
        archive = get_backup_by_age(backups, age)
    elif date:
        archive = get_backup_by_date(backups, date)
    # If no backup specifiers were given, restore the most recent backup
    else:
        archive = backup_paths[0]

    # First backup current files before overwriting, and delete them if clean_restore is specified
    make_backup(game, short_desc='pre-restore')
    if CONFIG[game]['clean_restore']:
        rmtree(source_dir)

    # Restore the selected backup
    if not archive.is_absolute():
        archive = backup_dir.joinpath(archive)
    source_dir.mkdir(parents=True, exist_ok=True)
    with ZipFile(archive) as f:
        f.extractall(source_dir)

    return f'Restored backup {archive} to {source_dir}'


def get_backup_by_age(backups: Dict[Path, datetime], age: str) -> Path:
    return get_backup_by_date(backups, get_datetime_by_age(age))


def get_backup_by_date(backups: Dict[Path, datetime], target_date: Union[datetime, str]) -> Path:
    if not isinstance(target_date, datetime):
        target_date = parse_date(target_date)

    # Backups are already sorted by date descending; get the first one on or before the target date
    for backup_path, creation_date in backups.items():
        if creation_date <= target_date:
            return backup_path
    raise NotImplementedError
