import argparse
import os
import sys
from typing import Callable

from vomit import to_unicode, to_utf8, walker, __version__


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='python -m vomit')

    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('-e', '--encode', action='store_true', help='indicate the file should be encoded')
    action_group.add_argument('-d', '--decode', action='store_true', help='indicate the file should be decoded')

    parser.add_argument('-f', '--file', type=str, help='the file to encode or decode, defaults to stdin')
    parser.add_argument('-s', '--source', type=str, help='the directory to encode or decode files recursively')

    parser.add_argument(
        '-i', '--ignore', type=str, nargs='*',
        help='list of files and directories to skip when using source as input'
    )
    parser.add_argument(
        '-r', '--ignore-regex', type=str, nargs='*',
        help='list of files and directories as regex patterns to skip when using source as input'
    )
    parser.add_argument(
        '-n', '--ignore-names', type=str, nargs='*',
        help='list of node names to skip'
    )

    parser.add_argument(
        '-t', '--ext', type=str, nargs='*',
        help='list of extensions to include along ".py" when using source as input'
    )

    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output used for file or source as input')

    return parser


def _output(code: str, dest: str | None):
    if not dest:
        print(code)
        return

    with open(dest, 'w') as f:
        f.write(code)


def _input(
        action: Callable[[str, list[str] | None], str],
        src: str | None,
        ignore_names: list[str] | None = None
    ) -> str:

    if not src:
        code = ''.join(line for line in sys.stdin)
        return action(code, ignore_names)

    with open(src, 'r') as f:
        code = f.read()
        return action(code, ignore_names)


def _pipe(action: Callable[[str, list[str] | None], str], source: str | None, ignore_names: list[str] | None = None):
    code = _input(action, source, ignore_names)
    _output(code, source)


def _validate_input(source: str, msg: str, check: Callable[[str], bool]):
    if not os.path.exists(source):
        print(f'[py-vomit] {msg} "{source}" not found')
        os._exit(1)

    if not check(source):
        print(f'[py-vomit] "{source}" not a {msg}')
        os._exit(1)


if __name__ == '__main__':
    args = _parser().parse_args()
    action = to_unicode if args.encode else to_utf8

    if not args.source and not args.file:
        _pipe(action, None)
        os._exit(0)

    def _print(msg: str):
        if args.verbose:
            print(f"[py-vomit] {msg}")

    _print(f"v{__version__}")

    if args.source:
        _validate_input(args.source, 'directory', os.path.isdir)
        for file in walker(args.source, args.ext, args.ignore, args.ignore_regex):
            _print(f"{action.__name__} {file}")
            _pipe(action, file, args.ignore_names)

    if args.file:
        _validate_input(args.file, 'file', os.path.isfile)
        _print(f"{action.__name__} {args.file}")
        _pipe(action, args.file, args.ignore_names)

    _print("done")
