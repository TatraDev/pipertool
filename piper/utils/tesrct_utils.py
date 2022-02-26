import cv2
import pytesseract
import numpy as np
from loguru import logger
import pdf2image
from piper.configurations import get_configuration

cfg = get_configuration()

def img_to_text(img):
    logger.info(f'pytesseract process file with len {len(img)}')
    txt_dict = pytesseract.image_to_data(
        img,
        lang='eng',
        config=r'--oem 1 --psm 11',
        output_type=pytesseract.Output.DICT
    )
    return txt_dict


def bytes_handler(bbytes, suf):
    if suf in cfg.image_suffixes:
        logger.info('there are bytes a image')
        return img_bytes_handler(bbytes)
    elif suf in cfg.pdf_suffixes:
        logger.info('there are bytes a pdf document')
        return pdf_bytes_handler(bbytes)

    
def pdf_bytes_handler(pdf_bytes):
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
        txt_dict = img_to_text(pages[0])
        logger.info(f'img_to_text retured {txt_dict}')
        return txt_dict
    else:
        logger.error('no pdf pages to recognize')


def img_bytes_handler(img_bytes):
    img = cv2.imdecode(np.asarray(bytearray(img_bytes), dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is not None:
        logger.info(f'processing img with shape {img.shape}')
        txt_dict = img_to_text(img)

        logger.info(f'get text from image {txt_dict}')
        return txt_dict

    else:
        logger.error('recive empty image or convertion failed')
