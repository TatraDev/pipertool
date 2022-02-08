from piper.services import TestMessageAdder, StringValue
from piper.envs import CurrentEnv
from piper.configurations import get_configuration

import asyncio
from loguru import logger
logger.add("file.log", level="INFO", backtrace=True, diagnose=True, rotation='5 MB')

if __name__ == '__main__':
    cfg = get_configuration()
    loop = asyncio.get_event_loop()
    with CurrentEnv() as env:
        x = StringValue(value="hello, world")
        adder = TestMessageAdder(appender="!", port=cfg.docker_app_port)
        result = loop.run_until_complete(adder(x))
        print(result)

    x = StringValue(value="hello, world")
    adder = TestMessageAdder(appender="!", port=cfg.docker_app_port)
    result = loop.run_until_complete(adder(x))
    print(result)
    adder.rm_container()
