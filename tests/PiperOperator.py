import requests
import json
import os
import sys
from pprint import pprint
from loguru import logger

# root_dir = os.path.realpath(os.path.pardir)
# logger.info(f'root dir is {root_dir}')
# sys.path.insert(1, root_dir)
# from piper.utils import tesrct_utils as tu


HEADERS = {"Content-Type": "application/json"}
NER_RESPONSE_KEY = 'body'

class PiperOperatorException(BaseException):
    def __init__(self, msg):
        pass
        # logger.exception(msg)
    


class FileLoadException(PiperOperatorException):
    def __init__(self, fn):
        self.fn = fn
        super().__init__(f'file {fn} can`t be loaded')    


class JSONGetKeyException(PiperOperatorException):
    def __init__(self, key):
        self.key = key
        super().__init__(f'can`t get JSON key {key}')    


class NoAvailableModelsException(PiperOperatorException):
    def __init__(self):
        super().__init__(f'there are no spacy models')


def get_data_by_key_from_response(cur_response, k):
    j = cur_response.json()
    if not j and k not in j.keys():
        raise JSONGetKeyException(k)
    v = j.get(k)
    return v

def get_data_by_key_from_url(url, key, post=True, data=None, file_name=""):    
    try:
        if post:
            if file_name:
                logger.info(f'filename is {file_name}')
                multipart_form_data = {
                    'file': open(file_name, 'rb')
                }
                cur_response = requests.post(url, files=multipart_form_data, verify=False)
            else:
                cur_response = requests.post(url, headers=HEADERS, data=data)

            logger.debug(f'url is {url}, response is {cur_response}, content is {cur_response.content}')
            cur_response.raise_for_status()
            if key:
                logger.debug(f'try to get value for key {key}')
                # pprint(cur_response.json())
                val = get_data_by_key_from_response(cur_response, key)
                logger.debug(f'value for key is {val}')
                return val
            else:
                return cur_response
            
        else:
            cur_response = requests.get(url, headers=HEADERS, data=data)
            cur_response.raise_for_status()
            # logger.debug(f'response is {cur_response.text}')
            val = get_data_by_key_from_response(cur_response, key)
            return val

    except requests.exceptions.ConnectionError as ce:
        logger.exception(f'can`t connect to url: {ce}')

    except JSONGetKeyException as cjke:
        logger.exception(f'can`t get key from response: {cjke}')

    except Exception as e:
        logger.exception(f'error while processing url {url}: {e}') 


class PiperNLPWorker():
    '''
        simple class shows how to use piper NLPProcessor
    '''

    def __init__(self, base_url):
        self.base_url = base_url

        ### RECOGNIZE
        self.url_tsrct_cfg = f'{self.base_url}/set_config'
        self.url_rcg = f'{self.base_url}/recognize'

        ### NER
        # get all available SPACY models url
        self.url_spacy_all_models = f'{self.base_url}/get_ner_models'
        # set current SPACY model url
        self.url_spacy_set_model = f'{self.base_url}/set_ner_model'
        # get named entitys from text url
        self.url_spacy_get_NE = f'{self.base_url}/extract_named_ents'


    def get_available_ner_models(self):
        return get_data_by_key_from_url(self.url_spacy_all_models, 'available_models', post=False)

    def set_current_spacy_model(self, model):
        return get_data_by_key_from_url(self.url_spacy_set_model, '', post=True, data=json.dumps({'model_name':model}))

    def get_named_ent_from_text(self, txt):
        resp = get_data_by_key_from_url(self.url_spacy_get_NE, 'result', post=False, data=json.dumps({'txt':txt}))
        logger.debug(f'url is {resp}, response is {resp}')
        if NER_RESPONSE_KEY in resp.keys():
            named_ents = resp.get(NER_RESPONSE_KEY)
            if named_ents:
                return json.loads(named_ents)
            else:
                logger.info(f'NER result is empty: {named_ents}')
                return []
        else:
            raise JSONGetKeyException(NER_RESPONSE_KEY)

    def get_text_from_file(self, fn):
        try:
            txt = get_data_by_key_from_url(self.url_rcg, 'text', post=True, file_name=fn)
            return txt

        except Exception as e:
            logger.error(f'error while extract text from file {fn}')
            logger.exception(e)

    def set_tesseract_config(self, conf):
        return get_data_by_key_from_url(self.url_tsrct_cfg, '', post=True, data=json.dumps(conf))

if __name__ == '__main__':
    piper_worker = PiperNLPWorker('http://localhost:8788')
    

    amodels = piper_worker.get_available_ner_models()
    print('all models', amodels)

    # model = amodels[0]
    model = 'en_core_web_sm'
    ok = piper_worker.set_current_spacy_model(model)
    # print(ok, ok.text)
    if ok:
        print('model set!')
    else:
        print('model does not set')
        sys.exit()

    txt = 'The Alraigo Incident occurred on 6th June 1983, when a lost British Royal Navy Sea Harrier fighter aircraft landed on the deck of a Spanish container ship.[1][2] Its pilot, Sub-lieutenant Ian Watson, was a junior Royal Navy Pilot undertaking his first NATO exercise from HMS Illustrious, which was operating off the coast of Portugal. Watson was launched in a pair of aircraft tasked with locating a French aircraft carrier under combat conditions including radio-silence and radar switched off.'
    try:
        resp = piper_worker.get_named_ent_from_text(txt)
    except JSONGetKeyException as e:
        logger.exception(e)
    # pprint(resp)


    txt = piper_worker.get_text_from_file('/home/pavel/repo/piper_new/piper/tests/ocr_data.pdf')
    logger.info(f'txt {txt}')


    ts_conf = dict()
    ts_conf['ts_lang'] = 'eng'
    ts_conf['ts_config_row'] = rf'--oem 1 --psm 6'

    resp = piper_worker.set_tesseract_config(ts_conf)
    logger.info(resp)
    
    
