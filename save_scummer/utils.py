"""Misc utility functions"""
from datetime import datetime
from pathlib import Path
from typing import List, Union

StrOrPath = Union[Path, str]


def get_latest_modified(paths: List[Path]) -> datetime:
    """Get the most recent 'modified on' timestamp (ISO format) from the paths given.
    For a save directory with multiple files, this is the best indicator of when the save was
    created, as not all files may be modified with each save.
    """
    datetimes = [datetime.fromtimestamp(path.stat().st_mtime) for path in paths]
    return max(datetimes).replace(microsecond=0)


def normalize_path(path: StrOrPath) -> Path:
    return Path(path).expanduser().resolve()
