# Save Scummer

[![Build](https://github.com/JWCook/save-scummer/workflows/Build/badge.svg?branch=main)](https://github.com/JWCook/save-scummer/actions)
[![PyPI](https://img.shields.io/pypi/v/save-scummer?color=blue)](https://pypi.org/project/save-scummer)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/save-scummer)](https://pypi.org/project/save-scummer)

* [Features](#features)
* [Installation](#installation)
  * [Autocompletion](#autocompletion--optional-)
* [Usage](#usage)
  * [Add](#add)
  * [Backup](#backup)
  * [List](#list)
  * [Restore](#restore)
    * [Backup specifiers](#backup-specifiers)
    * [Restore Examples](#restore-examples)


Save-Scummer is a simple CLI utility to backup and restore game saves.
This is intended for rogue-lite games like **Rogue Legacy**, **FTL** and **Don't Starve**,
but it could also be applied to other games or non-game applications.

I made this because I enjoy roguelike/rogue-lite games, but when one starts to get too difficult,
I may resort to [save-scumming](https://tvtropes.org/pmwiki/pmwiki.php/Main/SaveScumming) as an
option to make the game a bit easier. When doing that manually, I find myself wasting precious _seconds_
of time copying files back and forth, so naturally I decided to waste _hours_ making it (semi-)automated
instead.

A full backup utility (like [Duplicati](https://github.com/duplicati/duplicati)) or sync utility
(like [rsync](https://github.com/WayneD/rsync)) will obviously have _many_ more features, but for the
basic case of handling game saves, I wanted something simpler with concise command line usage.

# Features
* Just provide a save directory (or glob pattern) to configure a new game
* Easily make backups, and restore them by most recent (default), time expressions
  (to indicate how far back in time you want to go), or choose from a list
* Tab autocompletion

# Installation
Install with [pipx](https://pipx.pypa.io/stable/) (recommended):
```sh
pipx install save-scummer
```

Or with pip:
```sh
pip install save-scummer
```

## Autocompletion (optional)
Tab autocompletion is available for most common shells: **bash, fish, zsh** and Windows **PowerShell**.
To install, run:
```sh
ssc --install [shell name]
``````

# Usage
Save-scummer provides the command `save-scummer` (also aliased as `ssc`) with the following subcommands:

```sh
sh: ssc COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add      Add a game and its save directory
  backup   Create a backup of one, multiple, or all games
  ls       List all currently configured games
  restore  Restore a backup of the specified game
```

## Add
Use `ssc add` to add (or update) a game and its save directory.

Relative paths, user paths, and [glob patterns](https://en.wikipedia.org/wiki/Glob_(programming))
are supported:
```sh
ssc add game1 ~/Games/game1           # Add a dir (including any subdirs)
ssc add game1 '~/Games/game1/**'      # Equivalent glob pattern (quotes required)
ssc add game2 'C:\Games\game2\*.sav'  # Add files ending in .sav
````

## Backup
Use `ssc backup` to create a new backup. Just specify the game title, and an optional description:
```sh
ssc backup game1 -d 'level 10 with full health'
```
Or just backup everything:
```sh
ssc backup --all
```

## List
Use `ssc ls` to show a summary of all configured games:
```sh
╒════════╤═════════════════╤═════════════════════════════════╕
│ Title  │ Total backups   │ Last saved                      │
╞════════╪═════════════════╪═════════════════════════════════╡
│ game1  │ 0               │ never                           │
├────────┼─────────────────┼─────────────────────────────────┤
│ game2  │ 7 (94.96 KB)    │ 2021-01-19 15:20 (23 hours ago) │
╘════════╧═════════════════╧═════════════════════════════════╛
```

Or use `ssc ls [game title]` to show more details on a specific game and its backups:
```sh
Game:               game2
Total backups:      7 (94.96 KB)
Last saved:         2021-01-19 15:20 (23 hours ago)
Last backed up:     2021-01-19 16:24 (22 hours ago)
Source directory:   /home/user/game2/saves
Backup directory:   /home/user/.local/share/save-scummer/backups/game2
Backup files:
0:  game2-2021-01-26T19:23:26.zip
1:  game2-2021-01-20T16:33:42-pre-restore.zip
2:  game2-2021-01-19T19:26:10.zip
3:  game2-2021-01-19T18:31:58.zip
4:  game2-2021-01-18T12:17:52.zip
5:  game2-2021-01-17T16:18:09.zip
6:  game2-2021-01-17T15:01:58.zip
```

Note that "Last saved" is the time that the source files were created/modified.

## Restore

Use `ssc restore` to restore a backup. A specific backup can be indicated by backup
 **index, age, date/time, or filename**. Otherwise, the most recent backup is restored.

```sh
Usage: ssc restore [OPTIONS] [TITLE]

Options:
  -i, --index INTEGER  Backup number (starting at 0, from newest to oldest)
  -a, --age TEXT       Minimum age (relative to current time)
  -d, --date TEXT      Maximum date/time (absolute)
  -f TEXT              Backup filename; either absolute or relative to backup dir
```

### Backup specifiers

**Index:**
The backup index, sorted from newest to oldest, e.g.
**"Restore the save from x backups ago."** 0 is the latest backup, 1 is the
backup made before that, etc.
Negative values can also be given; -1 would give you the oldest backup.
See `ls` command for full list of available backups.

**Age:**
Minimum age of the save to restore, e.g **"I want to go back in time by 1 hour."**
Amounts of time can be specified in 'HH:MM' format, or with a number followed by a unit.
Examples:
* '1:30' (an hour and a half ago)
* '30m' (or '30 minutes')
* '6h' (or '6 hours')
* '9 hours, 15 minutes' (or '9:15')
* '2d' (or '2 days')
* See [pytimeparse](https://github.com/wroberts/pytimeparse) for more formats

**Date/Time:**
Maximum date/time of the save to restore, e.g., **"I want to go back in
time to 1:30 yesterday."** Most date/time formats are supported.
Examples:
* '16:30' or '4:30 PM' (today)
* '2021-01-20'
* 'August 3 2020'
* Most date/time formats are supported; see
[dateutil](https://dateutil.readthedocs.io/en/stable/examples.html#parse-examples)
for more examples.

**Filename:**
Either a full path or just the filename (relative to the backup dir)

### Restore Examples

```sh
# Just restore the most recent backup
ssc restore game1

# Restore the backup made 2 backups ago (aka the 3rd most recent)
ssc restore game1 -i 2

# Restore a backup from (at least) an hour and a half ago
ssc restore game1 -a '1:30'

# Restore a backup from (at least) 2 days ago
ssc restore game1 -a 2d

# Restore a backup from 4:00 PM today or earlier
ssc restore game1 -d '4:00 PM'

# Restore a backup from March 22 or earlier
ssc restore game1 -d 'Mar 22 2021'

# Restore a backup by filename
ssc restore game1 -f game1-2021-01-20T00:09:10.zip
```

# Development setup
To set up for local development:
```sh
git clone https://github.com/JWCook/save-scummer && cd save-scummer
pip install -Ue '.[dev]'
```

To run linting, formatting, etc.:
```sh
pre-commit run -a
```
