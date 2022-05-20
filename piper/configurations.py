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

    image_suffixes = set(['jpg', 'jpeg', 'png'])
    pdf_suffixes = set(['pdf'])

    # image to pdf settings
    thread_count = 4
    dpi = 160

    # models and where to find them
    # spacy_model = 'en_core_web_lg'
    spacy_model = 'en_core_web_sm'
    model_path = '/app/models'

def get_configuration():
    return Configuration
