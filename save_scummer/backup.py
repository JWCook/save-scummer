from glob import glob
from pathlib import Path
from typing import List, Tuple
from zipfile import ZIP_DEFLATED, ZipFile

from save_scummer.config import get_game_dirs, update_metadata
from save_scummer.utils import StrOrPath, format_file_size, get_latest_modified, normalize_path


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


def make_backup(game: str, short_desc: str = None):
    """Make a backup for the specified game. Backup will be named using the time the last save
    was created, optionally with a short description.
    """
    source_pattern, backup_dir = get_game_dirs(game)
    paths = get_included_files(source_pattern)
    if not paths:
        raise ValueError('No files are in the specified path')

    # Determine backup path & filename
    last_save_time = get_latest_modified([path[0] for path in paths])
    if short_desc:
        short_desc = '-' + short_desc.lower().replace(' ', '_')
    archive_path = backup_dir.joinpath(f'{game}-{last_save_time.isoformat()}{short_desc}.zip')

    # Write 'paths' inside archive relative to base (source) path
    with ZipFile(archive_path, 'w', compression=ZIP_DEFLATED) as archive:
        for abs_path, rel_path in paths:
            # print(f'Writing {abs_path} -> {rel_path}')
            archive.write(abs_path, rel_path)

    update_metadata(game, last_save_time)
    archive_size = format_file_size(archive_path.stat().st_size)
    print(f'Backed up {len(paths)} files to {archive_path} ({archive_size} bytes)')


def restore_backup(game, archive_path):
    # First, backup current state
    make_backup(game, short_desc='auto')

    source_dir, backup_dir = get_game_dirs(game)
    with ZipFile(archive_path) as archive:
        archive.extractall(source_dir)

    print(f'Restored backup {archive_path} to {source_dir}')
