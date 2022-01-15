from piper.services import TestMessageAdder, StringValue
from piper.base.executors import LocalEnvironment

import asyncio

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    with LocalEnvironment() as env:
        x = StringValue(value="hello, world")
        adder = TestMessageAdder(appender="!", port=8788)
        result = loop.run_until_complete(adder(x))
        print(result)

    x = StringValue(value="hello, world")
    adder = TestMessageAdder(appender="!", port=8788)
    result = loop.run_until_complete(adder(x))
    print(result)
