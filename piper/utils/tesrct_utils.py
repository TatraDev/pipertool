import cv2
import pytesseract
import numpy as np
from loguru import logger


def img_bytes_handler(img_bytes):
    img = cv2.imdecode(np.asarray(bytearray(img_bytes), dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is not None:
        logger.info(f'processing img with shape {img.shape}')
        txt_dict = pytesseract.image_to_data(
            img,
            lang='rus',
            config=r'--oem 1 --psm 11',
            output_type=pytesseract.Output.DICT
        )

        logger.info(f'get text from image {txt_dict}')
        return txt_dict

    else:
        logger.error('recive empty image or convertion failed')
