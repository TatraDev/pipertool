# from piper.base.docker import PythonTesseractImage
from piper.base.backend.utils import (render_fast_api_backend,
                                      render_fast_api_tsrct_backend)
from piper.base.docker import PythonImage
from piper.configurations import get_configuration
from piper.envs import is_docker_env
from piper.utils import docker_utils
from piper.utils.logger_utils import logger
from piper.base.executors import HTTPExecutor
from piper.base.executors.utils import write_requirements, copy_piper, \
    copy_scripts, build_image, add_row, add_packages_to_install, get_free_port

import asyncio
import inspect
import sys
import time

import docker
import requests

cfg = get_configuration()


def wait_for_fast_api_app_start(host, external_port, wait_on_iter, n_iters):
    """
        wait for fast api app will be loaded
        external_port -
        wait_on_iter - seconds between health_check requests
        n_iters - total health_check requests
    """
    logger.info('waiting for FastAPI app start')
    i = 0
    while True:
        try:
            r = requests.post(f"http://{host}:{external_port}/health_check/")
            logger.info(f'health_check status_code:{r.status_code}, '
                        f'reason:{r.reason}')
            if r.status_code == 200:
                break
        except Exception as e:
            logger.error(f"Exception while starting FastAPI app {e}")
            time.sleep(wait_on_iter)

        if i == n_iters:
            logger.error('FastAPI app can`t start or n_iters too small')
            sys.exit()
        i += 1


class FastAPIExecutor(HTTPExecutor):
    requirements = ["gunicorn", "fastapi", "uvicorn", "aiohttp",
                    "docker", "Jinja2", "pydantic", "loguru"]
    base_handler = "run"

    def __init__(self, port: int = -1, **service_kwargs):
        self.container = None
        self.image_tag = 'piper:latest'
        self.id = hash(self)
        self.container_name = f"piper_FastAPI_{self.id}"

        if port < 0:
            port = get_free_port()
        self.port = port

        if is_docker_env():
            docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
            cfg = get_configuration()
            project_output_path = cfg.path

            copy_piper(project_output_path)
            copy_scripts(project_output_path, self.scripts())
            self.create_fast_api_files(project_output_path, **service_kwargs)

            docker_image = PythonImage(tag=self.image_tag,
                                       python_docker_version="3.9",
                                       cmd=f"./run.sh",
                                       template_file='default-python.j2',
                                       run_rows="",
                                       post_install_lines="")
            build_image(project_output_path, docker_image)

            # create and run docker container
            # if container exits it will be recreated!
            docker_utils.create_image_and_container_by_dockerfile(
                docker_client,
                project_output_path,
                self.image_tag,
                self.container_name,
                port
            )

            wait_for_fast_api_app_start('localhost', self.port, cfg.wait_on_iter, cfg.n_iters)
        else:
            # TODO: Local ENVIRONMENT checks
            pass

        super().__init__('localhost', port, self.base_handler)

    async def aio_call(self, *args, **kwargs):
        return await super().__call__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.aio_call(*args, **kwargs))
        return result

    def rm_container(self):
        if self.container:
            self.container.remove(force=True)

    def scripts(self):
        return {"service": inspect.getfile(self.__class__)}

    def get_func_input(self):
        import inspect

        sig = inspect.signature(self.__class__.run)
        sig_dict = dict()

        for param in list(sig.parameters):
            all_sig_parameters = str(sig.parameters[param]).split(': ')

            if len(all_sig_parameters) == 2:
                sig_dict[all_sig_parameters[0]] = all_sig_parameters[1]

        return sig_dict

    def create_fast_api_files(self, path: str, **service_kwargs):
        cfg = get_configuration()

        backend = render_fast_api_backend(service_class=self.__class__.__name__,
                                          service_kwargs=dict(service_kwargs),
                                          scripts=self.scripts(),
                                          function_name=self.base_handler,
                                          request_model=self.get_func_input(),
                                          response_model="StringValue")
        with open(f"{path}/main.py", "w") as output:
            output.write(backend)

        write_requirements(path, self.requirements)

        gunicorn = "#!/bin/bash \n" \
                   f"gunicorn -b 0.0.0.0:8080 --workers {cfg.n_gunicorn_workers} " \
                   f"main:app --worker-class uvicorn.workers.UvicornWorker --preload --timeout 120"
        with open(f"{path}/run.sh", "w") as output:
            output.write(gunicorn)


class FastAPITesseractExecutor(HTTPExecutor):
    requirements = ["gunicorn", "fastapi", "uvicorn", "aiohttp", "docker", "Jinja2", "pydantic", "loguru", "numpy",
                    "opencv-python", "pytesseract", "python-multipart", "pdf2image", "spacy"]
    packages_list = ['tree', 'cmake', 'libgl1-mesa-glx', 'poppler-utils', 'tesseract-ocr', 'libtesseract-dev',
                     'libleptonica-dev', 'mc']
    base_handler = "recognize"

    def __init__(self, port: int = 8080, **service_kwargs):
        self.container = None
        self.image_tag = 'piper:latest'
        self.container_name = "piper_FastAPITsrct"

        if is_docker_env():
            docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
            cfg = get_configuration()
            project_output_path = cfg.path

            copy_piper(project_output_path)
            copy_scripts(project_output_path, self.scripts())

            run_rows = ''
            run_rows += add_row('RUN apt update && apt install -y apt-transport-https')
            run_rows += add_row('RUN apt install -y software-properties-common')
            run_rows += add_packages_to_install(self.packages_list)
            run_rows += add_row('RUN pip3 install --upgrade pip')

            # скачивает сюда /usr/local/lib/python3.9/site-packages/en_core_web_sm
            # post_install_lines = f'RUN python3 -m spacy download {cfg.spacy_model} --data-path {cfg.model_path}'
            post_install_lines = ""

            # docker_image = PythonTesseractImage(self.image_tag, "3.9", cmd=f"./run.sh")
            docker_image = PythonImage(self.image_tag, "3.9", cmd=f"./run.sh", template_file='default-python.j2',
                                       run_rows=run_rows, post_install_lines=post_install_lines)
            build_image(project_output_path, docker_image)

            self.create_fast_api_files(project_output_path, **service_kwargs)

            # create and run docker container
            # if container exits it will be recreated!
            docker_utils.create_image_and_container_by_dockerfile(
                docker_client,
                project_output_path,
                self.image_tag,
                self.container_name,
                port
            )

            wait_for_fast_api_app_start('localhost', cfg.docker_app_port, cfg.wait_on_iter, cfg.n_iters)
        else:
            # TODO: Local ENVIRONMENT checks
            pass

        super().__init__('localhost', port, self.base_handler)

    def rm_container(self):
        if self.container:
            self.container.remove(force=True)

    def scripts(self):
        return {"service": inspect.getfile(self.__class__)}

    def create_fast_api_files(self, path: str, **service_kwargs):
        cfg = get_configuration()

        # TODO add support more than one functions
        backend = render_fast_api_tsrct_backend(
            service_class=self.__class__.__name__,
            service_kwargs=dict(service_kwargs),
            scripts=self.scripts(),
            function_name=self.base_handler,
            # request_model="BytesObject",
            # response_model="ListOfStringsObject"
        )

        with open(f"{path}/main.py", "w") as output:
            output.write(backend)

        write_requirements(path, self.requirements)

        gunicorn = "#!/bin/bash \n" \
                   f"gunicorn -b 0.0.0.0:8080 --workers {cfg.n_gunicorn_workers} main:app --worker-class uvicorn.workers.UvicornWorker --preload --timeout 120"
        with open(f"{path}/run.sh", "w") as output:
            output.write(gunicorn)
