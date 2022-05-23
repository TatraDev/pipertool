import os
import sys
import asyncio
import requests
root_dir = os.path.join(os.path.realpath(os.path.pardir), 'piper')
sys.path.insert(1, root_dir)

from piper.utils import docker_utils as du
from piper.utils import tesrct_utils as tu

from piper.envs import DockerEnv
from piper.envs import is_docker_env
from piper.configurations import get_configuration
from piper.services import TesseractRecognizer, StringValue
from pathlib import Path
import os
import pytest
import json


# service urls
headers = {"Content-Type": "application/json"}
main_app_url = f'http://localhost:8788'

url_tsrct_cfg = f'{main_app_url}/set_config'
url_rcg = f'{main_app_url}/recognize'

url_spacy_all_models = f'{main_app_url}/get_ner_models'
url_spacy_set_model = f'{main_app_url}/set_ner_model'
url_spacy_get_NE = f'{main_app_url}/extract_named_ents'

# folder info
file_path = Path(__file__).parent
# fn = file_path.joinpath('ocr_data.jpg')

SOURCE_FOLDER = file_path
OUTPUT_FOLDER = file_path.joinpath('out')

def get_available_models():
    try:
        result = requests.get(url_spacy_all_models, headers=headers)
        if result.status_code == 200:
            models = result.json()
            models = models.get('available_models')
            return models

    except Exception as e:
        print(f'error while get all models: {e}') 


def set_current_spacy_model(model):
    try:
        result = requests.post(url_spacy_set_model, headers=headers, data=json.dumps({'model_name':model}))    
        if result.status_code == 200:
            return True

    except Exception as e:
        print(f'error while set spacy model: {e}') 

def get_named_ent_from_text(txt):
    try:    
        result = requests.get(url_spacy_get_NE, headers=headers, data=json.dumps({'txt':txt}))
        if result.status_code == 200:        
            named_ents = result.json()
            # print(named_ents)
            if named_ents:
                named_ents = named_ents.get('result').get('body')
                named_ents = named_ents[2:-2].split('],[')
                return named_ents
                
    except Exception as e:
        print(f'error while extract named ents: {e}') 

def get_text_from_file(fn):
    try:
        result = tu.send_file_to_service(url_rcg, fn)
        if result.status_code == 200:  
            txt = result.json()
            txt = txt.get('text')
            return txt

    except Exception as e:
        print(f'error while extract text from file: {e}') 


def set_tesseract_config(conf):
    try:
        result = requests.post(url_tsrct_cfg, data=json.dumps(ts_conf), headers=headers)
        if result.status_code == 200:
            return True

    except Exception as e:
        print(f'error while set tesseract config: {e}') 

if __name__ == '__main__':

    available_models = get_available_models()
    print(f'get_ner_models {available_models}')

    ts_conf = dict()
    ts_conf['ts_lang'] = 'eng'

    for v in [6, 8, 11]:
        # change tesseract config
        ts_conf['ts_config_row'] = rf'--oem 1 --psm {v}'
        set_tesseract_config(ts_conf)
        print(f"\ttesseract config changed to {ts_conf['ts_config_row']}")

        for model in available_models:
            # change spacy model
            set_current_spacy_model(model)
            print(f"\t\tspacy model changed to {model}")

            # create output folder
            cur_dir = OUTPUT_FOLDER.joinpath(f'ts_{v}_{model}')
            cur_dir.mkdir(parents=True, exist_ok=True)
            for fn in file_path.iterdir():
                if fn.suffix[1:] in ['jpg', 'jpeg', 'png', 'pdf']:
                    # folder processing
                    txt = get_text_from_file(fn)
                    txt = ' '.join(txt)
                    print(f'\t\t\textracted text {txt}')

                    named_ents = get_named_ent_from_text(txt)

                    if named_ents:
                        named_ents_str = "\n".join(f'\t\t\t{x}' for x in named_ents)
                        # print(type(named_ents))
                        print(f'\t\t\textract_named_ents {named_ents_str}')

                        out_fn = cur_dir.joinpath(f'res_{fn.stem}.txt')
                        with open(out_fn, 'w') as f:
                            f.write(txt)
                            f.write('\t')
                            f.write(named_ents_str)
