from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml
from appdirs import user_data_dir

from save_scummer.utils import format_timestamp, get_dir_files_by_date, get_dir_size, normalize_path

DATA_DIR = Path(user_data_dir()).joinpath('save-scummer')
CONFIG_PATH = DATA_DIR.joinpath('config.yml')
DEFAULT_BACKUP_DIR = DATA_DIR.joinpath('backups')
DEFAULT_CONFIG = {'games': {}}


def read_config() -> Dict[str, Any]:
    """Read config from the config file"""
    if not CONFIG_PATH.is_file():
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        return DEFAULT_CONFIG
    with CONFIG_PATH.open() as f:
        return yaml.safe_load(f)


CONFIG = read_config()


def add_game(game: str, source: str, clean_restore: bool = False):
    CONFIG['games'].setdefault(game, {})
    CONFIG['games'][game]['source'] = source
    CONFIG['games'][game]['clean_restore'] = clean_restore
    write_config(CONFIG)


def get_game_dirs(game: str) -> Tuple[Path, Path]:
    """Get the source and backup directories for the given game"""
    source_dir = CONFIG['games'].get(game).get('source')
    if not source_dir:
        raise ValueError(f'Game {game} not configured')

    # Get custom backup directory, if different from default
    backup_base_dir = CONFIG.get('backup_dir') or DEFAULT_BACKUP_DIR

    backup_dir = Path(backup_base_dir).joinpath(game)
    backup_dir.mkdir(parents=True, exist_ok=True)
    return normalize_path(source_dir), normalize_path(backup_dir)


def list_games() -> List[Dict[str, str]]:
    """Get formatted info on configured games and their backups

    Returns:
        A list of dicts containing formatted metadata
    """
    return [list_game(game) for game in CONFIG['games']]


def list_game(game: str, extra_details: bool = False) -> Dict[str, str]:
    """Get formatted info on a single game and its backups"""
    metadata = CONFIG['games'][game]
    source_pattern, backup_dir = get_game_dirs(game)
    backup_files = get_dir_files_by_date(backup_dir)

    # Format backup size and date/time info
    game_info = {
        'Game': game,
        'Total backups': f'{len(backup_files)} ({get_dir_size(backup_dir)})',
        'Last saved': format_timestamp(metadata.get('last_save_time')),
        'Last backed up': format_timestamp(metadata.get('last_backup_time')),
    }

    if extra_details:
        game_info['Source directory'] = source_pattern
        game_info['Backup directory'] = backup_dir
        formatted_files = [f'{i}:\t {f.name}' for i, f in enumerate(backup_files)]
        game_info['Backup files'] = '\n' + '\n'.join(formatted_files)

    return game_info


def update_metadata(game: str, last_save_time: datetime):
    """Store metadata for a given game on the date/time of the last save (source) and backup"""
    CONFIG['games'][game]['last_save_time'] = last_save_time.isoformat()
    CONFIG['games'][game]['last_backup_time'] = datetime.now().isoformat()
    write_config(CONFIG)


def write_config(new_config: Dict[str, Any]):
    """Write updated config to the config file"""
    with CONFIG_PATH.open('w') as f:
        yaml.safe_dump(new_config, f)
