import pathlib

import pytest

from vomit import walker


@pytest.mark.parametrize(
    'expected, skipped, extensions, ignored, ignored_regex',
    [
        [
            [pathlib.Path("vomit", "__init__.py"), pathlib.Path("vomit", "__main__.py")],
            [pathlib.Path("vomit", "sub", "__main__.pyc"), pathlib.Path("vomit", "__main__.pyi")],
            None,
            None,
            None
        ],
        [
            [pathlib.Path("vomit", "__init__.py"), pathlib.Path("vomit", "__main__.py")],
            [pathlib.Path("vomit", "sub", "__main__.py"), pathlib.Path("vomit", "__main__.pyi")],
            None,
            [pathlib.Path("vomit", "sub", "__main__.py")],
            None
        ],
        [
            [pathlib.Path("vomit", "__init__.py"), pathlib.Path("vomit", "__main__.py")],
            [
                pathlib.Path("vomit", "sub", "first_ignored.py"),
                pathlib.Path("vomit", "sub", "second_ignored.py"),
                pathlib.Path("vomit", "__main__.pyi")
            ],
            None,
            [pathlib.Path("vomit", "sub")],
            None
        ],
        [
            [pathlib.Path("vomit", "__init__.py")],
            [
                pathlib.Path("vomit", "__main__.py"),
                pathlib.Path("vomit", "sub", "first_ignored.py"),
                pathlib.Path("vomit", "sub", "second_ignored.py"),
                pathlib.Path("vomit", "__main__.pyi")
            ],
            None,
            [pathlib.Path("vomit", "sub"), pathlib.Path("vomit", "__main__.py")],
            None
        ],
        [
            [
                pathlib.Path("vomit", "__init__.py"),
                pathlib.Path("vomit", "__main__.pyi"),
                pathlib.Path("vomit", "__main__.py3"),
            ],
            [
                pathlib.Path("vomit", "__main__.py"),
                pathlib.Path("vomit", "sub", "first_ignored.py"),
                pathlib.Path("vomit", "sub", "second_ignored.py"),
            ],
            ['.pyi', 'py3'],
            [pathlib.Path("vomit", "sub"), pathlib.Path("vomit", "__main__.py")],
            None
        ],
        [
            [
                pathlib.Path("vomit", "__init__.py"),
                pathlib.Path("vomit", "sub", "first.py"),
                pathlib.Path("vomit", "sub", "second.py"),
            ],
            [
                pathlib.Path("vomit", "__main__.py"),
                pathlib.Path("vomit", "__main__.pyi"),
                pathlib.Path("vomit", "__main__.py3"),
            ],
            ['.pyi', 'py3'],
            None,
            [r".*__main__\.py(i|3)?$"]
        ]
    ]
)
def test_walker_is_ok(tmpdir, expected, skipped, extensions, ignored, ignored_regex):
    pathlib.Path(tmpdir, "vomit").mkdir()
    pathlib.Path(tmpdir, "vomit", "sub").mkdir()

    expected = {pathlib.Path(tmpdir) / path for path in expected}
    skipped = {pathlib.Path(tmpdir) / path for path in skipped}

    all: set[pathlib.Path] = expected | skipped

    for f in all:
        f.touch()

    ignore_arg = [str(pathlib.Path(tmpdir) / path) for path in ignored] if ignored else None
    obtained = {pathlib.Path(f) for f in walker(tmpdir, extensions, ignore_arg, ignored_regex)}

    assert expected == obtained
