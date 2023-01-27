# from piper.base.docker import PythonTesseractImage
from piper.base.backend.utils import render_fast_api_tsrct_backend
from piper.base.docker import PythonImage
from piper.configurations import get_configuration
from piper.envs import is_docker_env
from piper.utils import docker_utils
from piper.base.executors import HTTPExecutor
from piper.base.executors.utils import write_requirements, copy_piper, \
    copy_scripts, build_image, add_row, add_packages_to_install, wait_for_fast_api_app_start

import inspect

import docker

cfg = get_configuration()


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
