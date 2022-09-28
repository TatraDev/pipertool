from piper.base.executors import FastAPIExecutor, FastAPITesseractExecutor, FastAPIFaceRecognExecutor
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from loguru import logger
import json
# import spacy
import sys
from piper.configurations import get_configuration
# from piper.utils import tesrct_utils as tu
from piper.utils import face_recogn_utils as fru


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


class FaceRecognizer(FastAPIFaceRecognExecutor):
    '''
        FaceRecognizer implementation service
    '''
    def __init__(self, **kwargs):
        self.face_recogizer = fru.FaceRecognizer()
        super().__init__(**kwargs)

    
    async def recognize(self, file_content : BytesObject) -> ListOfStringsObject:     
        logger.info(f'face_recogizer recive {type(file_content)} object')
        text_dict = self.face_recogizer.bytes_handler(file_content)
        logger.info(f'face_recogizer img_bytes_handler return {(text_dict)} object')
        return JSONResponse(content=text_dict)
        # return JSONResponse(content={"1":"1"})


class TesseractRecognizer(FastAPITesseractExecutor):
    '''
        Tesseract OCR implementation service
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cfg = get_configuration()
        self.ts_config = cfg.ts_config

    def set_config_(self, config_):        
        if 'ts_lang' not in config_.keys():
            logger.error(f'tesseract config keys must contains ts_lang, keys {config_.keys()}')
            logger.error(f'tesseract config did not set')
            return None

        if 'ts_config_row' not in config_.keys():
            logger.error(f'tesseract config keys must contains ts_config_row, keys {config_.keys()}')
            logger.error(f'tesseract config did not set')
            return None

        self.ts_config = config_
        logger.info(f'tesseract config changed to {config_}')

    async def sconfig(self, conf) -> ListOfStringsObject:
        # conf = '12'
        logger.info(f'request to set config to {conf}')
        self.set_config_(conf)
        return JSONResponse(content={'text':'OK'})
    
    async def recognize(self, file_content : BytesObject, suf: str) -> ListOfStringsObject:
        logger.info(f'file_content {type(file_content)}, file suffix is {suf}')

        logger.info(f'current tesseract config is {self.ts_config}')
        text_dict = tu.bytes_handler(file_content, suf, self.ts_config)
        logger.info(f'img_bytes_handler return {type(text_dict)} object')
        return JSONResponse(content=text_dict)

    async def ner(self, txt: str): 
        sn = SpacyNER()
        if sn.available_models and len(sn.available_models) > 0:
            dummy_model = sn.available_models[0]
            sn.set_model(dummy_model)
        return JSONResponse(content=sn.extract_named_ents(txt))

# class ModelNameNotInList(BaseException):
#     def __init__(self, msg):
#         # pass
#         logger.exception(msg)


# class SpacyNER():
#     '''
#         Spacy NER service
#     '''
#     def __init__(self):
#         cfg = get_configuration()
#         self.available_models = set()
#         self.nlp = None

#         try:
#             for cur_model in cfg.spacy_models:
#                 logger.info(f'try to download model {cur_model} to {cfg.model_path}')
#                 # spacy.util.set_data_path(cfg.model_path)
#                 res = spacy.cli.download(cur_model)
#                 logger.info(f'result of spacy.cli.download is {res}')
#                 self.available_models.add(cur_model)
#         except Exception as e:
#             logger.error(f'catch exception {e}')
#             sys.exit()


#     def set_model(self, cur_model):
#         if cur_model not in self.available_models:
#             logger.error(f'there is not {cur_model} in available_models set: {self.available_models}')
#             self.nlp = None
#             raise ValueError(f'there is not {cur_model} in available_models set: {self.available_models}')

#         try:        
#             nlp = spacy.load(cur_model)
#             # nlp = spacy.load('en_default')
#             logger.info('spacy nlp object created with model {cur_model}')
#         except Exception as e:
#             logger.error(f'catch exception {e}')
#             if isinstance(e, OSError):                
#                 logger.error(f'you must download spacy model {cur_model}')
#             nlp = None
#             logger.info('spacy nlp object DID NOT create')
        
#         self.nlp = nlp


#     def extract_named_ents(self, txt: str):
#         logger.debug(f'got data type {type(txt)} and data <<{txt}>> for NER')
#         if self.nlp:
#             res = []
#             doc = self.nlp(txt)
#             for ent in doc.ents:
#                 res.append((ent.text,  ent.label_))
#             return JSONResponse(content=res)
#         else:
#             logger.error(f'nlp object didn`t create. you should use set_model(model_name)')
