from functools import reduce
from spexm8p.spex import Chex
from spexm8p.spex import Spex
from spexm8p.parser import tokenize, parse


def spex(spex_str):
    return _build_spex(parse(tokenize(spex_str)))


def _build_spex(parsed):
    if parsed['type'] == 'inc_chex':
        return Spex.build_by_chex(Chex(parsed['tokens'], True))
    elif parsed['type'] == 'exc_chex':
        return Spex.build_by_chex(Chex(parsed['tokens'], False))
    elif parsed['type'] == 'or':
        return _build_spex(parsed['left']) | _build_spex(parsed['right'])
    elif parsed['type'] == 'and':
        return _build_spex(parsed['left']) & _build_spex(parsed['right'])
    elif parsed['type'] == 'invert':
        return ~_build_spex(parsed['node'])
    elif parsed['type'] == 'repeat':
        return _build_spex(parsed['node']).repeat()
    elif parsed['type'] == 'concat':
        return reduce(lambda a, b: a.concat(b), [_build_spex(x) for x in parsed['nodes']])
    else:
        assert False  # unreachable code
