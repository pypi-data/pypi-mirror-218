from pipedi.util.text import tail

def test__tail():
    inp = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    res = list(inp | tail(3))

    assert res == ["h", "i", "j"]

def test__tail__can_return_empty_list():
    inp = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    res = list(inp | tail(0))

    assert res == []

def test__tail__num_can_be_more_than_iterable_length():
    inp = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    res = list(inp | tail(1000))

    assert res == ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]



from pipedi.util.text import head

def test__head():
    inp = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    res = list(inp | head(3))

    assert res == ["a", "b", "c"]

def test__head__can_return_empty_list():
    inp = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    res = list(inp | head(0))

    assert res == []

def test__head__num_can_be_more_than_iterable_length():
    inp = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    res = list(inp | head(1000))

    assert res == ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
