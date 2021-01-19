from pathlib import Path
from typing import Any, Dict, Tuple, Union

import yaml
from appdirs import user_data_dir

DATA_DIR = Path(user_data_dir()).joinpath('save-scummer')
CONFIG_PATH = DATA_DIR.joinpath('config.yml')
DEFAULT_BACKUP_DIR = DATA_DIR.joinpath('backups')
DEFAULT_CONFIG = {'games': {}}

StrOrPath = Union[Path, str]


def add_game(game: str, source_path: str):
    config = read_config()
    config['games'][game] = {'source': source_path}
    write_config(config)


# TODO: Add more formatting as more values are added
def list_games() -> Dict[str, Any]:
    return read_config()['games']


# TODO: Add secondary cloud storage sync dir
def get_game_dirs(game: str) -> Tuple[Path, Path]:
    """Get the source and backup directories for the given game"""
    config = read_config()
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


def read_config() -> Dict[str, Any]:
    """Read config from the config file"""
    if not CONFIG_PATH.is_file():
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        return DEFAULT_CONFIG
    with CONFIG_PATH.open() as f:
        return yaml.safe_load(f)


def write_config(new_config: Dict[str, Any]):
    """Write updated config to the config file"""
    with CONFIG_PATH.open('w') as f:
        yaml.safe_dump(new_config, f)


def normalize_path(path: StrOrPath) -> Path:
    return Path(path).expanduser().resolve()
