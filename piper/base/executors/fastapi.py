# from piper.base.docker import PythonTesseractImage
from piper.base.backend.utils import (render_fast_api_backend,
                                      render_fast_api_tsrct_backend)
from piper.base.docker import PythonImage
from piper.configurations import get_configuration
from piper.envs import is_docker_env
from piper.utils import docker_utils
from piper.base.executors import HTTPExecutor
from piper.base.executors.utils import write_requirements, copy_piper, \
    copy_scripts, build_image, get_free_port, wait_for_fast_api_app_start
from piper.base.rendering.meta import ExecutorMetaInfo, Function, FunctionArg


import asyncio
import inspect

import docker

cfg = get_configuration()


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

    def create_fast_api_files(self, path: str, **service_kwargs):
        cfg = get_configuration()

        meta_info = ExecutorMetaInfo(
            class_name=self.__class__.__name__,
            init_kwargs=dict(service_kwargs),
            scripts=self.scripts(),
            async_functions=[Function(name=self.base_handler,
                                      input_args=[FunctionArg("request_model", "StringValue")])]
        )

        backend = render_fast_api_backend(meta_info)
        with open(f"{path}/main.py", "w") as output:
            output.write(backend)

        write_requirements(path, self.requirements)

        gunicorn = "#!/bin/bash \n" \
                   f"gunicorn -b 0.0.0.0:8080 --workers {cfg.n_gunicorn_workers} " \
                   f"main:app --worker-class uvicorn.workers.UvicornWorker --preload --timeout 120"
        with open(f"{path}/run.sh", "w") as output:
            output.write(gunicorn)
