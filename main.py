from piper.services import TestMessageAdder, StringValue
from piper.envs import CurrentEnv

import asyncio
from loguru import logger
logger.add("file.log", level="INFO")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    with CurrentEnv() as env:
        x = StringValue(value="hello, world")
        adder = TestMessageAdder(appender="!", port=8788)
        result = loop.run_until_complete(adder(x))
        print(result)

    x = StringValue(value="hello, world")
    adder = TestMessageAdder(appender="!", port=8788)
    result = loop.run_until_complete(adder(x))
    print(result)
    adder.rm_container()
