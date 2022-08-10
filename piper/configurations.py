class Configuration:
    path = "./piper_new_out/"
    piper_path = "piper"
    default_env = "virtualenv"
    name_venv = "venv_test"
    api_host = "0.0.0.0"
    env = None


def get_configuration():
    return Configuration
