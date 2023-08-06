import json
import string
import unicodedata


def run():
    map = dict()
    fmt = '''
def fn_{c}{v}():
    pass
    '''.strip()

    for chars in [string.digits, string.ascii_letters]:
        for c in chars:
            _valid = []
            _vals = [chr(n) for n in range(0x10FFFF) if unicodedata.normalize('NFKC', chr(n)) == c]
            if not _vals:
                continue

            for v in _vals:
                _fmt = fmt.format(c=c, v=v)
                try:
                    exec(_fmt)
                except SyntaxError:
                    continue

                _valid.append(v)

            if not _valid:
                continue

            map[c] = ''.join(_valid)

    fmt = f"UNICODE_MAP: dict[str, str] = {json.dumps(map, indent=4, ensure_ascii=False)}"
    return fmt


if __name__ == "__main__":
    print(run())
