from piper.base.docker_compose.compose_executors import ComposeExecutor
from piper.base.virtualenv.venv_executors import VirtualEnvExecutor
from piper.configurations import get_configuration
from piper.utils.logger_utils import logger

cfg = get_configuration()


def init_default_env():
    """
    This method initialize the default environment by the string name from the configuration.
    CurrentEnv means default python where piper is installed.
    """
    if cfg.default_env == "docker":
        set_env(DockerEnv())
    elif cfg.default_env == "virtualenv":
        set_env(VirtualEnv())
    elif cfg.default_env == "compose":
        set_env(ComposeEnv())
    else:
        set_env(CurrentEnv())


def get_env():
    if cfg.env is None:
        init_default_env()
    return cfg.env


def set_env(env):
    print("Setting environment to: {}".format(env))
    cfg.env = env


class Env:
    name = "no_env"

    _subclasses = []

    def __enter__(self):
        logger.info(f"Entering Env: {self.__class__.__name__}")
        self._old_environment = get_env()
        set_env(self)

    def __exit__(self, *args, **kws):
        logger.info(f"Exit Env: {self.__class__.__name__}")
        set_env(self._old_environment)

    @classmethod
    def get_all_envs(cls):
        return list(cls._subclasses)

    def __init_subclass__(cls):
        Env._subclasses.append(cls)


class DockerEnv(Env):
    name = "docker"

    def __init__(self):
        pass


class CurrentEnv(Env):
    name = "current_env"

    def __init__(self):
        pass


class VirtualEnv(Env):
    name = "virtualenv"

    def __init__(self):
        self.__resource = VirtualEnvExecutor()

    def __enter__(self):
        super().__enter__()
        return self.__resource


class ComposeEnv(Env):
    name = "compose"

    def __init__(self):
        self.__resource = ComposeExecutor()

    def __enter__(self):
        super().__enter__()
        return self.__resource

    def __exit__(self, *args, **kws):
        super().__exit__(* args, ** kws)
        # self.__resource.stop_compose()


def is_current_env():
    return get_env().__class__.__name__ == "CurrentEnv"


def is_docker_env():
    return get_env().__class__.__name__ == "DockerEnv"


def is_virtual_env():
    return get_env().__class__.__name__ == "VirtualEnv"


def is_compose_env():
    return get_env().__class__.__name__ == "ComposeEnv"
