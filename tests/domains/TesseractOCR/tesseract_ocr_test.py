# pytest -vs tests/domains/TesseractOCR/tesseract_ocr_test.py::TestTesseract
# pytest -vs tests/domains/TesseractOCR/tesseract_ocr_test.py::TestTesseract::test_recognizer_jpg

import os
import sys
import requests
root_dir = os.path.join(os.path.realpath(os.path.pardir), 'piper_ng')
sys.path.insert(1, root_dir)

from piper.utils import docker_utils as du
from piper.utils.TesseractOCR import tesseract_ocr as tu

from piper.envs import DockerEnv
from piper.envs import is_docker_env
from piper.configurations import get_configuration
from piper.services import TesseractRecognizer, StringValue
from pathlib import Path
import os
import pytest


main_app_url = f'http://localhost:8788'
file_path = Path(__file__).parent
data_path = file_path.joinpath('data')

class TestTesseract():
    '''
        Docker container API test. Methods:
            test_recognizer_jpg
            test_recognizer_pdf
            health_check
    '''

    def test_recognizer_jpg(self):
        '''
            jpg file recognize test
        '''
        fn = data_path.joinpath('ocr_data.jpg')
        url = f'{main_app_url}/recognize'

        result = tu.send_file_to_ocr_service(url, fn)
        print('result.status_code', result.status_code)
        # assert result is None

        assert result.status_code == 200
        try:
            data = result.json()
            print('data', " ".join([x for x in data.get('text') if x]))
            assert len(data) != 0
        except Exception as e:
            pytest.raises(Exception)


    def test_recognizer_pdf(self):
        '''
            pdf file recognize test
        '''
        fn = data_path.joinpath('ocr_data.pdf')
        url = f'{main_app_url}/recognize'

        result = tu.send_file_to_ocr_service(url, fn)
        print('result.status_code', result.status_code)
        assert result.status_code == 200        
        try:
            data = result.json()
            print('data: ', " ".join([x for x in data.get('text') if x]))
            assert len(data) != 0
        except Exception as e:
            pytest.raises(Exception)


    def test_health_check(self):
        '''
            health check test
        '''
        url = f'{main_app_url}/health_check'
        print(url)
        result = requests.post(url)
        print('result.status_code', result.status_code)
        assert result.status_code == 200
