from piper.configurations import get_configuration

cfg = get_configuration()


def init_default_env():
    # INITIALIZE ENVIRONMENT FROM CONFIGURATION
    if cfg.default_env == "docker":
        set_env(DockerEnv())
    elif cfg.default_env == "virtualenv":
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


class VirtualEnv:

    def __init__(self):
        pass

    def __enter__(self):
        print("Entering VirtualEnv")
        self._old_environment = get_env()
        set_env(self)

    def __exit__(self, *args, **kws):
        print("Exiting VirtualEnv")
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


def is_current_env():
    return get_env().__class__.__name__ == "CurrentEnv"


def is_docker_env():
    return get_env().__class__.__name__ == "DockerEnv"


def is_virtual_env():
    return get_env().__class__.__name__ == "VirtualEnv"
