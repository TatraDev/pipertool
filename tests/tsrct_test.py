import os
import sys
import asyncio
import requests
root_dir = os.path.join(os.path.realpath(os.path.pardir), 'piper')
sys.path.insert(1, root_dir)

from piper.utils import docker_utils as du
from piper.envs import DockerEnv
from piper.envs import is_docker_env
from piper.configurations import get_configuration
from piper.services import TesseractRecognizer, StringValue
from pathlib import Path
import os
import pytest


main_app_url = f'http://localhost:8788'

# pytest -vs tests/tsrct_test.py::TestTesseract::test_recognizer
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
        file_path = Path(__file__).parent
        file_path = file_path.joinpath('ocr_data.jpg')
        print(file_path)

        url = f'{main_app_url}/recognize'
        print(url)

        multipart_form_data = {
            'file': open(file_path, 'rb')
            }

        print(multipart_form_data)
        print((multipart_form_data.get('file')))
                
        result = requests.post(url, files=multipart_form_data, verify=False)
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
        '''
            pdf file recognize test
        '''
        file_path = Path(__file__).parent
        file_path = file_path.joinpath('ocr_data.pdf')
        print(file_path)

        url = f'{main_app_url}/recognize'
        print(url)

        multipart_form_data = {
            'file': open(file_path, 'rb')
            }

        print(multipart_form_data)
        print((multipart_form_data.get('file')))

        result = requests.post(url, files=multipart_form_data, verify=False)

        print(result.status_code)
        assert result.status_code == 200        
        try:
            data = result.json()
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
        assert result.status_code == 200
