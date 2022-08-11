import asyncio

from piper.base.executors import VirtualEnvExecutor
from piper.envs import VirtualEnv
from piper.services import StringValue, TestMessageAdder


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     with VirtualEnv() as env:
#         x = StringValue(value="hello, world")
#         adder = TestMessageAdder(appender="!", port=8788)
#         result = loop.run_until_complete(adder(x))
#         print(result)
#
#     x = StringValue(value="hello, world")
#     adder = TestMessageAdder(appender="!", port=8788)
#     result = loop.run_until_complete(adder(x))
#     print(result)
#     adder.rm_container()

if __name__ == '__main__':
    with VirtualEnv() as env:
        adder = VirtualEnvExecutor()
