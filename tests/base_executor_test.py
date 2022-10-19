import asyncio
import pytest

from piper.envs import CurrentEnv, Env
from piper.base.executors import BaseExecutor


class ExecutorImpl(BaseExecutor):
    def run(self, x: int) -> int:
        return x + 1
    async def exec(self, x: int) -> int:
        return x - 1


inst = ExecutorImpl()
loop = asyncio.get_event_loop()


class TestBaseExecutorClass:

    def test_executor_not_async(self):
        assert not inst.is_async

    def test_executor_run(self):
        with CurrentEnv():
            assert inst(10) == 11

    def test_executor_exec_error(self):
        inst.is_async = True
        # it is coroutine must be an error here
        with pytest.raises(Exception):
            result = inst.exec(10)
            result + 1
        inst.is_async = False

    def test_executor_exec(self):
        inst.is_async = True
        with CurrentEnv():
            assert loop.run_until_complete(inst(10)) == 9
        inst.is_async = False

    def test_custom_env_run(self):
        class CustomEnv(Env):
            name = "custom_env"

        with CustomEnv():
            with pytest.raises(Exception):
                inst(10)

            # add implementation
            inst.custom_env_run = lambda x: x * 10
            assert inst(10) == 100
