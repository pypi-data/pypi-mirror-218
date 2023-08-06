import pytest

from pipedi import piped


@piped
def nop(iterable):
    for line in iterable:
        yield line

def test__piped_function_result_is_iterable():
    inp = ["a", "b", "c", "d", "e"]

    try:
        iter(inp | nop())
    except TypeError:
        pytest.fail("Not iterable")

def test__piped_function_can_pipe_foward():
    inp = ["a", "b", "c", "d", "e"]
    res = list(inp | nop())

    assert res == inp

def test__piped_function_can_pipe_foward_any_number():
    inp = ["a", "b", "c", "d", "e"]
    res = list(inp | nop() | nop() | nop())

    assert res == inp


@piped
def add_i(iterable):
    for i, line in enumerate(iterable):
        yield line + str(i + 1)

def test__piped_function_can_edit_piped_items():
    inp = ["a", "b", "c", "d", "e"]
    res = list(inp | add_i())

    assert res == ["a1", "b2", "c3", "d4", "e5"]


@piped
def enum(iterable):
    for i, line in enumerate(iterable):
        yield (i, line)

def test__piped_function_can_change_types():
    inp = ["a", "b", "c", "d", "e"]
    res = list(inp | enum())

    assert res == [(0, "a"), (1, "b"), (2, "c"), (3, "d"), (4, "e")]


@piped
def every_other(iterable):
    for i, line in enumerate(iterable):
        if i % 2 == 0:
            yield line

def test__piped_function_can_filter_items():
    inp = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    res = list(inp | every_other())

    assert res == ["a", "c", "e", "g", "i"]


@piped
def duplicate(iterable):
    for i, line in enumerate(iterable):
        yield line
        yield line

def test__piped_function_can_add_items():
    inp = ["a", "b", "c", "d"]
    res = list(inp | duplicate())

    assert res == ["a", "a", "b", "b", "c", "c", "d", "d"]


@piped
def wrap(iterable, pre, post):
    for line in iterable:
        yield pre + line + post

def test__piped_function_can_take_parameters():
    inp = ["a", "b", "c", "d", "e"]
    res = list(inp | wrap("[", "]"))

    assert res == ["[a]", "[b]", "[c]", "[d]", "[e]"]
