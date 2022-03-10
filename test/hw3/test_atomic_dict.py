from threading import Thread
from src.hw3.atomic_dict import AtomicDict


def test_atomic_dict():
    ad = AtomicDict()

    def modify_atomic_dict(ad: AtomicDict):
        with ad.acquire() as d:
            d["other_data"] = 69

    with ad.acquire() as d:
        d["some_data"] = 42

    t = Thread(target=modify_atomic_dict, args=(ad,))
    t.start()
    t.join()

    with ad.acquire() as d:
        assert d["some_data"] == 42
        assert d["other_data"] == 69
