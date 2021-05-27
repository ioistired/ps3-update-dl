# ps3-update-dl

[![Build Status](https://img.shields.io/travis/com/ioistired/ps3-update-dl/trunk.svg?label=tests)](https://travis-ci.com/ioistired/ps3-update-dl)

Downloads all updates for a given title directly from the PlayStation servers.

## Installation

[`pipx`](https://pipxproject.github.io/pipx/) is the recommended way to install ps3-update-dl.

```
$ pipx install ps3-update-dl
```

Afterwards, the command will be available as `ps3udl`.

## Usage

```
Usage: ps3udl -o BASE_DIR TITLE_ID_1 [TITLE_ID_2...]

Download all updates for all given titles to the given base directory.
A subdirectory inside the base directory will be created for each title.

Options:
    -o, --base-dir
    The directory that all titles will be downloaded to. It must exist.

    -f, --force
    Whether to overwrite existing files.

    -h, --help
    Display this message.
```

## License

© io mintz <io@mintz.cc>

ps3-update-dl is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

ps3-update-dl is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with ps3-update-dl. If not, see <https://www.gnu.org/licenses/>.
