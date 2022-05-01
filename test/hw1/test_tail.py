import pathlib
import sys
from unittest.mock import patch

import pytest
from src.hw1.tail import main


def test_tail(tmp_path: pathlib.Path, capsys: pytest.CaptureFixture):
    test_content = " a\n b\n c\n d\n e\n f\n g\n h\n i\n"
    result_content = " g\n h\n i\n"
    test_file = tmp_path / "file.txt"
    test_file.write_text(test_content)
    test_args = ["tail.py", "-n", "3", str(test_file)]
    with patch.object(sys, "argv", test_args):
        main()
        captured = capsys.readouterr()
        assert captured.out == result_content
