from os import makedirs
from os.path import isfile, join
from typing import Dict, Any

from appdirs import user_data_dir
import yaml

DATA_DIR = join(user_data_dir(), 'save-scummer')
CONFIG_PATH = join(DATA_DIR, 'config.yml')
BACKUP_DIR = join(DATA_DIR, 'backups')
DEFAULT_CONFIG = {'games': {}}


def read_config() -> Dict[str, Any]:
    """Read config from the config file"""
    if not isfile(CONFIG_PATH):
        makedirs(DATA_DIR, exist_ok=True)
        write_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def write_config(new_config: Dict[str, Any]):
    """Write updated config to the config file"""
    with open(CONFIG_PATH, 'w') as f:
        yaml.safe_dump(new_config, f)
