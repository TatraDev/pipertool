from abc import abstractmethod
import os
import time

import aiohttp
import docker
from pydantic import BaseModel

from piper.base.docker import PythonImage
from piper.base.backend.utils import render_fast_api_backend


LOCAL_ENVIRONMENT = "local"
DOCKER_ENVIRONMENT = "docker"
ENVIRONMENT = DOCKER_ENVIRONMENT


class BaseExecutor:
    pass


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


def kwargs_to_dict(**kwargs):
    return {k: prepare(v) for k, v in kwargs.items() if is_known(v)}


class HTTPExecutor(BaseExecutor):

    def __init__(self, host: str, port: int, base_handler: str):
        self.host = host
        self.port = port

    @abstractmethod
    async def run(self, *args, **kwargs):
        pass

    async def __call__(self, *args, **kwargs):
        global ENVIRONMENT
        if ENVIRONMENT == LOCAL_ENVIRONMENT:
            return await self.run(*args, **kwargs)
        else:
            function = "run"
            request_dict = kwargs_to_dict(**kwargs)
            print(request_dict)
            async with aiohttp.ClientSession() as session:
                async with session.post(f'http://{self.host}:{self.port}/{function}', json=request_dict) as resp:
                    return await resp.json()


class LocalEnvironment:

    def __init__(self):
        global ENVIRONMENT
        self._old_environment = ENVIRONMENT
        ENVIRONMENT = LOCAL_ENVIRONMENT

    def __enter__(self):
        pass

    def __exit__(self, *args, **kws):
        global ENVIRONMENT
        ENVIRONMENT = self._old_environment


class FastAPIExecutor(HTTPExecutor):
    base_handler = "run"
    image_class = PythonImage

    @abstractmethod
    def scripts(self):
        pass

    def __init__(self, port: int = 8080, **kwargs):
        global ENVIRONMENT
        if ENVIRONMENT == DOCKER_ENVIRONMENT:
            path = '/Users/olegsokolov/PycharmProjects/piper/applications'

            from distutils.dir_util import copy_tree
            copy_tree("piper", f"{path}/piper")

            with open(f"{path}/executors.py", "w") as output:
                scripts = self.scripts()
                with open(scripts[0], "r") as current_file:
                    output.write(current_file.read())

            backend = render_fast_api_backend(executor_class=self.__class__.__name__,
                                              executor_args=dict(kwargs),
                                              function_name=self.base_handler,
                                              request_model="StringValue",
                                              response_model="StringValue")

            with open(f"{path}/main.py", "w") as output:
                output.write(backend)

            with open(f"{path}/requirements.txt", "w") as output:
                output.write("gunicorn\n"
                             "fastapi\n"
                             "uvicorn\n"
                             "aiohttp\n"
                             "docker\n"
                             "Jinja2\n"
                             "pydantic")


            gunicorn = "#!/bin/bash \n" \
                       "gunicorn -b 0.0.0.0:8080 --workers 4 main:app --worker-class uvicorn.workers.UvicornWorker --preload --timeout 120"
            with open(f"{path}/run.sh", "w") as output:
                output.write(gunicorn)

            image = self.image_class(python_docker_version="3.9", cmd=f"./run.sh").render()
            with open(f"{path}/Dockerfile", "w") as output:
                output.write(image)

            # image, logs = client.images.build(path=path, tag="piper:latest", quiet=False, timeout=20)
            # for log in logs:
            #     print(log)
            # print(image)
            client = docker.DockerClient(base_url='unix://var/run/docker.sock')
            container = client.containers.run("piper:latest", detach=True, ports={8080:  port})
            for log in container.logs():
                print(log)
            print(container)
            time.sleep(10)
        else:
            # Local ENVIRONMENT checks
            pass
        super().__init__('localhost', port, self.base_handler)
