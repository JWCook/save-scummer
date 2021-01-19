from datetime import datetime

from save_scummer.config import get_game_dirs


def make_backup(name):
    source_dir, backup_dir = get_game_dirs(name)
    timestamp = datetime.now().isoformat()
    print(f'Source dir: {source_dir}; Backup dir: {backup_dir}')


def restore_backup(name):
    source_dir, backup_dir = get_game_dirs(name)
    print(f'Source dir: {source_dir}; Backup dir: {backup_dir}')
