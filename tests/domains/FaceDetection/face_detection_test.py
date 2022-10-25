# pytest -vs tests/domains/FaceDetection/face_detection_test.py::TestFaceDetection::test_detection
# pytest -vs tests/domains/FaceDetection/face_detection_test.py::TestFaceDetection::test_health_check
import os
import sys
import requests
root_dir = os.path.join(os.path.realpath(os.path.pardir), 'piper')
sys.path.insert(1, root_dir)

from pathlib import Path
import os
import pytest
from loguru import logger
import cv2
import base64
import numpy as np
import json

main_app_url = f'http://localhost:8788'
file_path = Path(__file__).parent

def send_file_to_service(url, file_path):
    '''
        Send file by path to service URL 
    '''
    multipart_form_data = {
        'file': open(file_path, 'rb')
    }

    logger.info(f'url: {url}')
    logger.info(f'data: {multipart_form_data}')

    try:
        result = requests.post(url, files=multipart_form_data, verify=False)
        return result
        
    except requests.exceptions.ConnectionError as ce:
        logger.error(f'exeption while connect to {url}')
        logger.error(ce)    

def draw_bb_on_initial_img(img, detections):
    '''
        Draw founded bounded boxes on initial image
    '''
    for detect_dict in detections:
        bbox = detect_dict.get('box')
        x, y, w, h = bbox
        cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)
    return img    


class TestFaceDetection():
    '''
        Docker container API test. Methods:
            test_detection
            health_check
    '''

    def test_detection(self):
        '''
            jpg file recognize test
        '''
        fn = file_path.joinpath('faces.jpg')
        # fn = file_path.joinpath('ocr_data.jpg')
        url = f'{main_app_url}/recognize'

        received_data = send_file_to_service(url, fn)

        assert received_data.status_code == 200, received_data.text

        try:
            detections = received_data.json()
            logger.info(f'received_data.json {detections}')

            logger.info('data', detections)
            assert len(detections) != 0

            if detections:
                initial_img = cv2.imread(str(fn))
                img_with_faces = draw_bb_on_initial_img(initial_img, detections)
                
                out_img_fn = str(file_path.joinpath('result_image.jpg'))
                write_result = cv2.imwrite(out_img_fn, img_with_faces)
                if write_result:
                    logger.info(f'img with detections saved to {out_img_fn}')
                else:
                    logger.error(f'img with detections did not save')


        except Exception as e:
            pytest.raises(Exception)
            assert False


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
