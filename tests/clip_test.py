# pytest -vs tests/base_test.py::TestPiperBase
import asyncio


from piper.services import StringValue
from piper.configurations import get_configuration
from piper.envs import CurrentEnv, DockerEnv

from piper.base.executors.clip import CLIPExecutor

cfg = get_configuration()
loop = asyncio.get_event_loop()


class TestPiperBase:

    def test_simple_async_executors(self):
        init_value_url = "https://cdn.kanobu.ru/games/f8ffb106-1d6b-497c-8b12-3943d570ddc3.jpg"
        init_value_text_snippets = ["hulk", "iron man", "black widow", "avengers"]
        x = StringValue(value=str([init_value_url, init_value_text_snippets]))
        
        need_result = str([('hulk', 0.002), ('iron man', 0.01), ('black widow', 0.0), ('avengers', 0.988)])

        with CurrentEnv() as env:
            adder = CLIPExecutor(port=cfg.docker_app_port)
            result = loop.run_until_complete(adder.aio_call(x))
            result = result.dict()
            
            assert result.get("value") == need_result

        with DockerEnv() as env:
            adder = CLIPExecutor(port=cfg.docker_app_port)
            result = loop.run_until_complete(adder.aio_call(x))
            adder.rm_container()
            
            assert result.get("value") == need_result
            
            