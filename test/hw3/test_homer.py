import os
from pathlib import Path
from unittest.mock import Mock, patch
from src.hw3.homer import download_file, download_random_homer


def get_test_dir():
    return os.path.dirname(os.path.realpath(__file__))


def test_download_file(tmp_path: Path):
    test_data = b"test_data"
    test_url = "https://localhost"

    with patch("src.hw3.homer.urlopen") as urlopen_mock:
        urlopen_obj = Mock()
        urlopen_obj.read.side_effect = [test_data, b""]
        urlopen_mock.return_value.__enter__.return_value = urlopen_obj

        tmp_file = tmp_path / "somefile"

        download_file(test_url, str(tmp_file))

        assert urlopen_mock.call_args.args == (test_url,)
        assert tmp_file.read_bytes() == test_data


def test_download_random_homer():
    homer_page = (Path(get_test_dir()) / "testdata/homer_page.html").read_bytes()
    homer_pic_url = "https://static.thisfuckeduphomerdoesnotexist.com/simpsons_large_cleaned_nobackground_1024_augall03_sle_res64-40-p88/images/2baa5f6f-20b1-45a8-8dbd-bb651c6e3ec1.jpg"
    homer_filename = "2baa5f6f-20b1-45a8-8dbd-bb651c6e3ec1.jpg"

    with patch("src.hw3.homer.download_file") as download_mock, patch("src.hw3.homer.urlopen") as urlopen_mock:
        urlopen_mock.return_value.read.return_value = homer_page
        result_filename = download_random_homer()

        assert result_filename == homer_filename
        download_mock.assert_called_once_with(homer_pic_url, result_filename)
