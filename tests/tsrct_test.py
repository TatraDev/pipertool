import docker
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


main_app_url = f'http://localhost:8788'

# pytest -vs tests/tsrct_test.py::TestTesseract::test_recognizer
class TestTesseract():

    def test_tesseract_install(self):
        #cfg = get_configuration()
        # loop = asyncio.get_event_loop()
        #tess = TesseractRecognizer(port=cfg.docker_app_port)
        # result = loop.run_until_complete()

        assert True

    def test_recognizer(self):        
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

        # headers = {'Content-Type': 'multipart/form-data'}
                
        result = requests.post(url, files=multipart_form_data, verify=False)

        data = result.json()

        assert len(data) != 0

        assert result.status_code == 200

    def test_health_check(self):
        url = f'{main_app_url}/health_check'
        print(url)
        result = requests.post(url)
        assert result.status_code == 200
