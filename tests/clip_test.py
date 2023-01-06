# pytest -vs tests/base_test.py::TestPiperBase
import asyncio

from piper.base.executors import FastAPIExecutor
from piper.services import StringValue, ListOfStringsObject
from piper.configurations import get_configuration
from piper.envs import CurrentEnv, DockerEnv

from piper.base.executors.clip import CLIPExecutor

cfg = get_configuration()
loop = asyncio.get_event_loop()


class TestPiperBase:

    def test_simple_async_executors(self):
        init_value_url = "https://cdn.kanobu.ru/games/f8ffb106-1d6b-497c-8b12-3943d570ddc3.jpg"
        init_value_text_snippets = ["hulk", "iron men", "black widow", "avengers"]
        x = StringValue(value=init_value_url)
        y = ListOfStringsObject(value=init_value_text_snippets)
        need_result = str([('hulk', 0.002), ('iron men', 0.024), ('black widow', 0.0), ('avengers', 0.974)])

        with CurrentEnv() as env:
            adder = CLIPExecutor(port=cfg.docker_app_port)
            result = loop.run_until_complete(adder.aio_call(x, y))
            
            assert result == need_result

        with DockerEnv() as env:
            adder = CLIPExecutor(port=cfg.docker_app_port)
            result = loop.run_until_complete(adder.aio_call(x, y))
            adder.rm_container()
            # assert result.get("value") == need_result
            assert result == need_result
            