from piper.configurations import get_configuration
from piper.utils.logger_utils import logger

import time
from typing import Dict
from distutils.dir_util import copy_tree
import subprocess

import docker


cfg = get_configuration()


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


def _build_image_old(path: str, docker_image):
    """
    deprecated:
    this doesn't stream logs from docker build
    TODO: fix it in build_image_old and use docker-py
    """
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    image = docker_image.render()

    with open(f"{path}Dockerfile", "w") as output:
        output.write(image)

    streamer = client.build(path=path,
                            decode=True,
                            tag=docker_image.tag,
                            quiet=False,
                            buildargs={"progress": "plain"},
                            timeout=cfg.docker_build_timeout)
    for chunk in streamer:
        logger.info(chunk)

    logger.info(f'piper built image {docker_image.tag}')


def build_image(path: str, docker_image):
    """
    Build docker image
    OLD build_image_old doesn't stream logs from docker build
    TODO: fix it in build_image_old and use docker-py instead of Popen
    """
    image = docker_image.render()

    with open(f"{path}Dockerfile", "w") as output:
        output.write(image)
    cmd = ['docker', 'build',  "--progress", "plain", '-t', docker_image.tag, path]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    with process.stdout:
        for line in iter(process.stdout.readline, b''):
            logger.info(line)

    logger.info(f'piper built image {docker_image.tag}')


def run_container(image: str, ports: Dict[int, int]):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    container = client.containers.run(image, detach=True, ports=ports)
    for log in container.logs():
        logger.info(f'executor run_container: {log}')
    logger.info(f'container is {container}')
    time.sleep(10)

    return container
