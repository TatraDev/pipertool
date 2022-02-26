from piper.base.executors import FastAPIExecutor, FastAPITesseractExecutor
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from loguru import logger
import json
from piper.utils import tesrct_utils as tu


logger.add("file.log", level="INFO", backtrace=True, diagnose=True, rotation='5 MB')


class StringValue(BaseModel):
    value: str

class BytesObject(BaseModel):
    value: bytes

class ListOfStringsObject(BaseModel):
    value: list

class TestMessageAdder(FastAPIExecutor):

    def __init__(self, appender="TEST", **kwargs):
        self.appender = appender
        super().__init__(**kwargs)

    async def run(self, message: StringValue) -> StringValue:
        return StringValue(value=(message.value + self.appender))


class TesseractRecognizer(FastAPITesseractExecutor):
    '''
        Tesseract OCR implementation service
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def recognize(self, file_content : BytesObject, suf: str) -> ListOfStringsObject:
        logger.info(f'file_content {type(file_content)}, file suffix is {suf}')

        text_dict = tu.bytes_handler(file_content, suf)
        logger.info(f'img_bytes_handler return {type(text_dict)} object')
        return JSONResponse(content=text_dict)

