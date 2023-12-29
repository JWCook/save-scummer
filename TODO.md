# TODO
Possible feature ideas:

* Global ignore glob patterns
* Per-game ignore glob patterns
* Option to restore to a specified directory instead of source dir
* Option to change backup directory
    * Mainly for cloud storage sync (Google Drive, Nextcloud, etc.)
* Support storing config in sync dir?
    * Will require ability to set directory per-device or at least per-platform
* Store time save files were actually last modified (in addition to backup save time)
    * Helpful for comparing timestamps within in-game save menu if there are multiple saves
* Terminology: 'games' -> 'titles'  (or something else more general)
* `backup -a/--all` option: run a backup for all configured games
  * Ignore any games with files that haven't changed; compare saved `last_save_time` to current
* Tab completion for backup filenames (requires processing an incomplete command from cli context)
* `autobackup` or `watch` command: Watch source directory, save at regular intervals (if any files changed),
  until canceled
  * Use `watchdog`
  * `autobackup -a/--all` option to monitor all game dirs
