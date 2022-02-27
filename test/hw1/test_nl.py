import pathlib
import sys
from unittest.mock import patch

import pytest
from src.hw1.nl import main


def test_nl(tmp_path: pathlib.Path, capsys: pytest.CaptureFixture):
    test_content = """black==22.1.0
mypy==0.931
pytest==7.0.1
"""
    result_content = """1 black==22.1.0
2 mypy==0.931
3 pytest==7.0.1
"""
    test_file = tmp_path / "file.txt"
    test_file.write_text(test_content)
    test_args = ["nl.py", str(test_file)]
    with patch.object(sys, "argv", test_args):
        main()
        captured = capsys.readouterr()
        assert captured.out == result_content
