import time


class Configuration:
    path: str = f"./applications/piper_project_{time.time_ns()}/"
    test_path: str = f"./applications/piper_project_{time.time_ns()}/"
    piper_path: str = "piper"
    templates_path: str = "templates"
    default_env: str = "compose"
    docker_app_port: int = 8788
    docker_build_timeout: int = 1000

    name_venv: str = "venv_test"
    number: int = 10

    env: str = None
    ignore_import_errors: bool = True
    safe_import_activated: bool = False

    # start time and counter
    wait_on_iter = 0.5
    n_iters = 10

    # docker start time and counter
    docker_wait_on_iter = 0.5
    docker_n_iters = 20

    n_gunicorn_workers = 1

    image_suffixes = set(['jpg', 'jpeg', 'png'])
    pdf_suffixes = set(['pdf'])

    # image to pdf settings
    thread_count = 4
    dpi = 160

    # tesseract available config options
    # OCR Engime mode OEM:
    # 0    Legacy engine only.
    # 1    Neural nets LSTM engine only.
    # 2    Legacy + LSTM engines.
    # 3    Default, based on what is available.
    available_OEM = [2, 3]

    # Page segmentation modes:
    # 0 Orientation and script detection (OSD) only.
    # 1 Automatic page segmentation with OSD.
    # 2 Automatic page segmentation, but no OSD, or OCR. (not implemented)
    # 3 Fully automatic page segmentation, but no OSD. (Default)
    # 4 Assume a single column of text of variable sizes.
    # 5 Assume a single uniform block of vertically aligned text.
    # 6 Assume a single uniform block of text.
    # 7 Treat the image as a single text line.
    # 8 Treat the image as a single word.
    # 9 Treat the image as a single word in a circle.
    # 10 Treat the image as a single character.
    # 11 Sparse text. Find as much text as possible in no particular order.
    # 12 Sparse text with OSD.
    # 13 Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.
    available_PSM = [6, 8, 11]

    # tesseract config
    ts_lang = 'eng'
    ts_config_row = r'--oem 1 --psm 11'
    ts_config = {'ts_lang': 'eng', 'ts_config_row': r'--oem 1 --psm 11'}

    # models and where to find them
    spacy_models = set(
        [
            'en_core_web_sm',
            # 'en_core_web_lg',
            # 'en_core_web_trf'
        ]
    )
    model_path = '/app/models'


def get_configuration():
    return Configuration
