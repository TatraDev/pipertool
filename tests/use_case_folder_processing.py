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

# service url
main_app_url = f'http://localhost:8788'

# folder info
file_path = Path(__file__).parent
# fn = file_path.joinpath('ocr_data.jpg')

SOURCE_FOLDER = file_path
OUTPUT_FOLDER = file_path.joinpath('out')


if __name__ == '__main__':
    cfg = get_configuration()

    # PiperWorker instanse
    piper_worker = PiperNLPWorker(main_app_url)

    available_models = piper_worker.get_available_ner_models()
    logger.info(f'available models are {available_models}')

    ts_conf = dict()
    ts_conf['ts_lang'] = 'eng'

    for oem in cfg.available_OEM: 
        for psm in cfg.available_PSM:
            # change tesseract config
            ts_conf['ts_config_row'] = rf'--oem {oem} --psm {psm}'
            piper_worker.set_tesseract_config(ts_conf)
            logger.info(f"\ttesseract config changed to {ts_conf['ts_config_row']}")

            for model in available_models:
                # change spacy model
                piper_worker.set_current_spacy_model(model)
                logger.info(f"\t\tspacy model changed to {model}")

                # create output folder
                cur_dir = OUTPUT_FOLDER.joinpath(f'oem_{oem}_psm_{psm}_{model}')
                cur_dir.mkdir(parents=True, exist_ok=True)
                for fn in file_path.iterdir():
                    if fn.suffix[1:] in ['jpg', 'jpeg', 'png', 'pdf']:
                        # folder processing
                        txt = piper_worker.get_text_from_file(fn)
                        if txt:
                            txt = ' '.join(txt)
                            logger.info(f'\t\t\textracted text {txt}')

                            out_fn = cur_dir.joinpath(f'res_{fn.stem}.txt')
                            with open(out_fn, 'w') as f:
                                f.write(txt)

                            logger.debug(f'get NEs from text: {txt}')
                            named_ents = piper_worker.get_named_ent_from_text(txt)
                            logger.debug(f'NEs are: {named_ents}')

                            if named_ents:
                                named_ents_str = "\n".join(f'\t\t\t{x}' for x in named_ents)
                                logger.info(f'\t\t\textract_named_ents {named_ents_str}')

                                # out_fn = cur_dir.joinpath(f'res_{fn.stem}.txt')
                                with open(out_fn, 'a') as f:
                                    f.write('\n')
                                    f.write(named_ents_str)
                        else:
                            logger.info(f'\t\t\tNO extracted text')
