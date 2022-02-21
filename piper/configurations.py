class Configuration:
    path = "/Users/olegsokolov/PycharmProjects/piper/applications"
    path = "/home/pavel/repo/piper_new_out/"
    test_path = "/home/pavel/repo/piper_test_out/"
    piper_path = "piper"
    default_env = "docker"
    docker_app_port = 8788
    env = None

    # start time and counter
    wait_on_iter = 0.5
    n_iters = 10

    n_gunicorn_workers = 1


def get_configuration():
    return Configuration
