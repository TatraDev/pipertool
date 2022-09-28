import imp
from piper.configurations import get_configuration
from loguru import logger

cfg = get_configuration()


def init_default_env():
    # INITIALIZE ENVIRONMENT FROM CONFIGURATION
    if cfg.default_env == "docker":
        set_env(DockerEnv())
    else:
        set_env(CurrentEnv())


def get_env():
    if cfg.env is None:
        init_default_env()
    return cfg.env


def set_env(env):
    logger.info("Setting environment to: {}".format(env))
    cfg.env = env


class DockerEnv:

    def __init__(self):
        pass

    def __enter__(self):
        logger.info("Docker context management __enter__")
        self._old_environment = get_env()
        set_env(self)

    def __exit__(self, *args, **kws):
        logger.info("Docker context management __exit__")
        set_env(self._old_environment)


class CurrentEnv:

    def __init__(self):
        pass

    def __enter__(self):
        logger.info("CurrentEnv context management __enter__")
        self._old_environment = get_env()
        set_env(self)

    def __exit__(self, *args, **kws):
        logger.info("CurrentEnv context management __exit__")
        set_env(self._old_environment)


def is_current_env():
    return get_env().__class__.__name__ == "CurrentEnv"


def is_docker_env():
    return get_env().__class__.__name__ == "DockerEnv"
