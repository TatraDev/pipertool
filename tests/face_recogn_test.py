import os
import sys
import asyncio
import requests
root_dir = os.path.join(os.path.realpath(os.path.pardir), 'piper')
sys.path.insert(1, root_dir)

# from piper.utils import docker_utils as du
# from piper.utils import tesrct_utils as tus

# from piper.envs import DockerEnv
# from piper.envs import is_docker_env
# from piper.configurations import get_configuration
# from piper.services import TesseractRecognizer, StringValue
from pathlib import Path
import os
import pytest
from loguru import logger
import cv2
import base64
import numpy as np
import json

def base64_str_to_cv2_image(b64_str):
    image = base64.b64decode(bytes(b64_str, "utf-8"))
    nparr = np.asarray(bytearray(image), dtype="uint8")
    cv2_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return cv2_image

def get_opencv_format_image(data_json):
    if 'image' in data_json.keys():
        image_base64 = data_json.get('image')
        if image_base64:
            cv2_image = base64_str_to_cv2_image(image_base64)
            return cv2_image
    return None

def cv2_image_to_base64(cv2_img):
    img_str = cv2.imencode('.jpg', cv2_img)[1].tobytes()
    encoded_pic = str(base64.b64encode(img_str), 'utf-8')  
    return encoded_pic


def send_file_to_service(url, file_path):
    multipart_form_data = {
        'file': open(file_path, 'rb')
    }

    logger.info(f'url: {url}')
    logger.info(f'data: {multipart_form_data}')

    try:

        # возврат excepiton
        result = requests.post(url, files=multipart_form_data, verify=False)
        return result
        
    except requests.exceptions.ConnectionError as ce:
        logger.error(f'exeption while connect to {url}')
        logger.error(ce)    

main_app_url = f'http://localhost:8788'
file_path = Path(__file__).parent

# curl -X POST -w "%{http_code}" -F "image=@tests/faces.jpg"  http://localhost:8788/recognize
# curl -X POST -w "%{http_code}" -H "Content-Type: application/json" -d "data=2"  http://localhost:8788/health_check
# pytest -vs tests/face_recogn_test.py::TestFaceRecogn::test_recognizer
class TestFaceRecogn():
    '''
        Docker container API test. Methods:
            test_recognizer_jpg
            test_recognizer_pdf
            health_check
    '''

    def test_recognizer(self):
        '''
            jpg file recognize test
        '''
        fn = file_path.joinpath('faces.jpg')
        # fn = file_path.joinpath('ocr_data.jpg')
        url = f'{main_app_url}/recognize'

        received_data = send_file_to_service(url, fn)

        logger.info(f'received_data.json {received_data.json()}')
        assert received_data.status_code == 200
        try:
            data = received_data.json()
            logger.info('data', data)
            assert len(data) != 0
        except Exception as e:
            pytest.raises(Exception)


    def test_health_check(self):
        '''
            health check test
        '''
        url = f'{main_app_url}/health_check'
        print(url)
        # убрать параметры
        result = requests.post(url, data=json.dumps({"1":"2"}), headers= {'Content-Type': 'application/json'})
        logger.info('health_check test')
        assert result.status_code == 200
