from os import makedirs
from os.path import isfile, join
from typing import Any, Dict, Tuple

import yaml
from appdirs import user_data_dir

DATA_DIR = join(user_data_dir(), 'save-scummer')
CONFIG_PATH = join(DATA_DIR, 'config.yml')
DEFAULT_BACKUP_DIR = join(DATA_DIR, 'backups')
DEFAULT_CONFIG = {'games': {}}


# TODO_ Support multiple paths, glob patterns
def add_game(name: str, source_path: str):
    config = read_config()
    config['games'][name] = {'source': source_path}
    write_config(config)


# TODO: Add more formatting as more values are added
def list_games() -> Dict[str, Any]:
    return read_config()['games']


# TODO: Cloud storage sync dir
def get_game_dirs(name: str) -> Tuple[str, str]:
    """Get the source and backup directories for the given game"""
    config = read_config()
    source_dir = config['games'].get(name).get('source')
    if not source_dir:
        raise ValueError(f'Game {name} not configured')

    # Get custom backup directory, if different from default
    backup_base_dir = DEFAULT_BACKUP_DIR
    if config.get('backup_dir'):
        backup_base_dir = config['backup_dir']

    backup_dir = join(backup_base_dir, name)
    makedirs(backup_dir, exist_ok=True)

    return source_dir, backup_dir


def read_config() -> Dict[str, Any]:
    """Read config from the config file"""
    if not isfile(CONFIG_PATH):
        makedirs(DATA_DIR, exist_ok=True)
        return DEFAULT_CONFIG
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def write_config(new_config: Dict[str, Any]):
    """Write updated config to the config file"""
    with open(CONFIG_PATH, 'w') as f:
        yaml.safe_dump(new_config, f)
