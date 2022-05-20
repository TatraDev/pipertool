from piper.base.executors import FastAPIExecutor, FastAPITesseractExecutor
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from loguru import logger
import json
import spacy
import sys
from piper.configurations import get_configuration
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

    async def ner(self, txt: str): 
        sn = SpacyNER()
        return JSONResponse(content=sn.extract_named_ents(txt))


class SpacyNER():
    '''
        Spacy NER service
    '''
    def __init__(self):
        cfg = get_configuration()
        self.available_models = set()
        self.nlp = None

        try:
            for cur_model in cfg.spacy_models:
                logger.info(f'try to download model {cur_model} to {cfg.model_path}')
                # spacy.util.set_data_path(cfg.model_path)
                res = spacy.cli.download(cur_model)
                logger.info(f'result of spacy.cli.download is {res}')
                self.available_models.add(cur_model)
        except Exception as e:
            logger.error(f'catch exception {e}')
            sys.exit()



    def set_model(self, cur_model):

        if cur_model not in self.available_models:
            logger.error(f'there is not {cur_model} in available_models set: {self.available_models}')
            self.nlp = None

        try:
            nlp = spacy.load(cur_model)
            # nlp = spacy.load('en_default')
            logger.info('spacy nlp object created with model {cur_model}')
        except Exception as e:
            logger.error(f'catch exception {e}')
            if isinstance(e, OSError):                
                logger.error(f'you must download spacy model {cur_model}')
            nlp = None
            logger.info('spacy nlp object DID NOT create')
        
        self.nlp = nlp

    
    def extract_named_ents(self, txt: str):
        logger.debug(f'got data type {type(txt)} and data <<{txt}>> for NER')
        if self.nlp:
            res = []
            doc = self.nlp(txt)
            for ent in doc.ents:
                res.append((ent.text,  ent.label_))
            return res
        else:
            logger.error(f'nlp object didn`t create. you should use set_model(model_name)')
