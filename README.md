# Save Scummer
**WIP / Not yet functional!**

A simple CLI utility to backup and restore game saves.
This is mainly intended for rogue-lite games like **FTL** and **Don't Starve**.
It could also be easily applied to other games, or non-game applications, for example
ones with breakage-prone or complex configuration.

I made this because I enjoy roguelike/rogue-lite games, but when I inevitably find one too difficult,
I often resort to working around the permadeath mechanic by
[save-scumming](https://tvtropes.org/pmwiki/pmwiki.php/Main/SaveScumming).
I then found myself wasting precious _seconds_ of time copying save files back and forth,
so I decided to waste hours (semi-)automating it instead!

## Features
None!

## Installation
```python
# Not yet on pypi; will be published when at least basic functionality is working 
pip install https://github.com/JWCook/save-scummer
```

## Usage
Save-scummer provides the command `save-scummer` (also aliased as `ssc`) with the following subcommands:

```
Usage: ssc COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add      Add a game and its save directory
  backup   Make a backup of the specified game
  ls       List all currently configured games
  restore  Restore a backup of the specified game
```

### Add
Use `ssc add` to add a game and its save directory.

Relative paths, user paths, and [glob patterns](https://en.wikipedia.org/wiki/Glob_(programming))
are supported:
```bash
ssc add game1 ~/Games/game1           # Add a dir (including any subdirs)
ssc add game1 '~/Games/game1/**'      # Equivalent glob pattern (quotes required)
ssc add game2 'C:\Games\game2\*.sav'  # Add files ending in .sav
````

### Backup
Use `ssc backup` to create a new backup. Just specify the game title, and an optional description:
```bash
ssc backup game1 'level 10 with full health'
```

### List
Use `ssc ls` to show a summary of all configured games and their backups:
```
╒════════╤═════════════════╤═════════════════════════════════╤═════════════════════════════════╕
│ Game   │ Total backups   │ Last saved                      │ Last backed up                  │
╞════════╪═════════════════╪═════════════════════════════════╪═════════════════════════════════╡
│ game1  │ 0               │ never                           │ never                           │
├────────┼─────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│ game2  │ 10 (60.68 KB)   │ 2021-01-19 15:20 (23 hours ago) │ 2021-01-19 16:24 (22 hours ago) │
╘════════╧═════════════════╧═════════════════════════════════╧═════════════════════════════════╛
```

Note that "Last saved" is the time the original save files were created/modified.

### Restore
**WIP**




