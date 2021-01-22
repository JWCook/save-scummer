"""Misc utility functions"""
from datetime import datetime
from dateutil.parser import parse as parse_date
from os.path import getmtime
from pathlib import Path
from typing import Iterable, List, Union

StrOrPath = Union[Path, str]
DATETIME_FORMAT = '%Y-%m-%d %H:%M'


def format_file_size(n_bytes: int) -> str:
    """Given a number of bytes, return in human-readable format"""
    filesize = float(n_bytes)
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if filesize >= 1024 and unit != 'TB':
            filesize /= 1024
        else:
            return f'{filesize:.2f} {unit}'
    return f'{filesize:.2f} {unit}'


def format_timestamp(timestamp: str) -> str:
    """Reformat a datetime string into a common format, along with time elapsed since that time.

    Time elapsed is in human-readable form, e.g. "5 minutes ago" or "2 days ago."
    Adapted from: https://stackoverflow.com/a/1551394
    """
    if not timestamp:
        return 'never'
    dt = parse_date(timestamp)
    diff = datetime.now() - dt

    if diff.days == 0:
        if diff.seconds < 60:
            time_elapsed = f'{diff.seconds} seconds ago'
        elif diff.seconds < 3600:
            time_elapsed = f'{int(diff.seconds / 60)} minutes ago'
        else:
            time_elapsed = f'{int(diff.seconds / 3600)} hours ago'
    elif diff.days == 1:
        time_elapsed = 'yesterday'
    else:
        time_elapsed = f'{diff.days} days ago'

    return f'{dt.strftime(DATETIME_FORMAT)} ({time_elapsed})'


def get_dir_files_by_date(path: Path = None) -> List[Path]:
    """Get all backup files for the specified game (or directory), sorted by creation date (desc)"""
    try:
        files = list(Path(path).iterdir())
    except IOError:
        return []
    return sorted(files, key=getmtime, reverse=True)


def get_dir_size(path: Path) -> str:
    """Get (non-recursive) sum of file sizes in the given directory, in human-readable format"""
    try:
        file_sizes = [f.stat().st_size for f in path.iterdir()]
    except IOError:
        return '0 bytes'
    return format_file_size(sum(file_sizes))


def get_latest_modified(paths: Iterable[Path]) -> datetime:
    """Get the most recent 'modified on' timestamp (ISO format) from the paths given.
    For a save directory with multiple files, this is the best indicator of when the save was
    created, as not all files may be modified with each save.
    """
    datetimes = [datetime.fromtimestamp(path.stat().st_mtime) for path in paths]
    return max(datetimes).replace(microsecond=0)


def normalize_path(path: StrOrPath) -> Path:
    return Path(path).expanduser().resolve()
