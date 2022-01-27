class Configuration:
    path = "/Users/olegsokolov/PycharmProjects/piper/applications"
    piper_path = "piper"
    default_env = "docker"
    env = None


def get_configuration():
    return Configuration
