from abc import abstractmethod

from piper.envs import get_env, is_current_env, Env
from piper.utils.logger_utils import logger


class BaseExecutor:
    """
    This class is main executor which you need
    to inherit to work with piper normally.
    This sync by default, but you can change
    to async and use __call__ with await.
    To create your child Executor just implement run
    for sync behavior or exec for async (set is_async)
    or implement both run and exec

    You can use prepared Executors like HTTPExecutor.
    Usually you don't need to control behavior for every environment.
    However you can do that properly for your custom Executor :

    class YourCustomExecutor(BaseExecutor):
        def run():
            x + x
        def docker_run():
            ... # your custom logic for docker env
        def compose_run():
            ... # your custom logic for compose env
        def custom_env_run():
            ... # for you own env
    """

    is_async: bool = False

    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError(f"run method not implemented in Executor {self}")

    @abstractmethod
    async def exec(self, *args, **kwargs):
        raise NotImplementedError(f"exec method not implemented in Executor {self}")

    def env_run(self, env: Env, *args, **kwargs):
        logger.debug(f"Executor {self} called with args {args} and kwargs {kwargs} in env {env}")
        if is_current_env():
            return self.run(*args, **kwargs)
        else:
            env_run_name = f"{env.name}_run"
            return getattr(self, env_run_name)(*args, **kwargs)

    async def env_exec(self, env: Env, *args, **kwargs):
        logger.debug(f"Executor {self} called with args {args} and kwargs {kwargs} in env {env}")
        if is_current_env():
            return await self.exec(*args, **kwargs)
        else:
            env_run_name = f"{env.name}_exec"
            return await getattr(self, env_run_name)(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        logger.debug(f"Executor {self} called with args {args} and kwargs {kwargs}")
        if self.is_async:
            return self.env_exec(get_env(), *args, **kwargs)
        else:
            return self.env_run(get_env(), *args, **kwargs)
