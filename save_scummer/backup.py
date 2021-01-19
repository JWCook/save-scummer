from datetime import datetime
from glob import glob
from pathlib import Path
from typing import List, Tuple
from zipfile import ZIP_DEFLATED, ZipFile

from save_scummer.config import StrOrPath, get_game_dirs, normalize_path


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


# TODO: use original file timestamp instead?
def make_backup(game: str, short_desc: str = None):
    # Determine backup path
    source_pattern, backup_dir = get_game_dirs(game)
    timestamp = datetime.now().isoformat()
    suffix = f'-{short_desc}.zip' if short_desc else '.zip'
    archive_path = backup_dir.joinpath(f'{game}-{timestamp}{suffix}')

    # Write 'paths' inside archive relative to base (source) path
    paths = get_included_files(source_pattern)
    with ZipFile(archive_path, 'w', compression=ZIP_DEFLATED) as archive:
        for abs_path, rel_path in paths:
            # print(f'Writing {abs_path} -> {rel_path}')
            archive.write(abs_path, rel_path)

    archive_size = archive_path.stat().st_size
    print(f'Backed up {len(paths)} files to {archive_path} ({archive_size} bytes)')


# TODO: how to specify a specific backup? ID, any nonambiguous relative path/prefix, or full filename?
def restore_backup(game, archive_path):
    # First, backup current state
    make_backup(game, short_desc='auto')

    source_dir, backup_dir = get_game_dirs(game)
    with ZipFile(archive_path) as archive:
        archive.extractall(source_dir)

    print(f'Restored backup {archive_path} to {source_dir}')
