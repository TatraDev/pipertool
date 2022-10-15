# pytest -vs tests/base_test.py::TestPiperBase
import asyncio
import os
import sys
import time

root_dir = os.path.join(os.path.realpath(os.path.pardir), 'piper')
sys.path.insert(1, root_dir)


class TestPiperBase:

    def test_simple_executor(self):
        from piper.base.executors import FastAPIExecutor
        from piper.services import StringValue
        from piper.configurations import get_configuration
        from piper.envs import CurrentEnv, DockerEnv

        class TestMessageAdder(FastAPIExecutor):

            def __init__(self, appender="TEST", **kwargs):
                self.appender = appender
                super().__init__(**kwargs)

            async def run(self, message: StringValue) -> StringValue:
                return StringValue(value=(message.value + self.appender))

        cfg = get_configuration()
        loop = asyncio.get_event_loop()
        init_value = "TEST_container_"
        x = StringValue(value=init_value)
        need_result = f'{init_value}TEST'

        with CurrentEnv() as env:
            adder = TestMessageAdder(appender="!", port=cfg.docker_app_port)
            result = loop.run_until_complete(adder(x))
            print(result)
            assert result.get('value') == need_result

        with DockerEnv() as env:
            adder = TestMessageAdder(appender="!", port=cfg.docker_app_port)
            result = loop.run_until_complete(adder(x))
            print(result)
            adder.rm_container()
            assert result.get('value') == need_result

