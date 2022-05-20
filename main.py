from piper.services import TestMessageAdder, StringValue, TesseractRecognizer, SpacyNER
from piper.envs import CurrentEnv, DockerEnv
from piper.configurations import get_configuration
import time
import asyncio
from loguru import logger
logger.add("file.log", level="INFO", backtrace=True, diagnose=True, rotation='5 MB')

if __name__ == '__main__':
    # cfg = get_configuration()
    # loop = asyncio.get_event_loop()
    # with CurrentEnv() as env:
    #     x = StringValue(value="hello, world")
    #     adder = TestMessageAdder(appender="!", port=cfg.docker_app_port)
    #     result = loop.run_until_complete(adder(x))
    #     print(result)

    # x = StringValue(value="hello, world") 
    # adder = TestMessageAdder(appender="!", port=cfg.docker_app_port)
    # result = loop.run_until_complete(adder(x))
    # print(result)
    # adder.rm_container()

    logger.info(f'main here {time.time()}')
    cfg = get_configuration()
    loop = asyncio.get_event_loop()
    with DockerEnv() as env:
        recognizer = TesseractRecognizer(port=cfg.docker_app_port)
        result = loop.run_until_complete(recognizer())
        logger.info(f'result of recognition is {result}')

        sn = SpacyNER()
        txt = 'The Alraigo Incident occurred on 6th June 1983, when a lost British Royal Navy Sea Harrier fighter aircraft landed on the deck of a Spanish container ship.[1][2] Its pilot, Sub-lieutenant Ian Watson, was a junior Royal Navy Pilot undertaking his first NATO exercise from HMS Illustrious, which was operating off the coast of Portugal. Watson was launched in a pair of aircraft tasked with locating a French aircraft carrier under combat conditions including radio-silence and radar switched off.'
        # switch models
        for avalable_model in sn.available_models:
            logger.info(f'current model is {avalable_model}')
            sn.set_model(avalable_model)
            result1 = sn.extract_named_ents(txt)
            if result1:
                result1_str = "\n".join(str(x) for x in result1)
                logger.info(f'result of NER for model {avalable_model} is {result1_str}')
            else:
                logger.info(f'module didn`t get NER data')
