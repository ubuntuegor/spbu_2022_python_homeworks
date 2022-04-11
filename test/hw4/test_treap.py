from src.hw4.treap import Treap


def test_empty_treap():
    t = Treap()
    assert len(t) == 0
    for _ in t:
        raise RuntimeError("This treap is empty!")


def test_treap_from_dict():
    r = range(100)
    src = {key: chr(key) for key in r}
    t = Treap(src)
    for i in r:
        assert i in src
        assert src[i] == chr(i)
    assert 100 not in t
    assert len(t) == 100
    assert list(iter(t)) == list(r)


def test_modifying_treap():
    t = Treap()
    t[420] = "w"
    assert len(t) == 1
    t[69] = "l"
    assert len(t) == 2
    t[1337] = "pwn"
    assert len(t) == 3

    assert list(iter(t)) == [69, 420, 1337]
    assert t[420] == "w"
    assert t[69] == "l"

    # Overriding a key
    t[420] = "new"
    assert t[420] == "new"

    del t[69]
    assert len(t) == 2
    assert list(iter(t)) == [420, 1337]

    t.clear()
    assert len(t) == 0
    assert list(iter(t)) == []


def test_treap_works_after_clear():
    t = Treap()
    t.clear()
    t[1] = "a"
    assert 1 in t
    assert t[1] == "a"


def test_treap_as_mutablemapping():
    t = Treap()
    t[10] = "c"
    t[1] = "a"
    t[7] = "b"
    assert list(t.keys()) == [1, 7, 10]
    assert list(t.values()) == ["a", "b", "c"]
    b = Treap(t)
    assert b == t
    assert b.pop(7) == "b"
    assert len(b) == 2
    assert b != t
