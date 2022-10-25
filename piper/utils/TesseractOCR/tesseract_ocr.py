from loguru import logger

try:
    import pdf2image
    import pytesseract

except ImportError as ie:
    print(ie)

import numpy as np
import cv2

import requests
from piper.configurations import get_configuration

cfg = get_configuration()

def send_file_to_ocr_service(url, file_path):
    '''Load file by path and sent it to OCR service by url'''
    multipart_form_data = {
        'file': open(file_path, 'rb')
    }

    try:
        result = requests.post(url, files=multipart_form_data, verify=False)
        return result

    except requests.exceptions.ConnectionError as ce:
        logger.error(f'exeption while connect to {url}')
        logger.error(ce)       

def img_to_text(img, ts_conf):
    '''Get text from image with Tesseract'''
    logger.info(f'pytesseract process file with len {len(img)}')
    txt_dict = pytesseract.image_to_data(
        img,
        lang=ts_conf.get('lang'),
        config=ts_conf.get('ts_config_row'),
        output_type=pytesseract.Output.DICT
    )
    return txt_dict


def bytes_handler(bbytes, suf, ts_conf):
    '''Process bytes as image or as PDF document'''
    if suf in cfg.image_suffixes:
        logger.info('bytes are image')
        return img_bytes_handler(bbytes, ts_conf)
    elif suf in cfg.pdf_suffixes:
        logger.info('bytes are pdf document')
        return pdf_bytes_handler(bbytes, ts_conf)

    
def pdf_bytes_handler(pdf_bytes, ts_conf):
    '''Process PDF document'''
    bytes_to_images = pdf2image.convert_from_bytes(
        pdf_bytes,
        thread_count=cfg.thread_count,
        dpi=cfg.dpi
    )
    logger.info(f'pdf to image return {bytes_to_images} pages')
    pages = [np.asarray(x) for x in bytes_to_images]
    #TODO add processing all pages
    if len(pages) > 0:
        logger.error(f'try to recognize pages {len(pages)}')
        txt_dict = img_to_text(pages[0], ts_conf)
        logger.info(f'img_to_text returned {txt_dict}')
        return txt_dict
    else:
        logger.error('no pdf pages to recognize')


def img_bytes_handler(img_bytes, ts_conf):
    '''Process image'''
    img = cv2.imdecode(np.asarray(bytearray(img_bytes), dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is not None:
        logger.info(f'processing img with shape {img.shape}')
        txt_dict = img_to_text(img, ts_conf)

        logger.info(f'get text from image {txt_dict}')
        logger.info(f'img_to_text returned {txt_dict}')
        return txt_dict

    else:
        logger.error('recive empty image or convertion failed')
