import numpy as np
import cv2
import sys

from mtcnn import MTCNN
from loguru import logger

class FaceRecognizer():

    def __init__(self):
        # doesnt work from docker
        # self.detector = MTCNN()
        self.detector = None
        logger.info('FaceRecognizer model is MTCNN')

    def bytes_handler(self, img_bytes):
        logger.info(f'bytes_handler with arg {type(img_bytes)} and len {sys.getsizeof(img_bytes)}')
        np_array = np.asarray(bytearray(img_bytes), dtype="uint8")
        logger.info(f'converted image is type of {type(np_array)} and size {np_array.shape}')
        img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if img is not None:
            logger.info(f'converted to cv2 image with shape {img.shape}')
            if img is not None:
                h, w, _ = img.shape
                if h > 0 and w > 0:
                    detector = MTCNN()
                    # logger.info(f'detector is {self.detector}')
                    logger.info('start detect faces')
                    detections = detector.detect_faces(img)
                    # detections = self.detector.detect_faces(img)
                    logger.info(f'detections is {detections}')
                    return detections
        else:
            logger.error('can not convert bytes to cv2 image')