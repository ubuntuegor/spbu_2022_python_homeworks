from pathlib import Path
from src.test1.safe_call import safe_call


def test_safe_call(tmp_path: Path):
    log_file = tmp_path / "my_log.log"

    @safe_call(str(log_file))
    def normal_function():
        return 1

    assert normal_function() == 1
    assert not log_file.exists()


def test_safe_call_raises(tmp_path: Path):
    log_file = tmp_path / "my_log.log"

    @safe_call(str(log_file))
    def bad_function():
        raise RuntimeError("Oh no!")

    assert bad_function() == None
    assert log_file.read_text().endswith("RuntimeError('Oh no!')\n")
