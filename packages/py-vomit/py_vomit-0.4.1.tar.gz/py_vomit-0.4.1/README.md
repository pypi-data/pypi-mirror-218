# vomit

[![Tests](https://github.com/bhmt/vomit/actions/workflows/tests.yml/badge.svg)](https://github.com/bhmt/vomit/actions/workflows/tests.yml)

Make your python code somewhat unintelligible but still readable and still **functional**.

Change the utf8 encoding of class names, function names, function args, and name nodes with a fitting unicode representation.
Or switch those back from unicode to utf8.

The ast is used and does not keep formating.

The changes are inplace if using a file or a directory for input.

## Installation

The package is available on pypi and can be installed using pip.
Activate a virtual environment and run

```

pip install py-vomit

```

## Usage

As a module run vomit with a required option to either encode or decode.
For input use a a stdin + stdout, a file, or a directory.
Add more extensions if `.py` is not enough.
Ignore node names, files, or directories if it keeps the code functional.


```shell

usage: python -m vomit [-h] (-e | -d) [-f FILE] [-s SOURCE] [-i [IGNORE ...]] [-r [IGNORE_REGEX ...]] [-n [IGNORE_NAMES ...]] [-t [EXT ...]] [-v]

options:
  -h, --help            show this help message and exit
  -e, --encode          indicate the file should be encoded
  -d, --decode          indicate the file should be decoded
  -f FILE, --file FILE  the file to encode or decode, defaults to stdin
  -s SOURCE, --source SOURCE
                        the directory to encode or decode files recursively
  -i [IGNORE ...], --ignore [IGNORE ...]
                        list of files and directories to skip when using source as input
  -r [IGNORE_REGEX ...], --ignore-regex [IGNORE_REGEX ...]
                        list of files and directories as regex patterns to skip when using source as input
  -n [IGNORE_NAMES ...], --ignore-names [IGNORE_NAMES ...]
                        list of node names to skip
  -t [EXT ...], --ext [EXT ...]
                        list of extensions to include along ".py" when using source as input
  -v, --verbose         verbose output used for file or source as input

```


or use vomit as a library

```py

from vomit import to_unicode
from vomit import to_utf8
from vomit import UNICODE_MAP

print(to_utf8('🯳'))
# '3'
print(to_unicode('1'))
# '𝟙'
print(UNICODE_MAP['2'])
# 2２𝟐𝟚𝟤𝟮𝟸🯲

```