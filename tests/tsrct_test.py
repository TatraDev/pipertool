import asyncio
import os
import sys

import requests

root_dir = os.path.join(os.path.realpath(os.path.pardir), 'piper')
sys.path.insert(1, root_dir)

import os
from pathlib import Path

import pytest

from piper.configurations import get_configuration
from piper.envs import DockerEnv, is_docker_env
from piper.services import StringValue, TesseractRecognizer
from piper.utils import docker_utils as du
from piper.utils import tesrct_utils as tu

main_app_url = f'http://localhost:8788'
file_path = Path(__file__).parent


# pytest -vs tests/tsrct_test.py::TestTesseract::test_recognizer
class TestTesseract:
    """
        Docker container API test. Methods:
            test_recognizer_jpg
            test_recognizer_pdf
            health_check
    """

    def test_recognizer_jpg(self):
        """
            jpg file recognize test
        """
        fn = file_path.joinpath('ocr_data.jpg')
        url = f'{main_app_url}/recognize'

        result = tu.send_file_to_service(url, fn)
        print('result.status_code', result.status_code)
        # assert result is None

        assert result.status_code == 200
        try:
            data = result.json()
            print('data', data)
            assert len(data) != 0
        except Exception as e:
            pytest.raises(Exception)

    def test_recognizer_pdf(self):
        """
            pdf file recognize test
        """
        fn = file_path.joinpath('ocr_data.pdf')
        url = f'{main_app_url}/recognize'

        result = tu.send_file_to_service(url, fn)
        print(result.status_code)
        assert result.status_code == 200
        try:
            data = result.json()
            print('data', data)
            assert len(data) != 0
        except Exception as e:
            pytest.raises(Exception)

    def test_health_check(self):
        """
            health check test
        """
        url = f'{main_app_url}/health_check'
        print(url)
        result = requests.post(url)
        assert result.status_code == 200
