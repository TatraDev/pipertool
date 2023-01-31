# pytest -vs tests/base_test.py::TestPiperBase
import asyncio

from piper.base.executors import FastAPIExecutor
from piper.services import StringValue
from piper.configurations import get_configuration
from piper.envs import CurrentEnv, DockerEnv

cfg = get_configuration()
loop = asyncio.get_event_loop()


class MessageAdder(FastAPIExecutor):

    def __init__(self, appender="TEST", **kwargs):
        self.appender = appender
        super().__init__(**kwargs)

    async def run(self, message: StringValue) -> StringValue:
        return StringValue(value=(message.value + self.appender))


class TestPiperBase:

    def test_simple_async_executors(self):
        init_value = "TEST_container_"
        x = StringValue(value=init_value)
        need_result = f'{init_value}TEST'

        with CurrentEnv() as env:
            adder = MessageAdder()
            result = loop.run_until_complete(adder.aio_call(x))
            assert result.value == need_result

        with DockerEnv() as env:
            adder = MessageAdder()
            result = loop.run_until_complete(adder.aio_call(x))
            adder.rm_container()
            assert result.get("value") == need_result

    def test_two_sync_executors(self):
        init_value = "TEST_container_"
        x = StringValue(value=init_value)
        need_result = f'{init_value}TESTTEST'

        with CurrentEnv() as env:
            adder_1 = MessageAdder()
            adder_2 = MessageAdder()
            result = adder_1(x)
            result = adder_2(result)

            assert result.value == need_result

        with DockerEnv() as env:
            adder_1 = MessageAdder()
            adder_2 = MessageAdder()
            result = adder_1(x)
            result = adder_2(result)

            assert result.get("value") == need_result
