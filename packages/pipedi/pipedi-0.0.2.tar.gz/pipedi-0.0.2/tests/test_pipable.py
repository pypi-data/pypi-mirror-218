import pytest

from pipedi import pipable


@pipable
def tostr(line):
    return str(line)

@pipable
def toint(line):
    return int(line)

def test__pipable__can_forward():
    inp = [1, 2, 3, 4, 5]

    res = list(inp | tostr() | toint())

    assert res == [1, 2, 3, 4, 5]


@pipable
def wrap(line, pre, post):
    return pre + line + post

def test__piped_function_can_take_parameters():
    inp = ["a", "b", "c", "d", "e"]
    res = list(inp | wrap("[", "]"))

    assert res == ["[a]", "[b]", "[c]", "[d]", "[e]"]
