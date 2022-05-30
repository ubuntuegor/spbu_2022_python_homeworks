from pathlib import Path
from src.test2.logger import logger


def test_logger(tmp_path: Path):
    log_file = tmp_path / "my_log.txt"

    @logger(log_file)
    def sum_args(*args):
        return sum(args)

    sum_args(1, 2, 3)

    assert log_file.read_text().endswith("sum_args (1, 2, 3) {} 6\n")


def test_logger_kwargs(tmp_path: Path):
    log_file = tmp_path / "my_log.txt"

    @logger(log_file)
    def do_nothing(*args, **kwargs):
        return True

    do_nothing(1, 2, 3, one=1, two=2, three=3)

    assert log_file.read_text().endswith("do_nothing (1, 2, 3) {'one': 1, 'two': 2, 'three': 3} True\n")


def test_logger_multiple(tmp_path: Path):
    log_file = tmp_path / "my_log.txt"

    @logger(log_file)
    def f(n):
        if n != 0:
            f(n - 1)

    f(2)

    calls = log_file.read_text().splitlines()
    assert len(calls) == 3
    assert calls[0].endswith("f (0,) {} None")
    assert calls[1].endswith("f (1,) {} None")
    assert calls[2].endswith("f (2,) {} None")
