class Configuration:
    path = "./piper_new_out/"
    piper_path = "piper"
    default_env = "virtualenv"
    name_venv = "venv_test"
    number = 10
    env = None


def get_configuration():
    return Configuration
