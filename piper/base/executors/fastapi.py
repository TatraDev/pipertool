# from piper.base.docker import PythonTesseractImage
from piper.base.backend.utils import (render_fast_api_backend,
                                      render_fast_api_tsrct_backend)
from piper.base.docker import PythonImage
from piper.configurations import get_configuration
from piper.envs import get_env, is_current_env, is_docker_env, Env
from piper.utils import docker_utils
from piper.utils.logger_utils import logger
from piper.base.executors import HTTPExecutor

import asyncio
import inspect
import sys
import time
from abc import ABC, abstractmethod
from typing import Dict
from distutils.dir_util import copy_tree

import aiohttp
import docker
import requests
from pydantic import BaseModel  # , BytesObject, ListOfStringsObject


def add_packages_to_install(packages_list):
    row = f'RUN apt install -y {" ".join(packages_list)} \n'
    return row


def add_row(row):
    return f'{row} \n'


def copy_piper(path: str):
    cfg = get_configuration()
    copy_tree(cfg.piper_path, f"{path}piper")


def copy_scripts(path: str, scripts: Dict[str, str]):
    for script_name, script_path in scripts.items():
        with open(f"{path}/{script_name}.py", "w") as output:
            with open(script_path, "r") as current_file:
                output.write(current_file.read())


def write_requirements(path, requirements):
    with open(f"{path}/requirements.txt", "w") as output:
        output.write("\n".join(requirements))


def build_image(path: str, docker_image):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    image = docker_image.render()
    print(f"{path}Dockerfile")
    with open(f"{path}Dockerfile", "w") as output:
        output.write(image)

    image, logs = client.images.build(path=path,
                                      tag=docker_image.tag,
                                      quiet=False,
                                      timeout=20)
    for log in logs:
        logger.info(f'executor build_image: {log}')
    logger.info(f'image is {image}')


def run_container(image: str, ports: Dict[int, int]):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    container = client.containers.run(image, detach=True, ports=ports)
    for log in container.logs():
        logger.info(f'executor run_container: {log}')
    logger.info(f'container is {container}')
    time.sleep(10)

    return container


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
            logger.info(f'health_check status_code:{r.status_code}, reason:{r.reason}')
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
    requirements = ["gunicorn", "fastapi", "uvicorn", "aiohttp", "docker", "Jinja2", "pydantic", "loguru"]
    base_handler = "run"

    def __init__(self, port: int = 8080, **service_kwargs):
        self.container = None
        self.image_tag = 'piper:latest'
        self.id = hash(self)
        self.container_name = f"piper_FastAPI_{self.id}"

        if is_docker_env():
            docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
            cfg = get_configuration()
            project_output_path = cfg.path

            copy_piper(project_output_path)
            copy_scripts(project_output_path, self.scripts())
            self.create_fast_api_files(project_output_path, **service_kwargs)

            docker_image = PythonImage(self.image_tag, "3.9", cmd=f"./run.sh", template_file='default-python.j2',
                                       run_rows="", post_install_lines="")
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

            wait_for_fast_api_app_start('localhost', cfg.docker_app_port, cfg.wait_on_iter, cfg.n_iters)
        else:
            # TODO: Local ENVIRONMENT checks
            pass

        super().__init__('localhost', port, self.base_handler)

    async def aio_call(self, *args, **kwargs):
        return await super().__call__(*args, ** kwargs)

    def __call__(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.aio_call(*args, **kwargs))
        return result

    def rm_container(self):
        if self.container:
            self.container.remove(force=True)

    def scripts(self):
        return {"service": inspect.getfile(self.__class__)}

    def create_fast_api_files(self, path: str, **service_kwargs):
        cfg = get_configuration()

        backend = render_fast_api_backend(service_class=self.__class__.__name__,
                                          service_kwargs=dict(service_kwargs),
                                          scripts=self.scripts(),
                                          function_name=self.base_handler,
                                          request_model="StringValue",
                                          response_model="StringValue")
        with open(f"{path}/main.py", "w") as output:
            output.write(backend)

        write_requirements(path, self.requirements)

        gunicorn = "#!/bin/bash \n" \
                   f"gunicorn -b 0.0.0.0:8080 --workers {cfg.n_gunicorn_workers} main:app --worker-class uvicorn.workers.UvicornWorker --preload --timeout 120"
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