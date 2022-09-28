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

from PiperOperator import *

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


if __name__ == '__main__':

    piper_worker = PiperNLPWorker('http://localhost:8788')

    available_models = piper_worker.get_available_ner_models()
    print(f'get_ner_models {available_models}')

    ts_conf = dict()
    ts_conf['ts_lang'] = 'eng'

    for v in [6, 8, 11]:
        # change tesseract config
        ts_conf['ts_config_row'] = rf'--oem 1 --psm {v}'
        piper_worker.set_tesseract_config(ts_conf)
        print(f"\ttesseract config changed to {ts_conf['ts_config_row']}")

        for model in available_models:
            # change spacy model
            piper_worker.set_current_spacy_model(model)
            print(f"\t\tspacy model changed to {model}")

            # create output folder
            cur_dir = OUTPUT_FOLDER.joinpath(f'ts_{v}_{model}')
            cur_dir.mkdir(parents=True, exist_ok=True)
            for fn in file_path.iterdir():
                if fn.suffix[1:] in ['jpg', 'jpeg', 'png', 'pdf']:
                    # folder processing
                    txt = piper_worker.get_text_from_file(fn)
                    txt = ' '.join(txt)
                    print(f'\t\t\textracted text {txt}')

                    named_ents = piper_worker.get_named_ent_from_text(txt)

                    if named_ents:
                        named_ents_str = "\n".join(f'\t\t\t{x}' for x in named_ents)
                        # print(type(named_ents))
                        print(f'\t\t\textract_named_ents {named_ents_str}')

                        out_fn = cur_dir.joinpath(f'res_{fn.stem}.txt')
                        with open(out_fn, 'w') as f:
                            f.write(txt)
                            f.write('\t')
                            f.write(named_ents_str)
