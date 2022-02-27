import pathlib
import sys
from unittest.mock import patch

import pytest
from src.hw1.head import main


def test_head(tmp_path: pathlib.Path, capsys: pytest.CaptureFixture):
    test_content = "a\nb\nc\nd\ne\nf\ng\nh\ni\n"
    result_content = "a\nb\nc\n"
    test_file = tmp_path / "file.txt"
    test_file.write_text(test_content)
    test_args = ["head.py", "-n", "3", str(test_file)]
    with patch.object(sys, "argv", test_args):
        main()
        captured = capsys.readouterr()
        assert captured.out == result_content
