import pathlib
import sys
from unittest.mock import patch

import pytest
from src.hw1.nl import main


@pytest.mark.parametrize(
    ["test_content", "result_content"],
    [
        (
            """black==22.1.0
mypy==0.931
pytest==7.0.1
""",
            """     1\tblack==22.1.0
     2\tmypy==0.931
     3\tpytest==7.0.1
""",
        ),
        (
            """check

empty

lines

""",
            """     1\tcheck
      \t
     2\tempty
      \t
     3\tlines
      \t
""",
        ),
    ],
)
def test_nl(tmp_path: pathlib.Path, capsys: pytest.CaptureFixture, test_content: str, result_content: str):
    test_file = tmp_path / "file.txt"
    test_file.write_text(test_content)
    test_args = ["nl.py", str(test_file)]
    with patch.object(sys, "argv", test_args):
        main()
        captured = capsys.readouterr()
        assert captured.out == result_content
