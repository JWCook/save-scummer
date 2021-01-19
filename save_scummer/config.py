from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

import yaml
from appdirs import user_data_dir

from save_scummer.utils import format_timedelta, format_timestamp, get_dir_size, normalize_path

DATA_DIR = Path(user_data_dir()).joinpath('save-scummer')
CONFIG_PATH = DATA_DIR.joinpath('config.yml')
DEFAULT_BACKUP_DIR = DATA_DIR.joinpath('backups')
DEFAULT_CONFIG = {'games': {}}


def add_game(game: str, source_path: str):
    config = read_config()
    config['games'][game] = {'source': source_path}
    write_config(config)


def get_game_dirs(game: str, config: Dict = None) -> Tuple[Path, Path]:
    """Get the source and backup directories for the given game"""
    config = config or read_config()
    source_dir = config['games'].get(game).get('source')
    if not source_dir:
        raise ValueError(f'Game {game} not configured')

    # Get custom backup directory, if different from default
    backup_base_dir = DEFAULT_BACKUP_DIR
    if config.get('backup_dir'):
        backup_base_dir = config['backup_dir']

    backup_dir = Path(backup_base_dir).joinpath(game)
    backup_dir.mkdir(parents=True, exist_ok=True)
    return normalize_path(source_dir), normalize_path(backup_dir)


def list_games() -> Dict[str, Dict[str:Any]]:
    backup_info = {}
    config = read_config()
    for game, metadata in config['games'].items():
        backup_info[game] = {}
        source_pattern, backup_dir = get_game_dirs(game, config)

        if 'last_save_time' not in metadata or 'last_backup_time' not in metadata:
            backup_info[game]['Last backed up'] = 'never'
            continue

        # Format backup size info
        backup_info[game]['Number of backups'] = len(list(backup_dir.iterdir()))
        backup_info[game]['Total backup size'] = get_dir_size(backup_dir)

        # Format last saved/backup info
        save_time = format_timestamp(metadata['last_save_time'])
        backup_time = format_timestamp(metadata['last_backup_time'])
        save_time_elapsed = format_timedelta(metadata['last_save_time'])
        backup_time_elapsed = format_timedelta(metadata['last_backup_time'])
        backup_info[game][f'Last saved'] = f'{save_time} ({save_time_elapsed})'
        backup_info[game][f'Last backed up'] = f'{backup_time} ({backup_time_elapsed})'

    return backup_info


def read_config() -> Dict[str, Any]:
    """Read config from the config file"""
    if not CONFIG_PATH.is_file():
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        return DEFAULT_CONFIG
    with CONFIG_PATH.open() as f:
        return yaml.safe_load(f)


def update_metadata(game: str, last_save_time: datetime):
    """Store metadata for a given game on the date/time of the last save (source) and backup"""
    config = read_config()
    config['games'][game]['last_save_time'] = last_save_time.isoformat()
    config['games'][game]['last_backup_time'] = datetime.now().isoformat()
    write_config(config)


def write_config(new_config: Dict[str, Any]):
    """Write updated config to the config file"""
    with CONFIG_PATH.open('w') as f:
        yaml.safe_dump(new_config, f)
