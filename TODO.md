# TODO

* How to specify an individual backup in `ssc restore`?
  * Default to latest
  * Index, e.g. `-2` for 2 backups ago
  * Date/time, for latest backup no later than given time,
    e.g. I messed up my game around 10:30, so specify `10:30am` for last backup created before then
  * Absolute or relative (to backup dir) filename 
* Add secondary cloud storage sync dir (for Google Drive, Nextcloud, etc.)
* 'backup all' command: run a backup for all configured games
  * Ignore any games with files that haven't changed; compare saved `last_save_time` to current
* 'autosave' command: Monitor source directory, save at regular intervals (if any files changed),
  until canceled
