from piper.base.docker_compose.compose_executors import ComposeExecutor
from piper.base.virtualenv.venv_executors import VirtualEnvExecutor
from piper.configurations import get_configuration
from piper.utils.logger_utils import logger

cfg = get_configuration()


def init_default_env():
    # INITIALIZE ENVIRONMENT FROM CONFIGURATION
    if cfg.default_env == "docker":
        set_env(DockerEnv())
    elif cfg.default_env == "virtualenv":
        set_env(VirtualEnv())
    elif cfg.default_env == "compose":
        set_env(VirtualEnv())
    else:
        set_env(CurrentEnv())


def get_env():
    if cfg.env is None:
        init_default_env()
    return cfg.env


def set_env(env):
    print("Setting environment to: {}".format(env))
    cfg.env = env


class DockerEnv:

    def __init__(self):
        pass

    def __enter__(self):
        print("Entering DockerEnv")
        self._old_environment = get_env()
        set_env(self)

    def __exit__(self, *args, **kws):
        print("Exiting DockerEnv")
        set_env(self._old_environment)


class CurrentEnv:

    def __init__(self):
        pass

    def __enter__(self):
        print("Entering CurrentEnv")
        self._old_environment = get_env()
        set_env(self)

    def __exit__(self, *args, **kws):
        print("Exiting CurrentEnv")
        set_env(self._old_environment)


class VirtualEnv:

    def __init__(self):
        self.__resource = VirtualEnvExecutor()

    def __enter__(self):
        logger.info("Entering VirtualEnv")
        self._old_environment = get_env()
        set_env(self)
        # TODO update work with return resource
        return self.__resource

    def __exit__(self, *args, **kws):
        logger.info("Exiting VirtualEnv")
        set_env(self._old_environment)


class ComposeEnv:

    def __init__(self):
        self.__resource = ComposeExecutor()

    def __enter__(self):
        logger.info("Entering ComposeEnv")
        self._old_environment = get_env()
        set_env(self)
        # TODO update work with return resource
        return self.__resource

    def __exit__(self, *args, **kws):
        logger.info("Exiting ComposeEnv")
        # self.__resource.stop_compose()
        set_env(self._old_environment)


def is_current_env():
    return get_env().__class__.__name__ == "CurrentEnv"


def is_docker_env():
    return get_env().__class__.__name__ == "DockerEnv"


def is_virtual_env():
    return get_env().__class__.__name__ == "VirtualEnv"


def is_compose_env():
    return get_env().__class__.__name__ == "ComposeEnv"
