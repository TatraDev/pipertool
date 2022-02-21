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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def run(self, file_ : BytesObject) -> ListOfStringsObject:
        print('1')
        return {1:1}
        # return tess_utils.file_handler(file_)

    async def recognize(self, file_content : BytesObject) -> ListOfStringsObject:
        logger.info(f'file_content {type(file_content)}')
        text_dict = tu.img_bytes_handler(file_content)
        return JSONResponse(content=text_dict)

