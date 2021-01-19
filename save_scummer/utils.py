"""Misc utility functions"""
from datetime import datetime
from dateutil.parser import parse as parse_date
from pathlib import Path
from typing import List, Union

StrOrPath = Union[Path, str]
DATETIME_FORMAT = '%Y-%m-%d %H:%M'


def format_timedelta(compare_timestamp: str) -> str:
    """Get the time elapsed since the specified timestamp in human-readable form,
    e.g. "5 minutes ago" or "2 days ago"
    """
    diff = datetime.now() - parse_date(compare_timestamp)

    if diff.days == 0:
        if diff.seconds < 60:
            return f'{diff.seconds} seconds ago'
        elif diff.seconds < 3600:
            return f'{int(diff.seconds / 60)} minutes ago'
        else:
            return f'{int(diff.seconds / 3600)} hours ago'
    elif diff.days == 1:
        return 'yesterday'
    else:
        return f'{diff.days} days ago'


def format_file_size(n_bytes: int) -> str:
    """Given a number of bytes, return in human-readable format"""
    filesize = n_bytes
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if filesize >= 1024 and unit != 'TB':
            filesize /= 1024
        else:
            return f'{filesize:.2f} {unit}'
    return f'{filesize:.2f} {unit}'


def format_timestamp(timestamp: str) -> str:
    """Reformat a datetime string into a common format"""
    return parse_date(timestamp).strftime(DATETIME_FORMAT)


def get_dir_size(path: Path) -> str:
    """Get (non-recursive) sum of file sizes in the given directory, in human-readable format"""
    file_sizes = [f.stat().st_size for f in path.iterdir()]
    return format_file_size(sum(file_sizes))


def get_latest_modified(paths: List[Path]) -> datetime:
    """Get the most recent 'modified on' timestamp (ISO format) from the paths given.
    For a save directory with multiple files, this is the best indicator of when the save was
    created, as not all files may be modified with each save.
    """
    datetimes = [datetime.fromtimestamp(path.stat().st_mtime) for path in paths]
    return max(datetimes).replace(microsecond=0)


def normalize_path(path: StrOrPath) -> Path:
    return Path(path).expanduser().resolve()
