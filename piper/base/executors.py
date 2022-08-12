import inspect
import os
import subprocess
import sys
import time
from abc import abstractmethod
from typing import Dict

import aiohttp
import docker
import requests
from pydantic import BaseModel

from piper.base.backend.utils import render_fast_api_backend
from piper.base.virtualenv.utils import VenvPython
from piper.configurations import get_configuration
from piper.envs import get_env, is_current_env, is_docker_env, is_virtual_env
from piper.utils import docker_utils as du
from piper.utils.logger_utils import logger


class BaseExecutor:
    def scripts(self):
        return {"service": inspect.getfile(self.__class__)}


class LocalExecutor:
    pass


def is_known(obj):
    basic = obj.__class__.__name__ in {'dict', 'list', 'tuple', 'str', 'int', 'float', 'bool'}
    models = isinstance(obj, (BaseModel,))
    return basic or models


def prepare(obj):
    if isinstance(obj, (BaseModel,)):
        return obj.dict()
    return obj


def inputs_to_dict(*args, **kwargs):
    from_args = {}
    for arg in args:
        if is_known(arg):
            from_args.update(prepare(arg))
    from_kwargs = {k: prepare(v) for k, v in kwargs.items() if is_known(v)}
    from_args.update(from_kwargs)
    return from_args


class HTTPExecutor(BaseExecutor):

    def __init__(self, host: str, port: int, base_handler: str):
        self.host = host
        self.port = port

    @abstractmethod
    async def run(self, *args, **kwargs):
        pass

    async def __call__(self, *args, **kwargs):
        print('get_env()', get_env())
        print('is_current_env()', is_current_env())
        if is_current_env():
            return await self.run(*args, **kwargs)
        else:
            function = "run"
            request_dict = inputs_to_dict(*args, **kwargs)
            print('request_dict', request_dict)
            async with aiohttp.ClientSession() as session:
                async with session.post(f'http://{self.host}:{self.port}/{function}', json=request_dict) as resp:
                    return await resp.json()


def copy_piper(path: str):
    cfg = get_configuration()
    from distutils.dir_util import copy_tree
    copy_tree(cfg.piper_path, f"{path}/piper")


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
    with open(f"{path}/Dockerfile", "w") as output:
        output.write(image)

    image, logs = client.images.build(path=path,
                                      tag=docker_image.tag,
                                      quiet=False,
                                      timeout=20)
    for log in logs:
        print(log)
    print(image)


def run_container(image: str, ports: Dict[int, int]):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    container = client.containers.run(image, detach=True, ports=ports)
    for log in container.logs():
        print(log)
    print(container)
    time.sleep(10)

    return container


def wait_for_fast_api_app_start(host, external_port, wait_on_iter, n_iters):
    '''
        wait for fast api app will be loaded
        external_port - 
        wait_on_iter - seconds between health_check requests
        n_iters - total health_check requests
    '''
    logger.info('waiting for FastAPI app start')
    i = 0
    while True:
        try:
            r = requests.post(f"http://{host}:{external_port}/health_check/")
            print(r.status_code, r.reason)
            if r.status_code == 200:
                break
        except Exception as e:
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
        self.container_name = "piper_FastAPI"

        if is_docker_env():
            logger.info('FastAPIExecutor init with is_docker_env()')

            docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
            cfg = get_configuration()
            project_output_path = cfg.path

            copy_piper(project_output_path)
            copy_scripts(project_output_path, self.scripts())

            self.create_fast_api_files(project_output_path, **service_kwargs)

            # create and run docker container
            # if container exits it will be recreated!
            du.create_image_and_container_by_dockerfile(
                docker_client,
                project_output_path,
                self.image_tag,
                self.container_name,
                port
            )

            wait_for_fast_api_app_start('localhost', 8788, 0.5, 10)

        # a = super().__init__('localhost', port, 'hl')
        # a.__call__()
        # print('hl', a)

        super().__init__('localhost', port, self.base_handler)

    def rm_container(self):
        if self.container:
            self.container.remove(force=True)

    def create_fast_api_files(self, path: str, **service_kwargs):
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
                   "gunicorn -b 0.0.0.0:8080 --workers 4 main:app --worker-class uvicorn.workers.UvicornWorker " \
                   "--preload --timeout 120 "
        with open(f"{path}/run.sh", "w") as output:
            output.write(gunicorn)


class VirtualEnvExecutor(BaseExecutor):
    requirements = ["gunicorn", "fastapi", "uvicorn", "aiohttp", "docker", "Jinja2", "pydantic", "loguru"]

    def __init__(self):
        if is_virtual_env():
            logger.info('VirtualEnvExecutor init with is_virtual_env()')

            cfg = get_configuration()
            project_output_path = cfg.path
            name_venv = cfg.name_venv
            number = cfg.number

            copy_piper(project_output_path)
            copy_scripts(project_output_path, self.scripts())

            self.create_files_for_venv(
                path=project_output_path,
                name_venv=name_venv,
                number=number,
            )

            VirtualEnvExecutor.create_files_for_tests(
                path=project_output_path,
                name_venv=name_venv,
                number=number,
            )

    def create_files_for_venv(
            self,
            path: str,
            name_venv: str,
            number: int,
    ):
        logger.info('VirtualEnvExecutor create_fast_api_files_venv()')

        venv_python_image = VenvPython(
            name_path=path,
            name_venv=name_venv,
            number=number,
        )

        venv_main = venv_python_image.render_venv_python()
        with open(f"{path}/main.py", "w") as output:
            output.write(venv_main)

        venv_bash = venv_python_image.render_venv_bash()
        with open(f"{path}/create_venv.sh", "w") as output:
            output.write(venv_bash)

        write_requirements(path, self.requirements)

        process_chmod = subprocess.run(f'chmod +x {path}create_venv.sh', shell=True)
        process_run = subprocess.run(f'{path}create_venv.sh', shell=True)

    @staticmethod
    def create_files_for_tests(
            path: str,
            name_venv: str,
            number: int,
    ):
        logger.info('VirtualEnvExecutor create_files_for_tests()')

        with open(f"{path}/__init__.py", "w") as output:
            pass

        tests_directory = f"{path}/tests"
        if not os.path.exists(tests_directory):
            os.makedirs(tests_directory)

        with open(f"{path}/tests/__init__.py", "w") as output:
            pass

        venv_python_image = VenvPython(
            name_path=path,
            name_venv=name_venv,
            number=number,
        )

        test_main = venv_python_image.render_tests_python()
        with open(f"{path}/tests/test_main.py", "w") as output:
            output.write(test_main)

        test_bash = venv_python_image.render_tests_bash()
        with open(f"{path}/test_venv.sh", "w") as output:
            output.write(test_bash)
