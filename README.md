# Save Scummer
**WIP / Not yet functional!**

A simple CLI utility to backup and restore game saves.
This is mainly intended for rogue-lite games like **FTL** and **Don't Starve**.

I made this because I enjoy roguelike/rogue-lite games, but when I inevitably find one too difficult,
I often resort to working around the permadeath mechanic by
[save-scumming](https://tvtropes.org/pmwiki/pmwiki.php/Main/SaveScumming).
I then found myself wasting precious _seconds_ of time copying save files back and forth,
so I decided to waste hours automating it instead!

## Features
None!

## Installation
```python
# Not yet on pypi; will be published when at least basic functionality is working 
pip install https://github.com/JWCook/save-scummer
```

## Usage
Save-scummer provides the command `ssc` with the following options:

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
