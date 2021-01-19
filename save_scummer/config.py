from os import makedirs
from os.path import isfile, join
from typing import Any, Dict

import yaml
from appdirs import user_data_dir

DATA_DIR = join(user_data_dir(), 'save-scummer')
CONFIG_PATH = join(DATA_DIR, 'config.yml')
BACKUP_DIR = join(DATA_DIR, 'backups')
DEFAULT_CONFIG = {'games': {}}


def add_game(name: str, source_path: str):
    config = read_config()
    config['games'][name] = {'source': source_path}
    write_config(config)


# TODO: Add more formatting as more values are added
def list_games() -> Dict[str, Any]:
    return read_config()['games']


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
