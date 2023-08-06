import string

import pytest

from vomit import to_unicode, to_utf8

_vomit = 'vomit'
_fn = 'fn'
_str = 'sval'
_bool = 'bval'
_sval = """
        anti\ngravity!
    """

_chars = ''.join(string.ascii_letters + string.digits)
_fmt = f'''

from dataclasses import dataclass

@dataclass
class NameClass:
    {_str} = """{_sval}"""

    {_chars} = 41 \
        + 1

    {_bool} = True # comment

    @staticmethod
    def {_fn}(
            a,
            b,
            c="test"
    ):
        """
            docs
        """

        for _ in range(0x11):
            pass

        return '{_vomit}'

'''

_change_name = "fn"
_ignore_name = "__version__"
_ignore_names_fmt = f'''
{_ignore_name} = '1.2.3'

def {_change_name}():
    ...
'''


@pytest.mark.parametrize('n', range(20))
def test_function_after_change_is_ok(n):
    unicode = to_unicode(_fmt)

    exec(unicode)
    cls = locals().get('NameClass')
    fn_obtained = cls.__dict__[_fn](None, None)
    str_obtained = cls.__dict__[_str]
    num_obtained = cls.__dict__[_chars]
    bool_obtained = cls.__dict__[_bool]

    assert fn_obtained == _vomit
    assert str_obtained == _sval
    assert num_obtained == 42
    assert bool_obtained


def test_function_after_roundtrip_is_ok():
    unicode = to_unicode(_fmt)
    utf8 = to_utf8(unicode)

    exec(utf8)
    cls = locals().get('NameClass')
    fn_obtained = cls.__dict__[_fn](None, None)
    str_obtained = cls.__dict__[_str]
    num_obtained = cls.__dict__[_chars]
    bool_obtained = cls.__dict__[_bool]

    assert fn_obtained == _vomit
    assert str_obtained == _sval
    assert num_obtained == 42
    assert bool_obtained


def test_names_are_ignored():
    unicode = to_unicode(_ignore_names_fmt, [_ignore_name])
    assert _ignore_name in unicode
    assert _change_name not in unicode
