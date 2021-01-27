# TODO

* Option to restore to a specified directory instead of source dir
* Terminology 'games' -> 'titles'  (more general)
* Add secondary cloud storage sync dir (for Google Drive, Nextcloud, etc.)
* 'backup all' command: run a backup for all configured games
  * Ignore any games with files that haven't changed; compare saved `last_save_time` to current
  * Or: make this the default behavior for `backup` if no game name is passed?
* Tab completion for backup filenames (requires processing an incomplete command from cli context)
* 'autosave' or 'watch' command: Watch source directory, save at regular intervals (if any files changed),
  until canceled
  * Use `watchdog`
  * Monitor either the specified game, or all game dirs if none is given
