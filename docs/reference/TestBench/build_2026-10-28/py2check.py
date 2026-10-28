# Python 2.7 (Jython) grammar check via lib2to3 (run with python3.11)
import sys, warnings
warnings.filterwarnings('ignore')
from lib2to3 import pygram, pytree
from lib2to3.pgen2 import driver, parse, tokenize

def check_source(src, name='<src>'):
    d = driver.Driver(pygram.python_grammar, convert=pytree.convert)
    if not src.endswith('\n'):
        src += '\n'
    try:
        d.parse_string(src)
        return None
    except (parse.ParseError, tokenize.TokenError, IndentationError, SyntaxError) as e:
        return '%s: %s' % (name, e)

if __name__ == '__main__':
    bad = 0
    for p in sys.argv[1:]:
        err = check_source(open(p, encoding='utf-8').read(), p)
        if err:
            print('FAIL', err); bad += 1
        else:
            print('OK  ', p)
    sys.exit(1 if bad else 0)

import re as _re
_PY3 = [(r'(?<![A-Za-z0-9_])[fF][rR]?["\']', 'f-string'), (r'\bnonlocal\b', 'nonlocal'), (r'\byield\s+from\b', 'yield from'),
        (r'\basync\s+def\b|\bawait\b', 'async'), (r'def\s+\w+\([^)]*\)\s*->', 'annotation'), (r'def\s+\w+\([^)]*\*\s*,', 'kw-only')]

def py3_only(src):
    out = []
    for i, line in enumerate(src.splitlines(), 1):
        code = line.split('#', 1)[0] if '"' not in line and "'" not in line else line
        for rx, what in _PY3:
            if _re.search(rx, code):
                out.append('%d: %s: %s' % (i, what, line.strip()[:100]))
    return out
